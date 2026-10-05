`default_nettype none
`timescale 1ns/1ps
// rtl/keccak/keccak_sponge_r2.sv
// Phase 8a (evidence/phase08/8a/test_plan_8a.md V5): copy of keccak_sponge.sv (K0) on top of keccak_f1600_r2 (two rounds per cycle, configuration C5); same FSM and ports.
// Modes (mode_i): 0 SHA3-256 (rate 136 B), 1 SHA3-512 (72 B), 2 SHAKE128 (168 B), 3 SHAKE256 (136 B).
// Message: len_i bytes (public), taken as ceil(len / 8) 64-bit words, byte k of a word is message byte 8w + k; bytes past len in the last word are ignored.
// Padding (domain byte 0x06 for SHA3, 0x1F for SHAKE, final 0x80) is applied in hardware by XOR into the lanes. The number of absorb permutations is
// floor(len / rate) + 1; the control never looks at message data.
// Output: SHA3 gives 4 / 8 words with out_last_o on the last, then IDLE. SHAKE squeezes until stop_i (a new permutation after every rate-words block).
// stop_i returns to IDLE from any state on the next cycle and wipes the state; so does the last SHA3 word. start_i is accepted only in IDLE.
// Cycles per permutation as seen by this controller: 1 (run) + 12 (busy_o of keccak_f1600_r2) + 1 (done) = 14: measured in test V6, not tuned.
// Reset: asynchronous, active low.

module keccak_sponge_r2 (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         start_i,
    input  wire  [ 1:0] mode_i,
    input  wire  [15:0] len_i,
    input  wire         stop_i,
    input  wire         in_valid_i,
    output wire         in_ready_o,
    input  wire  [63:0] in_data_i,
    output wire         out_valid_o,
    input  wire         out_ready_i,
    output wire  [63:0] out_data_o,
    output wire         out_last_o,
    output wire         busy_o,
    output wire  [15:0] perm_cnt_o
);

  typedef enum logic [2:0] {
    S_IDLE    = 3'd0,
    S_ABSORB  = 3'd1,
    S_PAD2    = 3'd2,
    S_PERM    = 3'd3,
    S_SQUEEZE = 3'd4
  } state_e;

  state_e       st_q;
  logic [  1:0] mode_q;
  logic [ 15:0] rem_q;      // message bytes not yet absorbed
  logic [  4:0] widx_q;     // word index inside the current block
  logic         fin_q;      // the message is absorbed: permutations return to SQUEEZE
  logic         started_q;  // run_i already issued for the current permutation
  logic [ 15:0] perm_cnt_q;

  logic [4:0] rw, last_lane, ow_last;
  logic [7:0] ds;
  logic       fixed_out;

  always_comb begin
    case (mode_q)
      2'd0:    rw = 5'd17;
      2'd1:    rw = 5'd9;
      2'd2:    rw = 5'd21;
      default: rw = 5'd17;
    endcase
    ds        = mode_q[1] ? 8'h1F : 8'h06;
    fixed_out = !mode_q[1];
    ow_last   = mode_q[0] ? 5'd7 : 5'd3;  // 8 or 4 digest words, minus one
  end
  assign last_lane = rw - 5'd1;

  // keccak_f1600 control
  logic        f_run, f_clear, f_xor_en, f_busy, f_done;
  logic [ 4:0] f_xor_lane;
  logic [63:0] f_xor_data, f_rd;

  keccak_f1600_r2 u_f (
      .clk_i     (clk_i),
      .rst_ni    (rst_ni),
      .run_i     (f_run),
      .clear_i   (f_clear),
      .xor_en_i  (f_xor_en),
      .xor_lane_i(f_xor_lane),
      .xor_data_i(f_xor_data),
      .rd_lane_i (widx_q),
      .rd_data_o (f_rd),
      .busy_o    (f_busy),
      .done_o    (f_done)
  );

  wire        whole = |rem_q[15:3];  // at least 8 message bytes left
  wire [ 5:0] sh = {rem_q[2:0], 3'b000};
  wire [63:0] keep = ~(64'hFFFF_FFFF_FFFF_FFFF << sh);
  wire [63:0] pad_hi = (widx_q == last_lane) ? 64'h8000_0000_0000_0000 : 64'h0;
  wire [63:0] final_word = (in_data_i & keep) | ({56'd0, ds} << sh) | pad_hi;

  assign in_ready_o = (st_q == S_ABSORB) && (rem_q != 16'd0);
  wire take = in_valid_i && in_ready_o;
  wire whole_take = take && whole;
  wire final_cyc = (st_q == S_ABSORB) && !whole && ((rem_q == 16'd0) || in_valid_i);
  wire sq_take = (st_q == S_SQUEEZE) && out_ready_i;
  wire sha3_done = sq_take && fixed_out && (widx_q == ow_last);
  wire start_ok = start_i && (st_q == S_IDLE) && !stop_i;

  assign f_clear = stop_i || start_ok || sha3_done;
  assign f_run = (st_q == S_PERM) && !started_q;
  assign f_xor_en = whole_take || final_cyc || (st_q == S_PAD2);
  assign f_xor_lane = (st_q == S_PAD2) ? last_lane : widx_q;
  assign f_xor_data = (st_q == S_PAD2) ? 64'h8000_0000_0000_0000 : whole ? in_data_i : final_word;

  assign out_valid_o = (st_q == S_SQUEEZE);
  assign out_data_o = f_rd;
  assign out_last_o = (st_q == S_SQUEEZE) && fixed_out && (widx_q == ow_last);
  assign busy_o = (st_q != S_IDLE);
  assign perm_cnt_o = perm_cnt_q;

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      st_q       <= S_IDLE;
      mode_q     <= 2'd0;
      rem_q      <= 16'd0;
      widx_q     <= 5'd0;
      fin_q      <= 1'b0;
      started_q  <= 1'b0;
      perm_cnt_q <= 16'd0;
    end else if (stop_i) begin
      st_q      <= S_IDLE;
      widx_q    <= 5'd0;
      started_q <= 1'b0;
    end else begin
      case (st_q)
        S_IDLE: begin
          if (start_ok) begin
            st_q       <= S_ABSORB;
            mode_q     <= mode_i;
            rem_q      <= len_i;
            widx_q     <= 5'd0;
            fin_q      <= 1'b0;
            started_q  <= 1'b0;
            perm_cnt_q <= 16'd0;
          end
        end
        S_ABSORB: begin
          if (whole_take) begin
            rem_q <= rem_q - 16'd8;
            if (widx_q == last_lane) begin
              widx_q <= 5'd0;
              st_q   <= S_PERM;
            end else begin
              widx_q <= widx_q + 5'd1;
            end
          end else if (final_cyc) begin
            rem_q <= 16'd0;
            fin_q <= 1'b1;
            if (widx_q == last_lane) begin
              widx_q <= 5'd0;
              st_q   <= S_PERM;
            end else begin
              st_q <= S_PAD2;
            end
          end
        end
        S_PAD2: begin
          widx_q <= 5'd0;
          st_q   <= S_PERM;
        end
        S_PERM: begin
          if (f_run) started_q <= 1'b1;
          if (f_done) begin
            started_q  <= 1'b0;
            perm_cnt_q <= perm_cnt_q + 16'd1;
            if (fin_q) st_q <= S_SQUEEZE;
            else st_q <= S_ABSORB;
          end
        end
        S_SQUEEZE: begin
          if (sq_take) begin
            if (fixed_out) begin
              if (widx_q == ow_last) begin
                st_q   <= S_IDLE;
                widx_q <= 5'd0;
              end else begin
                widx_q <= widx_q + 5'd1;
              end
            end else if (widx_q == last_lane) begin
              widx_q <= 5'd0;
              st_q   <= S_PERM;
            end else begin
              widx_q <= widx_q + 5'd1;
            end
          end
        end
        default: st_q <= S_IDLE;
      endcase
    end
  end

  wire unused_ok = &{1'b0, f_busy};

endmodule

`default_nettype wire
