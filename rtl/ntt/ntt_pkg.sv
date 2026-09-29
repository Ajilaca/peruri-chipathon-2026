`default_nettype none
`timescale 1ns/1ps
// rtl/ntt/ntt_pkg.sv
// Shared constants and modular-arithmetic helper functions for the Phase 1 NTT/INTT baseline
// (docs/ROADMAP.md Phase 1: "one modular multiplier with a straightforward, documented reduction
// method" -- this is that method: a plain constant-modulus reduction, not Barrett/Montgomery,
// which are Phase 5 optimisations, docs/ROADMAP.md Phase 5).
//
// Locked FIPS 203 parameters (tb/golden/params.py, checked by
// .claude/skills/mlkem-guard/scripts/check_params.py): Q=3329, N=256. Never change these.

package ntt_pkg;

  localparam int unsigned Q       = 3329;   // FIPS 203 Section 2.3
  localparam int unsigned N       = 256;    // FIPS 203 Section 2.3
  localparam int unsigned INV128  = 3303;   // 128^-1 mod q (FIPS 203 Algorithm 10, line 14)
  localparam int unsigned CW      = 12;     // coefficient width: ceil(log2(Q)) = 12 bits
  localparam int unsigned AW      = 8;      // address width: log2(N) = 8 bits
  localparam int unsigned ZW      = 7;      // twiddle-ROM address width: log2(128) = 7 bits

  // add_mod / sub_mod: straightforward reduction, documented per docs/ROADMAP.md Phase 1 scope.
  // Inputs are assumed already < Q (the invariant every module below maintains and that CRG-7's
  // "reduction output always < q" assertion checks in simulation). Internal arithmetic is done
  // at 32 bits (matching Q's natural `int` width) with explicit casts so Verilator's -Wall width
  // checks (WIDTHEXPAND/WIDTHTRUNC) see one intentional final narrowing, not an implicit one.
  function automatic logic [CW-1:0] add_mod(input logic [CW-1:0] a, input logic [CW-1:0] b);
    logic [31:0] s;
    begin
      s = 32'(a) + 32'(b);
      add_mod = (s >= Q) ? CW'(s - Q) : CW'(s);
    end
  endfunction

  function automatic logic [CW-1:0] sub_mod(input logic [CW-1:0] a, input logic [CW-1:0] b);
    // (a - b) mod Q, computed as (a + Q - b) mod Q to stay in unsigned arithmetic.
    logic [31:0] s;
    begin
      s = 32'(a) + Q - 32'(b);
      sub_mod = (s >= Q) ? CW'(s - Q) : CW'(s);
    end
  endfunction

endpackage
`default_nettype wire
