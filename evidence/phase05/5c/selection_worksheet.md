## Per seed, C4c (MEASURED)
| Seed | ALM | Register | M10K | DSP | Setup / hold terburuk (ns) | Timing terpenuhi @ 40 ns | Fmax slow corner terendah (MHz) | Evidence |
|---|---|---|---|---|---|---|---|---|
| 1 | 9,043 | 4076 | 29 | 18 | 9.682 / 0.098 | ya | 32.98 | `quartus_C4c.md` |
| 2 | 9,032 | 4078 | 29 | 18 | 11.636 / 0.129 | ya | 35.26 | `quartus_C4c-s2.md` |
| 3 | 9,094 | 4087 | 29 | 18 | 9.016 / 0.117 | ya | 32.27 | `quartus_C4c-s3.md` |
| 4 | 9,051 | 4080 | 29 | 18 | 9.242 / 0.107 | ya | 32.51 | `quartus_C4c-s4.md` |
| 5 | 9,068 | 4081 | 29 | 18 | 11.011 / 0.133 | ya | 34.50 | `quartus_C4c-s5.md` |
| 6 | 9,084 | 4091 | 29 | 18 | 9.895 / 0.095 | ya | 33.22 | `quartus_C4c-s6.md` |

## Perbandingan dengan Barrett 5b (C4b-B, median atas seed 1-6; INFERENCE)
| | Median ALM (min-maks) | Median Fmax (min-maks) MHz | t_NTT / t_INTT pada median Fmax (us) |
|---|---|---|---|
| C4b-B (Barrett, 5b) | 9,171.0 (9,166-9,208) | 34.515 (33.46-34.84) | 3.448 / 10.865 |
| C4c (masukan INTT malas) | 9,059.5 (9,032-9,094) | 33.100 (32.27-35.26) | 3.595 / 11.329 |

## Aturan adopsi (ADR 0014 §4)
- PASS: benar (verification_status.json)
- PASS: siklus persis 119 / 375
- PASS: ALM <= 12,573 di setiap seed
- PASS: timing terpenuhi pada 40,000 ns di setiap seed
- FAIL: median Fmax 33.100 MHz > 34.84 MHz (puncak Barrett 5b; puncak yang dihitung ulang 34.84)
- FAIL: ADR 0012: t_NTT 3.595 < 3.448 us dan t_INTT 11.329 < 10.865 us

Hasil aturan: C4c TIDAK diadopsi (C4b-B tetap konfigurasi C4).
