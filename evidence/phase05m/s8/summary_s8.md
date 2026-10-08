<!-- claim-lint: skip-file (internal checkpoint record, not proposal text) -->
# Checkpoint Fase 5M S8: register jalur tulis, P = 8, satu bubble per arah (revisi S8) lawan S7

Rencana dan aturan: `evidence/phase05m/test_plan_s8.md` (ditetapkan sebelum mengukur). Catatan: ADR 0023 (ketika itu Proposed).

| Besaran | S7 (MEASURED) | S8 (MEASURED) | Delta (INFERENCE) |
|---|---:|---:|---:|
| ALM, median seed 1-6 (min-maks) | 9,391.0 (9,361-9,405) | 9,443.5 (9,402-9,471) | +52.5 |
| Register (min-maks) | 4,296-4,324 | 4,130-4,144 | sekitar -170 |
| DSP / M10K | 16 / 31 | 16 / 33 | 0 / +2 |
| Median Fmax, slow corner terendah (MHz) | 38.720 (37.89-40.29) | 37.990 (36.76-40.22) | -0.730 (-1.9 %) |
| Siklus NTT / INTT (simulasi) | 120 / 120 | 122 / 122 | +2 / +2 |
| t_NTT / t_INTT pada median Fmax (us, perhitungan tim) | 3.099 / 3.099 | 3.211 / 3.211 | +0.112 |
| Timing terpenuhi pada 40,000 ns, setiap seed | ya | ya | - |
| Kompilasi informasi 20 ns (seed 1) | tidak dijalankan | 9,443 ALM, setup -2.242 ns, Fmax 44.96 MHz, tidak terpenuhi | - |

Hasil aturan: tidak diadopsi oleh aturan (syarat 4: memerlukan median Fmax di atas 39.365 MHz). Verifikasi: lint bersih, 12/12 di kedua simulator, kontrol negatif gagal sesuai syarat, formal 3/3, regresi penuh OVERALL PASS.
