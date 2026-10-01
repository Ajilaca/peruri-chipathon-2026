`default_nettype none
`timescale 1ns/1ps
// tb/arith/c4_tb_wrappers.sv
// Simulation-only wrappers (Phase 5 test plan V2-V4, amendment A3). For RED_KIND = 3 (Montgomery) the reducer
// returns a * b * 2^-12 mod q, so the operand that the C4 core always supplies in Montgomery form is converted
// here, combinationally, with the integer formula b * 2^12 mod q; the wrapped unit then computes the same function
// as kinds 0..2 and the existing tests (expecting a * b mod q, or the golden butterfly) apply unchanged.
// For every other RED_KIND the wrappers are plain pass-throughs. Never synthesised.

module modmul_c4_tb #(
    parameter int          RED_KIND  = 1,
    parameter logic [15:0] REG_AFTER = 16'd0
) (
    input  wire         clk_i,
    input  wire  [11:0] a_i,
    input  wire  [11:0] b_i,
    output logic [11:0] p_o
);
  logic [11:0] b_used;
  assign b_used = (RED_KIND == 3) ? 12'((32'(b_i) * 32'd4096) % 32'd3329) : b_i;
  modmul_sel #(.RED_KIND(RED_KIND), .REG_AFTER(REG_AFTER)) u_dut (
      .clk_i(clk_i), .a_i(a_i), .b_i(b_used), .p_o(p_o));
endmodule

module butterfly_c4_tb #(
    parameter int          RED_KIND = 1,
    parameter logic [15:0] MUL_REG  = 16'd0
) (
    input  wire         clk_i,
    input  wire         mode_i,
    input  wire  [11:0] a_i,
    input  wire  [11:0] b_i,
    input  wire  [11:0] zeta_i,
    output logic [11:0] a_o,
    output logic [11:0] b_o
);
  logic [11:0] zeta_used;
  assign zeta_used = (RED_KIND == 3) ? 12'((32'(zeta_i) * 32'd4096) % 32'd3329) : zeta_i;
  butterfly_c4 #(.RED_KIND(RED_KIND), .MUL_REG(MUL_REG)) u_dut (
      .clk_i(clk_i), .mode_i(mode_i), .a_i(a_i), .b_i(b_i), .zeta_i(zeta_used), .a_o(a_o), .b_o(b_o));
endmodule
`default_nettype wire
