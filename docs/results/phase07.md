<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Result - Phase 7: Keccak-f[1600] + SHA3/SHAKE baseline (configuration K0)

- Status: DONE
- Status note: Phase 7 PASS criteria met (all four modes bit-exact, fixed permutation latency shown, K0 row filled). The Approval box (Section 10) is empty. This is not tier T1 of ADR 0019: T1 also needs the samplers (Phase 8b), which are not built.
- Date (UTC): 2026-10-03
- Git commit (HEAD when verified): c69d62f (Phase 7 RTL, tests, formal, Quartus revisions and evidence), plus the documentation commit of this file
- Result: an iterative Keccak-f[1600] (one round per cycle, `busy_o` high for exactly 24 cycles for every state) and a sponge for SHA3-256, SHA3-512, SHAKE128 and SHAKE256 with multi-block absorb and squeeze, equal to hashlib for every tested length and output size on Verilator and Icarus, with data-independent cycle counts. Quartus (kernel-only, virtual pins): 3,572 ALM, 1,653 registers, 0 M10K, 0 DSP, timing met at 40 ns (setup +22.452 ns, Fmax 56.99 MHz, seed 1) and at 20 ns (setup +6.893 ns, Fmax 76.30 MHz, seed 1).
- Environment: Ubuntu 24.04.4 LTS, OSS CAD Suite 2026-09-23 (Verilator 5.053, Icarus 14.0 devel), cocotb 2.1.0, Quartus Prime Lite 25.1std.0 Build 1129.
- Constraint: 40.000 ns (`quartus/phase07_keccak/K.sdc`, identical to `quartus/phase06_sched/P.sdc`); information compile at 20.000 ns (`K-20.sdc`).

## 1. Done-criteria (Common RTL Gate, docs/ROADMAP.md)
| # | Criterion | Evidence | Status |
|---|---|---|---|
| CRG-1 | Lint clean | `evidence/phase07/verify.md` (Verilator -Wall: 0 warnings on keccak_f1600 and keccak_sponge) | PASS |
| CRG-2 | Elaboration clean (slang) | `evidence/phase07/verify.md` (slang: 0 errors, 0 warnings) | PASS |
| CRG-3 | Bit-exact vs golden, both simulators | `evidence/phase07/verify.md` (golden vs hashlib 16 pytest; permutation: every round of 1,802 states; sponge: all modes, boundary and ML-KEM lengths, back-pressure, stop, reset; Verilator and Icarus) | PASS |
| CRG-4 | Corner cases before tests | `evidence/phase07/test_plan.md` (written before the golden model and the RTL; Amendment A1 dated and explained, no threshold changed) | PASS |
| CRG-5 | Regression: earlier phases still pass | No existing RTL, test, proof, script or Quartus file was modified (`cmd: git diff --name-status b1b5789 HEAD -- rtl tb formal scripts quartus` lists additions only). The full earlier-phase regression is therefore not required (Phase 5M Amendment A1) | PASS |
| CRG-6 | Locked parameters | `evidence/phase07/verify.md` (`cmd: python3 .claude/skills/mlkem-guard/scripts/check_params.py`: all locked parameters match; constants package regenerated from the golden model, 0 differences); nothing of FIPS 203 or FIPS 202 changed | PASS |
| CRG-7 | Constant-cycle evidence | `evidence/phase07/keccak_cycles.md` (306 points, three messages each, one count per point; every point equals the FSM formula), `evidence/phase07/cycles_k0.json` | PASS |
| CRG-8 | Formal properties | `evidence/phase07/formal.md` (K1-K5 PASS by induction; NC-K1 and NC-K4 fail as required) | PASS |
| CRG-9 | Quartus evidence; no negative slack or the failure documented | `evidence/phase07/quartus_K0.md` (met at 40 ns), `evidence/phase07/quartus_K0-20.md` (met at 20 ns, information) | PASS |
| CRG-10 | Result artifact + claim checker | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase07.md` and `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

## 1b. Phase 7 PASS criteria (docs/ROADMAP.md Phase 7)
| # | Criterion | Evidence | Status |
|---|---|---|---|
| 1 | All modes bit-exact (SHA3-256 136 B, SHA3-512 72 B, SHAKE128 168 B, SHAKE256 136 B; lengths 0, rate -1, rate, rate +1, multiples, random; multi-block squeeze) | `evidence/phase07/verify.md` | PASS |
| 2 | Fixed permutation latency shown (24 cycles, independent of data); total cycles depend only on public lengths | `evidence/phase07/verify.md` (busy_o = 24 for all-zero, all-ones, 1,600 single-bit and 200 random states), `evidence/phase07/formal.md` (K1), `evidence/phase07/keccak_cycles.md` | PASS |
| 3 | K0 row filled (ALM, registers, Fmax, slack) | `docs/ROADMAP.md` (rows K0 and K0-20), `evidence/phase07/quartus_K0.md` | PASS |

## 2. What was produced
| Path | Purpose |
|---|---|
| `tb/golden/keccak.py`, `tb/golden/tests/test_keccak.py` | Golden Keccak-f[1600] (round constants and rho offsets computed from FIPS 202 Algorithms 2, 5, 6), sponge, four functions; proved equal to hashlib |
| `scripts/build/gen_keccak_consts.py`, `rtl/keccak/keccak_pkg.sv` | Generated round constants and rho offsets |
| `rtl/keccak/keccak_round.sv`, `keccak_f1600.sv`, `keccak_sponge.sv` | One combinational round; permutation core (24 busy cycles); sponge controller and Quartus top |
| `tb/keccak/` (`test_keccak_f1600.py`, `test_keccak_sponge.py`, `run_keccak_tests.py`) | cocotb tests, negative controls (NC-RC, NC-R, NC-PAD), runner for both simulators |
| `formal/phase07-keccak/`, `formal/run/run_formal_phase7.py` | Formal top (K1-K5), sby file, runner with NC-K1 and NC-K4 |
| `quartus/phase07_keccak/` | Revisions K0 (40 ns) and K0-20 (20 ns), constraints, run script |
| `scripts/test/phase7_verify.sh`, `scripts/test/phase7_op_cycles.py` | Verification script; Keccak cycles per ML-KEM operation (perhitungan tim) |
| `evidence/phase07/` | Test plan, verify, formal, cycle tables, Quartus extracts |
| `scripts/build/build_phase7_report.py`, `docs/reports/CHIPATON_Phase7_Report.pdf` | Report (Bahasa Indonesia, 4 pages); numbers parsed from the evidence files, cycle formula re-checked on all 306 points |

## 3. Numbers (MEASURED: Quartus reports and simulation; ESTIMATE and perhitungan tim marked)
| Quantity | K0 at 40.000 ns | K0-20 at 20.000 ns | Estimate written before measuring (ESTIMATE) |
|---|---|---|---|
| ALM (seed 1) | 3,572 / 41,910 (9 %) | 3,573 / 41,910 (9 %) | 1,500-3,500: measured is 2 % above the top of the range |
| Registers | 1,653 | 1,653 | 1,700-2,000: measured is below the range (1,600 state bits + 53 control; the estimate counted extra buffers that the design does not have) |
| M10K / DSP | 0 / 0 | 0 / 0 | about 0 / 0 |
| Timing | met; worst setup +22.452 ns (Slow 100 C), worst hold +0.163 ns (Fast -40 C) | met; worst setup +6.893 ns, worst hold +0.164 ns | not expected to limit the system (INFERENCE) |
| Fmax lowest slow corner (MHz) | 56.99 (seed 1) | 76.30 (seed 1) | - |
| Cycles per permutation | 24 busy (`keccak_f1600`), 26 as seen by the sponge | same | 24 |
| H(ek), 1184 B, 4 output words | 389 cycles | - | about 370 (superseded) |

Throughput at long lengths (perhitungan tim from the measured formula; absorb or squeeze of full blocks, no overlap): SHA3-256 and SHAKE256 17 words + 26 cycles = 43 cycles per 136 B (3.16 B per cycle); SHA3-512 35 cycles per 72 B (2.06); SHAKE128 squeeze 47 cycles per 168 B (3.57).
Time per permutation at the single-seed Fmax: 26 / 56.99 MHz = 0.456 us (K0), 26 / 76.30 MHz = 0.341 us (K0-20); these are one-seed values, not medians, and the 20 ns figure is not comparable with the 40 ns one.
Keccak cycles of one ML-KEM-768 operation with K0, each call run on its own and nothing overlapped (perhitungan tim, `evidence/phase07/keccak_cycles.md`): KeyGen about 2,026, Encaps about 2,078, Decaps about 2,070 (median over 200 random rho; ranges 2,013-2,088, 2,065-2,140, 2,057-2,132), 43-44 permutations.
That is about twice the pre-measurement figure of 1,060 (44 x 24), which omitted the control cycles and the word transfers. For scale: the Phase 6 arithmetic with S10 takes 5,475 / 6,789 / 3,109 cycles (MEASURED, simulation); the blocks are not connected yet.
Sources: `evidence/phase07/quartus_K0.md`, `quartus_K0-20.md`, `keccak_cycles.md`, `verify.md`.

## 4. Standards and sources pinned
FIPS 202 (Keccak-p[1600, 24], Algorithms 2, 5, 6 for the rho offsets and round constants, pad10*1, SHA3-256, SHA3-512, SHAKE128, SHAKE256, domain bytes 0x06 and 0x1F) as used by FIPS 203 (H, J, G, PRF, XOF); reference outputs from Python hashlib. No parameter or arithmetic of FIPS 203 changed (C1); `check_params.py` passes.

## 5. Coverage and limits
- Simulation, formal and static timing only. No board; Fmax and slack are kernel-only with virtual pins and one seed (ADR 0019: one compile for a block without an adoption rule). "Timing met at 20 ns" is this flow's static timing, not a system at 50 MHz.
- Formal covers control (K1-K5), not digest values; the digests are covered by simulation against hashlib.
- One round per cycle only (two rounds per cycle, unrolling, streaming samplers and the connection to the arithmetic unit are not allowed in this phase and were not built).
- Constant-time here means cycle counts depend only on the public length and the number of output words; it is not a side-channel statement.
- The K0 interface moves one 64-bit word per cycle and restarts for every call; 2,000 Keccak cycles per operation is a figure for that interface, not a bound for other designs.

## 6. Deviations, failures and open issues
- Test plan Amendment A1 lists them: the constants package name, 26 instead of 24 cycles per permutation in the cycle ESTIMATE, the extra state wipe, NC-K4 as BMC depth 40.
- First verification run: the sponge testbench had three mistakes (digest-end check lowered `out_ready_i` before the clock edge, a stop test asked SHA3 for one output word, the cycle log was overwritten by later builds); fixed in the testbenches, RTL unchanged by them. One RTL edit: an enum ternary rewritten as if/else because Icarus rejected it.
- The golden test first asserted 24 distinct round constants; the real table repeats two values (22 distinct); the assertion was corrected, the hashes were already equal to hashlib.
- ESTIMATE vs measurement: ALM 2 % above the written range, registers below it (Section 3).
- Critical Warning 15725 (virtual pin clock) in both compiles, as in earlier phases; Warning 10036 (`unused_ok` sink signal, deliberate, same device as `unused_widx` of Phase 6); no other critical warning; nothing waived.

## 7. Decisions needed
- Approval box of Phase 7 (Section 10).
- PENDING #26 (checkpoint protocol until 2026-10-08) is still open; this phase stopped at its end by the suggested default (one STOP per block).
- Next step per ADR 0019: the samplers (SampleNTT and CBD streaming from the Keccak output, tier T1) - order and scope are the team's choice; PENDING #25 (FIPS 203 input checks in hardware or on the HPS) before the controller work.

## 8. Claims made in this phase
None written for judges/proposal text. ROADMAP rows were filled from the evidence above.

## 9. Reproduce
```bash
. scripts/env.sh
scripts/test/phase7_verify.sh; python3 formal/run/run_formal_phase7.py
python3 scripts/build/gen_keccak_consts.py --check
cd quartus/phase07_keccak && ./run_k0.sh; cd ../..
python3 scripts/test/phase7_op_cycles.py 200
python3 scripts/build/build_phase7_report.py
python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase07.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 9b. Amendment note 1 (2026-10-03, after approval; nothing above is edited)
K0 seeds 2-6 were compiled as the baseline of the Phase 8a rule (`evidence/phase07/quartus_K0-s2.md` .. `quartus_K0-s6.md`). Over seeds 1-6: ALM 3,558-3,572, registers 1,653, Fmax lowest slow corner median 67.675 MHz (56.99-70.39), timing met at 40 ns at every seed. The 56.99 MHz of Section 3 is seed 1 and the lowest of the six; it should not be read as the typical value.

## 10. Approval
- [x] Human approver (name, date): Jose (Team J5), 2026-10-03
      Next phase starts only after a team member ticks this box. Claude never ticks it.
