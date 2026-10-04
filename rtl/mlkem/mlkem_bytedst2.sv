`default_nettype none
`timescale 1ns/1ps
// rtl/mlkem/mlkem_bytedst2.sv
// Phase 9M item 1 (docs/evidence/phase09m-optimisation/9m1/test_plan_9m1.md): rtl/mlkem/mlkem_bytedst.sv taking two bytes per beat. After start_i every accepted 16-bit beat (beat_valid_i, always accepted while busy) is
// collected, beat 0 first (byte 2i in bits 7:0), into a 64-bit word that is written (wr_en_o, wr_idx_o, wr_data_o) in the cycle of its fourth beat; the word index counts 0, 1, 2, ... from start_i. The number of bytes must be a
// multiple of 8 (it is for every polynomial of the core). No control depends on the data. Reset: asynchronous, active low, on the control state.

module mlkem_bytedst2 (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         start_i,
    input  wire         beat_valid_i,
    input  wire  [15:0] beat_data_i,
    output wire         wr_en_o,
    output wire  [8:0]  wr_idx_o,
    output wire  [63:0] wr_data_o
);

  logic [1:0]  bcnt_q;
  logic [8:0]  widx_q;
  logic [47:0] acc_q;

  assign wr_en_o   = beat_valid_i && (bcnt_q == 2'd3);
  assign wr_idx_o  = widx_q;
  assign wr_data_o = {beat_data_i, acc_q};

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      bcnt_q <= 2'd0;
      widx_q <= 9'd0;
    end else if (start_i) begin
      bcnt_q <= 2'd0;
      widx_q <= 9'd0;
    end else if (beat_valid_i) begin
      bcnt_q <= bcnt_q + 2'd1;
      if (bcnt_q == 2'd3) widx_q <= widx_q + 9'd1;
    end
  end

  always_ff @(posedge clk_i) begin
    if (beat_valid_i && (bcnt_q != 2'd3)) acc_q[16*bcnt_q +: 16] <= beat_data_i;
  end

endmodule
`default_nettype wire
