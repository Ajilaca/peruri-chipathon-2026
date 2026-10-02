`default_nettype none
`timescale 1ns/1ps
// tb/phase5m/mem_diff_top.sv -- test-only: the frozen rtl/mem/poly_mem_multiport_pipe.sv and rtl/mem/poly_mem_multiport_split.sv (RD_SPLIT = 0) driven by the
// same inputs, both outputs exposed, for the cycle-by-cycle differential test V3 (tb/phase5m/test_poly_mem_diff.py). Not part of any Quartus revision.
module mem_diff_top #(
    parameter logic [32:0] ARB_REG  = 33'd0,
    parameter int          WR_DELAY = 0
) (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire  [15:0] en_i,
    input  wire  [15:0] wr_i,
    input  wire  [127:0] addr_i,
    input  wire  [191:0] wdata_i,
    output wire  [191:0] rdata_a_o,
    output wire         ovf_a_o,
    output wire  [191:0] rdata_b_o,
    output wire         ovf_b_o
);
  poly_mem_multiport_pipe #(.NUM_LANES(8), .ARB_REG(ARB_REG), .WR_DELAY(WR_DELAY)) u_ref (
      .clk_i(clk_i), .rst_ni(rst_ni), .en_i(en_i), .wr_i(wr_i), .addr_i(addr_i), .rdata_o(rdata_a_o),
      .wdata_i(wdata_i), .bank_overflow_o(ovf_a_o));
  poly_mem_multiport_split #(.NUM_LANES(8), .ARB_REG(ARB_REG), .WR_DELAY(WR_DELAY), .RD_SPLIT(0)) u_new (
      .clk_i(clk_i), .rst_ni(rst_ni), .en_i(en_i), .wr_i(wr_i), .addr_i(addr_i), .rdata_o(rdata_b_o),
      .wdata_i(wdata_i), .bank_overflow_o(ovf_b_o));
endmodule
`default_nettype wire
