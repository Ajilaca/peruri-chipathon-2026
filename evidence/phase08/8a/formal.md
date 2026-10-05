<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Phase 8a formal run (test plan V8), 2026-10-03

Command: `. scripts/env.sh && python3 formal/run/run_formal_phase8a.py` (SymbiYosys, yosys-slang, smtbmc boolector). Properties K1-K5 of `formal/phase08-keccak-stream/keccak_sponge_r2_formal_top.sv` on `rtl/keccak/keccak_sponge_r2.sv` with
`keccak_f1600_r2.sv`, all inputs free, induction depth 30; K1 is "busy_o exactly 12 cycles, counter 0..11". Control properties only. Label: MEASURED (formal tool output of this run).

| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |
|---|---|---|---|---|---|---|
| A Phase 8a | keccak_sponge_r2 + keccak_f1600_r2 (K1, K2, K3, K4, K5) | PASS | PASS | basecase=pass, induction=pass | 81.6 | yes |
| B Negative control | NC-K1: 11 cycles per permutation (K1 busy length) | FAIL | FAIL | basecase=FAIL; failed assert keccak_sponge_r2_formal_top.sv:105 | 35.4 | yes |
| B Negative control | NC-K4: output data depends on out_ready_i (K4 hold; BMC depth 40: the squeeze phase is reached after about 30 cycles) | FAIL | FAIL | bmc=FAIL; failed assert keccak_sponge_r2_formal_top.sv:122 | 31.1 | yes |

ALL AS EXPECTED

Reading: the proof passes by induction (base case and step); NC-K1 (11 cycles) and NC-K4 (data depends on `out_ready_i`) fail as required. The runner text of NC-K4 says "the squeeze phase is reached after about 30 cycles", copied from
Phase 7; with 14 cycles per permutation the squeeze phase is reached after about 18 cycles (1 start, 1 absorb, 1 padding, 14 permutation, 1 squeeze); BMC depth 40 still covers it, the result is unchanged.
