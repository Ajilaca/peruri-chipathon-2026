`default_nettype none
`timescale 1ns/1ps
// rtl/sched/kpke_sched.sv
// Phase 6 (docs/evidence/phase06-scheduling/test_plan.md, ADR 0024): operation-level sequencer of the K-PKE arithmetic. It runs one of the fixed
// programs of rtl/sched/kpke_prog_rom.sv (generated from tb/golden/kpke_sched_model.py) on the slots of rtl/sched/poly_store.sv:
//
//   NTT / INTT s   LOAD   256 + 1 cycles: slot s -> NTT core through its host port (one coefficient per cycle)
//                  START  start_i held until the core reports busy (the core's own host-write guard decides the cycle; data-independent)
//                  RUN    until the core's done_o
//                  UNLOAD 256 + CORE_RDLAT cycles: core host port -> slot s (read data CORE_RDLAT cycles after the address)
//   PWM d a b F L  PASS   128 + 8 cycles: acc <- (F ? 0 : acc) + a o b (rtl/sched/pwm_unit.sv, latency 7, + 1 store read); when L the sum goes to slot d
//   ADD / SUB      PASS   128 + 2 cycles: slot d <- slot a +/- slot b
//
// Every operation has a fixed length and the program is fixed per prog_i, so the cycle count of a program does not depend on any data (constant time);
// no branch, address or loop count depends on polynomial values. The NTT core is used only through its host port (mode_i, start_i, host_*, busy_o,
// done_o), so any core with that port list can be connected (rtl/sched/kpke_sched_top.sv uses S7).
// Testbench port (tb_*): writes and reads single coefficients of any slot, only while the sequencer is idle (writes while busy are ignored).
// Reset: asynchronous, active low, on the state, counters and done flag; storage and datapath registers are not reset.

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module kpke_sched #(
    parameter int NPOLY      = 24,
    parameter int CORE_RDLAT = 4      // cycles from a host read address to its data at the NTT core (S7: 4)
) (
    input  wire         clk_i,
    input  wire         rst_ni,

    input  wire  [1:0]  prog_i,       // 0 KeyGen, 1 Encrypt, 2 Decrypt arithmetic
    input  wire         start_i,
    output logic        busy_o,
    output logic        done_o,

    input  wire         tb_we_i,
    input  wire  [4:0]  tb_slot_i,
    input  wire  [7:0]  tb_addr_i,
    input  wire  [11:0] tb_wdata_i,
    output logic [11:0] tb_rdata_o,   // one cycle after tb_slot_i / tb_addr_i

    output logic [5:0]  cnt_ntt_o,
    output logic [5:0]  cnt_intt_o,
    output logic [5:0]  cnt_pwm_o,

    output logic        core_mode_o,
    output logic        core_start_o,
    output logic [7:0]  core_haddr_o,
    output logic [11:0] core_hwdata_o,
    output logic        core_hwe_o,
    input  wire  [11:0] core_hrdata_i,
    input  wire         core_busy_i,
    input  wire         core_done_i
);

  localparam logic [2:0] OpEnd = 3'd0, OpNtt = 3'd1, OpIntt = 3'd2, OpPwm = 3'd3, OpAdd = 3'd4, OpSub = 3'd5;
  localparam int         LatPwm = 8;   // store read 1 + pwm_unit 7
  localparam int         LatAdd = 2;   // store read 1 + result register 1

  typedef enum logic [2:0] {S_IDLE, S_FETCH, S_LOAD, S_START, S_RUN, S_UNLOAD, S_PASS, S_DONE} state_t;
  state_t state_q;

  logic [1:0]  prog_q;
  logic [5:0]  pc_q;
  logic [8:0]  cnt_q;
  logic [2:0]  opc_q;
  logic        first_q, last_q;
  logic [4:0]  d_q, a_q, b_q;
  logic [19:0] op_w;

  kpke_prog_rom u_prog (.prog_i(prog_q), .pc_i(pc_q), .op_o(op_w));

  // -- store ------------------------------------------------------------------------------------------------
  logic [4:0]  ra_slot, rb_slot, w_slot;
  logic [6:0]  ra_pair, rb_pair, w_pair;
  logic [11:0] ra_e, ra_o, rb_e, rb_o, wd_e, wd_o;
  logic        we_e, we_o;

  poly_store #(.NPOLY(NPOLY)) u_store (
      .clk_i(clk_i),
      .ra_slot_i(ra_slot), .ra_pair_i(ra_pair), .ra_e_o(ra_e), .ra_o_o(ra_o),
      .rb_slot_i(rb_slot), .rb_pair_i(rb_pair), .rb_e_o(rb_e), .rb_o_o(rb_o),
      .we_e_i(we_e), .we_o_i(we_o), .w_slot_i(w_slot), .w_pair_i(w_pair), .wd_e_i(wd_e), .wd_o_i(wd_o));

  // -- accumulator of the PWM passes (128 pairs) -------------------------------------------------------------
  logic [11:0] acc_e [0:127];
  logic [11:0] acc_o [0:127];
  logic [11:0] acc_rd_e, acc_rd_o;
  logic        acc_we;

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

  pwm_unit u_pwm (
      .clk_i(clk_i),
      .a0_i(ra_e), .a1_i(ra_o), .b0_i(rb_e), .b1_i(rb_o), .gamma_i(gamma),
      .acc0_i(first_q ? 12'd0 : acc_rd_e), .acc1_i(first_q ? 12'd0 : acc_rd_o),
      .c0_o(pwm_c0), .c1_o(pwm_c1));

  always_ff @(posedge clk_i) begin
    pair_m1  <= cnt_q[6:0];
    half_q   <= (state_q == S_LOAD) ? cnt_q[0] : tb_addr_i[0];
    acc_rd_e <= acc_e[cnt_q[6:0]];
    acc_rd_o <= acc_o[cnt_q[6:0]];
    if (acc_we) begin
      acc_e[widx_pass[6:0]] <= pwm_c0;
      acc_o[widx_pass[6:0]] <= pwm_c1;
    end
    res_e <= (opc_q == OpSub) ? sub_mod(ra_e, rb_e) : add_mod(ra_e, rb_e);
    res_o <= (opc_q == OpSub) ? sub_mod(ra_o, rb_o) : add_mod(ra_o, rb_o);
  end

  assign acc_we = pass_wr && is_pwm && !last_q;

  // -- store port selection -----------------------------------------------------------------------------------
  always_comb begin
    ra_slot = tb_slot_i;
    ra_pair = tb_addr_i[7:1];
    rb_slot = b_q;
    rb_pair = cnt_q[6:0];
    if (state_q == S_LOAD) begin
      ra_slot = d_q;
      ra_pair = cnt_q[7:1];
    end else if (state_q == S_PASS) begin
      ra_slot = a_q;
      ra_pair = cnt_q[6:0];
    end

    we_e   = 1'b0;
    we_o   = 1'b0;
    w_slot = tb_slot_i;
    w_pair = tb_addr_i[7:1];
    wd_e   = tb_wdata_i;
    wd_o   = tb_wdata_i;
    if (state_q == S_IDLE || state_q == S_DONE) begin
      we_e = tb_we_i && !tb_addr_i[0];
      we_o = tb_we_i &&  tb_addr_i[0];
    end else if (unl_wr) begin
      w_slot = d_q;
      w_pair = widx_unl[7:1];
      wd_e   = core_hrdata_i;
      wd_o   = core_hrdata_i;
      we_e   = !widx_unl[0];
      we_o   =  widx_unl[0];
    end else if (pass_wr && !(is_pwm && !last_q)) begin
      w_slot = d_q;
      w_pair = widx_pass[6:0];
      wd_e   = is_pwm ? pwm_c0 : res_e;
      wd_o   = is_pwm ? pwm_c1 : res_o;
      we_e   = 1'b1;
      we_o   = 1'b1;
    end
  end

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
            state_q    <= S_FETCH;
          end
        end
        S_FETCH: begin
          {opc_q, first_q, last_q, d_q, a_q, b_q} <= op_w;
          cnt_q <= '0;
          case (op_w[19:17])
            OpNtt:   begin cnt_ntt_o  <= cnt_ntt_o + 6'd1;  state_q <= S_LOAD; end
            OpIntt:  begin cnt_intt_o <= cnt_intt_o + 6'd1; state_q <= S_LOAD; end
            OpPwm:   begin cnt_pwm_o  <= cnt_pwm_o + 6'd1;  state_q <= S_PASS; end
            OpAdd,
            OpSub:   state_q <= S_PASS;
            default: state_q <= S_DONE;
          endcase
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
        default: begin   // S_DONE
          done_o  <= 1'b1;
          state_q <= S_IDLE;
        end
      endcase
    end
  end

  assign busy_o = (state_q != S_IDLE) && (state_q != S_DONE);

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
