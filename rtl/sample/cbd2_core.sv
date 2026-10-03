`default_nettype none
`timescale 1ns/1ps
// rtl/sample/cbd2_core.sv
// Phase 8b (docs/evidence/phase08-keccak-stream/8b/test_plan_8b.md section 1): SamplePolyCBD_2 (FIPS 203 Algorithm 8, eta = 2) straight from a 64-bit word stream. OUTW = 1 (stage W1): one coefficient per cycle
// (256 cycles); OUTW = 2 (stage W2): one byte, i.e. two coefficients (lane 0 = even index), per cycle (128 cycles).
// Coefficient i uses stream bits 4i .. 4i+3: x = bit0 + bit1, y = bit2 + bit3, f = x - y mod 3329 (values 3327, 3328, 0, 1, 2); the word holds 16 coefficients, nibble 0 first (byte k gives 2k, 2k+1).
// Exactly 16 words are taken (128 bytes). Control never looks at the data: the cycle count is the same for every input (the stream's own timing aside), no branch, address or loop depends on a stream bit.
// The word register and the output register are cleared on the last handover, on abort_i, on start and on reset (the stream holds secret bytes). done_o is a one-cycle pulse after the last handover.
// Reset: asynchronous, active low. One clock domain, clk_i.

module cbd2_core #(
    parameter int OUTW = 1  // coefficients per output beat: 1 (stage W1) or 2 (stage W2)
) (
    input  wire        clk_i,
    input  wire        rst_ni,
    input  wire        start_i,       // accepted when not busy
    input  wire        abort_i,
    input  wire        in_valid_i,
    output wire        in_ready_o,
    input  wire [63:0] in_data_i,
    output wire        coef_valid_o,
    input  wire        coef_ready_i,
    output wire [12*OUTW-1:0] coef_data_o,
    output wire        coef_last_o,
    output wire [15:0] bytes_o,       // stream bytes taken: 8 per word
    output wire        busy_o,
    output wire        fin_o,         // level: all 256 coefficients are generated
    output wire        done_o         // pulse: the last coefficient was handed over
);

  localparam logic [11:0] QC = 12'd3329;  // FIPS 203 q (locked, C1); not named Q so that it does not hide ntt_pkg::Q where both are compiled together

  logic        busy_q, fin_q, done_q;
  logic        wv_q;  // the word register holds a word
  logic [63:0] w_q;
  logic [ 3:0] nib_q;
  logic [ 4:0] wcnt_q;  // words taken, 0..16
  logic [ 8:0] n_q;  // coefficients generated, 0..256
  logic        ov_q, ol_q;
  logic [12*OUTW-1:0] od_q;

  function automatic logic [11:0] cbd_f(input logic [3:0] nb);
    logic [1:0] x, y;
    x = {1'b0, nb[0]} + {1'b0, nb[1]};
    y = {1'b0, nb[2]} + {1'b0, nb[3]};
    if (x >= y) cbd_f = {10'd0, x - y};
    else cbd_f = QC - {10'd0, y - x};
  endfunction

  wire slot_free = !ov_q || coef_ready_i;
  wire emit = busy_q && !fin_q && wv_q && slot_free;
  wire e_last = emit && (n_q == 9'(256 - OUTW));  // the beat that holds the 256th coefficient
  wire last_nib = (nib_q == 4'(16 - OUTW));  // the last nibble (W1) or nibble pair (W2) of the word
  wire start_ok = start_i && !busy_q;
  wire hand = ov_q && coef_ready_i;
  wire done_ev = hand && ol_q;

  assign in_ready_o = busy_q && !fin_q && (wcnt_q < 5'd16) && (!wv_q || (emit && last_nib));
  wire take = in_valid_i && in_ready_o;

  wire [3:0] nb = w_q[{nib_q, 2'b00}+:4];  // nibble 2k (W2: the lower of the pair)
  wire [3:0] nb_hi = w_q[{nib_q + 4'd1, 2'b00}+:4];  // W2: nibble 2k + 1
  wire [12*OUTW-1:0] e_data = (OUTW == 1) ? (12*OUTW)'(cbd_f(nb)) : (12*OUTW)'({cbd_f(nb_hi), cbd_f(nb)});

  assign coef_valid_o = ov_q;
  assign coef_data_o = od_q;
  assign coef_last_o = ov_q && ol_q;
  assign bytes_o = {8'd0, wcnt_q, 3'b000};
  assign busy_o = busy_q;
  assign fin_o = fin_q;
  assign done_o = done_q;

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      busy_q <= 1'b0;
      fin_q  <= 1'b0;
      done_q <= 1'b0;
      wv_q   <= 1'b0;
      w_q    <= 64'd0;
      nib_q  <= 4'd0;
      wcnt_q <= 5'd0;
      n_q    <= 9'd0;
      ov_q   <= 1'b0;
      ol_q   <= 1'b0;
      od_q   <= '0;
    end else begin
      done_q <= 1'b0;
      if (abort_i) begin
        busy_q <= 1'b0;
        fin_q  <= 1'b0;
        wv_q   <= 1'b0;
        w_q    <= 64'd0;
        nib_q  <= 4'd0;
        ov_q   <= 1'b0;
        ol_q   <= 1'b0;
        od_q   <= '0;
      end else begin
        if (start_ok) begin
          busy_q <= 1'b1;
          fin_q  <= 1'b0;
          wv_q   <= 1'b0;
          w_q    <= 64'd0;
          nib_q  <= 4'd0;
          wcnt_q <= 5'd0;
          n_q    <= 9'd0;
          ov_q   <= 1'b0;
          ol_q   <= 1'b0;
        end
        if (done_ev) begin
          busy_q <= 1'b0;
          fin_q  <= 1'b0;
          done_q <= 1'b1;
          ov_q   <= 1'b0;
          ol_q   <= 1'b0;
          od_q   <= '0;
        end else if (emit) begin
          ov_q <= 1'b1;
          od_q <= e_data;
          ol_q <= e_last;
        end else if (hand) begin
          ov_q <= 1'b0;
        end
        if (emit) n_q <= n_q + 9'(OUTW);
        if (e_last) begin
          fin_q <= 1'b1;
          wv_q  <= 1'b0;
          w_q   <= 64'd0;
          nib_q <= 4'd0;
        end else if (take) begin
          wv_q   <= 1'b1;
          w_q    <= in_data_i;
          nib_q  <= 4'd0;
          wcnt_q <= wcnt_q + 5'd1;
        end else if (emit) begin
          nib_q <= nib_q + 4'(OUTW);
          if (last_nib) wv_q <= 1'b0;
        end
      end
    end
  end

endmodule

`default_nettype wire
