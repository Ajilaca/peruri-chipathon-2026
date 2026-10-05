<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Phase 9b block report: hash wrapper (G, H, J) and the FO comparison / key selection

- Status: **DONE** (STOP after the block, ADR 0032). A block checkpoint, not the phase result; `docs/results/phase09.md` comes at the end of Phase 9 and its Approval box is the team's.
- Date (UTC): 2026-10-03. The work is in the working tree and not committed (chat 2026-10-03: commits are made when the work is finished).
- Plan and rule: `test_plan_9b.md` (written before the RTL; Amendment A1 records the findings below), `../phase9_plan.md` (Amendment A1: word interface, no byte feeder). Simulation and formal results are not board results.

## 1. Result
`rtl/mlkem/mlkem_hash.sv` (H = SHA3-256, G = SHA3-512, J = SHAKE256 with 32 bytes, on a 64-bit word stream; the SHAKE squeeze is stopped after 4 words; parameter `CORE_R2` selects the C5 sponge or the K0 sponge), `rtl/mlkem/mlkem_fo_cmp.sv` (constant-time comparison of two 136-word ciphertexts and the mask selection of K' or K_bar; no early exit, no branch on data) and the wrapper `rtl/mlkem/mlkem_hash_fo_top.sv`. Digests equal the unmodified golden `primitives.H/G/J` (hashlib); the comparison equals the hardware-form model `tb/golden/fo_model.py`, which equals the unmodified golden `ml_kem_decaps_internal` end to end.

## 2. Verification (MEASURED; `verify.md`, `formal.md`, `formal_vacuity_check.md`)
| Test | Result |
|---|---|
| V1 lint: Verilator `-Wall` (both sponge cores) and slang | 0 warnings, 0 errors |
| V2 golden FO model vs `ml_kem_decaps_internal` (every one of the 8,704 single-bit changes for the select; 40 random changes end to end) | 3 passed |
| V3, V4 hash, both sponge cores: the four lengths of Algorithms 16-18, 16 boundary lengths at the rates of all modes and random lengths, 9 back-pressure / gap mode pairs, start / sel / len while busy ignored, reset mid-run, J then H then G in a row | 6/6 per core on each simulator |
| V5 compare: equal and random pairs, every one of the 8,704 single-bit differences, first / last / all beats, special keys, start while busy, reset, result held after done | 5/5 on each simulator |
| V6 constant cycles (hash per operation; compare for equal, first-bit, last-bit, random and all-different inputs) | identical |
| V7 negative controls (NC-STOP, NC-LAST, NC-SEL, NC-MASK, NC-SWAP, NC-EARLY) | each fails the test named for it, on both simulators |
| V8 formal: hash wrapper H1-H5 (with the protocol stub of the sponge) and compare F1-F4; cover runs; controls | both proofs PASS; both cover runs reach every covered state; NC-H1, NC-H5, NC-F1, NC-F3, NC-F4 FAIL as required |
| V10 cycles, always-ready sink, no gaps | G of 33 bytes 30, G of 64 bytes 33, H of 1,184 bytes 282, J of 1,120 bytes 274 (C5); 42, 45, 390, 382 (K0); compare 137 |

## 3. Quartus (MEASURED, kernel-only, virtual pins, 25.1std Lite; `selection_worksheet.md`, `quartus_HF*.md`)
- Seeds 1-6 at 40.000 ns, C5 sponge: ALM 6,712-6,745 (median 6,734.5), registers 1,976, DSP 0, block memory 0 bits, **timing met at every seed** (worst setup 19.095 ns, worst hold 0.161 ns); Fmax lowest slow corner median 50.625 MHz (47.84-52.07).
- Information: HF-20 (20.000 ns): timing met (worst setup 3.843 ns), Fmax 61.89 MHz. HF-K0 (K0 sponge, 40.000 ns, seed 1): 4,221 ALM, 1,977 registers, timing met (worst setup 25.719 ns), Fmax 70.02 MHz.
- Critical Warning 15725 (clock port fed by a virtual pin) in every compile, as in all earlier kernel-only compiles; nothing waived.

## 4. Findings and deviations (all in Amendment A1 of the test plan)
1. **A vacuous proof, found by a cover check and discarded.** The first stub of the sponge for the formal proof had a free signal that the tool treated as a constant, so the proof returned PASS without ever reaching the squeeze. The stub was corrected, cover statements and cover-mode runs were added to the runner, and the proofs and controls were rerun. The other formal stubs of the repository that use free signals were checked: the 8c sampler stub's free signals are free (covers reached; the PWMS state itself is not reached at depth 140 or 20, a depth effect, so the 8c PWMS properties rest on the induction, not on a trace), and the Phase 3 stub is confirmed free by its own control (`formal_vacuity_check.md`). No Phase 6-8 result was changed by this.
2. The hash wrapper is proved with a protocol stub of the sponge because the real sponge made the induction too slow (stopped after 30 minutes at step 20); the sponge's own control is covered by Phase 8a formal and its digests by simulation against hashlib. The comparison module is proved as it is.
3. A control text (NC-EARLY) did not compile on Icarus (use before declaration): fixed; every reported run was made after the fix.
4. ESTIMATE check: the hash and compare cycles matched the ESTIMATE within a few cycles; the wrapper plus comparison add about 570 ALM to the C5 sponge (INFERENCE).

## 5. What this does not show
No board result. The block has no buffers and no message assembly (9c). The sponge control inside the wrapper proof is stubbed (item 2). The input checks are not in the RTL (ADR 0031). Values outside the stated lengths (messages above 65,535 bytes) are not covered. Cycle invariance is shown in simulation only.

## 6. Cost for the budget of 9c (ESTIMATE, perhitungan tim, from the MEASURED cycles above)
KeyGen hashes: G(d || 3) about 30 + H(ek) about 282 = about 312 cycles; Encaps: H(ek) about 282 + G about 33 = about 315; Decaps: G about 33 + J about 274 + compare 137 = about 444 cycles (plus the re-encryption of the K-PKE engine); all with word buffers that deliver one word per cycle. These are costs to be placed in the schedule of 9c and not results.

## 7. Decision for the team
Optional, not blocking: the hash instance can use the C5 sponge (default, ADR 0027: 6,745 ALM and 50.6 MHz median here) or the K0 sponge (4,221 ALM and 70.0 MHz at seed 1, 26 cycles per permutation instead of 14). The hashing time is a small part of the operation either way (the numbers in section 3 and 6); the saving of the K0 choice is about 2,500 ALM. Not decided here; say so if you want it as a PENDING item.
The next block is 9c (the controller and all ACVP groups); it starts when the team says so (ADR 0032).
