`default_nettype none
`timescale 1ns/1ps
// tb/ntt/p4_reducer/modmul_staged_pair.sv
// Simulation-only wrapper (Phase 4, test plan V2): the frozen rtl/ntt/modmul_reduce.sv and
// rtl/ntt/modmul_reduce_staged.sv side by side on the same inputs, for the exhaustive Verilator
// harness in modmul_staged_exhaustive.cpp. No logic of its own.

module modmul_staged_pair #(
    parameter logic [13:0] REG_AFTER = 14'd0
) (
    input  wire         clk_i,
    input  wire  [11:0] a_i,
    input  wire  [11:0] b_i,
    output logic [11:0] ref_o,      // modmul_reduce, combinational
    output logic [11:0] dut_o       // modmul_reduce_staged, REG_AFTER-many cycles later
);
  modmul_reduce                                u_ref (.a_i(a_i), .b_i(b_i), .p_o(ref_o));
  modmul_reduce_staged #(.REG_AFTER(REG_AFTER)) u_dut (.clk_i(clk_i), .a_i(a_i), .b_i(b_i), .p_o(dut_o));
endmodule
`default_nettype wire
