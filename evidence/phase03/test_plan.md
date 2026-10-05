# Phase 3 test plan - multi-lane exploration L = 1/2/4/8 (C2), written before any RTL is coded (CRG-4)

Scope: new RTL only - `rtl/ntt/ntt_core_c2.sv` (parameterized `#(.NUM_LANES(L))`), instantiating
`L` copies of `rtl/ntt/butterfly.sv` and `rtl/ntt/twiddle_rom.sv`, driving
`rtl/mem/poly_mem_banked.sv #(.NUM_BANKS(L))`'s multi-bank crossbar (built in Phase 2, address-
proven but never exercised by a datapath - see `rtl/mem/poly_mem_banked.sv` header). No other
module changes: `rtl/ntt/ntt_core.sv` (C0) and `rtl/mem/ntt_core_c1.sv` (C1) stay frozen.
Reference: `tb/golden/primitives.py` (`ntt`, `intt`), `tb/mem/bank_model.py` (bank/offset scheme,
`lane_p`, and the two functions added for this phase: `zeta_index_of`, `reference_zeta_trace`).
Lane-count selection criterion: `docs/decisions/adr/ADR-0004-phase-3-lane-count-l-selection-criterion.md`
(ADR 0004, Accepted) - primary: min cycle count within a 10,478 ALM (25%) budget; secondary:
informational AT re-check once a timing-valid clock exists. No RTL below was written before this
plan.

## Architecture note: per-lane zeta index (verified before RTL, not assumed)

`ntt_core.sv`'s (C0) zeta index is one sequential counter, incremented once per finished block,
shared across the whole core - that does not generalise to `L` lanes advancing through different
blocks in the same cycle. Phase 3 instead gives each lane a **closed-form** zeta index,
`bank_model.zeta_index_of(layer, mode_inv, block)`:

- NTT (forward): `k = 2^layer + block`.
- INTT (inverse): `k = 127 - (blocks completed in earlier layers) - block`.

This was cross-checked against `bank_model.reference_zeta_trace` - a restatement of C0's own
sequential update rule (Phase 1 CRG-7/CRG-8, already proven bit-exact/cycle-exact) - for all 127
`(layer, block)` pairs, both directions: **0 mismatches**
(`evidence/phase03/lane_schedule_verification.txt`,
`scripts/build/gen_lane_schedule.py`). The same script also confirms, for every `L ∈ {1,2,4,8}`, every
mode, every layer: the `L` lanes active at each sub-cycle `t` (`bank_model.lane_p`) cover all 128
butterfly indices `p` of that layer exactly once - no duplicate, no gap.

RTL implication: each lane computes `(j, jlen, zeta)` purely combinationally from
`(layer_q, lane_id, t_q)`, with no lane-to-lane dependency and no shared running zeta counter -
this is what makes `L` a synthesis-time parameter rather than a control rewrite per `L`.

## Unit: ntt_core_c2 lane datapath, all four L instances

- Corner cases (same 6 as Phase 1's `ntt_core` test plan, run through every `L`): all-zero
  polynomial; all coefficients = q-1; impulse at coefficient 0; impulse at coefficient 255;
  alternating 0/q-1.
- Bit-exact, cross-checked against `tb/golden/primitives.py`:
  - `ntt(f)` and `intt(f)` match for every corner case + 100 random polynomials, for each `L`.
  - `intt(ntt(f)) == f`, 50 random polynomials, for each `L`.
- **Cycle count (CRG-7), measured per L, not assumed equal to C0/C1.** Unlike Phase 2 (L=1
  banking only, required cycle-identical to C0), Phase 3's `L>1` datapaths are expected to take
  fewer cycles (`128/L` sub-cycles per layer instead of 128) - this is the quantity Phase 3
  exists to measure. Requirement: constant cycle count *within* a given `L` (no data-dependent
  stall - same constant-cycle argument as CRG-7, now checked per `L`), and the measured NTT/INTT
  cycle counts for all four `L` recorded in `docs/results/phase03.md`'s comparison table.
- Stall cycles = 0 for every `L` (Phase 3 PASS criterion): no cycle spent waiting on a bank
  conflict, since the schedule above is conflict-free by the Phase 2 proof
  (`evidence/phase02/bank_scheme_exploration.txt`) applied per-`L`.
- Run twice: Icarus and Verilator (CRG-3), for every `L`.

## Formal (CRG-8, SymbiYosys), per L

- Re-run Phase 1/2's FSM safety properties (`busy_o`/`done_o` handshake; `done_o` asserted
  exactly one cycle) against `ntt_core_c2` at each `L`.
- Address range: every address driven into `poly_mem_banked` (per-lane `j`, `jlen`, and the
  scan address for the INTT scaling pass) stays in `[0, 255]` for every reachable state, for
  every `L` - re-proves Phase 2's own-pair/range properties still hold once the multi-bank
  crossbar is actually driven by `L>1` lanes concurrently (not just addressed one port at a time
  as in C1).

## Quartus: one revision per L (CRG-9/CRG-10 evidence)

- `quartus/phase03_multilane_c2/` - four revisions, `C2-L1`, `C2-L2`, `C2-L4`, `C2-L8`, identical
  constraints and seed to C0/C1 (`evidence/quartus/C0.md`,
  `evidence/quartus/C1.md`).
- Recorded per `L`: ALM, registers, M10K, DSP, Fmax (worst corner), worst setup/hold slack,
  measured NTT/INTT cycle counts, and whether `L` is in-budget (≤ 10,478 ALM, ADR 0004).
- The M10K situation inherited from Phase 2 (0/553, async-read limitation,
  `docs/results/phase02.md` §"Temuan Jujur") is expected to persist or worsen with `L>1`
  banks; report it as-is per `L`, do not treat it as a Phase 3 regression to hide.

## L-selection application (ADR 0004)

`docs/results/phase03.md` must show, in order: (1) the four `L` values with their measured
ALM vs the 10,478 budget - pass/fail; (2) cycle counts for the in-budget candidates; (3) the
selected `L` (lowest cycle count among in-budget candidates); (4) once any later phase produces a
timing-valid clock, the secondary informational AT re-check - explicitly marked as not
overriding the primary selection without a follow-up ADR.

## Explicitly out of scope for Phase 3 (see docs/ROADMAP.md "Not allowed yet")

`L > 8`; butterfly pipelining or arithmetic changes (Barrett/Montgomery, lazy reduction -
Phase 5); choosing `L` from anything other than the measured comparison table required above;
comparing against software or literature as if measured on the same platform; a target-clock ADR
(still open, `docs/decisions/PENDING.md`) - Phase 3's Fmax numbers remain relative-only until
that lands.
