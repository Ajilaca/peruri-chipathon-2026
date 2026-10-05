`default_nettype none
`timescale 1ns/1ps
// rtl/ntt/ntt_core_s10_p5.sv
// Thin Quartus top-level wrapper (S10, revision S10): rtl/ntt/ntt_core_s10.sv at NUM_LANES = 8, memory read latency 2 (16-bank 1R1W memory), multiplier-path cuts X, S_1, S_2
// (MUL_REG bits 0, 1, 2): P = 5. Phase 9F step S2 (evidence/phase9m/batch2/9s2/test_plan_9s2.md, amendment A1): the parameter P6 (default 0, the P = 5 design above) adds the
// fourth cut (bit 3: the register after the final Barrett correction): P = 6, 119 cycles per transform. The module name stays so that no file list changes. Phase 9F step S2b (evidence/phase9m/batch2/9s2b/test_plan_9s2b.md): the parameter AREG (default 0) registers the issue-stage addresses (computed one cycle early; same cycles and results).
// Same port list as rtl/ntt/ntt_core_m6_p6.sv. No logic here.

module ntt_core_s10_p5 #(
    parameter bit P6    = 1'b0,
    parameter bit AREG  = 1'b0
) (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         mode_i,
    input  wire         start_i,
    input  wire  [7:0]  host_addr_i,
    input  wire  [11:0] host_wdata_i,
    input  wire         host_we_i,
    output logic [11:0] host_rdata_o,
    output logic        busy_o,
    output logic        done_o,
    output logic        bank_overflow_o
);

  ntt_core_s10 #(
      .NUM_LANES(8),
      .RD_LAT   (2),
      .MUL_REG  ((16'd1 << 0) | (16'd1 << 1) | (16'd1 << 2) | (P6 ? (16'd1 << 3) : 16'd0)),
      .AREG     (AREG)
  ) u_core (
      .clk_i          (clk_i),
      .rst_ni         (rst_ni),
      .mode_i         (mode_i),
      .start_i        (start_i),
      .host_addr_i    (host_addr_i),
      .host_wdata_i   (host_wdata_i),
      .host_we_i      (host_we_i),
      .host_rdata_o   (host_rdata_o),
      .busy_o         (busy_o),
      .done_o         (done_o),
      .bank_overflow_o(bank_overflow_o)
  );

endmodule
`default_nettype wire
