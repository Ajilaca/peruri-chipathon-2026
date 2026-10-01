`default_nettype none
`timescale 1ns/1ps
// rtl/arith/modmul_barrett.sv
// Phase 5b candidate (docs/evidence/phase05-arith/test_plan.md section 3, ADR 0011): (a_i * b_i) mod Q by
// Barrett reduction, same port list as rtl/ntt/modmul_reduce_staged.sv and rtl/arith/modmul_fold.sv.
//
//   x  = a_i * b_i                       (24 bits)
//   t  = (x * M) >> 24,  M = floor(2^24 / q) = 5039     (13 bits; quotient estimate)
//   r  = x - t * q                       (t * q written as shift-and-add: q = 2^11 + 2^10 + 2^8 + 1)
//   p  = (r >= q) ? r - q : r
//
// For every 24-bit x (i.e. every pair of 12-bit operands, not only a, b < q) the remainder r is below 2q
// (largest r = 5,713 < 2q = 6,658, checked over all 2^24 values by script), so one conditional subtraction
// suffices. The multiplication x * M is left to the tool (DSP or logic); the multiplication by q is shift-add.
// Exhaustively checked in tb/arith/reducer_exhaustive/.
//
// Stages: n = 1 quotient estimate, n = 2 remainder, n = 3 final select. REG_AFTER[n] = 1 places a register
// after n stages; n = 0 is the 24-bit product (cut "X"), n = 3 an output register. Latency = bits set.
// Constant time: fixed latency, no data-dependent control. Reset: none (datapath registers).

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module modmul_barrett #(
    parameter logic [3:0] REG_AFTER = 4'd0
) (
    input  wire           clk_i,
    input  wire  [CW-1:0] a_i,
    input  wire  [CW-1:0] b_i,
    output logic [CW-1:0] p_o   // (a_i * b_i) mod Q, REG_AFTER-many cycles later
);

  localparam int PW = 24;                          // product width
  localparam int TW = 13;                          // quotient-estimate width: (2^24 - 1) * M >> 24 < 2^13
  localparam int SW = PW + TW;                     // stage vector: {t, x}
  localparam logic [TW-1:0] M = TW'((1 << 24) / Q);   // 5039

  // s_in[n] / s_cut[n]: value after n stages, before / after cut point n. Layout {t[TW-1:0], x[PW-1:0]}.
  logic [SW-1:0] s_in  [0:3];
  logic [SW-1:0] s_cut [0:3];

  assign s_in[0] = {TW'(0), PW'(a_i) * PW'(b_i)};

  // stage 1: quotient estimate
  logic [PW+TW-1:0] xm;
  assign xm      = (PW + TW)'(s_cut[0][PW-1:0]) * (PW + TW)'(M);
  assign s_in[1] = {xm[PW+TW-1:PW], s_cut[0][PW-1:0]};

  // stage 2: remainder r = x - t*q, r < 2q (fits 13 bits); stored in the x field
  logic [TW-1:0] t2;
  logic [PW-1:0] tq, r2;
  assign t2      = s_cut[1][SW-1:PW];
  assign tq      = (PW'(t2) << 11) + (PW'(t2) << 10) + (PW'(t2) << 8) + PW'(t2);
  assign r2      = s_cut[1][PW-1:0] - tq;
  assign s_in[2] = {TW'(0), PW'(r2[TW-1:0])};

  // stage 3: final select
  logic [TW:0]   d3;
  logic [CW-1:0] p3;
  always_comb begin
    d3 = {1'b0, s_cut[2][TW-1:0]} - (TW + 1)'(Q);
    p3 = d3[TW] ? s_cut[2][CW-1:0] : d3[CW-1:0];   // borrow: r < q, keep
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

  // clk_i is unused when REG_AFTER == 0; the low bits of xm, the upper bits of r2 and of the stage
  // vectors are structurally unused (their values are bounded as stated above)
  logic unused;
  assign unused = ^{clk_i, xm[PW-1:0], r2[PW-1:TW], s_cut[0][SW-1:PW], s_cut[2][SW-1:TW], s_cut[3][SW-1:CW]};

endmodule
`default_nettype wire
