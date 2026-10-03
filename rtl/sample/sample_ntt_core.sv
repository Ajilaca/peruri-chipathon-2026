`default_nettype none
`timescale 1ns/1ps
// rtl/sample/sample_ntt_core.sv
// Phase 8b (docs/evidence/phase08-keccak-stream/8b/test_plan_8b.md section 1): SampleNTT (FIPS 203 Algorithm 7) straight from a 64-bit word stream. OUTW = 1 (stage W1): one coefficient per cycle;
// OUTW = 2 (stage W2): two coefficients per cycle (a beat always holds OUTW consecutive coefficients, lane 0 = lower index).
// Stream bytes: byte k of a word is bits [8k+7:8k] (the byte order of the sponge lanes). A byte window of at most 11 bytes sits between the stream and the triple register; nothing else stores stream data.
// W1: a triple holds the triple register for max(1, accepted) cycles. W2: one triple per cycle; the accepted candidates and one carried coefficient form a pool of 0..3, a beat is emitted whenever the pool reaches 2, the remainder (at most 1) is carried.
// Per triple (b0, b1, b2): d1 = {b1[3:0], b0}, d2 = {b2, b1[7:4]}; a candidate is accepted when d < 3329 (compare with the constant: no modulo, no division). A triple holds the triple register for
// max(1, accepted) cycles, so with the output ready the cycles of a polynomial are the sum over triples of max(1, accepted) plus the cycles the stream needs (public data only).
// The 256th coefficient ends the polynomial: the unused second candidate of that triple is dropped, bytes_o has counted that triple (3 bytes per triple loaded), fin_o rises, and the window is cleared.
// done_o is a one-cycle pulse after the last coefficient has been handed over (coef_valid_o and coef_ready_i); busy_o falls at the same edge. abort_i clears everything at any time.
// Reset: asynchronous, active low. One clock domain, clk_i.

module sample_ntt_core #(
    parameter int OUTW = 1  // coefficients per output beat: 1 (stage W1) or 2 (stage W2)
) (
    input  wire                 clk_i,
    input  wire                 rst_ni,
    input  wire                 start_i,       // accepted when not busy; clears the counters
    input  wire                 abort_i,
    input  wire                 in_valid_i,
    output wire                 in_ready_o,
    input  wire [         63:0] in_data_i,
    output wire                 coef_valid_o,
    input  wire                 coef_ready_i,
    output wire [12*OUTW-1:0]   coef_data_o,
    output wire                 coef_last_o,
    output wire [         15:0] bytes_o,       // stream bytes consumed: 3 per triple loaded
    output wire                 busy_o,
    output wire                 fin_o,         // level: all 256 coefficients are generated, the stream is no longer needed
    output wire                 done_o         // pulse: the last coefficient was handed over
);

  localparam logic [11:0] QC = 12'd3329;  // FIPS 203 q (locked, C1); not named Q so that it does not hide ntt_pkg::Q where both are compiled together

  logic              busy_q, fin_q, done_q;
  logic [      87:0] win_q;  // stream bytes, oldest byte in [7:0]; bits above 8 x cnt_q are zero
  logic [       3:0] cnt_q;  // bytes in the window, 0..11
  logic              tv_q;  // the triple register holds a triple
  logic [      11:0] d1_q, d2_q;
  logic              a1_q, a2_q;  // W1: candidate accepted and not yet output; W2: candidate accepted
  logic [       8:0] n_q;  // W1: coefficients generated; W2: coefficients accepted (output register and carry included), 0..256
  logic [      15:0] bytes_q;
  logic              ov_q, ol_q;  // output register
  logic [12*OUTW-1:0] od_q;
  logic              cv_q;  // W2: a carried coefficient is held
  logic [      11:0] carry_q;

  logic emit, e_last, tri_done;  // driven by the variant below

  wire slot_free = !ov_q || coef_ready_i;
  wire have3 = (cnt_q >= 4'd3);
  wire load = busy_q && !fin_q && have3 && (!tv_q || tri_done) && !e_last;
  wire start_ok = start_i && !busy_q;
  wire hand = ov_q && coef_ready_i;
  wire done_ev = hand && ol_q;
  wire clr = abort_i || e_last || start_ok;

  assign in_ready_o = busy_q && !fin_q && ((cnt_q <= 4'd3) || (load && (cnt_q <= 4'd6)));
  wire take = in_valid_i && in_ready_o;

  wire [ 7:0] b0 = win_q[7:0];
  wire [ 7:0] b1 = win_q[15:8];
  wire [ 7:0] b2 = win_q[23:16];
  wire [11:0] nd1 = {b1[3:0], b0};
  wire [11:0] nd2 = {b2, b1[7:4]};
  wire        acc1 = (nd1 < QC);
  wire        acc2 = (nd2 < QC);

  wire [87:0] base = load ? (win_q >> 24) : win_q;
  wire [ 3:0] cbase = load ? (cnt_q - 4'd3) : cnt_q;
  wire [87:0] w_in = {24'd0, in_data_i} << {cbase, 3'b000};

  assign coef_valid_o = ov_q;
  assign coef_data_o = od_q;
  assign coef_last_o = ov_q && ol_q;
  assign bytes_o = bytes_q;
  assign busy_o = busy_q;
  assign fin_o = fin_q;
  assign done_o = done_q;

  generate
  if (OUTW == 1) begin : g_w1
    // ---- stage W1: one coefficient per cycle (logic as committed in stage W1) ----
    wire emit1 = busy_q && !fin_q && tv_q && a1_q && slot_free;
    wire emit2 = busy_q && !fin_q && tv_q && !a1_q && a2_q && slot_free;
    assign emit = emit1 || emit2;
    wire [11:0] e_data = emit1 ? d1_q : d2_q;
    assign e_last = emit && (n_q == 9'd255);
    assign tri_done = tv_q && ((!a1_q && !a2_q) || (emit1 && !a2_q) || emit2);

    assign cv_q = 1'b0;  // the carry exists only in stage W2
    assign carry_q = 12'd0;
    wire unused_w1 = &{1'b0, cv_q, carry_q};

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      busy_q  <= 1'b0;
      fin_q   <= 1'b0;
      done_q  <= 1'b0;
      win_q   <= 88'd0;
      cnt_q   <= 4'd0;
      tv_q    <= 1'b0;
      d1_q    <= 12'd0;
      d2_q    <= 12'd0;
      a1_q    <= 1'b0;
      a2_q    <= 1'b0;
      n_q     <= 9'd0;
      bytes_q <= 16'd0;
      ov_q    <= 1'b0;
      ol_q    <= 1'b0;
      od_q    <= 12'd0;
    end else begin
      done_q <= 1'b0;
      if (abort_i) begin
        busy_q  <= 1'b0;
        fin_q   <= 1'b0;
        win_q   <= 88'd0;
        cnt_q   <= 4'd0;
        tv_q    <= 1'b0;
        a1_q    <= 1'b0;
        a2_q    <= 1'b0;
        d1_q    <= 12'd0;
        d2_q    <= 12'd0;
        ov_q    <= 1'b0;
        ol_q    <= 1'b0;
        od_q    <= 12'd0;
      end else begin
        if (start_ok) begin
          busy_q  <= 1'b1;
          fin_q   <= 1'b0;
          n_q     <= 9'd0;
          bytes_q <= 16'd0;
          ov_q    <= 1'b0;
          ol_q    <= 1'b0;
        end
        if (done_ev) begin
          busy_q <= 1'b0;
          fin_q  <= 1'b0;
          done_q <= 1'b1;
          ov_q   <= 1'b0;
          ol_q   <= 1'b0;
          od_q   <= 12'd0;
        end else if (emit) begin
          ov_q <= 1'b1;
          od_q <= e_data;
          ol_q <= e_last;
        end else if (hand) begin
          ov_q <= 1'b0;
        end
        if (emit) n_q <= n_q + 9'd1;
        if (e_last) fin_q <= 1'b1;
        // window and triple register
        if (clr) begin
          win_q <= 88'd0;
          cnt_q <= 4'd0;
          tv_q  <= 1'b0;
          a1_q  <= 1'b0;
          a2_q  <= 1'b0;
          d1_q  <= 12'd0;
          d2_q  <= 12'd0;
        end else begin
          win_q <= take ? (base | w_in) : base;
          cnt_q <= take ? (cbase + 4'd8) : cbase;
          if (load) begin
            tv_q    <= 1'b1;
            d1_q    <= nd1;
            d2_q    <= nd2;
            a1_q    <= acc1;
            a2_q    <= acc2;
            bytes_q <= bytes_q + 16'd3;
          end else if (tri_done) begin
            tv_q <= 1'b0;
            a1_q <= 1'b0;
            a2_q <= 1'b0;
          end else begin
            if (emit1) a1_q <= 1'b0;
            if (emit2) a2_q <= 1'b0;
          end
        end
      end
    end
  end


  end else begin : g_w2
    // ---- stage W2: one triple per cycle, two coefficients per beat ----
    wire [1:0] k = {1'b0, a1_q} + {1'b0, a2_q};
    wire [1:0] kc = (k == 2'd2 && n_q == 9'd255) ? 2'd1 : k;  // the second candidate is dropped when the polynomial is full
    wire       pool2 = ((3'(cv_q) + 3'(kc)) >= 3'd2);  // the pool (carry + accepted candidates, 0..3) holds a full beat
    wire act = busy_q && !fin_q && tv_q;
    wire adv = act && (!pool2 || slot_free);  // the triple is consumed this cycle
    assign emit = adv && pool2;
    assign e_last = emit && ((n_q + {7'd0, kc}) == 9'd256);
    assign tri_done = adv;
    wire [11:0] first = a1_q ? d1_q : d2_q;
    wire [23:0] e_data = cv_q ? {first, carry_q} : {d2_q, d1_q};

    always_ff @(posedge clk_i or negedge rst_ni) begin
      if (!rst_ni) begin
        busy_q  <= 1'b0;
        fin_q   <= 1'b0;
        done_q  <= 1'b0;
        win_q   <= 88'd0;
        cnt_q   <= 4'd0;
        tv_q    <= 1'b0;
        d1_q    <= 12'd0;
        d2_q    <= 12'd0;
        a1_q    <= 1'b0;
        a2_q    <= 1'b0;
        n_q     <= 9'd0;
        bytes_q <= 16'd0;
        ov_q    <= 1'b0;
        ol_q    <= 1'b0;
        od_q    <= 24'd0;
        cv_q    <= 1'b0;
        carry_q <= 12'd0;
      end else begin
        done_q <= 1'b0;
        if (abort_i) begin
          busy_q  <= 1'b0;
          fin_q   <= 1'b0;
          win_q   <= 88'd0;
          cnt_q   <= 4'd0;
          tv_q    <= 1'b0;
          a1_q    <= 1'b0;
          a2_q    <= 1'b0;
          d1_q    <= 12'd0;
          d2_q    <= 12'd0;
          cv_q    <= 1'b0;
          carry_q <= 12'd0;
          ov_q    <= 1'b0;
          ol_q    <= 1'b0;
          od_q    <= 24'd0;
        end else begin
          if (start_ok) begin
            busy_q  <= 1'b1;
            fin_q   <= 1'b0;
            n_q     <= 9'd0;
            bytes_q <= 16'd0;
            ov_q    <= 1'b0;
            ol_q    <= 1'b0;
          end
          if (done_ev) begin
            busy_q <= 1'b0;
            fin_q  <= 1'b0;
            done_q <= 1'b1;
            ov_q   <= 1'b0;
            ol_q   <= 1'b0;
            od_q   <= 24'd0;
          end else if (emit) begin
            ov_q <= 1'b1;
            od_q <= e_data;
            ol_q <= e_last;
          end else if (hand) begin
            ov_q <= 1'b0;
          end
          if (adv) n_q <= n_q + {7'd0, kc};
          if (e_last) fin_q <= 1'b1;
          if (clr) begin
            win_q   <= 88'd0;
            cnt_q   <= 4'd0;
            tv_q    <= 1'b0;
            a1_q    <= 1'b0;
            a2_q    <= 1'b0;
            d1_q    <= 12'd0;
            d2_q    <= 12'd0;
            cv_q    <= 1'b0;
            carry_q <= 12'd0;
          end else begin
            win_q <= take ? (base | w_in) : base;
            cnt_q <= take ? (cbase + 4'd8) : cbase;
            if (adv) begin
              if (emit) begin
                cv_q    <= cv_q && (kc == 2'd2);
                carry_q <= (cv_q && (kc == 2'd2)) ? d2_q : 12'd0;
              end else if (!cv_q && kc == 2'd1) begin
                cv_q    <= 1'b1;
                carry_q <= first;
              end
            end
            if (load) begin
              tv_q    <= 1'b1;
              d1_q    <= nd1;
              d2_q    <= nd2;
              a1_q    <= acc1;
              a2_q    <= acc2;
              bytes_q <= bytes_q + 16'd3;
            end else if (tri_done) begin
              tv_q <= 1'b0;
              a1_q <= 1'b0;
              a2_q <= 1'b0;
            end
          end
        end
      end
    end
  end
  endgenerate

endmodule

`default_nettype wire
