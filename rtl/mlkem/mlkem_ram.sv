`default_nettype none
`timescale 1ns/1ps
// rtl/mlkem/mlkem_ram.sv
// Phase 9c (docs/evidence/phase09-integration/9c/test_plan_9c.md): simple dual-port word RAM, 64 bit, one write port and one read port, synchronous read (rdata_o one cycle after raddr_i). A read of the word that is written in the same cycle
// returns the old word (not used by the core). The memory is not reset.

module mlkem_ram #(
    parameter int DEPTH = 300,
    parameter int ADDR_W = 9
) (
    input  wire              clk_i,
    input  wire              we_i,
    input  wire  [ADDR_W-1:0]    waddr_i,
    input  wire  [63:0]      wdata_i,
    input  wire  [ADDR_W-1:0]    raddr_i,
    output logic [63:0]      rdata_o
);

  (* ramstyle = "M10K, no_rw_check" *) logic [63:0] mem [0:DEPTH-1];

  always_ff @(posedge clk_i) begin
    if (we_i) mem[waddr_i] <= wdata_i;
    rdata_o <= mem[raddr_i];
  end

endmodule
`default_nettype wire
