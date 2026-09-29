`default_nettype none
`timescale 1ns/1ps
// formal/phase02-mem/bank_map_props.sv
// CRG-8: proves the own-pair conflict-freedom property directly on the GENERATED
// rtl/mem/bank_map_rom.sv ROM contents (NUM_BANKS=8, the hardest/most general case -- L=2,4 are
// coarser versions of the same construction, already exhaustively checked in Python), for every
// address and every layer's distinguishing bit position (1..7), independently of the Python
// golden model in tb/mem/bank_model.py (that check is Python-vs-Python; this one is
// Python-scheme-vs-actual-RTL-ROM).
//
// Property: for every addr in [0,255] and every d in [1,7], bank(addr) != bank(addr XOR 2^d).
// This is a purely combinational invariant (no clock needed for its own sake); wrapped in a
// clocked harness only because SymbiYosys's BMC flow expects one.

module bank_map_props (
    input wire        clk_i,
    input wire [7:0]  addr_i,
    input wire [2:0]  d_i        // bit position 1..7 (0 is never a valid layer-distinguishing bit)
);

  logic [7:0] addr_pair;
  assign addr_pair = addr_i ^ (8'd1 << d_i);

  logic [2:0] bank_a, bank_b;
  bank_map_rom #(.NUM_BANKS(8)) u_a (.addr_i(addr_i),    .bank_o(bank_a), .offset_o());
  bank_map_rom #(.NUM_BANKS(8)) u_b (.addr_i(addr_pair), .bank_o(bank_b), .offset_o());

`ifdef FORMAL
  always @(posedge clk_i) begin
    if (d_i >= 3'd1) begin  // d_i==0 is out of the property's domain (see module docstring)
      assert (bank_a != bank_b);
    end
  end
`endif

endmodule
`default_nettype wire
