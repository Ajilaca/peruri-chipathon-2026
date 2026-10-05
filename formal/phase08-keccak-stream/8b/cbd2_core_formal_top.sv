`default_nettype none
`timescale 1ns/1ps
// formal/phase08-keccak-stream/8b/cbd2_core_formal_top.sv
// Phase 8b test V9 (evidence/phase08/8b/test_plan_8b.md): control and range properties of rtl/sample/cbd2_core.sv with a free input stream and free handshakes.
//   S1  coef_data_o < 3329 whenever coef_valid_o
//   S2  at most 256 coefficients are handed over per run; coef_last_o exactly on the 256th; at most 16 stream words are taken per run (the 17th is never taken)
//   S3  a pending output is held until coef_ready_i (or abort_i)
//   S4  bytes_o equals 8 x the words taken and never decreases inside a run
//   S5  legality: valid output only while busy; done_o only when not busy and not valid; fin only while busy; nibble index and word count in range
// Supporting invariants: n_q equals the handed-over count plus the output register; n_q follows the word and nibble position.
// Control and range only; coefficient values are covered by simulation against the golden.

module cbd2_core_formal_top #(
    parameter int OUTW = 1
) (
    input  wire        clk_i,
    input  wire        rst_ni,
    input  wire        start_i,
    input  wire        abort_i,
    input  wire        in_valid_i,
    input  wire [63:0] in_data_i,
    input  wire        coef_ready_i,
    output wire        in_ready_o,
    output wire        coef_valid_o,
    output wire [12*OUTW-1:0] coef_data_o,
    output wire        coef_last_o,
    output wire [15:0] bytes_o,
    output wire        busy_o,
    output wire        fin_o,
    output wire        done_o
);

  cbd2_core #(.OUTW(OUTW)) u_dut (
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
  wire [ 3:0] f_nib = u_dut.nib_q;
  wire [ 4:0] f_wcnt = u_dut.wcnt_q;
  wire        f_wv = u_dut.wv_q;
  wire        f_ov = u_dut.ov_q;
  wire        f_ol = u_dut.ol_q;
  wire [23:0] f_od = 24'(u_dut.od_q);
  wire        f_busy = u_dut.busy_q;
  wire        f_fin = u_dut.fin_q;
  wire        f_start_ok = u_dut.start_ok && !abort_i;  // abort_i has priority over start in the core
  wire        f_take = u_dut.take;
  localparam logic [11:0] Q = 12'd3329;
  wire [23:0] f_dat = 24'(coef_data_o);

`ifdef FORMAL
  logic f_init = 1'b1;
  always_ff @(posedge clk_i) f_init <= 1'b0;
  always_comb if (f_init) assume (!rst_ni);

  logic [ 8:0] nh;  // coefficients handed over this run
  logic [ 5:0] wt;  // stream words taken this run (counts a 17th if the core ever took one)
  logic        p_ok, p_valid, p_ready, p_abort, p_last, p_startok;
  logic [12*OUTW-1:0] p_data;
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
        if (coef_valid_o && coef_ready_i) nh <= nh + 9'(OUTW);
        if (in_valid_i && in_ready_o) wt <= wt + 6'd1;
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

  always_comb if (!f_start_ok) assume (nh <= 9'd256);
  always_comb if (!f_start_ok) assume (wt <= 6'd17);

  always_ff @(posedge clk_i) begin
    if (rst_ni) begin
      // S1
      if (coef_valid_o) begin
        assert (f_dat[11:0] < Q);
        assert (f_dat[23:12] < Q);  // OUTW = 1: the upper lane is zero
      end
      // S2
      if (f_busy) assert (f_n == nh + 9'(OUTW) * 9'(f_ov));
      if (coef_valid_o && f_busy) assert (nh <= 9'(256 - OUTW));
      if (coef_valid_o && f_busy) assert (coef_last_o == (nh == 9'(256 - OUTW)));
      assert (wt <= 6'd16);
      // S3
      if (p_ok && p_valid && !p_ready && !p_abort) begin
        assert (coef_valid_o);
        assert (coef_data_o == p_data);
        assert (coef_last_o == p_last);
      end
      // S4
      if (f_busy) assert (bytes_o == {5'd0, wt[4:0], 3'b000});
      if (p_ok && !p_startok) assert (bytes_o >= p_bytes);
      // S5
      if (coef_valid_o) assert (f_busy);
      if (done_o) assert (!f_busy && !coef_valid_o);
      if (f_fin) assert (f_busy);
      assert (f_wcnt <= 5'd16);
      assert (f_nib <= 4'd15);
      assert (f_n <= 9'd256);
      // supporting invariants
      if (f_busy && !f_fin && f_wv) assert (f_n == {f_wcnt - 5'd1, 4'b0000} + 9'(f_nib));
      if (f_busy && !f_fin && !f_wv) assert (f_n == {f_wcnt, 4'b0000});
      if (f_ov) begin
        assert (f_od[11:0] < Q);
        assert (f_od[23:12] < Q);
      end
      assert (f_nib[0] == 1'b0 || OUTW == 1);  // W2 steps over nibble pairs
      if (f_ov && f_ol) assert (f_n == 9'd256);
      if (f_ov && !f_ol) assert (f_n <= 9'd255);
    end
  end
`endif

endmodule

`default_nettype wire
