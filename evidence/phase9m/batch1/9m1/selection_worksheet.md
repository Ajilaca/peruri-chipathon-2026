## Per seed pada 40,000 ns (MEASURED), revisi MW (CODEC_W2 = 1)
| Seed | ALM | Register | Blok RAM | Bit memori blok | DSP | Setup / hold terburuk (ns) | Timing terpenuhi @ 40 ns | Fmax slow corner terendah (MHz) | Peringatan kritis | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 17,672 | 8233 | 54 | 120,350 | 28 | 20.825 / 0.116 | ya | 52.15 | 1 | `quartus_MW.md` |
| 2 | 17,641 | 8299 | 54 | 120,350 | 28 | 20.048 / 0.111 | ya | 50.12 | 1 | `quartus_MW-s2.md` |
| 3 | 17,644 | 8320 | 54 | 120,350 | 28 | 19.558 / 0.123 | ya | 48.92 | 1 | `quartus_MW-s3.md` |
| 4 | 17,655 | 8189 | 54 | 120,350 | 28 | 18.957 / 0.083 | ya | 47.52 | 1 | `quartus_MW-s4.md` |
| 5 | 17,683 | 8250 | 54 | 120,350 | 28 | 18.655 / 0.077 | ya | 46.85 | 1 | `quartus_MW-s5.md` |
| 6 | 17,653 | 8376 | 54 | 120,350 | 28 | 19.504 / 0.114 | ya | 48.79 | 1 | `quartus_MW-s6.md` |

MW: median ALM (min-maks) 17,654.0 (17,641-17,683); register 8189-8376; blok RAM 54-54; DSP 28-28; median Fmax (min-maks) 48.855 (46.85-52.15) MHz
Baseline Fase 9c MC (`evidence/phase09/9c/`): median ALM 17,620.5 (17,608-17,636); register 8210-8365; blok RAM 54-54; median Fmax 49.280 (47.64-51.74) MHz
Selisih MW - MC: ALM +33.5, Fmax -0.425 MHz
Informasi MW-20 (20,000 ns), seed 1: ALM 17,808, register 8487, setup terburuk 4.355 ns (terpenuhi), Fmax slow corner terendah 63.92 MHz (`quartus_MW-20.md`)

## Siklus dan waktu (masukan profil, MEASURED di simulasi; t = siklus / median Fmax adalah INFERENCE / perhitungan tim, timing statis kernel-only, bukan pengukuran papan)
| Operasi | Siklus Fase 9 | Siklus 9M-1 | Perubahan | t Fase 9 (us) pada median Fmax MC | t 9M-1 (us) pada median Fmax MW | Lebih rendah? |
|---|---|---|---|---|---|---|
| KeyGen | 9,095 | 8,327 | -8.4 % | 184.6 | 170.4 | ya |
| Encaps | 10,735 | 10,159 | -5.4 % | 217.8 | 207.9 | ya |
| Decaps | 16,667 | 15,515 | -6.9 % | 338.2 | 317.6 | ya |

### Butir numerik aturan adopsi (test plan bagian 6)
- PASS: butir 2, timing terpenuhi pada 40,000 ns di setiap seed 1-6
- PASS: butir 3, t KeyGen, Encaps, dan Decaps lebih rendah dari Fase 9 (tabel di atas)
- PASS: butir 4, median ALM MW paling banyak 1,000 di atas median Fase 9 (+33.5)
- butir 1 (V1-V3, V5-V7) adalah log yang didaftar di `result_9m1.md`
