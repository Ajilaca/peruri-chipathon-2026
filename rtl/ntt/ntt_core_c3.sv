`default_nettype none
`timescale 1ns/1ps
// rtl/ntt/ntt_core_c3.sv
// Phase 4 (docs/ROADMAP.md Phase 4, ADR 0006, ADR 0007, evidence/phase04/test_plan.md):
// configuration C3 = the schedule and FSM of rtl/ntt/ntt_core_c2_k2_k1.sv (multi-lane NTT/INTT, shared
// multiplier per butterfly; that file stays frozen and is the P = 0 reference) with pipeline registers
// between the cycle a butterfly's addresses are issued and the cycle its results are written.
//
//   issue (cycle t)      FSM counters -> per-lane addresses j / j+len -> memory request
//   read  (t + RdLat)    memory read data, per-lane zeta from the delayed (layer, t) -> butterfly input
//   write (t + Pipe)     butterfly output -> memory write, to the addresses issued at cycle t
//
//   RdLat = bits set in ARB_REG  (register stages inside / after the memory's slot arbitration)
//   WrDly = bits set in MUL_REG  (register stages after the multiplier / inside the reducer)
//   Pipe  = RdLat + WrDly        (the "P" of ADR 0007)
//
// What is unchanged from C2-K2-K1: the lane schedule p = l*(128/NUM_LANES) + t, the address arithmetic,
// the closed-form zeta index, the order of the layers, one address per cycle for the INTT x3303 scaling
// pass, the results (bit-exact, checked against tb/golden/primitives.py). No stall is inserted at layer
// boundaries: the schedule leaves more cycles between the write of an address and its next read than
// WrDly for the depths used (evidence/phase04/layer_boundary_slack.txt); the
// testbench scoreboard checks that on the RTL.
//
// What differs at the interface (all of it a consequence of the pipeline):
//   - after the last request the FSM waits Pipe cycles (S_DRAIN) before S_DONE, so busy_o covers every
//     write; cycles from busy_o to done_o are 113 + Pipe (NTT) / 369 + Pipe (INTT) at NUM_LANES = 8 if
//     nothing else stalls (measured by the testbench, not assumed);
//   - host_rdata_o shows the coefficient at host_addr_i RdLat cycles later;
//   - a host write lands Pipe cycles after host_we_i. start_i is accepted only in S_IDLE, with
//     host_we_i low and no host write still in the pipeline; until then it is simply not taken (hold
//     start_i until busy_o rises). host_we_i is ignored while busy_o is high.
//
// Reset: asynchronous, active low, on the FSM state, counters and the memory's write-valid chain.
// Datapath and address pipeline registers are not reset (they cannot cause a write: valid is reset).

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module ntt_core_c3 #(
    parameter int          NUM_LANES = 8,
    parameter logic [32:0] ARB_REG   = 33'd0,   // poly_mem_multiport_pipe.ARB_REG
    parameter logic [13:0] MUL_REG   = 14'd0    // modmul_reduce_staged.REG_AFTER
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

  localparam int RdLat = ones33(ARB_REG);
  localparam int WrDly = ones33({19'd0, MUL_REG});
  localparam int Pipe  = RdLat + WrDly;

  localparam int TMax = 128 / NUM_LANES - 1;                 // max t_q value
  localparam int TW   = (TMax > 0) ? $clog2(TMax + 1) : 1;
  localparam int DW   = (Pipe > 0) ? $clog2(Pipe + 1) : 1;   // drain / host-write-in-flight counters

  localparam int NumPorts = 2 * NUM_LANES;

  typedef enum logic [2:0] {S_IDLE, S_RUN, S_SCALE, S_DRAIN, S_DONE} state_t;
  state_t state_q, state_d;

  // what port 0 was asked to do, carried to the write stage to pick its write data
  localparam logic [1:0] KHost = 2'd0, KRun = 2'd1, KScale = 2'd2;

  logic          mode_q;
  logic [2:0]    layer_q, layer_d;
  logic [TW-1:0] t_q, t_d;
  logic [AW-1:0] scale_addr_q, scale_addr_d;
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

  poly_mem_multiport_pipe #(
      .NUM_LANES(NUM_LANES), .ARB_REG(ARB_REG), .WR_DELAY(WrDly)
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

  // -- INTT final scaling (Algorithm 10 line 14: f <- f * 3303 mod q), same depth as a butterfly ---
  logic [CW-1:0] scale_result;
  modmul_reduce_staged #(.REG_AFTER(MUL_REG)) u_scale_mul (
      .clk_i(clk_i),
      .a_i  (mem_rdata[0 +: CW]),
      .b_i  (CW'(INV128)),
      .p_o  (scale_result)
  );

  // -- port 0's write-data selection, aligned with the write stage -------------------------------
  logic [1:0]    kind_i, kind_w;
  logic [CW-1:0] host_wdata_w;

  always_comb begin
    case (state_q)
      S_RUN:   kind_i = KRun;
      S_SCALE: kind_i = KScale;
      default: kind_i = KHost;
    endcase
  end

  pipe_delay #(.W(2 + CW), .STAGES(Pipe), .HAS_RST(1'b0)) u_dly_kind (
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
      logic [CW-1:0] rom_zeta_lane, rom_gamma_unused_lane;

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

      twiddle_rom u_rom (
          .addr_i (zeta_idx_lane),
          .zeta_o (rom_zeta_lane),
          .gamma_o(rom_gamma_unused_lane)
      );

      butterfly_shared_pipe #(.MUL_REG(MUL_REG)) u_bfly (
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
          // Every other state: lane 0's j-port carries the single-address host / scaling access; all
          // other ports are disabled, so they never count toward the bank-capacity check.
          mem_en  [2*gl]               = 1'b1;
          mem_wr  [2*gl]               = (state_q == S_SCALE) ? 1'b1 : (host_we_i && host_wr_ok);
          mem_addr[(2*gl)*AW +: AW]    = (state_q == S_SCALE) ? scale_addr_q : host_addr_i;
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
        always_comb begin
          case (kind_w)
            KRun:    mem_wdata[0 +: CW] = bfly_a_o[0 +: CW];
            KScale:  mem_wdata[0 +: CW] = scale_result;
            default: mem_wdata[0 +: CW] = host_wdata_w;
          endcase
        end
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
    scale_addr_d = scale_addr_q;
    drain_d      = drain_q;
    done_set     = 1'b0;
    done_clear   = 1'b0;

    // a host write issued now can be overtaken by a read issued up to WrDly cycles later
    if (mem_wr[0] && host_wr_ok)  hw_d = DW'(WrDly);
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
            if (mode_q) begin
              state_d      = S_SCALE;
              scale_addr_d = 8'd0;
            end else begin
              state_d = (Pipe > 0) ? S_DRAIN : S_DONE;
              drain_d = DW'(0);
            end
          end else begin
            layer_d = layer_q + 3'd1;
          end
        end else begin
          t_d = t_q + TW'(1);
        end
      end

      S_SCALE: begin
        if (scale_addr_q == 8'd255) begin
          state_d = (Pipe > 0) ? S_DRAIN : S_DONE;
          drain_d = DW'(0);
        end else begin
          scale_addr_d = scale_addr_q + 8'd1;
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
      scale_addr_q <= 8'd0;
      drain_q      <= DW'(0);
      hw_q         <= DW'(0);
      done_o       <= 1'b0;
    end else begin
      state_q      <= state_d;
      layer_q      <= layer_d;
      t_q          <= t_d;
      scale_addr_q <= scale_addr_d;
      drain_q      <= drain_d;
      hw_q         <= hw_d;
      if (state_q == S_IDLE && start_ok) mode_q <= mode_i;
      if (done_set)   done_o <= 1'b1;
      if (done_clear) done_o <= 1'b0;
    end
  end

  assign busy_o = (state_q == S_RUN) || (state_q == S_SCALE) || (state_q == S_DRAIN);

`ifdef FORMAL
  // Auxiliary inductive invariants for the bank_overflow_o proof (same role as in
  // rtl/ntt/ntt_core_c2_k2_k1.sv): the counters never leave their reachable ranges.
  always_ff @(posedge clk_i) begin
    if (rst_ni) begin
      assert (t_q <= TW'(TMax));
      assert (layer_q <= 3'd6);
      assert (state_q <= S_DONE);
      assert (drain_q <= DW'((Pipe > 0) ? Pipe - 1 : 0));
      assert (hw_q <= DW'(WrDly));
    end
  end
`endif

endmodule
`default_nettype wire
