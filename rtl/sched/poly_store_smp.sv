`default_nettype none
`timescale 1ns/1ps
// rtl/sched/poly_store_smp.sv
// Phases 8c / 8d: copy of rtl/sched/poly_store.sv (Phase 6, unchanged and frozen) whose word index width follows the depth (NPOLY = 12 needs 11 bits, 24 needs 12), so that Verilator -Wall is clean for every NPOLY. Same behaviour.
// Original header:
// Phase 6 (docs/evidence/phase06-scheduling/test_plan.md): polynomial slots of the K-PKE arithmetic unit. NPOLY slots of 256 coefficients, stored as
// 128 words per slot of one coefficient pair (even half = coefficient 2i, odd half = 2i+1, two 12-bit arrays), word index {slot, pair}.
//   read ports A and B: synchronous, data one cycle after the address (both halves of the pair)
//   write port: per-half enables, so a single coefficient (testbench, read-back of the NTT core) or a whole pair (PWM, ADD, SUB) can be written
// No reset (storage). The caller never reads and writes the same word in one cycle (sequencer schedule); the result of such a read is not relied on.

module poly_store_smp #(
    parameter int NPOLY = 24
) (
    input  wire         clk_i,

    input  wire  [4:0]  ra_slot_i,
    input  wire  [6:0]  ra_pair_i,
    output logic [11:0] ra_e_o,
    output logic [11:0] ra_o_o,

    input  wire  [4:0]  rb_slot_i,
    input  wire  [6:0]  rb_pair_i,
    output logic [11:0] rb_e_o,
    output logic [11:0] rb_o_o,

    input  wire         we_e_i,
    input  wire         we_o_i,
    input  wire  [4:0]  w_slot_i,
    input  wire  [6:0]  w_pair_i,
    input  wire  [11:0] wd_e_i,
    input  wire  [11:0] wd_o_i
);

  localparam int Depth = NPOLY * 128;
  localparam int IW    = $clog2(Depth);   // word index width

  logic [11:0] mem_e [0:Depth-1];
  logic [11:0] mem_o [0:Depth-1];

  logic [11:0] ia12, ib12, iw12;
  logic [IW-1:0] ia, ib, iw;
  assign ia12 = {ra_slot_i, ra_pair_i};
  assign ib12 = {rb_slot_i, rb_pair_i};
  assign iw12 = {w_slot_i, w_pair_i};
  assign ia = ia12[IW-1:0];
  assign ib = ib12[IW-1:0];
  assign iw = iw12[IW-1:0];
  logic [11:0] hi_bits;   // the slot numbers of a program stay below NPOLY, so the bits above the index are 0
  logic        unused_hi;
  assign hi_bits   = (ia12 | ib12 | iw12) >> IW;
  assign unused_hi = |hi_bits;

  always_ff @(posedge clk_i) begin
    ra_e_o <= mem_e[ia];
    ra_o_o <= mem_o[ia];
    rb_e_o <= mem_e[ib];
    rb_o_o <= mem_o[ib];
    if (we_e_i) mem_e[iw] <= wd_e_i;
    if (we_o_i) mem_o[iw] <= wd_o_i;
  end

endmodule
`default_nettype wire
