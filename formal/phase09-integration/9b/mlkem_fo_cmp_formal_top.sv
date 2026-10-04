`default_nettype none
`timescale 1ns/1ps
// formal/phase09-integration/9b/mlkem_fo_cmp_formal_top.sv
// Phase 9b test V8 (docs/evidence/phase09-integration/9b/test_plan_9b.md): control and result properties of rtl/mlkem/mlkem_fo_cmp.sv (WORDS = 8 here: the properties do not depend on the count) with free inputs.
//   F1  at most WORDS beats accepted per run; no beat accepted while idle; done_o exactly one cycle after the last accepted beat, one pulse, only when not busy
//   F2  neq_o and k_o do not change except at the last accepted beat (they are held between runs)
//   F3  the accumulator equals the OR of the XORs of the accepted beats; neq_o equals (accumulator != 0)
//   F4  k_o equals the key chosen by neq_o from the two keys that were valid at the last beat: neq_o ? kbad : kgood (mask select, bit exact)
// Control and result only for the select; the compare of values is covered by simulation and by the model.

module mlkem_fo_cmp_formal_top (
    input  wire          clk_i,
    input  wire          rst_ni,
    input  wire          start_i,
    input  wire          in_valid_i,
    input  wire  [63:0]  a_data_i,
    input  wire  [63:0]  b_data_i,
    input  wire  [255:0] kgood_i,
    input  wire  [255:0] kbad_i,
    output wire          in_ready_o,
    output wire  [255:0] k_o,
    output wire          neq_o,
    output wire          busy_o,
    output wire          done_o
);

  localparam int WORDS = 8;
  localparam int CW = $clog2(WORDS);

  mlkem_fo_cmp #(.WORDS(WORDS)) u_dut (
      .clk_i(clk_i), .rst_ni(rst_ni), .start_i(start_i), .in_valid_i(in_valid_i), .in_ready_o(in_ready_o),
      .a_data_i(a_data_i), .b_data_i(b_data_i), .kgood_i(kgood_i), .kbad_i(kbad_i),
      .k_o(k_o), .neq_o(neq_o), .busy_o(busy_o), .done_o(done_o));

`ifdef FORMAL
  logic f_init = 1'b1;
  always_ff @(posedge clk_i) f_init <= 1'b0;
  always_comb if (f_init) assume (!rst_ni);

  logic [4:0]   nin;          // beats accepted this run
  logic [63:0]  accb;         // OR of the XORs of the accepted beats
  logic         p_ok, p_last, p_done;
  logic         p_neq;
  logic [255:0] p_k, p_kg, p_kb;
  wire          f_start_ok = start_i && !busy_o;
  wire          take = in_valid_i && in_ready_o;
  wire          f_last = take && (nin == 5'(WORDS - 1));

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      nin <= '0;
      accb <= '0;
      p_ok <= 1'b0;
      p_last <= 1'b0;
      p_done <= 1'b0;
      p_neq <= 1'b0;
      p_k <= '0;
      p_kg <= '0;
      p_kb <= '0;
    end else begin
      if (f_start_ok) begin
        nin <= '0;
        accb <= '0;
      end else if (take) begin
        nin <= nin + 5'd1;
        accb <= accb | (a_data_i ^ b_data_i);
      end
      p_ok <= 1'b1;
      p_last <= f_last;
      p_done <= done_o;
      p_neq <= neq_o;
      p_k <= k_o;
      p_kg <= kgood_i;
      p_kb <= kbad_i;
    end
  end

  always_ff @(posedge clk_i) begin
    if (rst_ni) begin
      // supporting invariants
      if (busy_o) begin
        assert (u_dut.cnt_q == nin[CW-1:0]);
        assert (nin < 5'(WORDS));
        assert (u_dut.diff_q == accb);
      end
      // F1
      if (!busy_o) assert (!in_ready_o);
      if (done_o) begin
        assert (!busy_o);
        assert (p_ok && p_last);
        assert (!p_done);
      end
      if (p_ok && p_last) assert (done_o);
      // F2
      if (p_ok && !p_last) begin
        assert (neq_o == p_neq);
        assert (k_o == p_k);
      end
      // reachability (anti-vacuity): both outcomes are reachable (run with mlkem_fo_cmp_cover.sby)
      cover (done_o && neq_o);
      cover (done_o && !neq_o);
      // F3 and F4 (the cycle after the last beat: the result registers show the selection of that beat)
      if (p_ok && p_last) begin
        assert (neq_o == (u_dut.diff_q != 64'd0));
        assert (k_o == (neq_o ? p_kb : p_kg));
      end
    end
  end
`endif

endmodule
`default_nettype wire
