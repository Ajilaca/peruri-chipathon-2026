`default_nettype none
`timescale 1ns/1ps
// rtl/sample/keccak_sampler.sv
// Phase 8b, stage W1 (docs/evidence/phase08-keccak-stream/8b/test_plan_8b.md section 1): Keccak sponge + streaming sampler, and the top of the Quartus revisions.
// kind_i 0: SampleNTT on SHAKE128 (mode 2), the message is rho || j || i (34 bytes); kind_i 1: SamplePolyCBD_2 on SHAKE256 (mode 3), the message is sigma || N (33 bytes). Any len_i is allowed.
// CORE_R2 = 1 uses keccak_sponge_r2 (C5, 14 cycles per permutation), 0 uses keccak_sponge (K0, 26). The message words pass through to the sponge; the sponge output words go straight to the selected core.
// When the polynomial is complete (fin of the core) or on abort_i the wrapper issues stop_i: the sponge returns to idle and wipes its state. done_o pulses after the last coefficient is handed over.
// start_i is accepted when not busy. Reset: asynchronous, active low. One clock domain, clk_i.

module keccak_sampler #(
    parameter bit CORE_R2 = 1'b1
) (
    input  wire        clk_i,
    input  wire        rst_ni,
    input  wire        start_i,
    input  wire        kind_i,         // 0 SampleNTT, 1 CBD2
    input  wire [15:0] len_i,          // message bytes
    input  wire        abort_i,
    input  wire        in_valid_i,
    output wire        in_ready_o,
    input  wire [63:0] in_data_i,
    output wire        coef_valid_o,
    input  wire        coef_ready_i,
    output wire [11:0] coef_data_o,
    output wire        coef_last_o,
    output wire [15:0] bytes_o,        // stream bytes consumed by the sampler
    output wire        busy_o,
    output wire        done_o,
    output wire [15:0] perm_cnt_o
);

  logic kind_q;

  // sponge
  logic sp_out_valid, sp_out_ready, sp_stop, sp_busy;
  logic [63:0] sp_out_data;
  logic sp_out_last;

  // cores
  logic n_in_ready, c_in_ready, n_busy, c_busy, n_fin, c_fin, n_done, c_done;
  logic n_cv, c_cv, n_cl, c_cl;
  logic [11:0] n_cd, c_cd;
  logic [15:0] n_bytes, c_bytes;

  assign busy_o = n_busy || c_busy;
  wire start_ok = start_i && !busy_o;
  assign sp_stop = abort_i || n_fin || c_fin;

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) kind_q <= 1'b0;
    else if (start_ok) kind_q <= kind_i;
  end

  generate
    if (CORE_R2) begin : g_r2
      keccak_sponge_r2 u_sp (
          .clk_i      (clk_i),
          .rst_ni     (rst_ni),
          .start_i    (start_ok),
          .mode_i     ({1'b1, kind_i}),
          .len_i      (len_i),
          .stop_i     (sp_stop),
          .in_valid_i (in_valid_i),
          .in_ready_o (in_ready_o),
          .in_data_i  (in_data_i),
          .out_valid_o(sp_out_valid),
          .out_ready_i(sp_out_ready),
          .out_data_o (sp_out_data),
          .out_last_o (sp_out_last),
          .busy_o     (sp_busy),
          .perm_cnt_o (perm_cnt_o)
      );
    end else begin : g_k0
      keccak_sponge u_sp (
          .clk_i      (clk_i),
          .rst_ni     (rst_ni),
          .start_i    (start_ok),
          .mode_i     ({1'b1, kind_i}),
          .len_i      (len_i),
          .stop_i     (sp_stop),
          .in_valid_i (in_valid_i),
          .in_ready_o (in_ready_o),
          .in_data_i  (in_data_i),
          .out_valid_o(sp_out_valid),
          .out_ready_i(sp_out_ready),
          .out_data_o (sp_out_data),
          .out_last_o (sp_out_last),
          .busy_o     (sp_busy),
          .perm_cnt_o (perm_cnt_o)
      );
    end
  endgenerate

  sample_ntt_core u_ntt (
      .clk_i       (clk_i),
      .rst_ni      (rst_ni),
      .start_i     (start_ok && !kind_i),
      .abort_i     (abort_i),
      .in_valid_i  (sp_out_valid && !kind_q),
      .in_ready_o  (n_in_ready),
      .in_data_i   (sp_out_data),
      .coef_valid_o(n_cv),
      .coef_ready_i(coef_ready_i),
      .coef_data_o (n_cd),
      .coef_last_o (n_cl),
      .bytes_o     (n_bytes),
      .busy_o      (n_busy),
      .fin_o       (n_fin),
      .done_o      (n_done)
  );

  cbd2_core u_cbd (
      .clk_i       (clk_i),
      .rst_ni      (rst_ni),
      .start_i     (start_ok && kind_i),
      .abort_i     (abort_i),
      .in_valid_i  (sp_out_valid && kind_q),
      .in_ready_o  (c_in_ready),
      .in_data_i   (sp_out_data),
      .coef_valid_o(c_cv),
      .coef_ready_i(coef_ready_i),
      .coef_data_o (c_cd),
      .coef_last_o (c_cl),
      .bytes_o     (c_bytes),
      .busy_o      (c_busy),
      .fin_o       (c_fin),
      .done_o      (c_done)
  );

  assign sp_out_ready = kind_q ? c_in_ready : n_in_ready;
  assign coef_valid_o = kind_q ? c_cv : n_cv;
  assign coef_data_o = kind_q ? c_cd : n_cd;
  assign coef_last_o = kind_q ? c_cl : n_cl;
  assign bytes_o = kind_q ? c_bytes : n_bytes;
  assign done_o = n_done || c_done;

  wire unused_ok = &{1'b0, sp_out_last, sp_busy};

endmodule

`default_nettype wire
