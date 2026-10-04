`default_nettype none
`timescale 1ns/1ps
// rtl/mlkem/mlkem_unpack2.sv
// Phase 9M item 1 (docs/evidence/phase09m-optimisation/9m1/test_plan_9m1.md): rtl/mlkem/mlkem_unpack.sv with an input of two bytes per beat. ByteDecode_d -> Decompress_d -> coefficients (FIPS 203 Algorithm 6), same arithmetic
// as the Phase 9a unpacker (Decompress_d(y) = (3329 y + 2^(d-1)) >> d as shifted terms; d = 12: one subtraction of q when the value is >= q).
// One run takes exactly 16 d beats (byte 2i of the polynomial in beat_data_i[7:0], byte 2i + 1 in [15:8]) and gives exactly 256 coefficients, d chosen by dsel_i at start_i: 0 -> 1, 1 -> 4, 2 -> 10, 3 -> 12.
// A beat is taken into the 32-bit buffer when at most 16 bits remain after this cycle's coefficient, so with an always-ready sink one coefficient leaves every cycle for every d. Counters and stalls depend on d and on the handshakes only.
// start_i is accepted only when idle; dsel_i is latched at start. coef_last_o marks coefficient 255; done_o is one pulse the cycle after that coefficient is accepted.
// Reset: asynchronous, active low, on the control state; the datapath registers are not reset (the bit buffer is cleared at start).

module mlkem_unpack2 (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         start_i,
    input  wire  [1:0]  dsel_i,
    input  wire         beat_valid_i,
    output wire         beat_ready_o,
    input  wire  [15:0] beat_data_i,
    output wire         coef_valid_o,
    input  wire         coef_ready_i,
    output wire  [11:0] coef_data_o,
    output wire         coef_last_o,
    output wire         busy_o,
    output wire         done_o
);

  logic        busy_q, done_q;
  logic [1:0]  dsel_q;
  logic [3:0]  dv_q;
  logic [8:0]  nbeats_q;   // 16 d
  logic [8:0]  bin_q;      // beats accepted
  logic [8:0]  cout_q;     // coefficients taken from the buffer
  logic [5:0]  cnt_q;      // bits in the buffer (0 .. 32)
  logic        ov_q, olast_q;
  logic [11:0] od_q;
  logic [31:0] acc_q;

  logic [3:0] dv_in;
  logic [8:0] nb_in;
  always_comb begin
    case (dsel_i)
      2'd0:    begin dv_in = 4'd1;  nb_in = 9'd16;  end
      2'd1:    begin dv_in = 4'd4;  nb_in = 9'd64;  end
      2'd2:    begin dv_in = 4'd10; nb_in = 9'd160; end
      default: begin dv_in = 4'd12; nb_in = 9'd192; end
    endcase
  end

  wire start_ok = start_i && !busy_q;
  wire drain    = ov_q && coef_ready_i;
  wire take     = busy_q && (cnt_q >= {2'b00, dv_q}) && (cout_q != 9'd256) && (!ov_q || coef_ready_i);

  logic [5:0]  take_bits, cnt_after;
  always_comb begin
    take_bits = take ? {2'b00, dv_q} : 6'd0;
    cnt_after = cnt_q - take_bits;
  end

  assign beat_ready_o = busy_q && (bin_q != nbeats_q) && (cnt_after <= 6'd16);
  wire baccept  = beat_valid_i && beat_ready_o;
  assign coef_valid_o = ov_q;
  assign coef_data_o  = od_q;
  assign coef_last_o  = ov_q && olast_q;
  assign busy_o = busy_q;
  assign done_o = done_q;

  // -- Decompress_d of the next d bits (as mlkem_unpack.sv) -------------------------------------------------------
  logic [11:0] x, dec;
  logic [21:0] t;
  logic [9:0]  y;
  always_comb begin
    case (dsel_q)
      2'd0:    y = {9'd0, acc_q[0]};
      2'd1:    y = {6'd0, acc_q[3:0]};
      default: y = acc_q[9:0];
    endcase
    x = (dsel_q == 2'd3) ? acc_q[11:0] : {2'd0, y};
    t = ({12'd0, y} << 11) + ({12'd0, y} << 10) + ({12'd0, y} << 8) + {12'd0, y};   // 3329 y
    case (dsel_q)
      2'd0:    dec = 12'((t + 22'd1) >> 1);
      2'd1:    dec = 12'((t + 22'd8) >> 4);
      2'd2:    dec = 12'((t + 22'd512) >> 10);
      default: dec = (x >= 12'd3329) ? (x - 12'd3329) : x;
    endcase
  end

  logic [31:0] acc_after, acc_ins;
  always_comb begin
    acc_after = acc_q >> take_bits;
    acc_ins   = {16'd0, beat_data_i} << cnt_after;
  end

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      busy_q   <= 1'b0;
      done_q   <= 1'b0;
      dsel_q   <= 2'd0;
      dv_q     <= 4'd1;
      nbeats_q <= 9'd16;
      bin_q    <= 9'd0;
      cout_q   <= 9'd0;
      cnt_q    <= 6'd0;
      ov_q     <= 1'b0;
      olast_q  <= 1'b0;
    end else begin
      done_q <= 1'b0;
      if (start_ok) begin
        busy_q   <= 1'b1;
        dsel_q   <= dsel_i;
        dv_q     <= dv_in;
        nbeats_q <= nb_in;
        bin_q    <= 9'd0;
        cout_q   <= 9'd0;
        cnt_q    <= 6'd0;
        ov_q     <= 1'b0;
        olast_q  <= 1'b0;
      end else if (busy_q) begin
        if (baccept) bin_q <= bin_q + 9'd1;
        cnt_q <= cnt_after + (baccept ? 6'd16 : 6'd0);
        if (take) begin
          cout_q  <= cout_q + 9'd1;
          ov_q    <= 1'b1;
          olast_q <= (cout_q == 9'd255);
        end else if (drain) begin
          ov_q <= 1'b0;
        end
        if (drain && olast_q) begin
          busy_q <= 1'b0;
          done_q <= 1'b1;
        end
      end
    end
  end

  always_ff @(posedge clk_i) begin
    if (take) od_q <= dec;
    if (start_ok) acc_q <= 32'd0;
    else          acc_q <= acc_after | (baccept ? acc_ins : 32'd0);
  end

endmodule
`default_nettype wire
