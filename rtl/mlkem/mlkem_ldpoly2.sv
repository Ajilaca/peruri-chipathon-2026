`default_nettype none
`timescale 1ns/1ps
// rtl/mlkem/mlkem_ldpoly2.sv
// Phase 9M item 1 (docs/evidence/phase09m-optimisation/9m1/test_plan_9m1.md): rtl/mlkem/mlkem_ldpoly.sv on the two-byte path (mlkem_wordbytes2, mlkem_unpack2); same ports and behaviour, one coefficient per cycle for every d.
// Loads one polynomial into an engine slot: the 4 d words starting at word woff_i of a region are read through the word read port (rd_req_o, rd_addr_o = woff + index; rd_data_i valid the cycle after rd_req_o), decoded and
// decompressed (d chosen by dsel_i: 0 -> 1, 1 -> 4, 2 -> 10, 3 -> 12) and written, one coefficient per cycle, into slot slot_i of the engine through its host port (tb_we_o, tb_slot_o, tb_addr_o = coefficient index, tb_wdata_o).
// done_o is one pulse after the last coefficient was written. start_i is accepted only when idle. No control depends on the data. Reset: asynchronous, active low, on the control state.

module mlkem_ldpoly2 (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         start_i,
    input  wire  [1:0]  dsel_i,
    input  wire  [3:0]  slot_i,
    input  wire  [8:0]  woff_i,
    output wire         rd_req_o,
    output wire  [8:0]  rd_addr_o,
    input  wire  [63:0] rd_data_i,
    output wire         tb_we_o,
    output wire  [4:0]  tb_slot_o,
    output wire  [7:0]  tb_addr_o,
    output wire  [11:0] tb_wdata_o,
    output wire         busy_o,
    output wire         done_o
);

  logic [3:0] slot_q;
  logic [8:0] woff_q;
  logic [7:0] cidx_q;
  logic       busy_q;

  wire start_ok = start_i && !busy_q;

  logic [8:0] nwords;
  always_comb begin
    case (dsel_i)
      2'd0:    nwords = 9'd4;
      2'd1:    nwords = 9'd16;
      2'd2:    nwords = 9'd40;
      default: nwords = 9'd48;
    endcase
  end

  logic [8:0] rd_idx;
  logic        byte_valid, byte_ready, coef_valid, unp_done, unp_busy;
  logic [15:0] byte_data;
  logic [11:0] coef_data;
  /* verilator lint_off UNUSEDSIGNAL */
  logic coef_last;
  /* verilator lint_on UNUSEDSIGNAL */

  mlkem_wordbytes2 u_wb (
      .clk_i(clk_i), .rst_ni(rst_ni), .start_i(start_ok), .nwords_i(nwords),
      .rd_req_o(rd_req_o), .rd_idx_o(rd_idx), .rd_data_i(rd_data_i),
      .beat_valid_o(byte_valid), .beat_ready_i(byte_ready), .beat_data_o(byte_data));

  mlkem_unpack2 u_unp (
      .clk_i(clk_i), .rst_ni(rst_ni), .start_i(start_ok), .dsel_i(dsel_i),
      .beat_valid_i(byte_valid), .beat_ready_o(byte_ready), .beat_data_i(byte_data),
      .coef_valid_o(coef_valid), .coef_ready_i(1'b1), .coef_data_o(coef_data), .coef_last_o(coef_last),
      .busy_o(unp_busy), .done_o(unp_done));

  assign rd_addr_o  = woff_q + rd_idx;
  assign tb_we_o    = coef_valid;
  assign tb_slot_o  = {1'b0, slot_q};
  assign tb_addr_o  = cidx_q;
  assign tb_wdata_o = coef_data;
  assign busy_o     = busy_q;
  assign done_o     = unp_done;

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      busy_q <= 1'b0;
      slot_q <= 4'd0;
      woff_q <= 9'd0;
      cidx_q <= 8'd0;
    end else if (start_ok) begin
      busy_q <= 1'b1;
      slot_q <= slot_i;
      woff_q <= woff_i;
      cidx_q <= 8'd0;
    end else begin
      if (coef_valid) cidx_q <= cidx_q + 8'd1;
      if (unp_done) busy_q <= 1'b0;
    end
  end

  wire unused_ok = &{1'b0, unp_busy};

endmodule
`default_nettype wire
