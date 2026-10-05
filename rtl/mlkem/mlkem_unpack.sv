`default_nettype none
`timescale 1ns/1ps
// rtl/mlkem/mlkem_unpack.sv
// Phase 9a (evidence/phase09/9a/test_plan_9a.md): ByteDecode_d -> Decompress_d -> coefficients (FIPS 203 Algorithm 6, Section 4.2.1).
// One run takes exactly 32 d bytes and gives exactly 256 coefficients, d chosen by dsel_i at start_i: 0 -> 1, 1 -> 4, 2 -> 10, 3 -> 12. For d = 12 the 12-bit value is reduced mod q (one subtraction of q when it is >= q; 4,095 < 2 q); for d < 12
// Decompress_d(y) = (3329 y + 2^(d-1)) >> d, written as four shifted terms (no division, no multiplier needed).
// The unpacker takes one byte per cycle into a 24-bit buffer (a byte is accepted when at most 16 bits are held) and takes d bits per coefficient into an output register. Counters and stalls depend on d and on the handshakes only, never on data.
// start_i is accepted only when idle; dsel_i is latched at start. coef_last_o marks coefficient 255; done_o is one pulse the cycle after that coefficient is accepted.
// Reset: asynchronous, active low, on the control state; the datapath registers are not reset (the bit buffer is cleared at start).

module mlkem_unpack (
    input  wire         clk_i,
    input  wire         rst_ni,
    input  wire         start_i,
    input  wire  [1:0]  dsel_i,
    input  wire         byte_valid_i,
    output wire         byte_ready_o,
    input  wire  [7:0]  byte_data_i,
    output wire         coef_valid_o,
    input  wire         coef_ready_i,
    output wire  [11:0] coef_data_o,
    output wire         coef_last_o,
    output wire         busy_o,
    output wire         done_o
);

  logic        busy_q, done_q;
  logic [1:0]  dsel_q;
  logic [3:0]  dv_q;
  logic [8:0]  nbytes_q;   // 32 d
  logic [8:0]  bin_q;      // bytes accepted
  logic [8:0]  cout_q;     // coefficients taken from the buffer
  logic [4:0]  cnt_q;      // bits in the buffer (0 .. 24)
  logic        ov_q, olast_q;
  logic [11:0] od_q;
  logic [23:0] acc_q;

  logic [3:0] dv_in;
  logic [8:0] nb_in;
  always_comb begin
    case (dsel_i)
      2'd0:    begin dv_in = 4'd1;  nb_in = 9'd32;  end
      2'd1:    begin dv_in = 4'd4;  nb_in = 9'd128; end
      2'd2:    begin dv_in = 4'd10; nb_in = 9'd320; end
      default: begin dv_in = 4'd12; nb_in = 9'd384; end
    endcase
  end

  wire start_ok = start_i && !busy_q;
  assign byte_ready_o = busy_q && (bin_q != nbytes_q) && (cnt_q <= 5'd16);
  wire baccept  = byte_valid_i && byte_ready_o;
  wire drain    = ov_q && coef_ready_i;
  wire take     = busy_q && (cnt_q >= {1'b0, dv_q}) && (cout_q != 9'd256) && (!ov_q || coef_ready_i);
  assign coef_valid_o = ov_q;
  assign coef_data_o  = od_q;
  assign coef_last_o  = ov_q && olast_q;
  assign busy_o = busy_q;
  assign done_o = done_q;

  // -- Decompress_d of the next d bits ---------------------------------------------------------------------------
  logic [11:0] x, dec;
  logic [21:0] t;
  logic [9:0]  y;
  always_comb begin
    case (dsel_q)
      2'd0:    y = {9'd0, acc_q[0]};
      2'd1:    y = {6'd0, acc_q[3:0]};
      default: y = acc_q[9:0];
    endcase
    x = (dsel_q == 2'd3) ? acc_q[11:0] : {2'd0, y};
    t = ({12'd0, y} << 11) + ({12'd0, y} << 10) + ({12'd0, y} << 8) + {12'd0, y};   // 3329 y
    case (dsel_q)
      2'd0:    dec = 12'((t + 22'd1) >> 1);
      2'd1:    dec = 12'((t + 22'd8) >> 4);
      2'd2:    dec = 12'((t + 22'd512) >> 10);
      default: dec = (x >= 12'd3329) ? (x - 12'd3329) : x;
    endcase
  end

  logic [4:0]  take_bits, cnt_after;
  logic [23:0] acc_after, acc_ins;
  always_comb begin
    take_bits = take ? {1'b0, dv_q} : 5'd0;
    cnt_after = cnt_q - take_bits;
    acc_after = acc_q >> take_bits;
    acc_ins   = {16'd0, byte_data_i} << cnt_after;
  end

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      busy_q   <= 1'b0;
      done_q   <= 1'b0;
      dsel_q   <= 2'd0;
      dv_q     <= 4'd1;
      nbytes_q <= 9'd32;
      bin_q    <= 9'd0;
      cout_q   <= 9'd0;
      cnt_q    <= 5'd0;
      ov_q     <= 1'b0;
      olast_q  <= 1'b0;
    end else begin
      done_q <= 1'b0;
      if (start_ok) begin
        busy_q   <= 1'b1;
        dsel_q   <= dsel_i;
        dv_q     <= dv_in;
        nbytes_q <= nb_in;
        bin_q    <= 9'd0;
        cout_q   <= 9'd0;
        cnt_q    <= 5'd0;
        ov_q     <= 1'b0;
        olast_q  <= 1'b0;
      end else if (busy_q) begin
        if (baccept) bin_q <= bin_q + 9'd1;
        cnt_q <= cnt_after + (baccept ? 5'd8 : 5'd0);
        if (take) begin
          cout_q  <= cout_q + 9'd1;
          ov_q    <= 1'b1;
          olast_q <= (cout_q == 9'd255);
        end else if (drain) begin
          ov_q <= 1'b0;
        end
        if (drain && olast_q) begin
          busy_q <= 1'b0;
          done_q <= 1'b1;
        end
      end
    end
  end

  always_ff @(posedge clk_i) begin
    if (take) od_q <= dec;
    if (start_ok) acc_q <= 24'd0;
    else          acc_q <= acc_after | (baccept ? acc_ins : 24'd0);
  end

endmodule
`default_nettype wire
