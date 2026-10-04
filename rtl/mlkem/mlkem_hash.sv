`default_nettype none
`timescale 1ns/1ps
// rtl/mlkem/mlkem_hash.sv
// Phase 9b (docs/evidence/phase09-integration/9b/test_plan_9b.md): the hash functions of FIPS 203 Section 4.1 on a 64-bit word stream: sel_i 0 H = SHA3-256 (4 digest words), 1 G = SHA3-512 (8 words), 2 and 3 J = SHAKE256, first 32 bytes (4 words).
// Message: len_i bytes (public), taken as ceil(len / 8) words, byte k of word w is message byte 8w + k (bytes past len_i in the last word are ignored by the sponge). Digest: word 0 holds digest bytes 0-7 (little endian).
// For J the squeeze is stopped after the 4th word (stop_i of the sponge, which wipes its state); for H and G the sponge returns to idle and wipes its state itself. The control never looks at message or digest data.
// CORE_R2 = 1: C5 sponge (keccak_sponge_r2, ADR 0027); 0: K0 sponge (keccak_sponge), same ports.
// start_i is accepted only when idle (sel_i and len_i are used at that start only). busy_o runs from the accepted start to done_o; done_o is one pulse after the last digest word was accepted and the sponge is idle again.
// Reset: asynchronous, active low, on the control state.

module mlkem_hash #(
    parameter bit CORE_R2 = 1'b1
) (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         start_i,
    input  wire  [1:0]  sel_i,
    input  wire  [15:0] len_i,
    input  wire         in_valid_i,
    output wire         in_ready_o,
    input  wire  [63:0] in_data_i,
    output wire         out_valid_o,
    input  wire         out_ready_i,
    output wire  [63:0] out_data_o,
    output wire         out_last_o,
    output wire         busy_o,
    output wire         done_o
);

  logic       busy_q, done_q, fin_q;
  logic [1:0] sel_q;
  logic [3:0] wcnt_q;      // digest words accepted

  wire        start_ok = start_i && !busy_q;
  wire        is_g     = (sel_q == 2'd1);
  wire        is_j     = sel_q[1];
  wire [3:0]  last_idx = is_g ? 4'd7 : 4'd3;

  logic [1:0] mode_in;
  always_comb begin
    case (sel_i)
      2'd0:    mode_in = 2'd0;
      2'd1:    mode_in = 2'd1;
      default: mode_in = 2'd3;
    endcase
  end

  logic sp_out_valid, sp_busy, sp_in_ready;
  logic [63:0] sp_out_data;
  /* verilator lint_off UNUSEDSIGNAL */
  logic sp_out_last;
  logic [15:0] sp_perm;
  /* verilator lint_on UNUSEDSIGNAL */

  assign out_valid_o = sp_out_valid && busy_q && !fin_q;
  wire   last_word   = (wcnt_q == last_idx);
  wire   take        = out_valid_o && out_ready_i;
  wire   sp_stop     = take && last_word && is_j;
  assign out_last_o  = out_valid_o && last_word;
  assign out_data_o  = sp_out_data;
  assign in_ready_o  = sp_in_ready && busy_q;
  assign busy_o      = busy_q;
  assign done_o      = done_q;

  generate
    if (CORE_R2) begin : g_c5
      keccak_sponge_r2 u_sp (
          .clk_i(clk_i), .rst_ni(rst_ni), .start_i(start_ok), .mode_i(mode_in), .len_i(len_i), .stop_i(sp_stop),
          .in_valid_i(in_valid_i && busy_q), .in_ready_o(sp_in_ready), .in_data_i(in_data_i),
          .out_valid_o(sp_out_valid), .out_ready_i(out_ready_i && busy_q && !fin_q), .out_data_o(sp_out_data), .out_last_o(sp_out_last),
          .busy_o(sp_busy), .perm_cnt_o(sp_perm));
    end else begin : g_k0
      keccak_sponge u_sp (
          .clk_i(clk_i), .rst_ni(rst_ni), .start_i(start_ok), .mode_i(mode_in), .len_i(len_i), .stop_i(sp_stop),
          .in_valid_i(in_valid_i && busy_q), .in_ready_o(sp_in_ready), .in_data_i(in_data_i),
          .out_valid_o(sp_out_valid), .out_ready_i(out_ready_i && busy_q && !fin_q), .out_data_o(sp_out_data), .out_last_o(sp_out_last),
          .busy_o(sp_busy), .perm_cnt_o(sp_perm));
    end
  endgenerate

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      busy_q <= 1'b0;
      done_q <= 1'b0;
      fin_q  <= 1'b0;
      sel_q  <= 2'd0;
      wcnt_q <= 4'd0;
    end else begin
      done_q <= 1'b0;
      if (start_ok) begin
        busy_q <= 1'b1;
        fin_q  <= 1'b0;
        sel_q  <= sel_i;
        wcnt_q <= 4'd0;
      end else if (busy_q) begin
        if (take) begin
          wcnt_q <= wcnt_q + 4'd1;
          if (last_word) fin_q <= 1'b1;
        end
        if (fin_q && !sp_busy) begin
          busy_q <= 1'b0;
          done_q <= 1'b1;
        end
      end
    end
  end

endmodule
`default_nettype wire
