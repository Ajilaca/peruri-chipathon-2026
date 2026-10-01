`default_nettype none
`timescale 1ns/1ps
// rtl/arith/lazy_bfly_io.sv
// Phase 5c (ADR 0014, docs/evidence/phase05-arith/test_plan.md amendment A4): combinational input and output logic of
// the C4 butterfly with lazy INTT inputs. Kept in its own module so that the value bounds can be proven formally
// without the multiplier (formal/phase05-arith/lazy_bfly_io_bounds.sby).
//
// Input side (inputs a_i, b_i < q):
//   NTT  (mode 0): mul_o = b,          side_o = a                    (as butterfly_c4.sv)
//   INTT (mode 1): mul_o = b + q - a,  side_o = a + b                (exact sums, no reduction)
//                  mul_o in [1, 2q) is congruent to b - a, side_o in [0, 2q) to a + b
// Output side (side_d_i = side_o delayed, t_i = multiplier result < q):
//   NTT  (mode 0): a_o = add_mod(side, t), b_o = sub_mod(side, t)  (side < q in NTT mode)
//   INTT (mode 1): a_o = side >= q ? side - q : side, b_o = t
// So the butterfly computes exactly what butterfly_c4.sv computes; the conditional subtraction of the INTT input
// moves from the read segment to the write segment.

/* verilator lint_off IMPORTSTAR */
import ntt_pkg::*;
/* verilator lint_on IMPORTSTAR */

module lazy_bfly_io (
    input  wire           mode_i,     // 0 = forward (CT), 1 = inverse (GS)
    // input side
    input  wire  [CW-1:0] a_i,
    input  wire  [CW-1:0] b_i,
    output logic [CW:0]   mul_o,      // to the multiplier (13 bits)
    output logic [CW:0]   side_o,     // to the side delay line (13 bits)
    // output side
    input  wire  [CW:0]   side_d_i,   // side_o, delayed by the multiplier latency
    input  wire  [CW-1:0] t_i,        // multiplier result, < q
    output logic [CW-1:0] a_o,
    output logic [CW-1:0] b_o
);

  localparam logic [CW:0] Q13 = (CW + 1)'(Q);

  always_comb begin
    if (mode_i) begin
      mul_o  = ({1'b0, b_i} + Q13) - {1'b0, a_i};
      side_o = {1'b0, a_i} + {1'b0, b_i};
    end else begin
      mul_o  = {1'b0, b_i};
      side_o = {1'b0, a_i};
    end
  end

  // side_d_i < 2q, so the reduced value is < q and fits CW bits (bound proven in formal/phase05-arith/)
  logic [CW:0] side_red;
  assign side_red = (side_d_i >= Q13) ? (side_d_i - Q13) : side_d_i;
  logic unused_msb;
  assign unused_msb = side_red[CW];

  always_comb begin
    if (mode_i) begin
      a_o = side_red[CW-1:0];
      b_o = t_i;
    end else begin
      a_o = add_mod(side_d_i[CW-1:0], t_i);
      b_o = sub_mod(side_d_i[CW-1:0], t_i);
    end
  end

endmodule
`default_nettype wire
