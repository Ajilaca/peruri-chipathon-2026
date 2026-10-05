<!-- claim-lint: skip-file (internal experiment record, not proposal text) -->
# Phase 3 supplementary experiment K1 — one shared multiplier per butterfly (config C2-K2-K1)

- Date (UTC): 2026-09-30
- Branch: `phase3-multilane`, on top of `b11b08f` (K2 committed)
- Status: **measured for all four L; L=8 is back under the ADR 0004 ALM budget. Selected by the team:
  ADR 0005 (Accepted 2026-09-30, Faza Dzil, Team J5) adopts C2-K2-K1 and selects L=8.** ADR 0004 is
  unchanged. (When this record was first written ADR 0005 was only Proposed and L=8 was a candidate.)
- Scope: approved by the team (2026-09-30) as a *separate, supplementary* experiment, because it
  changes the butterfly datapath and so deviates from the written Phase 3 scope
  ("butterfly, arithmetic and memory as in Phase 2"). Built on K2, measured for L=1/2/4/8.
- Frozen and untouched: `rtl/ntt/butterfly.sv`, `rtl/ntt/modmul_reduce.sv`, `rtl/ntt/ntt_core_c2.sv`,
  `rtl/ntt/ntt_core_c2_k2.sv`, every Phase 3 C2 evidence file and `docs/results/phase03.md`.

## What changed
- `rtl/ntt/butterfly_shared.sv` (new): the same forward (CT) and inverse (GS) equations as
  `butterfly.sv`, but with ONE `modmul_reduce` whose operand is `mode ? (b - a) mod q : b`, instead of
  one `modmul_reduce` per mode. mode is fixed for a whole NTT/INTT run, so both multipliers were never
  needed in the same cycle. The reduction method (`modmul_reduce.sv`, `%` by Q) is reused unchanged.
- `rtl/ntt/ntt_core_c2_k2_k1.sv`: copy of `ntt_core_c2_k2.sv`, one change (`butterfly` ->
  `butterfly_shared`). Wrappers `ntt_core_c2_k2_k1_l{1,2,4,8}.sv`; Quartus revisions
  `C2-K2-K1-L{1,2,4,8}` (QSF = C2-L<n>'s with only the top entity, output folder, the core/wrapper
  files and the added `butterfly_shared.sv` changed; SDC identical).
- To isolate K1 per L, K2 was also completed for L=1/2/4 (revisions `C2-L{1,2,4}-K2`), and the C2-L1 /
  C2-L2 baselines were re-compiled for their per-entity tables (totals reproduced exactly).

## Correctness
| Check | Result | Evidence |
|---|---|---|
| Lint (Verilator `-Wall`) core at L=1/2/4/8 + all four wrappers, slang | clean | `cmd: verilator --lint-only -Wall --timing -sv rtl/ntt/*.sv rtl/mem/*.sv --top-module ntt_core_c2_k2_k1 -GNUM_LANES=<L>` |
| Unit: `butterfly_shared` vs golden (unchanged `tb/ntt/test_butterfly.py`: corners + 1000 random per mode) | 2/2 Verilator, 2/2 Icarus | `k1_cocotb_regression.txt` |
| Core cocotb, L=1/2/4/8, bit-exact + round-trip + constant cycles + `bank_overflow_o`==0 | 16/16 Verilator, 16/16 Icarus | same file |
| Cycle counts | identical to C2 for every L (L=8: NTT 113, INTT 369; 8 butterflies/cycle) | same file |
| Core formal, first flow (same as C2, K2 at the time) | L=1 PASS; L=2/4/8 UNKNOWN (harness artefact, caveat 4) | `k1_formal.txt` |
| Core formal, corrected flow (`read_slang` + `memory_map -rom-only`) | **PASS at L=1/2/4/8**, negative controls fail as required | `formal_rerun.md` |
| Formal equivalence `butterfly` vs `butterfly_shared`, full arithmetic | not completed: 30-min timeout (caveat 5) | `formal/phase03-multilane/k1_butterfly_equiv.sby` |
| Equivalence, option 1: multiplier abstracted (uninterpreted function + Ackermann consistency), all modes, all inputs < q | **PASS**; both negative controls FAIL as required | `k1_equiv_abstraction.txt`, `formal/phase03-multilane/k1_butterfly_equiv_abs.sby`, `k1_negctl_operand.sby`, `k1_negctl_noack.sby` |
| Equivalence, option 2: exhaustive RTL simulation, all 2 x 3329^3 = 73,785,560,578 inputs, three-way vs golden | **PASS, 0 mismatches**, no assumptions | `k1_exhaustive_equivalence.txt`, `tb/ntt/k1_exhaustive/` |

## Resources and timing (MEASURED, Quartus Prime Lite 25.1std, 5CSEBA6U23I7, same constraints/seed)
| | L=1 | L=2 | L=4 | L=8 |
|---|---|---|---|---|
| ALM, C2 | 6,018 | 5,728 | 7,629 | 11,446 |
| ALM, C2-K2 | 6,389 | 5,788 | 7,600 | 11,232 |
| **ALM, C2-K2-K1** | **5,566** | **5,374** | **6,775** | **9,754** |
| K1 vs C2 | −452 | −354 | −854 | **−1,692** |
| Within ADR 0004 budget (10,478)? | yes | yes | yes | **yes (724 below)** |
| DSP, C2 → C2-K2-K1 | 3 → 2 | 5 → 3 | 9 → 5 | 17 → 9 |
| Registers, C2-K2-K1 | 3,099 | 3,095 | 3,098 | 3,094 |
| M10K | 0 / 553 (all configs) | | | |
| Fmax Slow 100C, C2 / K2 / K2+K1 (MHz) | 14.76 / 15.40 / 14.33 | 13.54 / 13.66 / 12.63 | 11.60 / 11.61 / 10.89 | 7.62 / 7.85 / 7.68 |
| Worst setup slack @ 20.000 ns, C2-K2-K1 | −49.804 ns | −59.148 ns | −71.868 ns | −110.494 ns |
| NTT / INTT cycles (simulation, all three configs) | 897 / 1153 | 449 / 705 | 225 / 481 | 113 / 369 |

Timing is NOT met for any configuration (as for C0/C1/C2; pipelining is Phase 4). Critical warnings
are the same two types as the baselines (15725 virtual-pin clock, 332148 timing not met); 0 ×
Warning 10335. Evidence: `evidence/quartus/C2-K2-K1-L{1,2,4,8}.md`,
`C2-L{1,2,4}-K2.md`, `C2-L8-K2.md`; per-entity tables in
`k1_entity_breakdown.txt`.

**Where the K1 saving comes from (L=8):** the 16 per-lane `modmul_reduce` instances (forward +
inverse, 3,068.7 ALM) become 8 shared ones (1,563.5 ALM); the added operand mux costs +48.3 ALM in the
butterflies (~6 ALM/lane). Same pattern at every L (per lane: one multiplier+divider of ~190–195 ALM
removed, ~5–8 ALM of mux added).

## Caveats found during the experiment (reported, not hidden)
1. **Fitter packing variation is large in the memory block.** K2 at L=1 is +371 ALM vs C2, but all of
   it is in `poly_mem_multiport` (5,180.9 → 5,554.7 ALM) with *identical* combinational ALUTs (2,669)
   and registers (3,072): same logic, packed into ALMs differently. So ALM totals can move by a few
   hundred ALM between compiles without any logic change (interpretation of MEASURED numbers, not a
   separate measurement). K1-L8's 724-ALM margin is larger than the largest swing seen (~370 ALM),
   but not by a wide factor; a seed sweep would quantify it.
2. **K2 is not a uniform improvement**: −214 (L8), −29 (L4), +60 (L2), +371 (L1, packing, see above).
3. **Fmax drops slightly with K1 at L=1/2/4** (the operand mux sits in front of the multiplier, on the
   critical path through the divider); at L=8 it is within noise of C2. Timing closure is Phase 4.
4. **Formal toolchain findings (both now handled in the flow).** (a) Yosys's native `read -formal`
   frontend does not elaborate the `ntt_pkg` package functions `add_mod`/`sub_mod` (their results
   become undriven wires), so its model of `butterfly.sv` is wrong (inverse a=b=1920 gives a_o=0
   instead of 511); `read_slang` models it correctly. (b) The L>1 core-proof UNKNOWN recorded in the
   table above was a separate harness artefact: `proc_rom` turns the ROMs into memory cells whose
   contents are free state in the induction step. With `read_slang` + `memory_map -rom-only`
   (harness only, RTL unchanged) C2, C2-K2 and C2-K2-K1 all PASS at L=1/2/4/8, negative controls
   fail as they must, and the Phase 1/2 proofs still PASS:
   `formal_rerun.md`. That file supersedes the L>1 lines of `k1_formal.txt`
   and `k2_formal.txt`.
5. **Butterfly equivalence: the full-arithmetic formal proof did not finish, but the equivalence is now
   established two other ways.** With `read_slang` the miter models the real 12x12 multiplier and 24/12
   divider on both sides; boolector did not finish in 30 min (multiplier/divider equivalence between
   structurally different circuits is a known hard case for bit-level solvers), so `k1_butterfly_equiv.sby`
   is kept as a record, not a result. Completed instead: (1) `k1_butterfly_equiv_abs.sby` abstracts
   `modmul_reduce` (the same unchanged module on both sides) as an uninterpreted function with
   functional-consistency constraints and proves the operand selection and add/sub/mux logic around it
   equivalent: PASS; its assumption (modmul_reduce is a pure function of its inputs) is stated in
   `modmul_reduce_uf.sv`; two negative controls (a deliberately wrong inverse operand; the miter without
   the consistency assumptions) both FAIL, so the PASS is not vacuous. (2) an exhaustive Verilator
   simulation of the unchanged RTL over every mode and every a, b, zeta in [0, q) (73,785,560,578
   evaluations, 1,229 s on 8 processes) compared against the golden butterfly step: 0 mismatches, no
   assumptions. One tooling note from making (1) work: `read_slang` turns a stub's `(* anyseq *)` wire
   into constant x, which made the first attempt FAIL spuriously; `setundef -anyseq` in the .sby script
   fixes that and is required.

## Conclusion
K1 is bit-exact (simulation on two simulators; butterfly equivalence proven with the multiplier
abstracted and by exhaustive simulation), cycle-identical, keeps 8 butterflies/cycle at L=8, does not
change the modular reduction method, and brings **C2-K2-K1-L8 to 9,754 ALM, 724 ALM under the ADR 0004
budget**. It also shrinks every other L, so all four L of this family are within budget. The team
decided (ADR 0005, Accepted) to adopt this configuration and select **L=8**; Phase 4 starts from
C2-K2-K1 at L=8. The C2 result (L=4) stays in `docs/results/phase03.md` as the baseline comparison.
