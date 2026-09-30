| P | bit-exact | constant cycle | ALM | ≤ 10,478? | worst setup / hold slack @ 40.000 ns | timing met? | cycles_NTT | cycles_INTT | Fmax per slow corner (MHz) | Fmax(P) = lowest | t_NTT (µs) | t_INTT (µs) | candidate? | d(P) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | PASS | PASS | 9,723 / 41,910 | yes | -90.653 / 0.207 | no | 113 | 369 | Slow 1100mV 100C: 7.65; Slow 1100mV -40C: 7.68 | 7.65 | 14.771 | 48.235 | no | — |
| 2 | PASS | PASS | 9,696 / 41,910 | yes | -0.368 / 0.174 | no | 115 | 371 | Slow 1100mV 100C: 25.04; Slow 1100mV -40C: 24.77 | 24.77 | 4.643 | 14.978 | no | — |
| 4 | PASS | PASS | 10,439 / 41,910 | yes | 8.734 / 0.157 | yes | 117 | 373 | Slow 1100mV 100C: 32.60; Slow 1100mV -40C: 31.98 | 31.98 | 3.659 | 11.664 | yes | 0.0000 |
| 6 | PASS | PASS | 10,505 / 41,910 | no | 10.753 / 0.140 | yes | 119 | 375 | Slow 1100mV 100C: 34.19; Slow 1100mV -40C: 34.50 | 34.19 | 3.481 | 10.968 | no | — |

Other resources (MEASURED): P=0: registers 3097, DSP 9 / 112, RAM blocks 0 / 553; P=2: registers 3817, DSP 9 / 112, RAM blocks 16 / 553; P=4: registers 4145, DSP 9 / 112, RAM blocks 26 / 553; P=6: registers 4168, DSP 9 / 112, RAM blocks 29 / 553
Evidence files: quartus_C3-P0_20260930.md, quartus_C3-P2_20260930.md, quartus_C3-P4_20260930.md, quartus_C3-P6_20260930.md, verification_status.json

Candidate set C = {4}
t_min = 3.658537 us; within 5% of t_min: {4}
RESULT: P_selected = 4 (smallest candidate with d(P) <= 0.05). To be recorded in a new ADR by the team.
