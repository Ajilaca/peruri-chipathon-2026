## Per seed at 40.000 ns (MEASURED), revision MW (CODEC_W2 = 1)
| Seed | ALM | Registers | RAM blocks | Block memory bits | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Critical warnings | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 17,672 | 8233 | 54 | 120,350 | 28 | 20.825 / 0.116 | yes | 52.15 | 1 | `quartus_MW.md` |
| 2 | 17,641 | 8299 | 54 | 120,350 | 28 | 20.048 / 0.111 | yes | 50.12 | 1 | `quartus_MW-s2.md` |
| 3 | 17,644 | 8320 | 54 | 120,350 | 28 | 19.558 / 0.123 | yes | 48.92 | 1 | `quartus_MW-s3.md` |
| 4 | 17,655 | 8189 | 54 | 120,350 | 28 | 18.957 / 0.083 | yes | 47.52 | 1 | `quartus_MW-s4.md` |
| 5 | 17,683 | 8250 | 54 | 120,350 | 28 | 18.655 / 0.077 | yes | 46.85 | 1 | `quartus_MW-s5.md` |
| 6 | 17,653 | 8376 | 54 | 120,350 | 28 | 19.504 / 0.114 | yes | 48.79 | 1 | `quartus_MW-s6.md` |

MW: ALM median (min-max) 17,654.0 (17,641-17,683); registers 8189-8376; RAM blocks 54-54; DSP 28-28; Fmax median (min-max) 48.855 (46.85-52.15) MHz
Phase 9c baseline MC (`evidence/phase09/9c/`): ALM median 17,620.5 (17,608-17,636); registers 8210-8365; RAM blocks 54-54; Fmax median 49.280 (47.64-51.74) MHz
Difference MW - MC: ALM +33.5, Fmax -0.425 MHz
Information MW-20 (20.000 ns), seed 1: ALM 17,808, registers 8487, worst setup 4.355 ns (met), Fmax lowest slow corner 63.92 MHz (`quartus_MW-20.md`)

## Cycles and time (profile inputs, MEASURED in simulation; t = cycles / median Fmax is INFERENCE / perhitungan tim, kernel-only static timing, not a board measurement)
| Operation | Phase 9 cycles | 9M-1 cycles | Change | t Phase 9 (us) at median Fmax of MC | t 9M-1 (us) at median Fmax of MW | Lower? |
|---|---|---|---|---|---|---|
| KeyGen | 9,095 | 8,327 | -8.4 % | 184.6 | 170.4 | yes |
| Encaps | 10,735 | 10,159 | -5.4 % | 217.8 | 207.9 | yes |
| Decaps | 16,667 | 15,515 | -6.9 % | 338.2 | 317.6 | yes |

### Numeric items of the adoption rule (test plan section 6)
- PASS: item 2, timing met at 40.000 ns at every seed 1-6
- PASS: item 3, t of KeyGen, Encaps and Decaps lower than Phase 9 (table above)
- PASS: item 4, ALM median of MW at most 1,000 above the Phase 9 median (+33.5)
- items 1 (V1-V3, V5-V7) are the logs listed in `result_9m1.md`
