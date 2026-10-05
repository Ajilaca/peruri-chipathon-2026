## 9M-1 core, C5 hash (`HASH_C5 = 1`, `CODEC_W2 = 1`) at 40.000 ns, seeds 1-6 (MEASURED, kernel-only, virtual pins)
| Revision | ALM | Registers | RAM blocks | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Critical warnings | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| MW | 17,672 | 8233 | 54 | 28 | 20.825 / 0.116 | yes | 52.15 | 1 | `evidence/phase9m/batch1/9m1/quartus_MW.md` |
| MW-s2 | 17,641 | 8299 | 54 | 28 | 20.048 / 0.111 | yes | 50.12 | 1 | `evidence/phase9m/batch1/9m1/quartus_MW-s2.md` |
| MW-s3 | 17,644 | 8320 | 54 | 28 | 19.558 / 0.123 | yes | 48.92 | 1 | `evidence/phase9m/batch1/9m1/quartus_MW-s3.md` |
| MW-s4 | 17,655 | 8189 | 54 | 28 | 18.957 / 0.083 | yes | 47.52 | 1 | `evidence/phase9m/batch1/9m1/quartus_MW-s4.md` |
| MW-s5 | 17,683 | 8250 | 54 | 28 | 18.655 / 0.077 | yes | 46.85 | 1 | `evidence/phase9m/batch1/9m1/quartus_MW-s5.md` |
| MW-s6 | 17,653 | 8376 | 54 | 28 | 19.504 / 0.114 | yes | 48.79 | 1 | `evidence/phase9m/batch1/9m1/quartus_MW-s6.md` |

ALM median (min-max) 17,654.0 (17,641-17,683); registers 8189-8376; RAM blocks 54-54; DSP 28-28
Worst setup slack over seeds 18.655 ns; Fmax lowest slow corner median (min-max) 48.855 (46.85-52.15) MHz
**Timing met at 40.000 ns at 6 of 6 seeds**

Latency at the median Fmax of this table (perhitungan tim; profile-input cycles):
KeyGen 8,327 cycles = 170.4 us; Encaps 10,159 = 207.9 us; Decaps 15,515 = 317.6 us

Information, MW-20 (seed 1, 20.000 ns): ALM 17,808; worst setup / hold 4.355 / 0.081 ns; Fmax lowest slow corner 63.92 MHz; `evidence/phase9m/batch1/9m1/quartus_MW-20.md`

## 9M-1 core, K0 hash (`HASH_C5 = 0`, `CODEC_W2 = 1`) at 40.000 ns, seeds 1-6 (MEASURED, kernel-only, virtual pins)
| Revision | ALM | Registers | RAM blocks | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Critical warnings | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| MK | 15,923 | 8249 | 54 | 28 | 19.069 / 0.080 | yes | 47.78 | 1 | `evidence/phase9m/batch1/9m3/quartus_MK.md` |
| MK-s2 | 15,899 | 8230 | 54 | 28 | 19.555 / 0.100 | yes | 48.91 | 1 | `evidence/phase9m/batch1/9m3/quartus_MK-s2.md` |
| MK-s3 | 15,911 | 8266 | 54 | 28 | 19.727 / 0.110 | yes | 49.33 | 1 | `evidence/phase9m/batch1/9m3/quartus_MK-s3.md` |
| MK-s4 | 15,912 | 8261 | 54 | 28 | 19.754 / 0.107 | yes | 49.39 | 1 | `evidence/phase9m/batch1/9m3/quartus_MK-s4.md` |
| MK-s5 | 15,926 | 8263 | 54 | 28 | 18.934 / 0.132 | yes | 47.47 | 1 | `evidence/phase9m/batch1/9m3/quartus_MK-s5.md` |
| MK-s6 | 15,940 | 8382 | 54 | 28 | 19.577 / 0.117 | yes | 48.96 | 1 | `evidence/phase9m/batch1/9m3/quartus_MK-s6.md` |

ALM median (min-max) 15,917.5 (15,899-15,940); registers 8230-8382; RAM blocks 54-54; DSP 28-28
Worst setup slack over seeds 18.934 ns; Fmax lowest slow corner median (min-max) 48.935 (47.47-49.39) MHz
**Timing met at 40.000 ns at 6 of 6 seeds**

Latency at the median Fmax of this table (perhitungan tim; profile-input cycles):
KeyGen 8,447 cycles = 172.6 us; Encaps 10,279 = 210.1 us; Decaps 15,635 = 319.5 us

Information, MK-20 (seed 1, 20.000 ns): ALM 16,007; worst setup / hold 4.003 / 0.067 ns; Fmax lowest slow corner 62.51 MHz; `evidence/phase9m/batch1/9m3/quartus_MK-20.md`

### Rule (test plan section 5), items 2-4 (items 1 = tests, see result_9m3.md)
- 2. timing met at 40.000 ns at every seed: met (6 of 6)
- 3. ALM median MW - MK = 1,736.5 (needs >= 1,500): met
- 4. latency of MK relative to MW (cycles / median Fmax): KeyGen +1.28 %, Encaps +1.02 %, Decaps +0.61 % (needs <= +2 % each): met
