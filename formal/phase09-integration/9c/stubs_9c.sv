`default_nettype none
`timescale 1ns/1ps
// formal/phase09-integration/9c/stubs_9c.sv
// Formal-only stand-ins (same module names, parameters and ports) for the sub-blocks of rtl/mlkem/mlkem_core.sv in the proof of the controller: the K-PKE engine (kpke_smp_top_s10), the hash wrapper (mlkem_hash), the comparison (mlkem_fo_cmp) and the two
// polynomial task modules (mlkem_ldpoly, mlkem_stpoly). Each keeps only the *protocol* the controller sees (start while idle makes it busy; it finishes after a free number of cycles with a one-cycle done pulse where the real block has one) and nothing else.
// Free signals are declared `(* anyseq *) wire` (a `logic` that is read only in procedural code is not free in yosys-slang: see docs/evidence/phase09-integration/9b/formal_vacuity_check_2026-10-03.md). The signals named f_c* are CONTROL (handshakes, strobes, addresses,
// counters): the proof assumes them equal in the two copies of the miter; the signals named f_d* are DATA: they differ between the copies. Not part of the synthesised design.

module kpke_smp_top_s10 #(
    parameter int NPOLY    = 24,
    parameter int VAR      = 0,
    parameter bit STREAM_A = 1'b0,
    parameter bit OVERLAP  = 1'b0,
    parameter bit CORE_R2  = 1'b1,
    parameter bit NTT_P6   = 1'b0,  // Phase 9F S2: accepted and ignored (the stub is protocol-level; the NTT length is not modelled)
    parameter bit NTT_AR   = 1'b0   // Phase 9F S2b: accepted and ignored
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
  (* anyseq *) wire        f_cfin;
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
  assign cnt_ntt_o = 6'd0;
  assign cnt_intt_o = 6'd0;
  assign cnt_pwm_o = 6'd0;
  assign cnt_smp_o = 6'd0;
  assign bank_overflow_o = 1'b0;
  wire unused_ok = &{1'b0, prog_i, tb_we_i, tb_slot_i, tb_addr_i, tb_wdata_i, seed_we_i, seed_sel_i, seed_idx_i, seed_data_i};
endmodule

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
  (* anyseq *) wire        f_cinr, f_cov, f_ccl, f_cfin;
  (* anyseq *) wire [63:0] f_dod;
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
  assign in_ready_o  = busy_q && f_cinr;
  assign out_valid_o = busy_q && f_cov;
  assign out_data_o  = f_dod;
  assign out_last_o  = busy_q && f_ccl;
  assign busy_o = busy_q;
  assign done_o = done_q;
  wire unused_ok = &{1'b0, sel_i, len_i, in_valid_i, in_data_i, out_ready_i};
endmodule

module mlkem_fo_cmp #(
    parameter int WORDS = 136
) (
    input  wire          clk_i,
    input  wire          rst_ni,
    input  wire          start_i,
    input  wire          in_valid_i,
    output wire          in_ready_o,
    input  wire  [63:0]  a_data_i,
    input  wire  [63:0]  b_data_i,
    input  wire  [255:0] kgood_i,
    input  wire  [255:0] kbad_i,
    output wire  [255:0] k_o,
    output wire          neq_o,
    output wire          busy_o,
    output wire          done_o
);
  (* anyseq *) wire         f_cfin;
  (* anyseq *) wire [255:0] f_dk;
  (* anyseq *) wire         f_dneq;
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
  assign in_ready_o = busy_q;
  assign k_o = f_dk;
  assign neq_o = f_dneq;
  assign busy_o = busy_q;
  assign done_o = done_q;
  wire unused_ok = &{1'b0, in_valid_i, a_data_i, b_data_i, kgood_i, kbad_i};
endmodule

module mlkem_ldpoly (
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

module mlkem_stpoly (
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
