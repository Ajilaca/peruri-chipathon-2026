`default_nettype none
`timescale 1ns/1ps
// rtl/keccak/keccak_round.sv
// Phase 7 (evidence/phase07/test_plan.md): one Keccak-f[1600] round, combinational: theta, rho, pi, chi, iota (FIPS 202 Section 3.2).
// State: 25 lanes of 64 bit packed as s_i[64*i +: 64], lane index i = x + 5y. The round constant is an input (selected by the permutation counter).
// No state, no data-dependent timing.

module keccak_round (
    input  wire [1599:0] s_i,
    input  wire [  63:0] rc_i,
    output wire [1599:0] s_o
);

  import keccak_pkg::*;

  function automatic logic [63:0] rotl(input logic [63:0] v, input logic [5:0] n);
    rotl = (n == 6'd0) ? v : ((v << n) | (v >> (7'd64 - {1'b0, n})));
  endfunction

  logic [63:0] a  [LANES];
  logic [63:0] c  [5];
  logic [63:0] d  [5];
  logic [63:0] th [LANES];
  logic [63:0] b  [LANES];
  logic [63:0] ch [LANES];

  always_comb begin
    for (int i = 0; i < LANES; i++) a[i] = s_i[64*i+:64];
    for (int x = 0; x < 5; x++) c[x] = a[x] ^ a[x+5] ^ a[x+10] ^ a[x+15] ^ a[x+20];
    for (int x = 0; x < 5; x++) d[x] = c[(x+4)%5] ^ rotl(c[(x+1)%5], 6'd1);
    for (int i = 0; i < LANES; i++) th[i] = a[i] ^ d[i%5];
    // rho then pi: B[y, 2x + 3y] = rot(A[x, y], offset[x, y])
    for (int x = 0; x < 5; x++)
      for (int y = 0; y < 5; y++) b[y+5*((2*x+3*y)%5)] = rotl(th[x+5*y], keccak_rho(5'(x+5*y)));
    for (int y = 0; y < 5; y++)
      for (int x = 0; x < 5; x++) ch[x+5*y] = b[x+5*y] ^ (~b[(x+1)%5+5*y] & b[(x+2)%5+5*y]);
  end

  genvar gi;
  generate
    for (gi = 0; gi < LANES; gi++) begin : g_out
      if (gi == 0) begin : g_l0
        assign s_o[64*gi+:64] = ch[gi] ^ rc_i;
      end else begin : g_ln
        assign s_o[64*gi+:64] = ch[gi];
      end
    end
  endgenerate

endmodule

`default_nettype wire
