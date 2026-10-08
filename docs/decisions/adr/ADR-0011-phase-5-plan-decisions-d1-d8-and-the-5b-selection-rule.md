# ADR 0011: Keputusan rencana Fase 5 D1-D8 dan aturan seleksi 5b

- Status: Accepted
- Tanggal: 2026-10-01
- Diputuskan oleh: Faza Dzil, Team J5 (sesi 2026-10-01: "terima semua saran")

## Konteks
Test plan Fase 5 (`evidence/phase05/test_plan.md`, CRG-4) mendaftar delapan pertanyaan terbuka (§13, D1-D8) dengan
saran untuk masing-masing, dan usulan aturan seleksi untuk langkah 5b (§11) yang harus ditetapkan sebelum revisi 5b
mana pun dikompilasi (seperti ADR 0004 / ADR 0007). Tujuan timing Fase 5 ada di ADR 0010. Titik awal: C3-P6
(ADR 0009), MEASURED di `evidence/phase04/quartus_C3-P6.md` dan
`evidence/phase05/baseline/c3p6_critical_path.md`.

## Opsi yang dipertimbangkan
Untuk tiap butir, opsinya adalah yang ada di test plan §13 dan §3; saran diterima di setiap kasus.

## Keputusan
| # | Keputusan |
|---|---|
| D1 | Setiap revisi Quartus Fase 5 (C4a-C4d) memakai `create_clock -period 40.000` pada `clk_i`, seperti C3-P6. Pada akhirnya, konfigurasi C4 akhir dan C3-P6 masing-masing dikompilasi sekali lagi pada 20,000 ns; kedua hasil itu informasi, bukan gerbang (ADR 0010). |
| D2 | Anggaran inti NTT tetap 12.573 ALM (ADR 0009). Kompilasi memakai bawaan Quartus seperti di Fase 4 (sebanding dengan C3-P6); kompilasi dengan setelan GHRD untuk C4 akhir bersifat opsional. Pemakaian DSP dilaporkan; tidak ada batas DSP. |
| D3 | Apakah 5c dan 5d dicoba ditentukan setelah hasil 5a / 5b; test plan menyimpan kedua rencana (5c bukti batas formal; 5d sebagai unit mandiri, karena `base_case_multiply.sv` bukan bagian C3-P6). |
| D4 | Pembacaan (ii) untuk 5a: reducer fold khusus q memakai q = 2^11 + 2^10 + 2^8 + 1 (2^12 ≡ 767 mod q, hanya penjumlahan geser, lalu jumlah tetap pengurangan bersyarat). 5b = Barrett dan Montgomery, yang pada keduanya perkalian dengan q adalah penjumlahan geser. |
| D5 | Di Fase 5 tidak ada register yang dipindah antara jalur memori dan jalur pengali; jalur pengali tetap persis 3 register (P = 6, siklus 119 / 375 tidak berubah). Posisi tepat di dalam tiap reducer baru ditulis di test plan sebelum kompilasinya. |
| D6 | Kontrak operand: reducer baru harus sama dengan (a·b) mod q untuk semua a, b di [0, q) (menyeluruh); perilaku untuk operand 12 bit ≥ q diukur dan dilaporkan, tidak disyaratkan. |
| D7 | Seed fitter bawaan untuk setiap revisi; seed 1-6 untuk kedua kandidat 5b. |
| D8 | Aturan seleksi 5b di bawah. |

Aturan seleksi 5b (D8).
1. Kedua kandidat (Barrett, Montgomery) dibangun, diverifikasi, dan dikompilasi pada seed 1-6 sebelum aturan diterapkan.
2. Sebuah kandidat memenuhi syarat hanya bila semuanya terpenuhi: benar menurut test plan §7 (kedua simulator, uji
   reducer menyeluruh, kontrol negatif); siklus NTT / INTT persis 119 / 375; ALM ≤ 12.573 ("ALMs needed" fitter);
   timing terpenuhi pada 40,000 ns (slack setup dan hold tidak negatif di setiap corner yang dilaporkan). Diterapkan
   per seed; sebuah kandidat memenuhi syarat bila lolos di setiap seed.
3. Metrik: Fmax(c) = median atas seed 1-6 dari Fmax slow-corner terendah (nilai seperti tercetak). Siklus sama
   menurut syarat 2, jadi waktu per NTT sebanding dengan 1 / Fmax.
4. Fmax lebih tinggi menang, kecuali kandidat lain yang memenuhi syarat berada dalam 5 % darinya (hampir seri).
   Pada hampir seri, kandidat dengan median ALM lebih rendah menang. Bila median ALM juga berbeda kurang dari 32 ALM
   (sebaran seed C3-P6), tim memutuskan; saran pemecah seri: Barrett (tanpa tabel bentuk Montgomery).
5. Bila tidak ada kandidat yang memenuhi syarat, tidak ada yang dipilih otomatis; hasil dilaporkan dan tim memutuskan.
6. Hasil aturan dicatat di ADR terpisah ("pilihan lewat ADR" di roadmap).

Dinyatakan sebelum mengukur (INFERENCE dari analisis jalur baseline): Fmax kemungkinan seri karena jalur kritis ada
di jalur pembacaan memori; aturan lalu menyempit ke ALM.

## Konsekuensi
- Test plan final dengan jawaban ini (§13-nya mencatatnya); RTL Fase 5 boleh mulai dengan 5a.
- Empat revisi Quartus pada seed bawaan (C4a, C4c, C4d, BCM-ref sesuai kebutuhan) ditambah 12 untuk 5b
  (seed 1-6 x 2), ditambah 2 kompilasi informasi pada 20,000 ns; satu per satu.
- Memindahkan register antara jalur memori dan pengali, perubahan P, dan stall termasuk fase terpisah di ADR 0010
  (aturan di ADR 0012).

## Bukti
- `evidence/phase05/test_plan.md` (§3, §5, §7, §9, §11, §13)
- `evidence/phase05/baseline/c3p6_critical_path.md`
- `evidence/phase04/seed_sweep.md` (sebaran seed 32 ALM pada C3-P6)
- `docs/decisions/adr/ADR-0006-*.md`, `ADR-0007-*.md`, `ADR-0009-*.md`, `ADR-0010-*.md`
