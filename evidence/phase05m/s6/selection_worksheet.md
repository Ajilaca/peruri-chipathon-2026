## Per seed, M6 (MEASURED)
| Seed | ALM | Register | M10K | DSP | Setup / hold terburuk (ns) | Timing terpenuhi @ 40 ns | Fmax slow corner terendah (MHz) | Evidence |
|---|---|---|---|---|---|---|---|---|
| 1 | 9,426 | 4041 | 29 | 16 | 11.161 / 0.145 | ya | 34.68 | `quartus_M6.md` |
| 2 | 9,394 | 4030 | 29 | 16 | 10.942 / 0.126 | ya | 34.41 | `quartus_M6-s2.md` |
| 3 | 9,417 | 4063 | 29 | 16 | 10.721 / 0.143 | ya | 34.15 | `quartus_M6-s3.md` |
| 4 | 9,409 | 4080 | 29 | 16 | 9.090 / 0.120 | ya | 32.35 | `quartus_M6-s4.md` |
| 5 | 9,441 | 4049 | 29 | 16 | 11.464 / 0.126 | ya | 35.04 | `quartus_M6-s5.md` |
| 6 | 9,429 | 4036 | 29 | 16 | 10.972 / 0.084 | ya | 34.45 | `quartus_M6-s6.md` |

## Perbandingan dengan C4b-B (median atas seed 1-6; INFERENCE)
| | Median ALM (min-maks) | DSP | Median Fmax (min-maks) MHz | siklus NTT / INTT | t_NTT / t_INTT pada median Fmax (us) |
|---|---|---|---|---|---|
| C4b-B (langkah sebelumnya) | 9,171.0 (9,166-9,208) | 18 | 34.515 (33.46-34.84) | 119 / 375 | 3.448 / 10.865 |
| M6 (INTT tanpa lintasan skala) | 9,421.5 (9,394-9,441) | 16 | 34.430 (32.35-35.04) | 119 / 119 | 3.456 / 3.456 |

## Aturan adopsi (test plan bagian 4)
- PASS: benar (verification_status.json: V1-V8; V9 tidak dijalankan untuk S6, Amandemen A1)
- PASS: siklus persis NTT 119 / INTT 119
- PASS: ALM <= 12,573 di setiap seed
- PASS: timing terpenuhi pada 40,000 ns di setiap seed
- PASS: ADR 0012, t_INTT 3.456 < 10.865 us (median Fmax C4b-B 34.515 MHz)
- FAIL: ADR 0012, t_NTT 3.456 < 3.448 us (memerlukan median Fmax M6 34.430 MHz > 34.515 MHz)

Hasil aturan: M6 TIDAK diadopsi oleh aturan (tidak ada toleransi yang ditambahkan).
Hanya bagian NTT ADR 0012 yang gagal (mode NTT tidak berubah dalam siklus; marginnya adalah median Fmax). Test plan bagian 4: dilaporkan seperti terukur; aturan lain apa pun adalah keputusan baru tim.
