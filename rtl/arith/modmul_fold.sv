`default_nettype none
`timescale 1ns/1ps
// rtl/arith/modmul_fold.sv
// Phase 5a (docs/evidence/phase05-arith/test_plan.md section 3, reading (ii) of ADR 0011 D4):
// (a_i * b_i) mod Q with a q-specific fold reduction, built from shifts and adds only.
//
// q = 3329 = 2^11 + 2^10 + 2^8 + 1, hence 2^12 = q + 767, i.e. 2^12 = 767 (mod q), with
// 767 = 2^10 - 2^8 - 1. Writing v = h * 2^12 + l (l = the low 12 bits), v = 767 * h + l (mod q), so
//
//   fold(v) = (h << 10) - (h << 8) - h + l          (same residue mod q, smaller value)
//
// Five folds bring every 24-bit product below 3q (upper bounds, computed for ALL 24-bit inputs, not only
// a, b < q: 2^24-1 -> 3,144,960 -> 592,384 -> 114,543 -> 24,804 -> 8,697 < 3q = 9,987), so one final stage
// selects v, v - q or v - 2q. Stage widths follow those bounds: 24, 22, 20, 17, 15, 14 bits.
// The function equals (a_i * b_i) mod Q for every 12-bit a_i, b_i; this is checked exhaustively
// (tb/arith/fold_exhaustive/). Same port list as rtl/ntt/modmul_reduce_staged.sv.
//
// Stages: n = 1..5 are the folds, n = 6 is the final select. REG_AFTER[n] = 1 places a register after
// n stages; n = 0 is the 24-bit product straight out of the multiplier (cut "X"), n = 6 an output
// register. Latency in cycles = number of bits set. REG_AFTER = 0 is purely combinational.
// The register positions used in Quartus are fixed in the test plan (section 14) before compiling.
//
// Constant time: fixed latency, no data-dependent control; the select is a multiplexer.
// Reset: none (datapath registers; validity is tracked by the core's control pipeline).

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module modmul_fold #(
    parameter logic [6:0] REG_AFTER = 7'd0
) (
    input  wire           clk_i,
    input  wire  [CW-1:0] a_i,
    input  wire  [CW-1:0] b_i,
    output logic [CW-1:0] p_o   // (a_i * b_i) mod Q, REG_AFTER-many cycles later
);

  localparam int PW = 24;                 // product width: 12 x 12 bits

  // s_in[n] = value after n stages; s_cut[n] = the same value after cut point n (registered or not).
  // Carried at PW bits; the bits above each stage's bound are 0 and are trimmed by the tool.
  logic [PW-1:0] s_in  [0:6];
  logic [PW-1:0] s_cut [0:6];

  assign s_in[0] = PW'(a_i) * PW'(b_i);

  // One fold: v -> 767 * (v >> 12) + (v mod 2^12). No overflow at PW bits: 4095 * 1024 + 4095 < 2^24.
  function automatic logic [PW-1:0] fold(input logic [PW-1:0] v);
    logic [PW-1:0] h, l;
    begin
      h    = v >> 12;
      l    = v & PW'(12'hFFF);
      fold = (h << 10) - (h << 8) - h + l;    // 767 * h + l; never negative: 1024h >= 256h + h
    end
  endfunction

  localparam int W1 = 22, W2 = 20, W3 = 17, W4 = 15, W5 = 14;   // bit widths after folds 1..5

  assign s_in[1] = fold(s_cut[0]) & PW'((1 << W1) - 1);
  assign s_in[2] = fold(s_cut[1]) & PW'((1 << W2) - 1);
  assign s_in[3] = fold(s_cut[2]) & PW'((1 << W3) - 1);
  assign s_in[4] = fold(s_cut[3]) & PW'((1 << W4) - 1);
  assign s_in[5] = fold(s_cut[4]) & PW'((1 << W5) - 1);

  // Final select: value in [0, 3q) -> value mod q. Both subtractions are evaluated in parallel.
  logic [W5:0]   d1, d2;                  // W5 + 1 bits: bit W5 is the borrow
  logic [CW-1:0] r;
  always_comb begin
    d1 = {1'b0, s_cut[5][W5-1:0]} - (W5 + 1)'(Q);
    d2 = {1'b0, s_cut[5][W5-1:0]} - (W5 + 1)'(2 * Q);
    if (!d2[W5])      r = d2[CW-1:0];      // v >= 2q
    else if (!d1[W5]) r = d1[CW-1:0];      // q <= v < 2q
    else              r = s_cut[5][CW-1:0];
  end
  assign s_in[6] = PW'(r);

  genvar gi;
  generate
    for (gi = 0; gi <= 6; gi++) begin : g_cut
      if (REG_AFTER[gi]) begin : g_reg
        logic [PW-1:0] q;
        always_ff @(posedge clk_i) q <= s_in[gi];
        assign s_cut[gi] = q;
      end else begin : g_wire
        assign s_cut[gi] = s_in[gi];
      end
    end
  endgenerate

  assign p_o = s_cut[6][CW-1:0];

  // clk_i is unused when REG_AFTER == 0
  logic unused_clk;
  assign unused_clk = clk_i;

endmodule
`default_nettype wire
