## Per seed at 40.000 ns (MEASURED)
| Seed | ALM | Registers | Block memory bits | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Critical warnings | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 298 | 192 | 0 | 2 | 30.143 / 0.168 | yes | 101.45 | 1 | `quartus_CD.md` |
| 2 | 299 | 192 | 0 | 2 | 30.046 / 0.167 | yes | 100.46 | 1 | `quartus_CD-s2.md` |
| 3 | 299 | 193 | 0 | 2 | 30.940 / 0.166 | yes | 110.38 | 1 | `quartus_CD-s3.md` |
| 4 | 299 | 192 | 0 | 2 | 30.624 / 0.167 | yes | 106.66 | 1 | `quartus_CD-s4.md` |
| 5 | 299 | 192 | 0 | 2 | 30.716 / 0.167 | yes | 107.71 | 1 | `quartus_CD-s5.md` |
| 6 | 299 | 192 | 0 | 2 | 30.440 / 0.167 | yes | 104.60 | 1 | `quartus_CD-s6.md` |

ALM median (min-max): 299.0 (298-299); registers 192-193; DSP 2-2; Fmax median (min-max): 105.630 (100.46-110.38) MHz

### Pass rule (test plan section 5, items 2 and 3)
- PASS: the fit succeeded at every seed
- PASS: timing met at 40.000 ns at every seed (worst setup and hold slack of all corners non-negative)
- reported as MEASURED: resource counts and Fmax (median of the lowest slow-corner Fmax over seeds 1-6) above; DSP is reported and not limited

- information CD-20 (20.000 ns), seed 1: ALM 298, worst setup 10.952 ns (met), Fmax lowest slow corner 110.52 MHz, `quartus_CD-20.md`

## Cycles per polynomial (MEASURED in simulation, always-ready sink, no input gaps; identical for every data value of one d: test V7)
| d | pack, Icarus | pack, Verilator | unpack, Icarus | unpack, Verilator |
|---|---|---|---|---|
| 1 | 261 | 261 | 259 | 259 |
| 4 | 261 | 261 | 259 | 259 |
| 10 | 325 | 325 | 323 | 323 |
| 12 | 389 | 389 | 387 | 387 |
