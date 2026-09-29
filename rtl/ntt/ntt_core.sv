`default_nettype none
`timescale 1ns/1ps
// rtl/ntt/ntt_core.sv
// Phase 1 baseline NTT/INTT core (configuration C0, docs/ROADMAP.md Phase 1): one butterfly per
// cycle, L = 1 lane, one unbanked polynomial memory (rtl/ntt/poly_mem.sv). Directly implements
// the loop structure of FIPS 203 Algorithm 9 (NTT) and Algorithm 10 (NTT^-1) as transcribed in
// tb/golden/primitives.py, bit-exactly, including the final x3303 INTT scaling pass.
//
// Address derivation per cycle (p = 0..127 counts butterflies within the current layer; every
// layer has exactly 128 butterflies since len * (256/(2*len)) = 128 for every valid len):
//   block      = p >> log2len
//   pos        = p - (block << log2len)      // position within the block, 0..len-1
//   start_addr = block << (log2len + 1)
//   j          = start_addr + pos            // FIPS 203 pseudocode's "j"
//   jlen       = j + len                     // FIPS 203 pseudocode's "j + len"
// len/log2len come from a per-layer, per-direction lookup (NTT: 128,64,...,2; INTT: 2,4,...,128).
// The running twiddle index (zeta_idx) persists across layers: it starts at 1 (NTT) or 127
// (INTT) and steps by +-1 exactly once per finished block (pos == len-1), which reproduces the
// golden model's single monotonic counter `i` across the whole 7-layer run.
//
// Host interface: load/read the 256 coefficients through host_addr_i/host_wdata_i/host_we_i and
// host_rdata_o while the core is idle (not busy_o); start with mode_i held and a start_i pulse;
// poll done_o (registered, cleared by the next start_i).

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module ntt_core (
    input  wire               clk_i,
    input  wire               rst_ni,

    input  wire                mode_i,       // 0 = NTT (forward), 1 = INTT (inverse)
    input  wire                start_i,

    input  wire  [AW-1:0]      host_addr_i,
    input  wire  [CW-1:0]      host_wdata_i,
    input  wire                host_we_i,
    output logic [CW-1:0]      host_rdata_o,

    output logic                busy_o,
    output logic                done_o
);

  typedef enum logic [1:0] {S_IDLE, S_RUN, S_SCALE, S_DONE} state_t;
  state_t state_q, state_d;

  logic       mode_q;
  logic [2:0] layer_q, layer_d;
  logic [7:0] p_q, p_d;
  logic [ZW-1:0] zeta_idx_q, zeta_idx_d;
  logic [AW-1:0] scale_addr_q, scale_addr_d;

  // -- per-layer length lookup (combinational) ------------------------------------------------
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

  logic [7:0] block, pos, start_addr, j, jlen;
  always_comb begin
    block      = p_q >> log2len;
    pos        = p_q - (block << log2len);
    start_addr = block << (log2len + 4'd1);
    j          = start_addr + pos;
    jlen       = j + len;
  end

  // -- twiddle ROM -----------------------------------------------------------------------------
  logic [CW-1:0] rom_zeta, rom_gamma_unused;
  twiddle_rom u_rom (.addr_i(zeta_idx_q), .zeta_o(rom_zeta), .gamma_o(rom_gamma_unused));

  // -- polynomial memory -------------------------------------------------------------------------
  logic              mem_we_a, mem_we_b;
  logic [AW-1:0]     mem_addr_a, mem_addr_b;
  logic [CW-1:0]     mem_wdata_a, mem_wdata_b;
  logic [CW-1:0]     mem_rdata_a, mem_rdata_b;

  poly_mem u_mem (
      .clk_i     (clk_i),
      .we_a_i    (mem_we_a),
      .addr_a_i  (mem_addr_a),
      .wdata_a_i (mem_wdata_a),
      .rdata_a_o (mem_rdata_a),
      .we_b_i    (mem_we_b),
      .addr_b_i  (mem_addr_b),
      .wdata_b_i (mem_wdata_b),
      .rdata_b_o (mem_rdata_b)
  );

  // -- butterfly ---------------------------------------------------------------------------------
  logic [CW-1:0] bfly_a_o, bfly_b_o;
  butterfly u_bfly (
      .mode_i (mode_q),
      .a_i    (mem_rdata_a),
      .b_i    (mem_rdata_b),
      .zeta_i (rom_zeta),
      .a_o    (bfly_a_o),
      .b_o    (bfly_b_o)
  );

  // -- INTT final scaling multiplier (Algorithm 10 line 14: f <- f * 3303 mod q) ------------------
  logic [CW-1:0] scale_result;
  modmul_reduce u_scale_mul (
      .a_i (mem_rdata_a),
      .b_i (CW'(INV128)),
      .p_o (scale_result)
  );

  // -- host port mux + datapath mux -----------------------------------------------------------
  always_comb begin
    host_rdata_o = mem_rdata_a;

    case (state_q)
      S_RUN: begin
        mem_addr_a  = j;
        mem_wdata_a = bfly_a_o;
        mem_we_a    = 1'b1;
        mem_addr_b  = jlen;
        mem_wdata_b = bfly_b_o;
        mem_we_b    = 1'b1;
      end
      S_SCALE: begin
        mem_addr_a  = scale_addr_q;
        mem_wdata_a = scale_result;
        mem_we_a    = 1'b1;
        mem_addr_b  = '0;
        mem_wdata_b = '0;
        mem_we_b    = 1'b0;
      end
      default: begin // S_IDLE, S_DONE: host access
        mem_addr_a  = host_addr_i;
        mem_wdata_a = host_wdata_i;
        mem_we_a    = host_we_i;
        mem_addr_b  = '0;
        mem_wdata_b = '0;
        mem_we_b    = 1'b0;
      end
    endcase
  end

  // -- FSM next-state / counters ------------------------------------------------------------------
  logic done_set, done_clear;

  always_comb begin
    state_d      = state_q;
    layer_d      = layer_q;
    p_d          = p_q;
    zeta_idx_d   = zeta_idx_q;
    scale_addr_d = scale_addr_q;
    done_set     = 1'b0;
    done_clear   = 1'b0;

    case (state_q)
      S_IDLE: begin
        if (start_i) begin
          state_d    = S_RUN;
          layer_d    = 3'd0;
          p_d        = 8'd0;
          zeta_idx_d = mode_i ? ZW'(127) : ZW'(1);
          done_clear = 1'b1;
        end
      end

      S_RUN: begin
        if (pos == len - 8'd1) begin
          zeta_idx_d = mode_q ? (zeta_idx_q - ZW'(1)) : (zeta_idx_q + ZW'(1));
        end
        if (p_q == 8'd127) begin
          p_d = 8'd0;
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
          p_d = p_q + 8'd1;
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
      p_q          <= 8'd0;
      zeta_idx_q   <= ZW'(1);
      scale_addr_q <= 8'd0;
      done_o       <= 1'b0;
    end else begin
      state_q      <= state_d;
      layer_q      <= layer_d;
      p_q          <= p_d;
      zeta_idx_q   <= zeta_idx_d;
      scale_addr_q <= scale_addr_d;
      if (state_q == S_IDLE && start_i) mode_q <= mode_i;
      if (done_set)   done_o <= 1'b1;
      if (done_clear) done_o <= 1'b0;
    end
  end

  assign busy_o = (state_q == S_RUN) || (state_q == S_SCALE);

endmodule
`default_nettype wire
