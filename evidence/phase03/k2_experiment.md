<!-- claim-lint: skip-file (internal experiment record, not proposal text) -->
# Eksperimen tambahan Fase 3 K2 - counter sub-siklus sempit (`t_q`) pada C2

- Tanggal (UTC): 2026-09-30
- Branch: `phase3-multilane`, di atas `f155f32` (sapuan C2 Fase 3, tidak berubah)
- Status: selesai, diterima tim sebagai eksperimen yang selesai - valid tetapi tidak cukup
- Baseline dibekukan: `rtl/ntt/ntt_core_c2.sv` dan setiap file evidence Fase 3
  (`evidence/quartus/C2-L{1,2,4,8}.md`, `docs/results/phase03.md`) tidak disentuh.

## Mengapa eksperimen ini ada
C2-L8 terukur 11,446 ALM, 968 ALM di atas anggaran 10,478 ALM (25%) ADR 0004. Tim bertanya apakah
L=8 dapat dibawa ke bawah anggaran sambil menjaga semua yang membuat perbandingan adil: NUM_LANES=8,
8 butterfly per siklus, bit-exact, NTT=113 / INTT=369 siklus, tanpa pipelining (Fase 4), tanpa perubahan pada
aritmetika modular, tanpa perubahan besar arsitektur memori. Audit per entitas ada di
`l8_opt_entity_breakdown.txt` (bagian C2-L4 lawan C2-L8); K2 adalah kandidat berisiko terendahnya.

## Apa yang berubah
`rtl/ntt/ntt_core_c2_k2.sv` adalah salinan `rtl/ntt/ntt_core_c2.sv` dengan tepat tiga edit logika
(nama modul, `TW`, dan perluasan nol eksplisit `8'(t_q)`):

- C2: `t_q` adalah register 8-bit tetap untuk setiap NUM_LANES.
- K2: `t_q` selebar `$clog2(128/NUM_LANES)` bit (7/6/5/4 bit untuk L=1/2/4/8) -- tepat cukup untuk
  rentang yang dapat dicapai 0..TMax. Nilai sama, FSM sama, jadwal sama.

File pendukung: `rtl/ntt/ntt_core_c2_k2_l8.sv` (pembungkus Quartus), revisi
`quartus/phase03_multilane_c2/C2-L8-K2` (QSF berbeda dari C2-L8 hanya pada top entity, folder keluaran dan
dua file RTL; SDC identik), `formal/phase03-multilane/ntt_core_c2_k2_*`,
`tb/ntt/run_ntt_c2_tests.py <sim> k2` (argumen opsional baru; bawaan tetap menjalankan C2 yang dibekukan), dan
`scripts/quartus/quartus_entity_breakdown.py` (mengelompokkan tabel per entitas dari fitter).

## Hasil
| Pemeriksaan | Hasil | Evidence |
|---|---|---|
| Lint (Verilator `-Wall`, keempat L) + slang | bersih | `cmd: verilator --lint-only -Wall --timing -sv rtl/ntt/*.sv rtl/mem/*.sv --top-module ntt_core_c2_k2 -GNUM_LANES=<L>` |
| cocotb, Verilator + Icarus, L=1/2/4/8 | 16/16 + 16/16, bit-exact | `k2_cocotb_regression.txt` |
| Jumlah siklus | identik dengan C2 untuk setiap L (L=8: NTT 113, INTT 369) | file yang sama |
| Formal (SymbiYosys) | tidak berubah dari C2: L=1 PASS; L=2/4/8 UNKNOWN (masalah induksi `bank_overflow_o` yang sama seperti C2) | `k2_formal.txt`, `formal_verification.txt` |
| Quartus C2-L8-K2 | lihat tabel di bawah | `evidence/quartus/C2-L8-K2.md` |

| MEASURED (Quartus) | C2-L8 | C2-L8-K2 | Selisih |
|---|---|---|---|
| ALM | 11,446 / 41,910 | 11,232 / 41,910 | −214 |
| Anggaran ADR 0004 (10,478) | lebih 968 | lebih 754 | |
| Register | 3,100 | 3,095 | −5 |
| DSP | 17 / 112 | 17 / 112 | 0 |
| M10K | 0 / 553 | 0 / 553 | 0 |
| Fmax (Slow 100C) | 7.62 MHz | 7.85 MHz | +0.23 |
| Slack setup terburuk @ 20.000 ns | −111.219 ns | −107.314 ns | timing masih TIDAK terpenuhi |
| Peringatan kritis | 5 (15725, 332148) | 5 (dua yang sama) | |

Dari mana penghematan berasal (`l8_opt_entity_breakdown.txt`, bagian K2): logika sendiri `ntt_core_c2`
−132.6 ALM, logika sendiri `poly_mem_multiport` −91.9 ALM; setiap kelompok lain bergeser +0.1 sampai
+6.2 ALM (variasi penempatan).

## Kesimpulan
K2 benar secara fungsional, identik siklus, dan perbaikan nyata (kecil), tetapi tidak cukup:
C2-L8-K2 masih 754 ALM di atas anggaran, jadi L=8 tetap tidak memenuhi syarat menurut ADR 0004 dan L=4 tetap
kandidat. Ini cocok dengan batas hasil audit: seluruh kelompok logika sendiri `ntt_core_c2` adalah 768 ALM, jadi tidak ada
perbaikan lebar di situ yang bisa mencapai 968 ALM sendirian.

## Penyimpangan yang dicatat selama eksperimen
Kompilasi K2 pertama memunculkan 9 × Warning 10335 ("Unrecognized synthesis attribute") karena satu baris
komentar header di `ntt_core_c2_k2.sv` diawali kata "synthesis", yang diparse Quartus sebagai pragma.
Komentar ditulis ulang dan desain dikompilasi ulang; setiap angka di atas berasal dari kompilasi kedua itu
(ALM/register/DSP identik dengan yang pertama, 0 × Warning 10335). cocotb dan formal dijalankan ulang pada
file yang di-commit juga.

## Tambahan (2026-09-30): K2 diukur juga untuk L=1/2/4
Untuk mengisolasi K1 per L, K2 juga dikompilasi untuk L=1/2/4 (`evidence/quartus/C2-L{1,2,4}-K2.md`):
6,389 / 5,788 / 7,600 ALM lawan 6,018 / 5,728 / 7,629 milik C2. Jadi K2 bukan perbaikan yang seragam
(−214 di L8, −29 di L4, +60 di L2, +371 di L1). Kenaikan di L=1 seluruhnya adalah pengepakan fitter di
`poly_mem_multiport` (ALUT dan register identik); lihat
`evidence/phase03/k1_entity_breakdown.txt` dan `k1_experiment.md`.

## Langkah berikutnya (keputusan tim, 2026-09-30)
K1 (satu pengali modular bersama per butterfly sebagai ganti pengali maju/mundur terpisah) disetujui
sebagai eksperimen tambahan terpisah `C2-K2-K1`, dibangun di atas K2, diukur untuk keempat L (bukan hanya
L=8), karena ia mengubah datapath butterfly dan karenanya menyimpang dari lingkup Fase 3 yang tertulis
("butterfly, aritmetika, dan memori seperti di Fase 2"). Belum dimulai. ADR 0004 tidak diubah oleh
eksperimen ini.
