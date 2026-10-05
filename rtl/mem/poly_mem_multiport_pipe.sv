`default_nettype none
`timescale 1ns/1ps
// rtl/mem/poly_mem_multiport_pipe.sv
// Phase 4 (ADR 0007, evidence/phase04/test_plan.md): the banked multi-port polynomial
// memory of rtl/mem/poly_mem_multiport.sv (which stays frozen), restructured for a pipelined
// butterfly. Same storage (256 x 12 bit in NUM_LANES banks, flip-flops), same bank mapping
// (rtl/mem/bank_map_rom.sv), same slot rule (the first two enabled ports that land on a bank get its
// sub-ports 0 and 1; a third is an overflow), but an access is now a transaction in time:
//
//   cycle t              request: en_i / wr_i / addr_i per port
//   cycle t + RdLat      rdata_o for that request            (RdLat = bits set in ARB_REG)
//   cycle t + RdLat + WR_DELAY
//                        the write of that request, if wr_i was set: data taken from wdata_i in
//                        THAT cycle, to the address given at cycle t
//
// so a read and the write-back of an earlier request use different addresses in the same cycle.
//
// Slot arbitration is a ripple over the ports (port 0 first). ARB_REG[k] = 1 puts a register stage
// after k ports have been processed (k = 1 .. 2*NUM_LANES; k = 2*NUM_LANES is the stage after the whole
// arbitration, cut "M" in the test plan, smaller k are the cuts "A_k"). This path depends only on the
// addresses, never on polynomial data. The (bank, offset, slot) found for a request's read is delayed
// and reused for its write, so writes need no second arbitration.
//
// The caller's contract is unchanged in substance: at most two enabled ports per bank per request cycle
// (checked, and flagged on bank_overflow_o, RdLat cycles after the offending request), and no read of
// an address whose write is still in flight (the schedule guarantees it:
// evidence/phase04/layer_boundary_slack.txt; the testbench scoreboard checks it).
//
// Reset (asynchronous, active low): only the enable / write-enable bits of the control pipeline, so no
// write can fire after reset. Addresses, slots and data are unreset.

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module poly_mem_multiport_pipe #(
    parameter int          NUM_LANES = 8,
    parameter logic [32:0] ARB_REG   = 33'd0,
    parameter int          WR_DELAY  = 0
) (
    input  wire                       clk_i,
    input  wire                       rst_ni,

    input  wire  [2*NUM_LANES-1:0]    en_i,      // request: port in use
    input  wire  [2*NUM_LANES-1:0]    wr_i,      // request: this access will write back
    input  wire  [2*NUM_LANES*AW-1:0] addr_i,    // request: address, port i at [i*AW +: AW]
    output logic [2*NUM_LANES*CW-1:0] rdata_o,   // RdLat cycles after the request
    input  wire  [2*NUM_LANES*CW-1:0] wdata_i,   // sampled RdLat + WR_DELAY cycles after the request

    output logic                      bank_overflow_o   // must stay 0
);

  localparam int NumPorts = 2 * NUM_LANES;
  localparam int BankAW   = (N / NUM_LANES > 1) ? $clog2(N / NUM_LANES) : 1;
  localparam int BankSelW = (NUM_LANES > 1) ? $clog2(NUM_LANES) : 1;

  // ---- request: address -> (bank, offset) ------------------------------------------------------
  logic [NumPorts*BankSelW-1:0] bank_rq;
  logic [NumPorts*BankAW-1:0]   off_rq;

  genvar gp;
  generate
    for (gp = 0; gp < NumPorts; gp++) begin : g_map
      bank_map_rom #(.NUM_BANKS(NUM_LANES)) u_map (
          .addr_i  (addr_i[gp*AW +: AW]),
          .bank_o  (bank_rq[gp*BankSelW +: BankSelW]),
          .offset_o(off_rq[gp*BankAW +: BankAW])
      );
    end
  endgenerate

  // ---- slot arbitration: ripple over the ports, optional register after any port ---------------
  // Index k of these arrays = state after k ports have been processed.
  logic [NumPorts-1:0]          en_s    [0:NumPorts] /* verilator split_var */;
  logic [NumPorts-1:0]          wr_s    [0:NumPorts] /* verilator split_var */;
  logic [NumPorts*BankSelW-1:0] bank_s  [0:NumPorts] /* verilator split_var */;
  logic [NumPorts*BankAW-1:0]   off_s   [0:NumPorts] /* verilator split_var */;
  logic [NumPorts*2-1:0]        slot_s  [0:NumPorts] /* verilator split_var */;   // per port: 0 / 1 = sub-port, 2 = none
  logic [NUM_LANES*2-1:0]       count_s [0:NumPorts] /* verilator split_var */;   // per bank: ports seen so far (saturating)

  assign en_s[0]    = en_i;
  assign wr_s[0]    = wr_i;
  assign bank_s[0]  = bank_rq;
  assign off_s[0]   = off_rq;
  assign slot_s[0]  = '0;
  assign count_s[0] = '0;

  genvar gk;
  generate
    for (gk = 0; gk < NumPorts; gk++) begin : g_arb
      logic [BankSelW-1:0]    bi;
      logic [1:0]             cnt;
      logic [NumPorts*2-1:0]  slot_c;
      logic [NUM_LANES*2-1:0] count_in, count_c;

      assign count_in = count_s[gk];

      always_comb begin
        bi      = bank_s[gk][gk*BankSelW +: BankSelW];
        cnt     = count_in[32'(bi)*2 +: 2];
        slot_c  = slot_s[gk];
        count_c = count_in;
        if (en_s[gk][gk]) begin
          slot_c[gk*2 +: 2] = (cnt < 2'd2) ? cnt : 2'd2;
          if (cnt < 2'd3) count_c[32'(bi)*2 +: 2] = cnt + 2'd1;
        end else begin
          slot_c[gk*2 +: 2] = 2'd2;                // disabled port: no sub-port
        end
      end

      if (ARB_REG[gk+1]) begin : g_reg
        logic [NumPorts-1:0]          en_q, wr_q;
        logic [NumPorts*BankSelW-1:0] bank_q;
        logic [NumPorts*BankAW-1:0]   off_q;
        logic [NumPorts*2-1:0]        slot_q;
        logic [NUM_LANES*2-1:0]       count_q;
        always_ff @(posedge clk_i or negedge rst_ni) begin
          if (!rst_ni) begin
            en_q <= '0;
            wr_q <= '0;
          end else begin
            en_q <= en_s[gk];
            wr_q <= wr_s[gk];
          end
        end
        always_ff @(posedge clk_i) begin
          bank_q  <= bank_s[gk];
          off_q   <= off_s[gk];
          slot_q  <= slot_c;
          count_q <= count_c;
        end
        assign en_s[gk+1]    = en_q;
        assign wr_s[gk+1]    = wr_q;
        assign bank_s[gk+1]  = bank_q;
        assign off_s[gk+1]   = off_q;
        assign slot_s[gk+1]  = slot_q;
        assign count_s[gk+1] = count_q;
      end else begin : g_wire
        assign en_s[gk+1]    = en_s[gk];
        assign wr_s[gk+1]    = wr_s[gk];
        assign bank_s[gk+1]  = bank_s[gk];
        assign off_s[gk+1]   = off_s[gk];
        assign slot_s[gk+1]  = slot_c;
        assign count_s[gk+1] = count_c;
      end
    end
  endgenerate

  // ---- read stage (the request of RdLat cycles ago) --------------------------------------------
  logic [NumPorts-1:0]          en_r, wr_r;
  logic [NumPorts*BankSelW-1:0] bank_r;
  logic [NumPorts*BankAW-1:0]   off_r;
  logic [NumPorts*2-1:0]        slot_r;

  assign en_r   = en_s[NumPorts];
  assign wr_r   = wr_s[NumPorts];
  assign bank_r = bank_s[NumPorts];
  assign off_r  = off_s[NumPorts];
  assign slot_r = slot_s[NumPorts];

  always_comb begin
    bank_overflow_o = 1'b0;
    for (int i = 0; i < NumPorts; i++) begin
      if (en_r[i] && slot_r[i*2 +: 2] == 2'd2) bank_overflow_o = 1'b1;
    end
  end

  // ---- write control: the read stage's control, WR_DELAY cycles later --------------------------
  logic [NumPorts-1:0]          wv_rd, wv_w;      // write valid per port
  logic [NumPorts-1:0]          wsub_rd, wsub_w;  // which sub-port (slot bit 0)
  logic [NumPorts*BankSelW-1:0] bank_w;
  logic [NumPorts*BankAW-1:0]   off_w;

  always_comb begin
    for (int i = 0; i < NumPorts; i++) begin
      wv_rd[i]   = en_r[i] && wr_r[i] && (slot_r[i*2 +: 2] != 2'd2);
      wsub_rd[i] = slot_r[i*2];
    end
  end

  pipe_delay #(.W(NumPorts), .STAGES(WR_DELAY), .HAS_RST(1'b1)) u_dly_wv (
      .clk_i(clk_i), .rst_ni(rst_ni), .d_i(wv_rd), .q_o(wv_w));
  pipe_delay #(.W(NumPorts), .STAGES(WR_DELAY), .HAS_RST(1'b0)) u_dly_wsub (
      .clk_i(clk_i), .rst_ni(1'b1), .d_i(wsub_rd), .q_o(wsub_w));
  pipe_delay #(.W(NumPorts*BankSelW), .STAGES(WR_DELAY), .HAS_RST(1'b0)) u_dly_bank (
      .clk_i(clk_i), .rst_ni(1'b1), .d_i(bank_r), .q_o(bank_w));
  pipe_delay #(.W(NumPorts*BankAW), .STAGES(WR_DELAY), .HAS_RST(1'b0)) u_dly_off (
      .clk_i(clk_i), .rst_ni(1'b1), .d_i(off_r), .q_o(off_w));

  // ---- banks: 2 read sub-ports + 2 write sub-ports each ----------------------------------------
  logic [NUM_LANES*2*CW-1:0] bank_rdata;   // bank b, sub-port s: [(b*2+s)*CW +: CW]

  genvar gb;
  generate
    for (gb = 0; gb < NUM_LANES; gb++) begin : g_bank
      logic [CW-1:0]     mem [0:(N / NUM_LANES) - 1];
      logic [BankAW-1:0] raddr0, raddr1, waddr0, waddr1;
      logic              we0, we1;
      logic [CW-1:0]     wdata0, wdata1;

      always_comb begin
        raddr0 = '0; raddr1 = '0;
        for (int i = 0; i < NumPorts; i++) begin
          if (en_r[i] && bank_r[i*BankSelW +: BankSelW] == gb[BankSelW-1:0]) begin
            if (slot_r[i*2 +: 2] == 2'd0)      raddr0 = off_r[i*BankAW +: BankAW];
            else if (slot_r[i*2 +: 2] == 2'd1) raddr1 = off_r[i*BankAW +: BankAW];
          end
        end
      end

      always_comb begin
        we0 = 1'b0; waddr0 = '0; wdata0 = '0;
        we1 = 1'b0; waddr1 = '0; wdata1 = '0;
        for (int i = 0; i < NumPorts; i++) begin
          if (wv_w[i] && bank_w[i*BankSelW +: BankSelW] == gb[BankSelW-1:0]) begin
            if (!wsub_w[i]) begin
              we0 = 1'b1; waddr0 = off_w[i*BankAW +: BankAW]; wdata0 = wdata_i[i*CW +: CW];
            end else begin
              we1 = 1'b1; waddr1 = off_w[i*BankAW +: BankAW]; wdata1 = wdata_i[i*CW +: CW];
            end
          end
        end
      end

      assign bank_rdata[(gb*2+0)*CW +: CW] = mem[raddr0];
      assign bank_rdata[(gb*2+1)*CW +: CW] = mem[raddr1];

      always_ff @(posedge clk_i) begin
        if (we0) mem[waddr0] <= wdata0;
        if (we1) mem[waddr1] <= wdata1;
      end
    end
  endgenerate

  generate
    for (gp = 0; gp < NumPorts; gp++) begin : g_rdout
      logic [BankSelW-1:0] rd_bank;
      logic                rd_sub;
      assign rd_bank = bank_r[gp*BankSelW +: BankSelW];
      assign rd_sub  = slot_r[gp*2];
      assign rdata_o[gp*CW +: CW] = bank_rdata[(32'(rd_bank)*2 + 32'(rd_sub))*CW +: CW];
    end
  endgenerate

endmodule
`default_nettype wire
