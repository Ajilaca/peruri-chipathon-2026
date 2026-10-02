`default_nettype none
`timescale 1ns/1ps
// rtl/ntt/ntt_core_s7.sv
// Phase 5M step S7 (docs/evidence/phase05m-memsched/test_plan_s7.md, ADR 0017/0019/0020): rtl/ntt/ntt_core_m6.sv (M6: Barrett, INTT without the
// scaling pass) with the memory read split by one register stage (rtl/mem/poly_mem_multiport_split.sv, RD_SPLIT) in place of
// rtl/mem/poly_mem_multiport_pipe.sv. Schedule, address arithmetic, zeta index, layer order, drain, host interface and reset are the M6 text;
// RdLat counts RD_SPLIT, so Pipe = RdLat + WrDly = 7 with the register positions of M6 and the cycle counts become 113 + Pipe = 120 (NTT and INTT).
//
//   RdLat = bits set in ARB_REG  (register stages inside / after the memory's slot arbitration)
//   WrDly = bits set in MUL_REG  (register stages after the multiplier / inside the reducer)
//   Pipe  = RdLat + WrDly        (the "P" of ADR 0007; Phase 5 keeps P = 6, ADR 0011 D5)
//
// Reset: asynchronous, active low, on the FSM state, counters and the memory's write-valid chain.
// Datapath and address pipeline registers are not reset (they cannot cause a write: valid is reset).

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module ntt_core_s7 #(
    parameter int          NUM_LANES = 8,
    parameter logic [32:0] ARB_REG   = 33'd0,   // poly_mem_multiport_pipe.ARB_REG
    parameter int          RD_SPLIT  = 1,       // poly_mem_multiport_split.RD_SPLIT
    parameter logic [15:0] MUL_REG   = 16'd0    // Barrett reducer REG_AFTER
) (
    input  wire           clk_i,
    input  wire           rst_ni,

    input  wire           mode_i,       // 0 = NTT (forward), 1 = INTT (inverse)
    input  wire           start_i,

    input  wire  [AW-1:0] host_addr_i,
    input  wire  [CW-1:0] host_wdata_i,
    input  wire           host_we_i,
    output logic [CW-1:0] host_rdata_o,

    output logic          busy_o,
    output logic          done_o,
    output logic          bank_overflow_o   // diagnostic; must stay 0
);

  function automatic int ones33(input logic [32:0] v);
    int n;
    begin
      n = 0;
      for (int i = 0; i < 33; i++) if (v[i]) n = n + 1;
      ones33 = n;
    end
  endfunction

  localparam int RdLat = ones33(ARB_REG) + RD_SPLIT;   // cycles from a request to its read data
  localparam int WrDly = ones33({17'd0, MUL_REG});
  localparam int Pipe  = RdLat + WrDly;
  localparam int WrEff = WrDly + RD_SPLIT;     // cycles from the physical storage read to the write landing

  // the identity the per-layer halving relies on: 3303 = 2^-7 mod q (7 layers), i.e. 2^7 * INV128 = 1 (mod q). It is checked as a
  // constant here (and in tb/golden/tests/test_intt_halving.py and tb/phase5m/check_half_rom.py); the sink keeps the lint clean.
  localparam bit InvOk = ((128 * INV128) % Q == 1);
  logic unused_inv_ok;
  assign unused_inv_ok = InvOk;

  localparam int TMax = 128 / NUM_LANES - 1;                 // max t_q value
  localparam int TW   = (TMax > 0) ? $clog2(TMax + 1) : 1;
  localparam int DW   = (Pipe > 0) ? $clog2(Pipe + 1) : 1;   // drain / host-write-in-flight counters

  localparam int NumPorts = 2 * NUM_LANES;

  // encoding keeps the values of ntt_core_c4.sv (S_SCALE = 2 is gone and never occurs), so that the Phase 4 test bench and
  // scoreboard, which read state_q, apply unchanged
  typedef enum logic [2:0] {S_IDLE = 3'd0, S_RUN = 3'd1, S_DRAIN = 3'd3, S_DONE = 3'd4} state_t;
  state_t state_q, state_d;

  logic          mode_q;
  logic [2:0]    layer_q, layer_d;
  logic [TW-1:0] t_q, t_d;
  logic [DW-1:0] drain_q, drain_d;
  logic [DW-1:0] hw_q, hw_d;          // cycles until the last host write can no longer be overtaken

  // -- per-layer tables (same values as C0..C2) --------------------------------------------------
  function automatic logic [3:0] f_log2len(input logic mode, input logic [2:0] layer);
    logic [2:0] lay;
    begin
      lay       = (layer > 3'd6) ? 3'd6 : layer;
      f_log2len = mode ? (4'(lay) + 4'd1) : (4'd7 - 4'(lay));
    end
  endfunction

  function automatic logic [6:0] f_cum_inv(input logic [2:0] layer);
    begin
      case (layer)
        3'd0:    f_cum_inv = 7'd0;
        3'd1:    f_cum_inv = 7'd64;
        3'd2:    f_cum_inv = 7'd96;
        3'd3:    f_cum_inv = 7'd112;
        3'd4:    f_cum_inv = 7'd120;
        3'd5:    f_cum_inv = 7'd124;
        default: f_cum_inv = 7'd126;   // layer 6
      endcase
    end
  endfunction

  logic [3:0] log2len;     // issue stage, 1..7
  logic [7:0] len;
  assign log2len = f_log2len(mode_q, layer_q);
  assign len     = 8'd1 << log2len;

  // -- read-stage copies of the schedule position (for the per-lane zeta) ------------------------
  logic [2:0]    layer_r;
  logic [TW-1:0] t_r;
  logic [3:0]    log2len_r;
  logic [6:0]    cum_inv_r;

  pipe_delay #(.W(3 + TW), .STAGES(RdLat), .HAS_RST(1'b0)) u_dly_pos (
      .clk_i(clk_i), .rst_ni(1'b1), .d_i({layer_q, t_q}), .q_o({layer_r, t_r}));

  assign log2len_r = f_log2len(mode_q, layer_r);
  assign cum_inv_r = f_cum_inv(layer_r);

  // -- memory ------------------------------------------------------------------------------------
  logic [NumPorts-1:0]    mem_en;      // issue stage
  logic [NumPorts-1:0]    mem_wr;
  logic [NumPorts*AW-1:0] mem_addr;
  logic [NumPorts*CW-1:0] mem_rdata;   // read stage
  logic [NumPorts*CW-1:0] mem_wdata;   // write stage

  poly_mem_multiport_split #(
      .NUM_LANES(NUM_LANES), .ARB_REG(ARB_REG), .WR_DELAY(WrDly), .RD_SPLIT(RD_SPLIT)
  ) u_mem (
      .clk_i          (clk_i),
      .rst_ni         (rst_ni),
      .en_i           (mem_en),
      .wr_i           (mem_wr),
      .addr_i         (mem_addr),
      .rdata_o        (mem_rdata),
      .wdata_i        (mem_wdata),
      .bank_overflow_o(bank_overflow_o)
  );

  assign host_rdata_o = mem_rdata[0 +: CW];

  // -- port 0's write-data selection, aligned with the write stage -------------------------------
  logic          kind_i, kind_w;      // 1: the write data of port 0 is the butterfly output, 0: the host write data
  logic [CW-1:0] host_wdata_w;

  assign kind_i = (state_q == S_RUN);

  pipe_delay #(.W(1 + CW), .STAGES(Pipe), .HAS_RST(1'b0)) u_dly_kind (
      .clk_i(clk_i), .rst_ni(1'b1), .d_i({kind_i, host_wdata_i}), .q_o({kind_w, host_wdata_w}));

  // -- per-lane address (issue stage), zeta (read stage), butterfly ------------------------------
  logic [NUM_LANES*CW-1:0] bfly_a_o;   // write stage
  logic [NUM_LANES*CW-1:0] bfly_b_o;
  logic                    host_wr_ok;

  assign host_wr_ok = (state_q == S_IDLE) || (state_q == S_DONE);

  genvar gl;
  generate
    for (gl = 0; gl < NUM_LANES; gl++) begin : g_lane
      logic [7:0]    p_lane, block_lane, pos_lane, start_addr_lane;
      logic [AW-1:0] j_lane, jlen_lane;
      logic [7:0]    p_rd;
      logic [ZW-1:0] block_rd;
      logic [ZW-1:0] zeta_idx_lane;
      logic [CW-1:0] rom_zeta_lane;

      always_comb begin
        p_lane          = 8'(gl * (128 / NUM_LANES)) + 8'(t_q);
        block_lane      = p_lane >> log2len;
        pos_lane        = p_lane - (block_lane << log2len);
        start_addr_lane = block_lane << (log2len + 4'd1);
        j_lane          = start_addr_lane + pos_lane;
        jlen_lane       = j_lane + len;
      end

      // zeta_index_of, closed form verified in tb/mem/bank_model.py: NTT k = 2^layer + block;
      // INTT k = 127 - cum_inv[layer] - block (both stay in [1,127]).
      always_comb begin
        p_rd          = 8'(gl * (128 / NUM_LANES)) + 8'(t_r);
        block_rd      = ZW'(p_rd >> log2len_r);
        zeta_idx_lane = mode_q ? (ZW'(127) - cum_inv_r - block_rd)
                               : (ZW'(8'd1 << layer_r) + block_rd);
      end

      twiddle_rom_half u_rom (
          .mode_i(mode_q),
          .addr_i(zeta_idx_lane),
          .zeta_o(rom_zeta_lane)
      );

      butterfly_m6 #(.MUL_REG(MUL_REG)) u_bfly (
          .clk_i  (clk_i),
          .mode_i (mode_q),
          .a_i    (mem_rdata[(2*gl)*CW +: CW]),
          .b_i    (mem_rdata[(2*gl+1)*CW +: CW]),
          .zeta_i (rom_zeta_lane),
          .a_o    (bfly_a_o[gl*CW +: CW]),
          .b_o    (bfly_b_o[gl*CW +: CW])
      );

      // request (issue stage)
      always_comb begin
        if (state_q == S_RUN) begin
          mem_en  [2*gl]               = 1'b1;
          mem_wr  [2*gl]               = 1'b1;
          mem_addr[(2*gl)*AW +: AW]    = j_lane;
          mem_en  [2*gl+1]             = 1'b1;
          mem_wr  [2*gl+1]             = 1'b1;
          mem_addr[(2*gl+1)*AW +: AW]  = jlen_lane;
        end else if (gl == 0) begin
          // Every other state: lane 0's j-port carries the single-address host access; all
          // other ports are disabled, so they never count toward the bank-capacity check.
          mem_en  [2*gl]               = 1'b1;
          mem_wr  [2*gl]               = host_we_i && host_wr_ok;
          mem_addr[(2*gl)*AW +: AW]    = host_addr_i;
          mem_en  [2*gl+1]             = 1'b0;
          mem_wr  [2*gl+1]             = 1'b0;
          mem_addr[(2*gl+1)*AW +: AW]  = '0;
        end else begin
          mem_en  [2*gl]               = 1'b0;
          mem_wr  [2*gl]               = 1'b0;
          mem_addr[(2*gl)*AW +: AW]    = '0;
          mem_en  [2*gl+1]             = 1'b0;
          mem_wr  [2*gl+1]             = 1'b0;
          mem_addr[(2*gl+1)*AW +: AW]  = '0;
        end
      end

      // write data (write stage); whether it is written is decided by the memory's valid chain
      if (gl == 0) begin : g_wd0
        assign mem_wdata[0 +: CW] = kind_w ? bfly_a_o[0 +: CW] : host_wdata_w;
      end else begin : g_wd
        assign mem_wdata[(2*gl)*CW +: CW] = bfly_a_o[gl*CW +: CW];
      end
      assign mem_wdata[(2*gl+1)*CW +: CW] = bfly_b_o[gl*CW +: CW];
    end
  endgenerate

  // -- FSM next-state / counters -----------------------------------------------------------------
  logic done_set, done_clear, start_ok;

  assign start_ok = start_i && !host_we_i && (hw_q == DW'(0));

  always_comb begin
    state_d      = state_q;
    layer_d      = layer_q;
    t_d          = t_q;
    drain_d      = drain_q;
    done_set     = 1'b0;
    done_clear   = 1'b0;

    // a host write issued now can be overtaken by a read issued up to WrEff cycles later (storage is read at the arbitration end)
    if (mem_wr[0] && host_wr_ok)  hw_d = DW'(WrEff);
    else if (hw_q != DW'(0))      hw_d = hw_q - DW'(1);
    else                          hw_d = hw_q;

    case (state_q)
      S_IDLE: begin
        if (start_ok) begin
          state_d    = S_RUN;
          layer_d    = 3'd0;
          t_d        = TW'(0);
          done_clear = 1'b1;
        end
      end

      S_RUN: begin
        if (t_q == TW'(TMax)) begin
          t_d = TW'(0);
          if (layer_q == 3'd6) begin
            state_d = (Pipe > 0) ? S_DRAIN : S_DONE;
            drain_d = DW'(0);
          end else begin
            layer_d = layer_q + 3'd1;
          end
        end else begin
          t_d = t_q + TW'(1);
        end
      end

      S_DRAIN: begin   // Pipe cycles: the last request's write lands in the last of them
        if (drain_q == DW'(Pipe - 1)) state_d = S_DONE;
        else                          drain_d = drain_q + DW'(1);
      end

      default: begin // S_DONE
        state_d  = S_IDLE;
        done_set = 1'b1;
      end
    endcase
  end

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      state_q      <= S_IDLE;
      mode_q       <= 1'b0;
      layer_q      <= 3'd0;
      t_q          <= TW'(0);
      drain_q      <= DW'(0);
      hw_q         <= DW'(0);
      done_o       <= 1'b0;
    end else begin
      state_q      <= state_d;
      layer_q      <= layer_d;
      t_q          <= t_d;
      drain_q      <= drain_d;
      hw_q         <= hw_d;
      if (state_q == S_IDLE && start_ok) mode_q <= mode_i;
      if (done_set)   done_o <= 1'b1;
      if (done_clear) done_o <= 1'b0;
    end
  end

  assign busy_o = (state_q == S_RUN) || (state_q == S_DRAIN);

`ifdef FORMAL
  // Auxiliary inductive invariants for the bank_overflow_o proof (same as in rtl/ntt/ntt_core_c4.sv):
  // the counters never leave their reachable ranges.
  always_ff @(posedge clk_i) begin
    if (rst_ni) begin
      assert (t_q <= TW'(TMax));
      assert (layer_q <= 3'd6);
      assert (state_q <= S_DONE);
      assert (drain_q <= DW'((Pipe > 0) ? Pipe - 1 : 0));
      assert (hw_q <= DW'(WrEff));
    end
  end
`endif

endmodule
`default_nettype wire
