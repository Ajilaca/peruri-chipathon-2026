`default_nettype none
`timescale 1ns/1ps
// formal/phase09-integration/9a/mlkem_pack_formal_top.sv
// Phase 9a test V9 (docs/evidence/phase09-integration/9a/test_plan_9a.md): control and range properties of rtl/mlkem/mlkem_pack.sv with free inputs (any start, dsel, valid, data, ready).
//   P1  at most 256 coefficients accepted and at most 32 d bytes accepted by the sink per run; byte_last_o exactly on byte 32 d - 1
//   P2  an unaccepted byte is held: byte_valid_o, byte_data_o and byte_last_o stay stable until byte_ready_i
//   P3  no output while idle: byte_valid_o and coef_ready_o only when busy; done_o only when not busy
//   P4  bit balance: bits in the buffer + 8 * bytes accepted = d * coefficients inserted; the buffer holds at most 24 bits
//   P5  coefficients accepted = coefficients inserted + coefficients in the pipeline
// Control and range only; nothing here proves values (simulation against the golden covers that).

module mlkem_pack_formal_top (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         start_i,
    input  wire  [1:0]  dsel_i,
    input  wire         coef_valid_i,
    input  wire  [11:0] coef_data_i,
    input  wire         byte_ready_i,
    output wire         coef_ready_o,
    output wire         byte_valid_o,
    output wire  [7:0]  byte_data_o,
    output wire         byte_last_o,
    output wire         busy_o,
    output wire         done_o
);

  mlkem_pack u_dut (
      .clk_i(clk_i), .rst_ni(rst_ni), .start_i(start_i), .dsel_i(dsel_i),
      .coef_valid_i(coef_valid_i), .coef_ready_o(coef_ready_o), .coef_data_i(coef_data_i),
      .byte_valid_o(byte_valid_o), .byte_ready_i(byte_ready_i), .byte_data_o(byte_data_o), .byte_last_o(byte_last_o),
      .busy_o(busy_o), .done_o(done_o));

`ifdef FORMAL
  logic f_init = 1'b1;
  always_ff @(posedge clk_i) f_init <= 1'b0;
  always_comb if (f_init) assume (!rst_ni);

  // black-box counters of the run (cleared at an accepted start)
  logic [8:0]  nin, nout;
  logic [8:0]  nins;    // coefficients inserted into the buffer this run
  logic        p_ok, p_valid, p_ready, p_last;
  logic [7:0]  p_data;
  wire         f_start_ok = start_i && !u_dut.busy_q;
  wire [3:0]   dv = u_dut.dv_q;

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      nin <= '0;
      nout <= '0;
      nins <= '0;
      p_ok <= 1'b0;
      p_valid <= 1'b0;
      p_ready <= 1'b0;
      p_last <= 1'b0;
      p_data <= '0;
    end else begin
      if (f_start_ok) begin
        nin <= '0;
        nout <= '0;
        nins <= '0;
      end else begin
        if (coef_valid_i && coef_ready_o) nin <= nin + 9'd1;
        if (byte_valid_o && byte_ready_i) nout <= nout + 9'd1;
        if (u_dut.ins) nins <= nins + 9'd1;
      end
      p_ok <= 1'b1;
      p_valid <= byte_valid_o;
      p_ready <= byte_ready_i;
      p_last <= byte_last_o;
      p_data <= byte_data_o;
    end
  end

  // legal values of the latched mode (supporting invariant)
  wire [8:0] nb = u_dut.nbytes_q;
  always_ff @(posedge clk_i) begin
    if (rst_ni) begin
      assert (dv == 4'd1 || dv == 4'd4 || dv == 4'd10 || dv == 4'd12);
      assert (nb == 9'd32 * {5'd0, dv});
      assert (u_dut.cnt_q <= 5'd24);
      if (u_dut.busy_q) begin
        // P1
        // the DUT's own counters equal the black-box ones (supporting invariants for P1)
        assert (u_dut.cin_q == nin);
        assert (u_dut.bout_q == nout);
        assert (nin <= 9'd256);
        assert (nout <= nb);
        if (byte_valid_o) assert (byte_last_o == (nout == nb - 9'd1));
        // P4
        assert ({8'd0, u_dut.cnt_q} + 13'd8 * {4'd0, nout} == {9'd0, dv} * {4'd0, nins});
        // P5
        assert (nin == nins + 9'(u_dut.v1_q) + 9'(u_dut.v2_q) + 9'(u_dut.v3_q));
      end
      // P2
      if (p_ok && p_valid && !p_ready && !f_start_ok) begin
        assert (byte_valid_o);
        assert (byte_data_o == p_data);
        assert (byte_last_o == p_last);
      end
      // P3
      if (byte_valid_o) assert (busy_o);
      if (coef_ready_o) assert (busy_o);
      if (done_o) assert (!busy_o);
    end
  end
`endif

endmodule
`default_nettype wire
