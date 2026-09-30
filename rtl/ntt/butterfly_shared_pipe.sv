`default_nettype none
`timescale 1ns/1ps
// rtl/ntt/butterfly_shared_pipe.sv
// Phase 4 (ADR 0007, docs/evidence/phase04-pipeline/test_plan.md): the equations of
// rtl/ntt/butterfly_shared.sv (one multiplier shared by both modes), with the multiplier + reduction
// replaced by rtl/ntt/modmul_reduce_staged.sv so that it can hold pipeline registers. The operand that
// does not go through the multiplier is delayed by the same number of cycles, so the outputs for the
// inputs of cycle t appear at cycle t + LAT, LAT = number of bits set in MUL_REG.
//
//   mode_i = 0 (forward, CT):  t = zeta*b mod q;        a_o = a + t;   b_o = a - t      (mod q)
//   mode_i = 1 (inverse, GS):  t = zeta*(b - a) mod q;  a_o = a + b;   b_o = t          (mod q)
//
// One CW-bit side register per stage carries `a` (forward) or `a + b` (inverse): mode_i is constant
// for a whole NTT/INTT run, so one delay line serves both. With MUL_REG = 0 this module is
// combinational and computes exactly what butterfly_shared.sv computes. butterfly.sv and
// butterfly_shared.sv stay frozen.

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module butterfly_shared_pipe #(
    parameter logic [13:0] MUL_REG = 14'd0     // modmul_reduce_staged.REG_AFTER
) (
    input  wire           clk_i,
    input  wire           mode_i,   // 0 = forward (CT), 1 = inverse (GS); constant during a run
    input  wire  [CW-1:0] a_i,
    input  wire  [CW-1:0] b_i,
    input  wire  [CW-1:0] zeta_i,
    output logic [CW-1:0] a_o,
    output logic [CW-1:0] b_o
);

  function automatic int unsigned ones14(input logic [13:0] v);
    int unsigned n;
    begin
      n = 0;
      for (int i = 0; i < 14; i++) if (v[i]) n = n + 1;
      ones14 = n;
    end
  endfunction

  localparam int unsigned Lat = ones14(MUL_REG);

  logic [CW-1:0] mul_in, side_in, side_d, t;

  always_comb begin
    mul_in  = mode_i ? sub_mod(b_i, a_i) : b_i;
    side_in = mode_i ? add_mod(a_i, b_i) : a_i;
  end

  modmul_reduce_staged #(.REG_AFTER(MUL_REG)) u_mul (
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

  always_comb begin
    if (mode_i == 1'b0) begin
      a_o = add_mod(side_d, t);
      b_o = sub_mod(side_d, t);
    end else begin
      a_o = side_d;
      b_o = t;
    end
  end

endmodule
`default_nettype wire
