<!-- claim-lint: skip-file (internal verification record, not proposal text) -->
# Phase 4 formal results (test plan V9, CRG-8) — C3, P = 2 / 4 / 6

- Generated: 2026-09-30 16:06 UTC. Command: `. scripts/env.sh && python3 formal/run/run_formal_phase4.py`
- Tools: SBY v0.69; Yosys 0.69+136 (git sha1 0fa1478ce-dirty, Release, Clang /us; yosys-slang frontend, `memory_map -rom-only`, smtbmc boolector; k-induction depth P + 3.
- Design under proof: the Quartus wrappers `rtl/ntt/ntt_core_c3_p2.sv`, `_p4.sv`, `_p6.sv` inside `formal/phase04-pipeline/ntt_core_c3_formal_top.sv`.
- **Scope: control and bank-capacity properties only.** Nothing here proves NTT/INTT arithmetic or memory data integrity; those rest on simulation (`cocotb_regression.txt`, `v2_modmul_staged_exhaustive.txt`).

## Properties
| | Property |
|---|---|
| H | `busy_o` drop is followed by `done_o` one cycle later (Phase 1 property module, reused) |
| O | `bank_overflow_o` == 0 |
| R | counter ranges: `t_q`, `layer_q`, `state_q`, `drain_q`, `hw_q` (asserted in `rtl/ntt/ntt_core_c3.sv` under `FORMAL`) |
| A | every memory write fires exactly P cycles after its request (write-valid bits == request's `en & wr` delayed P cycles in an independent delay model) |
| B | drained: in `S_DONE` no write requested in the last P cycles is outstanding and no write fires |
| C | no read and write of one storage location in the same cycle for transform traffic (`S_RUN` / `S_SCALE` requests) |

## Results
| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |
|---|---|---|---|---|---|---|
| A Phase 4 | C3 P=2 (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 6.8 | yes |
| A Phase 4 | C3 P=4 (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 8.2 | yes |
| A Phase 4 | C3 P=6 (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 12.7 | yes |
| B Negative control | NC-O P=2: bank_map_rom copy, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c3_formal_top.sv:144 | 7.5 | yes |
| B Negative control | NC-O P=6: bank_map_rom copy, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c3_formal_top.sv:144 | 11.7 | yes |
| B Negative control | NC-A P=2: delay model of property A one cycle short | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c3_formal_top.sv:145 | 8.5 | yes |
| B Negative control | NC-B P=2: drain one cycle short (induction must fail) | UNKNOWN | UNKNOWN | basecase=pass, induction=FAIL; failed assert ntt_core_c3_formal_top.sv:147 | 13.3 | yes |
| B Negative control | NC-B/bmc125 P=2: same mutant, BMC depth 125 (violation reachable) | FAIL | FAIL | bmc=FAIL; failed assert ntt_core_c3_formal_top.sv:147 | 2130.1 | yes |
| B Negative control | NC-C P=2: scaling pass may repeat an address (induction must fail) | UNKNOWN | UNKNOWN | basecase=pass, induction=FAIL; failed assert ntt_core_c3_formal_top.sv:150 | 18.5 | yes |

OVERALL: all results as expected (9/9)

## Reading the negative controls
All are run on corrupted copies under `formal/work/phase04/` (git-ignored); repository RTL is not modified.
- NC-O (one wrong bank in a copy of `bank_map_rom`) and NC-A (delay model one cycle short) fail in the base case, so
  properties O and A are not vacuous.
- NC-B (drain one cycle short) and NC-C (scaling pass may repeat an address) are violations that lie more than 100
  cycles from reset, beyond the base-case depth; the induction step fails, so the mutants are **not proven** (UNKNOWN,
  which is not the same as a demonstrated failure). For NC-B a bounded check of depth 125 reaches the violation and
  FAILS. NC-C's violation is in the INTT scaling pass, more than 112 cycles after a start; no deep bounded run was made for
  it, so for NC-C the evidence is only that the proof does not go through.
