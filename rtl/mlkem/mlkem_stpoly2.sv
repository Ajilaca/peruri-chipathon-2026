`default_nettype none
`timescale 1ns/1ps
// rtl/mlkem/mlkem_stpoly2.sv
// Phase 9M item 1 (docs/evidence/phase09m-optimisation/9m1/test_plan_9m1.md): rtl/mlkem/mlkem_stpoly.sv on the two-byte path (mlkem_pack2, mlkem_bytedst2); same ports and behaviour, one coefficient per cycle for every d.
// Stores one polynomial of an engine slot: the 256 coefficients of slot slot_i are read through the host port of the engine (tb_slot_o, tb_addr_o = coefficient index; tb_rdata_i valid one cycle after the address), buffered in a
// four-entry FIFO (credit control: at most three coefficients in flight or held), compressed and encoded (d chosen by dsel_i: 0 -> 1, 1 -> 4, 2 -> 10, 3 -> 12), gathered into 64-bit words and written (wr_en_o, wr_addr_o = woff +
// word index, wr_data_o) into a region. done_o is one pulse after the last beat. start_i is accepted only when idle. No control depends on the data. Reset: asynchronous, active low, on the control state.

module mlkem_stpoly2 (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         start_i,
    input  wire  [1:0]  dsel_i,
    input  wire  [3:0]  slot_i,
    input  wire  [8:0]  woff_i,
    output wire  [4:0]  tb_slot_o,
    output wire  [7:0]  tb_addr_o,
    input  wire  [11:0] tb_rdata_i,
    output wire         wr_en_o,
    output wire  [8:0]  wr_addr_o,
    output wire  [63:0] wr_data_o,
    output wire         busy_o,
    output wire         done_o
);

  logic [3:0] slot_q;
  logic [8:0] woff_q;
  logic [8:0] idx_q;       // addresses issued (0 .. 256)
  logic       busy_q, issue_q;

  wire start_ok = start_i && !busy_q;

  logic        pk_ready, pk_done, pk_busy, byte_valid, byte_last;
  logic [15:0] byte_data;
  logic [2:0]  count;
  logic        fifo_valid;
  logic [11:0] fifo_dout;
  wire         pop = fifo_valid && pk_ready;
  wire         do_issue = busy_q && (idx_q != 9'd256) && ({1'b0, count} + {3'd0, issue_q} < 4'd3);

  mlkem_fifo4 u_fifo (
      .clk_i(clk_i), .rst_ni(rst_ni), .clear_i(start_ok), .push_i(issue_q), .din_i(tb_rdata_i),
      .pop_valid_o(fifo_valid), .pop_i(pop), .dout_o(fifo_dout), .count_o(count));

  mlkem_pack2 u_pk (
      .clk_i(clk_i), .rst_ni(rst_ni), .start_i(start_ok), .dsel_i(dsel_i),
      .coef_valid_i(fifo_valid), .coef_ready_o(pk_ready), .coef_data_i(fifo_dout),
      .beat_valid_o(byte_valid), .beat_ready_i(1'b1), .beat_data_o(byte_data), .beat_last_o(byte_last),
      .busy_o(pk_busy), .done_o(pk_done));

  logic [8:0] w_idx;
  mlkem_bytedst2 u_bd (
      .clk_i(clk_i), .rst_ni(rst_ni), .start_i(start_ok), .beat_valid_i(byte_valid), .beat_data_i(byte_data),
      .wr_en_o(wr_en_o), .wr_idx_o(w_idx), .wr_data_o(wr_data_o));

  assign wr_addr_o = woff_q + w_idx;
  assign tb_slot_o = {1'b0, slot_q};
  assign tb_addr_o = idx_q[7:0];
  assign busy_o    = busy_q;
  assign done_o    = pk_done;

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      busy_q  <= 1'b0;
      issue_q <= 1'b0;
      idx_q   <= 9'd0;
      slot_q  <= 4'd0;
      woff_q  <= 9'd0;
    end else if (start_ok) begin
      busy_q  <= 1'b1;
      issue_q <= 1'b0;
      idx_q   <= 9'd0;
      slot_q  <= slot_i;
      woff_q  <= woff_i;
    end else begin
      issue_q <= do_issue;
      if (do_issue) idx_q <= idx_q + 9'd1;
      if (pk_done) busy_q <= 1'b0;
    end
  end

  wire unused_ok = &{1'b0, pk_busy, byte_last};

endmodule
`default_nettype wire
