`default_nettype none
`timescale 1ns/1ps
// rtl/arith/modmul_montgomery.sv
// Phase 5b candidate (docs/evidence/phase05-arith/test_plan.md section 3, ADR 0011): Montgomery multiplication
// with R = 2^12, same port list as rtl/ntt/modmul_reduce_staged.sv.
//
//   x  = a_i * b_i                                        (24 bits)
//   m  = (x mod R) * q' mod R,  q' = -q^-1 mod R = 3327 = -769 (mod R), 769 = 2^9 + 2^8 + 1
//   t  = (x + m * q) / R                                  (exact division; m * q as shift-and-add)
//   p  = (t >= q) ? t - q : t     =  a_i * b_i * R^-1 mod q
//
// t < 2q whenever x < q * R = 13,635,584, which holds for a_i, b_i < q (x <= 11,075,584). The output is
// a * b * R^-1 mod q: to obtain (a * b) mod q, one operand must be supplied in Montgomery form (b * R mod q).
// In the C4 core the constant operand is always the one in Montgomery form (twiddles from
// rtl/arith/twiddle_rom_mont.sv, INTT scaling constant 3303 * R mod q = 32), so the core's function is
// unchanged. Exhaustively checked in tb/arith/reducer_exhaustive/ (with b driven in Montgomery form).
//
// Stages: n = 1 m, n = 2 t, n = 3 final select. REG_AFTER[n] = 1 places a register after n stages; n = 0
// is the 24-bit product (cut "X"), n = 3 an output register. Latency = bits set.
// Constant time: fixed latency, no data-dependent control. Reset: none (datapath registers).

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module modmul_montgomery #(
    parameter logic [3:0] REG_AFTER = 4'd0
) (
    input  wire           clk_i,
    input  wire  [CW-1:0] a_i,
    input  wire  [CW-1:0] b_i,
    output logic [CW-1:0] p_o   // a_i * b_i * 2^-12 mod Q, REG_AFTER-many cycles later
);

  localparam int PW = 24;          // product width
  localparam int RW = 12;          // log2(R)
  localparam int TW = 13;          // t < 2q < 2^13
  localparam int SW = PW + RW;     // stage vector: {m, x}

  logic [SW-1:0] s_in  [0:3];
  logic [SW-1:0] s_cut [0:3];

  assign s_in[0] = {RW'(0), PW'(a_i) * PW'(b_i)};

  // stage 1: m = -(769 * xl) mod 2^12, xl = x mod 2^12
  logic [RW-1:0] xl, m1;
  assign xl      = s_cut[0][RW-1:0];
  assign m1      = RW'(0) - ((xl << 9) + (xl << 8) + xl);
  assign s_in[1] = {m1, s_cut[0][PW-1:0]};

  // stage 2: t = (x + m*q) >> 12; the low 12 bits of the sum are 0 by construction of m
  logic [RW-1:0] m2;
  logic [PW:0]   mq, sum2;
  assign m2      = s_cut[1][SW-1:PW];
  assign mq      = ((PW + 1)'(m2) << 11) + ((PW + 1)'(m2) << 10) + ((PW + 1)'(m2) << 8) + (PW + 1)'(m2);
  assign sum2    = (PW + 1)'(s_cut[1][PW-1:0]) + mq;
  assign s_in[2] = {RW'(0), PW'(sum2[PW:RW])};

  // stage 3: final select, t in [0, 2q)
  logic [TW:0]   d3;
  logic [CW-1:0] p3;
  always_comb begin
    d3 = {1'b0, s_cut[2][TW-1:0]} - (TW + 1)'(Q);
    p3 = d3[TW] ? s_cut[2][CW-1:0] : d3[CW-1:0];
  end
  assign s_in[3] = {RW'(0), PW'(p3)};

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

  // clk_i is unused when REG_AFTER == 0; the low bits of sum2 are 0 by construction and upper bits of the
  // stage vectors are bounded as stated above
  logic unused;
  assign unused = ^{clk_i, sum2[RW-1:0], s_cut[0][SW-1:PW], s_cut[2][SW-1:TW], s_cut[3][SW-1:CW]};

endmodule
`default_nettype wire
