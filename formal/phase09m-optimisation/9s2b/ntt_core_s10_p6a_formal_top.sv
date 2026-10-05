`default_nettype none
`timescale 1ns/1ps
// formal/phase09m-optimisation/9s2/ntt_core_s10_p6a_formal_top.sv (Phase 9F step S2, evidence/phase9m/batch2/9s2/test_plan_9s2.md V5; a copy of formal/s10/ntt_core_s10_formal_top.sv with P = 6 and the wrapper parameter P6 = 1)
// original header follows:
// formal/s10/ntt_core_s10_formal_top.sv
// S10 test V5 (evidence/phase06/test_plan_s10.md): the S7 formal top for rtl/ntt/ntt_core_s10_p5.sv (16-bank 1R1W memory, P = 5). Property A uses P = 5; property C
// uses the physical storage read in the request cycle (RdLat = 0); the memory probes have the same names as in the S7 memory, with 4-bit bank and offset fields; property O is the
// new memory's overflow (two ports on one bank).
// Properties, delay model and negative-control hook (F_SKEW):
//   H  busy_o drop -> done_o one cycle later           (formal/phase01-ntt/ntt_core_props.sv, reused)
//   O  bank_overflow_o == 0
//   R  counter ranges (asserted inside rtl/ntt/ntt_core_c4.sv, same as ntt_core_c3.sv)
//   A  every memory write fires exactly P cycles after its request
//   B  drained: in S_DONE no write requested in the last P cycles is outstanding, and no write fires
//   C  no read and write of one storage location in the same cycle for transform traffic
// Control and bank capacity only; nothing here proves NTT/INTT arithmetic or memory data.

module ntt_core_s10_p6a_formal_top #(
    parameter int F_SKEW = 0
) (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         mode_i,
    input  wire         start_i,
    input  wire  [7:0]  host_addr_i,
    input  wire  [11:0] host_wdata_i,
    input  wire         host_we_i,
    output wire  [11:0] host_rdata_o,
    output wire         busy_o,
    output wire         done_o,
    output wire         bank_overflow_o
);

  localparam int NumPorts = 16;   // NUM_LANES = 8 in every wrapper
  localparam int BankSelW = 4;
  localparam int BankAW   = 4;
  localparam int P        = 6;   // S2: the wrapper at P6 = 1 (four multiplier cuts)
  localparam int RdLat    = 0;     // physical storage read in the request cycle
  localparam int Pipe     = P;
  // ntt_core_m6.state_t encoding (S_IDLE = 0, S_RUN = 1, S_DRAIN = 3, S_DONE = 4)
  localparam logic [2:0] SRun = 3'd1, SDone = 3'd4;

  // probes into the design (read only)
  logic [2:0]                   f_state;
  logic [NumPorts-1:0]          f_mem_en, f_mem_wr;      // issue stage
  logic [NumPorts-1:0]          f_en_r;                  // read stage
  logic [NumPorts*BankSelW-1:0] f_bank_r;
  logic [NumPorts*BankAW-1:0]   f_off_r;
  logic [NumPorts-1:0]          f_wv_w;                  // write stage
  logic [NumPorts*BankSelW-1:0] f_bank_w;
  logic [NumPorts*BankAW-1:0]   f_off_w;

`define C3_DUT_PORTS \
      .clk_i(clk_i), .rst_ni(rst_ni), .mode_i(mode_i), .start_i(start_i), \
      .host_addr_i(host_addr_i), .host_wdata_i(host_wdata_i), .host_we_i(host_we_i), \
      .host_rdata_o(host_rdata_o), .busy_o(busy_o), .done_o(done_o), .bank_overflow_o(bank_overflow_o)
`define C3_PROBES \
      assign f_state  = 3'(u_dut.u_core.state_q); \
      assign f_mem_en = u_dut.u_core.mem_en; \
      assign f_mem_wr = u_dut.u_core.mem_wr; \
      assign f_en_r   = u_dut.u_core.u_mem.en_r; \
      assign f_bank_r = u_dut.u_core.u_mem.bank_r; \
      assign f_off_r  = u_dut.u_core.u_mem.off_r; \
      assign f_wv_w   = u_dut.u_core.u_mem.wv_w; \
      assign f_bank_w = u_dut.u_core.u_mem.bank_w; \
      assign f_off_w  = u_dut.u_core.u_mem.off_w;

  ntt_core_s10_p5 #(.P6(1'b1), .AREG(1'b1)) u_dut (`C3_DUT_PORTS);
  `C3_PROBES

  ntt_core_props u_props (
      .clk_i  (clk_i),
      .rst_ni (rst_ni),
      .busy_o (busy_o),
      .done_o (done_o)
  );

  // -- delay model of the requests: index d = d cycles ago (0 = this cycle) ------------------------
  logic [NumPorts-1:0] f_wr_h   [0:Pipe+1];
  logic                f_busy_h [0:Pipe+1];

  assign f_wr_h[0]   = f_mem_en & f_mem_wr;
  assign f_busy_h[0] = (f_state == SRun);

  genvar gd;
  generate
    for (gd = 0; gd <= Pipe; gd++) begin : g_hist
      logic [NumPorts-1:0] wr_q;
      logic                busy_q;
      always_ff @(posedge clk_i or negedge rst_ni) begin
        if (!rst_ni) begin
          wr_q   <= '0;
          busy_q <= 1'b0;
        end else begin
          wr_q   <= f_wr_h[gd];
          busy_q <= f_busy_h[gd];
        end
      end
      assign f_wr_h[gd+1]   = wr_q;
      assign f_busy_h[gd+1] = busy_q;
    end
  endgenerate

`ifdef FORMAL
  // First-cycle reset assumption (flag register: the yosys-slang frontend rejects an initial-block read
  // of an input net).
  logic f_init = 1'b1;
  always_ff @(posedge clk_i) f_init <= 1'b0;
  always_comb if (f_init) assume (!rst_ni);

  logic f_collide;
  always_comb begin
    f_collide = 1'b0;
    for (int i = 0; i < NumPorts; i++) begin
      for (int j = 0; j < NumPorts; j++) begin
        if (f_en_r[i] && f_wv_w[j]
            && f_bank_r[i*BankSelW +: BankSelW] == f_bank_w[j*BankSelW +: BankSelW]
            && f_off_r[i*BankAW +: BankAW] == f_off_w[j*BankAW +: BankAW]) f_collide = 1'b1;
      end
    end
  end

  logic f_outstanding;   // a write requested 1..Pipe cycles ago
  always_comb begin
    f_outstanding = 1'b0;
    for (int d = 1; d <= Pipe; d++) if (f_wr_h[d] != '0) f_outstanding = 1'b1;
  end

  always_ff @(posedge clk_i) begin
    if (rst_ni) begin
      assert (!bank_overflow_o);                                         // O
      assert (f_wv_w == f_wr_h[Pipe - F_SKEW]);                          // A
      if (f_state == SDone) begin                                        // B
        assert (!f_outstanding);
        assert (f_wv_w == '0);
      end
      if (f_busy_h[RdLat] && f_busy_h[Pipe]) assert (!f_collide);        // C
    end
  end
`endif

endmodule
`default_nettype wire
