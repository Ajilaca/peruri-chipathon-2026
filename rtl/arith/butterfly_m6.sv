`default_nettype none
`timescale 1ns/1ps
// rtl/arith/butterfly_m6.sv
// Phase 5M step S6 (evidence/phase05m/test_plan.md): the Barrett (RED_KIND = 2) butterfly of
// rtl/arith/butterfly_c4.sv with the INTT scaling folded into the layers (halving in every layer). Outputs for the inputs of
// cycle t appear at cycle t + LAT, LAT = number of bits set in MUL_REG.
//
//   mode_i = 0 (forward, CT):  t = zeta*b mod q;                  a_o = a + t;            b_o = a - t        (mod q)
//   mode_i = 1 (inverse, GS):  t = zeta_h*(b - a) mod q;          a_o = (a + b) / 2;      b_o = t            (mod q)
//                              zeta_h = zeta / 2 mod q is supplied by the caller (rtl/arith/twiddle_rom_half.sv).
// The halving of the side value is done on the write side (after the delay line), where the C4b-B timing report has slack.
// NTT mode is identical to butterfly_c4.sv with RED_KIND = 2.

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module butterfly_m6 #(
    parameter logic [15:0] MUL_REG = 16'd0    // Barrett REG_AFTER
) (
    input  wire           clk_i,
    input  wire           mode_i,   // 0 = forward (CT), 1 = inverse (GS); constant during a run
    input  wire  [CW-1:0] a_i,
    input  wire  [CW-1:0] b_i,
    input  wire  [CW-1:0] zeta_i,   // zeta (NTT) or zeta / 2 mod q (INTT)
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

  logic [CW-1:0] mul_in, side_in, side_d, t, side_half;

  always_comb begin
    mul_in  = mode_i ? sub_mod(b_i, a_i) : b_i;
    side_in = mode_i ? add_mod(a_i, b_i) : a_i;
  end

  modmul_sel #(.RED_KIND(2), .REG_AFTER(MUL_REG)) u_mul (
      .clk_i (clk_i),
      .a_i   (zeta_i),
      .b_i   (mul_in),
      .p_o   (t)
  );

  pipe_delay #(.W(CW), .STAGES(Lat), .HAS_RST(1'b0)) u_side (
      .clk_i (clk_i),
      .rst_ni(1'b1),
      .d_i   (side_in),
      .q_o   (side_d)
  );

  half_mod u_half (.x_i(side_d), .y_o(side_half));

  always_comb begin
    if (mode_i == 1'b0) begin
      a_o = add_mod(side_d, t);
      b_o = sub_mod(side_d, t);
    end else begin
      a_o = side_half;
      b_o = t;
    end
  end

endmodule
`default_nettype wire
