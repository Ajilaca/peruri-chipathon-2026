<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Fase 8a: dua ronde Keccak per siklus (konfigurasi C5) - test plan dan aturan adopsi

Ditulis 2026-10-03, sebelum RTL 8a apa pun dan sebelum pengukuran 8a apa pun (CRG-4). Lingkup: `docs/ROADMAP.md` Fase 8a; ADR 0026 (Accepted: 8a, 8b, 8c, 8d semuanya lanjut; menggantikan pelewatan di ADR 0019 butir 2);
ADR 0012 (aturan untuk pekerjaan timing). Basis: K0 (`rtl/keccak/keccak_f1600.sv`, `keccak_sponge.sv`, Fase 7, disetujui). Label: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED, perhitungan tim.
Matematika terkunci (C1): satu permutasi tetap 24 ronde theta, rho, pi, chi, iota; hanya jumlah ronde yang dihitung dalam satu siklus clock yang berubah.

## 1. Perubahannya (satu perubahan: ronde per siklus 1 -> 2)
- `rtl/keccak/keccak_f1600_r2.sv` baru: port sama dengan `keccak_f1600`; dua instans `keccak_round` berurutan per siklus, konstanta ronde `RC[2k]` dan `RC[2k+1]` untuk counter siklus k = 0..11
  (`{k, 1'b0}` dan `{k, 1'b1}`); register state mengambil keluaran ronde kedua; `busy_o` tinggi tepat 12 siklus; `done_o` satu siklus setelah tulis terakhir, seperti di K0.
- `rtl/keccak/keccak_sponge_r2.sv` baru: salinan `keccak_sponge.sv` dengan inti permutasi diganti (port sama, FSM sama, nama sama). Satu permutasi adalah 1 siklus run + 12 sibuk + 1 done = 14 siklus di sponge.
- `keccak_round.sv` dan `keccak_pkg.sv` dipakai ulang tanpa diedit. File RTL K0 tidak dimodifikasi. File test K0 `tb/keccak/test_keccak_f1600.py`, `test_keccak_sponge.py`, dan `run_keccak_tests.py` mendapat parameter lingkungan
  (ronde per siklus) yang nilai bawaannya mereproduksi K0 persis; karena file test yang ada berubah, verifikasi K0 (`scripts/test/phase7_verify.sh`) dijalankan ulang sebagai regresi dan hasilnya dicatat.
- Rumus siklus untuk sponge dengan p = 14 sebagai ganti 26: `1 + (len div 8 + 1) + pad2 + p * (len div rate + 1) + out_words + p * ((out_words - 1) div rate_words)`.
- ESTIMATE yang ditulis sebelum mengukur: ALM sekitar 1.6-2.0 kali logika ronde K0 (total K0 3,572 ALM MEASURED; logika ronde adalah bagian terbesar), jadi sekitar 5,500-7,500 ALM; register tidak berubah (1,653 diharapkan, register state sama);
  M10K 0, DSP 0; Fmax lebih rendah dari K0 (jalur berlipat dua: sekitar dua ronde logika); permutasi 14 siklus bukan 26 (rasio 0.538); siklus Keccak per operasi ML-KEM sekitar 2,000 - 12 x 44 = sekitar 1,500
  (2,026 / 2,078 / 2,070 dari `evidence/phase07/keccak_cycles.md` dikurangi 12 siklus per permutasi). Angka sekitar 1,200 yang dikutip di chat pada 2026-10-03 menghilangkan 2 siklus kendali dan transfer word
  dan digantikan oleh angka ini.

## 2. Kasus sudut (sama dengan rencana Fase 7, bagian 3, ditambah)
- Semua kasus sudut permutasi dan sponge Fase 7 pada latensi baru (nol, semua-satu, 1,600 state satu-bit, 200 state acak, rantai 10; setiap panjang batas keempat mode; panjang ML-KEM; back-pressure; stop; reset).
- Setiap konstanta ronde diuji: kesalahan pada konstanta berindeks ganjil hanya akan tampak di separuh kedua siklus, jadi jejak state setelah setiap siklus (ronde 2k+1) dibandingkan dan, selain itu, state setelah setiap
  ronde genap diperiksa lewat probe khusus test untuk nilai antara (`mid`, keluaran ronde pertama, diekspos ke testbench).
- `stop_i` di tengah permutasi 12 siklus; `run_i` dan xor diabaikan saat sibuk.

## 3. Test
| ID | Pemeriksaan | Alat | Disyaratkan |
|---|---|---|---|
| V1 | Lint `keccak_f1600_r2`, `keccak_sponge_r2` (CRG-1, CRG-2) | Verilator `-Wall`, slang | 0 peringatan, 0 error |
| V2 | Golden (`tb/golden/keccak.py`, tidak berubah) sama dengan hashlib | pytest (file test Fase 7) | semua sama (sudah PASS; dijalankan ulang) |
| V4 | Inti permutasi: state setelah setiap siklus sama dengan jejak golden pada ronde 1, 3, ..., 23; keluaran ronde pertama sama dengan jejak golden pada ronde 0, 2, ..., 22; `busy_o` tepat 12 siklus untuk setiap state | cocotb, kedua simulator (CRG-3) | semua sama, 12 di setiap run |
| V5 | Sponge: V5 Fase 7 pada latensi baru, terhadap hashlib dan sponge golden; counter permutasi sama dengan hitungan golden | cocotb, kedua simulator | semua sama |
| V6 | Siklus konstan (CRG-7): tiga pesan per (mode, panjang, word keluaran), hitungan identik; setiap titik sama dengan rumus dengan p = 14 | cocotb | identik per titik; rumus cocok dengan setiap titik yang dicatat |
| V7 | Kontrol negatif (salinan khusus test): NC-RC2 satu bit konstanta ronde berindeks ganjil salah; NC-R2 11 siklus (22 ronde); NC-PAD2 byte domain SHA3 0x1F | cocotb | pemeriksaan bit-exact FAIL (NC-R2 juga gagal pada pemeriksaan 12 siklus) |
| V8 | Formal: K1-K5 Fase 7 dengan counter 0..11 dan busy tepat 12 siklus (top formal baru, file baru); kontrol NC-K1 (11 siklus) dan NC-K4 | SymbiYosys | PASS; kontrol FAIL |
| V9 | Parameter terkunci (CRG-6); regresi K0: `scripts/test/phase7_verify.sh` dan `python3 formal/run/run_formal_phase7.py` lagi setelah perubahan file test | skrip | PASS |
| V10 | Quartus: baseline K0 seed 2-6 (K0 seed 1 sudah ada) dan C5 seed 1-6 pada 40.000 ns, satu per satu; ditambah `C5-20` seed 1 pada 20.000 ns (informasi) | `quartus_sh`, `/quartus-report` | evidence diekstrak |

## 4. Aturan adopsi (gaya ADR 0012, ditetapkan sebelum mengukur; tanpa toleransi)
C5 menggantikan K0 sebagai inti permutasi Keccak hanya bila semua berikut berlaku:
1. V1-V9 PASS dan kontrol gagal seperti disyaratkan, di kedua simulator.
2. `busy_o` tepat 12 siklus untuk setiap state dan hitungan siklus sponge sama dengan rumus dengan p = 14 di setiap titik yang dicatat.
3. ALM <= 12,573 di setiap seed (batas kerja = satu-satunya batas ALM di proyek, ADR 0009; ditulis untuk inti NTT dan dipakai di sini sebagai asumsi yang boleh ditolak tim) dan timing terpenuhi pada 40.000 ns di setiap seed 1-6.
4. Dengan F median atas seed 1-6 dari Fmax slow corner terendah pada 40 ns: t = 14 / F_C5 < 26 / F_K0 (F_K0 median K0 seed 1-6, dihitung ulang dari file), yaitu F_C5 > 0.5385 x F_K0.
Apakah hasil pada 20 ns terpenuhi dilaporkan, bukan bagian aturan. Jika aturan gagal, 8a dicatat sebagai terukur dan tidak diadopsi (seperti S8); K0 tetap inti Keccak untuk 8b-8d dan Fase 9 kecuali tim memutuskan lain.

## 5. Tidak dicakup
Perangkat keras (tanpa papan); seed selain 6; efek 8a pada seluruh operasi ML-KEM (blok baru tersambung di Fase 9; angka per operasi adalah perhitungan tim dari rumus, bukan pengukuran);
8b, 8c, dan 8d (rencana sendiri, ditulis sebelum masing-masing).
