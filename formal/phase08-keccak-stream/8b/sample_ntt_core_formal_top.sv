`default_nettype none
`timescale 1ns/1ps
// formal/phase08-keccak-stream/8b/sample_ntt_core_formal_top.sv
// Phase 8b test V9 (docs/evidence/phase08-keccak-stream/8b/test_plan_8b.md): control and range properties of rtl/sample/sample_ntt_core.sv with a free input stream (any bytes, any gaps) and free handshakes.
//   S1  coef_data_o < 3329 whenever coef_valid_o
//   S2  at most 256 coefficients are handed over per run; coef_last_o exactly on the 256th (the beat after 255 handed over)
//   S3  a pending output is held: coef_valid_o, coef_data_o and coef_last_o stay stable until coef_ready_i (or abort_i)
//   S4  bytes_o never decreases inside a run and bytes_o plus the bytes in the window never exceed the bytes the stream has delivered
//   S5  legality: valid output only while busy; done_o only when not busy and not valid; fin only while busy; window at most 11 bytes; at most 256 coefficients generated
// Supporting invariants (needed for the induction): n_q equals the handed-over count plus the output register; a candidate marked accepted is below 3329; the output register data is below 3329.
// Control and range only; nothing here proves coefficient values (simulation against the golden covers that).

module sample_ntt_core_formal_top (
    input  wire        clk_i,
    input  wire        rst_ni,
    input  wire        start_i,
    input  wire        abort_i,
    input  wire        in_valid_i,
    input  wire [63:0] in_data_i,
    input  wire        coef_ready_i,
    output wire        in_ready_o,
    output wire        coef_valid_o,
    output wire [11:0] coef_data_o,
    output wire        coef_last_o,
    output wire [15:0] bytes_o,
    output wire        busy_o,
    output wire        fin_o,
    output wire        done_o
);

  sample_ntt_core u_dut (
      .clk_i       (clk_i),
      .rst_ni      (rst_ni),
      .start_i     (start_i),
      .abort_i     (abort_i),
      .in_valid_i  (in_valid_i),
      .in_ready_o  (in_ready_o),
      .in_data_i   (in_data_i),
      .coef_valid_o(coef_valid_o),
      .coef_ready_i(coef_ready_i),
      .coef_data_o (coef_data_o),
      .coef_last_o (coef_last_o),
      .bytes_o     (bytes_o),
      .busy_o      (busy_o),
      .fin_o       (fin_o),
      .done_o      (done_o)
  );

  // probes (read only)
  wire [ 8:0] f_n = u_dut.n_q;
  wire [ 3:0] f_cnt = u_dut.cnt_q;
  wire        f_ov = u_dut.ov_q;
  wire [11:0] f_od = u_dut.od_q;
  wire        f_tv = u_dut.tv_q;
  wire        f_a1 = u_dut.a1_q;
  wire        f_a2 = u_dut.a2_q;
  wire [11:0] f_d1 = u_dut.d1_q;
  wire [11:0] f_d2 = u_dut.d2_q;
  wire [15:0] f_bytes = u_dut.bytes_q;
  wire        f_busy = u_dut.busy_q;
  wire        f_fin = u_dut.fin_q;
  wire        f_start_ok = u_dut.start_ok && !abort_i;  // abort_i has priority over start in the core
  wire        f_take = u_dut.take;
  localparam logic [11:0] Q = 12'd3329;

`ifdef FORMAL
  logic f_init = 1'b1;
  always_ff @(posedge clk_i) f_init <= 1'b0;
  always_comb if (f_init) assume (!rst_ni);

  // counters of the black-box view, cleared at a start (as the core clears its own)
  logic [ 8:0] nh;  // coefficients handed over this run
  logic [15:0] wt;  // stream words taken this run
  // previous-cycle values
  logic        p_ok, p_valid, p_ready, p_abort, p_last, p_startok;
  logic [11:0] p_data;
  logic [15:0] p_bytes;
  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      nh <= '0;
      wt <= '0;
      p_ok <= 1'b0;
      p_valid <= 1'b0;
      p_ready <= 1'b0;
      p_abort <= 1'b0;
      p_last <= 1'b0;
      p_startok <= 1'b0;
      p_data <= '0;
      p_bytes <= '0;
    end else begin
      if (f_start_ok) begin
        nh <= '0;
        wt <= '0;
      end else begin
        if (coef_valid_o && coef_ready_i) nh <= nh + 9'd1;
        if (f_take) wt <= wt + 16'd1;
      end
      p_ok <= 1'b1;
      p_valid <= coef_valid_o;
      p_ready <= coef_ready_i;
      p_abort <= abort_i;
      p_last <= coef_last_o;
      p_startok <= f_start_ok;
      p_data <= coef_data_o;
      p_bytes <= bytes_o;
    end
  end

  // a run needs at most 8,000 stream words here: bytes_o (16 bit) cannot wrap; stated limit of the proof
  always_comb assume (wt <= 16'd8000);
  always_comb if (!f_start_ok) assume (nh <= 9'd256);

  always_ff @(posedge clk_i) begin
    if (rst_ni) begin
      // S1
      if (coef_valid_o) assert (coef_data_o < Q);
      // S2
      if (f_busy) assert (f_n == nh + 9'(f_ov));
      if (coef_valid_o && f_busy) assert (nh <= 9'd255);
      if (coef_valid_o && f_busy) assert (coef_last_o == (nh == 9'd255));
      // S3
      if (p_ok && p_valid && !p_ready && !p_abort) begin
        assert (coef_valid_o);
        assert (coef_data_o == p_data);
        assert (coef_last_o == p_last);
      end
      // S4
      if (p_ok && !p_startok) assert (bytes_o >= p_bytes);
      assert ({1'b0, f_bytes} + 17'(f_cnt) <= {1'b0, wt[12:0], 3'b000});  // 17 bit: no wrap-around of the sum
      // S5
      if (coef_valid_o) assert (f_busy);
      if (done_o) assert (!f_busy && !coef_valid_o);
      if (f_fin) assert (f_busy);
      assert (f_cnt <= 4'd11);
      assert (f_n <= 9'd256);
      // supporting invariants
      if (f_tv && f_a1) assert (f_d1 < Q);
      if (f_tv && f_a2) assert (f_d2 < Q);
      if (f_ov) assert (f_od < Q);
      if (!f_tv) assert (!f_a1 && !f_a2);
      if (f_busy) assert (f_fin == (f_n == 9'd256));
      if (f_fin) assert (!f_tv && f_cnt == 4'd0);
    end
  end
`endif

endmodule

`default_nettype wire
