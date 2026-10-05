<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Phase 5M, step S8: write-path register and one bubble per direction (P = 7 -> 8) — test plan and adoption rule

Written 2026-10-02, **after the S8 RTL was written and linted (Verilator `-Wall`, slang: 0 warnings) but before any S8 simulation and before any S8 Quartus
compile** (CRG-4: nothing below depends on an S8 measurement). Scope and rules: ADR 0017 (S8 = lever 4 of the decision package: P -> 8, one data-independent stall
per transform), ADR 0019 (amendment note 2: S7 and S8 are planned before Phase 7), ADR 0020, Amendment A1 of `test_plan.md` (the full Phase 0-5 regression runs
once, at S8, on the final tree). Base configuration: **S7** (`rtl/ntt/ntt_core_s7_p7.sv`, revision S7, seeds 1-6 in `s7/`). The base for S8 is S7 whatever its
rule result was: S8 is defined as lever 4 on top of the split read (ADR 0017 table); this follows the team's instruction of 2026-10-02 (chat: "kerjakan sesuai
dengan agenda hari ini ... S7-S8 selesai"). The S7 rule result stays on record unchanged. Labels: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED.

## 1. The change (one change)
- new core `rtl/ntt/ntt_core_s8.sv` (copy of `ntt_core_s7.sv`), parameter `WR_REG` (0 or 1), wrapper `rtl/ntt/ntt_core_s8_p8.sv` (`WR_REG = 1`, all other parameters as S7:
  ARB_REG bits 4, 11, 16, RD_SPLIT 1, MUL_REG bits 0, 1, 2). The memory file is **not** changed: `poly_mem_multiport_split.sv` is reused with `WR_DELAY = WrDly + WR_REG`.
- With `WR_REG = 1` the 16 butterfly outputs (8 lanes x 2 x 12 bit = 192 bits) are registered (`pipe_delay`) before the memory write data; the memory's write
  control (valid, bank, offset, slot) and the port-0 host/butterfly select are delayed by the same cycle; `Pipe = RdLat + WrDly + WR_REG = 8`; the host-write guard
  uses `WrEff = WrDly + WR_REG + RD_SPLIT = 5`.
- The address schedule needs a bubble at Pipe = 8 (`scripts/test/phase5_stall_cycles.py 8`, INFERENCE from the Phase 5 decision package, stall table): one cycle at NTT
  boundary 3 (between layers 3 and 4) and one at INTT boundary 2 (between layers 2 and 3); the INTT scaling-pass boundary of that table does not exist in M6/S7/S8.
  New state `S_STALL` (encoding 2): all requests off for one cycle, entered only when `layer_q` equals the fixed boundary of the current mode. The bubble position is a
  function of (mode, layer) only, never of data, so the cycle count is constant.
- **Existing files modified: none** (new files only; S7, M6, C4b-B and the frozen Phase 1-5 files stay as they are).

## 2. Corner cases (enumerated before the tests)
- The two boundaries that carry a bubble (NTT 3, INTT 2) and the tightest-slack addresses of every other boundary (`_tight_addresses`), with boundary-directed data.
- A host write followed immediately by start (guard `hw_q` with `WrEff = 5`), host reads during `S_STALL` (lane 0 read port is enabled in that state, never a write),
  start during drain, reset in the middle of a transform and in the bubble cycle (no write after reset), `bank_overflow_o` never raised (bubble cycle has one enabled port).
- Constant cycles: every input of the corner set and random vectors give the same count per direction; NTT and INTT counts equal.
- Negative controls: bubble removed (the hazard must show up), write control not delayed with the write data register (one cycle short).

## 3. Tests
| ID | Check | Tool | Required |
|---|---|---|---|
| V1 | Lint of the S8 core and wrapper | Verilator `-Wall`, slang | 0 warnings, 0 errors |
| V2 | Core vs golden: NTT, INTT (`intt()`), round trip, boundary-directed data, 512 INTT unit vectors, constant cycles, `bank_overflow_o`, hazard scoreboard (read issued while an earlier write is in flight; read and write of the same address in the same cycle) with `C3_RDLAT = 4`, `C3_RDPHYS = 3`, `C3_WRDLY = 4` | cocotb `tb/phase5m/test_ntt_core_s8.py` (copy of the S7 test; the scoreboard treats `S_STALL` as a non-request cycle), both simulators | all PASS; 0 scoreboard violations; cycles constant; **NTT = INTT = 122** |
| V3 | NC-B: S8 copy without the bubble (`Stall = 0` mutant) | cocotb | bit-exact NTT and INTT FAIL and the scoreboard trips |
| V4 | NC-W: S8 copy whose write control is NOT delayed by `WR_REG` (memory `WR_DELAY = WrDly`, data register kept) | cocotb | bit-exact NTT and INTT FAIL |
| V5 | Formal H, O, R, A, B, C on `ntt_core_s8_p8` (copy of the S7 formal top with Pipe = 8, RdLat 4, WrDly 4, WR_REG, and the bubble in the control model) with NC-O, NC-A | SymbiYosys | PASS; controls FAIL |
| V6 | Memory unit tests for the reused memory at `WR_DELAY = 4`, `RD_SPLIT = 1` (V2/V3 of S7 at the new delay) | cocotb `tb/phase5m/test_poly_mem_split.py` | all equal to the reference |
| V7 | Re-run of S6 and S7 verification on the final tree (M6 and S7 are not modified; this proves it) | `scripts/test/phase5m_verify.sh`, `scripts/test/phase5m_verify_s7.sh`, `formal/run/run_formal_phase5m.py`, `formal/run/run_formal_phase5m_s7.py` | OVERALL PASS |
| V8 | **Phase 0-5 regression, once, on the final tree** (Amendment A1): `scripts/test/phase5_regression.sh` and `scripts/test/phase5_verify.sh`, plus `git diff --name-status 288a78c HEAD` listing added versus modified files | scripts, saved with the git SHA | OVERALL PASS; modified existing files: none (or each listed) |
| V9 | Quartus revisions `S8` (seed 1) and `S8-s2` .. `S8-s6`, 40.000 ns, Quartus defaults, full compile from a clean db, one at a time | `quartus_sh --flow compile` | evidence files extracted from the repository root |
| V10 | One information compile `S8-20` at 20.000 ns (same RTL and seed 1; information only, not part of the rule) | `quartus_sh --flow compile` | evidence file; worst setup and Fmax recorded |

## 4. Adoption rule (fixed before measuring)
S8 (revision `S8`, seeds 1-6) is adopted as the final Phase 5M core only if **all** hold:
1. correct: V1-V8 PASS on both simulators where applicable; V3 and V4 fail as required;
2. cycles constant and exactly NTT 122 / INTT 122 (113 + 8 + 1 bubble; ESTIMATE until simulated);
3. NTT-core ALM <= 12,573 at every seed; timing met at 40.000 ns at every seed (worst setup >= 0, worst hold >= 0);
4. ADR 0012 against the previous step S7 at its median Fmax of seeds 1-6 (`F_S7`, recomputed from the S7 evidence files by `scripts/quartus/phase5m_select_s8.py`):
   with F = median over seeds 1-6 of the lowest slow-corner Fmax of S8, **t_NTT = 122 / F < 120 / F_S7 and t_INTT = 122 / F < 120 / F_S7, i.e. F > F_S7 x 122 / 120**
   (perhitungan tim). The script also prints the comparison with M6 and C4b-B for the record; the rule compares with S7 only.
Notes fixed now:
- No tolerance. A median above the threshold by less than the seed spread (about 0.7 MHz in S6; the S7 spread is measured) is a pass by the rule with that caveat; a miss
  is **not adopted by the rule** and is reported (C5: the team decides). If S8 is not adopted, S7 (or M6) stays the datapath for Phase 6 and Phase 7; the team's choice.
- If the simulation shows a different bubble count than 1 per direction, the plan's cycle numbers are corrected as MEASURED and condition 2 is evaluated on the measured
  constant; a data-dependent count fails condition 2.
- The deadline-driven rule of the project applies: the S8 verdict comes from one sweep; no extra seeds.

## 5. Expectation (ESTIMATE, written before measuring; only a compile can tell)
- Cycles +2 versus S7 (120 -> 122). If the write segment (MEASURED slack of C4b-B at 40 ns: write segment 17.1 ns, side path 12.1 ns) becomes the critical one after S7, one register
  stage may raise Fmax; if S7 already moved the critical path elsewhere, S8 can lose (cycles +1.7 %, ALM and registers up) with no Fmax gain.
- Registers about +192 (ESTIMATE, signal widths); ALM +0 to about 650 by the Phase 4 per-stage range; DSP unchanged at 16.
- Break-even: S8 needs a median Fmax at least 1.7 % above S7's.

## 6. Not covered
- Hardware (no board). Formal covers control and bank capacity, not data. Path analysis after S8 only if the team asks. Seeds beyond 1-6; constraints other than 40.000 ns
  (S8-20 is information).

## 7. Evidence layout
`evidence/phase05m/s8/` (verification logs, formal, Quartus extracts, selection worksheet, regression output, summary); ADR for S8 (Proposed);
`docs/results/phase05m.md` and the PDF report at the end of S8 (the phase result, Approval box left empty).
