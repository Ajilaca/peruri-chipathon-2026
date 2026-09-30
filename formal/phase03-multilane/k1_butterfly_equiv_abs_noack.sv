`default_nettype none
`timescale 1ns/1ps
// formal/phase03-multilane/k1_butterfly_equiv_abs_noack.sv
// NEGATIVE CONTROL ONLY: identical to k1_butterfly_equiv_abs.sv but WITHOUT the functional-consistency
// assumptions; k1_negctl_noack.sby must FAIL.
// Experiment K1, equivalence option 1: rtl/ntt/butterfly.sv (two multipliers) vs
// rtl/ntt/butterfly_shared.sv (one shared multiplier), both unchanged, with every modmul_reduce
// instance replaced by formal/phase03-multilane/modmul_reduce_uf.sv (uninterpreted function) and
// functional-consistency constraints between each pair of multiplier instances. Proves that the
// operand selection and the add/sub/mux logic around the multiplier are equivalent for every mode and
// every a, b, zeta in [0, q). Complements (does not replace) the simulation evidence.

module k1_butterfly_equiv_abs (
    input wire        mode_i,
    input wire [11:0] a_i,
    input wire [11:0] b_i,
    input wire [11:0] zeta_i
);

  wire [11:0] ref_a, ref_b, dut_a, dut_b;

  butterfly        u_ref (.mode_i(mode_i), .a_i(a_i), .b_i(b_i), .zeta_i(zeta_i), .a_o(ref_a), .b_o(ref_b));
  butterfly_shared u_dut (.mode_i(mode_i), .a_i(a_i), .b_i(b_i), .zeta_i(zeta_i), .a_o(dut_a), .b_o(dut_b));

`ifdef FORMAL
  always_comb begin
    assume (a_i < 12'd3329);
    assume (b_i < 12'd3329);
    assume (zeta_i < 12'd3329);
    assert (dut_a == ref_a);
    assert (dut_b == ref_b);
  end
`endif

endmodule
`default_nettype wire
