## Inti 9M-1, hash C5 (`HASH_C5 = 1`, `CODEC_W2 = 1`) pada 40,000 ns, seed 1-6 (MEASURED, kernel-only, virtual pin)
| Revisi | ALM | Register | Blok RAM | DSP | Setup / hold terburuk (ns) | Timing terpenuhi @ 40 ns | Fmax slow corner terendah (MHz) | Peringatan kritis | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| MW | 17,672 | 8233 | 54 | 28 | 20.825 / 0.116 | ya | 52.15 | 1 | `evidence/phase9m/batch1/9m1/quartus_MW.md` |
| MW-s2 | 17,641 | 8299 | 54 | 28 | 20.048 / 0.111 | ya | 50.12 | 1 | `evidence/phase9m/batch1/9m1/quartus_MW-s2.md` |
| MW-s3 | 17,644 | 8320 | 54 | 28 | 19.558 / 0.123 | ya | 48.92 | 1 | `evidence/phase9m/batch1/9m1/quartus_MW-s3.md` |
| MW-s4 | 17,655 | 8189 | 54 | 28 | 18.957 / 0.083 | ya | 47.52 | 1 | `evidence/phase9m/batch1/9m1/quartus_MW-s4.md` |
| MW-s5 | 17,683 | 8250 | 54 | 28 | 18.655 / 0.077 | ya | 46.85 | 1 | `evidence/phase9m/batch1/9m1/quartus_MW-s5.md` |
| MW-s6 | 17,653 | 8376 | 54 | 28 | 19.504 / 0.114 | ya | 48.79 | 1 | `evidence/phase9m/batch1/9m1/quartus_MW-s6.md` |

Median ALM (min-maks) 17,654.0 (17,641-17,683); register 8189-8376; blok RAM 54-54; DSP 28-28
Setup slack terburuk atas seed 18.655 ns; median Fmax slow corner terendah (min-maks) 48.855 (46.85-52.15) MHz
Timing terpenuhi pada 40,000 ns di 6 dari 6 seed

Latensi pada median Fmax tabel ini (perhitungan tim; siklus masukan profil):
KeyGen 8,327 siklus = 170.4 us; Encaps 10,159 = 207.9 us; Decaps 15,515 = 317.6 us

Informasi, MW-20 (seed 1, 20,000 ns): ALM 17,808; setup / hold terburuk 4.355 / 0.081 ns; Fmax slow corner terendah 63.92 MHz; `evidence/phase9m/batch1/9m1/quartus_MW-20.md`

## Inti 9M-1, hash K0 (`HASH_C5 = 0`, `CODEC_W2 = 1`) pada 40,000 ns, seed 1-6 (MEASURED, kernel-only, virtual pin)
| Revisi | ALM | Register | Blok RAM | DSP | Setup / hold terburuk (ns) | Timing terpenuhi @ 40 ns | Fmax slow corner terendah (MHz) | Peringatan kritis | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| MK | 15,923 | 8249 | 54 | 28 | 19.069 / 0.080 | ya | 47.78 | 1 | `evidence/phase9m/batch1/9m3/quartus_MK.md` |
| MK-s2 | 15,899 | 8230 | 54 | 28 | 19.555 / 0.100 | ya | 48.91 | 1 | `evidence/phase9m/batch1/9m3/quartus_MK-s2.md` |
| MK-s3 | 15,911 | 8266 | 54 | 28 | 19.727 / 0.110 | ya | 49.33 | 1 | `evidence/phase9m/batch1/9m3/quartus_MK-s3.md` |
| MK-s4 | 15,912 | 8261 | 54 | 28 | 19.754 / 0.107 | ya | 49.39 | 1 | `evidence/phase9m/batch1/9m3/quartus_MK-s4.md` |
| MK-s5 | 15,926 | 8263 | 54 | 28 | 18.934 / 0.132 | ya | 47.47 | 1 | `evidence/phase9m/batch1/9m3/quartus_MK-s5.md` |
| MK-s6 | 15,940 | 8382 | 54 | 28 | 19.577 / 0.117 | ya | 48.96 | 1 | `evidence/phase9m/batch1/9m3/quartus_MK-s6.md` |

Median ALM (min-maks) 15,917.5 (15,899-15,940); register 8230-8382; blok RAM 54-54; DSP 28-28
Setup slack terburuk atas seed 18.934 ns; median Fmax slow corner terendah (min-maks) 48.935 (47.47-49.39) MHz
Timing terpenuhi pada 40,000 ns di 6 dari 6 seed

Latensi pada median Fmax tabel ini (perhitungan tim; siklus masukan profil):
KeyGen 8,447 siklus = 172.6 us; Encaps 10,279 = 210.1 us; Decaps 15,635 = 319.5 us

Informasi, MK-20 (seed 1, 20,000 ns): ALM 16,007; setup / hold terburuk 4.003 / 0.067 ns; Fmax slow corner terendah 62.51 MHz; `evidence/phase9m/batch1/9m3/quartus_MK-20.md`

### Aturan (test plan bagian 5), butir 2-4 (butir 1 = test, lihat result_9m3.md)
- 2. timing terpenuhi pada 40,000 ns di setiap seed: terpenuhi (6 dari 6)
- 3. median ALM MW - MK = 1,736.5 (memerlukan >= 1,500): terpenuhi
- 4. latensi MK relatif terhadap MW (siklus / median Fmax): KeyGen +1.28 %, Encaps +1.02 %, Decaps +0.61 % (memerlukan <= +2 % masing-masing): terpenuhi
