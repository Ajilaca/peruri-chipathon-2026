`default_nettype none
`timescale 1ns/1ps
// rtl/sched/kpke_sched_top_s10.sv
// S10 test V6 (evidence/phase06/test_plan_s10.md): rtl/sched/kpke_sched_top.sv with the S10 core (rtl/ntt/ntt_core_s10_p5.sv, host read latency 2)
// instead of S7. Same port list; the sequencer is unchanged (CORE_RDLAT = 2). No logic here.

module kpke_sched_top_s10 (
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
    output logic [5:0]  cnt_ntt_o,
    output logic [5:0]  cnt_intt_o,
    output logic [5:0]  cnt_pwm_o,
    output logic        bank_overflow_o
);

  logic        core_mode, core_start, core_hwe, core_busy, core_done;
  logic [7:0]  core_haddr;
  logic [11:0] core_hwdata, core_hrdata;

  kpke_sched #(.NPOLY(24), .CORE_RDLAT(2)) u_sched (
      .clk_i(clk_i), .rst_ni(rst_ni), .prog_i(prog_i), .start_i(start_i), .busy_o(busy_o), .done_o(done_o),
      .tb_we_i(tb_we_i), .tb_slot_i(tb_slot_i), .tb_addr_i(tb_addr_i), .tb_wdata_i(tb_wdata_i), .tb_rdata_o(tb_rdata_o),
      .cnt_ntt_o(cnt_ntt_o), .cnt_intt_o(cnt_intt_o), .cnt_pwm_o(cnt_pwm_o),
      .core_mode_o(core_mode), .core_start_o(core_start), .core_haddr_o(core_haddr), .core_hwdata_o(core_hwdata),
      .core_hwe_o(core_hwe), .core_hrdata_i(core_hrdata), .core_busy_i(core_busy), .core_done_i(core_done));

  ntt_core_s10_p5 u_core (
      .clk_i(clk_i), .rst_ni(rst_ni), .mode_i(core_mode), .start_i(core_start),
      .host_addr_i(core_haddr), .host_wdata_i(core_hwdata), .host_we_i(core_hwe), .host_rdata_o(core_hrdata),
      .busy_o(core_busy), .done_o(core_done), .bank_overflow_o(bank_overflow_o));

endmodule
`default_nettype wire
