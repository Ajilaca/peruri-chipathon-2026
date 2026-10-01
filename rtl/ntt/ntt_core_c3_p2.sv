`default_nettype none
`timescale 1ns/1ps
// rtl/ntt/ntt_core_c3_p2.sv
// Thin Quartus top-level wrapper: rtl/ntt/ntt_core_c3.sv at NUM_LANES = 8 with the register positions
// fixed for P = 2 in docs/evidence/phase04-pipeline/test_plan.md section 2 (cuts A_13, D_3).
// Same port list as rtl/ntt/ntt_core_c2_k2_k1_l8.sv (the P = 0 reference), so all Phase 4 revisions are
// compiled with identical constraints and virtual pins. No logic here.

module ntt_core_c3_p2 (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         mode_i,
    input  wire         start_i,
    input  wire  [7:0]  host_addr_i,
    input  wire  [11:0] host_wdata_i,
    input  wire         host_we_i,
    output logic [11:0] host_rdata_o,
    output logic        busy_o,
    output logic        done_o,
    output logic        bank_overflow_o
);

  ntt_core_c3 #(
      .NUM_LANES(8),
      .ARB_REG  (33'd1 << 13),
      .MUL_REG  (14'd1 << 3)
  ) u_core (
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

endmodule
`default_nettype wire
