`default_nettype none
`timescale 1ns/1ps
// formal/phase07-keccak/keccak_sponge_formal_top.sv
// Phase 7 test V8 (docs/evidence/phase07-keccak/test_plan.md): control properties of rtl/keccak/keccak_sponge.sv with rtl/keccak/keccak_f1600.sv, all inputs free.
//   K1  the permutation counter is in 0..23; once run, busy_o stays high exactly 24 cycles (the counter steps 0, 1, ..., 23 and busy_o drops after 23); done_o is a one-cycle pulse after round 23
//   K2  the sponge never asks for a state xor while the permutation is busy
//   K3  the word index is below the rate of the mode in every state; a xor lane is below the rate; in a fixed-output squeeze the index never passes the last digest word
//   K4  a pending output word is held: out_valid_o stays high and out_data_o stays stable until out_ready_i (or stop_i)
//   K5  state encoding legal; stop_i reaches IDLE in the next cycle
// Supporting invariants (needed for the induction): in PERM the word index is 0; busy_o of the permutation and the run flag only occur in PERM.
// Control only; nothing here proves digest values (simulation against hashlib covers that).

module keccak_sponge_formal_top (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         start_i,
    input  wire  [ 1:0] mode_i,
    input  wire  [15:0] len_i,
    input  wire         stop_i,
    input  wire         in_valid_i,
    input  wire  [63:0] in_data_i,
    input  wire         out_ready_i,
    output wire         in_ready_o,
    output wire         out_valid_o,
    output wire  [63:0] out_data_o,
    output wire         out_last_o,
    output wire         busy_o,
    output wire  [15:0] perm_cnt_o
);

  keccak_sponge u_dut (
      .clk_i      (clk_i),
      .rst_ni     (rst_ni),
      .start_i    (start_i),
      .mode_i     (mode_i),
      .len_i      (len_i),
      .stop_i     (stop_i),
      .in_valid_i (in_valid_i),
      .in_ready_o (in_ready_o),
      .in_data_i  (in_data_i),
      .out_valid_o(out_valid_o),
      .out_ready_i(out_ready_i),
      .out_data_o (out_data_o),
      .out_last_o (out_last_o),
      .busy_o     (busy_o),
      .perm_cnt_o (perm_cnt_o)
  );

  // probes (read only)
  wire [2:0] f_st      = 3'(u_dut.st_q);
  wire [4:0] f_widx    = u_dut.widx_q;
  wire [4:0] f_rw      = u_dut.rw;
  wire [4:0] f_ow_last = u_dut.ow_last;
  wire       f_fixed   = u_dut.fixed_out;
  wire       f_started = u_dut.started_q;
  wire       f_xor_en  = u_dut.f_xor_en;
  wire [4:0] f_xor_ln  = u_dut.f_xor_lane;
  wire       f_run     = u_dut.f_run;
  wire       f_clear   = u_dut.f_clear;
  wire       f_busy    = u_dut.u_f.busy_q;
  wire       f_done    = u_dut.u_f.done_q;
  wire [4:0] f_rnd     = u_dut.u_f.rnd_q;
  localparam logic [2:0] SIdle = 3'd0, SPerm = 3'd3, SSqueeze = 3'd4;

`ifdef FORMAL
  logic f_init = 1'b1;
  always_ff @(posedge clk_i) f_init <= 1'b0;
  always_comb if (f_init) assume (!rst_ni);

  // previous-cycle values
  logic        p_ok, p_busy, p_run, p_clear, p_valid, p_ready, p_stop;
  logic [ 4:0] p_rnd;
  logic [63:0] p_data;
  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      p_ok    <= 1'b0;
      p_busy  <= 1'b0;
      p_run   <= 1'b0;
      p_clear <= 1'b0;
      p_valid <= 1'b0;
      p_ready <= 1'b0;
      p_stop  <= 1'b0;
      p_rnd   <= '0;
      p_data  <= '0;
    end else begin
      p_ok    <= 1'b1;
      p_busy  <= f_busy;
      p_run   <= f_run;
      p_clear <= f_clear;
      p_valid <= out_valid_o;
      p_ready <= out_ready_i;
      p_stop  <= stop_i;
      p_rnd   <= f_rnd;
      p_data  <= out_data_o;
    end
  end

  always_ff @(posedge clk_i) begin
    if (rst_ni) begin
      // K1
      assert (f_rnd <= 5'd23);
      if (!f_busy) assert (f_rnd == 5'd0);
      if (p_ok && !p_clear && p_busy) begin
        if (p_rnd == 5'd23) assert (!f_busy && f_done);
        else assert (f_busy && !f_done && f_rnd == p_rnd + 5'd1);
      end
      if (p_ok && !p_clear && !p_busy && p_run) assert (f_busy && f_rnd == 5'd0);
      if (p_ok && f_done) assert (p_busy && p_rnd == 5'd23);  // done only follows round 23
      // K2
      assert (!(f_xor_en && f_busy));
      // K3
      assert (f_widx < f_rw);
      if (f_xor_en) assert (f_xor_ln < f_rw);
      if (f_st == SSqueeze && f_fixed) assert (f_widx <= f_ow_last);
      // supporting invariants
      if (f_st == SPerm) assert (f_widx == 5'd0);
      if (f_busy) assert (f_st == SPerm && f_started);
      if (f_started) assert (f_st == SPerm);
      // K4
      if (p_ok && p_valid && !p_ready && !p_stop) begin
        assert (out_valid_o);
        assert (out_data_o == p_data);
      end
      // K5
      assert (f_st <= SSqueeze);
      if (p_ok && p_stop) assert (f_st == SIdle && !busy_o);
    end
  end
`endif

endmodule

`default_nettype wire
