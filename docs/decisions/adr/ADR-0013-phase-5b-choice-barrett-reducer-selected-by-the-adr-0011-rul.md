# ADR 0013: Pilihan Fase 5b: reducer Barrett dipilih oleh aturan ADR 0011

- Status: Accepted
- Tanggal: 2026-10-01
- Diputuskan oleh: Jevan, Team J5 (chat 2026-10-02, menjawab tiga pertanyaan ADR)

## Konteks
- `docs/ROADMAP.md` Fase 5b: Montgomery lawan Barrett di balik antarmuka yang sama, keduanya diukur, "pilihan lewat ADR".
- ADR 0011 (Accepted) menetapkan aturan seleksi (D8) dan seed (D7, seed 1-6) sebelum kompilasi 5b apa pun.
- Kedua kandidat dibangun, diverifikasi, dan dikompilasi (test plan `evidence/phase05/test_plan.md`, amandemen A3):
  - kebenaran (MEASURED, kedua simulator): uji reducer menyeluruh 0 selisih pada semua a, b di [0, q) untuk masing-masing;
    uji unit 40/40; uji inti 22/22 termasuk siklus persis 119 / 375, pemeriksaan ROM Montgomery, dan kontrol negatif;
    formal 9/9 sesuai harapan (`evidence/phase05/5b/verify.txt`, `formal.md`);
  - Quartus, 40,000 ns, bawaan Quartus, seed 1-6 (MEASURED, `evidence/phase05/5b/quartus_C4b-*.md`),
    aturan diterapkan oleh `scripts/quartus/phase5_select_5b.py` (`evidence/phase05/5b/selection_worksheet.md`):

| Kandidat | Memenuhi syarat di 6 seed | Median ALM (min-maks) | Median Fmax, slow corner terendah (min-maks) | DSP | t_NTT pada median Fmax |
|---|---|---:|---:|---:|---:|
| Barrett (C4b-B) | ya | 9.171,0 (9.166-9.208) | 34,515 MHz (33,46-34,84) | 18 / 112 | 3,448 µs |
| Montgomery (C4b-M) | ya | 9.286,5 (9.249-9.297) | 33,780 MHz (32,81-34,25) | 9 / 112 | 3,523 µs |

## Opsi yang dipertimbangkan
1. Menerima hasil aturan: Barrett. Langkah aturan (ADR 0011 D8): keduanya memenuhi syarat; Barrett punya median Fmax
   lebih tinggi dan Montgomery 2,13 % lebih rendah, hampir seri (≤ 5 %); pada hampir seri median ALM lebih rendah
   menang; median ALM berbeda 115,5 ALM (≥ 32), jadi aturan memilih Barrett tanpa pemecah seri dari tim.
2. Menimpa aturan demi Montgomery karena pemakaian DSP (9, bukan 18). ADR 0011 D2 tidak menetapkan batas DSP, jadi
   aturan tidak menimbang DSP; penimpaan akan menjadi keputusan tim dengan alasan sendiri.

## Keputusan
(Diterima 2026-10-02 oleh Jevan, Team J5: Barrett, seperti dipilih aturan; biaya DSP di bawah ditunjukkan sebelum
pilihan.) Barrett (`rtl/arith/modmul_barrett.sv`, RED_KIND 2, revisi C4b-B) adalah pilihan Fase 5b, seperti dipilih
oleh aturan ADR 0011.

Dicatat eksplisit: pemakaian DSP berlipat dari 9 menjadi 18 (dari 112, penyebut fitter). Per entitas (MEASURED, seed 1,
`quartus/phase05_arith_c4/output_files_C4b-B/C4b-B.fit.rpt`): masing-masing dari sembilan reducer Barrett memakai
2 blok DSP dan 20,5-26,5 ALM, total 225,3 ALM (INFERENCE: DSP kedua memegang estimasi hasil bagi x·5039, satu-satunya
perkalian selain a·b yang diserahkan RTL ke alat); Montgomery memakai 1 DSP dan 37,7-42,1 ALM masing-masing
(total 352,0 ALM; perkalian q'-nya adalah penjumlahan geser). C3-P6 dan C4a memakai 9 DSP.

## Konsekuensi
- Konfigurasi C4 yang dibawa ke 5c / 5d dan ke kompilasi informasi 20,000 ns (ADR 0011 D1) adalah C4b-B, kecuali tim
  menolak ADR ini.
- DSP: 18 dari 112 untuk inti NTT (MEASURED). Tidak ada anggaran DSP; Keccak, sampler, dan blok lain BELUM DIUKUR,
  jadi apakah DSP menjadi langka nanti tidak diketahui. Bila batas DSP ditetapkan kelak, Montgomery (9 DSP, +115,5 ALM
  median) adalah alternatif terukur, atau Barrett dengan x·5039 ditulis sebagai penjumlahan geser (belum dibangun,
  BELUM DIUKUR).
- File Montgomery (`modmul_montgomery.sv`, `twiddle_rom_mont.sv`, generator, pemeriksaan ROM) tetap di repository
  sebagai kandidat terukur.
- Dibanding C3-P6 (INFERENCE): median ALM 9.171 lawan 10.484-10.516 (sekitar −1.330); median Fmax 34,515 MHz lawan
  rentang seed C3-P6 32,60-34,20 MHz (median 33,11, `evidence/phase04/seed_sweep.md`). Jalur kritis tetap di jalur
  pembacaan memori (`5b/C4b-B_top300_path_classes_slow100.txt`); 50 MHz tidak tercapai (ADR 0010).

## Bukti
- `evidence/phase05/5b/selection_worksheet.md`, `verification_status.json`,
  `verify.txt`, `formal.md`, `quartus_C4b-{B,M}[-s2..s6].md`,
  `C4b-{B,M}_top300_path_classes_slow100.txt`, `c4b_segments_slow100.txt`
- `docs/decisions/adr/ADR-0011-phase-5-plan-decisions-d1-d8-and-the-5b-selection-rule.md`
- `evidence/phase05/test_plan.md` (amandemen A3)
