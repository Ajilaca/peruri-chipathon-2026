`default_nettype none
`timescale 1ns/1ps
// rtl/ntt/ntt_core_c2_k2_k1_l4.sv
// Thin Quartus top-level wrapper fixing NUM_LANES=4 on rtl/ntt/ntt_core_c2_k2_k1.sv (optimisation
// experiments K2+K1, see that file). Same port list as rtl/ntt/ntt_core_c2_l4.sv so C2-L4 and C2-K2-K1-L4
// are compiled with identical constraints and virtual pins. No logic here.

module ntt_core_c2_k2_k1_l4 (
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

  ntt_core_c2_k2_k1 #(.NUM_LANES(4)) u_dut (
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
