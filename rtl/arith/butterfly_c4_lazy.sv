`default_nettype none
`timescale 1ns/1ps
// rtl/arith/butterfly_c4_lazy.sv
// Phase 5c (ADR 0014, docs/evidence/phase05-arith/test_plan.md amendment A4): the C4 butterfly with lazy INTT inputs.
// Same ports, function and latency as rtl/arith/butterfly_c4.sv with RED_KIND = 2 (Barrett):
//
//   mode_i = 0 (forward, CT):  t = zeta*b mod q;        a_o = a + t;   b_o = a - t      (mod q)
//   mode_i = 1 (inverse, GS):  t = zeta*(b - a) mod q;  a_o = a + b;   b_o = t          (mod q)
//
// but in INTT mode the multiplier receives u = b + q - a (13 bits, not reduced) and the side delay line carries
// s = a + b (13 bits, not reduced); s is reduced once at the output (rtl/arith/lazy_bfly_io.sv). The reducer is the
// Barrett variant with a 13-bit operand (rtl/arith/modmul_barrett_lazy.sv). Outputs for the inputs of cycle t
// appear at t + LAT, LAT = number of bits set in MUL_REG.

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module butterfly_c4_lazy #(
    parameter logic [15:0] MUL_REG = 16'd0     // Barrett REG_AFTER (bits 0..3)
) (
    input  wire           clk_i,
    input  wire           mode_i,   // 0 = forward (CT), 1 = inverse (GS); constant during a run
    input  wire  [CW-1:0] a_i,
    input  wire  [CW-1:0] b_i,
    input  wire  [CW-1:0] zeta_i,
    output logic [CW-1:0] a_o,
    output logic [CW-1:0] b_o
);

  function automatic int unsigned ones16(input logic [15:0] v);
    int unsigned n;
    begin
      n = 0;
      for (int i = 0; i < 16; i++) if (v[i]) n = n + 1;
      ones16 = n;
    end
  endfunction

  localparam int unsigned Lat = ones16(MUL_REG);

  logic [CW:0]   mul_in, side_in, side_d;
  logic [CW-1:0] t;

  lazy_bfly_io u_io (
      .mode_i  (mode_i),
      .a_i     (a_i),
      .b_i     (b_i),
      .mul_o   (mul_in),
      .side_o  (side_in),
      .side_d_i(side_d),
      .t_i     (t),
      .a_o     (a_o),
      .b_o     (b_o)
  );

  modmul_barrett_lazy #(.REG_AFTER(MUL_REG[3:0])) u_mul (
      .clk_i (clk_i),
      .a_i   (zeta_i),
      .b_i   (mul_in),
      .p_o   (t)
  );

  pipe_delay #(.W(CW + 1), .STAGES(Lat), .HAS_RST(1'b0)) u_side (
      .clk_i (clk_i),
      .rst_ni(1'b1),
      .d_i   (side_in),
      .q_o   (side_d)
  );

  // bits of MUL_REG above the Barrett stage count must be 0 (they would only change Lat)
  logic unused_reg;
  assign unused_reg = ^MUL_REG[15:4];

endmodule
`default_nettype wire
