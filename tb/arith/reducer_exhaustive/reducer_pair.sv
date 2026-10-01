`default_nettype none
`timescale 1ns/1ps
// tb/arith/reducer_exhaustive/reducer_pair.sv
// Simulation-only wrapper (Phase 5 test plan V2): the frozen rtl/ntt/modmul_reduce.sv (reference) and one
// Phase 5 reducer, selected through rtl/arith/modmul_sel.sv with the same RED_KIND numbering as the C4 core
// (1 = fold, 2 = Barrett, 3 = Montgomery), side by side on the same inputs, for the exhaustive Verilator harness in
// reducer_exhaustive.cpp. The reducer is wrapped by tb/arith/c4_tb_wrappers.sv:modmul_c4_tb, which for Montgomery
// supplies b in Montgomery form, so every kind is compared against (a * b) mod q. No logic of its own.

module reducer_pair #(
    parameter int          KIND      = 1,
    parameter logic [15:0] REG_AFTER = 16'd0
) (
    input  wire         clk_i,
    input  wire  [11:0] a_i,
    input  wire  [11:0] b_i,
    output logic [11:0] ref_o,      // modmul_reduce, combinational
    output logic [11:0] dut_o       // reducer under test, REG_AFTER-many cycles later
);
  modmul_reduce                                            u_ref (.a_i(a_i), .b_i(b_i), .p_o(ref_o));
  modmul_c4_tb #(.RED_KIND(KIND), .REG_AFTER(REG_AFTER)) u_dut (.clk_i(clk_i), .a_i(a_i), .b_i(b_i), .p_o(dut_o));
endmodule
`default_nettype wire
