<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Jumlah siklus K0 (Fase 7, test plan V6), 2026-10-03

## 1. Tabel siklus terukur (MEASURED, simulasi; `cycles_k0.json`, 306 titik, identik di Verilator dan Icarus)
Siklus dari siklus yang membawa `start_i` sampai siklus yang menerima word keluaran terakhir, tanpa back-pressure. Untuk setiap (mode, panjang, word keluaran) tiga pesan (acak, semua-0x00, semua-0xFF) memberi hitungan yang sama: jumlah siklus hanya bergantung pada panjang publik dan jumlah word keluaran, tidak pernah pada data (CRG-7). Titik terpilih:


| Mode | Byte pesan | Word keluaran | Siklus |
|---|---|---|---|
| sha3_256 | 0 | 4 | 33 |
| sha3_256 | 32 | 4 | 37 |
| sha3_256 | 135 | 4 | 48 |
| sha3_256 | 136 | 4 | 76 |
| sha3_256 | 137 | 4 | 76 |
| sha3_256 | 1184 | 4 | 389 |
| sha3_512 | 0 | 8 | 37 |
| sha3_512 | 64 | 8 | 44 |
| sha3_512 | 72 | 8 | 72 |
| shake_128 | 34 | 21 | 54 |
| shake_128 | 34 | 22 | 81 |
| shake_128 | 0 | 1 | 30 |
| shake_256 | 34 | 16 | 49 |
| shake_256 | 33 | 16 | 49 |
| shake_256 | 1120 | 4 | 381 |

Semua 306 titik sama dengan rumus yang diturunkan dari FSM `rtl/keccak/keccak_sponge.sv` (rumus ditulis setelah RTL, lalu diperiksa terhadap setiap titik; tidak disetel):

    cycles = 1 + (len div 8 + 1) + pad2 + 26 * (len div rate + 1) + out_words + 26 * ((out_words - 1) div rate_words)
    pad2   = 0 when (len mod rate) div 8 = rate_words - 1, else 1;   rate_words = rate / 8

Satu permutasi adalah 26 siklus seperti terlihat pengendali: 1 siklus run, 24 siklus dengan `keccak_f1600.busy_o` tinggi (V4: tepat 24 untuk setiap state), 1 siklus done. ESTIMATE test plan sebelum pengukuran
memakai 24 per permutasi dan sekitar 370 siklus untuk H(ek); nilai terukur adalah 389 siklus (+5 %). Estimasi itu optimistis sebesar 2 siklus kendali per permutasi; digantikan, tidak disetel.

## 2. Siklus Keccak satu operasi ML-KEM-768 dengan K0 (perhitungan tim, dihitung oleh `scripts/test/phase7_op_cycles.py` dari rumus terukur; tanpa pengukuran baru)
| Panggilan | Mode | Byte pesan | Word keluaran | Permutasi | Siklus (rumus) |
|---|---|---|---|---|---|
| G 33 B (KeyGen) | sha3_512 | 33 | 8 | 1 | 41 |
| G 64 B | sha3_512 | 64 | 8 | 1 | 44 |
| H(ek) 1184 B | sha3_256 | 1184 | 4 | 9 | 389 |
| PRF 33 B -> 128 B | shake_256 | 33 | 16 | 1 | 49 |
| J 1120 B -> 32 B | shake_256 | 1120 | 4 | 9 | 381 |
| SampleNTT x 9 (matrix), 200 random rho | shake_128 | 34 each | by rejection | min 27, median 27, max 29 | min 1289, median 1302, max 1364 |

| Operasi | Siklus Keccak tanpa SampleNTT | + SampleNTT (min / median / max) | Total siklus Keccak (min / median / maks) | Permutasi (total median) |
|---|---|---|---|---|
| KeyGen | 724 | 1289 / 1302 / 1364 | 2013 / 2026 / 2088 | 43 |
| Encaps | 776 | 1289 / 1302 / 1364 | 2065 / 2078 / 2140 | 44 |
| Decaps | 768 | 1289 / 1302 / 1364 | 2057 / 2070 / 2132 | 44 |

Pembacaan (INFERENCE): sekitar 2.000 siklus Keccak per operasi saat setiap panggilan berjalan sendiri dan tidak ada yang tumpang-tindih. Angka sekitar 1.060 siklus sebelum pengukuran (44 permutasi x 24) melewatkan
2 siklus kendali per permutasi, transfer word demi word (H(ek) saja memindahkan 148 word masuk dan 4 keluar) dan restart sponge untuk setiap panggilan; tabel ini menggantikannya. Bandingkan, dalam satuan sama,
dengan aritmetika Fase 6 dengan S10: KeyGen 5.475, Encrypt 6.789, Decrypt 3.109 siklus (MEASURED, simulasi, `evidence/phase06/verify.md`); kedua blok belum tersambung.
