`default_nettype none
`timescale 1ns/1ps
// rtl/ntt/pipe_delay.sv
// Phase 4: a W-bit value delayed by STAGES clock cycles (STAGES = 0: plain wire). Used for the control and
// data side-channels that must stay aligned with the pipelined butterfly
// (evidence/phase04/test_plan.md).
// Reset: HAS_RST = 1 clears every stage on the asynchronous active-low reset (for valid / write-enable
// bits, which must not fire after reset); HAS_RST = 0 leaves the stages unreset (plain data).

module pipe_delay #(
    parameter int W       = 1,
    parameter int STAGES  = 0,
    parameter bit HAS_RST = 1'b0
) (
    input  wire          clk_i,
    input  wire          rst_ni,
    input  wire  [W-1:0] d_i,
    output logic [W-1:0] q_o
);

  logic [W-1:0] st [0:STAGES];
  assign st[0] = d_i;

  genvar gi;
  generate
    for (gi = 0; gi < STAGES; gi++) begin : g_st
      logic [W-1:0] q;
      if (HAS_RST) begin : g_rst
        always_ff @(posedge clk_i or negedge rst_ni) begin
          if (!rst_ni) q <= '0;
          else         q <= st[gi];
        end
      end else begin : g_norst
        always_ff @(posedge clk_i) q <= st[gi];
      end
      assign st[gi+1] = q;
    end
  endgenerate

  assign q_o = st[STAGES];

  // clk_i / rst_ni are unused for STAGES = 0 or HAS_RST = 0
  logic unused_ck_rst;
  assign unused_ck_rst = clk_i ^ rst_ni;

endmodule
`default_nettype wire
