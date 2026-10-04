`default_nettype none
`timescale 1ns/1ps
// formal/phase09m-optimisation/9m1/stubs_9m1.sv
// Phase 9M item 1 (docs/evidence/phase09m-optimisation/9m1/test_plan_9m1.md V6): protocol stubs of mlkem_ldpoly2 and mlkem_stpoly2 for the 9c core proof with -D W2. They are the 9c stubs of mlkem_ldpoly and mlkem_stpoly
// (formal/phase09-integration/9c/stubs_9c.sv) under the new module names: the two-byte tasks have the same ports and the same handshake protocol.

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
  (* anyseq *) wire        f_cfin, f_creq, f_cwe;
  (* anyseq *) wire [8:0]  f_cadr;
  (* anyseq *) wire [4:0]  f_cslot;
  (* anyseq *) wire [7:0]  f_ctadr;
  (* anyseq *) wire [11:0] f_dwd;
  logic busy_q, done_q;
  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      busy_q <= 1'b0;
      done_q <= 1'b0;
    end else begin
      done_q <= 1'b0;
      if (start_i && !busy_q) busy_q <= 1'b1;
      else if (busy_q && f_cfin) begin
        busy_q <= 1'b0;
        done_q <= 1'b1;
      end
    end
  end
  assign rd_req_o = busy_q && f_creq;
  assign rd_addr_o = f_cadr;
  assign tb_we_o = busy_q && f_cwe;
  assign tb_slot_o = f_cslot;
  assign tb_addr_o = f_ctadr;
  assign tb_wdata_o = f_dwd;
  assign busy_o = busy_q;
  assign done_o = done_q;
  wire unused_ok = &{1'b0, dsel_i, slot_i, woff_i, rd_data_i};
endmodule

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
  (* anyseq *) wire        f_cfin, f_cwe;
  (* anyseq *) wire [8:0]  f_cadr;
  (* anyseq *) wire [4:0]  f_cslot;
  (* anyseq *) wire [7:0]  f_ctadr;
  (* anyseq *) wire [63:0] f_dwd;
  logic busy_q, done_q;
  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      busy_q <= 1'b0;
      done_q <= 1'b0;
    end else begin
      done_q <= 1'b0;
      if (start_i && !busy_q) busy_q <= 1'b1;
      else if (busy_q && f_cfin) begin
        busy_q <= 1'b0;
        done_q <= 1'b1;
      end
    end
  end
  assign tb_slot_o = f_cslot;
  assign tb_addr_o = f_ctadr;
  assign wr_en_o = busy_q && f_cwe;
  assign wr_addr_o = f_cadr;
  assign wr_data_o = f_dwd;
  assign busy_o = busy_q;
  assign done_o = done_q;
  wire unused_ok = &{1'b0, dsel_i, slot_i, woff_i, tb_rdata_i};
endmodule
`default_nettype wire
