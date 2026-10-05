<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Phase 5M, step S7: split the memory read path (P = 6 -> 7) - test plan and adoption rule

Written 2026-10-02, **before any S7 RTL and before any S7 measurement** (CRG-4). Scope and rules: ADR 0017, ADR 0019 (amendment note 2: S7 and S8 are
planned before Phase 7), ADR 0020 (M6 is the base). Base configuration: **M6** (`rtl/ntt/ntt_core_m6_p6.sv`: Barrett, INTT without the scaling pass,
P = 6, NTT = INTT = 119 cycles; MEASURED median Fmax of seeds 1-6 34.430 MHz, ALM 9,394-9,441, 16 DSP,
`evidence/phase05m/s6/selection_worksheet.md`). Labels: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED.

## 1. The change (one change)
The C4b-B / M6 critical path starts at the read stage of `rtl/mem/poly_mem_multiport_pipe.sv`: control registers (bank, offset, slot, after cut M) ->
per-bank read-address select among 16 ports -> storage read (32 words per bank, flip-flops) -> output select (bank, sub-port) among 16 read ports ->
`sub_mod` -> multiplier. MEASURED (C3-P6 baseline, the same memory): read-address decode and read mux 21.292 ns of 29.345 ns
(`evidence/phase05/baseline/c3p6_critical_path.md`); for C4b-B 21.03 ns + `sub_mod` 4.22 ns + DSP 3.59 ns
(`evidence/phase05/5c/precheck_critical_path.md`). S7 puts **one register stage in the middle of that read**:

- new module `rtl/mem/poly_mem_multiport_split.sv` (the frozen `poly_mem_multiport_pipe.sv` is not edited): same storage, bank map, slot rule and
  arbitration; parameter `RD_SPLIT` (0 or 1). With `RD_SPLIT = 1` the per-bank sub-port read data (8 banks x 2 sub-ports x 12 bit = 192 bits) and the output
  select (bank and sub-port per read port, 16 x 4 = 64 bits) are registered between the storage read and the output select (new registers: about 256
  bits, ESTIMATE from signal widths). `rdata_o` then appears `RdLat + RD_SPLIT` cycles after the request. The write control is delayed by one more cycle
  (`WR_DELAY + RD_SPLIT`) so that a write still lands after the data of its request has gone through the multiplier path; the physical read of storage
  stays at the arbitration-end cycle.
- new core `rtl/ntt/ntt_core_s7.sv` (copy of `ntt_core_m6.sv`; `RdLat` includes `RD_SPLIT`, so P = RdLat + WrDly = 7), wrapper `rtl/ntt/ntt_core_s7_p7.sv`
  (same cuts as M6: ARB_REG bits 4, 11, 16; MUL_REG bits 0, 1, 2; `RD_SPLIT = 1`).
- **Existing files modified: none** (all new files; M6, C4b-B and Phase 1-5 files stay as they are).
With `RD_SPLIT = 0` the new memory must behave exactly as the frozen one (test V3).

## 2. Corner cases (enumerated before the tests)
- Same-address read-after-write across layer boundaries (the tightest slack addresses of `tb/mem/bank_model.py`), for NTT and INTT; boundary-directed data of the Phase 4
  test.
- Back-to-back requests that hit the same bank (two sub-ports used, third = overflow flagged), disabled ports, requests with `wr_i = 0` (host reads), host
  write followed by start (the `hw_q` guard), host read-back latency now 4 cycles.
- Reset in the middle of a transform (no write after reset: control chain reset), start during drain.
- Maximum hazard: a read of an address whose write lands the same cycle (must not occur; scoreboard) and the negative control with a deeper write delay.

## 3. Tests
| ID | Check | Tool | Required |
|---|---|---|---|
| V1 | Lint | Verilator `-Wall`, slang, new memory, core, wrapper | 0 warnings, 0 errors |
| V2 | Memory unit test, `RD_SPLIT = 1`: random request streams (reads, writes, host accesses) against a Python reference of storage; read data at `RdLat + 1`, write landing time, `bank_overflow_o` | cocotb `tb/phase5m/test_poly_mem_split.py`, both simulators | all equal to the reference; overflow flagged only on a third port per bank |
| V3 | Differential test, `RD_SPLIT = 0`: the new memory equals the frozen `poly_mem_multiport_pipe.sv` cycle by cycle (all outputs) on the same random streams | cocotb | 0 differences |
| V4 | Core vs golden: NTT, INTT (against `intt()`), round trip, boundary-directed data, constant cycles, `bank_overflow_o`, hazard scoreboard, the 512 INTT unit vectors of S6 (V6 of the S6 plan) | cocotb, Phase 4 test adapted in `tb/phase5m/` (read latency 4, physical read latency 3 for the scoreboard), both simulators | all PASS; scoreboard 0 violations; cycles constant |
| V5 | Negative controls (test-only copies): NCD write control delayed by `WR_DELAY + RD_SPLIT - 1` (one cycle short, i.e. not delayed by `RD_SPLIT`) and NCS the output select (bank, sub-port) NOT delayed with the registered read data | cocotb | results must be WRONG and the scoreboard / bit-exact checks FAIL |
| V6 | Formal H, O, R, A, B, C of `ntt_core_s7_formal_top.sv` (a copy of the M6 top with delay model for P = 7, RdLat = 4) with NC-O and NC-A | SymbiYosys | PASS; controls FAIL |
| V7 | Phase 0-5 regression | **not run for S7**: Amendment A1 of `test_plan.md` (S7 modifies no existing file; S8 runs the regression once on the final tree) | - |
| V8 | Quartus revisions `S7` (seed 1) and `S7-s2` .. `S7-s6`, 40.000 ns, Quartus defaults, full compile from a clean db, one at a time | `quartus_sh --flow compile` | evidence files extracted from the repository root |

## 4. Adoption rule (fixed before measuring)
S7 (revision `S7`, seeds 1-6) is adopted as the base for S8 only if **all** hold:
1. correct: V1-V6 PASS on both simulators, the V5 negative controls fail as required;
2. cycles constant and exactly NTT 120 / INTT 120 (P = 7, no stall; NTT = 113 + 7, INTT = NTT; ESTIMATE until simulated);
3. NTT-core ALM <= 12,573 at every seed; timing met at 40.000 ns at every seed (worst setup >= 0, worst hold >= 0);
4. ADR 0012 against the previous step M6 at its median Fmax of seeds 1-6 (34.430 MHz, t_NTT = t_INTT = 119 / 34.430 = 3.456 us): with F = median over
   seeds 1-6 of the lowest slow-corner Fmax of S7, **t_NTT = 120 / F < 3.456 us and t_INTT = 120 / F < 3.456 us, i.e. F > 34.720 MHz** (perhitungan tim).
Notes fixed now:
- No tolerance is added. The S7 gain, if any, must exceed the seed spread to be visible (M6 seeds 32.35-35.04 MHz, C4b-B 33.46-34.84 MHz, INFERENCE); a median above
  34.720 MHz by less than the spread is still a pass by the rule but is reported with that caveat; a miss by less than the spread is **not adopted by the rule** and the
  team decides (C5), as for S6. The team's adoption of M6 despite a 0.25 % shortfall (ADR 0020) is not a precedent and changes no threshold.
- If a stall is needed (cycles not 120 / 120), S7 as defined fails condition 2 and is reported; S8's stall-based design would then be re-planned by the team.
- Time-box proposed (the team may change it): S7 verdict by Saturday 2026-10-03 evening, S8 by Monday 2026-10-05 noon; Phase 7 starts after S8's verdict or at that
  time, whichever comes first (ADR 0019).

## 5. Expectation (ESTIMATE, written before measuring; only a compile can tell)
- Cycles +1 (119 -> 120). The register is placed inside the 21 ns read segment; if the two halves are about equal, the read segment could shrink by up to
  roughly half (INFERENCE, not measured: the report lumps the read segment as one 21.292 ns delay). The next path classes (MEASURED slack, C4b-B at 40 ns: write
  segment 17.1 ns, side path 12.1 ns) bound the achievable gain: a worst path of about 25 ns would mean about 40 MHz.
- ALM: 0 to about 650 more (decision package, ESTIMATE; bound by the measured per-stage cost range of Phase 4), registers about +256. DSP unchanged at 16.
- The result may be a pass or a fail of condition 4: seed noise (about +-0.7 MHz) is comparable to a small gain.

## 6. Not covered
- Hardware (no board). Formal covers control and bank capacity, not data. No path analysis after S7 unless the team asks. Other constraints than 40.000 ns
  (the 20 ns information compile belongs to S8). The regression of Phases 0-5 (S8).

## 7. Evidence layout
`evidence/phase05m/s7/` (verification logs, formal, Quartus extracts, selection worksheet, summary); ADR for S7 (Proposed) with the result.

## Amendment A1 (2026-10-02, written before any S7 measurement)
Test V5 as first written listed two negative controls NCD and NCW; with `RD_SPLIT = 1` they are the same mutant (a write delay of `WR_DELAY + RD_SPLIT - 1` is
exactly "not delayed by `RD_SPLIT`"). NCW is replaced by NCS (output select not delayed together with the read data), a different, independent fault. Thresholds
and the adoption rule are unchanged. Formal V6 uses RdLat = 3 (physical read) for property C and P = 7 for property A.
