`default_nettype none
`timescale 1ns/1ps
// rtl/ntt/ntt_core_s7_p7.sv
// Thin Quartus top-level wrapper (Phase 5M step S7, revision S7): rtl/ntt/ntt_core_s7.sv at NUM_LANES = 8, P = 7: the register positions of M6 (memory cuts
// A_4, A_11, M = ARB_REG bits 4, 11, 16; multiplier-path cuts X, S_1, S_2 = MUL_REG bits 0, 1, 2) plus the split of the memory read (RD_SPLIT = 1).
// Same port list as rtl/ntt/ntt_core_m6_p6.sv. No logic here.

module ntt_core_s7_p7 (
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

  ntt_core_s7 #(
      .NUM_LANES(8),
      .ARB_REG  ((33'd1 << 4) | (33'd1 << 11) | (33'd1 << 16)),
      .RD_SPLIT (1),
      .MUL_REG  ((16'd1 << 0) | (16'd1 << 1) | (16'd1 << 2))
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
