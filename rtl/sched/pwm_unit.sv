`default_nettype none
`timescale 1ns/1ps
// rtl/sched/pwm_unit.sv
// Phase 6 (docs/evidence/phase06-scheduling/test_plan.md): BaseCaseMultiply (FIPS 203 Algorithm 12) plus accumulation, one coefficient pair per cycle:
//   c0 = acc0 + a0*b0 + a1*(b1*gamma)    c1 = acc1 + a0*b1 + a1*b0          (all mod q, inputs in [0, q))
// The term a1*b1*gamma is computed as a1*(b1*gamma mod q), which is the same value mod q. Five Barrett multipliers (rtl/arith/modmul_barrett.sv,
// cuts after stages 0, 1, 2: latency ML = 3 each). Outputs for the inputs of cycle t appear at t + LAT, LAT = 2*ML + 1 = 7. Fixed latency, no control,
// no data-dependent timing. No reset (datapath).

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module pwm_unit (
    input  wire           clk_i,
    input  wire  [CW-1:0] a0_i,
    input  wire  [CW-1:0] a1_i,
    input  wire  [CW-1:0] b0_i,
    input  wire  [CW-1:0] b1_i,
    input  wire  [CW-1:0] gamma_i,
    input  wire  [CW-1:0] acc0_i,
    input  wire  [CW-1:0] acc1_i,
    output logic [CW-1:0] c0_o,
    output logic [CW-1:0] c1_o
);

  localparam logic [3:0] MulReg = 4'b0111;
  localparam int         ML     = 3;

  logic [CW-1:0] m00, m01, m10, mbg, mhi;
  logic [CW-1:0] a1_d, m00_d, m01_d, m10_d, acc0_d, acc1_d;

  modmul_barrett #(.REG_AFTER(MulReg)) u_m00 (.clk_i(clk_i), .a_i(a0_i), .b_i(b0_i),    .p_o(m00));
  modmul_barrett #(.REG_AFTER(MulReg)) u_m01 (.clk_i(clk_i), .a_i(a0_i), .b_i(b1_i),    .p_o(m01));
  modmul_barrett #(.REG_AFTER(MulReg)) u_m10 (.clk_i(clk_i), .a_i(a1_i), .b_i(b0_i),    .p_o(m10));
  modmul_barrett #(.REG_AFTER(MulReg)) u_mbg (.clk_i(clk_i), .a_i(b1_i), .b_i(gamma_i), .p_o(mbg));
  modmul_barrett #(.REG_AFTER(MulReg)) u_mhi (.clk_i(clk_i), .a_i(a1_d), .b_i(mbg),     .p_o(mhi));

  pipe_delay #(.W(CW),     .STAGES(ML),     .HAS_RST(1'b0)) u_dly_a1  (.clk_i(clk_i), .rst_ni(1'b1), .d_i(a1_i), .q_o(a1_d));
  pipe_delay #(.W(3 * CW), .STAGES(ML),     .HAS_RST(1'b0)) u_dly_m   (.clk_i(clk_i), .rst_ni(1'b1),
                                                                         .d_i({m00, m01, m10}), .q_o({m00_d, m01_d, m10_d}));
  pipe_delay #(.W(2 * CW), .STAGES(2 * ML), .HAS_RST(1'b0)) u_dly_acc (.clk_i(clk_i), .rst_ni(1'b1),
                                                                         .d_i({acc0_i, acc1_i}), .q_o({acc0_d, acc1_d}));

  always_ff @(posedge clk_i) begin
    c0_o <= add_mod(add_mod(acc0_d, m00_d), mhi);
    c1_o <= add_mod(add_mod(acc1_d, m01_d), m10_d);
  end

endmodule
`default_nettype wire
