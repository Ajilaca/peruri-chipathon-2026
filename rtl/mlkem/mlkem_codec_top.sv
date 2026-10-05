`default_nettype none
`timescale 1ns/1ps
// rtl/mlkem/mlkem_codec_top.sv
// Phase 9a: Quartus and test top of the codec: the packer (p_*) and the unpacker (u_*) side by side, no logic between them (evidence/phase09/9a/test_plan_9a.md V10).

module mlkem_codec_top (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         p_start_i,
    input  wire  [1:0]  p_dsel_i,
    input  wire         p_coef_valid_i,
    output wire         p_coef_ready_o,
    input  wire  [11:0] p_coef_data_i,
    output wire         p_byte_valid_o,
    input  wire         p_byte_ready_i,
    output wire  [7:0]  p_byte_data_o,
    output wire         p_byte_last_o,
    output wire         p_busy_o,
    output wire         p_done_o,
    input  wire         u_start_i,
    input  wire  [1:0]  u_dsel_i,
    input  wire         u_byte_valid_i,
    output wire         u_byte_ready_o,
    input  wire  [7:0]  u_byte_data_i,
    output wire         u_coef_valid_o,
    input  wire         u_coef_ready_i,
    output wire  [11:0] u_coef_data_o,
    output wire         u_coef_last_o,
    output wire         u_busy_o,
    output wire         u_done_o
);

  mlkem_pack u_pack (
      .clk_i(clk_i), .rst_ni(rst_ni), .start_i(p_start_i), .dsel_i(p_dsel_i),
      .coef_valid_i(p_coef_valid_i), .coef_ready_o(p_coef_ready_o), .coef_data_i(p_coef_data_i),
      .byte_valid_o(p_byte_valid_o), .byte_ready_i(p_byte_ready_i), .byte_data_o(p_byte_data_o), .byte_last_o(p_byte_last_o),
      .busy_o(p_busy_o), .done_o(p_done_o));

  mlkem_unpack u_unpack (
      .clk_i(clk_i), .rst_ni(rst_ni), .start_i(u_start_i), .dsel_i(u_dsel_i),
      .byte_valid_i(u_byte_valid_i), .byte_ready_o(u_byte_ready_o), .byte_data_i(u_byte_data_i),
      .coef_valid_o(u_coef_valid_o), .coef_ready_i(u_coef_ready_i), .coef_data_o(u_coef_data_o), .coef_last_o(u_coef_last_o),
      .busy_o(u_busy_o), .done_o(u_done_o));

endmodule
`default_nettype wire
