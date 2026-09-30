`default_nettype none
`timescale 1ns/1ps
// formal/phase03-multilane/k1_butterfly_equiv.sv
// Experiment K1: combinational equivalence miter between rtl/ntt/butterfly.sv (frozen C0/C1/C2
// butterfly, two multipliers) and rtl/ntt/butterfly_shared.sv (one shared multiplier), for every
// mode and every a, b, zeta in [0, q) -- the operand invariant every caller maintains (Phase 1 CRG-7).

module k1_butterfly_equiv (
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
