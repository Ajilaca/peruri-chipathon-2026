<!-- claim-lint: skip-file (internal checkpoint record, not proposal text) -->
# Phase 5M S7 checkpoint: memory read path split (revision S7) vs M6

Plan and rule: `evidence/phase05m/test_plan_s7.md` (fixed before RTL and measurements). Record: ADR 0021 (Proposed).

| Quantity | M6 (MEASURED) | S7 (MEASURED) | Delta (INFERENCE) |
|---|---:|---:|---:|
| ALM, median of seeds 1-6 (min-max) | 9,421.5 (9,394-9,441) | 9,391.0 (9,361-9,405) | -30.5 |
| Registers (min-max) | about 4,030-4,080 | 4,296-4,324 | about +260 |
| DSP / M10K | 16 / 29 | 16 / 31 | 0 / +2 |
| Fmax median, lowest slow corner (MHz) | 34.430 (32.35-35.04) | 38.720 (37.89-40.29) | +4.290 (+12.5 %) |
| NTT / INTT cycles (simulation) | 119 / 119 | 120 / 120 | +1 / +1 |
| t_NTT / t_INTT at median Fmax (us, perhitungan tim) | 3.456 / 3.456 | 3.099 / 3.099 | -0.357 / -0.357 |
| Timing met at 40.000 ns, every seed | yes | yes | - |

Verification (MEASURED): lint and slang clean; memory unit tests (RD_SPLIT = 1 and 0) 8/8 and the differential test against the frozen memory 1/1 on both simulators; core 6/6 (NTT, INTT,
round trip, boundary data, constant cycles 120 / 120, 512 INTT unit vectors); NCD and NCS fail as required; formal H, O, R, A, B, C PASS with NC-O and NC-A failing (3/3). V7 (regression) not run
for S7, Amendment A1.

Rule result: **adopted by the rule** (all four conditions PASS, no tolerance). Team acceptance: ADR 0021 Proposed. S8 started on this base.
