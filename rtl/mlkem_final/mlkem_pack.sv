`default_nettype none
`timescale 1ns/1ps
// rtl/mlkem/mlkem_pack.sv
// Phase 9a (evidence/phase09/9a/test_plan_9a.md): coefficients -> Compress_d -> ByteEncode_d (FIPS 203 Algorithm 5, Section 4.2.1).
// One run takes exactly 256 coefficients (12 bit, value in [0, q-1]; a larger value is outside the input domain) and gives exactly 32 d bytes, d chosen by dsel_i at start_i: 0 -> 1, 1 -> 4, 2 -> 10, 3 -> 12 (d = 12: no compression).
// Compress_d without division: ((x << d) + 1664) * M >> S, low d bits, (M, S) = (315, 20) for d = 1 and 4, (161271, 29) for d = 10; constants proved on all 3,329 inputs against the golden (tb/golden/tests/test_codec_model.py).
// Pipeline of three register stages with one global enable (a stall holds all stages); the packer inserts d bits LSB first into a 24-bit buffer and puts out one byte per cycle. All counters and stalls depend on d and on the handshakes only, never on data.
// start_i is accepted only when idle (ignored while busy); dsel_i is latched at start. byte_last_o marks byte 32 d - 1; done_o is one pulse the cycle after that byte is accepted.
// Reset: asynchronous, active low, on the control state; the datapath registers are not reset (the bit buffer is cleared at start).

module mlkem_pack (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         start_i,
    input  wire  [1:0]  dsel_i,
    input  wire         coef_valid_i,
    output wire         coef_ready_o,
    input  wire  [11:0] coef_data_i,
    output wire         byte_valid_o,
    input  wire         byte_ready_i,
    output wire  [7:0]  byte_data_o,
    output wire         byte_last_o,
    output wire         busy_o,
    output wire         done_o
);

  // -- control ------------------------------------------------------------------------------------------------
  logic        busy_q, done_q;
  logic [1:0]  dsel_q;
  logic [3:0]  dv_q;       // d
  logic [8:0]  nbytes_q;   // 32 d
  logic [8:0]  cin_q;      // coefficients accepted
  logic [8:0]  bout_q;     // bytes accepted by the sink
  logic [4:0]  cnt_q;      // bits in the buffer (0 .. 24)
  logic        v1_q, v2_q, v3_q;

  logic [3:0] dv_in;
  logic [8:0] nb_in;
  always_comb begin
    case (dsel_i)
      2'd0:    begin dv_in = 4'd1;  nb_in = 9'd32;  end
      2'd1:    begin dv_in = 4'd4;  nb_in = 9'd128; end
      2'd2:    begin dv_in = 4'd10; nb_in = 9'd320; end
      default: begin dv_in = 4'd12; nb_in = 9'd384; end
    endcase
  end

  wire start_ok = start_i && !busy_q;
  wire can_ins  = ({1'b0, cnt_q} + {2'b00, dv_q}) <= 6'd24;
  wire ins      = v3_q && can_ins;
  wire adv      = !(v3_q && !can_ins);
  assign coef_ready_o = busy_q && (cin_q != 9'd256) && adv;
  wire accept   = coef_valid_i && coef_ready_o;
  assign byte_valid_o = busy_q && (cnt_q >= 5'd8);
  wire fire     = byte_valid_o && byte_ready_i;
  assign byte_last_o  = byte_valid_o && (bout_q == (nbytes_q - 9'd1));
  assign busy_o = busy_q;
  assign done_o = done_q;

  logic [4:0] cnt_after;   // bits left after this cycle's byte
  assign cnt_after = fire ? (cnt_q - 5'd8) : cnt_q;

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      busy_q   <= 1'b0;
      done_q   <= 1'b0;
      dsel_q   <= 2'd0;
      dv_q     <= 4'd1;
      nbytes_q <= 9'd32;
      cin_q    <= 9'd0;
      bout_q   <= 9'd0;
      cnt_q    <= 5'd0;
      v1_q     <= 1'b0;
      v2_q     <= 1'b0;
      v3_q     <= 1'b0;
    end else begin
      done_q <= 1'b0;
      if (start_ok) begin
        busy_q   <= 1'b1;
        dsel_q   <= dsel_i;
        dv_q     <= dv_in;
        nbytes_q <= nb_in;
        cin_q    <= 9'd0;
        bout_q   <= 9'd0;
        cnt_q    <= 5'd0;
        v1_q     <= 1'b0;
        v2_q     <= 1'b0;
        v3_q     <= 1'b0;
      end else if (busy_q) begin
        if (accept) cin_q <= cin_q + 9'd1;
        if (fire)   bout_q <= bout_q + 9'd1;
        cnt_q <= cnt_after + (ins ? {1'b0, dv_q} : 5'd0);
        if (adv) begin
          v1_q <= accept;
          v2_q <= v1_q;
          v3_q <= v2_q;
        end
        if (fire && byte_last_o) begin
          busy_q <= 1'b0;
          done_q <= 1'b1;
        end
      end
    end
  end

  // -- datapath -----------------------------------------------------------------------------------------------
  logic [11:0] x1_q, x2_q, x3_q;
  logic [21:0] n2_q;
  logic [9:0]  q10_q;      // bits [38:29] of the d = 10 product: the quotient (low d bits)
  logic [3:0]  q4_q;       // bits [23:20] of the d = 1 / 4 product
  logic [23:0] acc_q;

  logic [21:0] n_next;
  always_comb begin
    case (dsel_q)
      2'd0:    n_next = {9'd0, x1_q, 1'b0} + 22'd1664;
      2'd1:    n_next = {6'd0, x1_q, 4'd0} + 22'd1664;
      default: n_next = {x1_q, 10'd0} + 22'd1664;
    endcase
  end

  /* verilator lint_off UNUSEDSIGNAL */
  wire [24:0] ps = {9'd0, n2_q[15:0]} * 25'd315;
  wire [39:0] pb = {18'd0, n2_q} * 40'd161271;
  /* verilator lint_on UNUSEDSIGNAL */

  logic [11:0] cval;
  always_comb begin
    case (dsel_q)
      2'd0:    cval = {11'd0, q4_q[0]};
      2'd1:    cval = {8'd0, q4_q};
      2'd2:    cval = {2'd0, q10_q};
      default: cval = x3_q;
    endcase
  end

  logic [23:0] acc_after, acc_ins;
  always_comb begin
    acc_after = fire ? (acc_q >> 8) : acc_q;
    acc_ins   = {12'd0, cval} << cnt_after;
  end

  always_ff @(posedge clk_i) begin
    if (adv) begin
      x1_q <= coef_data_i;
      x2_q <= x1_q;
      x3_q <= x2_q;
      n2_q <= n_next;
      q10_q <= pb[38:29];
      q4_q  <= ps[23:20];
    end
    if (start_ok) acc_q <= 24'd0;
    else          acc_q <= acc_after | (ins ? acc_ins : 24'd0);
  end

  assign byte_data_o = acc_q[7:0];

endmodule
`default_nettype wire
