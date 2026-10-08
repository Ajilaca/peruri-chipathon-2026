<!-- claim-lint: skip-file (internal experiment record, not proposal text) -->
# Eksperimen tambahan Fase 3 K1 - satu pengali bersama per butterfly (konfigurasi C2-K2-K1)

- Tanggal (UTC): 2026-09-30
- Branch: `phase3-multilane`, di atas `b11b08f` (K2 di-commit)
- Status: terukur untuk keempat L; L=8 kembali di bawah anggaran ALM ADR 0004. Dipilih tim:
  ADR 0005 (Accepted 2026-09-30, Faza Dzil, Team J5) mengadopsi C2-K2-K1 dan memilih L=8. ADR 0004 tidak
  berubah. (Saat catatan ini pertama ditulis ADR 0005 baru Proposed dan L=8 adalah kandidat.)
- Lingkup: disetujui tim (2026-09-30) sebagai eksperimen tambahan yang terpisah, karena ia
  mengubah datapath butterfly dan karenanya menyimpang dari lingkup Fase 3 yang tertulis
  ("butterfly, aritmetika, dan memori seperti di Fase 2"). Dibangun di atas K2, diukur untuk L=1/2/4/8.
- Dibekukan dan tidak disentuh: `rtl/ntt/butterfly.sv`, `rtl/ntt/modmul_reduce.sv`, `rtl/ntt/ntt_core_c2.sv`,
  `rtl/ntt/ntt_core_c2_k2.sv`, setiap file evidence C2 Fase 3 dan `docs/results/phase03.md`.

## Apa yang berubah
- `rtl/ntt/butterfly_shared.sv` (baru): persamaan maju (CT) dan mundur (GS) yang sama dengan
  `butterfly.sv`, tetapi dengan SATU `modmul_reduce` yang operandnya `mode ? (b - a) mod q : b`, sebagai ganti
  satu `modmul_reduce` per mode. mode tetap untuk seluruh run NTT/INTT, jadi kedua pengali tidak pernah
  dibutuhkan dalam siklus yang sama. Metode reduksi (`modmul_reduce.sv`, `%` dengan Q) dipakai ulang tanpa perubahan.
- `rtl/ntt/ntt_core_c2_k2_k1.sv`: salinan `ntt_core_c2_k2.sv`, satu perubahan (`butterfly` ->
  `butterfly_shared`). Pembungkus `ntt_core_c2_k2_k1_l{1,2,4,8}.sv`; revisi Quartus
  `C2-K2-K1-L{1,2,4,8}` (QSF = milik C2-L<n> dengan hanya top entity, folder keluaran, file inti/pembungkus
  dan `butterfly_shared.sv` tambahan yang berubah; SDC identik).
- Untuk mengisolasi K1 per L, K2 juga diselesaikan untuk L=1/2/4 (revisi `C2-L{1,2,4}-K2`), dan baseline C2-L1 /
  C2-L2 dikompilasi ulang untuk tabel per entitas (total direproduksi persis).

## Kebenaran
| Pemeriksaan | Hasil | Evidence |
|---|---|---|
| Lint (Verilator `-Wall`) inti pada L=1/2/4/8 + keempat pembungkus, slang | bersih | `cmd: verilator --lint-only -Wall --timing -sv rtl/ntt/*.sv rtl/mem/*.sv --top-module ntt_core_c2_k2_k1 -GNUM_LANES=<L>` |
| Unit: `butterfly_shared` lawan golden (`tb/ntt/test_butterfly.py` tidak berubah: sudut + 1000 acak per mode) | 2/2 Verilator, 2/2 Icarus | `k1_cocotb_regression.txt` |
| cocotb inti, L=1/2/4/8, bit-exact + round-trip + siklus konstan + `bank_overflow_o`==0 | 16/16 Verilator, 16/16 Icarus | file yang sama |
| Jumlah siklus | identik dengan C2 untuk setiap L (L=8: NTT 113, INTT 369; 8 butterfly/siklus) | file yang sama |
| Formal inti, alur pertama (sama dengan C2, K2 saat itu) | L=1 PASS; L=2/4/8 UNKNOWN (artefak harness, caveat 4) | `k1_formal.txt` |
| Formal inti, alur terkoreksi (`read_slang` + `memory_map -rom-only`) | PASS pada L=1/2/4/8, kontrol negatif gagal seperti disyaratkan | `formal_rerun.md` |
| Ekuivalensi formal `butterfly` lawan `butterfly_shared`, aritmetika penuh | tidak selesai: timeout 30 menit (caveat 5) | `formal/phase03-multilane/k1_butterfly_equiv.sby` |
| Ekuivalensi, opsi 1: pengali diabstraksi (fungsi tak terinterpretasi + konsistensi Ackermann), semua mode, semua masukan < q | PASS; kedua kontrol negatif FAIL seperti disyaratkan | `k1_equiv_abstraction.txt`, `formal/phase03-multilane/k1_butterfly_equiv_abs.sby`, `k1_negctl_operand.sby`, `k1_negctl_noack.sby` |
| Ekuivalensi, opsi 2: simulasi RTL menyeluruh, semua 2 x 3329^3 = 73,785,560,578 masukan, tiga arah lawan golden | PASS, 0 ketidakcocokan, tanpa asumsi | `k1_exhaustive_equivalence.txt`, `tb/ntt/k1_exhaustive/` |

## Sumber daya dan timing (MEASURED, Quartus Prime Lite 25.1std, 5CSEBA6U23I7, batasan/seed sama)
| | L=1 | L=2 | L=4 | L=8 |
|---|---|---|---|---|
| ALM, C2 | 6,018 | 5,728 | 7,629 | 11,446 |
| ALM, C2-K2 | 6,389 | 5,788 | 7,600 | 11,232 |
| ALM, C2-K2-K1 | 5,566 | 5,374 | 6,775 | 9,754 |
| K1 lawan C2 | −452 | −354 | −854 | −1,692 |
| Dalam anggaran ADR 0004 (10,478)? | ya | ya | ya | ya (724 di bawah) |
| DSP, C2 → C2-K2-K1 | 3 → 2 | 5 → 3 | 9 → 5 | 17 → 9 |
| Register, C2-K2-K1 | 3,099 | 3,095 | 3,098 | 3,094 |
| M10K | 0 / 553 (semua konfigurasi) | | | |
| Fmax Slow 100C, C2 / K2 / K2+K1 (MHz) | 14.76 / 15.40 / 14.33 | 13.54 / 13.66 / 12.63 | 11.60 / 11.61 / 10.89 | 7.62 / 7.85 / 7.68 |
| Slack setup terburuk @ 20.000 ns, C2-K2-K1 | −49.804 ns | −59.148 ns | −71.868 ns | −110.494 ns |
| Siklus NTT / INTT (simulasi, ketiga konfigurasi) | 897 / 1153 | 449 / 705 | 225 / 481 | 113 / 369 |

Timing TIDAK terpenuhi untuk konfigurasi mana pun (seperti C0/C1/C2; pipelining adalah Fase 4). Peringatan kritis
adalah dua jenis yang sama dengan baseline (15725 clock virtual pin, 332148 timing tidak terpenuhi); 0 ×
Warning 10335. Evidence: `evidence/quartus/C2-K2-K1-L{1,2,4,8}.md`,
`C2-L{1,2,4}-K2.md`, `C2-L8-K2.md`; tabel per entitas di
`k1_entity_breakdown.txt`.

Dari mana penghematan K1 berasal (L=8): 16 instans `modmul_reduce` per lajur (maju +
mundur, 3,068.7 ALM) menjadi 8 yang dibagi (1,563.5 ALM); mux operand tambahan memakan +48.3 ALM di
butterfly (~6 ALM/lajur). Pola sama di setiap L (per lajur: satu pengali+pembagi sekitar 190–195 ALM
dihapus, sekitar 5–8 ALM mux ditambah).

## Caveat yang ditemukan selama eksperimen (dilaporkan, tidak disembunyikan)
1. Variasi pengepakan fitter besar di blok memori. K2 pada L=1 adalah +371 ALM lawan C2, tetapi semuanya
   ada di `poly_mem_multiport` (5,180.9 → 5,554.7 ALM) dengan ALUT kombinasional (2,669)
   dan register (3,072) yang identik: logika sama, dikemas ke ALM secara berbeda. Jadi total ALM dapat
   bergeser beberapa ratus ALM antar kompilasi tanpa perubahan logika (interpretasi angka MEASURED, bukan
   pengukuran terpisah). Margin 724 ALM K1-L8 lebih besar dari ayunan terbesar yang terlihat (~370 ALM),
   tetapi tidak dengan faktor besar; sapuan seed akan mengukurnya.
2. K2 bukan perbaikan yang seragam: −214 (L8), −29 (L4), +60 (L2), +371 (L1, pengepakan, lihat di atas).
3. Fmax turun sedikit dengan K1 pada L=1/2/4 (mux operand ada di depan pengali, di jalur
   kritis lewat pembagi); pada L=8 dalam derau C2. Penutupan timing adalah Fase 4.
4. Temuan toolchain formal (keduanya kini ditangani di alur). (a) Frontend `read -formal` asli Yosys
   tidak mengelaborasi fungsi paket `ntt_pkg` `add_mod`/`sub_mod` (hasilnya
   menjadi wire tak digerakkan), sehingga modelnya atas `butterfly.sv` salah (inverse a=b=1920 memberi a_o=0
   bukan 511); `read_slang` memodelkannya dengan benar. (b) UNKNOWN bukti inti L>1 yang dicatat di
   tabel di atas adalah artefak harness terpisah: `proc_rom` mengubah ROM menjadi sel memori yang
   isinya adalah state bebas pada langkah induksi. Dengan `read_slang` + `memory_map -rom-only`
   (hanya harness, RTL tidak berubah) C2, C2-K2, dan C2-K2-K1 semuanya PASS pada L=1/2/4/8, kontrol negatif
   gagal seperti seharusnya, dan bukti Fase 1/2 tetap PASS:
   `formal_rerun.md`. File itu menggantikan baris L>1 di `k1_formal.txt`
   dan `k2_formal.txt`.
5. Ekuivalensi butterfly: bukti formal aritmetika penuh tidak selesai, tetapi ekuivalensinya kini
   ditegakkan dengan dua cara lain. Dengan `read_slang` miter memodelkan pengali 12x12 dan
   pembagi 24/12 yang nyata di kedua sisi; boolector tidak selesai dalam 30 menit (ekuivalensi pengali/pembagi antara
   rangkaian yang strukturnya berbeda adalah kasus sulit yang dikenal bagi solver tingkat-bit), jadi `k1_butterfly_equiv.sby`
   disimpan sebagai catatan, bukan hasil. Diselesaikan sebagai gantinya: (1) `k1_butterfly_equiv_abs.sby` mengabstraksi
   `modmul_reduce` (modul tak berubah yang sama di kedua sisi) sebagai fungsi tak terinterpretasi dengan
   batasan konsistensi fungsional dan membuktikan pemilihan operand serta logika add/sub/mux di sekitarnya
   ekuivalen: PASS; asumsinya (modmul_reduce adalah fungsi murni dari masukannya) dinyatakan di
   `modmul_reduce_uf.sv`; dua kontrol negatif (operand inverse yang sengaja salah; miter tanpa
   asumsi konsistensi) keduanya FAIL, jadi PASS tidak vakum. (2) simulasi Verilator menyeluruh
   atas RTL tak berubah pada setiap mode dan setiap a, b, zeta dalam [0, q) (73,785,560,578
   evaluasi, 1,229 s pada 8 proses) dibandingkan dengan langkah butterfly golden: 0 ketidakcocokan, tanpa
   asumsi. Satu catatan alat dari membuat (1) bekerja: `read_slang` mengubah wire `(* anyseq *)` sebuah stub
   menjadi konstanta x, yang membuat percobaan pertama FAIL secara palsu; `setundef -anyseq` di skrip .sby
   memperbaikinya dan diperlukan.

## Kesimpulan
K1 bit-exact (simulasi di dua simulator; ekuivalensi butterfly dibuktikan dengan pengali
diabstraksi dan dengan simulasi menyeluruh), identik siklus, menjaga 8 butterfly/siklus pada L=8, tidak
mengubah metode reduksi modular, dan membawa C2-K2-K1-L8 ke 9,754 ALM, 724 ALM di bawah anggaran
ADR 0004. Ia juga mengecilkan setiap L lain, jadi keempat L keluarga ini dalam anggaran. Tim
memutuskan (ADR 0005, Accepted) mengadopsi konfigurasi ini dan memilih L=8; Fase 4 dimulai dari
C2-K2-K1 pada L=8. Hasil C2 (L=4) tetap di `docs/results/phase03.md` sebagai perbandingan baseline.
