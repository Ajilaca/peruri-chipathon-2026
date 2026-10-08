<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Jalur setup terburuk titik awal Fase 4 (C2-K2-K1, L = 8), per blok

- Tanggal (UTC): 2026-09-30
- Sumber: kompilasi Fase 3 yang sudah ada untuk revisi `C2-K2-K1-L8`
  (`evidence/quartus/C2-K2-K1-L8.md`); tanpa kompilasi baru. Hanya query timing:
  `report_timing -setup -npaths 1 -detail full_path` pada kondisi operasi `7_slow_1100mv_100c`,
  clock sementara 20.000 ns. MEASURED (Quartus Timing Analyzer); pengelompokan ke blok adalah
  klasifikasi elemen jalur yang dilaporkan menurut nama hierarki, dikerjakan dengan skrip.
- Tujuan: masukan untuk keputusan clock target dan kedalaman pipeline Fase 4 (ADR 0006, ADR 0007).

## Jalur
- Dari `ntt_core_c2_k2_k1:u_dut|t_q[2]` ke `...|poly_mem_multiport:u_mem|g_bank[6].mem[15][3]`
- Data tiba 135.696 ns, data dibutuhkan 25.527 ns, slack −110.169 ns (VIOLATED) pada corner ini
  (corner terburuk secara keseluruhan adalah Slow −40C, −110.494 ns, di file evidence di atas)
- Delay data 129.607 ns, 107 level logika

## Delay per blok (inkremen sel + interkoneksi dijumlahkan sepanjang jalur)
| Blok | Delay (ns) | Porsi | Kedatangan masuk → keluar (ns) |
|---|---|---|---|
| Inti: pembangkit alamat (`t_q`/`layer_q` → `j`, `jlen`), mux port | 10.0 (sekitar 4.8 di sisi baca dan 2.6 di sisi tulis antara masuk dan keluar; sisanya interkoneksi ke blok) | 7% | 5.5 → 10.3, dan 126.0 → 128.6 |
| `bank_map_rom` | 1.5 | 1% | 11.3 → 11.8 |
| Akses memori: arbitrasi slot bank di 16 port, mux baca, crossbar data baca; dan mux tulis di akhir | 64.0 (56.8 sisi baca, 4.4 sisi tulis, sisanya interkoneksi di antaranya) | 47% | 12.7 → 69.4, dan 130.6 → 135.0 |
| Butterfly: sub/mux sebelum pengali, add/sub sesudahnya | 6.6 | 5% | 70.7 → 74.1, dan 124.6 → 125.7 |
| Butterfly: pengali (DSP) | 4.4 | 3% | 75.4 → 78.5 |
| Butterfly: pembagi (`%` di `modmul_reduce`) | 45.2 | 34% | 79.3 → 123.7 |
| Jaringan clock ke register peluncur | 3.2 | 2% | - |

## Rincian lebih halus dua blok panjang (jalur sama, query sama)
Waktu kedatangan dalam ns sepanjang jalur (jaringan clock 0 → 3.2 termasuk):

| Bagian | Kedatangan masuk → keluar | Panjang | Bergantung data? |
|---|---|---|---|
| Pembangkit alamat, mux port | 3.2 → 10.3 | 7.1 | tidak (hanya `layer_q`, `t_q`, `mode_q`) |
| `bank_map_rom` | 10.3 → 11.8 | 1.5 | tidak |
| Memori: arbitrasi slot, riak di 16 port (elemen `count`/`slot` bergantian dengan mux) | 11.8 → 55.0 | 43.2 | tidak |
| Memori: pemilih sub-port per bank, mux baca, crossbar data baca | 55.0 → 69.4 | 14.4 | ya (data baca) |
| Butterfly: sub/mux operan invers, lalu pengali (DSP) | 69.4 → 78.5 | 9.0 | ya |
| Butterfly: pembagi, 13 tahap pengurangan (`op_4` … `op_17`), sekitar 3.4 ns masing-masing; kedatangan tiap tahap 79.3, 82.5, 86.4, 89.9, 93.3, 97.5, 101.4, 105.3, 108.6, 112.6, 115.2, 118.2, 121.1 | 78.5 → 123.7 | 45.2 | ya |
| Butterfly: add/sub setelah pembagi | 123.7 → 125.7 | 2.0 | ya |
| Sisi tulis: mux port, pemilih sub-port per bank, tulis | 125.7 → 135.0 | 9.3 | ya |

Arbitrasi slot (sekitar 43 ns) hanya kendali: ia fungsi dari counter jadwal, bukan dari
data polinomial. Itu yang memungkinkan stage register di dalamnya tanpa menyentuh datapath.

## Pembacaan
- Segmen terbesar pada L = 8 adalah jalur akses memori (sekitar 57 ns di sisi baca), bukan
  pembagi (sekitar 44 ns). Pada C0 (L = 1) pembagi mendominasi
  (`evidence/phase01/quartus_C0_timing_analysis.md`); arbitrasi slot multi-port
  dan crossbar yang ditambah di Fase 3 mengubah hal itu.
- Konsekuensi untuk pipelining (ESTIMATE, dari panjang segmen di atas, mengabaikan overhead register
  dan routing ulang): register yang hanya ditaruh di batas blok tidak bisa memberi periode clock lebih pendek dari
  blok tunggal terpanjang, sekitar 57 ns (sekitar 17 MHz). Turun di bawah itu butuh register di dalam
  jalur akses memori; turun di bawah sekitar 44 ns (sekitar 22 MHz) juga butuh satu di dalam rantai pembagi.
  Pembagian rata 129.6 ns butuh sekitar 7 stage untuk 20 ns dan sekitar 4 untuk 40 ns.
- Ini angka satu jalur dari satu kompilasi; jalur hampir-kritis lain ada dan fitter
  menempatkan ulang logika saat register ditambah, jadi angka ini membatasi harapan, bukan memprediksi Fmax.
