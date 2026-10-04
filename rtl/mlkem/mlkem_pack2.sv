`default_nettype none
`timescale 1ns/1ps
// rtl/mlkem/mlkem_pack2.sv
// Phase 9M item 1 (docs/evidence/phase09m-optimisation/9m1/test_plan_9m1.md): rtl/mlkem/mlkem_pack.sv with an output of two bytes per beat. Coefficients -> Compress_d -> ByteEncode_d (FIPS 203 Algorithm 5), the same
// pipeline and the same division-free Compress constants as the Phase 9a packer ((M, S) = (315, 20) for d = 1 and 4, (161271, 29) for d = 10; proved on all 3,329 inputs).
// One run takes exactly 256 coefficients and gives exactly 16 d beats (byte 2i of the encoding in beat_data_o[7:0], byte 2i + 1 in [15:8]), d chosen by dsel_i at start_i: 0 -> 1, 1 -> 4, 2 -> 10, 3 -> 12.
// The packer inserts d bits LSB first into a 32-bit buffer (when the bits left after this cycle's beat plus d fit) and puts out a beat when 16 bits are buffered, so with an always-ready sink one coefficient enters every cycle for
// every d. All counters and stalls depend on d and on the handshakes only, never on data. start_i is accepted only when idle; dsel_i is latched at start. beat_last_o marks beat 16 d - 1; done_o is one pulse the cycle after it.
// Reset: asynchronous, active low, on the control state; the datapath registers are not reset (the bit buffer is cleared at start).

module mlkem_pack2 (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         start_i,
    input  wire  [1:0]  dsel_i,
    input  wire         coef_valid_i,
    output wire         coef_ready_o,
    input  wire  [11:0] coef_data_i,
    output wire         beat_valid_o,
    input  wire         beat_ready_i,
    output wire  [15:0] beat_data_o,
    output wire         beat_last_o,
    output wire         busy_o,
    output wire         done_o
);

  // -- control ------------------------------------------------------------------------------------------------
  logic        busy_q, done_q;
  logic [1:0]  dsel_q;
  logic [3:0]  dv_q;       // d
  logic [8:0]  nbeats_q;   // 16 d
  logic [8:0]  cin_q;      // coefficients accepted
  logic [8:0]  bout_q;     // beats accepted by the sink
  logic [5:0]  cnt_q;      // bits in the buffer (0 .. 32)
  logic        v1_q, v2_q, v3_q;

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
  assign beat_valid_o = busy_q && (cnt_q >= 6'd16);
  wire fire     = beat_valid_o && beat_ready_i;
  assign beat_last_o  = beat_valid_o && (bout_q == (nbeats_q - 9'd1));
  logic [5:0] cnt_after;   // bits left after this cycle's beat
  assign cnt_after = fire ? (cnt_q - 6'd16) : cnt_q;
  wire can_ins  = ({1'b0, cnt_after} + {3'b000, dv_q}) <= 7'd32;
  wire ins      = v3_q && can_ins;
  wire adv      = !(v3_q && !can_ins);
  assign coef_ready_o = busy_q && (cin_q != 9'd256) && adv;
  wire accept   = coef_valid_i && coef_ready_o;
  assign busy_o = busy_q;
  assign done_o = done_q;

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      busy_q   <= 1'b0;
      done_q   <= 1'b0;
      dsel_q   <= 2'd0;
      dv_q     <= 4'd1;
      nbeats_q <= 9'd16;
      cin_q    <= 9'd0;
      bout_q   <= 9'd0;
      cnt_q    <= 6'd0;
      v1_q     <= 1'b0;
      v2_q     <= 1'b0;
      v3_q     <= 1'b0;
    end else begin
      done_q <= 1'b0;
      if (start_ok) begin
        busy_q   <= 1'b1;
        dsel_q   <= dsel_i;
        dv_q     <= dv_in;
        nbeats_q <= nb_in;
        cin_q    <= 9'd0;
        bout_q   <= 9'd0;
        cnt_q    <= 6'd0;
        v1_q     <= 1'b0;
        v2_q     <= 1'b0;
        v3_q     <= 1'b0;
      end else if (busy_q) begin
        if (accept) cin_q <= cin_q + 9'd1;
        if (fire)   bout_q <= bout_q + 9'd1;
        cnt_q <= cnt_after + (ins ? {2'b00, dv_q} : 6'd0);
        if (adv) begin
          v1_q <= accept;
          v2_q <= v1_q;
          v3_q <= v2_q;
        end
        if (fire && beat_last_o) begin
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
  logic [31:0] acc_q;

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

  logic [31:0] acc_after, acc_ins;
  always_comb begin
    acc_after = fire ? (acc_q >> 16) : acc_q;
    acc_ins   = {20'd0, cval} << cnt_after;
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
    if (start_ok) acc_q <= 32'd0;
    else          acc_q <= acc_after | (ins ? acc_ins : 32'd0);
  end

  assign beat_data_o = acc_q[15:0];

endmodule
`default_nettype wire
