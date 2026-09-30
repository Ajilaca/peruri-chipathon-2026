`default_nettype none
`timescale 1ns/1ps
// formal/phase03-multilane/modmul_reduce_uf.sv
// FORMAL-ONLY stand-in for rtl/ntt/modmul_reduce.sv (same module name and ports), used only by
// k1_butterfly_equiv_abs.sby. The product is an unconstrained value (anyseq); the miter adds the only
// fact kept about it: equal inputs give equal outputs (Ackermann / functional consistency). Sound
// because modmul_reduce.sv is a pure combinational function of (a_i, b_i): an equivalence proven for
// every consistent function also holds for (a_i * b_i) mod q. Never used in simulation or in Quartus.

module modmul_reduce (
    input  wire  [11:0] a_i,
    input  wire  [11:0] b_i,
    output logic [11:0] p_o
);
  (* anyseq *) logic [11:0] uf_p;
  assign p_o = uf_p;
endmodule
`default_nettype wire
