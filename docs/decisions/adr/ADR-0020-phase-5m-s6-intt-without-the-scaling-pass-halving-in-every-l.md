# ADR 0020: Phase 5M S6: INTT without the scaling pass (halving in every layer), measured result and adoption verdict

- Status: Accepted
- Date: 2026-10-02
- Decided by: Jevan, Team J5 (chat 2026-10-02: "gunakan M6 karena nantinya kita akan mengambil s7 dan s8 kemudian kita masuk ke fase selanjutnya")

## Context
- ADR 0017 (Accepted) step S6; test plan and adoption rule written before RTL and before measuring
  (`evidence/phase05m/test_plan.md`, commit f47efcc); base C4b-B (ADR 0013 Accepted).
- ADR 0019 first reduced Phase 5M to S6 *(edited 2026-10-03 at the team's request: S7, S8 and S9 were later done, see ADR 0019 amendment note 3; the original text said "S7-S9 are not done before the 2026-10-08 deadline")*.

## Options considered
(a) Adopt M6 as the INTT design (INTT 375 -> 119 cycles, 16 DSP, about +250 ALM, NTT Fmax unchanged within seed noise): the pre-fixed rule says
    not adopted (the NTT part of ADR 0012 fails by 0.008 us); adopting needs a team decision that changes the rule.
(b) Report M6 as measured, not adopted by the rule; C4b-B stays the NTT/INTT configuration for the deadline scope.
(c) Team decides a different rule for this case (for example "t_NTT must not be worse than the seed spread"). Not made by the assistant.

## Decision
M6 is adopted as the base for S7 and S8 by decision of the team (Jevan, 2026-10-02), option (c) of the list above. The pre-fixed rule of the test
plan is not changed and its result stays on record as measured: M6 is not adopted by the rule (only the NTT part of ADR 0012 failed, t_NTT
3.456 us vs 3.448 us, a 0.25 % median-Fmax difference inside the seed spread). The team's reason: S7 and S8 follow on this base, and INTT drops from
375 to 119 cycles. Consequences of the team's choice, stated so they are not forgotten:
- the NTT/INTT configuration from now on is M6 (revision `M6`, `rtl/ntt/ntt_core_m6_p6.sv`), 16 DSP, about 250 more ALM than C4b-B, INTT = NTT = 119 cycles;
- the ADR 0012 comparison of S7 is against M6's median Fmax (34.430 MHz; t_NTT = t_INTT = 3.456 us), not against C4b-B;
- ADR 0013 (Barrett) is unchanged.

## Equivalence argument (the mathematics is not changed, C1)
1. q = 3329 is odd, so 2^-1 exists: 2 * 1665 = 3330 = 1 (mod q). For x in [0, q): x/2 mod q = x/2 (x even) or (x + q)/2 (x odd), both < q;
   `half_mod` computes exactly this and was checked for all 3,329 inputs (RTL, both simulators) and against the golden function.
2. zeta * (b - a) / 2 = (zeta * 1665 mod q) * (b - a) (mod q): the b output of the halved butterfly is the standard b output times 2^-1; the a
   output is the standard a output times 2^-1 by (1).
3. A halved layer = the standard layer times the scalar 2^-1. Seven layers give 2^-7 times the unscaled INTT; 128 * 3303 = 127 * 3329 + 1, so
   2^-7 = 3303 (mod q), which is exactly the final multiplication of FIPS 203 Algorithm 10 line 14. Hence the result equals Algorithm 10 for all inputs
   in [0, q)^256.
4. Checked, not assumed: golden `intt_halving()` equals `intt()` on 256 unit vectors, 256 (q-1)-unit vectors, edge vectors and 1,000 random vectors;
   the RTL INTT equals both golden models on the 512 unit vectors and on 100 random + corner polynomials; three negative controls (golden layer
   dropped, RTL `half_mod` bypass, RTL ROM entries of one layer not halved) fail as required.

## Consequences
- Measured (MEASURED, Quartus, seeds 1-6, 40.000 ns; `evidence/phase05m/s6/selection_worksheet.md`): ALM 9,394-9,441 (C4b-B
  9,166-9,208), registers about 4,030-4,080, M10K 29, DSP 16 (C4b-B 18), Fmax median 34.430 MHz (C4b-B 34.515), timing met at every seed, NTT / INTT cycles
  119 / 119 (C4b-B 119 / 375, simulation). t_NTT 3.456 us (C4b-B 3.448), t_INTT 3.456 us (C4b-B 10.865) at the median Fmax (perhitungan tim).
- The Fmax ranges overlap (M6 32.35-35.04 vs C4b-B 33.46-34.84 MHz), so the 0.25 % median difference is not distinguishable from seed noise (INFERENCE).
- ALM rose by about 250 (INFERENCE: the INTT twiddle table doubles the ROM per lane and eight `half_mod` units were added, offset by the removed scaling
  reducer; not decomposed per entity).
- Full Phase 0-5 regression (V9) was not run for S6 (Amendment A1; no existing file was modified). The 5M branch carries the code; if the team later wants
  the INTT cycle gain (a standalone INTT of 119 instead of 375 cycles), this record is where to start.
- Not covered: hardware, other seeds or constraints, path analysis of the NTT Fmax.

## Evidence
- `evidence/phase05m/test_plan.md` (rule, Amendment A1), `s6/verify.md`, `s6/formal.md`,
  `s6/verification_status.json`, `s6/selection_worksheet.md`, `s6/quartus_M6[-s2..s6].md`
