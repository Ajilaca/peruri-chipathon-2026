`default_nettype none
`timescale 1ns/1ps
// rtl/mlkem/mlkem_bytedst.sv
// Phase 9c: byte to word gatherer. After start_i every accepted byte (byte_valid_i, always accepted while busy) is collected, byte 0 first, into a 64-bit word that is written (wr_en_o, wr_idx_o, wr_data_o) in the cycle of its eighth byte;
// the word index counts 0, 1, 2, ... from start_i. The number of bytes must be a multiple of 8 (it is for every polynomial of the core). No control depends on the data. Reset: asynchronous, active low, on the control state.

module mlkem_bytedst (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         start_i,
    input  wire         byte_valid_i,
    input  wire  [7:0]  byte_data_i,
    output wire         wr_en_o,
    output wire  [8:0]  wr_idx_o,
    output wire  [63:0] wr_data_o
);

  logic [2:0]  bcnt_q;
  logic [8:0]  widx_q;
  logic [55:0] acc_q;

  assign wr_en_o   = byte_valid_i && (bcnt_q == 3'd7);
  assign wr_idx_o  = widx_q;
  assign wr_data_o = {byte_data_i, acc_q};

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      bcnt_q <= 3'd0;
      widx_q <= 9'd0;
    end else if (start_i) begin
      bcnt_q <= 3'd0;
      widx_q <= 9'd0;
    end else if (byte_valid_i) begin
      bcnt_q <= bcnt_q + 3'd1;
      if (bcnt_q == 3'd7) widx_q <= widx_q + 9'd1;
    end
  end

  always_ff @(posedge clk_i) begin
    if (byte_valid_i && (bcnt_q != 3'd7)) acc_q[8*bcnt_q +: 8] <= byte_data_i;
  end

endmodule
`default_nettype wire
