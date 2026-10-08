## Per seed, S8 (MEASURED)
| Seed | ALM | Register | M10K | DSP | Setup / hold terburuk (ns) | Timing terpenuhi @ 40 ns | Fmax slow corner terendah (MHz) | Evidence |
|---|---|---|---|---|---|---|---|---|
| 1 | 9,464 | 4144 | 33 | 16 | 15.135 / 0.073 | ya | 40.22 | `quartus_S8.md` |
| 2 | 9,423 | 4136 | 33 | 16 | 13.759 / 0.107 | ya | 38.11 | `quartus_S8-s2.md` |
| 3 | 9,471 | 4139 | 33 | 16 | 13.017 / 0.090 | ya | 37.06 | `quartus_S8-s3.md` |
| 4 | 9,402 | 4137 | 33 | 16 | 12.794 / 0.131 | ya | 36.76 | `quartus_S8-s4.md` |
| 5 | 9,469 | 4138 | 33 | 16 | 13.772 / 0.140 | ya | 38.13 | `quartus_S8-s5.md` |
| 6 | 9,419 | 4130 | 33 | 16 | 13.593 / 0.152 | ya | 37.87 | `quartus_S8-s6.md` |

## Perbandingan dengan langkah sebelumnya (median atas seed 1-6; INFERENCE; aturan hanya membandingkan dengan S7)
| | Median ALM (min-maks) | DSP | Median Fmax (min-maks) MHz | siklus NTT / INTT | t_NTT / t_INTT pada median Fmax (us) |
|---|---|---|---|---|---|
| C4b-B (Fase 5) | 9,171.0 (9,166-9,208) | 18 | 34.515 (33.46-34.84) | 119 / 375 | 3.448 / 10.865 |
| M6 (S6) | 9,421.5 (9,394-9,441) | 16 | 34.430 (32.35-35.04) | 119 / 119 | 3.456 / 3.456 |
| S7 (langkah sebelumnya) | 9,391.0 (9,361-9,405) | 16 | 38.720 (37.89-40.29) | 120 / 120 | 3.099 / 3.099 |
| S8 (register tulis, P = 8, satu bubble) | 9,443.5 (9,402-9,471) | 16 | 37.990 (36.76-40.22) | 122 / 122 | 3.211 / 3.211 |

## Aturan adopsi (test plan bagian 4)
- PASS: benar (verification_status.json: V1-V8, regresi V8 dijalankan sekali di S8 menurut Amandemen A1)
- PASS: siklus persis NTT 122 / INTT 122
- PASS: ALM <= 12,573 di setiap seed
- PASS: timing terpenuhi pada 40,000 ns di setiap seed
- FAIL: ADR 0012, t_NTT 3.211 < 3.099 us (median Fmax S7 38.720 MHz; median S8 37.990 MHz harus melebihi 39.365 MHz)
- FAIL: ADR 0012, t_INTT 3.211 < 3.099 us

Hasil aturan: S8 TIDAK diadopsi oleh aturan (tidak ada toleransi yang ditambahkan).
Sebaran seed Fmax S8: 3.46 MHz (min-maks).
