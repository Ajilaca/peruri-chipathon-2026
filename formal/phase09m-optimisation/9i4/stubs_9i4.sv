`default_nettype none
`timescale 1ns/1ps
// formal/phase09m-optimisation/9i4/stubs_9i4.sv
// Phase 9I item 4: formal-only protocol stubs (same module names, parameters and ports) of the engine variant kpke_smp_top_s10o and of the loader mlkem_ldpoly2o, derived from the stubs of 9c and 9m1 (see there). The engine stub's tb_wready_o is a free control signal (equal in the two copies of the miter).

module kpke_smp_top_s10o #(
    parameter int NPOLY    = 24,
    parameter int VAR      = 0,
    parameter bit STREAM_A = 1'b0,
    parameter bit OVERLAP  = 1'b0,
    parameter bit CORE_R2  = 1'b1,
    parameter bit NTT_P6   = 1'b0,  // Phase 9F S2: accepted and ignored (the stub is protocol-level; the NTT length is not modelled)
    parameter bit NTT_AR   = 1'b0,  // Phase 9F S2b: accepted and ignored
    parameter bit HOSTOV   = 1'b1   // Phase 9I item 4: accepted and ignored
) (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire  [1:0]  prog_i,
    input  wire         start_i,
    output wire         busy_o,
    output wire         done_o,
    input  wire         tb_we_i,
    input  wire  [4:0]  tb_slot_i,
    input  wire  [7:0]  tb_addr_i,
    input  wire  [11:0] tb_wdata_i,
    output wire  [11:0] tb_rdata_o,
    output wire         tb_wready_o,
    input  wire  [11:0] ov_pend_i,
    input  wire         seed_we_i,
    input  wire         seed_sel_i,
    input  wire  [1:0]  seed_idx_i,
    input  wire  [63:0] seed_data_i,
    output wire  [5:0]  cnt_ntt_o,
    output wire  [5:0]  cnt_intt_o,
    output wire  [5:0]  cnt_pwm_o,
    output wire  [5:0]  cnt_smp_o,
    output wire         bank_overflow_o
);
  (* anyseq *) wire        f_cfin, f_cwrdy;
  (* anyseq *) wire [11:0] f_drd;
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
  assign busy_o = busy_q;
  assign done_o = done_q;
  assign tb_rdata_o = f_drd;
  assign tb_wready_o = f_cwrdy;   // free (control): the host-write grant depends on the sequencer, not on data
  assign cnt_ntt_o = 6'd0;
  assign cnt_intt_o = 6'd0;
  assign cnt_pwm_o = 6'd0;
  assign cnt_smp_o = 6'd0;
  assign bank_overflow_o = 1'b0;
  wire unused_ok = &{1'b0, ov_pend_i, prog_i, tb_we_i, tb_slot_i, tb_addr_i, tb_wdata_i, seed_we_i, seed_sel_i, seed_idx_i, seed_data_i};
endmodule

module mlkem_ldpoly2o (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         start_i,
    input  wire  [1:0]  dsel_i,
    input  wire  [3:0]  slot_i,
    input  wire  [8:0]  woff_i,
    output wire         rd_req_o,
    output wire  [8:0]  rd_addr_o,
    input  wire  [63:0] rd_data_i,
    input  wire         tb_wready_i,
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
  wire unused_ok = &{1'b0, tb_wready_i, dsel_i, slot_i, woff_i, rd_data_i};
endmodule
`default_nettype wire
