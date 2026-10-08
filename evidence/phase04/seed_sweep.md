<!-- claim-lint: skip-file (internal experiment record, not proposal text) -->
# Sapuan seed fitter Fase 4, P = 4 dan P = 6 (masukan untuk ADR 0008)

- Tanggal (UTC): 2026-10-01. Diminta tim setelah ADR 0008 diusulkan, karena margin ALM (P = 4: 39
  di bawah anggaran 10,478, P = 6: 27 di atasnya) lebih kecil daripada ayunan pengepakan fitter yang terlihat di Fase 3.
- Apa yang berubah: hanya `set_global_assignment -name SEED <n>` (n = 2..6) pada salinan `C3-P4.qsf` / `C3-P6.qsf`
  (`quartus/phase04_pipeline_c3/C3-P{4,6}-s{2..6}.qsf`). Seed 1 adalah bawaan yang dipakai revisi terukur
  (dikonfirmasi di laporan fitter mereka). RTL (git 7947c0c), SDC (40.000 ns), dan setiap assignment lain identik.
- Alat: Quartus Prime Lite 25.1std.0 Build 1129. Evidence per seed diekstrak dengan `extract_quartus_report.py` ke
  `evidence/phase04/seed_sweep/`; tabel di bawah dibangkitkan oleh `python3 scripts/quartus/phase4_seed_sweep_summary.py`.
- Sapuan ini tidak mengubah worksheet terukur (`selection_worksheet.md`), aturan ADR 0007, atau
  test plan, yang menetapkan seed bawaan. Ia informasi untuk keputusan tim tentang ADR 0008.

## Hasil (MEASURED)
| P | Seed | ALM | <= 10,478? | Register | M10K | Slack setup / hold terburuk (ns) | Timing terpenuhi? | Fmax(P) slow corner terendah (MHz) | t_NTT (us) | Memenuhi semua kondisi ADR 0007? | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 1 (bawaan) | 10,439 | ya | 4145 | 26 / 553 | 8.734 / 0.157 | ya | 31.98 | 3.659 | ya | `evidence/phase04/quartus_C3-P4.md` |
| 4 | 2 | 10,503 | tidak | 4160 | 26 / 553 | 9.482 / 0.143 | ya | 32.77 | 3.570 | tidak | `evidence/phase04/seed_sweep/quartus_C3-P4-s2.md` |
| 4 | 3 | 10,479 | tidak | 4151 | 26 / 553 | 7.324 / 0.129 | ya | 30.60 | 3.824 | tidak | `evidence/phase04/seed_sweep/quartus_C3-P4-s3.md` |
| 4 | 4 | 10,472 | ya | 4166 | 26 / 553 | 8.555 / 0.120 | ya | 31.80 | 3.679 | ya | `evidence/phase04/seed_sweep/quartus_C3-P4-s4.md` |
| 4 | 5 | 10,467 | ya | 4160 | 26 / 553 | 7.580 / 0.118 | ya | 30.85 | 3.793 | ya | `evidence/phase04/seed_sweep/quartus_C3-P4-s5.md` |
| 4 | 6 | 10,468 | ya | 4149 | 26 / 553 | 9.701 / 0.130 | ya | 33.00 | 3.545 | ya | `evidence/phase04/seed_sweep/quartus_C3-P4-s6.md` |
| 6 | 1 (bawaan) | 10,505 | tidak | 4168 | 29 / 553 | 10.753 / 0.140 | ya | 34.19 | 3.481 | tidak | `evidence/phase04/quartus_C3-P6.md` |
| 6 | 2 | 10,508 | tidak | 4153 | 29 / 553 | 9.773 / 0.139 | ya | 33.08 | 3.597 | tidak | `evidence/phase04/seed_sweep/quartus_C3-P6-s2.md` |
| 6 | 3 | 10,511 | tidak | 4160 | 29 / 553 | 9.328 / 0.132 | ya | 32.60 | 3.650 | tidak | `evidence/phase04/seed_sweep/quartus_C3-P6-s3.md` |
| 6 | 4 | 10,516 | tidak | 4152 | 29 / 553 | 10.756 / 0.128 | ya | 34.20 | 3.480 | tidak | `evidence/phase04/seed_sweep/quartus_C3-P6-s4.md` |
| 6 | 5 | 10,504 | tidak | 4139 | 29 / 553 | 9.824 / 0.144 | ya | 33.14 | 3.591 | tidak | `evidence/phase04/seed_sweep/quartus_C3-P6-s5.md` |
| 6 | 6 | 10,484 | tidak | 4162 | 29 / 553 | 9.764 / 0.131 | ya | 33.07 | 3.598 | tidak | `evidence/phase04/seed_sweep/quartus_C3-P6-s6.md` |

| P | ALM min / median / maks | Seed dalam 10,478 | Fmax min / median / maks (MHz) | Seed yang memenuhi semua kondisi ADR 0007 |
|---|---|---|---|---|
| 4 | 10,439 / 10,470.0 / 10,503 | 4 dari 6 | 30.60 / 31.89 / 33.00 | 4 dari 6 |
| 6 | 10,484 / 10,506.5 / 10,516 | 0 dari 6 | 32.60 / 33.11 / 34.20 | 0 dari 6 |

Per seed, aturan ADR 0007 diterapkan hanya pada {P=4, P=6} (P=0 dan P=2 tidak disapu; pada seed bawaan keduanya gagal timing pada 40.000 ns):

| Seed | Kandidat di antara {4, 6} | Hasil aturan |
|---|---|---|
| 1 | {4} | P = 4 |
| 2 | {} | tidak ada kandidat |
| 3 | {} | tidak ada kandidat |
| 4 | {4} | P = 4 |
| 5 | {4} | P = 4 |
| 6 | {4} | P = 4 |

## Membaca hasil
- Timing bukan masalahnya. Semua 12 kompilasi memenuhi 40.000 ns (setup dan hold, setiap corner). Fmax slow corner terendah
  P = 4 berkisar 30.60–33.00 MHz antar seed, P = 6 32.60–34.20 MHz.
- Kondisi ALM-lah masalahnya. P = 6 melebihi anggaran 10,478 di setiap seed (10,484–10,516), jadi P = 6 tidak pernah
  menjadi kandidat. P = 4 berkisar 10,439–10,503 ALM dan dalam anggaran di 4 dari 6 seed; pada seed 2 dan 3 ia melebihi
  (sebesar 25 dan 1 ALM), dan pada seed itu tidak ada kandidat sama sekali.
- Aturan per seed tidak pernah memilih selain P = 4; ia memilih P = 4 atau tidak memilih apa pun.
- Register bervariasi sedikit menurut seed (duplikasi/pengepakan register oleh fitter); M10K (26 untuk P = 4, 29 untuk
  P = 6) dan DSP (9) tidak.
- Sebaran seed di sini 64 ALM (P = 4) dan 32 ALM (P = 6). Itu jauh lebih kecil daripada ayunan ~370 ALM
  yang tercatat di Fase 3 (K2 pada L = 1, `docs/results/phase03.md`); sapuan ini tidak menjelaskan ayunan itu dan
  tidak menunjukkan bahwa perubahan RTL berikutnya akan tetap dalam 64 ALM.

## Catatan proses (dinyatakan apa adanya)
- Upaya sapuan pertama terputus di seed 4 saat sesi berakhir; database seed-4 yang setengah tertulis
  rusak. Dua rantai lalu dijalankan paralel, yang membuat Quartus menulis ulang `.qpf` bersama secara bersamaan dan
  menghilangkan satu baris revisi (P4 seed 5 gagal dengan "Revision does not exist"). Tiga kompilasi yang terkena (P4 s4,
  P6 s4, P4 s5) dijalankan ulang satu per satu setelah menghapus database mereka dan memulihkan `.qpf`; laporan fitter
  mereka mengonfirmasi seed 4 / 4 / 5. Tujuh kompilasi yang berhasil pada run paralel diperiksa seed dan top entity-nya
  di laporan masing-masing (semua benar). Tidak ada hasil yang diambil dari run yang gagal.
- Peringatan kritis di semua 10 kompilasi baru: hanya 15725 (clock virtual pin), seperti di setiap revisi Fase 1–4;
  tidak ada 332148 (timing terpenuhi).
