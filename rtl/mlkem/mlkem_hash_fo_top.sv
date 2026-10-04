`default_nettype none
`timescale 1ns/1ps
// rtl/mlkem/mlkem_hash_fo_top.sv
// Phase 9b: Quartus and test top: the hash wrapper (h_*) and the FO comparison (f_*) side by side, no logic between them (docs/evidence/phase09-integration/9b/test_plan_9b.md V9).

module mlkem_hash_fo_top #(
    parameter bit CORE_R2 = 1'b1,
    parameter int WORDS   = 136
) (
    input  wire          clk_i,
    input  wire          rst_ni,
    input  wire          h_start_i,
    input  wire  [1:0]   h_sel_i,
    input  wire  [15:0]  h_len_i,
    input  wire          h_in_valid_i,
    output wire          h_in_ready_o,
    input  wire  [63:0]  h_in_data_i,
    output wire          h_out_valid_o,
    input  wire          h_out_ready_i,
    output wire  [63:0]  h_out_data_o,
    output wire          h_out_last_o,
    output wire          h_busy_o,
    output wire          h_done_o,
    input  wire          f_start_i,
    input  wire          f_in_valid_i,
    output wire          f_in_ready_o,
    input  wire  [63:0]  f_a_data_i,
    input  wire  [63:0]  f_b_data_i,
    input  wire  [255:0] f_kgood_i,
    input  wire  [255:0] f_kbad_i,
    output wire  [255:0] f_k_o,
    output wire          f_neq_o,
    output wire          f_busy_o,
    output wire          f_done_o
);

  mlkem_hash #(.CORE_R2(CORE_R2)) u_hash (
      .clk_i(clk_i), .rst_ni(rst_ni), .start_i(h_start_i), .sel_i(h_sel_i), .len_i(h_len_i),
      .in_valid_i(h_in_valid_i), .in_ready_o(h_in_ready_o), .in_data_i(h_in_data_i),
      .out_valid_o(h_out_valid_o), .out_ready_i(h_out_ready_i), .out_data_o(h_out_data_o), .out_last_o(h_out_last_o),
      .busy_o(h_busy_o), .done_o(h_done_o));

  mlkem_fo_cmp #(.WORDS(WORDS)) u_fo (
      .clk_i(clk_i), .rst_ni(rst_ni), .start_i(f_start_i),
      .in_valid_i(f_in_valid_i), .in_ready_o(f_in_ready_o), .a_data_i(f_a_data_i), .b_data_i(f_b_data_i),
      .kgood_i(f_kgood_i), .kbad_i(f_kbad_i), .k_o(f_k_o), .neq_o(f_neq_o), .busy_o(f_busy_o), .done_o(f_done_o));

endmodule
`default_nettype wire
