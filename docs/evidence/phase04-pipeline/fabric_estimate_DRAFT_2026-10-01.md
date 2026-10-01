<!-- claim-lint: skip-file (internal planning draft, not proposal text; every number below is labelled) -->
# DRAFT — Fabric content estimate for Phases 5–10 (input to the ALM-budget review of ADR 0004 / ADR 0008)

- Status: **DRAFT for team discussion. Not a decision, not a requirement, not a proposal number.**
- Date (UTC): 2026-10-01. Written at the team's request after the review of the 25% ALM budget.
- Every figure is labelled **MEASURED** (path to a Quartus report in this repo) or **ESTIMATE** (method and
  assumptions stated). No figure is taken from literature: this draft has **no cited source** for any block
  that does not exist yet. Where a cited figure would help, the row says so.
- Confidence of the ESTIMATE rows is **low**. The ranges are wide on purpose; they are meant to show which
  decisions move the total, not to predict it.

## 1. Why this estimate exists
ADR 0004 reserves 75% of the device for "Keccak, the sampler, or protocol logic sharing the same fabric",
but no estimate of that content was ever written (review of 2026-10-01). A budget for the NTT core only
makes sense as *total available − everything else*. This draft is a first attempt at "everything else".

## 2. Calibration from our own measurements (MEASURED)
Source: `quartus/phase04_pipeline_c3/output_files_P4/C3-P4.fit.rpt`, "Fitter Resource Utilization by
Entity" (the extracted summary is `docs/evidence/phase04-pipeline/quartus_C3-P4_20260930.md`).

| Part of C3-P4 (L = 8, P = 4) | ALM | Comb. ALUTs | Registers | DSP | Note |
|---|---|---|---|---|---|
| Whole core | 10,439 | 13,047 | 4,145 | 9 | |
| `poly_mem_multiport_pipe` (256 × 12 bit, 8 banks, 16 ports, flip-flop storage) | 7,621 | 8,019 | 3,660 | 0 | **73% of the core** |
| 8 × `butterfly_shared_pipe` (incl. multiplier + staged reducer) | ~2,097 (257–277 each) | ~3,862 | ~394 | 8 | |
| `modmul_reduce_staged` (scaling multiplier, alone) | 151 | 303 | 21 | 1 | one multiplier + 13-stage reducer |
| 8 × `twiddle_rom` | ~240 (30 each) | 288 | 0 | 0 | 128 × 12 bit ROM in logic |
| FSM, counters, address generation (core own logic) | ~296 | 567 | 30 | 0 | |

Ratios used below (perhitungan tim from the row above): ~1.25 combinational ALUTs per ALM for this design
style; storage of one 12-bit coefficient in flip-flops **with 16-port access** costs ~30 ALM
(7,621 / 256). The second ratio is the reason storage technology dominates everything else in Section 4.

## 3. Blocks that will share the fabric (ESTIMATE unless marked)

| # | Block (phase) | ALM low | ALM high | M10K | DSP | Method and assumptions |
|---|---|---|---|---|---|---|
| 1 | NTT/INTT core C3-P4 (Phase 4) | 10,439 | 10,503 | 26 | 9 | **MEASURED**, seeds 1–6, `docs/evidence/phase04-pipeline/seed_sweep_2026-10-01.md` |
| 2 | Phase 5 arithmetic change (delta on row 1) | −700 | +300 | 0 | 0 to +9 | ESTIMATE. The 9 multiplier+reducers are ~150 ALM each by row "modmul_reduce_staged" (~1,350 total). Barrett/Montgomery may move part of the reducer into DSP blocks (saving ALM) or add correction logic (costing ALM). Sign unknown. |
| 3 | Pointwise base-case multiply + operation scheduler (Phase 6) | 500 | 2,000 | 0–4 | 2–10 | ESTIMATE. Base case: 4–5 modular multiplications (each ~150 ALM by row "modmul_reduce_staged", fewer if DSP-mapped) plus accumulation; scheduler is an FSM / microcode sequencer, sized like 1–5 × the core's own control (~300 ALM). |
| 4 | Keccak-f[1600], 1 round/cycle, sponge for SHA3/SHAKE (Phase 7, K0) | 3,000 | 5,000 | 0 | 0 | ESTIMATE, first-principles LUT count: 1,600 state registers (≥ 800 ALM at 2 registers/ALM, not binding); θ column parities 320 × one 5-input XOR; θ+ρ+π+χ per state bit needs 9 inputs → ~2 LUT levels → ~3,200 LUTs; absorb XOR and load/hold mux on the rate part (up to 1,344 bits) ~1 LUT per bit; total ~5,000–6,500 ALUTs → ÷ 1.25–1.7 ALUT/ALM. **A cited figure for an iterative Keccak on Cyclone V would replace this row** (none in `docs/proposal/references.md` yet). |
| 5 | Keccak 2 rounds/cycle (Phase 8a, optional) — delta | +2,500 | +4,000 | 0 | 0 | ESTIMATE: second copy of the round logic (row 4 minus state and absorb logic). Only if 8a is adopted. |
| 6 | Samplers: SampleNTT (rejection, from XOF stream) + CBD η = 2 (Phase 8b) | 200 | 800 | 0–2 | 0 | ESTIMATE: 12-bit field extraction from the squeeze stream, two comparisons with q, small counters; CBD = bit counts on 2 + 2 bits and a subtraction mod q. Width of the stream interface is the main unknown. |
| 7 | Top-level KEM controller: KeyGen / Encaps / Decaps (Phase 9) | 500 | 2,000 | 0–2 | 0 | ESTIMATE: sequencing FSM or microcode with a small ROM; sized as 2–7 × the core's control logic. |
| 8 | Encode/decode, compress/decompress without division (du = 10, dv = 4, d = 1) (Phase 9) | 500 | 2,000 | 0 | 0–4 | ESTIMATE: compress needs a multiplication by a constant reciprocal and rounding per coefficient (≈ one constant multiplier each, LUT or DSP); byte packing is a shift/mux network whose size depends on the chosen bus width. |
| 9 | FO transform: constant-time ciphertext comparison (1,088 B) + implicit-rejection select (Phase 9) | 100 | 300 | 0 | 0 | ESTIMATE: streaming compare with an OR accumulator and a 32-byte select; the re-encryption reuses rows 1–8. |
| 10 | Key and polynomial storage (Phase 9), **in M10K** | 200 | 800 | 20 | 0 | ESTIMATE (count is an inference from the K-PKE data flow, not yet instrumented): ~20–30 polynomials live at once (s, e, t̂, r, e1, e2, u, v, u′, v′ …; Â generated on the fly per 8c) at 3,072 bit each → one M10K each (10,240 bit) plus dk (19,200 bit) and ek (9,472 bit) → ~20–40 M10K of 553; ALM only for address/port logic. |
| 10′ | Same storage **in flip-flops** (alternative to row 10) | see method | — | 0 | 0 | ESTIMATE by the calibration ratio. Single-port FF storage: 61,000–92,000 registers for 20–30 polynomials (37–55% of the device's 166,036 registers) plus wide read multiplexers — large, but not shown infeasible. Multi-port FF storage as in row 1 (~30 ALM per coefficient): 20 polynomials ≈ 153,600 ALM, **more than the device**. Listed to show why the storage technology must be decided before Phase 9. |
| 11 | FIPS 203 input checks in hardware (Phase 9, only if the team puts them in fabric) | 0 | 400 | 0 | 0 | ESTIMATE: modulus check = streaming comparison of 768 coefficients with q; hash check reuses Keccak. 0 if done on the HPS (open team decision, ROADMAP Phase 9). |
| 12 | HPS bridge, Platform Designer interconnect, CSRs, cycle counter, clock crossing (Phase 10) | 300 | 2,000 | 0–4 | 0 | ESTIMATE. **Can be MEASURED now without a board** by compiling the Intel DE10-Nano GHRD (`intel/de10-nano-hardware`, already cited in ADR 0006) with and without a stub slave; that would replace this row. Depends on PENDING #3 (DMA or memory-mapped). |
| 13 | SignalTap for the demo bitstream (Phase 10) | 0 | 1,500 | 5–30 | 0 | ESTIMATE: depends on the number of tapped signals and sample depth; ROADMAP restricts taps to non-secret control signals. Debug builds only. |

## 4. Totals (ESTIMATE, sum of the rows; percentages of the fitter's 41,910 ALM)

| Scenario | ALM | % of device | NTT core (row 1) share of the total |
|---|---|---|---|
| Low (rows 1–4, 6–12 at "low"; no 8a; no SignalTap) | ~15,000 | ~36% | ~70% |
| High without optional items (rows 1–4, 6–12 at "high") | ~26,100 | ~62% | ~40% |
| High with 8a and SignalTap | ~31,600 | ~75% | ~33% |
| Any scenario with multi-port FF storage (row 10′) instead of row 10 | > 41,910 | > 100% | — |

Arithmetic (perhitungan tim): low = 10,439 − 700 + 500 + 3,000 + 200 + 500 + 500 + 100 + 200 + 0 + 300 + 0 = 15,039;
high = 10,503 + 300 + 2,000 + 5,000 + 800 + 2,000 + 2,000 + 300 + 800 + 400 + 2,000 = 26,103; plus 4,000 (8a) and
1,500 (SignalTap) = 31,603. M10K stays below ~100 of 553 in every scenario; DSP below ~40 of 112 (ESTIMATE).

## 5. What the estimate does and does not say
- **The NTT core is probably the largest single block**, but most likely not the majority of the final
  fabric content. The "everything else" part ranges from ~4,600 to ~21,100 ALM (ESTIMATE) — a factor of
  ~4.6 between the ends. That spread, not the 25-vs-35% question, is the main uncertainty.
- **Storage technology decides feasibility.** Multi-port flip-flop storage for the operation-level data (row 10′) would exceed the whole device; M10K storage (row 10) costs a few hundred ALM. The NTT
  core's own working memory (7,621 ALM, MEASURED) is the single largest item in the low scenario; whether
  any of it can move to M10K is the Phase 2 open gap (async read). C3 now has a registered read stage,
  which ADR 0007 names as the precondition for M10K, but the memory needs 2 reads + 2 writes per bank per
  cycle and an M10K has two ports — so this is **not** shown to be possible (inference, not evidence).
- A budget for the NTT core derived from these numbers would be *(total the team is willing to fill) −
  (rows 2–13)*. This draft does not propose the "total the team is willing to fill"; that remains a team
  decision (C5).
- Nothing here is a claim about routing, timing or fit of the integrated system. Only a full-system compile
  (Phase 9 core, Phase 10 SoC) measures that.

## 6. How to replace estimates with evidence (cheapest first)
1. **Row 12 — compile the DE10-Nano GHRD** in Quartus 25.1std (no board needed): MEASURED ALM / M10K of the
   HPS system shell and its interconnect.
2. **Row 4 — a cited reference** for an iterative Keccak-f[1600] on Cyclone V (add to `references.md`), and
   later the Phase 7 K0 compile itself.
3. **Rows 10 / 10′ — decide early that operation-level storage is M10K-based** (Phase 6/9 design input),
   and check whether part of the NTT working memory can be M10K.
4. **Rows 7–9 — a block-level sketch** of the Phase 9 datapath (bus width, which units are shared) to narrow
   the 500–2,000 ranges.
5. Re-run this table after each of the above; keep each row's label honest (ESTIMATE → MEASURED).
