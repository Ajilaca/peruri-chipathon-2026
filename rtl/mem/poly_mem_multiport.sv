`default_nettype none
`timescale 1ns/1ps
// rtl/mem/poly_mem_multiport.sv
// Phase 3 (docs/ROADMAP.md Phase 3, docs/evidence/phase03-multilane/test_plan.md): the
// multi-lane datapath's memory, built on the same conflict-free bank mapping as
// rtl/mem/poly_mem_banked.sv (rtl/mem/bank_map_rom.sv, NUM_BANKS = NUM_LANES) but exposing
// 2*NUM_LANES logical ports instead of 2 -- one (j, jlen) port pair per lane -- so all NUM_LANES
// butterflies of a sub-cycle can read and write concurrently.
//
// Per-port signals are packed vectors (port `i`'s slice is bits [i*W +: W]), not unpacked
// arrays: SymbiYosys's restricted SystemVerilog formal reader
// (formal/phase03-multilane/*.sby) does not accept unpacked-array module ports, and this shape
// is also the more portable/standard synthesizable idiom.
//
// `en_i` marks which ports are actually in use this cycle (e.g. only port 0 during host
// load/read or the INTT scaling pass, all 2*NUM_LANES during the S_RUN butterfly loop); a
// disabled port's addr_i is caller "don't care" and never occupies a bank slot or is counted
// toward the capacity check below.
//
// Capacity precondition (caller contract, not re-derived here): at most 2 of the *enabled*
// logical ports may map to the same bank in any one cycle -- exactly what
// docs/evidence/phase03-multilane/lane_schedule_verification_2026-09-29.txt
// (scripts/gen_lane_schedule.py) proves for the lane_p-based schedule rtl/ntt/ntt_core_c2.sv
// drives this module with, for every L in {1,2,4,8}, every layer, every direction. This module
// does not assume that silently: a third same-cycle, same-bank access is not serviced (dropped)
// but IS flagged on `bank_overflow_o` so simulation/formal can assert it is never asserted
// (docs/evidence/phase03-multilane/test_plan.md, "Formal (CRG-8)").
//
// Per bank: 2 physical read/write sub-ports (matching a Cyclone V M10K true dual-port block,
// same as rtl/mem/poly_mem_banked.sv), combinational read / synchronous write (async-read
// limitation inherited unchanged from Phase 2, docs/results/result_phase2.md).

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module poly_mem_multiport #(
    parameter int NUM_LANES = 1
) (
    input  wire         clk_i,

    input  wire [2*NUM_LANES-1:0]        en_i,      // bit i: 0 = port i unused this cycle
    input  wire [2*NUM_LANES-1:0]        we_i,
    input  wire [2*NUM_LANES*AW-1:0]     addr_i,     // port i: addr_i[i*AW +: AW]
    input  wire [2*NUM_LANES*CW-1:0]     wdata_i,    // port i: wdata_i[i*CW +: CW]
    output logic [2*NUM_LANES*CW-1:0]    rdata_o,    // port i: rdata_o[i*CW +: CW]

    output logic bank_overflow_o   // must stay 0 for a valid Phase 3 schedule
);

  localparam int NumPorts = 2 * NUM_LANES;
  localparam int BankAW   = (N / NUM_LANES > 1) ? $clog2(N / NUM_LANES) : 1;
  localparam int BankSelW = (NUM_LANES > 1) ? $clog2(NUM_LANES) : 1;

  logic [NumPorts*BankSelW-1:0] bank;   // port i: bank[i*BankSelW +: BankSelW]
  logic [NumPorts*BankAW-1:0]   off;    // port i: off[i*BankAW +: BankAW]

  genvar gp;
  generate
    for (gp = 0; gp < NumPorts; gp++) begin : g_map
      bank_map_rom #(.NUM_BANKS(NUM_LANES)) u_map (
          .addr_i  (addr_i[gp*AW +: AW]),
          .bank_o  (bank[gp*BankSelW +: BankSelW]),
          .offset_o(off[gp*BankAW +: BankAW])
      );
    end
  endgenerate

  // Slot assignment: among the *enabled* (en_i) ports, the 0th/1st (in port-index order)
  // landing on a given bank this cycle gets that bank's physical sub-port 0/1. A disabled port
  // never occupies a slot (its addr_i is caller "don't care" and must not count against real
  // ports). A 3rd+ enabled same-bank port (slot==2) is a capacity violation -- proof-guaranteed
  // not to happen for the schedule this module is driven with.
  logic [NumPorts*2-1:0] slot;   // port i: slot[i*2 +: 2]
  logic [NUM_LANES*2-1:0] count; // bank b: count[b*2 +: 2]

  logic [BankSelW-1:0] bi;
  always_comb begin
    for (int b = 0; b < NUM_LANES; b++) count[b*2 +: 2] = 2'd0;
    for (int i = 0; i < NumPorts; i++) begin
      bi = bank[i*BankSelW +: BankSelW];
      if (en_i[i]) begin
        slot[i*2 +: 2] = (count[bi*2 +: 2] < 2'd2) ? count[bi*2 +: 2] : 2'd2;
        if (count[bi*2 +: 2] < 2'd3) count[bi*2 +: 2] = count[bi*2 +: 2] + 2'd1;
      end else begin
        slot[i*2 +: 2] = 2'd2;   // disabled: never assigned a physical sub-port
      end
    end
  end

  always_comb begin
    bank_overflow_o = 1'b0;
    for (int i = 0; i < NumPorts; i++) begin
      if (en_i[i] && slot[i*2 +: 2] == 2'd2) bank_overflow_o = 1'b1;
    end
  end

  logic [NUM_LANES*2*CW-1:0] bank_rdata;   // bank b, sub-port s: bank_rdata[(b*2+s)*CW +: CW]

  genvar gb;
  generate
    for (gb = 0; gb < NUM_LANES; gb++) begin : g_bank
      logic [CW-1:0] mem [0:(N / NUM_LANES) - 1];
      logic               we0, we1;
      logic [BankAW-1:0]  addr0, addr1;
      logic [CW-1:0]      wdata0, wdata1;

      always_comb begin
        we0 = 1'b0; addr0 = '0; wdata0 = '0;
        we1 = 1'b0; addr1 = '0; wdata1 = '0;
        for (int i = 0; i < NumPorts; i++) begin
          if (en_i[i] && bank[i*BankSelW +: BankSelW] == gb[BankSelW-1:0]) begin
            if (slot[i*2 +: 2] == 2'd0) begin
              we0 = we_i[i]; addr0 = off[i*BankAW +: BankAW]; wdata0 = wdata_i[i*CW +: CW];
            end else if (slot[i*2 +: 2] == 2'd1) begin
              we1 = we_i[i]; addr1 = off[i*BankAW +: BankAW]; wdata1 = wdata_i[i*CW +: CW];
            end
          end
        end
      end

      assign bank_rdata[(gb*2+0)*CW +: CW] = mem[addr0];
      assign bank_rdata[(gb*2+1)*CW +: CW] = mem[addr1];

      always_ff @(posedge clk_i) begin
        if (we0) mem[addr0] <= wdata0;
        if (we1) mem[addr1] <= wdata1;
      end
    end
  endgenerate

  generate
    for (gp = 0; gp < NumPorts; gp++) begin : g_rdout
      logic [BankSelW-1:0] rd_bank;
      logic                rd_sub;
      assign rd_bank = bank[gp*BankSelW +: BankSelW];
      assign rd_sub  = slot[gp*2];
      assign rdata_o[gp*CW +: CW] = bank_rdata[(rd_bank*2 + rd_sub)*CW +: CW];
    end
  endgenerate

endmodule
`default_nettype wire
