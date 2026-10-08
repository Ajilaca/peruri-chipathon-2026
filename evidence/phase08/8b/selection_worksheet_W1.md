## W1: per seed pada 40,000 ns (MEASURED)
| Seed | ALM | Register | M10K | DSP | Setup / hold terburuk (ns) | Timing terpenuhi @ 40 ns | Fmax slow corner terendah (MHz) | Evidence |
|---|---|---|---|---|---|---|---|---|
| 1 | 5,276 | 1913 | 0 | 0 | 20.399 / 0.161 | ya | 51.02 | `quartus_SM1.md` |
| 2 | 5,271 | 1913 | 0 | 0 | 20.470 / 0.162 | ya | 51.20 | `quartus_SM1-s2.md` |
| 3 | 5,298 | 1913 | 0 | 0 | 20.789 / 0.162 | ya | 52.05 | `quartus_SM1-s3.md` |
| 4 | 5,311 | 1913 | 0 | 0 | 20.038 / 0.163 | ya | 50.10 | `quartus_SM1-s4.md` |
| 5 | 5,282 | 1913 | 0 | 0 | 20.484 / 0.162 | ya | 51.24 | `quartus_SM1-s5.md` |
| 6 | 5,273 | 1913 | 0 | 0 | 22.075 / 0.161 | ya | 55.79 | `quartus_SM1-s6.md` |

Median ALM (min-maks): 5,279.0 (5,271-5,311); register 1913-1913; median Fmax (min-maks): 51.220 (50.10-55.79) MHz

### Gerbang penerimaan W1 (test plan bagian 4)
- PASS: benar (verification_status: V1-V10, kedua simulator, kontrol gagal, formal, regresi)
- PASS: M10K = 0 dan DSP = 0 di setiap seed
- PASS: ALM <= 12,573 di setiap seed (batas kerja)
- PASS: timing terpenuhi pada 40,000 ns di setiap seed
- PASS: median Fmax 51.220 MHz >= median S10 44.320 MHz

Hasil gerbang W1: LOLOS.

Siklus (top C5, `cycles_w1_c5.json`; coef_ready selalu tinggi): SampleNTT rata-rata 305.23 siklus pada 500 polinomial; CBD [280] siklus.

- informasi SM1-20 (20,000 ns), seed 1: ALM 5,296, setup terburuk 3.892 ns (terpenuhi), Fmax slow corner terendah 62.08 MHz, `quartus_SM1-20.md`
- informasi SM1-K0 (sponge K0), seed 1: ALM 3,470, setup terburuk 23.928 ns (terpenuhi), Fmax slow corner terendah 62.22 MHz, `quartus_SM1-K0.md`

## W2: tidak diukur (tidak ada file evidence)

Acuan: median Fmax S10 (inti NTT/INTT) 44.320 MHz pada seed 1-6 (dihitung ulang dari `evidence/phase06/s10/`).

## Pemilihan W1 lawan W2 (test plan bagian 5)
- W2 belum diukur. Gerbang W1: lolos.
