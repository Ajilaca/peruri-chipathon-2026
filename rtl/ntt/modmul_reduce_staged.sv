`default_nettype none
`timescale 1ns/1ps
// rtl/ntt/modmul_reduce_staged.sv
// Phase 4 (docs/ROADMAP.md Phase 4, ADR 0007, docs/evidence/phase04-pipeline/test_plan.md):
// (a_i * b_i) mod Q with the reduction written out as explicit stages so that pipeline registers can
// be placed between them. Same function as rtl/ntt/modmul_reduce.sv (which stays frozen): the generic
// `prod % Q` there is replaced by the restoring division it stands for,
//
//     r = a_i * b_i;   for k = 12 downto 0:  if (r >= (Q << k)) r = r - (Q << k);   p_o = r
//
// 13 conditional subtractions, the same number of stages as the divider Quartus inferred for the
// `%` (docs/evidence/phase04-pipeline/k1_l8_worst_path_breakdown_2026-09-30.md). Because
// Q << 13 > 2^24, this equals `prod % Q` for EVERY 24-bit product, i.e. for every 12-bit a_i, b_i, not
// only for operands below Q; the equality is checked exhaustively (tb/ntt/p4_reducer/).
// This is not a change of reduction method or of any result (no Barrett/Montgomery: Phase 5).
//
// REG_AFTER[n] = 1 places a register after n stages: n = 0 is the 24-bit product straight out of the
// multiplier (cut "X" in the test plan), n = 1..12 are the cuts "D_n" inside the reducer, n = 13 is an
// output register. Latency in cycles = number of bits set. REG_AFTER = 0 is purely combinational.
// After the stage for shift k the remainder is below Q << k < 2^(12+k), so the bits above that are
// tied to 0, which keeps the pipeline registers as narrow as the value needs.
//
// Reset: none. These are datapath registers; validity is tracked by the core's control pipeline
// (rtl/ntt/ntt_core_c3.sv), which is reset.

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module modmul_reduce_staged #(
    parameter logic [13:0] REG_AFTER = 14'd0
) (
    input  wire           clk_i,
    input  wire  [CW-1:0] a_i,
    input  wire  [CW-1:0] b_i,
    output logic [CW-1:0] p_o   // (a_i * b_i) mod Q, REG_AFTER-many cycles later
);

  localparam int NStages = 13;
  localparam int PW      = 24;            // product width: 12 x 12 bits

  logic [PW-1:0] s_in  [0:NStages];       // value entering cut point n (after n stages)
  logic [PW-1:0] s_cut [0:NStages];       // value leaving cut point n (registered or not)

  assign s_in[0] = PW'(a_i) * PW'(b_i);

  genvar gi;
  generate
    for (gi = 0; gi <= NStages; gi++) begin : g_cut
      if (REG_AFTER[gi]) begin : g_reg
        logic [PW-1:0] q;
        always_ff @(posedge clk_i) q <= s_in[gi];
        assign s_cut[gi] = q;
      end else begin : g_wire
        assign s_cut[gi] = s_in[gi];
      end
    end

    for (gi = 0; gi < NStages; gi++) begin : g_stage
      localparam int          Shift = NStages - 1 - gi;          // 12 downto 0
      localparam logic [PW:0] QS    = (PW + 1)'(Q) << Shift;      // Q << Shift, up to 25 bits
      localparam logic [PW-1:0] Mask = PW'((1 << (CW + Shift)) - 1);
      logic [PW:0]   diff;
      logic [PW-1:0] nxt;
      always_comb begin
        diff = {1'b0, s_cut[gi]} - QS;
        nxt  = diff[PW] ? s_cut[gi] : diff[PW-1:0];              // borrow set: keep, else subtract
      end
      assign s_in[gi+1] = nxt & Mask;
    end
  endgenerate

  assign p_o = s_cut[NStages][CW-1:0];

  // clk_i is unused when REG_AFTER == 0
  logic unused_clk;
  assign unused_clk = clk_i;

endmodule
`default_nettype wire
