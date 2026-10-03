`default_nettype none
`timescale 1ns/1ps
// rtl/keccak/keccak_f1600_r2.sv
// Phase 8a (docs/evidence/phase08-keccak-stream/8a/test_plan_8a.md V4): iterative Keccak-f[1600], configuration C5: TWO rounds per cycle (two keccak_round instances in series, round constants
// RC[2k] and RC[2k+1] for the cycle counter k = 0..11), exactly 12 cycles per permutation (busy_o high for exactly 12 cycles after a run_i, whatever the state; no early exit, no data-dependent
// condition). done_o is a one-cycle pulse in the cycle after the last cycle is written, when the state already holds the result. Same ports and control as keccak_f1600 (K0).
//   run_i      start a permutation (ignored while busy)
//   clear_i    state <= 0 and drop busy (start of a message, stop, wipe after a digest); wins over everything
//   xor_en_i   state lane xor_lane_i ^= xor_data_i (ignored while busy and for lane >= 25)
//   rd_lane_i  combinational read of one lane
// Reset: asynchronous, active low (rst_ni); the state is wiped as well.

module keccak_f1600_r2 (
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
  logic [1599:0] mid;      // output of the first round of the cycle (also read by the testbench)
  logic [1599:0] round_o;  // output of the second round: next state
  logic [   3:0] rnd_q;    // cycle counter 0..11
  logic          busy_q;
  logic          done_q;

  keccak_round u_round_a (
      .s_i (state_q),
      .rc_i(keccak_rc({rnd_q, 1'b0})),
      .s_o (mid)
  );

  keccak_round u_round_b (
      .s_i (mid),
      .rc_i(keccak_rc({rnd_q, 1'b1})),
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
        if (rnd_q == 4'(ROUNDS / 2 - 1)) begin
          rnd_q  <= '0;
          busy_q <= 1'b0;
          done_q <= 1'b1;
        end else begin
          rnd_q <= rnd_q + 4'd1;
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
