## Per seed, S10 pada 40,000 ns (MEASURED)
| Seed | ALM | Register | M10K | DSP | Setup / hold terburuk (ns) | Timing terpenuhi @ 40 ns | Fmax slow corner terendah (MHz) | Evidence |
|---|---|---|---|---|---|---|---|---|
| 1 | 5,091 | 545 | 24 | 16 | 17.662 / 0.089 | ya | 44.77 | `quartus_S10.md` |
| 2 | 5,088 | 543 | 24 | 16 | 16.382 / 0.132 | ya | 42.34 | `quartus_S10-s2.md` |
| 3 | 5,069 | 555 | 24 | 16 | 18.376 / 0.095 | ya | 46.24 | `quartus_S10-s3.md` |
| 4 | 5,082 | 548 | 24 | 16 | 16.865 / 0.111 | ya | 43.22 | `quartus_S10-s4.md` |
| 5 | 5,045 | 552 | 24 | 16 | 17.205 / 0.106 | ya | 43.87 | `quartus_S10-s5.md` |
| 6 | 5,072 | 554 | 24 | 16 | 18.565 / 0.155 | ya | 46.65 | `quartus_S10-s6.md` |

## Perbandingan dengan S7 (median atas seed 1-6; INFERENCE)
| | Median ALM (min-maks) | DSP | Median Fmax (min-maks) MHz | siklus NTT / INTT | t_NTT / t_INTT pada median Fmax (us) |
|---|---|---|---|---|---|
| S7 (langkah sebelumnya) | 9,391.0 (9,361-9,405) | 16 | 38.720 (37.89-40.29) | 120 / 120 | 3.099 / 3.099 |
| S10 (16 x 1R1W, P = 5) | 5,077.0 (5,045-5,091) | 16 | 44.320 (42.34-46.65) | 118 / 118 | 2.662 / 2.662 |

## Aturan adopsi (test plan bagian 4)
- PASS: benar (verification_status.json: V1-V6 termasuk top Fase 6 dengan S10)
- PASS: siklus persis NTT 118 / INTT 118
- PASS: ALM <= 12,573 di setiap seed
- PASS: timing terpenuhi pada 40,000 ns di setiap seed
- PASS: ADR 0012, t_NTT 2.662 < 3.099 us (median Fmax S7 38.720 MHz; median S10 44.320 MHz harus melebihi 38.075 MHz)
- PASS: ADR 0012, t_INTT 2.662 < 3.099 us

Hasil aturan: S10 DIADOPSI.
Sebaran seed Fmax S10: 4.31 MHz (min-maks).

## Informasi: kompilasi 20,000 ns (bukan bagian aturan; 50 MHz memerlukan slack setup terburuk >= 0 pada 20 ns)
| Revisi | seed | setup terburuk (ns) per seed | timing terpenuhi pada 20 ns | Fmax slow corner terendah per seed (MHz) | median |
|---|---|---|---|---|---|
| S7-20 | 1-6 | -1.388, -1.655, -2.296, -2.431, -1.933, -1.615 | 0/6 | 46.76, 46.18, 44.85, 44.58, 45.59, 46.26 | 45.885 |
| S10-20 | 1-6 | 1.176, 1.718, 0.984, 1.050, 1.241, 0.792 | 6/6 | 53.12, 54.70, 52.59, 52.77, 53.31, 52.06 | 52.945 |
