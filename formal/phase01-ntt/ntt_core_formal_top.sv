`default_nettype none
`timescale 1ns/1ps
// formal/phase01-ntt/ntt_core_formal_top.sv
// Wraps rtl/ntt/ntt_core.sv together with its CRG-8 property checker for SymbiYosys. A plain
// top-level instantiation is used instead of `bind` (the oss-cad-suite Yosys build's SV reader
// did not accept the `bind` statement syntax tried here); ntt_core.sv itself carries no
// assertions.

module ntt_core_formal_top (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         mode_i,
    input  wire         start_i,
    input  wire  [7:0]  host_addr_i,
    input  wire  [11:0] host_wdata_i,
    input  wire         host_we_i,
    output wire  [11:0] host_rdata_o,
    output wire         busy_o,
    output wire         done_o
);

  ntt_core u_dut (
      .clk_i        (clk_i),
      .rst_ni       (rst_ni),
      .mode_i       (mode_i),
      .start_i      (start_i),
      .host_addr_i  (host_addr_i),
      .host_wdata_i (host_wdata_i),
      .host_we_i    (host_we_i),
      .host_rdata_o (host_rdata_o),
      .busy_o       (busy_o),
      .done_o       (done_o)
  );

  ntt_core_props u_props (
      .clk_i  (clk_i),
      .rst_ni (rst_ni),
      .busy_o (busy_o),
      .done_o (done_o)
  );

`ifdef FORMAL
  // Standard SymbiYosys reset assumption: without it, the solver is free to pick rst_ni=1 (not
  // in reset) for every step of the trace, including step 0, so every register (including the
  // ones inside ntt_core_props.sv) would start at an arbitrary, never-actually-reset value and
  // trivially "violate" the safety property before the design's own reset logic ever ran.
  initial assume (!rst_ni);
`endif

endmodule
`default_nettype wire
