<!-- claim-lint: skip-file (generated worksheet) -->
# ADR 0007 rule with the ADR 0009 budget (30% = 12,573 ALM) — generated 2026-10-01

Command: `python3 scripts/phase4_select_p.py --alm-budget 12573` and `python3 scripts/phase4_seed_sweep_summary.py --alm-budget 12573`. Inputs are the unchanged MEASURED evidence files listed below; the historical 25% worksheet is `selection_worksheet_2026-09-30.md`.

## Default seed (all four P)

ALM budget used for condition 3: 12,573

| P | bit-exact | constant cycle | ALM | ≤ 12,573? | worst setup / hold slack @ 40.000 ns | timing met? | cycles_NTT | cycles_INTT | Fmax per slow corner (MHz) | Fmax(P) = lowest | t_NTT (µs) | t_INTT (µs) | candidate? | d(P) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | PASS | PASS | 9,723 / 41,910 | yes | -90.653 / 0.207 | no | 113 | 369 | Slow 1100mV 100C: 7.65; Slow 1100mV -40C: 7.68 | 7.65 | 14.771 | 48.235 | no | — |
| 2 | PASS | PASS | 9,696 / 41,910 | yes | -0.368 / 0.174 | no | 115 | 371 | Slow 1100mV 100C: 25.04; Slow 1100mV -40C: 24.77 | 24.77 | 4.643 | 14.978 | no | — |
| 4 | PASS | PASS | 10,439 / 41,910 | yes | 8.734 / 0.157 | yes | 117 | 373 | Slow 1100mV 100C: 32.60; Slow 1100mV -40C: 31.98 | 31.98 | 3.659 | 11.664 | yes | 0.0511 |
| 6 | PASS | PASS | 10,505 / 41,910 | yes | 10.753 / 0.140 | yes | 119 | 375 | Slow 1100mV 100C: 34.19; Slow 1100mV -40C: 34.50 | 34.19 | 3.481 | 10.968 | yes | 0.0000 |

Other resources (MEASURED): P=0: registers 3097, DSP 9 / 112, RAM blocks 0 / 553; P=2: registers 3817, DSP 9 / 112, RAM blocks 16 / 553; P=4: registers 4145, DSP 9 / 112, RAM blocks 26 / 553; P=6: registers 4168, DSP 9 / 112, RAM blocks 29 / 553
Evidence files: quartus_C3-P0_20260930.md, quartus_C3-P2_20260930.md, quartus_C3-P4_20260930.md, quartus_C3-P6_20260930.md, verification_status.json

Candidate set C = {4, 6}
t_min = 3.480550 us; within 5% of t_min: {6}
RESULT: P_selected = 6 (smallest candidate with d(P) <= 0.05). To be recorded in a new ADR by the team.

## Seeds 1–6 (P = 4 and P = 6)

ALM budget: 12,573

| P | Seed | ALM | <= 12,573? | Registers | M10K | Worst setup / hold slack (ns) | Timing met? | Fmax(P) lowest slow corner (MHz) | t_NTT (us) | Meets all ADR 0007 conditions? | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 1 (default) | 10,439 | yes | 4145 | 26 / 553 | 8.734 / 0.157 | yes | 31.98 | 3.659 | yes | `docs/evidence/phase04-pipeline/quartus_C3-P4_20260930.md` |
| 4 | 2 | 10,503 | yes | 4160 | 26 / 553 | 9.482 / 0.143 | yes | 32.77 | 3.570 | yes | `docs/evidence/phase04-pipeline/seed_sweep/quartus_C3-P4-s2_20261001.md` |
| 4 | 3 | 10,479 | yes | 4151 | 26 / 553 | 7.324 / 0.129 | yes | 30.60 | 3.824 | yes | `docs/evidence/phase04-pipeline/seed_sweep/quartus_C3-P4-s3_20261001.md` |
| 4 | 4 | 10,472 | yes | 4166 | 26 / 553 | 8.555 / 0.120 | yes | 31.80 | 3.679 | yes | `docs/evidence/phase04-pipeline/seed_sweep/quartus_C3-P4-s4_20261001.md` |
| 4 | 5 | 10,467 | yes | 4160 | 26 / 553 | 7.580 / 0.118 | yes | 30.85 | 3.793 | yes | `docs/evidence/phase04-pipeline/seed_sweep/quartus_C3-P4-s5_20261001.md` |
| 4 | 6 | 10,468 | yes | 4149 | 26 / 553 | 9.701 / 0.130 | yes | 33.00 | 3.545 | yes | `docs/evidence/phase04-pipeline/seed_sweep/quartus_C3-P4-s6_20261001.md` |
| 6 | 1 (default) | 10,505 | yes | 4168 | 29 / 553 | 10.753 / 0.140 | yes | 34.19 | 3.481 | yes | `docs/evidence/phase04-pipeline/quartus_C3-P6_20260930.md` |
| 6 | 2 | 10,508 | yes | 4153 | 29 / 553 | 9.773 / 0.139 | yes | 33.08 | 3.597 | yes | `docs/evidence/phase04-pipeline/seed_sweep/quartus_C3-P6-s2_20261001.md` |
| 6 | 3 | 10,511 | yes | 4160 | 29 / 553 | 9.328 / 0.132 | yes | 32.60 | 3.650 | yes | `docs/evidence/phase04-pipeline/seed_sweep/quartus_C3-P6-s3_20261001.md` |
| 6 | 4 | 10,516 | yes | 4152 | 29 / 553 | 10.756 / 0.128 | yes | 34.20 | 3.480 | yes | `docs/evidence/phase04-pipeline/seed_sweep/quartus_C3-P6-s4_20261001.md` |
| 6 | 5 | 10,504 | yes | 4139 | 29 / 553 | 9.824 / 0.144 | yes | 33.14 | 3.591 | yes | `docs/evidence/phase04-pipeline/seed_sweep/quartus_C3-P6-s5_20261001.md` |
| 6 | 6 | 10,484 | yes | 4162 | 29 / 553 | 9.764 / 0.131 | yes | 33.07 | 3.598 | yes | `docs/evidence/phase04-pipeline/seed_sweep/quartus_C3-P6-s6_20261001.md` |

| P | ALM min / median / max | Seeds within 12,573 | Fmax min / median / max (MHz) | Seeds meeting all ADR 0007 conditions |
|---|---|---|---|---|
| 4 | 10,439 / 10,470.0 / 10,503 | 6 of 6 | 30.60 / 31.89 / 33.00 | 6 of 6 |
| 6 | 10,484 / 10,506.5 / 10,516 | 6 of 6 | 32.60 / 33.11 / 34.20 | 6 of 6 |

Per seed, the ADR 0007 rule applied to {P=4, P=6} only (P=0 and P=2 were not swept; at the default seed both miss timing at 40.000 ns):

| Seed | Candidates among {4, 6} | Rule result |
|---|---|---|
| 1 | {4, 6} | P = 6 |
| 2 | {4, 6} | P = 4 |
| 3 | {4, 6} | P = 4 |
| 4 | {4, 6} | P = 6 |
| 5 | {4, 6} | P = 6 |
| 6 | {4, 6} | P = 4 |
