`default_nettype none
`timescale 1ns/1ps
// rtl/mem/poly_mem_m10k.sv
// S10 (docs/evidence/phase06-scheduling/test_plan_s10.md, ADR 0024, ADR 0022 option A): polynomial memory of the NTT core as 16 banks of 16 x 12 bit, one read and one
// write per bank per cycle, without slot arbitration. Same port list as rtl/mem/poly_mem_multiport_split.sv. Bank map (S9 study, conflict-free over the whole L = 8
// schedule of both directions, docs/evidence/phase05m-memsched/s9/port_analysis_2026-10-03.txt):
//
//   bank(a)   = {a[1]^a[2]^a[3]^a[4], a[7], a[6], a[5]}        offset(a) = a[3:0]
//
//   cycle t                     request (en_i / wr_i / addr_i per port); each bank takes the offset of the one port that addresses it (AND-OR select) into its RAM
//                               at the end of cycle t (physical read in the request cycle)
//   cycle t + 1                 per port, the data of its bank are selected and registered
//   cycle t + RD_LAT            rdata_o for that request (RD_LAT >= 2; extra stages are plain registers)
//   cycle t + RD_LAT + WR_DELAY the write of that request, if wr_i was set: data taken from wdata_i in THAT cycle, to the (bank, offset) of the request
//
// Contract: at most one enabled port per bank per request cycle (the schedule guarantees it; bank_overflow_o, registered, flags a violation one cycle later), and no
// read of an address whose write is still in flight (the core's schedule; the testbench scoreboard checks it). The selection logic depends only on addresses, never on
// polynomial data. Reset (asynchronous, active low): the write-valid chain and the overflow flag only, so no write can fire after reset. Storage and data are unreset.

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module poly_mem_m10k #(
    parameter int NUM_LANES = 8,
    parameter int RD_LAT    = 2,
    parameter int WR_DELAY  = 0
) (
    input  wire                       clk_i,
    input  wire                       rst_ni,

    input  wire  [2*NUM_LANES-1:0]    en_i,
    input  wire  [2*NUM_LANES-1:0]    wr_i,
    input  wire  [2*NUM_LANES*AW-1:0] addr_i,
    output logic [2*NUM_LANES*CW-1:0] rdata_o,
    input  wire  [2*NUM_LANES*CW-1:0] wdata_i,

    output logic                      bank_overflow_o
);

  localparam int NumPorts = 2 * NUM_LANES;   // 16
  localparam int NumBanks = 16;
  localparam int BankSelW = 4;
  localparam int BankAW   = $clog2(N / NumBanks);   // 4: 16 words per bank
  localparam int WrLat    = RD_LAT + WR_DELAY;

  function automatic logic [BankSelW-1:0] f_bank(input logic [AW-1:1] a);   // address bit 0 does not enter the bank
    f_bank = {a[1] ^ a[2] ^ a[3] ^ a[4], a[7], a[6], a[5]};
  endfunction

  // ---- request stage: (bank, offset) per port -------------------------------------------------------------
  logic [NumPorts*BankSelW-1:0] bank_r;      // "read stage" = request stage here (physical read in the request cycle)
  logic [NumPorts*BankAW-1:0]   off_r;
  logic [NumPorts-1:0]          en_r;
  assign en_r = en_i;

  genvar gp, gb;
  generate
    for (gp = 0; gp < NumPorts; gp++) begin : g_req
      assign bank_r[gp*BankSelW +: BankSelW] = f_bank(addr_i[gp*AW+1 +: AW-1]);
      assign off_r [gp*BankAW   +: BankAW]   = addr_i[gp*AW +: BankAW];
    end
  endgenerate

  // ---- write stage: the request's control delayed by RD_LAT + WR_DELAY ---------------------------------------
  logic [NumPorts-1:0]          wv_w;
  logic [NumPorts*BankSelW-1:0] bank_w;
  logic [NumPorts*BankAW-1:0]   off_w;

  pipe_delay #(.W(NumPorts), .STAGES(WrLat), .HAS_RST(1'b1)) u_dly_wv (
      .clk_i(clk_i), .rst_ni(rst_ni), .d_i(en_i & wr_i), .q_o(wv_w));
  pipe_delay #(.W(NumPorts * (BankSelW + BankAW)), .STAGES(WrLat), .HAS_RST(1'b0)) u_dly_bo (
      .clk_i(clk_i), .rst_ni(1'b1), .d_i({bank_r, off_r}), .q_o({bank_w, off_w}));

  // ---- banks -------------------------------------------------------------------------------------------------
  logic [CW-1:0] bank_q [0:NumBanks-1];     // read data of each bank, one cycle after the request

  generate
    for (gb = 0; gb < NumBanks; gb++) begin : g_bank
      logic [BankAW-1:0] ra, wa;
      logic [CW-1:0]     wd;
      logic              we;

      always_comb begin
        ra = '0;
        wa = '0;
        wd = '0;
        we = 1'b0;
        for (int p = 0; p < NumPorts; p++) begin
          if (en_r[p] && bank_r[p*BankSelW +: BankSelW] == BankSelW'(gb)) ra = ra | off_r[p*BankAW +: BankAW];
          if (wv_w[p] && bank_w[p*BankSelW +: BankSelW] == BankSelW'(gb)) begin
            wa = wa | off_w[p*BankAW +: BankAW];
            wd = wd | wdata_i[p*CW +: CW];
            we = 1'b1;
          end
        end
      end

      (* ramstyle = "M10K, no_rw_check" *) logic [CW-1:0] mem [0:(1 << BankAW)-1];

      always_ff @(posedge clk_i) begin
        if (we) mem[wa] <= wd;
        bank_q[gb] <= mem[ra];
      end
    end
  endgenerate

  // ---- per port: select the data of its bank, register, extra stages ------------------------------------------
  logic [NumPorts*BankSelW-1:0] bank_d1;
  logic [NumPorts*CW-1:0]       rsel_c, rsel_q;

  always_ff @(posedge clk_i) bank_d1 <= bank_r;

  generate
    for (gp = 0; gp < NumPorts; gp++) begin : g_rsel
      assign rsel_c[gp*CW +: CW] = bank_q[bank_d1[gp*BankSelW +: BankSelW]];
    end
  endgenerate

  always_ff @(posedge clk_i) rsel_q <= rsel_c;

  pipe_delay #(.W(NumPorts * CW), .STAGES(RD_LAT - 2), .HAS_RST(1'b0)) u_dly_rd (
      .clk_i(clk_i), .rst_ni(1'b1), .d_i(rsel_q), .q_o(rdata_o));

  // ---- diagnostic: two or more enabled ports on one bank in one request cycle ---------------------------------
  logic ovf_c;
  always_comb begin
    ovf_c = 1'b0;
    for (int b = 0; b < NumBanks; b++) begin
      int n;
      n = 0;
      for (int p = 0; p < NumPorts; p++)
        if (en_r[p] && bank_r[p*BankSelW +: BankSelW] == BankSelW'(b)) n = n + 1;
      if (n > 1) ovf_c = 1'b1;
    end
  end

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) bank_overflow_o <= 1'b0;
    else         bank_overflow_o <= ovf_c;
  end

endmodule
`default_nettype wire
