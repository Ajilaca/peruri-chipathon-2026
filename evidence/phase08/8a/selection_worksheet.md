## Per seed pada 40,000 ns (MEASURED)
| Seed | Konfigurasi | ALM | Register | M10K | DSP | Setup / hold terburuk (ns) | Timing terpenuhi @ 40 ns | Fmax slow corner terendah (MHz) | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | K0 | 3,572 | 1653 | 0 | 0 | 22.452 / 0.163 | ya | 56.99 | `quartus_K0.md` |
| 2 | K0 | 3,569 | 1653 | 0 | 0 | 24.373 / 0.164 | ya | 63.99 | `quartus_K0-s2.md` |
| 3 | K0 | 3,566 | 1653 | 0 | 0 | 25.196 / 0.162 | ya | 67.55 | `quartus_K0-s3.md` |
| 4 | K0 | 3,558 | 1653 | 0 | 0 | 25.794 / 0.164 | ya | 70.39 | `quartus_K0-s4.md` |
| 5 | K0 | 3,567 | 1653 | 0 | 0 | 25.646 / 0.163 | ya | 69.67 | `quartus_K0-s5.md` |
| 6 | K0 | 3,561 | 1653 | 0 | 0 | 25.251 / 0.164 | ya | 67.80 | `quartus_K0-s6.md` |
| 1 | C5 | 6,169 | 1652 | 0 | 0 | 19.952 / 0.162 | ya | 49.88 | `quartus_C5.md` |
| 2 | C5 | 6,166 | 1652 | 0 | 0 | 20.648 / 0.162 | ya | 51.67 | `quartus_C5-s2.md` |
| 3 | C5 | 6,152 | 1652 | 0 | 0 | 20.557 / 0.162 | ya | 51.43 | `quartus_C5-s3.md` |
| 4 | C5 | 6,169 | 1652 | 0 | 0 | 20.582 / 0.162 | ya | 51.50 | `quartus_C5-s4.md` |
| 5 | C5 | 6,155 | 1652 | 0 | 0 | 19.145 / 0.162 | ya | 47.95 | `quartus_C5-s5.md` |
| 6 | C5 | 6,168 | 1652 | 0 | 0 | 18.894 / 0.162 | ya | 47.38 | `quartus_C5-s6.md` |

## Perbandingan dengan K0 (median atas seed 1-6; INFERENCE)
| | Median ALM (min-maks) | Register | Median Fmax (min-maks) MHz | siklus per permutasi (sponge) | t per permutasi pada median Fmax (us) |
|---|---|---|---|---|---|
| K0 (langkah sebelumnya) | 3,566.5 (3,558-3,572) | 1653-1653 | 67.675 (56.99-70.39) | 26 | 0.3842 |
| C5 (dua ronde per siklus) | 6,167.0 (6,152-6,169) | 1652-1652 | 50.655 (47.38-51.67) | 14 | 0.2764 |

## Aturan adopsi (test plan bagian 4)
- PASS: benar (verification_status.json: V1-V9, kedua simulator, kontrol gagal, formal)
- PASS: busy persis 12 siklus dan 14 siklus per permutasi di sponge
- PASS: ALM <= 12,573 di setiap seed (batas kerja)
- PASS: timing terpenuhi pada 40,000 ns di setiap seed
- PASS: gaya ADR 0012: t = 14 / F_C5 = 0.2764 us < 26 / F_K0 = 0.3842 us (median Fmax K0 67.675 MHz; median C5 50.655 MHz harus melebihi 36.440 MHz)

Hasil aturan: C5 DIADOPSI.
Sebaran seed Fmax C5: 4.29 MHz (min-maks); K0: 13.40 MHz.

## Informasi: kompilasi 20,000 ns (bukan bagian aturan)
- K0-20 (seed 1): ALM 3,573, setup terburuk 6.893 ns (terpenuhi), Fmax slow corner terendah 76.30 MHz, `quartus_K0-20.md`
- C5-20 (seed 1): ALM 6,178, setup terburuk 4.591 ns (terpenuhi), Fmax slow corner terendah 64.90 MHz, `quartus_C5-20.md`
