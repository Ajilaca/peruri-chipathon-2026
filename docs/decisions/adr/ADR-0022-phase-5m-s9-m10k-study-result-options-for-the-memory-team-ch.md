# ADR 0022: Fase 5M S9: hasil studi M10K, opsi untuk memori (pilihan tim)

- Status: Superseded by 0025
- Tanggal: 2026-10-03
- Diputuskan oleh: opsi (A) dibangun sebagai S10 dan diterima di ADR 0025 (Jevan, Team J5, chat 2026-10-03: "kan udah di adaptasi dan kita menggambil s10"; header sebelumnya "Proposed / menunggu keputusan tim")

## Konteks
- ADR 0017 mendefinisikan S9 sebagai studi hanya-dokumentasi tanpa aturan adopsi ("tim memilih"); ADR 0019 telah
  melepasnya untuk batas waktu; tim memintanya di chat pada 2026-10-03 ("s9 sekalian dikerjain", dicatat di ADR 0019
  catatan amandemen 3). Rencana: `evidence/phase05m/test_plan_s9.md` (ditulis sebelum skrip analisis).
- Batas terukur inti adalah jalur pembacaan memori (ADR 0010; S7 mengonfirmasinya: median Fmax 34,430 -> 38,720 MHz
  dengan satu register di pembacaan). Penyimpanan adalah flip-flop (tanpa M10K).

## Opsi yang dipertimbangkan
(A) 16 bank 1R1W dengan peta `bank = (a1^a2^a3^a4, a7, a6, a5)`, `offset = a[3:0]`, satu M10K per bank, crossbar,
    tanpa arbitrasi slot (langkah baru, "S10").
(B) dua koefisien per word (tidak berguna: hanya satu layer per arah yang diuntungkan); (C) double-pumping (memerlukan
domain clock kedua dan frekuensi maksimum M10K, BELUM DIVERIFIKASI); (D) lajur lebih sedikit (siklus berlipat);
(E) mempertahankan memori flip-flop S7 dan melanjutkan ke Fase 6 / 7.

## Keputusan
Tidak ada yang dibuat di sini (C5). Saran (bukan keputusan): (E) sekarang; buka (A) sebagai langkah tersendiri setelah
blok kritis batas waktu (Keccak, sampler), dengan test plan dan aturan ADR 0012.

## Konsekuensi
- MEASURED oleh model jadwal alamat nyata (`evidence/phase05m/s9/port_analysis.txt`): peta 8 bank saat ini
  memerlukan 2 pembacaan + 2 penulisan per bank pada beberapa siklus, yang tidak muat di satu M10K true-dual-port per
  bank (fakta mode device tidak diverifikasi ulang di sini); peta 16 bank di atas memerlukan tepat 1 pembacaan + 1
  penulisan per bank per siklus di seluruh lini waktu kedua arah, bijektif dan seimbang; peta pertama yang diturunkan
  tangan salah dan dibantah skrip (test plan Amandemen A1); dua kontrol negatif konflik sesuai syarat.
- ESTIMATE (metode di studi): opsi A memakai 16 M10K (2,9 % dari 553), menghapus sekitar 3.000 flip-flop penyimpanan,
  menambah crossbar paling banyak sekitar 1.920 ALM (batas atas dengan hitungan LUT, tidak diukur); efek Fmax BELUM DIUKUR.
- Tidak ada yang berubah di RTL, test, atau bukti oleh S9; tidak perlu regresi untuknya.
- Terbuka sebelum RTL apa pun: mode read-during-write M10K, latensi baca-sinkron, pemeriksaan Cyclone V Device
  Handbook, ROM crossbar, properti bank formal baru.

## Bukti
- `evidence/phase05m/test_plan_s9.md`, `s9/study_m10k.md`, `s9/port_analysis.txt`, `scripts/test/phase5m_s9_port_analysis.py`.

## Catatan amandemen 1 (2026-10-03, Jevan, Team J5)
Konsekuensi ADR 0025 (Accepted 2026-10-03, Jevan, Team J5, chat 2026-10-03: "kan udah di adaptasi dan kita menggambil
s10"): S10 adalah inti NTT/INTT untuk fase berikutnya. Opsi (A) studi ini dibangun dan diukur sebagai S10 (urutan ADR
0024, hasil ADR 0025). ESTIMATE crossbar studi terlalu rendah (entitas memori terukur 3.343 ALM,
`evidence/phase06/s10/resource_breakdown.md`). Teks studi di atas tidak berubah.
