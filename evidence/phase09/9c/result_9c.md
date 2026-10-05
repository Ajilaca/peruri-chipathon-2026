<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Phase 9c block report: the ML-KEM-768 core (`mlkem_core`)

- Status: **DONE** (STOP after the block, ADR 0032). A block checkpoint; the phase result is `docs/results/phase09.md`, whose Approval box is the team's.
- Date (UTC): 2026-10-03 / 2026-10-04. The work is in the working tree and not committed (chat 2026-10-03: commits are made when the work is finished).
- Plan and rule: `test_plan_9c.md` (written before the RTL; Amendment A1 records the findings below), `../phase9_plan.md`. Simulation results are not board results.

## 1. Result
`rtl/mlkem/mlkem_core.sv` runs KeyGen_internal, Encaps_internal and Decaps_internal of FIPS 203 (Algorithms 16-18) from a straight-line micro-program (`mlkem_ctl_rom.sv`, generated from the golden model `tb/golden/mlkem_ctl_model.py`) on byte buffers, a register file, the K-PKE engine of 8d (unchanged), the codec of 9a and the hash wrapper and comparison of 9b. **Every pinned ACVP vector of ML-KEM-768 passes on both simulators: keyGen 25 (ek and dk), encapsulation 25 (c and k), decapsulation 10 (k, including the modified ciphertexts that exercise implicit rejection).** The two key-check groups are not run against the RTL (ADR 0031: the input checks are on the HPS).

## 2. Verification (MEASURED, simulation; `verify.md`, `sim_verilator.md`, `sim_icarus.md`)
| Test | Result |
|---|---|
| V1 lint of the whole design (Verilator `-Wall`, slang) | 0 warnings, 0 errors |
| V2 ROM equals the generated ROM; static ROM checks; golden control model against ACVP (25 + 25 + 10) and the unmodified golden | 4 passed |
| V3 ACVP: keyGen 25, encapsulation 25, decapsulation 10 | 100 % equal, Icarus and Verilator |
| V4 random cross-check (20 cases of KeyGen, Encaps, Decaps with valid and one-bit-changed ciphertexts) and the chain KeyGen -> Encaps -> Decaps | all equal on both simulators |
| V5 protocol: start, op and host write while busy ignored, reset in the middle of a Decaps then a clean KeyGen, back to back with other keys, shared secret held after done | pass on both simulators |
| V6 constant cycles (Decaps: valid and rejected ciphertexts and different secret keys with the same ek; Encaps: different m with the same ek) | identical on both simulators |
| V7 negative controls (NC-CMP, NC-SEL, NC-LEN, NC-OFF, NC-ROM) | each fails the test named for it, both simulators |
| V10 regression: the 9a and 9b scripts; no file of the frozen blocks differs from main | PASS |

## 2b. Formal (MEASURED, SymbiYosys with boolector; `formal.md`, test plan Amendment A2)
| Run | Result |
|---|---|
| A safety: E1 non-interference of the control (two copies, different data, same handshakes), S1 ranges, S2 busy / done, S3 no host write while busy, S4 strobes, S5 engine ports, S6 addresses, S7 counters | PASS (base case and induction) |
| B controls NC-E1, NC-S3, NC-S4 on corrupted copies | each FAILS in the base case, as required |
| C cover, depth 260: KeyGen done, Encaps done, a digest word written | reached (the proof is not vacuous) |
Decaps done and the state S_CMPK need more than 260 steps (the hash feed takes 136-148 words); the separate deep run (depth 480, 28 minutes) reaches both (S_CMPK at step 266, Decaps done at step 272): `formal_deep_cover.md`.

## 3. Cycles (MEASURED, simulation, no host stalls)
Encaps 10,691 (constant for every m with the same ek), Decaps 16,623 (constant for valid and rejected ciphertexts and for different secret keys with the same ek), KeyGen 9,035-9,076 over the 25 ACVP seeds. The cycles depend on the public rho only (the rejection sampling of the matrix A inside the engine): over the 25 ACVP encapsulation keys Encaps takes 10,664-10,727 cycles, over the 10 ACVP decapsulation keys Decaps takes 16,601-16,663.

## 4. Quartus (MEASURED, kernel-only, virtual pins, 25.1std Lite; `selection_worksheet.md` and `quartus_MC*.md`)
- Seeds 1-6 at 40.000 ns: ALM 17,608-17,636 (median 17,620.5; 42 % of the 41,910 of the fitter), registers 8,210-8,365, 54 RAM blocks, 120,350 block memory bits, 28 DSP; **timing met at every seed** (worst setup 19.010 ns, worst hold 0.075 ns); Fmax lowest slow corner median 49.280 MHz (47.64-51.74).
- Information: MC-20 (20.000 ns, seed 1): timing met (worst setup 4.419 ns), Fmax 64.18 MHz, 17,650 ALM.
- Critical Warning 15725 (clock port fed by a virtual pin) in every compile, as in all earlier kernel-only compiles; nothing waived.

## 5. Findings and deviations (all in Amendment A1 of the test plan)
1. ESTIMATE misses: Encaps cycles estimated about 11,500 and measured 10,691; ALM estimated about 20,000 and measured 17,620.5 (the sum of the measured parts over-estimated the glue).
2. Setup mistakes of mine, not RTL defects: a missing import in the protocol test; wrong file paths in the first Quartus `.qsf` (the first runs failed in 45 seconds and none of their output is used).
3. Lint: two hidden names (renamed) and width fixes; the rename in the 9b comparison module was followed by a rerun of the 9b simulations and proofs (the 9b Quartus evidence was not recompiled for a renamed local parameter, which cannot change the logic: INFERENCE).
4. The controls use a reduced vector set to bound the run time (the `core` target runs the full set). The Icarus run of the whole set takes about an hour.

## 6. What this does not show
No board result, no HPS integration (Phase 10), no comparison with software and no speed-up or power claim. The formal proof of the core covers control and range properties only, with the sub-blocks replaced by protocol stubs (section 2b; values are covered by simulation against ACVP). The input checks of FIPS 203 are not in the RTL (ADR 0031). Constant-cycle is shown in simulation for fixed ek (the public rho decides the length of the matrix sampling); it is not a side-channel result.

## 7. Cost note (INFERENCE, perhitungan tim)
The encode and decode of the polynomials is serial and is not overlapped with the engine: a KeyGen spends about 2,300 cycles in the pack of t_hat and s_hat and a Decaps about 2,400 cycles in the loads; these are measured costs of the schedule, a possible later optimisation, and not part of this result.

## 8. Decision for the team
The Phase 9 result (`docs/results/phase09.md`) lists the open points: acceptance of the C7-core configuration as built (ADR 0033, Proposed), the choice of the hash sponge core (C5 default, K0 smaller) and the board question (PENDING #8). Nothing is decided here.
