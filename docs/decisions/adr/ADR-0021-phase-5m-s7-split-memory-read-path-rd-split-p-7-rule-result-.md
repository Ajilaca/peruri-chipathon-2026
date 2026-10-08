# ADR 0021: Fase 5M S7: jalur baca memori terbelah (RD_SPLIT, P = 7) - hasil aturan dan basis untuk S8

- Status: Superseded by 0025
- Tanggal: 2026-10-02
- Diputuskan oleh: tidak diterima sebagai konfigurasi; digantikan ADR 0025 (Jevan, Team J5, chat 2026-10-03: "kan udah di adaptasi dan kita menggambil s10"; header sebelumnya "Proposed / menunggu keputusan tim")

## Konteks
- ADR 0017 langkah S7 (tuas 1 paket keputusan: satu tahap register di dalam pembacaan memori, P 6 -> 7, tanpa stall,
  +1 siklus); ADR 0019 catatan amandemen 2 (S7 dan S8 direncanakan sebelum Fase 7); ADR 0020 (M6 adalah basis). Test
  plan dan aturan adopsi ditulis dan di-commit sebelum RTL S7 apa pun dan sebelum pengukuran S7 apa pun
  (`evidence/phase05m/test_plan_s7.md`, commit f39b074).
- Perubahan S7 hanya berupa file baru (`rtl/mem/poly_mem_multiport_split.sv`, `rtl/ntt/ntt_core_s7.sv`,
  `ntt_core_s7_p7.sv`); tidak ada file yang ada yang diubah.

## Opsi yang dipertimbangkan
(a) Mengadopsi S7 sebagai basis S8 dan fase berikutnya (aturan di bawah menyatakan lolos).
(b) Mempertahankan M6 (P = 6) sebagai konfigurasi NTT/INTT dan memperlakukan S7 sebagai eksperimen terukur.
(c) Basis lain yang dipilih tim.

## Keputusan
Hasil aturan yang ditetapkan lebih dulu (`scripts/quartus/phase5m_select_s7.py`, tanpa toleransi): S7 diadopsi oleh
aturan (keempat syarat PASS). Apakah tim menerimanya sebagai konfigurasi tidak diputuskan di sini (C5): status tetap
Proposed. Karena alasan jadwal, pekerjaan S8 dimulai di basis S7 (S8 didefinisikan sebagai tuas 4 di atas pembacaan
terbelah, tabel ADR 0017) mengikuti instruksi kerja tim 2026-10-02 (chat: "kerjakan sesuai dengan agenda hari ini ...
s7-s8 selesai"); bila tim memilih (b) atau (c), vonis S8 lalu dibaca sebagai eksperimen terukur di S7.

## Konsekuensi
- MEASURED (Quartus, seed 1-6, 40,000 ns; `evidence/phase05m/s7/selection_worksheet.md`): ALM 9.361-9.405 (median
  9.391,0; median M6 9.421,5), register 4.296-4.324, M10K 31 (M6 29), DSP 16, timing terpenuhi di setiap seed, median
  Fmax 38,720 MHz (37,89-40,29) lawan M6 34,430 MHz (32,35-35,04); siklus NTT = INTT = 120 (simulasi).
- INFERENCE (perhitungan tim): t_NTT = t_INTT = 120 / 38,720 = 3,099 us lawan M6 3,456 us (-10,3 %). Seed S7 terendah
  (37,89 MHz) di atas seed M6 tertinggi (35,04 MHz), jadi kenaikan Fmax lebih besar dari sebaran seed yang terlihat
  sejauh ini (sebaran S7 2,40 MHz). Slack setup terburuk pada 40 ns naik ke 13,6-15,2 ns (M6 sekitar 11 ns dalam
  istilah C4b-B).
- Ambang yang tercetak di test plan (34,720 MHz) adalah nilai bulat dari 120 x 34,430 / 119 = 34,7193; pembulatan tidak
  berpengaruh pada vonis.
- Kenaikan tidak diprediksi sebesar ini pada ESTIMATE rencana (sekitar 40 MHz untuk jalur terburuk 25 ns; median
  terukur 38,7 MHz ada di dalam batas itu).
- ALM tidak naik (median -30 terhadap M6, di dalam sebaran seed 44 ALM, INFERENCE) meski sekitar 270 register
  ditambahkan; M10K naik dari 29 ke 31 (disimpulkan alat, tidak dianalisis).
- Tidak tercakup: perangkat keras, seed atau batasan lain, analisis jalur setelah S7 (jalur kritis baru tidak diperiksa;
  hanya menjadi masukan ekspektasi S8 sebagai hipotesis), regresi Fase 0-5 (dijalankan sekali di S8, Amandemen A1).
- Verifikasi (MEASURED): V1-V6 PASS di Verilator dan Icarus (`s7/verify.md`), formal H, O, R, A, B, C PASS dengan NC-O
  dan NC-A gagal (`s7/formal.md`); kontrol negatif NCD (kendali tulis kurang satu siklus) dan NCS (pemilih keluaran
  tidak ditunda) gagal sesuai syarat; RD_SPLIT = 0 sama dengan memori beku siklus demi siklus (V3). Build cocotb
  Verilator mencetak `WIDTHEXPAND` untuk nilai parameter ARB_REG 32 bit dari runner; lint RTL (V1) bersih.

## Bukti
- `evidence/phase05m/test_plan_s7.md`, `s7/verify.md`, `s7/formal.md`, `s7/verification_status.json`,
  `s7/selection_worksheet.md`, `s7/quartus_S7[-s2..s6].md`, `s6/quartus_M6[-s2..s6].md` (baseline),
  `scripts/quartus/phase5m_select_s7.py`.

## Catatan amandemen 1 (2026-10-03, Jevan, Team J5)
Konsekuensi ADR 0025 (Accepted 2026-10-03, Jevan, Team J5, chat 2026-10-03: "kan udah di adaptasi dan kita menggambil
s10"): S10 adalah inti NTT/INTT untuk fase berikutnya. S7 tidak dipakai sebagai konfigurasi; tetap tercatat sebagai
basis terukur S8 dan sebagai baseline perbandingan S10 (`evidence/phase06/s10/selection_worksheet.md`). Hasil aturan
dan pengukuran di atas tidak berubah.
