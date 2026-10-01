# ADR 0014: Phase 5c: lazy INTT butterfly inputs, operand contract D6 amended, adoption rule

- Status: Accepted
- Date: 2026-10-01
- Decided by: Faza Dzil, Team J5 (session 2026-10-01: scope option (b); adoption rule as instructed for 5c)

## Context
- 5c (optional, `docs/ROADMAP.md`): lazy reduction, only with proven value bounds. ADR 0011 D3 deferred the decision to
  attempt it until after 5a/5b; the team asked for it on 2026-10-01 with the goal of taking `sub_mod` off the critical
  segment.
- Pre-check (`docs/evidence/phase05-arith/5c/precheck_critical_path_2026-10-01.md`, MEASURED on C4b-B seed 1): the worst
  path is memory read (21.03 ns) → `sub_mod(b, a)` (4.22 ns) → DSP (3.59 ns), slack +11.044 ns; the next path class is
  memory read → `add_mod(a, b)` (3.96 ns) → side delay line, slack +12.102 ns. Removing only `sub_mod` would leave an
  Fmax cap near 35.8 MHz (INFERENCE, one seed).
- ADR 0011 D6 (operand contract): every reducer must equal (a·b) mod q for a, b in [0, q).
- Base configuration: C4b-B (Barrett, ADR 0013 Proposed; the team continued on it).

## Options considered
(a) lazy multiplier input only (`b + q − a`); (b) both INTT butterfly inputs lazy. See the pre-check for the costs.

## Decision
1. **Scope (b).** In INTT mode the butterfly feeds the multiplier with `u = b + q − a` (exact, in [1, 2q), 13 bits)
   instead of `sub_mod(b, a)`, and carries the side operand `s = a + b` (exact, in [0, 2q), 13 bits) instead of
   `add_mod(a, b)`; `s` is reduced once at the butterfly output (one conditional subtraction, in the write segment).
   NTT mode is unchanged. Memory, schedule, L, P = 6 and the register positions of C4b-B stay as they are.
2. **Operand contract D6, amended for the C4c lane multiplier only:** the Barrett reducer used there must equal
   (z·u) mod q for every z in [0, q) and every u in [0, 2q) (exhaustive, 22,164,482 pairs). The scaling multiplier and
   every other use keep the D6 contract [0, q) × [0, q). Results stay bit-exact with FIPS 203 (`tb/golden`).
3. **Value bounds proven formally** (SymbiYosys) on the lazy input / output logic: u < 2q, s < 2q, (u mod q) =
   (b − a) mod q, butterfly outputs < q and equal to the reference equations, no signal wider than its declaration;
   with a negative control.
4. **Adoption rule (fixed before measuring).** C4c (lazy, revision `C4c`, seeds 1–6, 40.000 ns, Quartus defaults) is
   adopted as the C4 configuration only if **all** hold:
   - correct (test plan V1–V8 incl. the 5c items, both simulators) and the formal bound proof PASS with its negative
     control failing;
   - NTT / INTT cycles constant and exactly 119 / 375;
   - ALM ≤ 12,573 at every seed;
   - timing met at 40.000 ns at every seed;
   - median over seeds 1–6 of the lowest slow-corner Fmax **above 34.84 MHz** (the top of Barrett's 5b seed range,
     `docs/evidence/phase05-arith/5b/selection_worksheet_2026-10-01.md`);
   - ADR 0012: t_NTT and t_INTT at that median Fmax **better** than Barrett 5b at its median Fmax (34.515 MHz):
     t_NTT < 3.448 µs and t_INTT < 10.865 µs (119 / 34.515 and 375 / 34.515, perhitungan tim).
   If any condition fails, C4c is reported as measured and not adopted; C4b-B stays the C4 configuration.

## Consequences
- New files only (`rtl/arith/` Barrett variant with a 13-bit lazy operand, lazy butterfly, I/O logic for the formal
  proof; a `ntt_core_c4` parameter that defaults to the current behaviour; wrapper `ntt_core_c4c.sv`); C4a / C4b-B /
  C4b-M must still pass unchanged after the core change.
- The side delay line widens from 12 to 13 bits per lane (registers / M10K bits may rise; measured).
- Six Quartus compiles (seeds 1–6), one at a time.

## Evidence
- `docs/evidence/phase05-arith/5c/precheck_critical_path_2026-10-01.md`
- `docs/evidence/phase05-arith/5b/selection_worksheet_2026-10-01.md`
- `docs/decisions/0011-*.md` (D3, D6), `0012-*.md`, `0013-*.md`

## Outcome (added 2026-10-01 after the sweep; the decision above is unchanged)
- The adoption rule was applied unchanged to seeds 1-6 (`docs/evidence/phase05-arith/5c/selection_worksheet_2026-10-01.md`).
  Median Fmax 33.100 MHz (rule: above 34.84 MHz); t_NTT 3.595 us and t_INTT 11.329 us (rule: below 3.448 / 10.865 us).
  Correctness, 119 / 375 cycles, ALM and timing at 40 ns passed. C4c is **not adopted**; C4b-B stays the C4 configuration.
- The D6 amendment ([0, 2q) second operand) applies **only to the C4c experiment** (`modmul_barrett_lazy.sv`,
  `ntt_core_c4c.sv`). The C4 configuration keeps the D6 contract [0, q) x [0, q).
- The pre-RTL baseline path check required by the 5c instruction is recorded in
  `docs/evidence/phase05-arith/5c/precheck_critical_path_2026-10-01.md` (measured before any 5c RTL was written).
- No seed was added and the rule was not changed after measuring.
