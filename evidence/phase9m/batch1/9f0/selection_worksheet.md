## S0: inti 9M-1 (`CODEC_W2 = 1`, hash dan sampler C5) di bawah batasan lebih ketat (MEASURED, kernel-only, virtual pin)
| Revisi | Batasan (ns) | Upaya | ALM | Register | Blok RAM | DSP | Setup / hold terburuk (ns) | Timing terpenuhi | Fmax slow corner terendah (MHz) | Peringatan kritis | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F16-s1 | 16.000 | bawaan | 17,980 | 8635 | 53 | 28 | 1.992 / 0.118 | ya | 71.39 | 1 | `evidence/phase9m/batch1/9f0/quartus_F16-s1.md` |
| F16-s2 | 16.000 | bawaan | 17,888 | 8575 | 53 | 28 | 2.075 / 0.108 | ya | 71.81 | 1 | `evidence/phase9m/batch1/9f0/quartus_F16-s2.md` |
| F15-s1 | 15.000 | bawaan | 17,971 | 8719 | 53 | 28 | 1.475 / 0.102 | ya | 73.94 | 1 | `evidence/phase9m/batch1/9f0/quartus_F15-s1.md` |
| F15-s2 | 15.000 | bawaan | 17,926 | 8700 | 53 | 28 | 1.363 / 0.071 | ya | 73.33 | 1 | `evidence/phase9m/batch1/9f0/quartus_F15-s2.md` |
| F14-s1 | 14.000 | bawaan | 17,907 | 8770 | 53 | 28 | 0.721 / 0.109 | ya | 75.31 | 1 | `evidence/phase9m/batch1/9f0/quartus_F14-s1.md` |
| F14-s2 | 14.000 | bawaan | 17,889 | 8669 | 53 | 28 | 1.062 / 0.108 | ya | 77.29 | 1 | `evidence/phase9m/batch1/9f0/quartus_F14-s2.md` |
| H14-s1 | 14.000 | kinerja tinggi | 18,876 | 10966 | 49 | 28 | 0.826 / 0.090 | ya | 75.91 | 1 | `evidence/phase9m/batch1/9f0/quartus_H14-s1.md` |
| H14-s2 | 14.000 | kinerja tinggi | 18,897 | 10935 | 49 | 28 | 0.423 / 0.107 | ya | 73.65 | 1 | `evidence/phase9m/batch1/9f0/quartus_H14-s2.md` |
| F13-s1 | 13.000 | bawaan | 17,900 | 8807 | 53 | 28 | 0.227 / 0.112 | ya | 78.29 | 1 | `evidence/phase9m/batch1/9f0/quartus_F13-s1.md` |
| F13-s2 | 13.000 | bawaan | 17,891 | 8873 | 53 | 28 | -0.213 / 0.100 | TIDAK | 75.68 | 3 | `evidence/phase9m/batch1/9f0/quartus_F13-s2.md` |

### Per batasan
| Kelompok | Batasan (ns) | Terpenuhi di k dari 2 seed | Fmax lebih rendah dari keduanya (MHz) | Setup terburuk dari keduanya (ns) | ALM (min-maks) | Latensi KeyGen / Encaps / Decaps pada Fmax lebih rendah (us, perhitungan tim) |
|---|---|---|---|---|---|---|
| F16 | 16.000 | 2 of 2 | 71.39 | 1.992 | 17,888-17,980 | 116.6 / 142.3 / 217.3 |
| F15 | 15.000 | 2 of 2 | 73.33 | 1.363 | 17,926-17,971 | 113.6 / 138.5 / 211.6 |
| F14 | 14.000 | 2 of 2 | 75.31 | 0.721 | 17,889-17,907 | 110.6 / 134.9 / 206.0 |
| H14 | 14.000 | 2 of 2 | 73.65 | 0.423 | 18,876-18,897 | 113.1 / 137.9 / 210.7 |
| F13 | 13.000 | 1 of 2 | 75.68 | -0.213 | 17,891-17,900 | 110.0 / 134.2 / 205.0 |

### Aturan (test plan bagian 5)
- Informasi, tanpa adopsi. Batas desain yang ada adalah batasan terketat yang terpenuhi di kedua seed: F16 (16 ns), F15 (15 ns), F14 (14 ns), H14 (14 ns).
- Amandemen A2 (sapuan diperluas, aturan: berhenti pada batasan pertama yang tidak terpenuhi): sapuan berhenti pada 13 ns (seed 1 terpenuhi, seed 2 tidak); batasnya ada di antara 13 dan 14 ns untuk desain dan setelan ini.
