`default_nettype none
`timescale 1ns/1ps
// formal/phase06-scheduling/kpke_sched_formal_top.sv
// Phase 6 test plan V7: control properties of rtl/sched/kpke_sched.sv with the NTT core abstracted (its busy / done / read data are free inputs, constrained only to
// the core's own handshake: done never while busy). NPOLY = 1 (slot storage is not part of the properties). Properties:
//   H  busy_o drop -> done_o one cycle later                 (formal/phase01-ntt/ntt_core_props.sv, reused)
//   T  no store write from the testbench port while busy (a write while busy may only come from the read-back or a pass)
//   C  the core's host write only in LOAD, the core's start only in START, never both
//   R  state and counter ranges (asserted inside rtl/sched/kpke_sched.sv)
// Negative-control hook F_TBLEAK = 1: the testbench write enable is OR-ed into the store write while busy (in a test-only copy), so T must fail.

module kpke_sched_formal_top (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire  [1:0]  prog_i,
    input  wire         start_i,
    input  wire         tb_we_i,
    input  wire  [4:0]  tb_slot_i,
    input  wire  [7:0]  tb_addr_i,
    input  wire  [11:0] tb_wdata_i,
    input  wire  [11:0] core_hrdata_i,
    input  wire         core_busy_i,
    input  wire         core_done_i
);

  logic        busy, done, core_mode, core_start, core_hwe;
  logic [7:0]  core_haddr;
  logic [11:0] core_hwdata, tb_rdata;
  logic [5:0]  c_ntt, c_intt, c_pwm;

  kpke_sched #(.NPOLY(1), .CORE_RDLAT(4)) u_dut (
      .clk_i(clk_i), .rst_ni(rst_ni), .prog_i(prog_i), .start_i(start_i), .busy_o(busy), .done_o(done),
      .tb_we_i(tb_we_i), .tb_slot_i(tb_slot_i), .tb_addr_i(tb_addr_i), .tb_wdata_i(tb_wdata_i), .tb_rdata_o(tb_rdata),
      .cnt_ntt_o(c_ntt), .cnt_intt_o(c_intt), .cnt_pwm_o(c_pwm),
      .core_mode_o(core_mode), .core_start_o(core_start), .core_haddr_o(core_haddr), .core_hwdata_o(core_hwdata),
      .core_hwe_o(core_hwe), .core_hrdata_i(core_hrdata_i), .core_busy_i(core_busy_i), .core_done_i(core_done_i));

  ntt_core_props u_props (.clk_i(clk_i), .rst_ni(rst_ni), .busy_o(busy), .done_o(done));

  logic unused;
  assign unused = ^{core_mode, core_haddr, core_hwdata, tb_rdata, c_ntt, c_intt, c_pwm};

`ifdef FORMAL
  logic f_init = 1'b1;
  always_ff @(posedge clk_i) f_init <= 1'b0;
  always_comb if (f_init) assume (!rst_ni);
  always_comb assume (!(core_busy_i && core_done_i));

  logic [2:0] st;
  assign st = 3'(u_dut.state_q);
  // encoding of kpke_sched.state_t: S_IDLE 0, S_FETCH 1, S_LOAD 2, S_START 3, S_RUN 4, S_UNLOAD 5, S_PASS 6, S_DONE 7
  always_ff @(posedge clk_i) begin
    if (rst_ni) begin
      if (busy && st != 3'd5 && st != 3'd6) assert (!u_dut.we_e && !u_dut.we_o);                        // T (and no write in FETCH / LOAD / START / RUN)
      if (busy && st == 3'd5) assert (u_dut.we_e != u_dut.we_o || (!u_dut.we_e && !u_dut.we_o));          // T: read-back writes one half per cycle
      assert (!core_hwe   || st == 3'd2);                                                                   // C
      assert (!core_start || st == 3'd3);                                                                   // C
      assert (!(core_hwe && core_start));                                                                   // C
    end
  end
`endif

endmodule
`default_nettype wire
