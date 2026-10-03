`default_nettype none
`timescale 1ns/1ps
// formal/phase08-keccak-stream/8c/keccak_sampler_stub.sv
// Formal-only stand-in for rtl/sample/keccak_sampler.sv (same name, parameters and ports) in the proofs of the sequencer: it keeps the sampler's *protocol* and nothing else.
//   start_i while idle makes it busy; while busy it may offer a beat (coef_valid_o, free data) and holds the beat (valid and data stable) until coef_ready_i; after 128 beats it stops being busy and done_o pulses
//   in the first idle cycle (the real wrapper clears busy_o and raises done_o on the same edge); no beat is offered when idle or after the 128th; in_ready_o, bytes_o, perm_cnt_o are free.
// Not part of the synthesised design; digests, coefficients and rejection sampling are covered by simulation against the golden model.

module keccak_sampler #(
    parameter bit CORE_R2 = 1'b1,
    parameter int OUTW    = 1
) (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         start_i,
    input  wire         kind_i,
    input  wire  [15:0] len_i,
    input  wire         abort_i,
    input  wire         in_valid_i,
    output wire         in_ready_o,
    input  wire  [63:0] in_data_i,
    output wire         coef_valid_o,
    input  wire         coef_ready_i,
    output wire  [12*OUTW-1:0] coef_data_o,
    output wire         coef_last_o,
    output wire  [15:0] bytes_o,
    output wire         busy_o,
    output wire         done_o,
    output wire  [15:0] perm_cnt_o
);

  (* anyseq *) logic        f_ready, f_offer, f_last;
  (* anyseq *) logic [12*OUTW-1:0] f_data;
  (* anyseq *) logic [15:0] f_bytes, f_perm;

  logic       busy_q, done_q, v_q;
  logic [7:0] nb_q;
  logic [12*OUTW-1:0] d_q;

  wire        offer = busy_q && (nb_q < 8'd128) && (v_q || f_offer);   // a held beat stays offered
  wire [12*OUTW-1:0] data = v_q ? d_q : f_data;
  wire        hand  = offer && coef_ready_i;

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      busy_q <= 1'b0;
      done_q <= 1'b0;
      v_q    <= 1'b0;
      nb_q   <= 8'd0;
      d_q    <= '0;
    end else begin
      done_q <= 1'b0;
      if (start_i && !busy_q) begin
        busy_q <= 1'b1;
        nb_q   <= 8'd0;
        v_q    <= 1'b0;
      end else if (busy_q) begin
        v_q <= offer && !coef_ready_i;
        d_q <= data;
        if (hand) begin
          nb_q <= nb_q + 8'd1;
          if (nb_q == 8'd127) begin
            busy_q <= 1'b0;
            done_q <= 1'b1;
          end
        end
      end
    end
  end

  assign in_ready_o   = f_ready;
  assign coef_valid_o = offer;
  assign coef_data_o  = data;
  assign coef_last_o  = f_last;
  assign bytes_o      = f_bytes;
  assign busy_o       = busy_q;
  assign done_o       = done_q;
  assign perm_cnt_o   = f_perm;

  wire unused_ok = &{1'b0, kind_i, len_i, abort_i, in_valid_i, in_data_i};

endmodule
`default_nettype wire
