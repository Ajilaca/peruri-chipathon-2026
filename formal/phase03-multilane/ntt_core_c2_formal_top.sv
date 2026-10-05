`default_nettype none
`timescale 1ns/1ps
// formal/phase03-multilane/ntt_core_c2_formal_top.sv
// Re-runs Phase 1's CRG-8 FSM safety property (formal/phase01-ntt/ntt_core_props.sv, reused
// unchanged) against rtl/ntt/ntt_core_c2.sv, plus a Phase 3-specific property: the multi-port
// memory's bank_overflow_o (rtl/mem/poly_mem_multiport.sv) must never assert -- the formal
// counterpart to the exhaustive Python proof
// (evidence/phase03/lane_schedule_verification.txt) that the lane
// schedule never puts more than 2 ports on the same bank in one cycle, now checked against the
// actual generated bank_map_rom.sv contents, not the Python model. NUM_LANES is overridden per
// run by `-G NUM_LANES=<L>` on the read_slang line of each formal/phase03-multilane/*.sby script.

module ntt_core_c2_formal_top #(
    parameter int NUM_LANES = 1
) (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         mode_i,
    input  wire         start_i,
    input  wire  [7:0]  host_addr_i,
    input  wire  [11:0] host_wdata_i,
    input  wire         host_we_i,
    output wire  [11:0] host_rdata_o,
    output wire          busy_o,
    output wire          done_o,
    output wire          bank_overflow_o
);

  ntt_core_c2 #(.NUM_LANES(NUM_LANES)) u_dut (
      .clk_i          (clk_i),
      .rst_ni         (rst_ni),
      .mode_i         (mode_i),
      .start_i        (start_i),
      .host_addr_i    (host_addr_i),
      .host_wdata_i   (host_wdata_i),
      .host_we_i      (host_we_i),
      .host_rdata_o   (host_rdata_o),
      .busy_o         (busy_o),
      .done_o         (done_o),
      .bank_overflow_o(bank_overflow_o)
  );

  ntt_core_props u_props (
      .clk_i  (clk_i),
      .rst_ni (rst_ni),
      .busy_o (busy_o),
      .done_o (done_o)
  );

`ifdef FORMAL
  // First-cycle reset assumption. Written with a flag register instead of `initial assume (!rst_ni);`
  // because the yosys-slang frontend rejects an initial-block read of an input net.
  logic f_init = 1'b1;
  always_ff @(posedge clk_i) f_init <= 1'b0;
  always_comb if (f_init) assume (!rst_ni);
  always_ff @(posedge clk_i) begin
    if (rst_ni) assert (!bank_overflow_o);
  end
`endif

endmodule
`default_nettype wire
