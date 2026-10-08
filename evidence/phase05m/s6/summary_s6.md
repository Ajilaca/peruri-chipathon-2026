<!-- claim-lint: skip-file (internal checkpoint record, not proposal text) -->
# Checkpoint Fase 5M S6: INTT tanpa lintasan skala (revisi M6) lawan C4b-B

Rencana dan aturan: `evidence/phase05m/test_plan.md` (ditetapkan sebelum RTL dan pengukuran). Catatan: ADR 0020 (ketika itu Proposed).

| Besaran | C4b-B (MEASURED) | M6 (MEASURED) | Delta (INFERENCE) |
|---|---:|---:|---:|
| ALM, median seed 1-6 (min-maks) | 9,171.0 (9,166-9,208) | 9,421.5 (9,394-9,441) | +250.5 |
| DSP / M10K | 18 / 29 | 16 / 29 | -2 / 0 |
| Median Fmax, slow corner terendah (MHz) | 34.515 (33.46-34.84) | 34.430 (32.35-35.04) | -0.085 (-0.25 %) |
| Siklus NTT / INTT (simulasi) | 119 / 375 | 119 / 119 | 0 / -256 |
| t_NTT / t_INTT pada median Fmax (us, perhitungan tim) | 3.448 / 10.865 | 3.456 / 3.456 | +0.008 / -7.409 |
| Timing terpenuhi pada 40,000 ns, setiap seed | ya | ya | - |

Verifikasi (MEASURED): lint Verilator -Wall dan slang bersih; `intt_halving` acuan = `intt` (12 pytest); ROM dibangkitkan dan diperiksa; `half_mod` menyeluruh
3,329/3,329; inti: test Fase 4 tidak berubah 5/5, INTT 512 vektor satuan 1/1 di Verilator dan Icarus; tiga kontrol negatif gagal sesuai syarat; formal H, O, R, A, B, C
PASS dengan NC-O dan NC-A gagal (3/3). V9 (regresi Fase 0-5) tidak dijalankan, Amandemen A1.

Hasil aturan: tidak diadopsi (hanya bagian NTT ADR 0012 yang gagal, sebesar 0.008 us; tidak ada toleransi yang ditambahkan). Keputusan langkah berikutnya: tim (ADR 0020).
