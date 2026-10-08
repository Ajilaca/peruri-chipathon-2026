# ADR 0025: S10 (di dalam Fase 6): memori 16 bank 1R1W tanpa arbitrasi slot - hasil aturan

- Status: Accepted
- Tanggal: 2026-10-03
- Diputuskan oleh: Jevan, Team J5, chat 2026-10-03: "kan udah di adaptasi dan kita menggambil s10" (header sebelumnya "Proposed / menunggu keputusan tim")

## Konteks
- ADR 0024 (Accepted): S10 dikerjakan di dalam Fase 6 setelah blok Fase 6. ADR 0022 (Proposed) opsi A: peta 16 bank
  `bank = (a1^a2^a3^a4, a7, a6, a5)`, `offset = a[3:0]` bebas konflik (satu pembacaan, satu penulisan per bank per
  siklus) di seluruh jadwal. Analisis jalur S7 (permintaan tim "jalankan opsi 1 dan 2") menunjukkan riak arbitrasi
  slot sebagai batas S7 (`evidence/phase05m/fmax50/path_analysis.md`).
- Test plan dan aturan ditulis sebelum RTL dan pengukuran: `evidence/phase06/test_plan_s10.md` (Amandemen A1: batas
  latensi start pada uji inti diturunkan dari pengaman tulis-host; tidak ada ambang yang diubah).
- Hanya file baru: `rtl/mem/poly_mem_m10k.sv`, `rtl/ntt/ntt_core_s10.sv`, `ntt_core_s10_p5.sv`,
  `rtl/sched/kpke_sched_top_s10.sv`.

## Opsi yang dipertimbangkan
(a) Mengadopsi S10 sebagai inti NTT/INTT untuk fase berikutnya (dan top Fase 6 dengan S10). (b) Mempertahankan S7.
(c) Lainnya.

## Keputusan
Hasil aturan yang ditetapkan lebih dulu (`scripts/quartus/select_s10.py`, tanpa toleransi): S10 diadopsi oleh aturan
(semua syarat PASS). Penerimaan sebagai konfigurasi milik tim (C5): catatan ini sebelumnya Proposed.

## Konsekuensi
- MEASURED (Quartus, seed 1-6, 40,000 ns; `evidence/phase06/s10/selection_worksheet.md`): ALM 5.045-5.091 (median
  5.077,0; S7 9.391,0), register 543-555 (S7 4.296-4.324; penyimpanan pindah ke blok RAM), M10K 24 (S7 31), DSP 16,
  timing terpenuhi di setiap seed, median Fmax 44,320 MHz (42,34-46,65) lawan S7 38,720 (37,89-40,29); siklus NTT =
  INTT = 118 (simulasi). t = 118 / 44,320 = 2,662 us lawan 3,099 us (perhitungan tim, -14 %).
- MEASURED pada 20,000 ns (informasi, seed 1-6): timing terpenuhi di 6 dari 6 seed (setup terburuk +0,792 sampai
  +1,718 ns, Fmax corner terendah 52,06-54,70 MHz); S7 pada 20 ns terpenuhi 0 dari 6. Ini kompilasi kernel-only dengan
  virtual pin (tanpa papan, tanpa clock sistem): menunjukkan inti memenuhi batasan 20 ns dalam alur ini, bukan sistem
  yang berjalan pada 50 MHz.
- Seed S10 terendah pada 40 ns (42,34 MHz) di atas seed S7 tertinggi (40,29 MHz): kenaikannya lebih besar dari
  sebaran seed (INFERENCE).
- Verifikasi: memori, inti, kontrol negatif (peta tanpa bit XOR, tulis kurang satu siklus), top Fase 6 dengan S10
  (KeyGen 5.475 / Encrypt 6.789 / Decrypt 3.109 siklus) di Verilator dan Icarus; formal 3/3.
- Peringatan kritis: hanya 15725 (clock virtual pin), pada setiap kompilasi 20 ns dan 40 ns; tidak ada yang diabaikan.
- Tidak tercakup: perangkat keras, analisis jalur setelah S10, mode read-during-write M10K di perangkat keras (jadwal
  tidak pernah membaca dan menulis satu word pada satu siklus: properti formal C).

## Bukti
- `evidence/phase06/test_plan_s10.md`, `s10/verify.md`, `s10/formal.md`, `s10/verification_status.json`,
  `s10/selection_worksheet.md`, `s10/quartus_S10[-s2..s6].md`, `s10/quartus_S10-20[-s2..s6].md`,
  `evidence/phase05m/fmax50/` (S7 pada 20 ns, analisis jalur), `scripts/quartus/select_s10.py`.

## Catatan amandemen 1 (2026-10-03, Jevan, Team J5)
Tim menerima opsi (a): S10 (`rtl/ntt/ntt_core_s10_p5.sv` dengan `rtl/mem/poly_mem_m10k.sv`) adalah inti NTT/INTT untuk
fase berikutnya, dan `rtl/sched/kpke_sched_top_s10.sv` adalah top Fase 6 yang dipakai mulai sekarang. Menutup PENDING
#28 dan, seperti tertulis di teksnya, membuat pertanyaan S7 / S9 pada #27 tidak relevan; ADR 0021, 0022, dan 0023
ditandai digantikan oleh catatan ini. Hasil aturan dan pengukuran di atas tidak berubah.
