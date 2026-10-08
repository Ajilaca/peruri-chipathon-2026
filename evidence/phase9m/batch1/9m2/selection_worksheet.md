## Inti Fase 9 (`CODEC_W2 = 0`) pada 20,000 ns (MEASURED, kernel-only, virtual pin)
| Seed | ALM | Register | Blok RAM | DSP | Setup / hold terburuk (ns) | Timing terpenuhi @ 20 ns | Fmax slow corner terendah (MHz) | Peringatan kritis | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 17,650 | 8374 | 54 | 28 | 4.419 / 0.113 | ya | 64.18 | 1 | `evidence/phase09/9c/quartus_MC-20.md` |
| 2 | 17,780 | 8465 | 54 | 28 | 4.155 / 0.102 | ya | 63.11 | 1 | `evidence/phase9m/batch1/9m2/quartus_MC-20-s2.md` |
| 3 | 17,694 | 8431 | 54 | 28 | 4.534 / 0.094 | ya | 64.66 | 1 | `evidence/phase9m/batch1/9m2/quartus_MC-20-s3.md` |
| 4 | 17,729 | 8369 | 54 | 28 | 3.730 / 0.121 | ya | 61.46 | 1 | `evidence/phase9m/batch1/9m2/quartus_MC-20-s4.md` |
| 5 | 17,682 | 8461 | 54 | 28 | 4.522 / 0.109 | ya | 64.61 | 1 | `evidence/phase9m/batch1/9m2/quartus_MC-20-s5.md` |
| 6 | 17,723 | 8504 | 54 | 28 | 3.831 / 0.077 | ya | 61.85 | 1 | `evidence/phase9m/batch1/9m2/quartus_MC-20-s6.md` |

Median ALM (min-maks) 17,708.5 (17,650-17,780); register 8369-8504; blok RAM 54-54; DSP 28-28
Setup slack terburuk atas seed 3.730 ns; median Fmax slow corner terendah (min-maks) 63.645 (61.46-64.66) MHz
Timing terpenuhi pada 20,000 ns di 6 dari 6 seed

Latensi pada median Fmax tabel ini (perhitungan tim; siklus masukan profil; timing statis kernel-only, bukan pengukuran papan):
KeyGen 9,095 siklus = 142.9 us; Encaps 10,735 = 168.7 us; Decaps 16,667 = 261.9 us

## Inti 9M-1 (`CODEC_W2 = 1`) pada 20,000 ns (MEASURED, kernel-only, virtual pin)
| Seed | ALM | Register | Blok RAM | DSP | Setup / hold terburuk (ns) | Timing terpenuhi @ 20 ns | Fmax slow corner terendah (MHz) | Peringatan kritis | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 17,808 | 8487 | 54 | 28 | 4.355 / 0.081 | ya | 63.92 | 1 | `evidence/phase9m/batch1/9m1/quartus_MW-20.md` |
| 2 | 17,756 | 8411 | 54 | 28 | 4.972 / 0.088 | ya | 66.54 | 1 | `evidence/phase9m/batch1/9m2/quartus_MW-20-s2.md` |
| 3 | 17,800 | 8447 | 54 | 28 | 4.236 / 0.131 | ya | 63.44 | 1 | `evidence/phase9m/batch1/9m2/quartus_MW-20-s3.md` |
| 4 | 17,759 | 8460 | 54 | 28 | 4.498 / 0.112 | ya | 64.51 | 1 | `evidence/phase9m/batch1/9m2/quartus_MW-20-s4.md` |
| 5 | 17,845 | 8481 | 54 | 28 | 4.184 / 0.100 | ya | 63.23 | 1 | `evidence/phase9m/batch1/9m2/quartus_MW-20-s5.md` |
| 6 | 17,728 | 8407 | 54 | 28 | 4.389 / 0.080 | ya | 64.06 | 1 | `evidence/phase9m/batch1/9m2/quartus_MW-20-s6.md` |

Median ALM (min-maks) 17,779.5 (17,728-17,845); register 8407-8487; blok RAM 54-54; DSP 28-28
Setup slack terburuk atas seed 4.184 ns; median Fmax slow corner terendah (min-maks) 63.990 (63.23-66.54) MHz
Timing terpenuhi pada 20,000 ns di 6 dari 6 seed

Latensi pada median Fmax tabel ini (perhitungan tim; siklus masukan profil; timing statis kernel-only, bukan pengukuran papan):
KeyGen 8,327 siklus = 130.1 us; Encaps 10,159 = 158.8 us; Decaps 15,515 = 242.5 us

### Aturan (test plan bagian 5)
- terpenuhi: pernyataan "timing terpenuhi pada 20,000 ns" berlaku untuk sebuah konfigurasi hanya bila keenam seed memenuhinya; lihat baris "Timing terpenuhi pada 20,000 ns di k dari 6 seed" pada tiap tabel
