# Roadmap — ML-KEM-768 accelerator on DE10-Nano

**Status line (update only from verified evidence):**
Phase 0 **completed and verified** (team-approved `docs/results/result_phase0.md`; evidence in
`docs/evidence/golden/`) · Phase 1 (C0 baseline) **PARTIAL, approved as a documented failing baseline (Faza Dzil, 2026-09-29)**: RTL, lint, both-simulator cocotb bit-exact, constant-cycle and formal safety pass; Quartus C0 compile MEASURED (7,010 ALM, 3104 registers, 0 RAM blocks, 3 DSP; Fmax 14.64 MHz; worst setup slack -48.323 ns at the provisional 20.000 ns clock -> **timing not met**; `docs/evidence/phase01-ntt-baseline/quartus_C0_timing_analysis_2026-09-29.md`). Target-clock ADR still missing · Phase 2 (C1 memory banking) **PARTIAL, approved as a documented failing baseline (Faza Dzil, 2026-09-29); started on top of an unapproved Phase 1 on explicit team instruction** (not per the strict gate below): conflict-free bank mapping proven (Python exhaustive + formal, all L∈{1,2,4,8}), RTL bit-exact and cycle-identical to C0 (0 stall), Quartus C1 MEASURED (6,749 ALM, 0 RAM blocks -- M10K goal NOT achieved, async-read limitation; Fmax 14.99 MHz; worst setup slack -46.720 ns -- still timing not met, same root cause as C0); `docs/evidence/phase02-memory/` · Phase 3 (C2 multi-lane) **PARTIAL, approved as a documented baseline with timing not met (Faza Dzil, 2026-09-30)**: RTL bit-exact + constant-cycle for L∈{1,2,4,8} (cocotb, both simulators, 16/16), ADR 0004 fixes the L-selection criterion (min cycle count within a 10,478 ALM / 25% budget) before the sweep was measured; Quartus C2-L1/L2/L4/L8 all MEASURED (6,018 / 5,728 / 7,629 / 11,446 ALM; L=8 **exceeds the ADR 0004 budget**; Fmax 14.76/13.54/11.60/7.62 MHz; all timing NOT met, worse than C0/C1 as L grows); cycles NTT/INTT 897/1153, 449/705, 225/481, 113/369 -- on C2 the ADR 0004 rule gives L = 4; supplementary experiments K2 (counter width) and K1 (one shared multiplier per butterfly, outside the written Phase 3 scope, team-approved) give the optimised **C2-K2-K1**, MEASURED 5,566 / 5,374 / 6,775 / 9,754 ALM with identical cycle counts, bit-exact on both simulators, butterfly equivalence proven (abstraction proof + exhaustive simulation); **selected operating point: C2-K2-K1 at L = 8 (ADR 0005, Accepted, Faza Dzil, 2026-09-30)**, `docs/evidence/phase03-multilane/k1_experiment_2026-09-30.md`; formal (SymbiYosys k-induction) PASSES for L=1/2/4/8 for bank_overflow_o==0, the busy/done handshake and the counter ranges (not bit-exactness); the earlier L=2/4/8 UNKNOWN was a formal-harness artefact (ROMs modelled as free memory state in the induction step), fixed in the harness only with negative controls, `docs/evidence/phase03-multilane/formal_rerun_2026-09-30.md` · tooling verified (Quartus 25.1std smoke
compile MEASURED, see `docs/TOOLING_INSTALL_LOG.md`) · no DE10-Nano attached at last check
(`jtagconfig` empty, 2026-09-24) · competition schedule unknown.

> If `docs/results/result_phase0.md` is missing, fails `check_result.py`, or has an unticked Approval box,
> the Phase 0 status above is wrong: stop, report it, and do not start Phase 1.

## How this roadmap works

- **Strict gates.** Phases run in order. A phase starts only after the previous phase's result artifact
  passes `check_result.py` **and** a team member has ticked its Approval box. Skill: `/phase-gate`.
- **Correct baseline first.** No optimisation phase starts until the configuration it modifies is
  bit-exact against the golden model and measured.
- **One major change at a time.** Phases with sub-steps (5, 6, 8) measure and record each sub-step on its
  own; a human reviews each sub-step checkpoint before the next one starts. Never combine two
  optimisations in one measurement.
- **Nothing invented.** Every resource, timing or performance number is `MEASURED` (Quartus report or
  simulation/board log in this repository, with its path) or labelled `ESTIMATE` with method and
  assumptions. Literature values are context only.
- **Failed gate = stop.** Do not proceed after a failed gate. Write the result artifact with Status
  `NOT DONE` or `PARTIAL`, record the failure and its log path, and ask the team. Do not weaken a test,
  tolerance, assertion or timing constraint to pass.
- **Every phase ends with a result artifact** `docs/results/result_phase<N>.md` (template
  `docs/results/TEMPLATE_result_phase.md`), validated by
  `python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/result_phase<N>.md`.
- Evidence for phase N lives in `docs/evidence/phaseNN-<topic>/` (Phase 0 keeps `docs/evidence/golden/`).
  Prompts per phase: `docs/prompts/phase<N>.md`; only `docs/prompts/phase0.md` exists so far.

## Locked FIPS 203 requirements (apply to every phase; never modified)

The mathematics is locked; only the hardware architecture changes (ADR 0002, `/mlkem-guard`).

| Requirement | Value / rule | Source |
|---|---|---|
| Ring | R_q = Z_q[X]/(X^256 + 1), q = 3329, n = 256 | FIPS 203; `/mlkem-guard` |
| ML-KEM-768 parameters | k = 3, η1 = 2, η2 = 2, du = 10, dv = 4 | FIPS 203 Table 2 (confirmed in Phase 0) |
| Sizes | ek 1184 B, dk 2400 B, ct 1088 B, shared key 32 B | FIPS 203; NIST ACVP vectors |
| NTT | ζ = 17; **incomplete** NTT: 7 layers (block lengths 128 → 2), 128 butterflies per layer | FIPS 203 Alg. 9/10 |
| Pointwise product | 128 base-case products of degree-1 polynomials modulo (X² − ζ^(2·BitRev7(i)+1)), not scalar products | FIPS 203 Alg. 11/12 |
| Hash / XOF | SHA3-256, SHA3-512, SHAKE128, SHAKE256 over Keccak-f[1600] | FIPS 203; FIPS 202 |
| Compress / Decompress, encode | exactly as defined in FIPS 203; no division on secret data | FIPS 203 |
| Input checks and implicit rejection | encapsulation-key and decapsulation-key checks; Decaps re-encrypts, compares in constant time and selects K or the implicit-rejection key | FIPS 203 |
| Correctness reference | Python golden model in `tb/golden/` (Phase 0), locked constants checked by `check_params.py` | Phase 0 |

## Common definitions

### Metrics tracked (per configuration)

| Metric | Definition | Source |
|---|---|---|
| ALM | Logic utilisation in ALMs | Fitter summary |
| Registers | Total registers | Fitter summary |
| M10K | Total RAM blocks | Fitter summary |
| DSP | Total DSP blocks | Fitter summary |
| Utilisation | Used / available, **with the denominators printed by the fitter** | Fitter summary |
| Fmax | Per clock, from the Timing Analyzer "Fmax Summary" (slow model) | STA report |
| Slack | Worst setup **and** hold slack, all corners, at the constrained clock | STA summary |
| Cycles/op | Clock cycles per operation from a cycle counter (simulation first, later on board) | Test logs |
| Stall cycles | Cycles lost to bank conflicts or pipeline hazards | Test logs |
| Latency | cycles ÷ f_clk, where f_clk is the **constrained clock that met timing** (not Fmax); state the clock with every latency | Derived from MEASURED values |
| Area-time (AT) | ALM × latency (report DSP and M10K alongside; they are not folded into AT) | Derived from MEASURED values |

Reference capacity of the target device 5CSEBA6U23I7, as printed by the fitter in the team's smoke compile
(MEASURED, `docs/TOOLING_INSTALL_LOG.md`): 41,910 ALMs, 553 RAM blocks (5,662,720 block-memory bits) and
112 DSP blocks. Always quote the denominators of the current fitter report.

Cycles/op has two scopes. **Kernel scope:** cycles per NTT, per INTT, per pointwise product (one
polynomial), per Keccak-f permutation. **Operation scope:** cycles per KeyGen, Encaps, Decaps. Compare
configurations only within the same scope.

### Measurement protocol (every Quartus measurement)

- Same Quartus version (25.1std unless an ADR changes it), same device, same timing-constraint method,
  fitter seed recorded. One Quartus revision per configuration; revision name = configuration ID from the
  ablation matrix.
- Kernel-only compiles use virtual pins so that I/O does not distort area or timing.
- Target clock: a team decision recorded as an ADR at the Phase 1 gate. Until then, constrain with a
  documented provisional period and report Fmax. Never state a latency without its clock.
- Extract evidence with the `/quartus-report` skill, writing into the phase folder:
  `extract_quartus_report.py <output_files> <revision> --log <compile.log> --out docs/evidence/phaseNN-<topic>/quartus_<revision>_<UTCdate>.md --note "<git sha, parameters, clock>"`.
  Raw `.rpt` files and `output_files/` are not committed.
- Critical warnings are triaged in writing in the result artifact.

### Common RTL gate (CRG) — required at every RTL phase

| ID | Check | Tool |
|---|---|---|
| CRG-1 | Lint clean | `verilator --lint-only -Wall` |
| CRG-2 | Elaboration clean | `slang` |
| CRG-3 | Bit-exact against the golden model, on **both** simulators | cocotb on Verilator **and** Icarus |
| CRG-4 | Corner cases listed in the test plan before tests are written (zeros, all coefficients q−1, impulses, maximum values, boundary lengths) | Test plan in the phase evidence folder |
| CRG-5 | Regression: all tests of every earlier phase still pass | pytest / cocotb |
| CRG-6 | Locked parameters | `check_params.py` |
| CRG-7 | Constant-cycle evidence where applicable: identical cycle count for different secret inputs with identical public inputs | Cycle-count log |
| CRG-8 | Formal properties for new control/address logic (FSM reaches done, no out-of-range address, and phase-specific properties) | SymbiYosys |
| CRG-9 | Quartus evidence where the phase requires it; no negative worst slack at the constrained clock, or the failure documented | `/quartus-report` |
| CRG-10 | Result artifact validated; text for judges passes the claim checker | `check_result.py`; `claim_lint.py` |

## Renumbering note (2026-09-29)

This revision replaces the earlier 0-6 phase list. Old → new: old 1 (NTT) → new 1-6; old 2 (Keccak) →
new 7-8; old 3 (integration) → new 9-10; old 4 (protocol demonstration) → new 10 (functional) and 11
(measured); old 5 (measurement) → new 11; old 6 (advanced) → new 12. Other files that still cite old
numbers must be updated separately (not part of this revision).

---

## Phase 0 — Golden model / FIPS 203 — **COMPLETED (verified, team-approved)**

1. **Goal.** An independent, trusted Python reference for ML-KEM-768 that every later gate compares against.
2. **Implementation scope (delivered).** `tb/golden/`: locked constants (`params.py`), primitives (NTT,
   INTT, pointwise, sampling, encode, compress), K-PKE and ML-KEM top level; FIPS 203 errata reviewed.
3. **Tests / verification (done).** Property tests; NIST ACVP ML-KEM-768 vectors (pinned commit and
   sha256 in `.claude/skills/mlkem-guard/reference/kat_sources.md`; NIST **sample** sets, 25 cases per
   group); random cross-check against kyber-py in a throwaway virtualenv.
4. **Quartus.** Not applicable.
5. **PASS criteria (met).** `check_params.py` passes and k/η/du/dv confirmed against FIPS 203; golden model
   reproduces the pinned vectors; errata recorded (evidence + ADR); cross-check log present;
   `result_phase0.md` validated and approved.
6. **Not allowed from now on.** Changing the golden model without an ADR and a full Phase 0 re-run;
   using old CRYSTALS-Kyber vectors; treating the sample vectors as exhaustive coverage.
7. **Evidence artifact.** `docs/evidence/golden/`, `docs/results/result_phase0.md`.
8. **Approval gate.** Approved (see the Approval box in `result_phase0.md`).

## Phase 1 — Minimal RTL baseline: L = 1 NTT/INTT + pointwise multiplication

1. **Goal.** The first correct, measured hardware reference for the arithmetic kernel (configuration
   **C0**). Every later optimisation is compared against it.
2. **Implementation scope.** `rtl/ntt/`: one butterfly unit (forward Cooley-Tukey and inverse
   Gentleman-Sande modes), one modular multiplier with a straightforward, documented reduction method,
   base-case multiplier in the direct 5-multiplication form, twiddle ROM **generated by a script from the
   golden model** (never hand-typed), INTT final scaling as specified in FIPS 203, a simple polynomial
   memory (no banking), start/done control, fixed schedule.
3. **Tests / verification.** CRG-1 to CRG-10. Bit-exact against `tb/golden` `ntt`, `intt` and the NTT-domain
   product for random polynomials and the corner cases; `intt(ntt(f)) = f`; reduction output always < q
   (assertion); formal: FSM completion, addresses in range.
4. **Quartus.** Kernel-only compile of C0: ALM, registers, M10K, DSP, Fmax, worst setup/hold slack, triaged
   warnings. Cycles per NTT, INTT and pointwise product from simulation.
5. **PASS criteria.** All CRG checks pass; cycle count identical across all tested inputs; one Quartus
   evidence file for C0; target-clock ADR recorded; C0 row of the ablation matrix filled with MEASURED values.
6. **Not allowed yet.** More than one lane; memory banking; pipelining beyond what correctness needs;
   q-specific reduction tricks, Montgomery-vs-Barrett comparison, lazy reduction, Karatsuba; Keccak; HPS
   integration; any performance or speed-up claim.
7. **Evidence artifact.** `docs/evidence/phase01-ntt-baseline/` (test plan, simulation and cycle logs for
   both simulators, lint/slang logs, formal logs, `quartus_C0_<date>.md`); `docs/results/result_phase1.md`.
8. **Approval gate.** A team member reviews and ticks Approval in `result_phase1.md` before Phase 2.

## Phase 2 — Memory architecture: M10K storage, banking, address generation

1. **Goal.** A polynomial memory and address generator that can feed L lanes without bank conflicts,
   measured at L = 1 so that only the memory change is visible (configuration **C1**).
2. **Implementation scope.** `rtl/mem/`: M10K polynomial storage with a documented packing (e.g. two
   coefficients per word) and several polynomials per bank; bank-mapping function parameterised for
   L ∈ {1, 2, 4, 8}; address generation for all 7 NTT layers, all 7 INTT layers and the pointwise product,
   with no separate bit-reversal pass; twiddle-ROM organisation per lane; ping-pong buffering only if a
   documented schedule requires it. Datapath stays at L = 1.
3. **Tests / verification.** CRG-1 to CRG-10. Phase 1 bit-exact regression; **conflict-freedom proof**: for
   every L ∈ {1, 2, 4, 8}, every layer and every cycle, no two accesses target the same bank port
   (formal property on the generator plus exhaustive enumeration in a Python model); no out-of-range
   address; stall cycles counted in simulation.
4. **Quartus.** C1 compile: same metrics as C0, with the change in M10K and ALM stated against C0.
5. **PASS criteria.** Conflict-freedom proven for all four L values; measured stall cycles = 0 at L = 1;
   bit-exact; constant cycle count; C1 row filled.
6. **Not allowed yet.** Activating more than one lane; pipeline changes; arithmetic changes; Keccak.
7. **Evidence artifact.** `docs/evidence/phase02-memory/` (bank-map specification, proof and enumeration
   logs, simulation logs, `quartus_C1_<date>.md`); `docs/results/result_phase2.md`.
8. **Approval gate.** Human approval in `result_phase2.md` before Phase 3.

## Phase 3 — Multi-lane exploration: L = 1 / 2 / 4 / 8

1. **Goal.** Measure the resource-versus-performance trade-off of parallel butterflies on the Phase 2
   memory, and let the team choose an operating point (configuration **C2**).
2. **Implementation scope.** Lane count as a parameter; butterfly, arithmetic and memory as in Phase 2.
   The selection criterion (for example, lowest AT within a stated resource budget) is written into an ADR
   **before** the sweep is measured.
3. **Tests / verification.** CRG-1 to CRG-10 for each L: bit-exact, constant cycle count, stall cycles = 0,
   cycles per NTT, INTT and pointwise product.
4. **Quartus.** One revision per L (`C2-L1`, `C2-L2`, `C2-L4`, `C2-L8`), identical constraints and seed.
5. **PASS criteria.** All four configurations correct; four Quartus evidence files; comparison table
   complete; ADR choosing L (or keeping L configurable) signed by the team.
6. **Not allowed yet.** L > 8; pipeline or arithmetic changes; choosing L without measurements; comparing
   against software or literature as if on the same platform.
7. **Evidence artifact.** `docs/evidence/phase03-multilane/` (per-L logs, `quartus_C2-L<n>_<date>.md`,
   comparison table); `docs/results/result_phase3.md`.
8. **Approval gate.** Human approval in `result_phase3.md` (including the chosen L) before Phase 4.

## Phase 4 — Butterfly pipeline optimisation

1. **Goal.** Raise Fmax, and throughput if possible, at the chosen L by pipelining the butterfly
   (configuration **C3**).
2. **Implementation scope.** Pipeline depth P as a parameter over a small documented set; hazard handling
   between NTT layers (stall or schedule), with the stall cost counted. No arithmetic changes; no layer merging.
3. **Tests / verification.** CRG-1 to CRG-10; dedicated hazard tests at layer boundaries; cycles and stall
   cycles per P; constant cycle count.
4. **Quartus.** One revision per P: Fmax, slack and registers compared against the Phase 3 configuration.
5. **PASS criteria.** Correct for every P; measured comparison complete; ADR for the chosen P; C3 row filled.
6. **Not allowed yet.** Arithmetic optimisation; radix-4 layer merging; Keccak.
7. **Evidence artifact.** `docs/evidence/phase04-pipeline/`; `docs/results/result_phase4.md`.
8. **Approval gate.** Human approval in `result_phase4.md` before Phase 5.

## Phase 5 — Modular arithmetic optimisation

1. **Goal.** Cheaper and faster modular arithmetic for q = 3329 without changing any FIPS 203 result
   (configuration **C4**). Sub-steps, each measured and reviewed separately, in this order:
   - **5a** q-specific reduction: exploit the structure of q (multiplication by the constant q as
     shift-and-add in ALMs) inside the current reduction method.
   - **5b** Montgomery versus Barrett behind the same interface, both measured; choice by ADR. Tables in
     Montgomery form (if chosen) are generated by script from the golden model.
   - **5c** (optional) lazy reduction, only with proven value bounds.
   - **5d** (optional) Karatsuba-style base-case multiplication (4 multiplications instead of 5).
2. **Implementation scope.** `rtl/arith/` units only; the schedule, memory, L and P stay fixed.
3. **Tests / verification.** CRG-1 to CRG-10 after each sub-step. The modular multiplier-reducer is tested
   **exhaustively over all input pairs a, b in [0, q)** (feasible at this size); lazy reduction requires a
   formal overflow/bound proof; full kernel bit-exact regression.
4. **Quartus.** One revision per sub-step (`C4a` to `C4d`): DSP, ALM, Fmax and slack against the previous
   sub-step.
5. **PASS criteria.** Every attempted sub-step correct and measured; the 5b choice recorded in an ADR;
   optional sub-steps either completed with evidence or explicitly marked "not attempted".
6. **Not allowed yet.** Any change to q or to FIPS 203 arithmetic; approximate reduction without proof;
   scheduling changes; Keccak.
7. **Evidence artifact.** `docs/evidence/phase05-arith/5a/` to `5d/` (exhaustive-test logs, formal proofs,
   Quartus files); `docs/results/result_phase5.md` with one section per sub-step.
8. **Approval gate.** Human review of each sub-step checkpoint; approval of `result_phase5.md` before Phase 6.

## Phase 6 — NTT scheduling at operation level

1. **Goal.** Minimise transforms and data movement across whole ML-KEM operations while the inputs that
   will later come from Keccak are still supplied by the testbench.
2. **Implementation scope.** A scheduler for the K-PKE arithmetic of KeyGen, Encrypt and Decrypt: keep
   operands in the NTT domain where FIPS 203 allows it; accumulate matrix-vector products in the NTT
   domain and apply one INTT per output polynomial; no explicit reordering passes. Optional sub-step
   **6b**: radix-4 layer merging, measured separately.
   Expected transform counts (reference-model count from an instrumented kyber-py run, 2026-09-28; must be
   reproduced by instrumenting `tb/golden` before use): KeyGen 6 NTT / 0 INTT / 9 pointwise polynomials;
   Encaps 3 / 4 / 12; Decaps 6 / 5 / 15.
3. **Tests / verification.** CRG-1 to CRG-10. Operation-level arithmetic bit-exact against the golden
   model with matrices and noise polynomials injected from the golden model; transform counters equal
   the reproduced expected counts; constant cycle count.
4. **Quartus.** Kernel plus scheduler: metrics compared against C4; separate revision for 6b.
5. **PASS criteria.** Bit-exact; counts match; cycles and Quartus evidence recorded.
6. **Not allowed yet.** Keccak or samplers in hardware; streaming; changing the order of operations in a
   way that alters any FIPS 203 output.
7. **Evidence artifact.** `docs/evidence/phase06-scheduling/`; `docs/results/result_phase6.md`.
8. **Approval gate.** Human approval in `result_phase6.md` before Phase 7.

## Phase 7 — Keccak-f[1600] + SHA3/SHAKE baseline

1. **Goal.** A correct, measured Keccak baseline (configuration **K0**) before any Keccak optimisation.
2. **Implementation scope.** `rtl/keccak/`: iterative Keccak-f[1600], one round per cycle, fixed 24-cycle
   permutation; sponge modes SHA3-256, SHA3-512, SHAKE128, SHAKE256 with multi-block absorb and squeeze.
   If `tb/golden` has no permutation-level Keccak-f reference, add `tb/golden/keccak.py` first and verify
   it against `hashlib`.
3. **Tests / verification.** CRG-1 to CRG-10. Outputs against `hashlib` for random lengths and boundary
   lengths (0, rate − 1, rate, rate + 1, multiples) for each rate (SHA3-256 136 B, SHA3-512 72 B,
   SHAKE128 168 B, SHAKE256 136 B); multi-block squeeze; permutation-level tests; cycles per permutation
   independent of data (total cycles may depend only on public message lengths).
4. **Quartus.** Standalone K0 revision: ALM, registers, Fmax, slack.
5. **PASS criteria.** All modes bit-exact; fixed permutation latency shown; K0 row filled.
6. **Not allowed yet.** Two rounds per cycle or unrolling; streaming samplers; connection to the arithmetic kernel.
7. **Evidence artifact.** `docs/evidence/phase07-keccak/`; `docs/results/result_phase7.md`.
8. **Approval gate.** Human approval in `result_phase7.md` before Phase 8.

## Phase 8 — Keccak optimisation and streaming

1. **Goal.** Remove Keccak from the critical path. Sub-steps, each measured and reviewed separately:
   - **8a** two rounds per cycle versus one (configuration **C5**).
   - **8b** streaming samplers: CBD directly from the PRF stream; SampleNTT directly from the XOF stream.
   - **8c** matrix A generated on the fly (no storage of Â).
   - **8d** overlap of Keccak with arithmetic (sampling runs while the kernel computes).
   Sub-steps 8b to 8d together form configuration **C6** (recorded as C6b, C6c, C6d).
2. **Implementation scope.** `rtl/keccak/`, `rtl/sample/`, scheduler interface; arithmetic kernel unchanged.
3. **Tests / verification.** CRG-1 to CRG-10 after each sub-step. SampleNTT bit-exact against the golden
   model **including the exact number of XOF bytes consumed**; CBD bit-exact; generated matrix bit-exact.
   Constant-cycle rule for rejection sampling: with fixed ρ and varied secret inputs, cycle counts are
   identical; with varied ρ, cycle-count variation is fully explained by the golden model's rejection count
   for that ρ (public data only).
4. **Quartus.** One revision per sub-step: ALM, registers, M10K, Fmax, slack, and kernel/operation cycles.
5. **PASS criteria.** Each attempted sub-step correct, measured and reviewed; C5 and C6 rows filled.
6. **Not allowed yet.** Full KEM control; compress/encode/FO in hardware; HPS integration.
7. **Evidence artifact.** `docs/evidence/phase08-keccak-stream/8a/` to `8d/`; `docs/results/result_phase8.md`.
8. **Approval gate.** Human review of each sub-step checkpoint; approval of `result_phase8.md` before Phase 9.

## Phase 9 — Full ML-KEM-768 RTL integration (simulation)

1. **Goal.** Complete KeyGen, Encaps and Decaps in RTL, bit-exact against the official vectors
   (configuration **C7-core**).
2. **Implementation scope.** `rtl/mlkem/`: top-level controller for KeyGen_internal, Encaps_internal and
   Decaps_internal (randomness enters as an input port); encode/decode; compress/decompress without
   division; FO re-encryption, constant-time comparison and implicit-rejection selection; key storage;
   the FIPS 203 input checks. Whether the input checks run in hardware or on the HPS is a team decision
   (ADR) taken before this phase starts.
3. **Tests / verification.** CRG-1 to CRG-10. All ML-KEM-768 groups of the pinned NIST ACVP vectors:
   keyGen (25), encapsulation (25), decapsulation (10, including modified ciphertexts), and the key-check
   groups (10 + 10) if the checks are in hardware. Random cross-check against the golden model on a
   documented number of cases with a fixed seed. **Constant-cycle evidence for Decaps**: identical cycles
   for valid and rejected ciphertexts and for different secret keys (fixed public inputs). Full regression.
4. **Quartus.** Full core compile (virtual pins): all metrics.
5. **PASS criteria.** 100% of the applicable vectors pass on both simulators; constant-cycle evidence
   present; Quartus evidence; C7-core row filled.
6. **Not allowed yet.** Any claim about the board; HPS integration; comparisons with software; protocol claims.
7. **Evidence artifact.** `docs/evidence/phase09-integration/` (vector-run logs per group, cross-check log,
   cycle-invariance log, `quartus_C7-core_<date>.md`); `docs/results/result_phase9.md`.
8. **Approval gate.** Human approval in `result_phase9.md` before Phase 10.

## Phase 10 — HPS-FPGA integration on DE10-Nano

1. **Goal.** The accelerator working on the real board under HPS control (configuration **C7-soc**).
   **Blocked until** a DE10-Nano is available (PENDING #8); the protocol flow needs PENDING #1 (target side) and PENDING #7 (emulated message flow).
2. **Implementation scope.** Platform Designer system with the HPS; bridge chosen by measurement
   (transfer mechanism by ADR, PENDING #3); command-level interface (HPS issues KeyGen/Encaps/Decaps, not
   individual NTTs); secret keys and intermediate polynomials stay in the fabric; encode/decode in the
   fabric; a fabric cycle counter readable by the HPS; key zeroisation on reset; driver and test programs
   in `sw/hps/`; functional emulation of the PACE-style key-exchange flow described in the proposal.
   SignalTap taps only on non-secret control signals in the demo bitstream.
3. **Tests / verification.** The same pinned NIST vectors run **on the board** from the HPS; random
   cross-check against the golden model; soak test over many iterations; clock-domain crossings reviewed;
   SignalTap captures of control handshakes; transfer overhead measured separately from core time.
4. **Quartus.** Full system compile with all clocks constrained: all metrics, slack for every clock domain.
5. **PASS criteria.** 100% of the vectors pass on the board; timing met for every clock; bridge/transfer
   ADR recorded; board logs and captures stored. Without a board this phase stays `NOT DONE`.
6. **Not allowed yet.** Final performance claims; comparisons with the software baseline (Phase 11);
   security claims beyond constant-cycle behaviour.
7. **Evidence artifact.** `docs/evidence/phase10-hps-integration/` (board logs, SignalTap captures,
   `quartus_C7-soc_<date>.md`, transfer measurements); `docs/results/result_phase10.md`.
8. **Approval gate.** Human approval in `result_phase10.md` before Phase 11.

## Phase 11 — Final benchmarking and comparison against the software baseline

1. **Goal.** Honest end-to-end numbers for the proposal and the demo.
2. **Implementation scope.** Software baseline on the HPS of the same board (implementation, compiler and
   flags recorded; second baseline only if the team decides, PENDING #6); a written benchmark method
   (warm-up, number of runs, median and spread, timer sources) fixed **before** measuring.
3. **Tests / verification.** Per KeyGen/Encaps/Decaps: core cycles (fabric counter), end-to-end time
   (HPS), transfer overhead, throughput; protocol-level latency of the emulated key exchange; cycle
   invariance repeated on the board; vector runs repeated on the final bitstream.
4. **Quartus.** Final bitstream evidence (the configuration actually measured), all metrics.
5. **PASS criteria.** Every ablation-matrix cell is MEASURED or explicitly marked "not measured" with a
   reason; `docs/proposal/CLAIMS_REGISTER.md` updated; proposal numbers changed from ESTIMATE only where
   evidence exists; claim checker clean.
6. **Not allowed.** Selecting favourable runs; comparing against literature numbers from other platforms
   as if equivalent; power or energy claims without a power measurement; security claims beyond constant-cycle.
7. **Evidence artifact.** `docs/evidence/phase11-benchmark/` (method, raw timing logs, summary tables,
   final Quartus file); `docs/results/result_phase11.md`.
8. **Approval gate.** Human approval in `result_phase11.md` before anything is published as a result or
   before Phase 12.

## Phase 12 — Advanced security features (optional)

1. **Goal.** Optional hardening: masking/shuffling, fault detection (e.g. duplicated FO comparison, memory
   parity), TVLA with the team's oscilloscope, ML-KEM-512/1024 parameterisation, hybrid ECDH + ML-KEM on
   the HPS.
2. **Implementation scope.** One feature at a time, each with its own ADR stating the threat, the method
   and the claim it would support.
3. **Tests / verification.** Full CRG and full vector regression after each feature; TVLA with a documented
   acquisition set-up and trace count; overhead re-measured.
4. **Quartus.** One revision per feature: overhead against the Phase 11 configuration.
5. **PASS criteria.** Feature-specific criteria written in its ADR before implementation.
6. **Not allowed.** Any side-channel or fault-resistance claim without its evidence; weakening the core
   design's constant-cycle property.
7. **Evidence artifact.** `docs/evidence/phase12-security/<feature>/`; `docs/results/result_phase12.md`.
8. **Approval gate.** Human approval per feature.

---

## Optimisation ablation matrix

Every row differs from the row it is compared with by **one** change. All cells are empty until a Quartus
report or test log in this repository fills them; then the cell holds the value and the Evidence column
holds the path. A row that regresses is kept and discussed in its phase's result; an ADR decides whether
the change stays.

| ID | Configuration | Change vs. compared row | Phase | Compared with | Scope | ALM | Registers | M10K | DSP | Fmax (MHz) | Worst slack (ns) | Cycles/op | Latency (µs @ f_clk) | AT (ALM × µs) | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | Baseline | — (L = 1, simple memory) | 1 | — | Kernel | 7,010 / 41,910 | 3104 | 0 / 553 | 3 / 112 | 14.64 (Slow 100C) | -48.323 @ 20.000 ns (NOT met) | NTT 897, INTT 1153 (simulation) | not stated: timing not met at the constrained clock | not stated | `docs/evidence/quartus/C0-20260929.md`, `docs/evidence/phase01-ntt-baseline/quartus_C0_timing_analysis_2026-09-29.md`, `docs/evidence/phase01-ntt-baseline/cocotb_regression_2026-09-29.txt` |
| C1 | + Memory banking | M10K banking + address generation | 2 | C0 | Kernel | 6,749 / 41,910 (-261 vs C0) | 3,105 | 0 / 553 (M10K NOT achieved, async-read limitation -- see evidence) | 3 / 112 | 14.99 (Slow 100C) | -46.720 @ 20.000 ns (NOT met) | NTT 897, INTT 1153 (simulation, identical to C0, 0 stall) | not stated: timing not met at the constrained clock | not stated | `docs/evidence/quartus/C1-20260929.md`, `docs/evidence/phase02-memory/quartus_C1_vs_C0_2026-09-29.md`, `docs/evidence/phase02-memory/cocotb_regression_2026-09-29.txt` |
| C2-L1 | + Multi-lane (L=1) | Lane datapath rebuilt on multi-port memory (parity check vs C0/C1) | 3 | C1 | Kernel | 6,018 / 41,910 | 3100 | 0 / 553 | 3 / 112 | 14.76 (Slow 100C) | -47.733 @ 20.000 ns (NOT met) | NTT 897, INTT 1153 (simulation, identical to C0/C1) | not stated: timing not met at the constrained clock | not stated | `docs/evidence/quartus/C2-L1-20260929.md`, `docs/evidence/phase03-multilane/cocotb_regression_2026-09-29.txt` |
| C2-L2 | + Multi-lane (L=2) | 2 butterflies/cycle | 3 | C1 | Kernel | 5,728 / 41,910 | 3098 | 0 / 553 | 5 / 112 | 13.54 (Slow 100C) | -54.644 @ 20.000 ns (NOT met) | NTT 449, INTT 705 (simulation) | not stated: timing not met at the constrained clock | not stated | `docs/evidence/quartus/C2-L2-20260929.md`, `docs/evidence/phase03-multilane/cocotb_regression_2026-09-29.txt` |
| C2-L4 | + Multi-lane (L=4) | 4 butterflies/cycle | 3 | C1 | Kernel | 7,629 / 41,910 | 3102 | 0 / 553 | 9 / 112 | 11.60 (Slow 100C) | -66.690 @ 20.000 ns (NOT met) | NTT 225, INTT 481 (simulation) | not stated: timing not met at the constrained clock | not stated | `docs/evidence/quartus/C2-L4-20260929.md`, `docs/evidence/phase03-multilane/cocotb_regression_2026-09-29.txt` |
| C2-L8 | + Multi-lane (L=8) | 8 butterflies/cycle | 3 | C1 | Kernel | 11,446 / 41,910 (**over ADR 0004's 10,478 ALM budget**) | 3100 | 0 / 553 | 17 / 112 | 7.62 (Slow 100C) | -111.219 @ 20.000 ns (NOT met) | NTT 113, INTT 369 (simulation) | not stated: timing not met at the constrained clock | not stated | `docs/evidence/quartus/C2-L8-20260929.md`, `docs/evidence/phase03-multilane/cocotb_regression_2026-09-29.txt` |
| C2-K2-K1-L1 | + K2, K1 (L=1) | TWO changes vs C2-L1, an exception to the one-change rule: t_q sized per L (K2) + one shared multiplier per butterfly (K1); the single-change step C2 -> C2-K2 is measured in `docs/evidence/quartus/C2-L1-K2-20260930.md`. Supplementary, outside the written Phase 3 scope | 3 | C2-L1 | Kernel | 5,566 / 41,910 | 3099 | 0 / 553 | 2 / 112 | 14.33 (Slow 100C) | -49.804 @ 20.000 ns (NOT met) | NTT 897, INTT 1153 (simulation, identical to C2-L1) | not stated: timing not met at the constrained clock | not stated | `docs/evidence/quartus/C2-K2-K1-L1-20260930.md`, `docs/evidence/phase03-multilane/k1_cocotb_regression_2026-09-30.txt` |
| C2-K2-K1-L2 | + K2, K1 (L=2) | TWO changes vs C2-L2, an exception to the one-change rule: t_q sized per L (K2) + one shared multiplier per butterfly (K1); the single-change step C2 -> C2-K2 is measured in `docs/evidence/quartus/C2-L2-K2-20260930.md`. Supplementary, outside the written Phase 3 scope | 3 | C2-L2 | Kernel | 5,374 / 41,910 | 3095 | 0 / 553 | 3 / 112 | 12.63 (Slow 100C) | -59.148 @ 20.000 ns (NOT met) | NTT 449, INTT 705 (simulation, identical to C2-L2) | not stated: timing not met at the constrained clock | not stated | `docs/evidence/quartus/C2-K2-K1-L2-20260930.md`, `docs/evidence/phase03-multilane/k1_cocotb_regression_2026-09-30.txt` |
| C2-K2-K1-L4 | + K2, K1 (L=4) | TWO changes vs C2-L4, an exception to the one-change rule: t_q sized per L (K2) + one shared multiplier per butterfly (K1); the single-change step C2 -> C2-K2 is measured in `docs/evidence/quartus/C2-L4-K2-20260930.md`. Supplementary, outside the written Phase 3 scope | 3 | C2-L4 | Kernel | 6,775 / 41,910 | 3098 | 0 / 553 | 5 / 112 | 10.89 (Slow 100C) | -71.868 @ 20.000 ns (NOT met) | NTT 225, INTT 481 (simulation, identical to C2-L4) | not stated: timing not met at the constrained clock | not stated | `docs/evidence/quartus/C2-K2-K1-L4-20260930.md`, `docs/evidence/phase03-multilane/k1_cocotb_regression_2026-09-30.txt` |
| C2-K2-K1-L8 | + K2, K1 (L=8) | TWO changes vs C2-L8, an exception to the one-change rule: t_q sized per L (K2) + one shared multiplier per butterfly (K1); the single-change step C2 -> C2-K2 is measured in `docs/evidence/quartus/C2-L8-K2-20260930.md`. Supplementary, outside the written Phase 3 scope | 3 | C2-L8 | Kernel | 9,754 / 41,910 **(selected, ADR 0005; within the 10,478 ALM budget)** | 3094 | 0 / 553 | 9 / 112 | 7.68 (Slow 100C) | -110.494 @ 20.000 ns (NOT met) | NTT 113, INTT 369 (simulation, identical to C2-L8) | not stated: timing not met at the constrained clock | not stated | `docs/evidence/quartus/C2-K2-K1-L8-20260930.md`, `docs/evidence/phase03-multilane/k1_cocotb_regression_2026-09-30.txt` |
| C3-P0 | + Pipeline (P=0, reference) | Frozen C2-K2-K1-L8 re-compiled at 40.000 ns | 4 | C2-K2-K1-L8 (ADR 0005) | Kernel | 9,723 / 41,910 | 3097 | 0 / 553 | 9 / 112 | 7.65 (Slow 100C) | -90.653 @ 40.000 ns (NOT met) | NTT 113, INTT 369 (simulation) | not stated: kernel-only Fmax, no board | not stated | `docs/evidence/phase04-pipeline/quartus_C3-P0_20260930.md`, `docs/evidence/phase04-pipeline/cocotb_regression_2026-09-30.txt` |
| C3-P2 | + Pipeline (P=2) | Cuts A_13, D_3 | 4 | C2-K2-K1-L8 (ADR 0005) | Kernel | 9,696 / 41,910 | 3,817 | 16 / 553 (tool-inferred) | 9 / 112 | 24.77 (lowest slow corner) | -0.368 @ 40.000 ns (NOT met) | NTT 115, INTT 371 (simulation) | not stated: kernel-only Fmax, no board | not stated | `docs/evidence/phase04-pipeline/quartus_C3-P2_20260930.md`, `docs/evidence/phase04-pipeline/cocotb_regression_2026-09-30.txt` |
| C3-P4 | + Pipeline (P=4) | Cuts A_7, M, X, D_7 -- proposed by ADR 0008 under the historical 25% budget (never accepted, superseded by ADR 0009); integration baseline for GHRD + C3-P4 (`docs/evidence/phase04-pipeline/ghrd_plus_c3p4_integration_2026-10-01.md`) | 4 | C2-K2-K1-L8 (ADR 0005) | Kernel | 10,439 / 41,910 (seeds 1–6: 10,439–10,503; within the 30% / 12,573 budget of ADR 0009) | 4,145 | 26 / 553 (tool-inferred) | 9 / 112 | 31.98 (lowest slow corner) | +8.734 @ 40.000 ns (met) | NTT 117, INTT 373 (simulation) | not stated: kernel-only Fmax, no board | not stated | `docs/evidence/phase04-pipeline/quartus_C3-P4_20260930.md`, `docs/evidence/phase04-pipeline/cocotb_regression_2026-09-30.txt` |
| C3-P6 | + Pipeline (P=6) | Cuts A_4, A_11, M, X, D_5, D_11 -- **SELECTED (ADR 0009, 2026-10-01): L = 8, P = 6**; integration with GHRD: `docs/evidence/phase04-pipeline/ghrd_plus_c3p6_integration_2026-10-01.md` (12,375 ALM combined, NTT 40 ns met, MEASURED) | 4 | C2-K2-K1-L8 (ADR 0005) | Kernel | 10,505 / 41,910 (seeds 1–6: 10,484–10,516; over the historical 25% budget, **within the 30% / 12,573 budget of ADR 0009**) | 4,168 | 29 / 553 (tool-inferred) | 9 / 112 | 34.19 (lowest slow corner) | +10.753 @ 40.000 ns (met) | NTT 119, INTT 375 (simulation) | not stated: kernel-only Fmax, no board | not stated | `docs/evidence/phase04-pipeline/quartus_C3-P6_20260930.md`, `docs/evidence/phase04-pipeline/cocotb_regression_2026-09-30.txt` |
| C4a | + Arithmetic 5a (fold reducer) | q-specific reduction: 2^12 = 767 (mod q), shift-and-add folds + select; cuts A_4, A_11, M, X, F_3, F_5 (P = 6) | 5 | C3-P6 | Kernel | 9,847 / 41,910 | 4,109 | 29 / 553 (tool-inferred) | 9 / 112 | 33.73 (lowest slow corner) | +10.352 @ 40.000 ns (met) | NTT 119, INTT 375 (simulation) | not stated: kernel-only Fmax, no board | not stated | `docs/evidence/phase05-arith/5a/quartus_C4a_20261001.md`, `docs/evidence/phase05-arith/5a/summary_5a_2026-10-01.md`, `docs/evidence/phase05-arith/5a/verify_2026-10-01.txt` |
| C4b-B | + Arithmetic 5b (Barrett) | Barrett reducer (k = 24, M = 5039), cuts X, S_1, S_2; **selected by the ADR 0011 rule, ADR 0013 Proposed (PENDING #23): this is the C4 configuration** | 5 | C4a | Kernel | 9,208 / 41,910 (seeds 1-6: 9,166-9,208; median 9,171) | 4,115 | 29 / 553 (tool-inferred) | 18 / 112 (C3-P6: 9) | 34.54 (seed 1; median over seeds 1-6 34.515, range 33.46-34.84) | +11.044 @ 40.000 ns (met at every seed) | NTT 119, INTT 375 (simulation) | t_NTT 3.448 us, t_INTT 10.865 us at median Fmax (perhitungan tim); kernel-only, no board | not stated | `docs/evidence/phase05-arith/5b/quartus_C4b-B_20261001.md` (+ `-s2..s6`), `docs/evidence/phase05-arith/5b/selection_worksheet_2026-10-01.md`, `docs/evidence/phase05-arith/5b/verify_2026-10-01.txt` |
| C4b-M | + Arithmetic 5b (Montgomery, comparison) | Montgomery reducer (R = 2^12), Montgomery-form twiddle ROM; not selected | 5 | C4a | Kernel | 9,249 / 41,910 (seeds 1-6: 9,249-9,297; median 9,286.5) | 4,297 | 29 / 553 (tool-inferred) | 9 / 112 | 32.81 (seed 1; median 33.780, range 32.81-34.25) | +9.526 @ 40.000 ns (met at every seed) | NTT 119, INTT 375 (simulation) | not stated: kernel-only Fmax, no board | not stated | `docs/evidence/phase05-arith/5b/quartus_C4b-M_20261001.md` (+ `-s2..s6`), `docs/evidence/phase05-arith/5b/selection_worksheet_2026-10-01.md` |
| C4c | + Arithmetic 5c (lazy INTT inputs) | INTT multiplier input b + q - a in [1, 2q), side operand a + b in [0, 2q), reduced once at the output (ADR 0014; D6 amended for this experiment only); **NOT adopted** (median Fmax 33.100 MHz, rule needs > 34.84; ADR 0012 not met) | 5 | C4b-B | Kernel | 9,043 / 41,910 (seeds 1-6: 9,032-9,094; median 9,059.5) | 4,076 | 29 / 553 (tool-inferred) | 18 / 112 | 32.98 (seed 1; median 33.100, range 32.27-35.26) | +9.682 @ 40.000 ns (met at every seed) | NTT 119, INTT 375 (simulation) | not stated: not adopted | not stated | `docs/evidence/phase05-arith/5c/quartus_C4c_20261001.md` (+ `-s2..s6`), `docs/evidence/phase05-arith/5c/selection_worksheet_2026-10-01.md`, `docs/evidence/phase05-arith/5c/summary_5c_2026-10-01.md` |
| C4d | + Arithmetic 5d (Karatsuba-style base case) | **Not attempted in Phase 5** (proposed to move to Phase 6: `base_case_multiply.sv` is not part of the C3-P6 / C4 core; ADR 0015 Proposed) | 5 | C4b-B | Kernel | not attempted | not attempted | not attempted | not attempted | not attempted | not attempted | not attempted | not attempted | not attempted | `docs/decisions/0015-phase-5d-karatsuba-style-base-case-not-attempted-in-phase-5-.md` |
| C4b-B-20 | Information compile at 20.000 ns (final C4) | Same RTL as C4b-B; constraint 20.000 ns, default seed; not a gate (ADR 0010, ADR 0011 D1) | 5 | C3-P6-20 | Kernel | 9,305 / 41,910 | 4,272 | 29 / 553 (tool-inferred) | 18 / 112 | 44.33 (lowest slow corner) | -2.557 @ 20.000 ns (NOT met) | NTT 119, INTT 375 (simulation) | not stated: timing not met at the constrained clock | not stated | `docs/evidence/phase05-arith/closure/quartus_C4b-B-20_20261001.md`, `docs/evidence/phase05-arith/closure/info_20ns_2026-10-01.md` |
| C3-P6-20 | Information compile at 20.000 ns (C3-P6 reference) | Phase 4 RTL unchanged; constraint 20.000 ns, default seed; not a gate | 5 | C3-P6 | Kernel | 10,557 / 41,910 | 4,316 | 29 / 553 (tool-inferred) | 9 / 112 | 45.33 (lowest slow corner) | -2.059 @ 20.000 ns (NOT met) | NTT 119, INTT 375 (simulation) | not stated: timing not met at the constrained clock | not stated | `docs/evidence/phase05-arith/closure/quartus_C3-P6-20_20261001.md`, `docs/evidence/phase05-arith/closure/info_20ns_2026-10-01.md` |
| S1 | NTT scheduling *(reference row)* | Operation-level schedule (+ 6b sub-row) | 6 | C4 | Kernel + scheduler | — | — | — | — | — | — | — | — | — | — |
| K0 | Keccak baseline *(reference row)* | Iterative Keccak-f, 1 round/cycle | 7 | — | Keccak | — | — | — | — | — | — | — | — | — | — |
| C5 | + Keccak optimisation | 2 rounds/cycle | 8a | K0 | Keccak | — | — | — | — | — | — | — | — | — | — |
| C6 | + Streaming | 8b / 8c / 8d (one sub-row each) | 8 | C5 + S1 | Operation | — | — | — | — | — | — | — | — | — | — |
| C7 | Full integration | Complete KEM (C7-core in simulation; C7-soc on board) | 9, 10 | C6 | Operation / system | — | — | — | — | — | — | — | — | — | — |

Rows S1 and K0 are reference points added so that C5 and C6 each still differ by one change. Cycles/op:
kernel rows report cycles per NTT, INTT and pointwise product; Keccak rows report cycles per permutation
and per hash call; operation rows report cycles per KeyGen, Encaps and Decaps. Latency uses the
constrained clock that met timing. The final measured copy of this matrix goes into
`docs/evidence/phase11-benchmark/ablation_matrix.md`.

## Proposal pages (cover and references not counted; limit 6 pages)
- Pages 1-3: Sections 1-2 (written).
- Pages 4-6: Section 3 "Proposed Chip Design" (block diagram, RTL module list, resource table, tools,
  test plan, success metrics). **Not written yet.** Resource cells stay `ESTIMATE` or `[...]` until the
  corresponding phase produces Quartus evidence (kernel values from Phase 1 onward, full-core values from
  Phase 9, system values from Phase 10); every number cites its evidence file.
- Template error to avoid: it lists 415,000 flip-flops, while Intel's table says 166,036.
