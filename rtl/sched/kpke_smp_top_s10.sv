`default_nettype none
`timescale 1ns/1ps
// rtl/sched/kpke_smp_top_s10.sv
// Phases 8c / 8d: Quartus top of the K-PKE arithmetic with sampling: the sequencer rtl/sched/kpke_sched_smp.sv (store, PWM unit, 8b sampler on the C5 sponge) with the S10 NTT/INTT core (rtl/ntt/ntt_core_s10_p5.sv, host read latency 2).
// VAR selects the program ROM variant (0 STORE, 1 STREAM, 2 OVERLAP) at compile time; NPOLY the slots of the store (24 for STORE, 12 for STREAM / OVERLAP); STREAM_A and OVERLAP enable the 8c and 8d hardware. No logic here. NTT_P6 (S2, default 0) selects P = 6 in the NTT core.

module kpke_smp_top_s10 #(
    parameter int NPOLY    = 24,
    parameter int VAR      = 0,
    parameter bit STREAM_A = 1'b0,
    parameter bit OVERLAP  = 1'b0,
    parameter bit CORE_R2  = 1'b1,
    parameter bit NTT_P6   = 1'b0,  // S2: 1 adds the fourth multiplier cut to the NTT core (P = 6)
    parameter bit NTT_AR   = 1'b0   // S2b: 1 registers the issue-stage addresses of the NTT core
) (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire  [1:0]  prog_i,
    input  wire         start_i,
    output logic        busy_o,
    output logic        done_o,
    input  wire         tb_we_i,
    input  wire  [4:0]  tb_slot_i,
    input  wire  [7:0]  tb_addr_i,
    input  wire  [11:0] tb_wdata_i,
    output logic [11:0] tb_rdata_o,
    input  wire         seed_we_i,
    input  wire         seed_sel_i,
    input  wire  [1:0]  seed_idx_i,
    input  wire  [63:0] seed_data_i,
    output logic [5:0]  cnt_ntt_o,
    output logic [5:0]  cnt_intt_o,
    output logic [5:0]  cnt_pwm_o,
    output logic [5:0]  cnt_smp_o,
    output logic        bank_overflow_o
);

  logic        core_mode, core_start, core_hwe, core_busy, core_done;
  logic [7:0]  core_haddr;
  logic [11:0] core_hwdata, core_hrdata;

  kpke_sched_smp #(.NPOLY(NPOLY), .CORE_RDLAT(2), .VAR(VAR), .STREAM_A(STREAM_A), .OVERLAP(OVERLAP), .CORE_R2(CORE_R2)) u_sched (
      .clk_i(clk_i), .rst_ni(rst_ni), .prog_i(prog_i), .start_i(start_i), .busy_o(busy_o), .done_o(done_o),
      .tb_we_i(tb_we_i), .tb_slot_i(tb_slot_i), .tb_addr_i(tb_addr_i), .tb_wdata_i(tb_wdata_i), .tb_rdata_o(tb_rdata_o),
      .seed_we_i(seed_we_i), .seed_sel_i(seed_sel_i), .seed_idx_i(seed_idx_i), .seed_data_i(seed_data_i),
      .cnt_ntt_o(cnt_ntt_o), .cnt_intt_o(cnt_intt_o), .cnt_pwm_o(cnt_pwm_o), .cnt_smp_o(cnt_smp_o),
      .core_mode_o(core_mode), .core_start_o(core_start), .core_haddr_o(core_haddr), .core_hwdata_o(core_hwdata),
      .core_hwe_o(core_hwe), .core_hrdata_i(core_hrdata), .core_busy_i(core_busy), .core_done_i(core_done));

  ntt_core_s10_p5 #(.P6(NTT_P6), .AREG(NTT_AR)) u_core (
      .clk_i(clk_i), .rst_ni(rst_ni), .mode_i(core_mode), .start_i(core_start),
      .host_addr_i(core_haddr), .host_wdata_i(core_hwdata), .host_we_i(core_hwe), .host_rdata_o(core_hrdata),
      .busy_o(core_busy), .done_o(core_done), .bank_overflow_o(bank_overflow_o));

endmodule
`default_nettype wire
