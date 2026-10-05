`default_nettype none
`timescale 1ns/1ps
// rtl/mlkem/mlkem_fo_cmp.sv
// Phase 9b (evidence/phase09/9b/test_plan_9b.md): constant-time comparison of the ciphertext c with the re-encrypted c' and the mask selection of the key (FIPS 203 Algorithm 18 lines 8-11, implicit rejection).
// WORDS beats (default 136 = 1,088 bytes / 8) carry a_data_i (c) and b_data_i (c'); the XOR of every beat is ORed into a 64-bit accumulator: every beat is visited, no early exit, no branch on data. kgood_i (K') and kbad_i (K_bar) must be valid in the cycle of the last
// accepted beat. After that beat done_o pulses once the next cycle, neq_o = 1 if c != c', and k_o = (kgood & ~m) | (kbad & m) with m all ones when the ciphertexts differ; neq_o and k_o are registered and held until the next completed run.
// start_i is accepted only when idle. The beat count and the cycle count depend on the handshake only.
// Reset: asynchronous, active low, on the control state; the accumulator, the result and the key registers are not reset (the accumulator is cleared at start).

module mlkem_fo_cmp #(
    parameter int WORDS = 136
) (
    input  wire          clk_i,
    input  wire          rst_ni,
    input  wire          start_i,
    input  wire          in_valid_i,
    output wire          in_ready_o,
    input  wire  [63:0]  a_data_i,
    input  wire  [63:0]  b_data_i,
    input  wire  [255:0] kgood_i,
    input  wire  [255:0] kbad_i,
    output wire  [255:0] k_o,
    output wire          neq_o,
    output wire          busy_o,
    output wire          done_o
);

  localparam int CNTW = $clog2(WORDS);

  logic          busy_q, done_q;
  logic [CNTW-1:0] cnt_q;
  logic [63:0]   diff_q;
  logic          neq_q;
  logic [255:0]  k_q;

  wire start_ok = start_i && !busy_q;
  assign in_ready_o = busy_q;
  wire take    = in_valid_i && busy_q;
  wire last    = take && (cnt_q == CNTW'(WORDS - 1));
  wire [63:0]  diff_next = diff_q | (a_data_i ^ b_data_i);
  wire         neq_next  = |diff_next;
  wire [255:0] mask      = {256{neq_next}};

  assign k_o    = k_q;
  assign neq_o  = neq_q;
  assign busy_o = busy_q;
  assign done_o = done_q;

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      busy_q <= 1'b0;
      done_q <= 1'b0;
      cnt_q  <= '0;
    end else begin
      done_q <= 1'b0;
      if (start_ok) begin
        busy_q <= 1'b1;
        cnt_q  <= '0;
      end else if (take) begin
        cnt_q <= cnt_q + CNTW'(1);
        if (last) begin
          busy_q <= 1'b0;
          done_q <= 1'b1;
        end
      end
    end
  end

  always_ff @(posedge clk_i) begin
    if (start_ok) diff_q <= 64'd0;
    else if (take) diff_q <= diff_next;
    if (last) begin
      neq_q <= neq_next;
      k_q   <= (kgood_i & ~mask) | (kbad_i & mask);
    end
  end

endmodule
`default_nettype wire
