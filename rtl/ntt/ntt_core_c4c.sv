`default_nettype none
`timescale 1ns/1ps
// rtl/ntt/ntt_core_c4c.sv
// Thin Quartus top-level wrapper (Phase 5c, revision C4c, ADR 0014): rtl/ntt/ntt_core_c4.sv at NUM_LANES = 8 with
// Barrett reducers (RED_KIND = 2) and lazy INTT butterfly inputs (LAZY = 1, rtl/arith/butterfly_c4_lazy.sv).
// Memory cuts as C3-P6 (A_4, A_11, M); multiplier-path cuts X, S_1, S_2 (REG_AFTER bits 0, 1, 2; test plan
// amendment A4). P = 6. Same port list as rtl/ntt/ntt_core_c3_p6.sv. No logic here.

module ntt_core_c4c (
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

  ntt_core_c4 #(
      .NUM_LANES(8),
      .ARB_REG  ((33'd1 << 4) | (33'd1 << 11) | (33'd1 << 16)),
      .RED_KIND (2),
      .LAZY     (1'b1),
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
