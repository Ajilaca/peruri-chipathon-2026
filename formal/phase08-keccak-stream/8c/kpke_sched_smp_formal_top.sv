`default_nettype none
`timescale 1ns/1ps
// formal/phase08-keccak-stream/8c/kpke_sched_smp_formal_top.sv
// Phase 8c test V7 (docs/evidence/phase08-keccak-stream/8c/test_plan_8c.md): control properties of rtl/sched/kpke_sched_smp.sv with the NTT core abstracted (free busy / done / read data, never busy and done together) and the sampler replaced by the
// protocol stub keccak_sampler_stub.sv. NPOLY = 1 (slot storage is not part of the properties). Properties:
//   F1  state and counter ranges (asserted inside rtl/sched/kpke_sched_smp.sv), the beat counter and the drain counter in range
//   F2  the seed registers never change while the sequencer is busy (a seed write while busy is ignored)
//   F3  PWMS takes at most 128 beats; a beat is only taken in the PWMS state; the result tags are all empty outside the PWMS state
//   F4  the store write of the sequencer and the store write of a sampler beat never happen in the same cycle
//   F5  the sampler is started only when it is idle and only from the start state of the sequencer
// Control only, not values (simulation against the golden model covers values).

module kpke_sched_smp_formal_top #(
    parameter bit STREAM_A = 1'b1,
    parameter bit OVERLAP  = 1'b0
) (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire  [1:0]  prog_i,
    input  wire         start_i,
    input  wire         tb_we_i,
    input  wire  [4:0]  tb_slot_i,
    input  wire  [7:0]  tb_addr_i,
    input  wire  [11:0] tb_wdata_i,
    input  wire         seed_we_i,
    input  wire         seed_sel_i,
    input  wire  [1:0]  seed_idx_i,
    input  wire  [63:0] seed_data_i,
    input  wire  [11:0] core_hrdata_i,
    input  wire         core_busy_i,
    input  wire         core_done_i
);

  logic        busy, done, core_mode, core_start, core_hwe;
  logic [7:0]  core_haddr;
  logic [11:0] core_hwdata, tb_rdata;
  logic [5:0]  c_ntt, c_intt, c_pwm, c_smp;

  kpke_sched_smp #(.NPOLY(1), .CORE_RDLAT(2), .VAR(STREAM_A ? (OVERLAP ? 2 : 1) : 0), .STREAM_A(STREAM_A), .OVERLAP(OVERLAP), .CORE_R2(1'b1)) u_dut (
      .clk_i(clk_i), .rst_ni(rst_ni), .prog_i(prog_i), .start_i(start_i), .busy_o(busy), .done_o(done),
      .tb_we_i(tb_we_i), .tb_slot_i(tb_slot_i), .tb_addr_i(tb_addr_i), .tb_wdata_i(tb_wdata_i), .tb_rdata_o(tb_rdata),
      .seed_we_i(seed_we_i), .seed_sel_i(seed_sel_i), .seed_idx_i(seed_idx_i), .seed_data_i(seed_data_i),
      .cnt_ntt_o(c_ntt), .cnt_intt_o(c_intt), .cnt_pwm_o(c_pwm), .cnt_smp_o(c_smp),
      .core_mode_o(core_mode), .core_start_o(core_start), .core_haddr_o(core_haddr), .core_hwdata_o(core_hwdata),
      .core_hwe_o(core_hwe), .core_hrdata_i(core_hrdata_i), .core_busy_i(core_busy_i), .core_done_i(core_done_i));

  logic unused;
  assign unused = ^{core_mode, core_start, core_hwe, core_haddr, core_hwdata, tb_rdata, c_ntt, c_intt, c_pwm, c_smp, done};

`ifdef FORMAL
  logic f_init = 1'b1;
  always_ff @(posedge clk_i) f_init <= 1'b0;
  always_comb if (f_init) assume (!rst_ni);
  always_comb assume (!(core_busy_i && core_done_i));

  localparam logic [3:0] SSmps = 4'd7, SSmpr = 4'd8, SPwms = 4'd9;
  logic [3:0] st;
  assign st = 4'(u_dut.state_q);

  logic        p_ok, p_busy;
  logic [63:0] p_rho [0:3];
  logic [63:0] p_sd  [0:3];
  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      p_ok   <= 1'b0;
      p_busy <= 1'b0;
    end else begin
      p_ok   <= 1'b1;
      p_busy <= busy;
    end
  end
  always_ff @(posedge clk_i) begin
    for (int k = 0; k < 4; k++) begin
      p_rho[k] <= u_dut.rho_q[k];
      p_sd[k]  <= u_dut.sd_q[k];
    end
  end

  always_ff @(posedge clk_i) begin
    if (rst_ni) begin
      // F1
      assert (u_dut.bcnt_q <= 8'd128);
      assert (u_dut.drain_q <= 3'd7);
      // F2
      if (p_ok && p_busy && busy) begin
        for (int k = 0; k < 4; k++) begin
          assert (u_dut.rho_q[k] == p_rho[k]);
          assert (u_dut.sd_q[k] == p_sd[k]);
        end
      end
      // F3 (supporting invariant: in a PWMS pass the beat counter equals the beats the sampler has handed over)
      if (STREAM_A && st == SPwms) begin
        assert (u_dut.bcnt_q == u_dut.u_smp.nb_q);
        if (u_dut.bcnt_q < 8'd128) assert (u_dut.smp_pwm_q);   // smp_pwm_q falls with the sampler's done pulse, i.e. during the drain
      end
      if (u_dut.beat) assert (st == SPwms && u_dut.bcnt_q < 8'd128);
      if (st != SPwms) assert (u_dut.tag_v == '0);
      // supporting invariants for the line above: the drain counter is 0 until the last beat; tags younger than the drain counter minus one are empty (no beat after the last)
      if (u_dut.bcnt_q < 8'd128) assert (u_dut.drain_q == 3'd0);
      if (st == SPwms && u_dut.drain_q != 3'd0) assert ((u_dut.tag_v & ((7'd1 << (u_dut.drain_q - 3'd1)) - 7'd1)) == '0);  // drain_q counts from the cycle of the last beat
      // F4 (supporting invariant: without OVERLAP the beat writer is armed only in the blocking sampling state)
      if (!OVERLAP && u_dut.smp_wr_q) assert (st == SSmpr);
      assert (!(u_dut.seq_wr && u_dut.smp_wr));
      // F5
      if (u_dut.smp_start) assert (st == SSmps && !u_dut.smp_busy);
    end
  end
`endif

endmodule
`default_nettype wire
