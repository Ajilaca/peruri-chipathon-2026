`default_nettype none
`timescale 1ns/1ps
// rtl/ntt/poly_mem.sv
// One 256 x 12-bit polynomial memory, asynchronous-read / synchronous-write, two independent
// read/write ports so a single butterfly (f[j], f[j+len]) can be read and written back in one
// cycle. Deliberately NOT banked and NOT mapped to a specific M10K packing yet -- that is
// Phase 2 scope (docs/ROADMAP.md Phase 2: "M10K storage, banking, address generation"). Phase 1
// only needs a correct, simple store; Quartus is free to infer whatever it infers for this.
//
// Host load/unload reuses port A with we_b_i tied low.

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module poly_mem (
    input  wire              clk_i,
    input  wire              we_a_i,
    input  wire  [AW-1:0]    addr_a_i,
    input  wire  [CW-1:0]    wdata_a_i,
    output logic [CW-1:0]    rdata_a_o,
    input  wire              we_b_i,
    input  wire  [AW-1:0]    addr_b_i,
    input  wire  [CW-1:0]    wdata_b_i,
    output logic [CW-1:0]    rdata_b_o
);

  logic [CW-1:0] mem [0:N-1];

  assign rdata_a_o = mem[addr_a_i];
  assign rdata_b_o = mem[addr_b_i];

  always_ff @(posedge clk_i) begin
    if (we_a_i) mem[addr_a_i] <= wdata_a_i;
    if (we_b_i) mem[addr_b_i] <= wdata_b_i;
  end

endmodule
`default_nettype wire
