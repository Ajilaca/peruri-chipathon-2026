`default_nettype none
`timescale 1ns/1ps
// rtl/ntt/modmul_reduce.sv
// (a * b) mod q, combinational. Straightforward, documented reduction: full-width multiply
// followed by a generic modulo-by-constant. This is the Phase 1 baseline method
// (docs/ROADMAP.md Phase 1); Montgomery/Barrett/lazy reduction are Phase 5 optimisations and are
// explicitly out of scope here ("Not allowed yet").
//
// Used by: rtl/ntt/butterfly.sv (Algorithm 9/10, line "zeta * f[...]") and
// rtl/ntt/base_case_multiply.sv (Algorithm 12).

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module modmul_reduce (
    input  wire  [CW-1:0] a_i,
    input  wire  [CW-1:0] b_i,
    output logic [CW-1:0] p_o   // (a_i * b_i) mod Q
);

  logic [31:0] prod;   // max (Q-1)^2 < 2^24, well within 32 bits (Q's own width)

  always_comb begin
    prod = 32'(a_i) * 32'(b_i);
    p_o  = CW'(prod % Q);   // generic modulo by the constant Q (Phase 5 replaces this)
  end

endmodule
`default_nettype wire
