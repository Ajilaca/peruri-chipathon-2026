`default_nettype none
`timescale 1ns/1ps
// formal/phase09-integration/9a/mlkem_unpack_formal_top.sv
// Phase 9a test V9 (docs/evidence/phase09-integration/9a/test_plan_9a.md): control and range properties of rtl/mlkem/mlkem_unpack.sv with free inputs (any start, dsel, valid, data, ready).
//   U1  at most 32 d bytes accepted and at most 256 coefficients handed over per run; coef_last_o exactly on coefficient 255
//   U2  an unaccepted coefficient is held: coef_valid_o, coef_data_o and coef_last_o stay stable until coef_ready_i
//   U3  no output while idle: coef_valid_o and byte_ready_o only when busy; done_o only when not busy
//   U4  bit balance: bits in the buffer + d * coefficients taken = 8 * bytes accepted; the buffer holds at most 24 bits
//   U5  coefficients taken = coefficients handed over + the output register
//   U6  every handed-over coefficient is below 4096 and, for d < 12, below q (range of the decompress result); for d = 12 below q after the reduction
// Control and range only; nothing here proves values (simulation against the golden covers that).

module mlkem_unpack_formal_top (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         start_i,
    input  wire  [1:0]  dsel_i,
    input  wire         byte_valid_i,
    input  wire  [7:0]  byte_data_i,
    input  wire         coef_ready_i,
    output wire         byte_ready_o,
    output wire         coef_valid_o,
    output wire  [11:0] coef_data_o,
    output wire         coef_last_o,
    output wire         busy_o,
    output wire         done_o
);

  mlkem_unpack u_dut (
      .clk_i(clk_i), .rst_ni(rst_ni), .start_i(start_i), .dsel_i(dsel_i),
      .byte_valid_i(byte_valid_i), .byte_ready_o(byte_ready_o), .byte_data_i(byte_data_i),
      .coef_valid_o(coef_valid_o), .coef_ready_i(coef_ready_i), .coef_data_o(coef_data_o), .coef_last_o(coef_last_o),
      .busy_o(busy_o), .done_o(done_o));

`ifdef FORMAL
  logic f_init = 1'b1;
  always_ff @(posedge clk_i) f_init <= 1'b0;
  always_comb if (f_init) assume (!rst_ni);

  logic [8:0]  nbin, nhand, ntake;   // bytes accepted, coefficients handed over, coefficients taken from the buffer (this run)
  logic        p_ok, p_valid, p_ready, p_last;
  logic [11:0] p_data;
  wire         f_start_ok = start_i && !u_dut.busy_q;
  wire [3:0]   dv = u_dut.dv_q;
  wire [8:0]   nb = u_dut.nbytes_q;

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      nbin <= '0;
      nhand <= '0;
      ntake <= '0;
      p_ok <= 1'b0;
      p_valid <= 1'b0;
      p_ready <= 1'b0;
      p_last <= 1'b0;
      p_data <= '0;
    end else begin
      if (f_start_ok) begin
        nbin <= '0;
        nhand <= '0;
        ntake <= '0;
      end else begin
        if (byte_valid_i && byte_ready_o) nbin <= nbin + 9'd1;
        if (coef_valid_o && coef_ready_i) nhand <= nhand + 9'd1;
        if (u_dut.take) ntake <= ntake + 9'd1;
      end
      p_ok <= 1'b1;
      p_valid <= coef_valid_o;
      p_ready <= coef_ready_i;
      p_last <= coef_last_o;
      p_data <= coef_data_o;
    end
  end

  always_ff @(posedge clk_i) begin
    if (rst_ni) begin
      assert (dv == 4'd1 || dv == 4'd4 || dv == 4'd10 || dv == 4'd12);
      assert (nb == 9'd32 * {5'd0, dv});
      assert (u_dut.cnt_q <= 5'd24);
      if (u_dut.busy_q) begin
        // U1
        // the DUT's own counters equal the black-box ones (supporting invariants for U1 and U5)
        assert (u_dut.bin_q == nbin);
        assert (u_dut.cout_q == ntake);
        assert (nbin <= nb);
        assert (nhand <= 9'd256);
        if (coef_valid_o) assert (coef_last_o == (nhand == 9'd255));
        // U4
        assert ({8'd0, u_dut.cnt_q} + {9'd0, dv} * {4'd0, ntake} == 13'd8 * {4'd0, nbin});
        // U5
        assert (ntake == nhand + 9'(u_dut.ov_q));
        assert (ntake <= 9'd256);
      end
      // U2
      if (p_ok && p_valid && !p_ready && !f_start_ok) begin
        assert (coef_valid_o);
        assert (coef_data_o == p_data);
        assert (coef_last_o == p_last);
      end
      // U3
      if (coef_valid_o) assert (busy_o);
      if (byte_ready_o) assert (busy_o);
      if (done_o) assert (!busy_o);
      // U6
      if (coef_valid_o) assert (coef_data_o < 12'd3329);
    end
  end
`endif

endmodule
`default_nettype wire
