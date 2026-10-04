`default_nettype none
`timescale 1ns/1ps
// rtl/mlkem/mlkem_core4.sv
// Phase 9I item 4 (docs/evidence/phase09m-optimisation/9i4/test_plan_9i4.md): rtl/mlkem/mlkem_core3.sv (K1b with the background hash) with loads that run behind the K-PKE engine. Two micro-operations: RUNS (start the engine program and continue at once; the 12-bit mask of the slots that are loaded behind it is the interlock mask of the engine) and RUNJ (wait until the engine is done). The engine (rtl/sched/kpke_smp_top_s10o.sv) grants the host write port to the loader while it runs and starts an operation only after every slot it uses is completely loaded. ROM: rtl/mlkem/mlkem_ctl_rom3.sv. Requires CODEC_W2 = 1. Same ports and parameters as mlkem_core3.
// original header follows:
// Phase 9F step S1b (docs/evidence/phase09m-optimisation/9f1b/test_plan_9f1b.md, amendment A1): mlkem_core2 (itself a copy of mlkem_core with the parameter SMP_C5) with a background hash job: a second small sequencer (the sidecar) runs the words HST, HFD..., HGT, END stored after the main program of rtl/mlkem/mlkem_ctl_rom2.sv while the main controller continues; BGS starts a job, JN waits for it. The main controller always wins the read bus and the write bus; the sidecar uses the cycles it leaves. Written as a new module because the Quartus campaign of S1 reads mlkem_core2.sv.
// Phase 9F step S1 (docs/evidence/phase09m-optimisation/9f1/test_plan_9f1.md, amendment A1): a copy of rtl/mlkem/mlkem_core.sv (Phase 9 / 9M) with one added parameter SMP_C5 for the sampler sponge of the K-PKE engine. Written as a new module so that the Quartus campaigns that read mlkem_core.sv are not disturbed; at SMP_C5 = 1 it is the same design as mlkem_core. S1b (hash concurrency) builds on this file.
// Phase 9c (docs/evidence/phase09-integration/9c/test_plan_9c.md): ML-KEM-768 core: KeyGen_internal (op 0), Encaps_internal (op 1), Decaps_internal (op 2) of FIPS 203 Algorithms 16-18 as a straight-line micro-program (rtl/mlkem/mlkem_ctl_rom.sv, generated from
// tb/golden/mlkem_ctl_model.py) on byte buffers, a register file and the K-PKE engine of 8d. Randomness enters as data (d, z, m are written by the host). The FIPS 203 input checks are not in the RTL (ADR 0031).
// Host port (only while idle; a write while busy is ignored): h_addr_i[11:10] region (0 KB, 1 CB, 2 CB2, 3 RF), h_addr_i[8:0] word (h_addr_i[9] is not used), 64-bit words, byte k of word w is byte 8w + k; h_rdata_o is valid one cycle after the address.
//   KB (300 words): dk layout: dk_pke at word 0 (144 words), ek at word 144 (148 words; its rho at word 288), H(ek) at word 292, z at word 296. CB (136 words): ciphertext. CB2 (136 words): re-encrypted ciphertext.
//   RF (32 words = registers of 4 words): 0 d, 1 z, 2 m (m' in Decaps), 3 rho, 4 sigma / r, 5 K (K' in Decaps; the shared secret after Encaps and Decaps), 6 K_bar, 7 H(ek).
// Operation: write the inputs, op_i and start_i (accepted only when idle); busy_o until done_o (one pulse). Every micro-operation has a fixed length except the sampling of the public matrix inside the engine; no control depends on a secret.
// Reset: asynchronous, active low, on the control state; memories, the register file and the datapath registers are not reset. One clock domain.

module mlkem_core4 #(
    parameter bit HASH_C5  = 1'b1,     // hash instance: 1 C5 sponge (ADR 0027), 0 K0 sponge
    parameter bit SMP_C5   = 1'b1,     // sampler sponge inside the K-PKE engine: 1 C5 (ADR 0027), 0 K0 (S1)
    parameter bit NTT_P6   = 1'b0,     // S2: 1 adds the fourth multiplier cut to the NTT core of the engine (P = 6, 119 cycles per transform)
    parameter bit NTT_AR   = 1'b0,     // S2b: 1 registers the issue-stage addresses of the NTT core of the engine (no change of cycles or results)
    parameter bit CODEC_W2 = 1'b0      // load / store tasks: 0 the Phase 9 one-byte path, 1 the Phase 9M two-byte path (mlkem_ldpoly2 / mlkem_stpoly2, test_plan_9m1.md)
) (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire  [1:0]  op_i,
    input  wire         start_i,
    output wire         busy_o,
    output wire         done_o,
    input  wire         h_we_i,
    input  wire  [11:0] h_addr_i,
    input  wire  [63:0] h_wdata_i,
    output wire  [63:0] h_rdata_o
);

  localparam logic [3:0] OpEnd = 4'd0, OpLdp = 4'd1, OpStp = 4'd2, OpHst = 4'd3, OpHfd = 4'd4, OpHgt = 4'd5, OpSdl = 4'd6, OpRun = 4'd7, OpWr32 = 4'd8, OpRd32 = 4'd9, OpCmp = 4'd10, OpBgs = 4'd11, OpJn = 4'd12, OpRns = 4'd13, OpRnj = 4'd14;

  typedef enum logic [3:0] {S_IDLE, S_FETCH, S_DISP, S_LDP, S_STP, S_HFD, S_HGT, S_SDL, S_RUN, S_WR32, S_RD32, S_CMP, S_CMPK, S_RUNJ} state_t;
  state_t state_q;

  logic [1:0]  op_q;
  logic [5:0]  pc_q;
  logic [39:0] ins_q, rom_w;
  logic        done_q;

  mlkem_ctl_rom3 u_rom (.op_i(op_q), .pc_i(pc_q), .word_o(rom_w));

  wire [3:0]  opc    = ins_q[39:36];
  wire [3:0]  f_slot = ins_q[35:32];
  wire [1:0]  f_rgn  = ins_q[31:30];
  wire [8:0]  f_woff = ins_q[29:21];
  wire [1:0]  f_dsel = ins_q[20:19];
  wire [1:0]  f_hsel = ins_q[35:34];
  wire [10:0] f_hlen = ins_q[33:23];
  wire [2:0]  f_hsrc = ins_q[35:33];
  wire [8:0]  f_hwof = ins_q[32:24];
  wire [8:0]  f_hnw  = ins_q[23:15];
  wire [2:0]  f_da   = ins_q[35:33];
  wire [2:0]  f_db   = ins_q[32:30];
  wire [1:0]  f_prog = ins_q[35:34];
  wire [5:0]  f_bpc  = ins_q[35:30];
  wire [11:0] f_pm   = ins_q[33:22];   // RUNS: slots loaded behind the engine
  wire [2:0]  f_reg  = ins_q[35:33];
  wire [8:0]  f_rwof = ins_q[32:24];

  wire idle_st = (state_q == S_IDLE);
  assign busy_o = !idle_st;
  assign done_o = done_q;

  // -- background hash sidecar (S1b): state, program counter, instruction, feeder and digest counters -----------------------------------
  typedef enum logic [2:0] {B_IDLE, B_FETCH, B_DISP, B_HFD, B_HGT} bstate_t;
  bstate_t     bs_q;
  logic [5:0]  bpc_q;
  logic [39:0] bins_q, rom_bw;
  logic [8:0]  bfd_issued_q, bfd_cons_q;
  logic        bfd_valid_q, bhold_v_q, bgq_q;
  logic [63:0] bhold_q;
  logic [3:0]  bhg_w_q;

  mlkem_ctl_rom3 u_rom_b (.op_i(op_q), .pc_i(bpc_q), .word_o(rom_bw));

  wire [3:0]  b_opc  = bins_q[39:36];
  wire [1:0]  b_hsel = bins_q[35:34];
  wire [10:0] b_hlen = bins_q[33:23];
  wire [2:0]  b_hsrc = bins_q[35:33];
  wire [8:0]  b_hwof = bins_q[32:24];
  wire [8:0]  b_hnw  = bins_q[23:15];
  wire [2:0]  b_da   = bins_q[35:33];
  wire [2:0]  b_db   = bins_q[32:30];
  wire        bg_own = (bs_q != B_IDLE);

  // -- memories and register file ------------------------------------------------------------------------------
  logic [63:0] rf_q [0:31];
  logic        wr_en;
  logic [1:0]  wr_rgn;
  logic [8:0]  wr_addr;
  logic [63:0] wr_data;
  logic [8:0]  rd_addr;
  logic [1:0]  rd_rgn_q, h_rgn_q;
  logic [63:0] kb_q, cb_q, cb2_q, rf_rd_q, rd_data;

  mlkem_ram #(.DEPTH(300), .ADDR_W(9)) u_kb  (.clk_i(clk_i), .we_i(wr_en && wr_rgn == 2'd0), .waddr_i(wr_addr), .wdata_i(wr_data), .raddr_i(rd_addr), .rdata_o(kb_q));
  mlkem_ram #(.DEPTH(136), .ADDR_W(8)) u_cb  (.clk_i(clk_i), .we_i(wr_en && wr_rgn == 2'd1), .waddr_i(wr_addr[7:0]), .wdata_i(wr_data), .raddr_i(rd_addr[7:0]), .rdata_o(cb_q));
  mlkem_ram #(.DEPTH(136), .ADDR_W(8)) u_cb2 (.clk_i(clk_i), .we_i(wr_en && wr_rgn == 2'd2), .waddr_i(wr_addr[7:0]), .wdata_i(wr_data), .raddr_i(rd_addr[7:0]), .rdata_o(cb2_q));

  always_ff @(posedge clk_i) begin
    if (wr_en && wr_rgn == 2'd3) rf_q[wr_addr[4:0]] <= wr_data;
    rf_rd_q <= rf_q[rd_addr[4:0]];
  end

  always_comb begin
    case (bgq_q ? b_hsrc[1:0] : (idle_st ? h_rgn_q : rd_rgn_q))
      2'd0:    rd_data = kb_q;
      2'd1:    rd_data = cb_q;
      2'd2:    rd_data = cb2_q;
      default: rd_data = rf_rd_q;
    endcase
  end
  assign h_rdata_o = rd_data;

  // -- sub-blocks ----------------------------------------------------------------------------------------------
  // engine
  logic        eng_start, eng_busy, eng_done, eng_seed_we, eng_seed_sel, eng_tb_we;
  logic [1:0]  eng_prog, eng_seed_idx;
  logic [63:0] eng_seed_data;
  logic [4:0]  eng_tb_slot;
  logic [7:0]  eng_tb_addr;
  logic [11:0] eng_tb_wdata, eng_tb_rdata;
  /* verilator lint_off UNUSEDSIGNAL */
  logic [5:0]  eng_c0, eng_c1, eng_c2, eng_c3;
  logic        eng_ovf;
  /* verilator lint_on UNUSEDSIGNAL */

  logic        eng_wready;
  logic [11:0] pend_q;       // slots whose load is not complete (interlock mask of the engine)
  logic        eng_dn_q;     // the engine finished (sticky from RUNS to RUNJ)

  kpke_smp_top_s10o #(.NPOLY(12), .VAR(2), .STREAM_A(1'b1), .OVERLAP(1'b1), .CORE_R2(SMP_C5), .NTT_P6(NTT_P6), .NTT_AR(NTT_AR), .HOSTOV(1'b1)) u_eng (
      .clk_i(clk_i), .rst_ni(rst_ni), .prog_i(eng_prog), .start_i(eng_start), .busy_o(eng_busy), .done_o(eng_done),
      .tb_we_i(eng_tb_we), .tb_slot_i(eng_tb_slot), .tb_addr_i(eng_tb_addr), .tb_wdata_i(eng_tb_wdata), .tb_rdata_o(eng_tb_rdata), .tb_wready_o(eng_wready), .ov_pend_i(pend_q),
      .seed_we_i(eng_seed_we), .seed_sel_i(eng_seed_sel), .seed_idx_i(eng_seed_idx), .seed_data_i(eng_seed_data),
      .cnt_ntt_o(eng_c0), .cnt_intt_o(eng_c1), .cnt_pwm_o(eng_c2), .cnt_smp_o(eng_c3), .bank_overflow_o(eng_ovf));

  // load / store tasks
  logic        ld_start, ld_we, ld_busy, ld_done;
  logic [8:0]  ld_rd_addr;
  logic [4:0]  ld_slot;
  logic [7:0]  ld_addr;
  logic [11:0] ld_wdata;
  logic        ld_rd_req_u;
  generate
  if (CODEC_W2) begin : g_ld2
    mlkem_ldpoly2o u_ld (
        .clk_i(clk_i), .rst_ni(rst_ni), .start_i(ld_start), .dsel_i(f_dsel), .slot_i(f_slot), .woff_i(f_woff),
        .rd_req_o(ld_rd_req_u), .rd_addr_o(ld_rd_addr), .rd_data_i(rd_data),
        .tb_wready_i(eng_wready), .tb_we_o(ld_we), .tb_slot_o(ld_slot), .tb_addr_o(ld_addr), .tb_wdata_o(ld_wdata), .busy_o(ld_busy), .done_o(ld_done));
  end else begin : g_ld1
    // the one-byte loader of Phase 9 has no write handshake: not supported here
    initial $error("mlkem_core4 requires CODEC_W2 = 1");
    assign ld_rd_req_u = 1'b0;
    assign ld_rd_addr  = 9'd0;
    assign ld_we       = 1'b0;
    assign ld_slot     = 5'd0;
    assign ld_addr     = 8'd0;
    assign ld_wdata    = 12'd0;
    assign ld_busy     = 1'b0;
    assign ld_done     = 1'b0;
  end
  endgenerate

  logic        st_start, st_wr_en, st_busy, st_done;
  logic [4:0]  st_slot;
  logic [7:0]  st_addr;
  logic [8:0]  st_wr_addr;
  logic [63:0] st_wr_data;
  generate
  if (CODEC_W2) begin : g_st2
    mlkem_stpoly2 u_st (
        .clk_i(clk_i), .rst_ni(rst_ni), .start_i(st_start), .dsel_i(f_dsel), .slot_i(f_slot), .woff_i(f_woff),
        .tb_slot_o(st_slot), .tb_addr_o(st_addr), .tb_rdata_i(eng_tb_rdata),
        .wr_en_o(st_wr_en), .wr_addr_o(st_wr_addr), .wr_data_o(st_wr_data), .busy_o(st_busy), .done_o(st_done));
  end else begin : g_st1
    mlkem_stpoly u_st (
        .clk_i(clk_i), .rst_ni(rst_ni), .start_i(st_start), .dsel_i(f_dsel), .slot_i(f_slot), .woff_i(f_woff),
        .tb_slot_o(st_slot), .tb_addr_o(st_addr), .tb_rdata_i(eng_tb_rdata),
        .wr_en_o(st_wr_en), .wr_addr_o(st_wr_addr), .wr_data_o(st_wr_data), .busy_o(st_busy), .done_o(st_done));
  end
  endgenerate

  // hash and comparison
  logic        hs_start, hs_in_valid, hs_in_ready, hs_out_valid, hs_out_ready, hs_out_last, hs_busy, hs_done;
  logic [63:0] hs_in_data, hs_out_data;
  wire [1:0]  hx_sel = bg_own ? b_hsel : f_hsel;
  wire [15:0] hx_len = bg_own ? {5'd0, b_hlen} : {5'd0, f_hlen};
  mlkem_hash #(.CORE_R2(HASH_C5)) u_hash (
      .clk_i(clk_i), .rst_ni(rst_ni), .start_i(hs_start), .sel_i(hx_sel), .len_i(hx_len),
      .in_valid_i(hs_in_valid), .in_ready_o(hs_in_ready), .in_data_i(hs_in_data),
      .out_valid_o(hs_out_valid), .out_ready_i(hs_out_ready), .out_data_o(hs_out_data), .out_last_o(hs_out_last),
      .busy_o(hs_busy), .done_o(hs_done));

  logic         fo_start, fo_in_valid, fo_in_ready, fo_busy, fo_done, fo_neq;
  logic [255:0] fo_k;
  wire  [255:0] k_good = {rf_q[23], rf_q[22], rf_q[21], rf_q[20]};
  wire  [255:0] k_bad  = {rf_q[27], rf_q[26], rf_q[25], rf_q[24]};
  mlkem_fo_cmp #(.WORDS(136)) u_fo (
      .clk_i(clk_i), .rst_ni(rst_ni), .start_i(fo_start), .in_valid_i(fo_in_valid), .in_ready_o(fo_in_ready), .a_data_i(cb_q), .b_data_i(cb2_q),
      .kgood_i(k_good), .kbad_i(k_bad), .k_o(fo_k), .neq_o(fo_neq), .busy_o(fo_busy), .done_o(fo_done));

  // -- feeder (HFD), digest capture (HGT), seeds (SDL), compare stream (CMP), 32-byte moves (WR32 / RD32) ------------------
  logic [8:0] fd_issued_q, fd_cons_q;
  logic       fd_valid_q, hold_v_q;
  logic [63:0] hold_q;
  logic [3:0] hg_w_q;
  logic [3:0] k_q;           // step counter of SDL, WR32, RD32, CMPK
  logic [8:0] cm_issued_q;
  logic       cm_valid_q;

  wire        fd_const = (f_hsrc == 3'd4);
  wire        fg_in_valid = (state_q == S_HFD) && (hold_v_q || fd_valid_q);
  wire        bg_in_valid = (bs_q == B_HFD) && (bhold_v_q || bfd_valid_q);
  wire        bg_const    = (b_hsrc == 3'd4);
  assign      hs_in_valid = bg_own ? bg_in_valid : fg_in_valid;
  assign      hs_in_data  = bg_own ? (bhold_v_q ? bhold_q : (bg_const ? 64'd3 : rd_data)) : (hold_v_q ? hold_q : (fd_const ? 64'd3 : rd_data));
  wire        fd_consumed = fg_in_valid && hs_in_ready;
  wire        fd_issue    = (state_q == S_HFD) && (fd_issued_q != f_hnw) && ((!fd_valid_q && !hold_v_q) || fd_consumed);
  wire        bfd_consumed = bg_in_valid && hs_in_ready;

  wire   fg_out_ready = (state_q == S_HGT);
  logic  fg_wr_en;
  logic        fw_en;
  logic [1:0]  fw_rgn;
  logic [8:0]  fw_addr;
  logic [63:0] fw_data;
  wire   bg_out_ready = (bs_q == B_HGT) && !fg_wr_en;
  assign hs_out_ready = bg_own ? bg_out_ready : fg_out_ready;
  wire   hg_take      = hs_out_valid && fg_out_ready;
  wire   bg_take      = hs_out_valid && bg_out_ready;

  assign fo_in_valid  = (state_q == S_CMP) && cm_valid_q;
  wire   cm_issue     = (state_q == S_CMP) && (cm_issued_q != 9'd136);

  // the main controller always wins the read bus; the sidecar issues in a cycle in which the main controller issues none
  wire        fg_rd_req   = ((state_q == S_LDP) && ld_rd_req_u) || fd_issue || ((state_q == S_RD32) && (k_q < 4'd4)) || ((state_q == S_CMP) && cm_issue);
  wire        bfd_issue   = (bs_q == B_HFD) && (bfd_issued_q != b_hnw) && ((!bfd_valid_q && !bhold_v_q) || bfd_consumed) && !fg_rd_req;

  // read address bus and write bus
  always_comb begin
    rd_addr = h_addr_i[8:0];
    if (bfd_issue) begin
      rd_addr = b_hwof + bfd_issued_q;
    end else if (!idle_st) begin
      case (state_q)
        S_LDP:   rd_addr = ld_rd_addr;
        S_HFD:   rd_addr = f_hwof + fd_issued_q;
        S_RD32:  rd_addr = f_rwof + 9'(k_q);
        S_CMP:   rd_addr = cm_issued_q;
        default: rd_addr = 9'd0;
      endcase
    end
    fw_en   = 1'b0;
    fw_rgn  = 2'd0;
    fw_addr = 9'd0;
    fw_data = 64'd0;
    case (state_q)
      S_IDLE: begin
        fw_en   = h_we_i;
        fw_rgn  = h_addr_i[11:10];
        fw_addr = h_addr_i[8:0];
        fw_data = h_wdata_i;
      end
      S_STP: begin
        fw_en   = st_wr_en;
        fw_rgn  = f_rgn;
        fw_addr = st_wr_addr;
        fw_data = st_wr_data;
      end
      S_HGT: begin
        fw_en   = hg_take;
        fw_rgn  = 2'd3;
        fw_addr = {4'd0, (hg_w_q[2] ? f_db : f_da), hg_w_q[1:0]};
        fw_data = hs_out_data;
      end
      S_WR32: begin
        fw_en   = (k_q < 4'd4);
        fw_rgn  = 2'd0;
        fw_addr = f_rwof + 9'(k_q);
        fw_data = rf_q[{f_reg, k_q[1:0]}];
      end
      S_RD32: begin
        fw_en   = (k_q != 4'd0);
        fw_rgn  = 2'd3;
        fw_addr = {4'd0, f_reg, k_q[1:0] - 2'd1};
        fw_data = rd_data;
      end
      S_CMPK: begin
        fw_en   = (k_q < 4'd4);
        fw_rgn  = 2'd3;
        fw_addr = {4'd0, 3'd5, k_q[1:0]};
        fw_data = fo_k[64*k_q[1:0] +: 64];
      end
      default: ;
    endcase
  end

  // write bus: the main controller wins; the digest of the background job takes a cycle in which the main controller does not write
  assign fg_wr_en = fw_en;
  always_comb begin
    wr_en   = fw_en;
    wr_rgn  = fw_rgn;
    wr_addr = fw_addr;
    wr_data = fw_data;
    if (!fw_en && bg_take) begin
      wr_en   = 1'b1;
      wr_rgn  = 2'd3;
      wr_addr = {4'd0, (bhg_w_q[2] ? b_db : b_da), bhg_w_q[1:0]};
      wr_data = hs_out_data;
    end
  end

  // engine host port and seed port
  always_comb begin
    eng_tb_we    = 1'b0;
    eng_tb_slot  = 5'd0;
    eng_tb_addr  = 8'd0;
    eng_tb_wdata = 12'd0;
    if (state_q == S_LDP) begin
      eng_tb_we    = ld_we;
      eng_tb_slot  = ld_slot;
      eng_tb_addr  = ld_addr;
      eng_tb_wdata = ld_wdata;
    end else if (state_q == S_STP) begin
      eng_tb_slot = st_slot;
      eng_tb_addr = st_addr;
    end
    eng_seed_we   = (state_q == S_SDL) && (k_q < 4'd8);
    eng_seed_sel  = k_q[2];
    eng_seed_idx  = k_q[1:0];
    eng_seed_data = rf_q[{3'd3 + {2'd0, k_q[2]}, k_q[1:0]}];
  end
  assign eng_prog = f_prog;

  wire disp = (state_q == S_DISP);
  assign ld_start = disp && (opc == OpLdp);
  assign st_start = disp && (opc == OpStp);
  wire   bg_hs_start = (bs_q == B_DISP) && (b_opc == OpHst);
  wire   m_hs_start  = disp && (opc == OpHst) && !bg_own;
  assign hs_start = m_hs_start || bg_hs_start;
  assign eng_start = disp && ((opc == OpRun) || (opc == OpRns));
  assign fo_start = disp && (opc == OpCmp);

  // -- sequencer -----------------------------------------------------------------------------------------------
  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      state_q     <= S_IDLE;
      op_q        <= 2'd0;
      pc_q        <= 6'd0;
      done_q      <= 1'b0;
      rd_rgn_q    <= 2'd0;
      h_rgn_q     <= 2'd0;
      fd_issued_q <= 9'd0;
      fd_cons_q   <= 9'd0;
      fd_valid_q  <= 1'b0;
      hold_v_q    <= 1'b0;
      hg_w_q      <= 4'd0;
      k_q         <= 4'd0;
      cm_issued_q <= 9'd0;
      cm_valid_q  <= 1'b0;
      bs_q         <= B_IDLE;
      bpc_q        <= 6'd0;
      bfd_issued_q <= 9'd0;
      bfd_cons_q   <= 9'd0;
      bfd_valid_q  <= 1'b0;
      bhold_v_q    <= 1'b0;
      bhg_w_q      <= 4'd0;
      bgq_q        <= 1'b0;
      pend_q       <= 12'd0;
      eng_dn_q     <= 1'b0;
    end else begin
      done_q  <= 1'b0;
      h_rgn_q <= h_addr_i[11:10];
      bgq_q   <= bfd_issue;
      if (eng_done) eng_dn_q <= 1'b1;
      if (state_q == S_LDP && ld_done && f_slot < 4'd12) pend_q[f_slot] <= 1'b0;   // the load of this slot is complete
      // background hash sidecar
      case (bs_q)
        B_FETCH: bs_q <= B_DISP;
        B_DISP: begin
          bfd_issued_q <= 9'd0;
          bfd_cons_q   <= 9'd0;
          bfd_valid_q  <= 1'b0;
          bhold_v_q    <= 1'b0;
          bhg_w_q      <= 4'd0;
          case (b_opc)
            OpHst: begin
              bpc_q <= bpc_q + 6'd1;
              bs_q  <= B_FETCH;
            end
            OpHfd:   bs_q <= B_HFD;
            OpHgt:   bs_q <= B_HGT;
            default: bs_q <= B_IDLE;       // END (or a wrong word) ends the job
          endcase
        end
        B_HFD: begin
          bfd_valid_q <= bfd_issue;
          if (bfd_issue) bfd_issued_q <= bfd_issued_q + 9'd1;
          if (bfd_consumed) begin
            bfd_cons_q <= bfd_cons_q + 9'd1;
            bhold_v_q  <= 1'b0;
          end else if (bfd_valid_q && !bhold_v_q) begin
            bhold_v_q <= 1'b1;
            bhold_q   <= bg_const ? 64'd3 : rd_data;
          end
          if (bfd_consumed && (bfd_cons_q + 9'd1 == b_hnw)) begin
            bpc_q <= bpc_q + 6'd1;
            bs_q  <= B_FETCH;
          end
        end
        B_HGT: begin
          if (bg_take) bhg_w_q <= bhg_w_q + 4'd1;
          if (hs_done) begin
            bpc_q <= bpc_q + 6'd1;
            bs_q  <= B_FETCH;
          end
        end
        default: ;
      endcase
      case (state_q)
        S_IDLE: begin
          if (start_i) begin
            op_q    <= op_i;
            pc_q    <= 6'd0;
            state_q <= S_FETCH;
          end
        end
        S_FETCH: state_q <= S_DISP;
        S_DISP: begin
          fd_issued_q <= 9'd0;
          fd_cons_q   <= 9'd0;
          fd_valid_q  <= 1'b0;
          hold_v_q    <= 1'b0;
          hg_w_q      <= 4'd0;
          k_q         <= 4'd0;
          cm_issued_q <= 9'd0;
          cm_valid_q  <= 1'b0;
          case (opc)
            OpEnd: if (!bg_own) begin              // the result registers are complete when done_o rises
              done_q  <= 1'b1;
              state_q <= S_IDLE;
            end
            OpLdp: begin
              rd_rgn_q <= f_rgn;
              state_q  <= S_LDP;
            end
            OpStp:  state_q <= S_STP;
            OpHst: if (!bg_own) begin              // the hash unit belongs to the background job while it runs
              pc_q    <= pc_q + 6'd1;
              state_q <= S_FETCH;
            end
            OpBgs: if (!bg_own) begin
              bpc_q   <= f_bpc;
              bs_q    <= B_FETCH;
              pc_q    <= pc_q + 6'd1;
              state_q <= S_FETCH;
            end
            OpJn: if (!bg_own) begin
              pc_q    <= pc_q + 6'd1;
              state_q <= S_FETCH;
            end
            OpHfd: if (!bg_own) begin
              rd_rgn_q <= f_hsrc[1:0];
              state_q  <= S_HFD;
            end
            OpHgt:  if (!bg_own) state_q <= S_HGT;
            OpSdl:  state_q <= S_SDL;
            OpRun:  state_q <= S_RUN;
            OpRns: begin                           // start the engine and continue; the slots in the mask are loaded behind it
              pend_q   <= f_pm;
              eng_dn_q <= 1'b0;
              pc_q     <= pc_q + 6'd1;
              state_q  <= S_FETCH;
            end
            OpRnj:  state_q <= S_RUNJ;
            OpWr32: state_q <= S_WR32;
            OpRd32: begin
              rd_rgn_q <= 2'd0;
              state_q  <= S_RD32;
            end
            OpCmp:  state_q <= S_CMP;
            default: begin
              done_q  <= 1'b1;
              state_q <= S_IDLE;
            end
          endcase
        end
        S_LDP: if (ld_done) begin
          pc_q    <= pc_q + 6'd1;
          state_q <= S_FETCH;
        end
        S_STP: if (st_done) begin
          pc_q    <= pc_q + 6'd1;
          state_q <= S_FETCH;
        end
        S_HFD: begin
          fd_valid_q <= fd_issue;
          if (fd_issue) fd_issued_q <= fd_issued_q + 9'd1;
          if (fd_consumed) begin
            fd_cons_q <= fd_cons_q + 9'd1;
            hold_v_q  <= 1'b0;
          end else if (fd_valid_q && !hold_v_q) begin
            hold_v_q <= 1'b1;
            hold_q   <= fd_const ? 64'd3 : rd_data;
          end
          if (fd_consumed && (fd_cons_q + 9'd1 == f_hnw)) begin
            pc_q    <= pc_q + 6'd1;
            state_q <= S_FETCH;
          end
        end
        S_HGT: begin
          if (hg_take) hg_w_q <= hg_w_q + 4'd1;
          if (hs_done) begin
            pc_q    <= pc_q + 6'd1;
            state_q <= S_FETCH;
          end
        end
        S_SDL: begin
          k_q <= k_q + 4'd1;
          if (k_q == 4'd7) begin
            pc_q    <= pc_q + 6'd1;
            state_q <= S_FETCH;
          end
        end
        S_RUN: if (eng_done) begin
          pc_q    <= pc_q + 6'd1;
          state_q <= S_FETCH;
        end
        S_RUNJ: if (eng_dn_q || eng_done) begin
          pend_q  <= 12'd0;
          pc_q    <= pc_q + 6'd1;
          state_q <= S_FETCH;
        end
        S_WR32: begin
          k_q <= k_q + 4'd1;
          if (k_q == 4'd3) begin
            pc_q    <= pc_q + 6'd1;
            state_q <= S_FETCH;
          end
        end
        S_RD32: begin
          k_q <= k_q + 4'd1;
          if (k_q == 4'd4) begin
            pc_q    <= pc_q + 6'd1;
            state_q <= S_FETCH;
          end
        end
        S_CMP: begin
          cm_valid_q <= cm_issue;
          if (cm_issue) cm_issued_q <= cm_issued_q + 9'd1;
          if (fo_done) begin
            k_q     <= 4'd0;
            state_q <= S_CMPK;
          end
        end
        S_CMPK: begin
          k_q <= k_q + 4'd1;
          if (k_q == 4'd3) begin
            pc_q    <= pc_q + 6'd1;
            state_q <= S_FETCH;
          end
        end
        default: state_q <= S_IDLE;
      endcase
    end
  end

  always_ff @(posedge clk_i) begin
    if (state_q == S_FETCH) ins_q <= rom_w;
    if (bs_q == B_FETCH)    bins_q <= rom_bw;
  end

  wire unused_ok = &{1'b0, eng_busy, ld_busy, st_busy, hs_busy, fo_busy, fo_neq, ld_rd_req_u, fo_in_ready, hs_out_last, h_addr_i[9], ins_q[14:0], bins_q[14:0]};

endmodule
`default_nettype wire
