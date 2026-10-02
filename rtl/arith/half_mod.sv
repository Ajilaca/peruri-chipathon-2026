`default_nettype none
`timescale 1ns/1ps
// rtl/arith/half_mod.sv
// Phase 5M step S6 (docs/evidence/phase05m-memsched/test_plan.md): y = x / 2 mod q for x in [0, q).
//   y = (x + (x odd ? q : 0)) >> 1       q is odd, so x + q is even exactly when x is odd; y < q because x < q.
// Combinational; 2 * y = x (mod q) is checked for all 3,329 inputs (tb/phase5m/test_half_mod.py). Inputs >= q are not specified.

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module half_mod (
    input  wire  [CW-1:0] x_i,    // < q
    output logic [CW-1:0] y_o     // x_i / 2 mod q
);

  logic [CW:0] s;
  assign s   = {1'b0, x_i} + (x_i[0] ? (CW + 1)'(Q) : (CW + 1)'(0));
  assign y_o = s[CW:1];

  logic unused_lsb;
  assign unused_lsb = s[0];     // always 0: x_i + q is even whenever it was added

endmodule
`default_nettype wire
