## Per seed, S7 (MEASURED)
| Seed | ALM | Register | M10K | DSP | Setup / hold terburuk (ns) | Timing terpenuhi @ 40 ns | Fmax slow corner terendah (MHz) | Evidence |
|---|---|---|---|---|---|---|---|---|
| 1 | 9,394 | 4317 | 31 | 16 | 14.439 / 0.128 | ya | 39.12 | `quartus_S7.md` |
| 2 | 9,388 | 4317 | 31 | 16 | 13.906 / 0.118 | ya | 38.32 | `quartus_S7-s2.md` |
| 3 | 9,361 | 4302 | 31 | 16 | 13.894 / 0.113 | ya | 38.31 | `quartus_S7-s3.md` |
| 4 | 9,405 | 4296 | 31 | 16 | 13.606 / 0.111 | ya | 37.89 | `quartus_S7-s4.md` |
| 5 | 9,362 | 4298 | 31 | 16 | 14.545 / 0.130 | ya | 39.29 | `quartus_S7-s5.md` |
| 6 | 9,396 | 4324 | 31 | 16 | 15.178 / 0.088 | ya | 40.29 | `quartus_S7-s6.md` |

## Perbandingan dengan M6 (median atas seed 1-6; INFERENCE)
| | Median ALM (min-maks) | DSP | Median Fmax (min-maks) MHz | siklus NTT / INTT | t_NTT / t_INTT pada median Fmax (us) |
|---|---|---|---|---|---|
| M6 (langkah sebelumnya) | 9,421.5 (9,394-9,441) | 16 | 34.430 (32.35-35.04) | 119 / 119 | 3.456 / 3.456 |
| S7 (RD_SPLIT = 1, P = 7) | 9,391.0 (9,361-9,405) | 16 | 38.720 (37.89-40.29) | 120 / 120 | 3.099 / 3.099 |

## Aturan adopsi (test plan bagian 4)
- PASS: benar (verification_status.json: V1-V6; V7 tidak dijalankan untuk S7, Amandemen A1)
- PASS: siklus persis NTT 120 / INTT 120
- PASS: ALM <= 12,573 di setiap seed
- PASS: timing terpenuhi pada 40,000 ns di setiap seed
- PASS: ADR 0012, t_NTT 3.099 < 3.456 us (median Fmax M6 34.430 MHz; memerlukan median S7 38.720 MHz > 34.719 MHz)
- PASS: ADR 0012, t_INTT 3.099 < 3.456 us

Hasil aturan: S7 DIADOPSI.
Sebaran seed Fmax S7: 2.40 MHz (min-maks).
