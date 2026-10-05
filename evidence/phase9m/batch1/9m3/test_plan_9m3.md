<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Phase 9M item 3 (9M-3): the K0 sponge for the hash instance - test plan and adoption rule

Written 2026-10-04 before any 9M-3 measurement. Scope: ADR 0034 (Accepted, Faza Dzil), item 3 ("lanjut", chat 2026-10-04). Labels: MEASURED, ESTIMATE, INFERENCE, perhitungan tim. The mathematics is locked (C1): K0 and C5 compute the same Keccak-f[1600] and the same sponge; only rounds per cycle differ.

## 1. What this item is
The hash instance of the core (`mlkem_hash`, G, H, J) can use the C5 sponge (two rounds per cycle, 12 busy cycles, ADR 0027) or the K0 sponge (one round per cycle, 24 busy cycles, Phase 7). The core already has the parameter `HASH_C5` (default 1) and `mlkem_hash` the parameter `CORE_R2`; K0 files are already in every file list. **No RTL file changes in this item.** It measures `HASH_C5 = 0`, which Phase 9 kept open for the team (ADR 0033, 9b: K0 hash instance 4,221 ALM against 6,712-6,745 ALM for the C5 wrapper). The sampler inside the K-PKE engine keeps its own C5 sponge; this parameter does not touch it.
Base of the measurement: the 9M-1 core (`CODEC_W2 = 1`), revision MK = MW with `HASH_C5 = 0`. Choice stated here: the comparison that decides is MK against MW (identical except the sponge); the Phase 9 default core with K0 (`CODEC_W2 = 0`, `HASH_C5 = 0`) is **not** measured (INFERENCE: the effect of the two parameters is additive, not tested).

## 2. Estimates written before measuring (ESTIMATE, from 9b: cycles per hash, G33 30 -> 42, G64 33 -> 45, H1184 282 -> 390, J1120 274 -> 382; sampler engine unchanged)
| Quantity | MW (`CODEC_W2 = 1`, C5) MEASURED | MK ESTIMATE |
|---|---|---|
| KeyGen cycles (G33 + H(ek)) | 8,327 | about 8,447 (+120) |
| Encaps cycles (H(ek) + G64) | 10,159 | about 10,279 (+120) |
| Decaps cycles (G64 + J) | 15,515 | about 15,635 (+120) |
| ALM median, seeds 1-6 | 17,654.0 | 2,000 to 2,800 fewer (the 9b difference of the hash instance is about 2,500) |
| Registers | 8,189-8,376 | about 300 to 700 fewer |
| RAM blocks / DSP | 54 / 28 | 54 / 28 |
| Fmax lowest slow corner, median | 48.855 MHz | 47-53 MHz (the critical path is elsewhere: INFERENCE) |
| Timing at 40.000 ns | met at every seed | met at every seed |

## 3. Tests (both simulators; the repository RTL is never mutated)
| # | Test | Pass condition |
|---|---|---|
| V1 | lint Verilator `-Wall` and slang of the core with `HASH_C5 = 0`, `CODEC_W2 = 1` | 0 warnings, 0 errors |
| V2 | core with `HASH_C5 = 0`, `CODEC_W2 = 1`: the whole Phase 9c `core` target (ACVP keyGen 25, encapsulation 25, decapsulation 10; random cross-check; chain; protocol; constant cycles), env `CORE_K0=1 CORE_W2=1` | 100 % equal, both simulators |
| V3 | profile with `HASH_C5 = 0`, `CODEC_W2 = 1` (same inputs as `../../profile.md`) | recorded; the HFD / HGT states take the extra cycles; every other state count equal to MW |
| V4 | control that the K0 path is really in use and tested: `nclen` (every hash one byte short) with `CORE_K0=1 CORE_W2=1` | `test_acvp_encaps` fails, both simulators |
| V5 | formal: the hash wrapper proof of 9b (H1-H5) for `CORE_R2 = 0` with a protocol stub of `keccak_sponge` (the 9b stub under the K0 name, same ports); the 9c controller proof is independent of the hash parameter (the hash is a stub there) | PASS, as 9b; INFERENCE stated: that the real K0 sponge follows the stub's protocol is shown by the simulations of V2 and by the Phase 7 proofs |
| V6 | regression: the default core is not changed (no RTL file changed); `tb/mlkem/run_core_tests.py verilator core` at the default | 6/6 and the default profile equals the Phase 9 profile |
| V7 | Quartus: revision MK seeds 1-6 at 40.000 ns and MK-20 (seed 1, 20.000 ns, information), one at a time, kernel-only | extracts; timing met or the failure documented |

## 4. Parameters reported
ALM (median, min-max, % of the fitter's denominator), registers, RAM blocks, block memory bits, DSP, worst setup and hold slack, timing met per seed, Fmax lowest slow corner (median, min-max); cycles per operation (profile inputs and ACVP ranges) and per micro-operation; latency t = cycles / median Fmax (perhitungan tim); ACVP counts; constant-cycle results; formal results; critical warnings.

## 5. Adoption rule (fixed before measuring; not changed afterwards)
K0 is **adopted** as the hash sponge of the core (as the smaller option) only if all hold:
1. V1-V6 pass as stated (any ACVP mismatch rejects it).
2. Timing met at 40.000 ns at every seed 1-6.
3. The ALM median of MK is at least 1,500 below that of MW (17,654.0).
4. For each of KeyGen, Encaps and Decaps (profile inputs), t = cycles / median Fmax of MK is at most 2 % above that of MW (cycles of the profile of MW / 48.855 MHz).
Otherwise C5 stays. The result is recorded as a Proposed ADR; the choice between the smaller K0 and the C5 default (ADR 0027) stays with the team (ADR 0033 lists it). This rule decides only whether the numbers justify K0; it does not change ADR 0027.

## 6. Not in this item
No RTL change; no board result; no speed claim against software; constant time means cycle-count invariance only.
