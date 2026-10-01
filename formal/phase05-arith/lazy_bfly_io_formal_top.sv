`default_nettype none
`timescale 1ns/1ps
// formal/phase05-arith/lazy_bfly_io_formal_top.sv
// Phase 5c formal bound proof (ADR 0014 §3, test plan amendment A4 V8-lazy) for rtl/arith/lazy_bfly_io.sv.
// Free inputs: mode, a, b, t; assumed a, b, t < q (t is the multiplier result; that it equals (zeta * u) mod q < q for
// every u in [0, 2q) is shown by the exhaustive test tb/arith/lazy_exhaustive/, not here). The side delay line is
// modelled as a wire (side_d = side_o): the delay is a plain register chain and is covered by the simulations.
// Proven for every input (mode prove):
//   P1  mul_o < 2q and side_o < 2q                                     (13-bit values, no overflow of the width)
//   P2  INTT: (mul_o >= q ? mul_o - q : mul_o) == (b - a) mod q         (the lazy multiplier input is congruent)
//       NTT:  mul_o == b
//   P3  outputs < q and equal to the reference butterfly equations:
//       INTT: a_o == (a + b) mod q, b_o == t;  NTT: a_o == (a + t) mod q, b_o == (a - t) mod q
// Reference values are written here with plain integer arithmetic, independent of ntt_pkg's add_mod / sub_mod.

module lazy_bfly_io_formal_top (
    input wire        clk_i,
    input wire        mode_i,
    input wire [11:0] a_i,
    input wire [11:0] b_i,
    input wire [11:0] t_i
);
  localparam int Q = 3329;

  logic [12:0] mul, side;
  logic [11:0] a_o, b_o;

  lazy_bfly_io u_dut (
      .mode_i(mode_i), .a_i(a_i), .b_i(b_i), .mul_o(mul), .side_o(side),
      .side_d_i(side), .t_i(t_i), .a_o(a_o), .b_o(b_o));

  logic [13:0] r_sub_ba, r_add_ab, r_add_at, r_sub_at, mul_red;
  always_comb begin
    r_sub_ba = (b_i >= a_i) ? 14'(b_i - a_i) : 14'(32'(b_i) + Q - 32'(a_i));
    r_add_ab = (32'(a_i) + 32'(b_i) >= Q) ? 14'(32'(a_i) + 32'(b_i) - Q) : 14'(32'(a_i) + 32'(b_i));
    r_add_at = (32'(a_i) + 32'(t_i) >= Q) ? 14'(32'(a_i) + 32'(t_i) - Q) : 14'(32'(a_i) + 32'(t_i));
    r_sub_at = (a_i >= t_i) ? 14'(a_i - t_i) : 14'(32'(a_i) + Q - 32'(t_i));
    mul_red  = (32'(mul) >= Q) ? 14'(32'(mul) - Q) : 14'(mul);
  end

`ifdef FORMAL
  always_comb begin
    assume (32'(a_i) < Q);
    assume (32'(b_i) < Q);
    assume (32'(t_i) < Q);
  end
  always_ff @(posedge clk_i) begin
    assert (32'(mul) < 2 * Q);                                         // P1
    assert (32'(side) < 2 * Q);                                        // P1
    assert (32'(a_o) < Q);                                             // P3
    assert (32'(b_o) < Q);                                             // P3
    if (mode_i) begin
      assert (mul_red == r_sub_ba);                                    // P2
      assert (14'(a_o) == r_add_ab);                                   // P3
      assert (b_o == t_i);                                             // P3
    end else begin
      assert (mul == {1'b0, b_i});                                     // P2
      assert (14'(a_o) == r_add_at);                                   // P3
      assert (14'(b_o) == r_sub_at);                                   // P3
    end
  end
`endif
endmodule
`default_nettype wire
