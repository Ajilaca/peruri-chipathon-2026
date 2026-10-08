## Per seed (MEASURED; kualifikasi menurut ADR 0011 D8)
| Kandidat | Seed | ALM | Register | M10K | DSP | Setup / hold terburuk (ns) | Timing terpenuhi @ 40 ns | Fmax slow corner terendah (MHz) | t_NTT (us) | Memenuhi syarat | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Barrett | 1 | 9,208 | 4115 | 29 | 18 | 11.044 / 0.120 | ya | 34.54 | 3.445 | ya | `quartus_C4b-B.md` |
| Barrett | 2 | 9,168 | 4102 | 29 | 18 | 10.832 / 0.130 | ya | 34.28 | 3.471 | ya | `quartus_C4b-B-s2.md` |
| Barrett | 3 | 9,167 | 4098 | 29 | 18 | 11.175 / 0.134 | ya | 34.69 | 3.430 | ya | `quartus_C4b-B-s3.md` |
| Barrett | 4 | 9,174 | 4089 | 29 | 18 | 10.112 / 0.134 | ya | 33.46 | 3.556 | ya | `quartus_C4b-B-s4.md` |
| Barrett | 5 | 9,166 | 4089 | 29 | 18 | 11.300 / 0.142 | ya | 34.84 | 3.416 | ya | `quartus_C4b-B-s5.md` |
| Barrett | 6 | 9,188 | 4083 | 29 | 18 | 11.009 / 0.100 | ya | 34.49 | 3.450 | ya | `quartus_C4b-B-s6.md` |
| Montgomery | 1 | 9,249 | 4297 | 29 | 9 | 9.526 / 0.107 | ya | 32.81 | 3.627 | ya | `quartus_C4b-M.md` |
| Montgomery | 2 | 9,287 | 4287 | 29 | 9 | 10.669 / 0.134 | ya | 34.09 | 3.491 | ya | `quartus_C4b-M-s2.md` |
| Montgomery | 3 | 9,276 | 4292 | 29 | 9 | 10.404 / 0.143 | ya | 33.79 | 3.522 | ya | `quartus_C4b-M-s3.md` |
| Montgomery | 4 | 9,286 | 4294 | 29 | 9 | 9.884 / 0.112 | ya | 33.20 | 3.584 | ya | `quartus_C4b-M-s4.md` |
| Montgomery | 5 | 9,297 | 4299 | 29 | 9 | 10.387 / 0.102 | ya | 33.77 | 3.524 | ya | `quartus_C4b-M-s5.md` |
| Montgomery | 6 | 9,296 | 4284 | 29 | 9 | 10.806 / 0.158 | ya | 34.25 | 3.474 | ya | `quartus_C4b-M-s6.md` |

## Per kandidat (median atas seed 1-6; INFERENCE dari baris di atas)
| Kandidat | Benar | Siklus NTT / INTT | Memenuhi syarat (semua seed) | Median ALM (min-maks) | Median Fmax (min-maks) MHz | t_NTT pada median Fmax (us) |
|---|---|---|---|---|---|---|
| Barrett | PASS | 119 / 375 | ya | 9,171.0 (9,166-9,208) | 34.515 (33.46-34.84) | 3.448 |
| Montgomery | PASS | 119 / 375 | ya | 9,286.5 (9,249-9,297) | 33.780 (32.81-34.25) | 3.523 |

## Hasil aturan
Median Fmax lebih tinggi: Barrett (34.515 MHz); Montgomery 2.13 % lebih rendah.
Hampir seri (<= 5 %). Median ALM: Barrett 9,171.0, Montgomery 9,286.5 (selisih 115.5).
Median ALM lebih rendah menang: Barrett dipilih oleh aturan.
