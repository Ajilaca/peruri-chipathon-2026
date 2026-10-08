# ADR 0023: Fase 5M S8: register jalur tulis dan satu bubble per arah (P = 8) - hasil aturan

- Status: Superseded by 0025
- Tanggal: 2026-10-03
- Diputuskan oleh: tidak diterima sebagai konfigurasi; digantikan ADR 0025 (Jevan, Team J5, chat 2026-10-03: "kan udah di adaptasi dan kita menggambil s10"; header sebelumnya "Proposed / menunggu keputusan tim")

## Konteks
- ADR 0017 langkah S8 (tuas 4: register di jalur tulis, P 7 -> 8, satu stall independen-data per transformasi,
  kompilasi informasi 20 ns); ADR 0019 catatan amandemen 2 (S7 dan S8 sebelum Fase 7); basis S7 (ADR 0021 Proposed;
  S8 dimulai di basis itu atas instruksi kerja tim 2026-10-02/03). Test plan dan aturan:
  `evidence/phase05m/test_plan_s8.md` (commit 01c8fb1, sebelum simulasi atau kompilasi S8 apa pun).
- Hanya file baru (`rtl/ntt/ntt_core_s8.sv`, `ntt_core_s8_p8.sv`); file memori S7 dipakai ulang dengan
  `WR_DELAY = WrDly + WR_REG`. Bubble: NTT setelah layer 3, INTT setelah layer 2 (posisi hanya bergantung pada mode
  dan layer).

## Opsi yang dipertimbangkan
(a) Mengadopsi S8 sebagai inti Fase 5M akhir. (b) Mempertahankan S7 (P = 7, 120 / 120 siklus) sebagai konfigurasi
untuk Fase 6 dan 7; S8 tetap eksperimen terukur. (c) Mempertahankan M6 atau basis lain.

## Keputusan
Hasil aturan yang ditetapkan lebih dulu (`scripts/quartus/phase5m_select_s8.py`, tanpa toleransi): S8 TIDAK diadopsi
oleh aturan: syarat 1-3 lolos; syarat 4 gagal (t = 122 / 37,990 = 3,211 us lawan S7 120 / 38,720 = 3,099 us; S8
memerlukan median Fmax di atas 39,365 MHz). Pilihan konfigurasi untuk fase berikutnya milik tim (C5): catatan ini tetap
Proposed. Saran (bukan keputusan): (b).

## Konsekuensi
- MEASURED (Quartus, seed 1-6, 40,000 ns; `evidence/phase05m/s8/selection_worksheet.md`): ALM 9.402-9.471 (median
  9.443,5; S7 9.391,0), register 4.130-4.144 (S7 4.296-4.324), M10K 33, DSP 16, timing terpenuhi di setiap seed,
  median Fmax 37,990 MHz (36,76-40,22) lawan S7 38,720 (37,89-40,29); siklus NTT = INTT = 122 (simulasi, seperti
  diprediksi: 113 + 8 + 1).
- INFERENCE: selisih median (0,73 MHz, -1,9 %) ada di dalam sebaran seed kedua langkah (S7 2,40 MHz, S8 3,46 MHz),
  jadi S8 "tidak lebih baik", bukan "terukur lebih buruk"; dengan dua siklus lebih banyak (+1,7 %) ia kalah dari aturan
  bagaimanapun. Hipotesis, tidak dianalisis: setelah S7 segmen tulis bukan lagi jalur pembatas, jadi satu register lagi
  menambah siklus tanpa memperpendek jalur terburuk. Jumlah register turun meski 192 bit ditambahkan: tidak diatribusikan.
- Kompilasi informasi 20 ns (MEASURED, `s8/quartus_S8-20.md`): 9.443 ALM, setup -2,242 ns (Slow -40C), Fmax 44,96 MHz,
  timing tidak terpenuhi; peringatan kritis 15725 dan 332148 x2 dibahas seperti fase sebelumnya, tidak ada yang diabaikan.
- Verifikasi (MEASURED): V1-V4 dan V6 di Verilator dan Icarus (masing-masing 12/12), kontrol negatif NC-B (tanpa
  bubble) dan NC-W (kendali tulis tidak ditunda) gagal sesuai syarat, formal H, O, R, A, B, C PASS dengan NC-O dan NC-A
  gagal (3/3), dan satu regresi penuh pada pohon akhir (Amandemen A1): Fase 0-5, S6, S7 semuanya OVERALL PASS, 95 file
  ditambah, 2 dokumen diubah sejak 288a78c (`s8/regression.md`).
- Tidak tercakup: perangkat keras, analisis jalur setelah S7 atau S8, seed atau batasan lain.

## Bukti
- `evidence/phase05m/test_plan_s8.md`, `s8/verify.md`, `s8/formal.md`, `s8/regression.md`,
  `s8/verification_status.json`, `s8/selection_worksheet.md`, `s8/quartus_S8[-s2..s6].md`, `s8/quartus_S8-20.md`,
  `s7/quartus_S7[-s2..s6].md` (baseline), `scripts/quartus/phase5m_select_s8.py`.

## Catatan amandemen 1 (2026-10-03, Jevan, Team J5)
Konsekuensi ADR 0025 (Accepted 2026-10-03, Jevan, Team J5, chat 2026-10-03: "kan udah di adaptasi dan kita menggambil
s10"): S10 adalah inti NTT/INTT untuk fase berikutnya. Baik opsi (a) S8 maupun opsi (b) S7 tidak dipakai. S8 tetap
tercatat seperti terukur dan tidak diadopsi oleh aturannya. Hasil aturan dan pengukuran di atas tidak berubah.
