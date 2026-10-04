`default_nettype none
`timescale 1ns/1ps
// formal/phase09m-optimisation/9m3/keccak_sponge_stub.sv
// Formal-only stand-in for rtl/keccak/keccak_sponge.sv (the K0 sponge; same name and ports; Phase 9M-3: the 9b stub of the C5 sponge under the K0 name, same protocol) in the proof of rtl/mlkem/mlkem_hash.sv: it keeps the sponge's *protocol* and nothing else, as the real sponge shows it to a user (see its header and the Phase 8a proofs K4 and K5):
//   start_i while idle makes it busy (mode latched); after a free number of cycles it offers digest words (out_valid_o, free data), holds a word (valid and data stable) until out_ready_i;
//   a fixed-output mode (0, 1) has 4 or 8 words, out_last_o on the last, and returns to idle in the cycle after the last word is taken; a SHAKE mode offers words until stop_i; stop_i returns to idle in the next cycle from any state.
// The real sponge with its 1,600-bit state made the induction of the wrapper too slow (the first proof run was stopped after 30 minutes at induction step 20); digests are covered by simulation against hashlib, the sponge's own control by Phase 8a formal.
// Not part of the synthesised design.

module keccak_sponge (
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

  (* anyseq *) wire        f_go, f_ready, f_offer;
  (* anyseq *) wire [63:0] f_data;
  (* anyseq *) wire [15:0] f_perm;

  typedef enum logic [1:0] {S_IDLE, S_ABS, S_SQ} st_e;
  st_e        st_q;
  logic [1:0] mode_q;
  logic [3:0] w_q;
  logic       v_q;
  logic [63:0] d_q;

  wire fixed_out = !mode_q[1];
  wire [3:0] ow_last = mode_q[0] ? 4'd7 : 4'd3;
  wire offer = (st_q == S_SQ) && (v_q || f_offer);
  wire [63:0] data = v_q ? d_q : f_data;
  wire take = offer && out_ready_i;
  wire last = fixed_out && (w_q == ow_last);

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      st_q <= S_IDLE;
      mode_q <= 2'd0;
      w_q <= 4'd0;
      v_q <= 1'b0;
      d_q <= '0;
    end else if (stop_i) begin
      st_q <= S_IDLE;
      w_q <= 4'd0;
      v_q <= 1'b0;
    end else begin
      case (st_q)
        S_IDLE: if (start_i) begin
          st_q <= S_ABS;
          mode_q <= mode_i;
          w_q <= 4'd0;
          v_q <= 1'b0;
        end
        S_ABS: if (f_go) st_q <= S_SQ;
        default: begin
          v_q <= offer && !out_ready_i;
          d_q <= data;
          if (take) begin
            if (last) begin
              st_q <= S_IDLE;
              w_q <= 4'd0;
            end else begin
              w_q <= w_q + 4'd1;
            end
          end
        end
      endcase
    end
  end

  assign in_ready_o  = f_ready && (st_q == S_ABS);
  assign out_valid_o = offer;
  assign out_data_o  = data;
  assign out_last_o  = offer && last;
  assign busy_o      = (st_q != S_IDLE);
  assign perm_cnt_o  = f_perm;

  wire unused_ok = &{1'b0, len_i, in_valid_i, in_data_i};

endmodule
`default_nettype wire
