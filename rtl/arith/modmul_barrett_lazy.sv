`default_nettype none
`timescale 1ns/1ps
// rtl/arith/modmul_barrett_lazy.sv
// Phase 5c (ADR 0014, evidence/phase05/test_plan.md amendment A4): rtl/arith/modmul_barrett.sv with a 13-bit
// second operand for the lazy INTT butterfly input u = b + q - a in [1, 2q). Same method, constant and stages:
//
//   x  = a_i * b_i                       (25 bits; a_i < q, b_i < 2q -> x <= (q-1)(2q-1) = 22,154,496)
//   t  = (x * M) >> 24,  M = 5039        (14-bit field; <= 6,654 in the contract domain)
//   r  = x - t * q                       (t * q as shift-and-add)
//   p  = (r >= q) ? r - q : r
//
// Contract (ADR 0014 §2): p = (a_i * b_i) mod q for every a_i in [0, q) and b_i in [0, 2q); for those products the
// remainder r stays below 2q (largest r = 6,478, perhitungan tim over all products), so one conditional subtraction
// suffices. Outside that domain the result is not specified (reported by the exhaustive harness, not required).
// Exhaustively checked in tb/arith/lazy_exhaustive/.
//
// Stages: n = 1 quotient estimate, n = 2 remainder, n = 3 final select; REG_AFTER[n] places a register after n
// stages (n = 0: the product, cut "X"). Latency = bits set. Constant time; no reset (datapath registers).

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module modmul_barrett_lazy #(
    parameter logic [3:0] REG_AFTER = 4'd0
) (
    input  wire           clk_i,
    input  wire  [CW-1:0] a_i,     // < q
    input  wire  [CW:0]   b_i,     // < 2q
    output logic [CW-1:0] p_o      // (a_i * b_i) mod Q, REG_AFTER-many cycles later
);

  localparam int PW = 25;                          // product width: 12 x 13 bits
  localparam int TW = 14;                          // quotient-estimate field: (2^25 - 1) * M >> 24 < 2^14
  localparam int RW = 13;                          // remainder field: r < 2q < 2^13 in the contract domain
  localparam int SW = PW + TW;                     // stage vector: {t, x}
  localparam logic [TW-1:0] M = TW'((1 << 24) / Q);   // 5039, as in modmul_barrett.sv

  logic [SW-1:0] s_in  [0:3];
  logic [SW-1:0] s_cut [0:3];

  assign s_in[0] = {TW'(0), PW'(a_i) * PW'(b_i)};

  // stage 1: quotient estimate
  logic [PW+TW-1:0] xm;
  assign xm      = (PW + TW)'(s_cut[0][PW-1:0]) * (PW + TW)'(M);
  assign s_in[1] = {xm[PW+TW-1-1:24], s_cut[0][PW-1:0]};

  // stage 2: remainder r = x - t*q (stored in the x field)
  logic [TW-1:0] t2;
  logic [PW-1:0] tq, r2;
  assign t2      = s_cut[1][SW-1:PW];
  assign tq      = (PW'(t2) << 11) + (PW'(t2) << 10) + (PW'(t2) << 8) + PW'(t2);
  assign r2      = s_cut[1][PW-1:0] - tq;
  assign s_in[2] = {TW'(0), PW'(r2[RW-1:0])};

  // stage 3: final select
  logic [RW:0]   d3;
  logic [CW-1:0] p3;
  always_comb begin
    d3 = {1'b0, s_cut[2][RW-1:0]} - (RW + 1)'(Q);
    p3 = d3[RW] ? s_cut[2][CW-1:0] : d3[CW-1:0];
  end
  assign s_in[3] = {TW'(0), PW'(p3)};

  genvar gi;
  generate
    for (gi = 0; gi <= 3; gi++) begin : g_cut
      if (REG_AFTER[gi]) begin : g_reg
        logic [SW-1:0] q;
        always_ff @(posedge clk_i) q <= s_in[gi];
        assign s_cut[gi] = q;
      end else begin : g_wire
        assign s_cut[gi] = s_in[gi];
      end
    end
  endgenerate

  assign p_o = s_cut[3][CW-1:0];

  logic unused;
  assign unused = ^{clk_i, xm[23:0], xm[PW+TW-1], r2[PW-1:RW], s_cut[0][SW-1:PW], s_cut[2][SW-1:RW],
                    s_cut[3][SW-1:CW]};

endmodule
`default_nettype wire
