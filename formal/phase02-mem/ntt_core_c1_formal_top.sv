`default_nettype none
`timescale 1ns/1ps
// formal/phase02-mem/ntt_core_c1_formal_top.sv
// Re-runs Phase 1's CRG-8 FSM safety property (formal/phase01-ntt/ntt_core_props.sv, reused
// unchanged) against rtl/mem/ntt_core_c1.sv: the FSM logic is a byte-for-byte copy of C0's, so
// this re-proof exists to catch any accidental divergence introduced when the memory
// instantiation was swapped, not because the FSM was redesigned.

module ntt_core_c1_formal_top (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         mode_i,
    input  wire         start_i,
    input  wire  [7:0]  host_addr_i,
    input  wire  [11:0] host_wdata_i,
    input  wire         host_we_i,
    output wire  [11:0] host_rdata_o,
    output wire         busy_o,
    output wire         done_o
);

  ntt_core_c1 u_dut (
      .clk_i        (clk_i),
      .rst_ni       (rst_ni),
      .mode_i       (mode_i),
      .start_i      (start_i),
      .host_addr_i  (host_addr_i),
      .host_wdata_i (host_wdata_i),
      .host_we_i    (host_we_i),
      .host_rdata_o (host_rdata_o),
      .busy_o       (busy_o),
      .done_o       (done_o)
  );

  ntt_core_props u_props (
      .clk_i  (clk_i),
      .rst_ni (rst_ni),
      .busy_o (busy_o),
      .done_o (done_o)
  );

`ifdef FORMAL
  initial assume (!rst_ni);
`endif

endmodule
`default_nettype wire
