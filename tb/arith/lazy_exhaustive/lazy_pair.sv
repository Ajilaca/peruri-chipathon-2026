`default_nettype none
`timescale 1ns/1ps
// tb/arith/lazy_exhaustive/lazy_pair.sv
// Simulation-only wrapper (Phase 5c, test plan A4 V2-lazy): rtl/arith/modmul_barrett_lazy.sv on its own; the
// reference is the integer formula in lazy_exhaustive.cpp (the frozen modmul_reduce.sv has 12-bit ports only).
module lazy_pair #(
    parameter logic [3:0] REG_AFTER = 4'd0
) (
    input  wire         clk_i,
    input  wire  [11:0] a_i,
    input  wire  [12:0] b_i,
    output logic [11:0] dut_o
);
  modmul_barrett_lazy #(.REG_AFTER(REG_AFTER)) u_dut (.clk_i(clk_i), .a_i(a_i), .b_i(b_i), .p_o(dut_o));
endmodule
`default_nettype wire
