<!-- claim-lint: skip-file (result artifact: internal status page, not proposal text) -->
# Result — Phase 9: full ML-KEM-768 in RTL, simulation (blocks 9a, 9b, 9c; configuration C7-core)

- Status: DONE (all three blocks built, verified and measured; the acceptance of ADR 0033 and the Approval box are the team's)
- Status note: ADR 0031 (Accepted, Jo 2026-10-03): the FIPS 203 input checks run on the HPS, not in the RTL, so the key-check ACVP groups are not run against the RTL. ADR 0032 (Accepted): one STOP per block. Chat 2026-10-03 (Jo): no commits while working, at least 20 commits at the end in the real order of work. **Every block has its test plan written before its RTL, and the pass rule was not changed after measuring** (Amendments A1 of 9a, 9b and 9c, A2 of 9c record what was found or added afterwards). The work is in the working tree; the commits are made after this result.
- Date (UTC): 2026-10-03 / 2026-10-04
- Git commit (HEAD when verified): see `git log main..phase9-mlkem-core` (the branch is created when the commits are made; until then the whole Phase 9 is uncommitted in the working tree on top of main 497482f)
- **Result:** `rtl/mlkem/mlkem_core.sv` runs KeyGen_internal, Encaps_internal and Decaps_internal of FIPS 203 (Algorithms 16-18) on byte buffers, with the Phase 8d K-PKE engine unchanged, a coefficient/byte codec (9a), the hash wrapper G / H / J and the constant-time comparison with mask select (9b), and a straight-line micro-program controller (9c). **Every pinned ACVP vector of ML-KEM-768 passes on both simulators: keyGen 25, encapsulation 25, decapsulation 10** (the modified-ciphertext cases included). Cycles are constant: Decaps 16,623 for valid and rejected ciphertexts and for different secret keys with the same ek; Encaps 10,691; KeyGen 9,035-9,076. Quartus kernel-only (seeds 1-6, 40 ns): 17,608-17,636 ALM (42 % of 41,910), 54 RAM blocks, 28 DSP, timing met at every seed, median Fmax 49.280 MHz. Formal proofs of the control of 9a, 9b and 9c with negative controls. Simulation only, no board (PENDING #8).
- Environment: Ubuntu 24.04.4 LTS, OSS CAD Suite 2026-09-23 (Verilator 5.053, Icarus 14.0 devel, slang, SymbiYosys with boolector), cocotb 2.1.0, Quartus Prime Lite 25.1std.0 Build 1129.
- Constraint: 40.000 ns (`C.sdc` style constraint of the new Quartus projects, identical to Phases 5-8); information compiles at 20.000 ns.

## 1. Done-criteria (Common RTL Gate, docs/ROADMAP.md), Phase 9
| # | Criterion | Evidence | Status |
|---|---|---|---|
| CRG-1 | Lint clean | `docs/evidence/phase09-integration/9a/verify_2026-10-03.md`, `docs/evidence/phase09-integration/9b/verify_2026-10-03.md`, `docs/evidence/phase09-integration/9c/verify_2026-10-03.md` (Verilator -Wall: 0 warnings; two hidden-name warnings of the first 9c lint were fixed by renaming) | PASS |
| CRG-2 | Elaboration clean (slang) | `docs/evidence/phase09-integration/9a/verify_2026-10-03.md`, `docs/evidence/phase09-integration/9b/verify_2026-10-03.md`, `docs/evidence/phase09-integration/9c/verify_2026-10-03.md` (slang: 0 errors, 0 warnings) | PASS |
| CRG-3 | Bit-exact vs golden, both simulators | 9a: pack and unpack against the golden primitives for d = 1, 4, 10, 12 and the Compress constants on all 3,329 inputs; 9b: G, H, J against hashlib and the comparison and mask select against the golden FO model; 9c: every pinned ACVP vector (keyGen 25, encapsulation 25, decapsulation 10) and the random cross-check: `docs/evidence/phase09-integration/9a/verify_2026-10-03.md`, `docs/evidence/phase09-integration/9b/verify_2026-10-03.md`, `docs/evidence/phase09-integration/9c/sim_verilator_2026-10-03.md`, `docs/evidence/phase09-integration/9c/sim_icarus_2026-10-03.md` | PASS |
| CRG-4 | Corner cases before tests | `docs/evidence/phase09-integration/9a/test_plan_9a.md`, `docs/evidence/phase09-integration/9b/test_plan_9b.md`, `docs/evidence/phase09-integration/9c/test_plan_9c.md`, `docs/evidence/phase09-integration/phase9_plan.md` (written before the RTL of each block; the amendments record changes after the first runs) | PASS |
| CRG-5 | Regression: earlier phases still pass | `docs/evidence/phase09-integration/9c/verify_2026-10-03.md` (reruns 9a and 9b on both simulators and formal; 0 files of the frozen Phase 6-8 blocks differ from main), `docs/evidence/phase09-integration/9c/regression_phase8_2026-10-04.md` (Phase 8 engine tests rerun) | PASS |
| CRG-6 | Locked parameters | `.claude/skills/mlkem-guard/scripts/check_params.py` (run in this phase, output below in the verification of this result); no constant of FIPS 203 changed; Compress, Decompress and ByteEncode follow FIPS 203 Algorithms 5, 6 and 4.7 and are exact against the unmodified golden on all inputs | PASS |
| CRG-7 | Constant-cycle evidence | `docs/evidence/phase09-integration/9c/cycles_verilator_core_2026-10-03.json`, `docs/evidence/phase09-integration/9c/cycles_icarus_core_2026-10-03.json`, `docs/evidence/phase09-integration/9c/sim_verilator_2026-10-03.md`: Decaps identical for valid and rejected ciphertexts and for different secret keys with the same ek; Encaps identical for different m; 9a and 9b cycle tables in `docs/evidence/phase09-integration/9a/cycles_verilator_pack_2026-10-03.json` and `docs/evidence/phase09-integration/9b/cycles_verilator_fo_2026-10-03.json` | PASS |
| CRG-8 | Formal properties | `docs/evidence/phase09-integration/9a/formal_2026-10-03.md`, `docs/evidence/phase09-integration/9b/formal_2026-10-03.md`, `docs/evidence/phase09-integration/9b/formal_vacuity_check_2026-10-03.md`, `docs/evidence/phase09-integration/9c/formal_2026-10-04.md` (every proof as expected, every negative control fails as required; the controller is proved with protocol stubs) | PASS |
| CRG-9 | Quartus evidence; no negative slack or the failure documented | `docs/evidence/phase09-integration/9a/selection_worksheet_2026-10-03.md`, `docs/evidence/phase09-integration/9b/selection_worksheet_2026-10-03.md`, `docs/evidence/phase09-integration/9c/selection_worksheet_2026-10-03.md` and the Quartus extracts next to them (for example `docs/evidence/phase09-integration/9c/quartus_MC-20261003.md`): seeds 1-6 at 40 ns timing met for CD, HF and MC, plus 20 ns information compiles | PASS |
| CRG-10 | Result artifact + claim checker | `cmd: python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/result_phase9.md` and `cmd: python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal` | PASS |

## 1b. Phase 9 PASS criteria (docs/ROADMAP.md Phase 9, item 5) and blocks
| # | Criterion | Evidence | Status |
|---|---|---|---|
| P9-1 | 100 % of the applicable vectors pass on both simulators (keyGen 25, encapsulation 25, decapsulation 10; the key-check groups are on the HPS by ADR 0031) | `docs/evidence/phase09-integration/9c/sim_verilator_2026-10-03.md`, `docs/evidence/phase09-integration/9c/sim_icarus_2026-10-03.md`, `docs/decisions/0031-phase-9-fips-203-input-checks-are-done-by-the-hps-not-in-the.md` | PASS |
| P9-2 | Constant-cycle evidence for Decaps (valid and rejected ciphertexts, different secret keys, fixed public inputs) | `docs/evidence/phase09-integration/9c/cycles_verilator_core_2026-10-03.json`, `docs/evidence/phase09-integration/9c/cycles_icarus_core_2026-10-03.json` | PASS |
| P9-3 | Quartus evidence for the full core | `docs/evidence/phase09-integration/9c/selection_worksheet_2026-10-03.md`, `docs/evidence/phase09-integration/9c/quartus_MC-20261003.md` | PASS |
| P9-4 | C7-core row of the ROADMAP filled | `docs/ROADMAP.md` (rows C7a, C7b, C7-core), `docs/decisions/0033-phase-9-c7-core-as-built-ml-kem-768-in-simulation-acvp-100-p.md` | PASS |
| 9a | Codec (pack and unpack), exact, formal, Quartus | `docs/evidence/phase09-integration/9a/result_9a.md` | PASS |
| 9b | Hash wrapper and FO comparison, exact, formal, Quartus | `docs/evidence/phase09-integration/9b/result_9b.md` | PASS |
| 9c | ML-KEM core controller, ACVP 100 %, formal, Quartus | `docs/evidence/phase09-integration/9c/result_9c.md` | PASS |

## 2. What was produced
| Path | Purpose |
|---|---|
| `rtl/mlkem/mlkem_pack.sv`, `mlkem_unpack.sv`, `mlkem_codec_top.sv` | 9a: Compress_d + ByteEncode_d and ByteDecode_d + Decompress_d, d in {1, 4, 10, 12}, division-free |
| `rtl/mlkem/mlkem_hash.sv`, `mlkem_fo_cmp.sv`, `mlkem_hash_fo_top.sv` | 9b: G, H, J on the sponge (C5 default, `CORE_R2`), constant-time 1,088-byte comparison and mask select of K / K_bar |
| `rtl/mlkem/mlkem_core.sv`, `mlkem_ctl_rom.sv` (generated), `mlkem_ram.sv`, `mlkem_fifo4.sv`, `mlkem_wordbytes.sv`, `mlkem_bytedst.sv`, `mlkem_ldpoly.sv`, `mlkem_stpoly.sv` | 9c: the controller with its 40-bit micro-program, key buffers, byte / word converters, polynomial load and store tasks; the 8d engine is instantiated unchanged |
| `tb/golden/codec_model.py`, `fo_model.py`, `mlkem_ctl_model.py` and their tests | golden models first (codec, comparison, controller programs with a static checker) |
| `tb/mlkem/` | cocotb tests and runners on both simulators with negative controls (pack, unpack, hash, FO comparison, core) |
| `formal/phase09-integration/9a`, `9b`, `9c`, `formal/run_formal_phase9a.py`, `9b.py`, `9c.py` | SymbiYosys proofs, covers and negative controls |
| `quartus/phase09a_codec/`, `phase09b_hashfo/`, `phase09c_core/` | Quartus revisions (kernel-only, virtual pins), seeds 1-6 and 20 ns |
| `scripts/phase9a_verify.sh`, `phase9b_verify.sh`, `phase9c_verify.sh`, `select_9a.py`, `select_9b.py`, `select_9c.py`, `gen_mlkem_ctl_rom.py`, `build_phase9_report.py` | verification, rules from files, ROM generation, the PDF report |
| `docs/evidence/phase09-integration/` | phase plan, test plans, verification, simulation and formal logs, cycle tables, Quartus extracts, worksheets, block reports |
| `docs/decisions/0031` to `0033` | input checks on the HPS (Accepted), checkpoint protocol (Accepted), C7-core as built (Proposed) |
| `docs/report/CHIPATON_Phase9_Report.pdf` | the report (Bahasa Indonesia) |

## 3. Numbers (MEASURED: Quartus reports and simulation; latencies in microseconds are INFERENCE / perhitungan tim)
### 3a. 9a, codec (kernel-only)
| Quantity | Value | ESTIMATE written before measuring |
|---|---|---|
| ALM, median (min-max), seeds 1-6 | 299.0 (298-299) | not stated as a range |
| Registers / M10K / DSP | 192-193 / 0 / 2 | - |
| Timing at 40.000 ns | met at every seed | - |
| Fmax lowest slow corner, median (min-max) MHz | 105.630 (100.46-110.38) | - |
| Cycles per polynomial, pack d = 1 / 4 / 10 / 12 | 261 / 261 / 325 / 389 | d = 1 and 4: estimate missed (the unit is input-bound at 256 coefficients) |
| Cycles per polynomial, unpack d = 1 / 4 / 10 / 12 | 259 / 259 / 323 / 387 | same |
Information at 20.000 ns (seed 1): met, setup +10.952 ns. Sources: `docs/evidence/phase09-integration/9a/selection_worksheet_2026-10-03.md`, `cycles_*_2026-10-03.json`.

### 3b. 9b, hash wrapper and comparison (kernel-only, C5 sponge)
| Quantity | Value | Note |
|---|---|---|
| ALM, median (min-max), seeds 1-6 | 6,734.5 (6,712-6,745) | sponge C5 is 6,167 of them (Phase 8a) |
| Registers / M10K / DSP | 1,976 / 0 / 0 | - |
| Timing at 40.000 ns | met at every seed | - |
| Fmax lowest slow corner, median (min-max) MHz | 50.625 (47.84-52.07) | - |
| Cycles, C5: G (33 B) / G (64 B) / H (1,184 B) / J (1,120 B) / compare 1,088 B | 30 / 33 / 282 / 274 / 137 | - |
| Cycles, K0 sponge (information): G 33 / G 64 / H / J | 42 / 45 / 390 / 382 | K0 instance: 4,221 ALM, 70.02 MHz (seed 1, `HF-K0`) |
Information at 20.000 ns (seed 1): met, setup +3.843 ns. Sources: `docs/evidence/phase09-integration/9b/selection_worksheet_2026-10-03.md`, `cycles_*_2026-10-03.json`.

### 3c. 9c, the ML-KEM-768 core (kernel-only, `HF` hash with C5 sponge, engine 8d OVERLAP unchanged)
| Quantity | Value | ESTIMATE written before measuring |
|---|---|---|
| ALM, median (min-max), seeds 1-6 | 17,620.5 (17,608-17,636), 42 % of the fitter's 41,910 | about 20,000: **overestimate** (the sum of the measured parts) |
| Registers | 8,210-8,365 | - |
| RAM blocks / block memory bits / DSP | 54 / 120,350 / 28 | - |
| Timing at 40.000 ns | met at every seed (worst setup 19.010 ns, worst hold 0.075 ns) | - |
| Fmax lowest slow corner, median (min-max) MHz | 49.280 (47.64-51.74) | - |
| Cycles: Encaps (fixed ek) | 10,691 (ACVP ek range 10,664-10,727) | about 11,500: miss |
| Cycles: Decaps (fixed ek) | 16,623 (ACVP dk range 16,601-16,663) | - |
| Cycles: KeyGen over the 25 ACVP seeds | 9,035-9,076 | - |
| Latency at median Fmax (perhitungan tim; kernel-only static timing, not a board measurement) | KeyGen about 184 us, Encaps about 217 us, Decaps about 337 us | - |
Information at 20.000 ns (seed 1, MC-20): timing met (worst setup +4.419 ns), 64.18 MHz, 17,650 ALM; kernel-only static timing, not a system at 50 MHz.
ACVP: keyGen 25 (ek and dk), encapsulation 25 (c and k), decapsulation 10: 100 % on Icarus and on Verilator. Sims: the `core` target 6/6 and the five negative controls (NC-CMP, NC-SEL, NC-LEN, NC-OFF, NC-ROM) each fail the test named for them: 11/11 per simulator.
Sources: `docs/evidence/phase09-integration/9c/selection_worksheet_2026-10-03.md`, `quartus_MC*_20261003.md`, `sim_*_2026-10-03.md`, `cycles_*_core_2026-10-03.json`.

### 3d. Formal (MEASURED, control and range properties; values are covered by simulation)
| Block | Proof | Controls | Cover |
|---|---|---|---|
| 9a | P1-P5 (counts, held byte, idle, bit balance) PASS (base case and induction) | NC-P2, NC-U6 fail; NC-P1 and NC-U1 give UNKNOWN in the proof and FAIL in BMC at depth 300, as required (section 6) | reached |
| 9b | H1-H5 hash wrapper (with the sponge replaced by a protocol stub), F1-F4 comparison PASS | NC-H1, NC-H5, NC-F1, NC-F3, NC-F4 fail as required | reached; the stub proof was first vacuous and was corrected (section 6) |
| 9c | E1 non-interference of the controller, S1-S7 PASS (base case and induction) | NC-E1, NC-S3, NC-S4 fail as required | KeyGen done, Encaps done, digest word written reached at depth 260; Decaps done and S_CMPK reached in the deep run (depth 480, `9c/formal_deep_cover_2026-10-04.md`) |
Sources: `9a/formal_2026-10-03.md`, `9b/formal_2026-10-03.md`, `9b/formal_vacuity_check_2026-10-03.md`, `9c/formal_2026-10-04.md`, `9c/formal_deep_cover_2026-10-04.md` under `docs/evidence/phase09-integration/`.

## 4. Standards and sources pinned
FIPS 203 (ML-KEM) Algorithms 4-6 (ByteEncode, ByteDecode, Compress, Decompress) and Algorithms 16-18 (ML-KEM.KeyGen_internal, Encaps_internal, Decaps_internal); FIPS 202 as in Phase 7; the NIST ACVP ML-KEM-768 vectors pinned in `reference/kat_sources.md` (they are NIST sample sets from the ACVP server, not the full CAVP validation). No parameter or arithmetic of FIPS 203 changed (C1). The FIPS 203 input checks (Sections 7.2 and 7.3) are not in the RTL (ADR 0031).

## 5. Coverage and limits
- **Simulation, formal and static timing only.** No board; Fmax is kernel-only with virtual pins. "Timing met at 20 ns" is this flow's static timing, not a system at 50 MHz. No claim on speed against software, on power, or on side channels (C3). Nothing here is a hardware validation (C8).
- Constant-time here means the cycle count does not depend on a secret value, shown in simulation for fixed public inputs. The cycle count depends on the public ek or rho through the rejection sampling of the matrix A (Encaps 10,664-10,727 and Decaps 16,601-16,663 over the ACVP keys). It is not a side-channel result.
- Formal covers control and range properties with the sub-blocks replaced by protocol stubs (the K-PKE engine, the sponge, the hash wrapper, the loaders), not values; values are covered by simulation against the golden model, hashlib and ACVP. The deep cover (Decaps done, S_CMPK, depth 480) is a separate run, evidence in section 6.
- The ACVP vectors are the pinned sample set; the two key-check groups are not run against the RTL (ADR 0031, the HPS does the checks, not tested on a board).
- Randomness enters through ports (`d`, `z`, `m`); no random source in the RTL. Secret key material stays in registers and memories that are not wiped after an operation (no claim on this).
- The Icarus run of the whole ACVP set takes about an hour, so the negative controls use a reduced vector set; the `core` target runs the full set.
- The codec and the loads are serial and not overlapped with the engine (about 2,300 cycles in KeyGen, about 2,400 in Decaps): a measured cost of the schedule and a possible later optimisation, not a result.

## 6. Deviations, failures and open issues
- **A vacuous formal proof was found and discarded (9b):** the first proof of the hash wrapper with the protocol stub passed because a stub signal declared as `(* anyseq *) logic` and read only in procedural code is treated as a constant. The cover run showed it; the stub was changed to `(* anyseq *) wire`, the proof was rerun and the discarded result is documented in `docs/evidence/phase09-integration/9b/formal_vacuity_check_2026-10-03.md`. The other anyseq stubs of earlier phases were checked afterwards (8c stub free; Phase 3 `modmul_reduce_uf` free, shown by its own control); no Phase 3-8 result changed.
- **The 9b wrapper proof with the real sponge was too slow** (stopped after 30 minutes by its process id); the wrapper is proved with a protocol stub of the sponge and the sponge itself has its own proofs (Phase 7 and 8a). Values of the digests are covered by simulation against hashlib.
- **A formal proof of the core was not planned and was added** (Amendment A2 of the 9c test plan) after the verification runs because CRG-8 asks for it; the rule of the plan was not changed.
- **Formal controls of 9a (NC-P1 and NC-U1)** give UNKNOWN in the proof run (the violation lies beyond the induction depth) and FAIL in BMC at depth 300, as for NC-B of Phase 3; documented in Amendment A1 of the 9a plan.
- **Deep cover (depth 480) reached every covered state**, including Decaps done (step 272) and S_CMPK (step 266); it is a separate long run (28 minutes, `formal/run_formal_phase9c.py deep` equivalent, `formal/phase09-integration/9c/mlkem_core_cover_deep.sby`), evidence `docs/evidence/phase09-integration/9c/formal_deep_cover_2026-10-04.md`. At depth 260 only KeyGen done, Encaps done and a digest word were reached.
- **ESTIMATE misses:** pack and unpack cycles for d = 1 and 4 (input-bound); Encaps cycles about 11,500 estimated, 10,691 measured; core ALM about 20,000 estimated, 17,620.5 measured.
- **Process mistakes (mine, not RTL defects):** a missing import in the 9c protocol test; wrong file paths in the first Quartus `.qsf` of 9c (the first runs failed in 45 seconds and none of their output is used; all seven revisions were rerun); the first 9a driver never offered a 257th coefficient, so one control was void until the driver was fixed.
- **A renamed local parameter in `mlkem_fo_cmp.sv`** (lint hidden name) was followed by a rerun of the 9b simulations and proofs; the 9b Quartus extracts were not recompiled for it (INFERENCE: a rename cannot change the logic).
- Critical Warning 15725 (clock port fed by a virtual pin) in every kernel-only compile, as in earlier phases; nothing waived.
- Open: PENDING #8 (no board); the repository holds about 855 MB of untracked parallel Quartus copies under `quartus/par_a` to `par_d` that are never committed (to be moved to cloud storage by the team).

## 7. Decisions needed
- **ADR 0033** (C7-core as built; also: the hash sponge core of the wrapper, C5 default at 6,734.5 ALM against K0 at 4,221 ALM per hash instance, and whether to optimise the serial codec): Proposed; PENDING #33. The team accepts or rejects it.
- PENDING #8 (board): Phases 10 and 11 need a DE10-Nano.
- Proposal Section 3 (pages 4-6) is not written (C4); it is written only when the team asks.

## 8. Claims made in this phase
None written for judges or proposal text. The ROADMAP rows C7a, C7b and C7-core were filled from the evidence above. Any later claim must carry the label simulation only.

## 9. Reproduce
```bash
. scripts/env.sh
scripts/phase9a_verify.sh; scripts/phase9b_verify.sh; scripts/phase9c_verify.sh
python3 formal/run_formal_phase9a.py; python3 formal/run_formal_phase9b.py all; python3 formal/run_formal_phase9c.py all
cd quartus/phase09a_codec && ./run_cd.sh; cd ../phase09b_hashfo && ./run_hf.sh; cd ../phase09c_core && ./run_mc.sh; cd ../..
python3 scripts/select_9a.py; python3 scripts/select_9b.py; python3 scripts/select_9c.py
python3 scripts/gen_mlkem_ctl_rom.py --check
python3 scripts/build_phase9_report.py
python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/result_phase9.md
python3 .claude/skills/proposal-claims/scripts/claim_lint.py docs/results docs/proposal
```

## 10. Approval
- [ ] Human approver (name, date):
      Next phase starts only after a team member ticks this box. Claude never ticks it.
