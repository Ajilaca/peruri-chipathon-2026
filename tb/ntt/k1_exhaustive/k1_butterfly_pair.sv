`default_nettype none
`timescale 1ns/1ps
// tb/ntt/k1_exhaustive/k1_butterfly_pair.sv
// Simulation-only wrapper (experiment K1, equivalence option 2): the frozen rtl/ntt/butterfly.sv
// and rtl/ntt/butterfly_shared.sv side by side on the same inputs, for the exhaustive Verilator
// harness in k1_exhaustive.cpp. No logic of its own.

module k1_butterfly_pair (
    input  wire         mode_i,
    input  wire  [11:0] a_i,
    input  wire  [11:0] b_i,
    input  wire  [11:0] zeta_i,
    output logic [11:0] ref_a_o,
    output logic [11:0] ref_b_o,
    output logic [11:0] dut_a_o,
    output logic [11:0] dut_b_o
);
  butterfly        u_ref (.mode_i(mode_i), .a_i(a_i), .b_i(b_i), .zeta_i(zeta_i), .a_o(ref_a_o), .b_o(ref_b_o));
  butterfly_shared u_dut (.mode_i(mode_i), .a_i(a_i), .b_i(b_i), .zeta_i(zeta_i), .a_o(dut_a_o), .b_o(dut_b_o));
endmodule
`default_nettype wire
