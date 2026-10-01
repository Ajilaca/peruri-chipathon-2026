`default_nettype none
`timescale 1ns/1ps
// rtl/arith/modmul_sel.sv
// Phase 5 (docs/evidence/phase05-arith/test_plan.md section 4): one interface for every modular
// multiplier-reducer, so that the C4 butterfly and core select the reducer by parameter only.
//
//   RED_KIND = 0: rtl/ntt/modmul_reduce_staged.sv (frozen Phase 4 reducer, the C3-P6 reference)
//   RED_KIND = 1: rtl/arith/modmul_fold.sv        (5a, q-specific fold)
//   RED_KIND = 2: rtl/arith/modmul_barrett.sv     (5b candidate, Barrett)
//   RED_KIND = 3: rtl/arith/modmul_montgomery.sv  (5b candidate, Montgomery, R = 2^12)
//
// Kinds 0..2 compute p_o = (a_i * b_i) mod Q for a_i, b_i in [0, Q); kind 3 computes a_i * b_i * 2^-12 mod Q, so the
// caller supplies one operand in Montgomery form (the C4 core does this for its constant operands). All results
// appear REG_AFTER-many cycles later
// (REG_AFTER is passed through; its meaning, i.e. which stage boundary each bit names, is the
// selected reducer's). No logic of its own.

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module modmul_sel #(
    parameter int          RED_KIND  = 0,
    parameter logic [15:0] REG_AFTER = 16'd0
) (
    input  wire           clk_i,
    input  wire  [CW-1:0] a_i,
    input  wire  [CW-1:0] b_i,
    output logic [CW-1:0] p_o
);

  generate
    if (RED_KIND == 1) begin : g_fold
      modmul_fold #(.REG_AFTER(REG_AFTER[6:0])) u_red (
          .clk_i(clk_i), .a_i(a_i), .b_i(b_i), .p_o(p_o));
    end else if (RED_KIND == 2) begin : g_barrett
      modmul_barrett #(.REG_AFTER(REG_AFTER[3:0])) u_red (
          .clk_i(clk_i), .a_i(a_i), .b_i(b_i), .p_o(p_o));
    end else if (RED_KIND == 3) begin : g_mont
      modmul_montgomery #(.REG_AFTER(REG_AFTER[3:0])) u_red (
          .clk_i(clk_i), .a_i(a_i), .b_i(b_i), .p_o(p_o));
    end else begin : g_staged
      modmul_reduce_staged #(.REG_AFTER(REG_AFTER[13:0])) u_red (
          .clk_i(clk_i), .a_i(a_i), .b_i(b_i), .p_o(p_o));
    end
  endgenerate

  // Bits of REG_AFTER beyond the selected reducer's stage count must be 0: the caller derives the latency
  // from the number of bits set, so a stray bit would misalign the pipeline (caught by the bit-exact tests).
  logic unused_reg;
  assign unused_reg = ^REG_AFTER;

endmodule
`default_nettype wire
