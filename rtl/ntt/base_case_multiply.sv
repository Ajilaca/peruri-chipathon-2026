`default_nettype none
`timescale 1ns/1ps
// rtl/ntt/base_case_multiply.sv
// FIPS 203 Algorithm 12, BaseCaseMultiply(a0,a1,b0,b1,gamma): the "pointwise multiplication"
// building block for products in T_q (Section 4.3.1). Direct 5-multiplication form, matching
// tb/golden/primitives.py:base_case_multiply bit-exactly:
//   c0 = a0*b0 + a1*b1*gamma  (mod q)
//   c1 = a0*b1 + a1*b0        (mod q)
// gamma is one of the 128 tabulated zeta^(2*BitRev7(i)+1) constants (rtl/ntt/twiddle_rom.sv);
// this module itself is agnostic to where gamma comes from.

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module base_case_multiply (
    input  wire  [CW-1:0] a0_i,
    input  wire  [CW-1:0] a1_i,
    input  wire  [CW-1:0] b0_i,
    input  wire  [CW-1:0] b1_i,
    input  wire  [CW-1:0] gamma_i,
    output logic [CW-1:0] c0_o,
    output logic [CW-1:0] c1_o
);

  logic [CW-1:0] a0b0, a1b1, a1b1_gamma, a0b1, a1b0;

  modmul_reduce u_a0b0 (.a_i(a0_i), .b_i(b0_i), .p_o(a0b0));
  modmul_reduce u_a1b1 (.a_i(a1_i), .b_i(b1_i), .p_o(a1b1));
  modmul_reduce u_a1b1_gamma (.a_i(a1b1), .b_i(gamma_i), .p_o(a1b1_gamma));
  modmul_reduce u_a0b1 (.a_i(a0_i), .b_i(b1_i), .p_o(a0b1));
  modmul_reduce u_a1b0 (.a_i(a1_i), .b_i(b0_i), .p_o(a1b0));

  always_comb begin
    c0_o = add_mod(a0b0, a1b1_gamma);
    c1_o = add_mod(a0b1, a1b0);
  end

endmodule
`default_nettype wire
