`default_nettype none
`timescale 1ns/1ps
// rtl/sched/kpke_sched_smp4.sv
// Phase 9I item 4 (docs/evidence/phase09m-optimisation/9i4/test_plan_9i4.md): rtl/sched/kpke_sched_smp.sv (Phases 8c / 8d, frozen) with a host port that also works while the engine runs (parameter HOSTOV = 1; at HOSTOV = 0 it is the same behaviour):
//   - a host write (tb_we_i) while a program runs is granted only in a cycle in which neither the sequencer nor a sampler beat writes the store (tb_wready_o = 1); the host has the lowest priority;
//   - ov_pend_i[slot] = 1 marks a slot whose load is not complete: an operation that reads or writes such a slot (NTT, INTT: d; PWM, ADD, SUB: d, a, b; SMPN, SMPA: d; PWMS: d, b) is not started until the bit is 0 (the sequencer waits in FETCH). Reads through the host port are only possible while idle.
// original header follows:
// Phases 8c / 8d (docs/evidence/phase08-keccak-stream/8c/test_plan_8c.md, 8d/test_plan_8d.md): the Phase 6 operation-level sequencer (rtl/sched/kpke_sched.sv, unchanged) plus the 8b sampler.
// Operations as in Phase 6, and (opcode 4 bits; programs from rtl/sched/kpke_smp_prog_rom.sv, generated from tb/golden/kpke_smp_model.py):
//   SMPN d ctr   slot d <- CBD2 sample of PRF(seed, ctr): the sampler starts with the 33-byte message sd || ctr and its beats (two coefficients = one store pair) are written into slot d
//   SMPA d m     slot d <- SampleNTT(rho || j || i), m = 3i + j (j = m mod 3, i = m div 3); same path, 34-byte message (STORE variant)
//   PWMS d m b F L  PWM pass whose operand a is the sampler stream of A_hat[i][j] (STREAM_A = 1): the b operand, the accumulator word and gamma are addressed one cycle ahead by the beat counter, so their data
//                   are there when a beat arrives; a valid/index tag shift register of the PWM latency (7 cycles) routes the results (accumulate by index, or the final slot write); a bubble feeds nothing
//   WAIT         wait until the sampler is idle (OVERLAP = 1)
// SMPN/SMPA block the sequencer until the sampler is idle again, except SMPN with first = 1 when OVERLAP = 1 (non-blocking: the sampler runs while the next operations compute, its beats are written when the store write port
// is free, the sequencer always has priority). An END with a busy sampler waits for it.
// Seeds: rho and sd (256 bit each) are written through the seed port while the sequencer is idle (writes while busy are ignored). Hashing of keys is not in hardware.
// Every operation has a fixed length except the sampling ones, whose length depends on the public rho (rejection sampling) and not on any secret; no branch, address or loop count depends on a secret value.
// Reset: asynchronous, active low, on the state, counters and done flag; storage and datapath registers are not reset (as Phase 6).

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module kpke_sched_smp4 #(
    parameter int NPOLY      = 24,
    parameter int CORE_RDLAT = 2,       // cycles from a host read address to its data at the NTT core (S10: 2)
    parameter int VAR        = 0,       // program ROM variant: 0 STORE, 1 STREAM, 2 OVERLAP
    parameter bit STREAM_A   = 1'b0,    // 1: PWMS implemented (A_hat streamed from the sampler)
    parameter bit OVERLAP    = 1'b0,    // 1: non-blocking SMPN, WAIT and store-port arbitration implemented
    parameter bit CORE_R2    = 1'b1,    // sampler sponge: 1 C5 (two rounds per cycle), 0 K0
    parameter bit HOSTOV     = 1'b0     // 1: host writes are granted while a program runs; ov_pend_i interlock active
) (
    input  wire         clk_i,
    input  wire         rst_ni,

    input  wire  [1:0]  prog_i,         // 0 KeyGen, 1 Encrypt, 2 Decrypt arithmetic
    input  wire         start_i,
    output logic        busy_o,
    output logic        done_o,

    input  wire         tb_we_i,
    input  wire  [4:0]  tb_slot_i,
    input  wire  [7:0]  tb_addr_i,
    input  wire  [11:0] tb_wdata_i,
    output logic [11:0] tb_rdata_o,     // one cycle after tb_slot_i / tb_addr_i
    output logic        tb_wready_o,    // a host write in this cycle is written (always 1 while idle)
    input  wire  [11:0] ov_pend_i,      // slots whose load is not complete (HOSTOV = 1)

    input  wire         seed_we_i,      // seed port: while idle
    input  wire         seed_sel_i,     // 0 rho, 1 sd
    input  wire  [1:0]  seed_idx_i,     // 64-bit word, byte 0 in bits [7:0]
    input  wire  [63:0] seed_data_i,

    output logic [5:0]  cnt_ntt_o,
    output logic [5:0]  cnt_intt_o,
    output logic [5:0]  cnt_pwm_o,      // PWM and PWMS
    output logic [5:0]  cnt_smp_o,      // SMPN and SMPA

    output logic        core_mode_o,
    output logic        core_start_o,
    output logic [7:0]  core_haddr_o,
    output logic [11:0] core_hwdata_o,
    output logic        core_hwe_o,
    input  wire  [11:0] core_hrdata_i,
    input  wire         core_busy_i,
    input  wire         core_done_i
);

  localparam logic [3:0] OpEnd = 4'd0, OpNtt = 4'd1, OpIntt = 4'd2, OpPwm = 4'd3, OpAdd = 4'd4, OpSub = 4'd5, OpSmpn = 4'd6, OpSmpa = 4'd7, OpPwms = 4'd8, OpWait = 4'd9;
  localparam int         LatPwm = 8;   // store read 1 + pwm_unit 7
  localparam int         LatAdd = 2;   // store read 1 + result register 1
  localparam int         LatTag = 7;   // pwm_unit latency (the stream path)

  typedef enum logic [3:0] {S_IDLE, S_FETCH, S_LOAD, S_START, S_RUN, S_UNLOAD, S_PASS, S_SMPS, S_SMPR, S_PWMS, S_WAITS, S_DONE} state_t;
  state_t state_q;

  logic [1:0]  prog_q;
  logic [5:0]  pc_q;
  logic [8:0]  cnt_q;
  logic [3:0]  opc_q;
  logic        first_q, last_q;
  logic [4:0]  d_q, a_q, b_q;
  logic [20:0] op_w;

  kpke_smp_prog_rom #(.VAR(VAR)) u_prog (.prog_i(prog_q), .pc_i(pc_q), .op_o(op_w));

  // -- sampler, message feeder, seeds ----------------------------------------------------------------------------
  logic [63:0] rho_q [0:3];
  logic [63:0] sd_q  [0:3];
  logic        smp_start, smp_in_valid, smp_in_ready, smp_cvalid, smp_cready, smp_busy, smp_done, smp_clast;
  logic        smp_kind_q, smp_pwm_q, smp_wr_q;   // sampling kind (0 SampleNTT, 1 CBD2), beats go to the PWM unit, beats go to the store
  logic [4:0]  smp_dst_q;
  logic [6:0]  smp_idx_q;
  logic [63:0] smp_in_data;
  logic [23:0] smp_cdata;
  logic [15:0] smp_bytes, smp_perm;
  logic        feed_q;
  logic [2:0]  fw_q;
  logic [7:0]  msg_b32_q, msg_b33_q;

  wire is_smp_op = (opc_q == OpSmpn) || (opc_q == OpSmpa) || (opc_q == OpPwms);
  wire idle_st   = (state_q == S_IDLE) || (state_q == S_DONE);

  always_comb begin
    smp_in_valid = feed_q;
    if (fw_q[2]) smp_in_data = {48'd0, msg_b33_q, msg_b32_q};
    else         smp_in_data = smp_kind_q ? sd_q[fw_q[1:0]] : rho_q[fw_q[1:0]];
  end

  assign smp_start = (state_q == S_SMPS) && !smp_busy && ((opc_q != OpPwms) || STREAM_A);

  keccak_sampler #(.CORE_R2(CORE_R2), .OUTW(2)) u_smp (
      .clk_i(clk_i), .rst_ni(rst_ni), .start_i(smp_start), .kind_i((opc_q == OpSmpn)), .len_i((opc_q == OpSmpn) ? 16'd33 : 16'd34), .abort_i(1'b0),
      .in_valid_i(smp_in_valid), .in_ready_o(smp_in_ready), .in_data_i(smp_in_data),
      .coef_valid_o(smp_cvalid), .coef_ready_i(smp_cready), .coef_data_o(smp_cdata), .coef_last_o(smp_clast),
      .bytes_o(smp_bytes), .busy_o(smp_busy), .done_o(smp_done), .perm_cnt_o(smp_perm));

  logic smp_wr;   // the beat is written into the store this cycle

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      feed_q     <= 1'b0;
      fw_q       <= 3'd0;
      smp_kind_q <= 1'b0;
      smp_pwm_q  <= 1'b0;
      smp_wr_q   <= 1'b0;
      smp_dst_q  <= 5'd0;
      smp_idx_q  <= 7'd0;
      msg_b32_q  <= 8'd0;
      msg_b33_q  <= 8'd0;
    end else begin
      if (smp_done) begin   // before the start branch: a start in the same cycle as the previous done pulse wins
        smp_pwm_q <= 1'b0;
        smp_wr_q  <= 1'b0;
      end
      if (smp_start) begin
        feed_q     <= 1'b1;
        fw_q       <= 3'd0;
        smp_kind_q <= (opc_q == OpSmpn);
        smp_pwm_q  <= (opc_q == OpPwms);
        smp_wr_q   <= (opc_q != OpPwms);
        smp_dst_q  <= d_q;
        smp_idx_q  <= 7'd0;
        if (opc_q == OpSmpn) begin
          msg_b32_q <= {3'd0, b_q};
          msg_b33_q <= 8'd0;
        end else begin
          msg_b32_q <= 8'(a_q % 5'd3);   // j = m mod 3
          msg_b33_q <= 8'(a_q / 5'd3);   // i = m div 3
        end
      end else if (feed_q && smp_in_ready) begin
        fw_q <= fw_q + 3'd1;
        if (fw_q == 3'd4) feed_q <= 1'b0;
      end
      if (smp_wr) smp_idx_q <= smp_idx_q + 7'd1;
      if (idle_st && seed_we_i) begin
        if (seed_sel_i) sd_q[seed_idx_i]  <= seed_data_i;
        else            rho_q[seed_idx_i] <= seed_data_i;
      end
    end
  end

  // -- store ------------------------------------------------------------------------------------------------
  logic [4:0]  ra_slot, rb_slot, w_slot;
  logic [6:0]  ra_pair, rb_pair, w_pair;
  logic [11:0] ra_e, ra_o, rb_e, rb_o, wd_e, wd_o;
  logic        we_e, we_o;

  poly_store_smp #(.NPOLY(NPOLY)) u_store (
      .clk_i(clk_i),
      .ra_slot_i(ra_slot), .ra_pair_i(ra_pair), .ra_e_o(ra_e), .ra_o_o(ra_o),
      .rb_slot_i(rb_slot), .rb_pair_i(rb_pair), .rb_e_o(rb_e), .rb_o_o(rb_o),
      .we_e_i(we_e), .we_o_i(we_o), .w_slot_i(w_slot), .w_pair_i(w_pair), .wd_e_i(wd_e), .wd_o_i(wd_o));

  // -- accumulator of the PWM passes (128 pairs) -------------------------------------------------------------
  logic [11:0] acc_e [0:127];
  logic [11:0] acc_o [0:127];
  logic [11:0] acc_rd_e, acc_rd_o;
  logic        acc_we;
  logic [6:0]  acc_widx;

  // -- PWMS beat counter and result tags ----------------------------------------------------------------------
  logic [7:0]  bcnt_q;                  // beats consumed in this pass
  logic [2:0]  drain_q;
  logic        beat;                    // a sampler beat enters the PWM unit this cycle
  logic [7:0]  nxt;                     // index of the next beat
  logic [LatTag-1:0] tag_v;             // tag_v[k]: a beat entered k + 1 cycles ago
  logic [6:0]  tag_i [0:LatTag-1];
  logic        out_v;
  logic [6:0]  out_i;

  assign beat  = STREAM_A && (state_q == S_PWMS) && smp_cvalid && smp_pwm_q;
  assign nxt   = bcnt_q + {7'd0, beat};
  assign out_v = STREAM_A && tag_v[LatTag-1];
  assign out_i = tag_i[LatTag-1];

  always_ff @(posedge clk_i or negedge rst_ni) begin   // the valid tags are reset (no stray write after power-up); the index tags are data
    if (!rst_ni) begin
      tag_v <= '0;
    end else begin
      tag_v <= {tag_v[LatTag-2:0], beat};
    end
  end

  always_ff @(posedge clk_i) begin
    tag_i[0] <= bcnt_q[6:0];
    for (int k = 1; k < LatTag; k++) tag_i[k] <= tag_i[k-1];
  end

  // -- pass datapath ------------------------------------------------------------------------------------------
  logic [6:0]  pair_m1;                 // pair whose store data is visible this cycle
  logic        half_q;                  // LOAD / testbench read: which half of the pair
  logic [11:0] gamma;
  logic [11:0] pwm_c0, pwm_c1;
  logic [11:0] res_e, res_o;            // ADD / SUB result register
  logic        is_pwm;
  logic [8:0]  pass_len, wlat;
  logic [8:0]  widx_pass, widx_unl;
  logic        pass_wr, unl_wr;
  wire         in_pwms = (state_q == S_PWMS);
  wire [6:0]   rd_idx  = in_pwms ? nxt[6:0] : cnt_q[6:0];

  assign is_pwm   = (opc_q == OpPwm);
  assign wlat     = is_pwm ? 9'(LatPwm) : 9'(LatAdd);
  assign pass_len = 9'd128 + wlat;      // cycles 0 .. pass_len - 1
  assign widx_pass = cnt_q - wlat;
  assign pass_wr  = (state_q == S_PASS) && (cnt_q >= wlat);
  assign widx_unl = cnt_q - 9'(CORE_RDLAT);
  assign unl_wr   = (state_q == S_UNLOAD) && (cnt_q >= 9'(CORE_RDLAT));
  logic unused_widx;                    // high bits are 0 whenever a write is enabled (index < 128 / < 256)
  assign unused_widx = ^{widx_pass[8:7], widx_unl[8]};

  gamma_rom u_gamma (.addr_i(pair_m1), .gamma_o(gamma));

  wire [11:0] pwm_a0 = in_pwms ? smp_cdata[11:0]  : ra_e;
  wire [11:0] pwm_a1 = in_pwms ? smp_cdata[23:12] : ra_o;

  pwm_unit u_pwm (
      .clk_i(clk_i),
      .a0_i(pwm_a0), .a1_i(pwm_a1), .b0_i(rb_e), .b1_i(rb_o), .gamma_i(gamma),
      .acc0_i(first_q ? 12'd0 : acc_rd_e), .acc1_i(first_q ? 12'd0 : acc_rd_o),
      .c0_o(pwm_c0), .c1_o(pwm_c1));

  assign acc_widx = out_v ? out_i : widx_pass[6:0];

  always_ff @(posedge clk_i) begin
    pair_m1  <= rd_idx;
    half_q   <= (state_q == S_LOAD) ? cnt_q[0] : tb_addr_i[0];
    acc_rd_e <= acc_e[rd_idx];
    acc_rd_o <= acc_o[rd_idx];
    if (acc_we) begin
      acc_e[acc_widx] <= pwm_c0;
      acc_o[acc_widx] <= pwm_c1;
    end
    res_e <= (opc_q == OpSub) ? sub_mod(ra_e, rb_e) : add_mod(ra_e, rb_e);
    res_o <= (opc_q == OpSub) ? sub_mod(ra_o, rb_o) : add_mod(ra_o, rb_o);
  end

  assign acc_we = (pass_wr && is_pwm && !last_q) || (out_v && !last_q);

  // -- store port selection -----------------------------------------------------------------------------------
  logic seq_wr;   // the sequencer itself writes the store this cycle (priority over the sampler beats)
  logic host_grant;
  always_comb begin
    ra_slot = tb_slot_i;
    ra_pair = tb_addr_i[7:1];
    rb_slot = b_q;
    rb_pair = in_pwms ? nxt[6:0] : cnt_q[6:0];
    if (state_q == S_LOAD) begin
      ra_slot = d_q;
      ra_pair = cnt_q[7:1];
    end else if (state_q == S_PASS) begin
      ra_slot = a_q;
      ra_pair = cnt_q[6:0];
    end

    we_e   = 1'b0;
    we_o   = 1'b0;
    seq_wr = 1'b0;
    w_slot = tb_slot_i;
    w_pair = tb_addr_i[7:1];
    wd_e   = tb_wdata_i;
    wd_o   = tb_wdata_i;
    if (idle_st) begin
      we_e = tb_we_i && !tb_addr_i[0];
      we_o = tb_we_i &&  tb_addr_i[0];
    end else if (unl_wr) begin
      w_slot = d_q;
      w_pair = widx_unl[7:1];
      wd_e   = core_hrdata_i;
      wd_o   = core_hrdata_i;
      we_e   = !widx_unl[0];
      we_o   =  widx_unl[0];
      seq_wr = 1'b1;
    end else if (pass_wr && !(is_pwm && !last_q)) begin
      w_slot = d_q;
      w_pair = widx_pass[6:0];
      wd_e   = is_pwm ? pwm_c0 : res_e;
      wd_o   = is_pwm ? pwm_c1 : res_o;
      we_e   = 1'b1;
      we_o   = 1'b1;
      seq_wr = 1'b1;
    end else if (out_v && last_q) begin
      w_slot = d_q;
      w_pair = out_i;
      wd_e   = pwm_c0;
      wd_o   = pwm_c1;
      we_e   = 1'b1;
      we_o   = 1'b1;
      seq_wr = 1'b1;
    end
    if (smp_wr) begin   // sampler beat: only when the sequencer does not write
      w_slot = smp_dst_q;
      w_pair = smp_idx_q;
      wd_e   = smp_cdata[11:0];
      wd_o   = smp_cdata[23:12];
      we_e   = 1'b1;
      we_o   = 1'b1;
    end
    host_grant = idle_st || (HOSTOV && !seq_wr && !smp_wr);
    if (HOSTOV && !idle_st && tb_we_i && host_grant) begin   // host write while a program runs: lowest priority
      w_slot = tb_slot_i;
      w_pair = tb_addr_i[7:1];
      wd_e   = tb_wdata_i;
      wd_o   = tb_wdata_i;
      we_e   = !tb_addr_i[0];
      we_o   =  tb_addr_i[0];
    end
  end
  assign tb_wready_o = host_grant;

  wire wr_free = OVERLAP ? !seq_wr && !idle_st : 1'b1;
  assign smp_cready = smp_pwm_q ? in_pwms : (smp_wr_q && wr_free);
  assign smp_wr     = smp_cvalid && smp_wr_q && wr_free;

  assign tb_rdata_o = half_q ? ra_o : ra_e;

  // -- NTT core host port -------------------------------------------------------------------------------------
  assign core_mode_o   = (opc_q == OpIntt);
  assign core_start_o  = (state_q == S_START);
  assign core_hwe_o    = (state_q == S_LOAD) && (cnt_q != 9'd0);
  assign core_haddr_o  = (state_q == S_LOAD) ? 8'(cnt_q - 9'd1) : cnt_q[7:0];
  assign core_hwdata_o = half_q ? ra_o : ra_e;

  // -- sequencer ------------------------------------------------------------------------------------------------
  logic start_ok;
  assign start_ok = start_i && (state_q == S_IDLE);

  // interlock (HOSTOV): the operation fetched this cycle uses a slot whose load is not complete
  logic       hz;
  logic [3:0] hz_opc;
  logic [4:0] hz_d, hz_a, hz_b;
  assign hz_opc = op_w[20:17];
  assign hz_d   = op_w[14:10];
  assign hz_a   = op_w[9:5];
  assign hz_b   = op_w[4:0];
  always_comb begin
    hz = 1'b0;
    if (HOSTOV && (state_q == S_FETCH)) begin
      case (hz_opc)
        OpNtt, OpIntt, OpSmpn, OpSmpa: hz = (hz_d < 5'd12) && ov_pend_i[hz_d[3:0]];
        OpPwm, OpAdd, OpSub:           hz = ((hz_d < 5'd12) && ov_pend_i[hz_d[3:0]]) || ((hz_a < 5'd12) && ov_pend_i[hz_a[3:0]]) || ((hz_b < 5'd12) && ov_pend_i[hz_b[3:0]]);
        OpPwms:                        hz = ((hz_d < 5'd12) && ov_pend_i[hz_d[3:0]]) || ((hz_b < 5'd12) && ov_pend_i[hz_b[3:0]]);
        default: ;
      endcase
    end
  end
  wire nb_op = OVERLAP && (opc_q == OpSmpn) && first_q;   // non-blocking sampling operation

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      state_q    <= S_IDLE;
      prog_q     <= 2'd0;
      pc_q       <= '0;
      cnt_q      <= '0;
      opc_q      <= OpEnd;
      first_q    <= 1'b0;
      last_q     <= 1'b0;
      d_q        <= '0;
      a_q        <= '0;
      b_q        <= '0;
      done_o     <= 1'b0;
      cnt_ntt_o  <= '0;
      cnt_intt_o <= '0;
      cnt_pwm_o  <= '0;
      cnt_smp_o  <= '0;
      bcnt_q     <= '0;
      drain_q    <= '0;
    end else begin
      case (state_q)
        S_IDLE: begin
          if (start_ok) begin
            prog_q     <= prog_i;
            pc_q       <= '0;
            done_o     <= 1'b0;
            cnt_ntt_o  <= '0;
            cnt_intt_o <= '0;
            cnt_pwm_o  <= '0;
            cnt_smp_o  <= '0;
            state_q    <= S_FETCH;
          end
        end
        S_FETCH: if (!hz) begin
          {opc_q, first_q, last_q, d_q, a_q, b_q} <= op_w;
          cnt_q <= '0;
          case (op_w[20:17])
            OpNtt:   begin cnt_ntt_o  <= cnt_ntt_o + 6'd1;  state_q <= S_LOAD; end
            OpIntt:  begin cnt_intt_o <= cnt_intt_o + 6'd1; state_q <= S_LOAD; end
            OpPwm:   begin cnt_pwm_o  <= cnt_pwm_o + 6'd1;  state_q <= S_PASS; end
            OpAdd,
            OpSub:   state_q <= S_PASS;
            OpSmpn,
            OpSmpa:  begin cnt_smp_o  <= cnt_smp_o + 6'd1;  state_q <= S_SMPS; end
            OpPwms:  begin
              if (STREAM_A) begin
                cnt_pwm_o <= cnt_pwm_o + 6'd1;
                state_q   <= S_SMPS;
              end else begin
                state_q <= S_DONE;
              end
            end
            OpWait:  state_q <= OVERLAP ? S_WAITS : S_FETCH;
            default: begin   // END (or an unknown opcode): wait for a busy sampler first
              if (smp_busy) state_q <= S_WAITS;
              else          state_q <= S_DONE;
            end
          endcase
          if (op_w[20:17] == OpWait && !OVERLAP) pc_q <= pc_q + 6'd1;
        end
        S_LOAD: begin
          if (cnt_q == 9'd256) state_q <= S_START;
          else                 cnt_q   <= cnt_q + 9'd1;
        end
        S_START: begin
          if (core_busy_i) state_q <= S_RUN;
        end
        S_RUN: begin
          if (core_done_i && !core_busy_i) begin
            state_q <= S_UNLOAD;
            cnt_q   <= '0;
          end
        end
        S_UNLOAD: begin
          if (cnt_q == 9'(255 + CORE_RDLAT)) begin
            pc_q    <= pc_q + 6'd1;
            state_q <= S_FETCH;
          end else begin
            cnt_q <= cnt_q + 9'd1;
          end
        end
        S_PASS: begin
          if (cnt_q == pass_len - 9'd1) begin
            pc_q    <= pc_q + 6'd1;
            state_q <= S_FETCH;
          end else begin
            cnt_q <= cnt_q + 9'd1;
          end
        end
        S_SMPS: begin   // wait until the sampler is idle, then start it (one cycle)
          if (!smp_busy) begin
            bcnt_q  <= '0;
            drain_q <= '0;
            if (opc_q == OpPwms)  state_q <= S_PWMS;
            else if (nb_op)       begin pc_q <= pc_q + 6'd1; state_q <= S_FETCH; end
            else                  state_q <= S_SMPR;
          end
        end
        S_SMPR: begin   // blocking sampling: until the sampler is idle again (its beats are written meanwhile)
          if (!smp_busy && !smp_start) begin
            pc_q    <= pc_q + 6'd1;
            state_q <= S_FETCH;
          end
        end
        S_PWMS: begin
          bcnt_q <= nxt;
          if (nxt == 8'd128) begin
            if (drain_q == 3'(LatTag)) begin
              pc_q    <= pc_q + 6'd1;
              state_q <= S_FETCH;
            end else begin
              drain_q <= drain_q + 3'd1;
            end
          end
        end
        S_WAITS: begin
          if (!smp_busy) begin
            if (opc_q == OpWait) pc_q <= pc_q + 6'd1;
            if (opc_q == OpEnd) state_q <= S_DONE;
            else                state_q <= S_FETCH;
          end
        end
        default: begin   // S_DONE
          done_o  <= 1'b1;
          state_q <= S_IDLE;
        end
      endcase
    end
  end

  assign busy_o = !idle_st;

  wire unused_smp = &{1'b0, smp_clast, smp_done, smp_bytes, smp_perm, is_smp_op, seed_we_i};

`ifdef FORMAL
  always_ff @(posedge clk_i) begin
    if (rst_ni) begin
      assert (state_q <= S_DONE);
      assert (state_q != S_LOAD   || cnt_q <= 9'd256);
      assert (state_q != S_UNLOAD || cnt_q <= 9'(255 + CORE_RDLAT));
      assert (state_q != S_PASS   || cnt_q <  pass_len);
    end
  end
`endif

endmodule
`default_nettype wire
