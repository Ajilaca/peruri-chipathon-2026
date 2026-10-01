`default_nettype none
`timescale 1ns/1ps
// formal/phase05-arith/ntt_core_c4_formal_top.sv
// Phase 5 formal top (docs/evidence/phase05-arith/test_plan.md, V8): the Phase 4 top
// formal/phase04-pipeline/ntt_core_c3_formal_top.sv (frozen) with the Phase 5 Quartus wrappers in place of the
// C3 ones, selected with `-G V=<n>` (0 = rtl/ntt/ntt_core_c4a.sv,
// 1 = rtl/ntt/ntt_core_c4b_b.sv, 2 = rtl/ntt/ntt_core_c4b_m.sv). Every C4 wrapper keeps P = 6 with three cuts
// before the read and three after it (ADR 0011 D5), so P = 6 and RdLat = 3 are fixed here. Properties, delay
// model and negative-control hook (F_SKEW) are the Phase 4 ones unchanged:
//   H  busy_o drop -> done_o one cycle later           (formal/phase01-ntt/ntt_core_props.sv, reused)
//   O  bank_overflow_o == 0
//   R  counter ranges (asserted inside rtl/ntt/ntt_core_c4.sv, same as ntt_core_c3.sv)
//   A  every memory write fires exactly P cycles after its request
//   B  drained: in S_DONE no write requested in the last P cycles is outstanding, and no write fires
//   C  no read and write of one storage location in the same cycle for transform traffic
// Control and bank capacity only; nothing here proves NTT/INTT arithmetic or memory data.

module ntt_core_c4_formal_top #(
    parameter int V      = 0,
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
  localparam int BankSelW = 3;
  localparam int BankAW   = 5;
  localparam int P        = 6;
  localparam int RdLat    = 3;     // cuts A_4, A_11, M before the read; three in the multiplier path
  localparam int Pipe     = P;
  // ntt_core_c4.state_t encoding (= ntt_core_c3's) (S_IDLE, S_RUN, S_SCALE, S_DRAIN, S_DONE)
  localparam logic [2:0] SRun = 3'd1, SScale = 3'd2, SDone = 3'd4;

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

  generate
    if (V == 0) begin : g_c4a
      ntt_core_c4a u_dut (`C3_DUT_PORTS);
      `C3_PROBES
    end else if (V == 1) begin : g_c4bb
      ntt_core_c4b_b u_dut (`C3_DUT_PORTS);
      `C3_PROBES
    end else begin : g_c4bm
      ntt_core_c4b_m u_dut (`C3_DUT_PORTS);
      `C3_PROBES
    end
  endgenerate

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
  assign f_busy_h[0] = (f_state == SRun) || (f_state == SScale);

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
