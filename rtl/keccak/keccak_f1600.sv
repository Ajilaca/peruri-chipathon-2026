`default_nettype none
`timescale 1ns/1ps
// rtl/keccak/keccak_f1600.sv
// Phase 7 (test plan V4): iterative Keccak-f[1600], configuration K0: one round per cycle, exactly 24 cycles per permutation (busy_o is high for exactly
// 24 cycles after a run_i, whatever the state; no early exit, no data-dependent condition). done_o is a one-cycle pulse in the cycle after the last round
// is written, when the state already holds the result.
//   run_i      start a permutation (ignored while busy)
//   clear_i    state <= 0 and drop busy (start of a message, stop, wipe after a digest); wins over everything
//   xor_en_i   state lane xor_lane_i ^= xor_data_i (ignored while busy and for lane >= 25)
//   rd_lane_i  combinational read of one lane
// Reset: asynchronous, active low (rst_ni); the state is wiped as well.

module keccak_f1600 (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         run_i,
    input  wire         clear_i,
    input  wire         xor_en_i,
    input  wire  [ 4:0] xor_lane_i,
    input  wire  [63:0] xor_data_i,
    input  wire  [ 4:0] rd_lane_i,
    output logic [63:0] rd_data_o,
    output wire         busy_o,
    output wire         done_o
);

  import keccak_pkg::*;

  logic [1599:0] state_q;
  logic [1599:0] round_o;
  logic [   4:0] rnd_q;
  logic          busy_q;
  logic          done_q;

  keccak_round u_round (
      .s_i (state_q),
      .rc_i(keccak_rc(rnd_q)),
      .s_o (round_o)
  );

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      state_q <= '0;
      rnd_q   <= '0;
      busy_q  <= 1'b0;
      done_q  <= 1'b0;
    end else begin
      done_q <= 1'b0;
      if (clear_i) begin
        state_q <= '0;
        rnd_q   <= '0;
        busy_q  <= 1'b0;
      end else if (busy_q) begin
        state_q <= round_o;
        if (rnd_q == 5'(ROUNDS - 1)) begin
          rnd_q  <= '0;
          busy_q <= 1'b0;
          done_q <= 1'b1;
        end else begin
          rnd_q <= rnd_q + 5'd1;
        end
      end else if (run_i) begin
        busy_q <= 1'b1;
        rnd_q  <= '0;
      end else if (xor_en_i && xor_lane_i < 5'(LANES)) begin
        for (int i = 0; i < LANES; i++)
          if (xor_lane_i == 5'(i)) state_q[64*i+:64] <= state_q[64*i+:64] ^ xor_data_i;
      end
    end
  end

  always_comb begin
    rd_data_o = '0;
    for (int i = 0; i < LANES; i++)
      if (rd_lane_i == 5'(i)) rd_data_o = state_q[64*i+:64];
  end

  assign busy_o = busy_q;
  assign done_o = done_q;

endmodule

`default_nettype wire
