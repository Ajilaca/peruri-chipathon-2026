`default_nettype none
`timescale 1ns/1ps
// rtl/mlkem/mlkem_wordbytes.sv
// Phase 9c: word to byte serialiser with read-ahead. After start_i it reads nwords_i words (index 0, 1, ... through rd_req_o / rd_idx_o; the data rd_data_i is valid the cycle after rd_req_o) and gives their bytes, byte 0 of a word first, one per cycle
// (byte_valid_o / byte_ready_i). A word is requested only when the buffer for the next word is empty, so the read data is never lost. Sustained rate: one byte per cycle. No control depends on the data.
// Reset: asynchronous, active low, on the control state; the data registers are not reset.

module mlkem_wordbytes (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         start_i,
    input  wire  [8:0]  nwords_i,
    output wire         rd_req_o,
    output wire  [8:0]  rd_idx_o,
    input  wire  [63:0] rd_data_i,
    output wire         byte_valid_o,
    input  wire         byte_ready_i,
    output wire  [7:0]  byte_data_o
);

  logic        busy_q, land_q, cur_v_q, nxt_v_q;
  logic [8:0]  nw_q, widx_q;
  logic [2:0]  bpos_q;
  logic [63:0] cur_q, nxt_q;

  assign rd_req_o     = busy_q && (widx_q != nw_q) && !nxt_v_q && !land_q;
  assign rd_idx_o     = widx_q;
  assign byte_valid_o = cur_v_q;
  assign byte_data_o  = cur_q[8*bpos_q +: 8];

  wire consumed     = cur_v_q && byte_ready_i;
  wire consume_last = consumed && (bpos_q == 3'd7);

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      busy_q  <= 1'b0;
      land_q  <= 1'b0;
      cur_v_q <= 1'b0;
      nxt_v_q <= 1'b0;
      nw_q    <= 9'd0;
      widx_q  <= 9'd0;
      bpos_q  <= 3'd0;
    end else if (start_i) begin
      busy_q  <= 1'b1;
      land_q  <= 1'b0;
      cur_v_q <= 1'b0;
      nxt_v_q <= 1'b0;
      nw_q    <= nwords_i;
      widx_q  <= 9'd0;
      bpos_q  <= 3'd0;
    end else begin
      land_q <= rd_req_o;
      if (rd_req_o) widx_q <= widx_q + 9'd1;
      if (consumed) bpos_q <= bpos_q + 3'd1;
      if (land_q) begin
        if (!cur_v_q || consume_last) begin
          cur_v_q <= 1'b1;
          bpos_q  <= 3'd0;
        end else begin
          nxt_v_q <= 1'b1;
        end
      end else if (consume_last) begin
        if (nxt_v_q) begin
          cur_v_q <= 1'b1;
          nxt_v_q <= 1'b0;
          bpos_q  <= 3'd0;
        end else begin
          cur_v_q <= 1'b0;
        end
      end
      if (consume_last && (widx_q == nw_q) && !nxt_v_q && !land_q) busy_q <= 1'b0;
    end
  end

  always_ff @(posedge clk_i) begin
    if (land_q) begin
      if (!cur_v_q || consume_last) cur_q <= rd_data_i;
      else                          nxt_q <= rd_data_i;
    end else if (consume_last && nxt_v_q) begin
      cur_q <= nxt_q;
    end
  end

endmodule
`default_nettype wire
