`default_nettype none
`timescale 1ns/1ps
// rtl/ntt/ntt_core_c2.sv
// Phase 3 (docs/ROADMAP.md Phase 3, evidence/phase03/test_plan.md): multi-lane
// NTT/INTT, config C2, NUM_LANES in {1,2,4,8} (`L` in the roadmap). NUM_LANES butterflies run
// concurrently per cycle, against rtl/mem/poly_mem_multiport.sv #(.NUM_LANES(NUM_LANES)).
//
// Per-cycle lane assignment: lane `l` processes butterfly index
// `p_lane = l*(128/NUM_LANES) + t_q` (the contiguous-block grouping
// `tb/mem/bank_model.py:lane_p`, proven conflict-free and full-coverage for every
// NUM_LANES/layer/direction, evidence/phase03/lane_schedule_verification.txt).
// `t_q` (0..128/NUM_LANES-1) replaces C0/C1's single `p_q` (0..127).
//
// Unlike C0/C1, there is NO shared sequential zeta-index register: each lane computes its own
// twiddle-ROM index purely combinationally from (layer_q, its own block index), via the closed
// form verified against C0's sequential update rule (`tb/mem/bank_model.py:zeta_index_of`,
// same evidence file as above, 0 mismatches over all 127 (layer,block) pairs, both directions):
//   NTT (forward):  k = 2^layer_q + block
//   INTT (inverse): k = 127 - cum_inv[layer_q] - block   (cum_inv from _INV_LEN block counts:
//                                                          0,64,96,112,120,124,126)
// This is what lets NUM_LANES lanes advance through different blocks in the same cycle without
// coordinating a shared counter.
//
// Everything else -- FSM shape, the len/log2len per-layer table, the INTT final x3303 scaling
// pass (single address per cycle, NOT lane-parallelized this phase -- out of the "butterfly,
// arithmetic and memory as in Phase 2" scope), the host load/read interface -- is unchanged from
// rtl/ntt/ntt_core.sv (C0). At NUM_LANES=1 this module is expected to be cycle-identical to
// C0/C1 (897 NTT / 1153 INTT cycles, evidence/phase01/) since
// 128/1-1 == 127 reproduces the same t/p sequence; cocotb checks this as a regression anchor,
// not merely assumes it.
//
// rtl/ntt/ntt_core.sv (C0) and rtl/mem/ntt_core_c1.sv (C1) are NOT modified by this phase.

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module ntt_core_c2 #(
    parameter int NUM_LANES = 1
) (
    input  wire               clk_i,
    input  wire                rst_ni,

    input  wire                mode_i,       // 0 = NTT (forward), 1 = INTT (inverse)
    input  wire                start_i,

    input  wire  [AW-1:0]      host_addr_i,
    input  wire  [CW-1:0]      host_wdata_i,
    input  wire                host_we_i,
    output logic [CW-1:0]      host_rdata_o,

    output logic                busy_o,
    output logic                done_o,
    output logic                bank_overflow_o   // diagnostic; must stay 0 (see test plan CRG-8)
);

  localparam int TMax = 128 / NUM_LANES - 1;   // max t_q value
  localparam int TW   = 8;                     // t_q width (127 max at NUM_LANES=1)

  typedef enum logic [1:0] {S_IDLE, S_RUN, S_SCALE, S_DONE} state_t;
  state_t state_q, state_d;

  logic          mode_q;
  logic [2:0]    layer_q, layer_d;
  logic [TW-1:0] t_q, t_d;
  logic [AW-1:0] scale_addr_q, scale_addr_d;

  // -- per-layer length lookup (combinational, identical to C0) ------------------------------
  logic [7:0] len;
  logic [3:0] log2len;   // 1..7

  always_comb begin
    case (layer_q)
      3'd0: begin len = mode_q ? 8'd2   : 8'd128; log2len = mode_q ? 4'd1 : 4'd7; end
      3'd1: begin len = mode_q ? 8'd4   : 8'd64;  log2len = mode_q ? 4'd2 : 4'd6; end
      3'd2: begin len = mode_q ? 8'd8   : 8'd32;  log2len = mode_q ? 4'd3 : 4'd5; end
      3'd3: begin len = 8'd16;                    log2len = 4'd4; end
      3'd4: begin len = mode_q ? 8'd32  : 8'd8;   log2len = mode_q ? 4'd5 : 4'd3; end
      3'd5: begin len = mode_q ? 8'd64  : 8'd4;   log2len = mode_q ? 4'd6 : 4'd2; end
      default: begin len = mode_q ? 8'd128 : 8'd2; log2len = mode_q ? 4'd7 : 4'd1; end // layer 6
    endcase
  end

  // -- cumulative INTT block count before layer_q (verified closed form, see header) ----------
  logic [6:0] cum_inv;
  always_comb begin
    case (layer_q)
      3'd0: cum_inv = 7'd0;
      3'd1: cum_inv = 7'd64;
      3'd2: cum_inv = 7'd96;
      3'd3: cum_inv = 7'd112;
      3'd4: cum_inv = 7'd120;
      3'd5: cum_inv = 7'd124;
      default: cum_inv = 7'd126; // layer 6
    endcase
  end

  // -- multi-port banked memory ---------------------------------------------------------------
  localparam int NumPorts = 2 * NUM_LANES;

  logic [NumPorts-1:0]        mem_en;
  logic [NumPorts-1:0]        mem_we;
  logic [NumPorts*AW-1:0]     mem_addr;    // port i: mem_addr[i*AW +: AW]
  logic [NumPorts*CW-1:0]     mem_wdata;   // port i: mem_wdata[i*CW +: CW]
  logic [NumPorts*CW-1:0]     mem_rdata;   // port i: mem_rdata[i*CW +: CW]

  poly_mem_multiport #(.NUM_LANES(NUM_LANES)) u_mem (
      .clk_i          (clk_i),
      .en_i           (mem_en),
      .we_i           (mem_we),
      .addr_i         (mem_addr),
      .wdata_i        (mem_wdata),
      .rdata_o        (mem_rdata),
      .bank_overflow_o(bank_overflow_o)
  );

  // -- INTT final scaling multiplier (Algorithm 10 line 14: f <- f * 3303 mod q) ----------------
  logic [CW-1:0] scale_result;
  modmul_reduce u_scale_mul (
      .a_i (mem_rdata[0 +: CW]),
      .b_i (CW'(INV128)),
      .p_o (scale_result)
  );

  // -- per-lane address / zeta / butterfly ------------------------------------------------------
  logic [NUM_LANES*CW-1:0] bfly_a_o;   // lane l: bfly_a_o[l*CW +: CW]
  logic [NUM_LANES*CW-1:0] bfly_b_o;

  genvar gl;
  generate
    for (gl = 0; gl < NUM_LANES; gl++) begin : g_lane
      logic [7:0]    p_lane, block_lane, pos_lane, start_addr_lane;
      logic [AW-1:0] j_lane, jlen_lane;
      logic [ZW-1:0] zeta_idx_lane;
      logic [CW-1:0] rom_zeta_lane, rom_gamma_unused_lane;

      always_comb begin
        p_lane           = 8'(gl * (128 / NUM_LANES)) + t_q;
        block_lane       = p_lane >> log2len;
        pos_lane         = p_lane - (block_lane << log2len);
        start_addr_lane  = block_lane << (log2len + 4'd1);
        j_lane            = start_addr_lane + pos_lane;
        jlen_lane         = j_lane + len;
        // zeta_index_of, closed form verified in tb/mem/bank_model.py (module header): NTT
        // k = 2^layer + block; INTT k = 127 - cum_inv[layer] - block. Both branches stay in
        // [1,127] for every (layer,block) pair by that verification, so plain ZW-bit unsigned
        // arithmetic never underflows.
        zeta_idx_lane = mode_q
                           ? (ZW'(127) - ZW'(cum_inv) - ZW'(block_lane))
                           : (ZW'(8'd1 << layer_q) + ZW'(block_lane));
      end

      twiddle_rom u_rom (
          .addr_i (zeta_idx_lane),
          .zeta_o (rom_zeta_lane),
          .gamma_o(rom_gamma_unused_lane)
      );

      butterfly u_bfly (
          .mode_i (mode_q),
          .a_i    (mem_rdata[(2*gl)*CW +: CW]),
          .b_i    (mem_rdata[(2*gl+1)*CW +: CW]),
          .zeta_i (rom_zeta_lane),
          .a_o    (bfly_a_o[gl*CW +: CW]),
          .b_o    (bfly_b_o[gl*CW +: CW])
      );

      always_comb begin
        if (state_q == S_RUN) begin
          mem_en   [2*gl]                  = 1'b1;
          mem_addr [(2*gl)*AW +: AW]       = j_lane;
          mem_wdata[(2*gl)*CW +: CW]       = bfly_a_o[gl*CW +: CW];
          mem_we   [2*gl]                  = 1'b1;
          mem_en   [2*gl+1]                = 1'b1;
          mem_addr [(2*gl+1)*AW +: AW]     = jlen_lane;
          mem_wdata[(2*gl+1)*CW +: CW]     = bfly_b_o[gl*CW +: CW];
          mem_we   [2*gl+1]                = 1'b1;
        end else if (gl == 0) begin
          // S_IDLE/S_SCALE/S_DONE: lane 0's j-port carries the host/scale single-address access;
          // every other port (including lane 0's jlen-port) is disabled (en_i=0), so it is never
          // counted toward poly_mem_multiport's bank-capacity check.
          mem_en   [2*gl]                  = 1'b1;
          mem_addr [(2*gl)*AW +: AW]       = (state_q == S_SCALE) ? scale_addr_q : host_addr_i;
          mem_wdata[(2*gl)*CW +: CW]       = (state_q == S_SCALE) ? scale_result : host_wdata_i;
          mem_we   [2*gl]                  = (state_q == S_SCALE) ? 1'b1 : host_we_i;
          mem_en   [2*gl+1]                = 1'b0;
          mem_addr [(2*gl+1)*AW +: AW]     = '0;
          mem_wdata[(2*gl+1)*CW +: CW]     = '0;
          mem_we   [2*gl+1]                = 1'b0;
        end else begin
          mem_en   [2*gl]                  = 1'b0;
          mem_addr [(2*gl)*AW +: AW]       = '0;
          mem_wdata[(2*gl)*CW +: CW]       = '0;
          mem_we   [2*gl]                  = 1'b0;
          mem_en   [2*gl+1]                = 1'b0;
          mem_addr [(2*gl+1)*AW +: AW]     = '0;
          mem_wdata[(2*gl+1)*CW +: CW]     = '0;
          mem_we   [2*gl+1]                = 1'b0;
        end
      end
    end
  endgenerate

  assign host_rdata_o = mem_rdata[0 +: CW];

  // -- FSM next-state / counters ----------------------------------------------------------------
  logic done_set, done_clear;

  always_comb begin
    state_d      = state_q;
    layer_d      = layer_q;
    t_d          = t_q;
    scale_addr_d = scale_addr_q;
    done_set     = 1'b0;
    done_clear   = 1'b0;

    case (state_q)
      S_IDLE: begin
        if (start_i) begin
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
              state_d = S_DONE;
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
          state_d = S_DONE;
        end else begin
          scale_addr_d = scale_addr_q + 8'd1;
        end
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
      done_o       <= 1'b0;
    end else begin
      state_q      <= state_d;
      layer_q      <= layer_d;
      t_q          <= t_d;
      scale_addr_q <= scale_addr_d;
      if (state_q == S_IDLE && start_i) mode_q <= mode_i;
      if (done_set)   done_o <= 1'b1;
      if (done_clear) done_o <= 1'b0;
    end
  end

  assign busy_o = (state_q == S_RUN) || (state_q == S_SCALE);

`ifdef FORMAL
  // Auxiliary inductive invariants for the bank_overflow_o proof
  // (formal/phase03-multilane/ntt_core_c2_formal_top.sv): k-induction on bank_overflow_o alone
  // fails for NUM_LANES>1 without these -- the induction step otherwise starts from an
  // unconstrained state where t_q/layer_q could take a value the FSM itself never reaches (e.g.
  // t_q > TMax), which the per-lane address/bank derivation was never proven conflict-free for.
  // t_q/layer_q never leaving their reachable ranges is a genuine, separately-provable FSM fact
  // (both only ever increment toward their max then reset to 0, never jump); asserting it here
  // gives the solver that fact as a hypothesis when it proves bank_overflow_o.
  always_ff @(posedge clk_i) begin
    if (rst_ni) begin
      assert (t_q <= TW'(TMax));
      assert (layer_q <= 3'd6);
    end
  end
`endif

endmodule
`default_nettype wire
