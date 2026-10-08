# Ringkasan Fase 5c (C4c, masukan INTT malas): terukur, tidak diadopsi

Aturan: ADR 0014 bagian 4, diterapkan tanpa perubahan oleh `scripts/quartus/phase5_select_5c.py` (`selection_worksheet.md`).

| Butir | C4c (seed 1-6) | C4b-B (Barrett 5b, seed 1-6) | Sumber |
|---|---|---|---|
| Median ALM (min-maks) | 9,059.5 (9,032-9,094) | 9,171.0 (9,166-9,208) | MEASURED, `quartus_C4c*.md`, `../5b/quartus_C4b-B*` |
| Median Fmax, slow corner terendah (min-maks) MHz | 33.100 (32.27-35.26) | 34.515 (33.46-34.84) | MEASURED, file yang sama; median = INFERENCE |
| t_NTT / t_INTT pada median Fmax (us) | 3.595 / 11.329 | 3.448 / 10.865 | perhitungan tim (119 / 375 siklus) |
| Siklus NTT / INTT | 119 / 375 | 119 / 375 | MEASURED (simulasi), `verification_status.json` |
| DSP / M10K | 18 / 29 | 18 / 29 | MEASURED |

Hasil: C4c TIDAK diadopsi (median Fmax dan syarat ADR 0012 gagal; empat syarat lain lolos).
Rentang seed saling tumpang tindih (seed 2 C4c = 35.26 MHz di atas setiap seed C4b-B), jadi selisih median tidak
dapat dibedakan dari derau seed (INFERENCE); aturan ditetapkan sebelum mengukur dan tidak dibuka kembali.

## Analisis jalur sesudahnya (slack MEASURED, `quartus_sta` pada salinan, tanpa kompilasi ulang; Slow 1100mV 100C)
- `c4c_segments_slow100.txt`: seed 2 (terbaik) dan seed 3 (terburuk). Setiap segmen pengali punya slack di atas 17 ns
  (cut2 lajur ke penulisan memori 17.831 / 18.470 ns; cut0 ke cut1 dan cut1 ke cut2 di atas 32 ns).
- `C4c-s2_top300_path_classes_slow100.txt`, `C4c-s3_top300_path_classes_slow100.txt`: kelas terburuk pada kedua seed
  adalah register sisi pembacaan memori (`g_arb[*].g_reg.en_q` / `bank_q`) ke cut masukan pengali (`u_mul.cut0`):
  slack terburuk 11.806 ns (seed 2) dan 9.172 ns (seed 3), lawan 11.221 ns untuk C4b-B seed 1.
- HIPOTESIS (tidak diuji): jalur pembacaan-ke-masukan-pengali masih menjadi batas, jadi mengganti `sub_mod` dengan
  penjumlah hanya sedikit memengaruhi, dan sebaran 2.6 ns antara dua seed C4c lebih besar dari selisih terhadap C4b-B.
  Menetapkan sebab memerlukan eksperimen terkendali (misalnya lebih banyak seed atau perubahan tingkat jalur), yang tidak dijalankan.
