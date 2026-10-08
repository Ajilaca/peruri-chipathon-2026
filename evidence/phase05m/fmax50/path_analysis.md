<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Pertanyaan 50 MHz, opsi 1: analisis jalur kritis S7 dan S8 (2026-10-03, permintaan tim "jalankan opsi 1 dan 2")

Metode (hanya baca, MEASURED): `scripts/quartus/phase5m_top_paths.tcl` dijalankan dengan `quartus_sta` pada salinan `quartus/phase05m_memsched/` (database revisi S7 dan S8, seed 1, 40,000 ns; `.qpf` repository
tidak pernah dibuka oleh analisis), 300 jalur setup terburuk per corner (Slow 1100 mV 100 C dan -40 C), tiga dalam detail penuh; dikelompokkan menurut blok awal dan akhir dengan `scripts/quartus/phase5_path_classes.py`
(indeks bit diringkas). File: `S7_top300_path_classes_slow{100,-40}.txt`, `S8_top300_path_classes_slow{100,-40}.txt`, `S7_worst_path_slow-40.txt`.

## Kelas jalur terburuk (slack pada 40,000 ns; delay jalur = 40 - slack, INFERENCE)
| Revisi / corner | Kelas terburuk | Slack (ns) | Kelas berikutnya |
|---|---|---|---|
| S7 / -40 C | ROM peta bank (diinferensi sebagai M10K, `bank_map_rom:g_map[4]`) -> riak arbitrasi slot port 4..10 -> register potong `g_arb[10].count_q` (potongan A_11) | 14.439 (16 jalur) | potongan pengali 2 (`u_mul.cut2`) -> penulisan memori (flip-flop penyimpanan): 17.711 (269 jalur) |
| S7 / 100 C | sama | 14.617 | sama, 17.770 |
| S8 / -40 C | kelas arbitrasi yang sama | 15.135 | `layer_q` -> RAM; `bank_rdata_q` -> potongan pengali 0: 19.015 (kelas jalur tulis S7 hilang) |

Jalur terburuk S7 secara rinci (`S7_worst_path_slow-40.txt`): clock ke M10K 7,043 ns, clock-to-out M10K 1,080 ns, lalu sekitar 22,6 ns sel mux / penjumlah riak arbitrasi (`Mux7` ... `Mux18`,
`count_c` port 4 sampai 10) sampai `g_arb[10].count_q`; jalur data 23,932 ns, skew clock -1,569 ns.

## Pembacaan (INFERENCE)
- Setelah S7 batasnya adalah arbitrasi slot di antara potongan A_4 dan A_11 (tujuh port riak), diberi makan ROM peta bank yang ditempatkan Quartus di blok M10K (ini juga menjelaskan sebagian
  jumlah M10K 31 / 33: ROM peta bank diinferensi sebagai blok RAM; tidak diurai lebih lanjut).
- Untuk 50 MHz (20 ns) baik segmen arbitrasi (sekitar 25,6 ns pada -40 C) maupun segmen pengali-ke-tulis (sekitar 22,3 ns) harus turun di bawah sekitar 19-20 ns. Register tulis S8 menghapus kelas kedua
  tetapi bukan yang pertama, itulah sebabnya S8 tidak menaikkan Fmax.
- Arbitrasi hanya bergantung pada alamat, yaitu pada jadwal tetap, tidak pernah pada data. Dua cara menghapusnya, keduanya langkah baru untuk tim: (a) S10 (16 bank 1R1W, ADR 0022): tidak ada arbitrasi slot sama sekali;
  (b) tabel arbitrasi yang dihitung lebih dulu (slot dan offset per port dan siklus dari ROM yang diindeks mode, layer, dan t) sebagai ganti riak. Lebih banyak potongan arbitrasi adalah cara ketiga, dengan stall (P > 7).
- Opsi Quartus tanpa RTL: menjaga ROM peta bank di luar M10K (ROM logika) akan mengganti clock-to-out blok RAM (1,080 ns) dan skew jalur clock-nya (-1,569 ns) di awal jalur dengan delay ROM logika (efek tidak diukur).

## Opsi 2: S7 pada 20,000 ns, seed 1-6 (MEASURED, `quartus_S7-20[-s2..s6].md`, `quartus/phase05m_memsched/run_s7_20_sweep.sh`)
| Seed | ALM | Setup terburuk (ns, semua corner) | Hold terburuk (ns) | Fmax slow corner terendah (MHz) |
|---|---|---|---|---|
| 1 | 9,365 | -1.388 | 0.151 | 46.76 |
| 2 | 9,358 | -1.655 | 0.127 | 46.18 |
| 3 | 9,359 | -2.296 | 0.136 | 44.85 |
| 4 | 9,383 | -2.431 | 0.125 | 44.58 |
| 5 | 9,369 | -1.933 | 0.124 | 45.59 |
| 6 | 9,355 | -1.615 | 0.150 | 46.26 |

Timing pada 20,000 ns terpenuhi di 0 dari 6 seed; median Fmax corner terendah 45,885 MHz (INFERENCE: median). Di bawah batasan 20 ns fitter bekerja lebih keras daripada pada 40 ns, jadi nilai Fmax ini tidak sebanding
dengan angka 40 ns. Catatan: pesan status 2026-10-03 mengutip "-0,836 ns" untuk seed 1; itu hanya baris setup Slow 100 C; yang terburuk atas semua corner adalah -1,388 ns (dikoreksi di sini).
