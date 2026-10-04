`default_nettype none
`timescale 1ns/1ps
// formal/phase09m-optimisation/9m3/mlkem_hash_k0_formal_top.sv
// Phase 9M-3 test V5 (docs/evidence/phase09m-optimisation/9m3/test_plan_9m3.md): the Phase 9b properties H1-H5 of rtl/mlkem/mlkem_hash.sv with CORE_R2 = 0 (K0 sponge instance, replaced by its protocol stub) with free inputs (any start, sel, len, valid, data, ready).
//   H1  at most 4 / 8 / 4 digest words accepted per run (H / G / J); out_last_o exactly on the last of them
//   H2  done_o only after exactly that many words were accepted; one pulse; only when not busy
//   H3  an unaccepted digest word is held: out_valid_o, out_data_o and out_last_o stay stable until out_ready_i
//   H4  no output and no input acceptance while idle
//   H5  after the last digest word the sponge is idle (the SHAKE256 squeeze was stopped): fin_q implies the sponge is not busy
// Control only; nothing here proves digest values (simulation against hashlib covers that).

module mlkem_hash_k0_formal_top (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         start_i,
    input  wire  [1:0]  sel_i,
    input  wire  [15:0] len_i,
    input  wire         in_valid_i,
    input  wire  [63:0] in_data_i,
    input  wire         out_ready_i,
    output wire         in_ready_o,
    output wire         out_valid_o,
    output wire  [63:0] out_data_o,
    output wire         out_last_o,
    output wire         busy_o,
    output wire         done_o
);

  mlkem_hash #(.CORE_R2(1'b0)) u_dut (
      .clk_i(clk_i), .rst_ni(rst_ni), .start_i(start_i), .sel_i(sel_i), .len_i(len_i),
      .in_valid_i(in_valid_i), .in_ready_o(in_ready_o), .in_data_i(in_data_i),
      .out_valid_o(out_valid_o), .out_ready_i(out_ready_i), .out_data_o(out_data_o), .out_last_o(out_last_o),
      .busy_o(busy_o), .done_o(done_o));

`ifdef FORMAL
  logic f_init = 1'b1;
  always_ff @(posedge clk_i) f_init <= 1'b0;
  always_comb if (f_init) assume (!rst_ni);

  logic [3:0]  nacc;          // digest words accepted this run
  logic [1:0]  sel_b;         // sel latched at the accepted start
  logic        p_ok, p_valid, p_ready, p_last;
  logic [63:0] p_data;
  wire         f_start_ok = start_i && !busy_o;
  wire [3:0]   nw = (sel_b == 2'd1) ? 4'd8 : 4'd4;

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      nacc <= '0;
      sel_b <= '0;
      p_ok <= 1'b0;
      p_valid <= 1'b0;
      p_ready <= 1'b0;
      p_last <= 1'b0;
      p_data <= '0;
    end else begin
      if (f_start_ok) begin
        nacc <= '0;
        sel_b <= sel_i;
      end else if (out_valid_o && out_ready_i) begin
        nacc <= nacc + 4'd1;
      end
      p_ok <= 1'b1;
      p_valid <= out_valid_o;
      p_ready <= out_ready_i;
      p_last <= out_last_o;
      p_data <= out_data_o;
    end
  end

  logic p_done;
  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) p_done <= 1'b0;
    else p_done <= done_o;
  end

  always_ff @(posedge clk_i) begin
    if (rst_ni) begin
      // supporting invariants for the protocol stub: its state is consistent with the wrapper's (counter, latched mode); a busy sponge implies a busy wrapper
      if (u_dut.g_k0.u_sp.st_q != 2'd0) begin
        assert (busy_o);
        assert (u_dut.g_k0.u_sp.mode_q == ((u_dut.sel_q == 2'd0) ? 2'd0 : (u_dut.sel_q == 2'd1) ? 2'd1 : 2'd3));
      end
      if (u_dut.g_k0.u_sp.st_q == 2'd1) begin
        assert (u_dut.g_k0.u_sp.w_q == 4'd0);
        assert (u_dut.wcnt_q == 4'd0);
        assert (!u_dut.fin_q);
      end
      if (u_dut.g_k0.u_sp.st_q == 2'd2) begin
        assert (u_dut.g_k0.u_sp.w_q == u_dut.wcnt_q);
        assert (!u_dut.fin_q);
      end
      // supporting invariants: the wrapper's counter and latched mode equal the black-box ones
      if (busy_o) begin
        assert (u_dut.wcnt_q == nacc);
        assert (u_dut.sel_q == sel_b);
        assert (u_dut.fin_q == (nacc == nw));
      end
      // H1
      if (busy_o) begin
        assert (nacc <= nw);
        if (out_valid_o) begin
          assert (nacc < nw);
          assert (out_last_o == (nacc == nw - 4'd1));
        end
      end
      // H2
      if (done_o) begin
        assert (!busy_o);
        assert (nacc == nw);
        assert (!p_done);
      end
      // H3
      if (p_ok && p_valid && !p_ready && !f_start_ok) begin
        assert (out_valid_o);
        assert (out_data_o == p_data);
        assert (out_last_o == p_last);
      end
      // H4
      if (!busy_o) begin
        assert (!out_valid_o);
        assert (!in_ready_o);
      end
      // reachability (anti-vacuity): the states the properties are about are reachable (run with mlkem_hash_cover.sby)
      cover (busy_o && out_valid_o && nacc == 4'd3);
      cover (done_o && sel_b == 2'd0);
      cover (done_o && sel_b == 2'd1);
      cover (done_o && sel_b[1]);
      // H5
      if (u_dut.fin_q) assert (!u_dut.sp_busy);
    end
  end
`endif

endmodule
`default_nettype wire
