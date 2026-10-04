`default_nettype none
`timescale 1ns/1ps
// rtl/mlkem/mlkem_fifo4.sv
// Phase 9c: four-entry FIFO, 12 bit, valid / ready on both sides, count_o = entries held. A push into a full FIFO is ignored (the producer must not do it). clear_i empties it. Reset: asynchronous, active low, on the pointers.

module mlkem_fifo4 (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         clear_i,
    input  wire         push_i,
    input  wire  [11:0] din_i,
    output wire         pop_valid_o,
    input  wire         pop_i,
    output wire  [11:0] dout_o,
    output wire  [2:0]  count_o
);

  logic [11:0] mem_q [0:3];
  logic [1:0]  rp_q, wp_q;
  logic [2:0]  cnt_q;

  wire do_push = push_i && (cnt_q != 3'd4);
  wire do_pop  = pop_i && (cnt_q != 3'd0);

  assign pop_valid_o = (cnt_q != 3'd0);
  assign dout_o      = mem_q[rp_q];
  assign count_o     = cnt_q;

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      rp_q  <= 2'd0;
      wp_q  <= 2'd0;
      cnt_q <= 3'd0;
    end else if (clear_i) begin
      rp_q  <= 2'd0;
      wp_q  <= 2'd0;
      cnt_q <= 3'd0;
    end else begin
      if (do_push) wp_q <= wp_q + 2'd1;
      if (do_pop)  rp_q <= rp_q + 2'd1;
      cnt_q <= cnt_q + {2'd0, do_push} - {2'd0, do_pop};
    end
  end

  always_ff @(posedge clk_i) begin
    if (do_push) mem_q[wp_q] <= din_i;
  end

endmodule
`default_nettype wire
