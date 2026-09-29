`default_nettype none
`timescale 1ns/1ps
// rtl/ntt/butterfly.sv
// Single NTT/INTT butterfly, combinational. Two modes, matching
// tb/golden/primitives.py:ntt / intt bit-exactly:
//
//   mode_i = 0 (forward, Cooley-Tukey, FIPS 203 Algorithm 9 lines 8-10):
//     t      = (zeta * b_i) mod q
//     a_o    = (a_i + t) mod q
//     b_o    = (a_i - t) mod q
//
//   mode_i = 1 (inverse, Gentleman-Sande, FIPS 203 Algorithm 10 lines 8-10):
//     t      = a_i
//     a_o    = (t + b_i) mod q
//     b_o    = (zeta * (b_i - t)) mod q
//
// a_i/a_o correspond to f[j], b_i/b_o to f[j+len]; zeta_i is ROM_ZETA[current twiddle index]
// (rtl/ntt/twiddle_rom.sv). The final INTT x3303 scaling (Algorithm 10 line 14) is NOT done
// here; it is a separate pass in rtl/ntt/ntt_core.sv.

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module butterfly (
    input  wire         mode_i,   // 0 = forward (CT), 1 = inverse (GS)
    input  wire  [CW-1:0] a_i,
    input  wire  [CW-1:0] b_i,
    input  wire  [CW-1:0] zeta_i,
    output logic [CW-1:0] a_o,
    output logic [CW-1:0] b_o
);

  logic [CW-1:0] t_fwd, t_inv_diff, zeta_mul_b, zeta_mul_diff;

  modmul_reduce u_fwd_mul  (.a_i(zeta_i), .b_i(b_i),        .p_o(zeta_mul_b));
  modmul_reduce u_inv_mul  (.a_i(zeta_i), .b_i(t_inv_diff),  .p_o(zeta_mul_diff));

  always_comb begin
    // forward path operands
    t_fwd = zeta_mul_b;
    // inverse path operand: (b_i - a_i) mod q, fed into u_inv_mul above
    t_inv_diff = sub_mod(b_i, a_i);

    if (mode_i == 1'b0) begin
      // forward (CT)
      a_o = add_mod(a_i, t_fwd);
      b_o = sub_mod(a_i, t_fwd);
    end else begin
      // inverse (GS)
      a_o = add_mod(a_i, b_i);
      b_o = zeta_mul_diff;
    end
  end

endmodule
`default_nettype wire
