`default_nettype none
`timescale 1ns/1ps
// formal/phase03-multilane/k1_negctl_butterfly_shared_wrong_operand.sv
// NEGATIVE CONTROL ONLY (never synthesised or simulated): a copy of rtl/ntt/butterfly_shared.sv with the
// inverse multiplier operand deliberately wrong (sub_mod(a_i, b_i) instead of sub_mod(b_i, a_i)).
// k1_negctl_operand.sby must FAIL; if it ever passes, the abstraction proof is vacuous.
// (original header of the copied file follows)
// Optimisation experiment K1 (evidence/phase03/, L=8 ALM audit): the same
// NTT/INTT butterfly as rtl/ntt/butterfly.sv, computing exactly the same equations, but with ONE
// modular multiplier shared by both modes instead of one per mode. mode_i is fixed for a whole
// NTT or INTT run, so the forward multiplier (zeta*b) and the inverse multiplier (zeta*(b-a))
// are never both needed in the same cycle; the multiplier operand is selected by mode_i.
//
//   mode_i = 0 (forward, Cooley-Tukey, FIPS 203 Algorithm 9 lines 8-10):
//     t   = (zeta * b_i) mod q
//     a_o = (a_i + t) mod q
//     b_o = (a_i - t) mod q
//
//   mode_i = 1 (inverse, Gentleman-Sande, FIPS 203 Algorithm 10 lines 8-10):
//     t   = (zeta * ((b_i - a_i) mod q)) mod q
//     a_o = (a_i + b_i) mod q
//     b_o = t
//
// modmul_reduce.sv (the reduction method) is reused unchanged. rtl/ntt/butterfly.sv stays the
// frozen C0/C1/C2 butterfly.

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module butterfly_shared (
    input  wire           mode_i,   // 0 = forward (CT), 1 = inverse (GS)
    input  wire  [CW-1:0] a_i,
    input  wire  [CW-1:0] b_i,
    input  wire  [CW-1:0] zeta_i,
    output logic [CW-1:0] a_o,
    output logic [CW-1:0] b_o
);

  logic [CW-1:0] mul_in, t;

  modmul_reduce u_mul (.a_i(zeta_i), .b_i(mul_in), .p_o(t));

  always_comb begin
    mul_in = mode_i ? sub_mod(a_i, b_i) : b_i;

    if (mode_i == 1'b0) begin
      a_o = add_mod(a_i, t);
      b_o = sub_mod(a_i, t);
    end else begin
      a_o = add_mod(a_i, b_i);
      b_o = t;
    end
  end

endmodule
`default_nettype wire
