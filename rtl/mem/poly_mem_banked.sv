`default_nettype none
`timescale 1ns/1ps
// rtl/mem/poly_mem_banked.sv
// Banked version of rtl/ntt/poly_mem.sv (docs/ROADMAP.md Phase 2): the same 256 x 12-bit
// polynomial store, split into NUM_BANKS independent 2-port banks using the conflict-free
// mapping in rtl/mem/bank_map_rom.sv (proven for NUM_BANKS in {1,2,4,8},
// evidence/phase02/bank_scheme_exploration.txt).
//
// Two logical ports (A, B), each carrying one *logical* 8-bit address (j or jlen). Each port's
// address is translated to (bank, offset); each bank instance gets up to 2 simultaneous
// accesses (one from port A, one from port B, if they both map there this cycle) -- which the
// proof shows can happen for at most 2 accesses per bank per cycle, matching a Cyclone V M10K
// true dual-port block. This phase instantiates NUM_BANKS=1 only (rtl/mem/ntt_core_c1.sv);
// larger NUM_BANKS compiles (CRG-1/CRG-2) and is address-proven, but its multi-bank read/write
// crossbar below is NOT exercised by any cocotb test this phase (see
// evidence/phase02/test_plan.md) -- building the L>1 datapath is Phase 3 scope.

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module poly_mem_banked #(
    parameter int NUM_BANKS = 1
) (
    input  wire              clk_i,

    input  wire               we_a_i,
    input  wire  [AW-1:0]     addr_a_i,
    input  wire  [CW-1:0]     wdata_a_i,
    output logic [CW-1:0]     rdata_a_o,

    input  wire               we_b_i,
    input  wire  [AW-1:0]     addr_b_i,
    input  wire  [CW-1:0]     wdata_b_i,
    output logic [CW-1:0]     rdata_b_o
);

  localparam int BankAW = (N / NUM_BANKS > 1) ? $clog2(N / NUM_BANKS) : 1;
  localparam int BankSelW = (NUM_BANKS > 1) ? $clog2(NUM_BANKS) : 1;

  logic [BankSelW-1:0] bank_a, bank_b;
  logic [BankAW-1:0]   off_a, off_b;

  bank_map_rom #(.NUM_BANKS(NUM_BANKS)) u_map_a (.addr_i(addr_a_i), .bank_o(bank_a), .offset_o(off_a));
  bank_map_rom #(.NUM_BANKS(NUM_BANKS)) u_map_b (.addr_i(addr_b_i), .bank_o(bank_b), .offset_o(off_b));

  // Per-bank storage + per-bank 2-port read/write, generated once per bank.
  logic [CW-1:0] bank_rdata_a [0:NUM_BANKS-1];
  logic [CW-1:0] bank_rdata_b [0:NUM_BANKS-1];

  genvar gb;
  generate
    for (gb = 0; gb < NUM_BANKS; gb++) begin : g_bank
      logic [CW-1:0] mem [0:(N / NUM_BANKS) - 1];
      logic we_a_this, we_b_this;

      assign we_a_this = we_a_i && (bank_a == gb[BankSelW-1:0]);
      assign we_b_this = we_b_i && (bank_b == gb[BankSelW-1:0]);

      assign bank_rdata_a[gb] = mem[off_a];
      assign bank_rdata_b[gb] = mem[off_b];

      always_ff @(posedge clk_i) begin
        if (we_a_this) mem[off_a] <= wdata_a_i;
        if (we_b_this) mem[off_b] <= wdata_b_i;
      end
    end
  endgenerate

  // Read-data mux: select the bank that each logical port's address actually maps to.
  always_comb begin
    rdata_a_o = bank_rdata_a[bank_a];
    rdata_b_o = bank_rdata_b[bank_b];
  end

endmodule
`default_nettype wire
