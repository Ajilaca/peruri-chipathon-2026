`default_nettype none
`timescale 1ns/1ps
// rtl/mlkem/mlkem_wordbytes2.sv
// Phase 9M item 1 (docs/evidence/phase09m-optimisation/9m1/test_plan_9m1.md): rtl/mlkem/mlkem_wordbytes.sv giving two bytes per beat. After start_i it reads nwords_i words (rd_req_o / rd_idx_o; rd_data_i valid the cycle
// after rd_req_o) and gives their bytes as 16-bit beats, bytes 0 and 1 of a word first (byte 2i in bits 7:0), four beats per word (beat_valid_o / beat_ready_i). A word is requested only when the buffer for the next word is
// empty, so the read data is never lost. Sustained rate: one beat per cycle. No control depends on the data. Reset: asynchronous, active low, on the control state; the data registers are not reset.

module mlkem_wordbytes2 (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         start_i,
    input  wire  [8:0]  nwords_i,
    output wire         rd_req_o,
    output wire  [8:0]  rd_idx_o,
    input  wire  [63:0] rd_data_i,
    output wire         beat_valid_o,
    input  wire         beat_ready_i,
    output wire  [15:0] beat_data_o
);

  logic        busy_q, land_q, cur_v_q, nxt_v_q;
  logic [8:0]  nw_q, widx_q;
  logic [1:0]  bpos_q;
  logic [63:0] cur_q, nxt_q;

  assign rd_req_o     = busy_q && (widx_q != nw_q) && !nxt_v_q && !land_q;
  assign rd_idx_o     = widx_q;
  assign beat_valid_o = cur_v_q;
  assign beat_data_o  = cur_q[16*bpos_q +: 16];

  wire consumed     = cur_v_q && beat_ready_i;
  wire consume_last = consumed && (bpos_q == 2'd3);

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      busy_q  <= 1'b0;
      land_q  <= 1'b0;
      cur_v_q <= 1'b0;
      nxt_v_q <= 1'b0;
      nw_q    <= 9'd0;
      widx_q  <= 9'd0;
      bpos_q  <= 2'd0;
    end else if (start_i) begin
      busy_q  <= 1'b1;
      land_q  <= 1'b0;
      cur_v_q <= 1'b0;
      nxt_v_q <= 1'b0;
      nw_q    <= nwords_i;
      widx_q  <= 9'd0;
      bpos_q  <= 2'd0;
    end else begin
      land_q <= rd_req_o;
      if (rd_req_o) widx_q <= widx_q + 9'd1;
      if (consumed) bpos_q <= bpos_q + 2'd1;
      if (land_q) begin
        if (!cur_v_q || consume_last) begin
          cur_v_q <= 1'b1;
          bpos_q  <= 2'd0;
        end else begin
          nxt_v_q <= 1'b1;
        end
      end else if (consume_last) begin
        if (nxt_v_q) begin
          cur_v_q <= 1'b1;
          nxt_v_q <= 1'b0;
          bpos_q  <= 2'd0;
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
