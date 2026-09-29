`default_nettype none
`timescale 1ns/1ps
// rtl/ntt/ntt_core_c2_l8.sv
// Thin Quartus top-level wrapper fixing NUM_LANES=8 on rtl/ntt/ntt_core_c2.sv (docs/ROADMAP.md
// Phase 3), so each L gets its own synthesizable top entity -- same pattern as ntt_core (C0) vs
// rtl/mem/ntt_core_c1.sv (C1): one compile revision per config, same port list, comparable
// reports. No logic here; ntt_core_c2.sv is the only place the datapath is described.

module ntt_core_c2_l8 (
    input  wire               clk_i,
    input  wire                rst_ni,
    input  wire                mode_i,
    input  wire                start_i,
    input  wire  [7:0]         host_addr_i,
    input  wire  [11:0]        host_wdata_i,
    input  wire                host_we_i,
    output logic [11:0]        host_rdata_o,
    output logic                busy_o,
    output logic                done_o,
    output logic                bank_overflow_o
);

  ntt_core_c2 #(.NUM_LANES(8)) u_dut (
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
