<!-- claim-lint: skip-file (internal checkpoint record, not proposal text) -->
# Checkpoint Fase 5M S7: jalur baca memori terbelah (revisi S7) lawan M6

Rencana dan aturan: `evidence/phase05m/test_plan_s7.md` (ditetapkan sebelum RTL dan pengukuran). Catatan: ADR 0021 (ketika itu Proposed).

| Besaran | M6 (MEASURED) | S7 (MEASURED) | Delta (INFERENCE) |
|---|---:|---:|---:|
| ALM, median seed 1-6 (min-maks) | 9,421.5 (9,394-9,441) | 9,391.0 (9,361-9,405) | -30.5 |
| Register (min-maks) | sekitar 4,030-4,080 | 4,296-4,324 | sekitar +260 |
| DSP / M10K | 16 / 29 | 16 / 31 | 0 / +2 |
| Median Fmax, slow corner terendah (MHz) | 34.430 (32.35-35.04) | 38.720 (37.89-40.29) | +4.290 (+12.5 %) |
| Siklus NTT / INTT (simulasi) | 119 / 119 | 120 / 120 | +1 / +1 |
| t_NTT / t_INTT pada median Fmax (us, perhitungan tim) | 3.456 / 3.456 | 3.099 / 3.099 | -0.357 / -0.357 |
| Timing terpenuhi pada 40,000 ns, setiap seed | ya | ya | - |

Verifikasi (MEASURED): lint dan slang bersih; uji unit memori (RD_SPLIT = 1 dan 0) 8/8 dan uji diferensial terhadap memori beku 1/1 di kedua simulator; inti 6/6 (NTT, INTT,
round trip, data batas, siklus konstan 120 / 120, 512 vektor satuan INTT); NCD dan NCS gagal sesuai syarat; formal H, O, R, A, B, C PASS dengan NC-O dan NC-A gagal (3/3). V7 (regresi) tidak dijalankan
untuk S7, Amandemen A1.

Hasil aturan: diadopsi oleh aturan (keempat syarat PASS, tanpa toleransi). Penerimaan tim: ADR 0021 (ketika itu Proposed). S8 dimulai di basis ini.
