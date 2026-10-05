`default_nettype none
`timescale 1ns/1ps
// formal/phase01-ntt/ntt_core_props.sv
// FSM safety property for rtl/ntt/ntt_core.sv (CRG-8, docs/ROADMAP.md Phase 1).
// Uses plain immediate `assert()` (not SVA property/sequence syntax), the reliably supported
// subset of the oss-cad-suite Yosys build's `read -formal` SystemVerilog reader.
//
// Actual timing of ntt_core's FSM (confirmed by both this proof and the cocotb regression,
// evidence/phase01/cocotb_regression.txt): busy_o drops to 0 on the
// cycle the FSM ENTERS S_DONE; done_o is asserted one cycle later, when the FSM LEAVES S_DONE
// back to S_IDLE. So the safety property checked here is "exactly one cycle after busy_o drops,
// done_o is 1" -- not "done_o is already 1 the same cycle busy_o drops" (an earlier, incorrect
// version of this property was caught by SymbiYosys's k-induction step, not by simulation).
//
// Liveness ("done_o is eventually asserted") is NOT formally proven here: the real run is
// 897/1153 cycles, and a bounded model check to that depth is impractical for this phase. That
// the FSM does reach done_o is evidence from the cocotb regression (CRG-3/CRG-7), not from
// SymbiYosys.
//
// Address-range note: the internal butterfly addresses (j, jlen, scale_addr) are declared as
// 8-bit unsigned values (AW=8, matching N=256 exactly), so they cannot represent a value outside
// [0,255] by construction (verified by manual width/range analysis in rtl/ntt/ntt_core.sv's
// comments), not by a separate SymbiYosys proof.

module ntt_core_props (
    input wire clk_i,
    input wire rst_ni,
    input wire busy_o,
    input wire done_o
);

  logic was_busy;        // busy_o, delayed by 1 cycle
  logic busy_just_dropped; // was_busy && !busy_o, delayed by 1 more cycle
  logic [1:0] valid_cnt;   // counts up to 2 so the checks below only run once both regs are real

  always_ff @(posedge clk_i or negedge rst_ni) begin
    if (!rst_ni) begin
      was_busy          <= 1'b0;
      busy_just_dropped <= 1'b0;
      valid_cnt         <= 2'd0;
    end else begin
      was_busy          <= busy_o;
      busy_just_dropped <= was_busy && !busy_o;
      if (valid_cnt != 2'd2) valid_cnt <= valid_cnt + 2'd1;
    end
  end

`ifdef FORMAL
  always_ff @(posedge clk_i) begin
    if (rst_ni && valid_cnt == 2'd2) begin
      if (busy_just_dropped) begin
        assert (done_o);
      end
    end
  end
`endif

endmodule
`default_nettype wire
