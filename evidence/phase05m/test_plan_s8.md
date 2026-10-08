<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Fase 5M, langkah S8: register jalur tulis dan satu gelembung per arah (P = 7 -> 8) - test plan dan aturan adopsi

Ditulis 2026-10-02, setelah RTL S8 ditulis dan di-lint (Verilator `-Wall`, slang: 0 peringatan) tetapi sebelum simulasi S8 apa pun dan sebelum kompilasi Quartus
S8 apa pun (CRG-4: tidak ada di bawah yang bergantung pada pengukuran S8). Lingkup dan aturan: ADR 0017 (S8 = tuas 4 paket keputusan: P -> 8, satu stall tak bergantung data
per transformasi), ADR 0019 (catatan amandemen 2: S7 dan S8 direncanakan sebelum Fase 7), ADR 0020, Amandemen A1 `test_plan.md` (regresi penuh Fase 0-5 dijalankan
sekali, di S8, pada pohon akhir). Konfigurasi basis: S7 (`rtl/ntt/ntt_core_s7_p7.sv`, revisi S7, seed 1-6 di `s7/`). Basis S8 adalah S7 apa pun hasil
aturannya: S8 didefinisikan sebagai tuas 4 di atas baca terpecah (tabel ADR 0017); ini mengikuti instruksi tim 2026-10-02 (chat: "kerjakan sesuai
dengan agenda hari ini ... S7-S8 selesai"). Hasil aturan S7 tetap tercatat tanpa perubahan. Label: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED.

## 1. Perubahannya (satu perubahan)
- inti baru `rtl/ntt/ntt_core_s8.sv` (salinan `ntt_core_s7.sv`), parameter `WR_REG` (0 atau 1), pembungkus `rtl/ntt/ntt_core_s8_p8.sv` (`WR_REG = 1`, semua parameter lain seperti S7:
  bit ARB_REG 4, 11, 16, RD_SPLIT 1, bit MUL_REG 0, 1, 2). File memori tidak diubah: `poly_mem_multiport_split.sv` dipakai ulang dengan `WR_DELAY = WrDly + WR_REG`.
- Dengan `WR_REG = 1` 16 keluaran butterfly (8 lajur x 2 x 12 bit = 192 bit) diregister (`pipe_delay`) sebelum data tulis memori; kendali tulis memori
  (valid, bank, offset, slot) dan pemilih host/butterfly port-0 ditunda satu siklus yang sama; `Pipe = RdLat + WrDly + WR_REG = 8`; guard tulis host
  memakai `WrEff = WrDly + WR_REG + RD_SPLIT = 5`.
- Jadwal alamat butuh gelembung pada Pipe = 8 (`scripts/test/phase5_stall_cycles.py 8`, INFERENCE dari paket keputusan Fase 5, tabel stall): satu siklus pada batas
  NTT 3 (antara layer 3 dan 4) dan satu pada batas INTT 2 (antara layer 2 dan 3); batas pass skala INTT pada tabel itu tidak ada di M6/S7/S8.
  State baru `S_STALL` (encoding 2): semua permintaan mati satu siklus, dimasuki hanya bila `layer_q` sama dengan batas tetap mode saat ini. Posisi gelembung adalah
  fungsi (mode, layer) saja, tidak pernah data, jadi jumlah siklus konstan.
- File yang sudah ada dimodifikasi: tidak ada (hanya file baru; S7, M6, C4b-B, dan file beku Fase 1-5 tetap).

## 2. Kasus sudut (didaftar sebelum test)
- Dua batas yang membawa gelembung (NTT 3, INTT 2) dan alamat slack-terketat setiap batas lain (`_tight_addresses`), dengan data terarah-batas.
- Tulis host diikuti langsung start (guard `hw_q` dengan `WrEff = 5`), baca host saat `S_STALL` (port baca lajur 0 aktif di state itu, tidak pernah tulis),
  start saat drain, reset di tengah transformasi dan di siklus gelembung (tidak ada tulis setelah reset), `bank_overflow_o` tidak pernah aktif (siklus gelembung punya satu port aktif).
- Siklus konstan: setiap masukan set sudut dan vektor acak memberi hitungan sama per arah; hitungan NTT dan INTT sama.
- Kontrol negatif: gelembung dihapus (bahaya harus muncul), kendali tulis tidak ditunda bersama register data tulis (kurang satu siklus).

## 3. Test
| ID | Pemeriksaan | Alat | Disyaratkan |
|---|---|---|---|
| V1 | Lint inti dan pembungkus S8 | Verilator `-Wall`, slang | 0 peringatan, 0 error |
| V2 | Inti lawan golden: NTT, INTT (`intt()`), round trip, data terarah-batas, 512 vektor satuan INTT, siklus konstan, `bank_overflow_o`, scoreboard bahaya (baca diterbitkan saat tulis lebih awal masih terbang; baca dan tulis alamat sama dalam siklus sama) dengan `C3_RDLAT = 4`, `C3_RDPHYS = 3`, `C3_WRDLY = 4` | cocotb `tb/phase5m/test_ntt_core_s8.py` (salinan test S7; scoreboard memperlakukan `S_STALL` sebagai siklus bukan-permintaan), kedua simulator | semua PASS; 0 pelanggaran scoreboard; siklus konstan; NTT = INTT = 122 |
| V3 | NC-B: salinan S8 tanpa gelembung (mutan `Stall = 0`) | cocotb | NTT dan INTT bit-exact FAIL dan scoreboard memicu |
| V4 | NC-W: salinan S8 yang kendali tulisnya TIDAK ditunda oleh `WR_REG` (memori `WR_DELAY = WrDly`, register data dipertahankan) | cocotb | NTT dan INTT bit-exact FAIL |
| V5 | Formal H, O, R, A, B, C pada `ntt_core_s8_p8` (salinan top formal S7 dengan Pipe = 8, RdLat 4, WrDly 4, WR_REG, dan gelembung di model kendali) dengan NC-O, NC-A | SymbiYosys | PASS; kontrol FAIL |
| V6 | Unit test memori untuk memori yang dipakai ulang pada `WR_DELAY = 4`, `RD_SPLIT = 1` (V2/V3 S7 pada delay baru) | cocotb `tb/phase5m/test_poly_mem_split.py` | semua sama dengan acuan |
| V7 | Run ulang verifikasi S6 dan S7 pada pohon akhir (M6 dan S7 tidak dimodifikasi; ini membuktikannya) | `scripts/test/phase5m_verify.sh`, `scripts/test/phase5m_verify_s7.sh`, `formal/run/run_formal_phase5m.py`, `formal/run/run_formal_phase5m_s7.py` | OVERALL PASS |
| V8 | Regresi Fase 0-5, sekali, pada pohon akhir (Amandemen A1): `scripts/test/phase5_regression.sh` dan `scripts/test/phase5_verify.sh`, ditambah `git diff --name-status 288a78c HEAD` yang mendaftar file ditambah lawan dimodifikasi | skrip, disimpan dengan SHA git | OVERALL PASS; file yang ada dimodifikasi: tidak ada (atau masing-masing terdaftar) |
| V9 | Revisi Quartus `S8` (seed 1) dan `S8-s2` .. `S8-s6`, 40.000 ns, bawaan Quartus, kompilasi penuh dari db bersih, satu per satu | `quartus_sh --flow compile` | file evidence diekstrak dari root repository |
| V10 | Satu kompilasi informasi `S8-20` pada 20.000 ns (RTL dan seed 1 sama; hanya informasi, bukan bagian aturan) | `quartus_sh --flow compile` | file evidence; setup terburuk dan Fmax dicatat |

## 4. Aturan adopsi (ditetapkan sebelum mengukur)
S8 (revisi `S8`, seed 1-6) diadopsi sebagai inti Fase 5M akhir hanya bila semua berikut berlaku:
1. benar: V1-V8 PASS di kedua simulator bila berlaku; V3 dan V4 gagal seperti disyaratkan;
2. siklus konstan dan tepat NTT 122 / INTT 122 (113 + 8 + 1 gelembung; ESTIMATE sampai disimulasikan);
3. ALM inti NTT <= 12,573 di setiap seed; timing terpenuhi pada 40.000 ns di setiap seed (setup terburuk >= 0, hold terburuk >= 0);
4. ADR 0012 terhadap langkah sebelumnya S7 pada median Fmax seed 1-6-nya (`F_S7`, dihitung ulang dari file evidence S7 oleh `scripts/quartus/phase5m_select_s8.py`):
   dengan F median atas seed 1-6 dari Fmax slow corner terendah S8, t_NTT = 122 / F < 120 / F_S7 dan t_INTT = 122 / F < 120 / F_S7, yaitu F > F_S7 x 122 / 120
   (perhitungan tim). Skrip juga mencetak perbandingan dengan M6 dan C4b-B sebagai catatan; aturan hanya membandingkan dengan S7.
Catatan yang ditetapkan sekarang:
- Tanpa toleransi. Median di atas ambang kurang dari sebaran seed (sekitar 0.7 MHz di S6; sebaran S7 terukur) adalah lulus menurut aturan dengan catatan itu; kegagalan
  tidak diadopsi menurut aturan dan dilaporkan (C5: tim memutuskan). Bila S8 tidak diadopsi, S7 (atau M6) tetap menjadi datapath untuk Fase 6 dan Fase 7; pilihan tim.
- Jika simulasi menunjukkan jumlah gelembung berbeda dari 1 per arah, angka siklus rencana dikoreksi sebagai MEASURED dan kondisi 2 dievaluasi pada konstanta terukur; hitungan
  yang bergantung data gagal pada kondisi 2.
- Aturan proyek yang digerakkan tenggat berlaku: vonis S8 datang dari satu sapuan; tanpa seed tambahan.

## 5. Harapan (ESTIMATE, ditulis sebelum mengukur; hanya kompilasi yang bisa memastikan)
- Siklus +2 lawan S7 (120 -> 122). Jika segmen tulis (slack MEASURED C4b-B pada 40 ns: segmen tulis 17.1 ns, jalur samping 12.1 ns) menjadi yang kritis setelah S7, satu tahap register
  dapat menaikkan Fmax; jika S7 sudah memindahkan jalur kritis ke tempat lain, S8 dapat rugi (siklus +1.7 %, ALM dan register naik) tanpa kenaikan Fmax.
- Register sekitar +192 (ESTIMATE, lebar sinyal); ALM +0 sampai sekitar 650 menurut rentang per-stage Fase 4; DSP tidak berubah di 16.
- Titik impas: S8 butuh median Fmax paling sedikit 1.7 % di atas S7.

## 6. Tidak dicakup
- Perangkat keras (tanpa papan). Formal mencakup kendali dan kapasitas bank, bukan data. Analisis jalur setelah S8 hanya bila tim memintanya. Seed selain 1-6; batasan selain 40.000 ns
  (S8-20 adalah informasi).

## 7. Tata letak evidence
`evidence/phase05m/s8/` (log verifikasi, formal, ekstrak Quartus, worksheet pemilihan, keluaran regresi, ringkasan); ADR untuk S8 (Proposed);
`docs/results/phase05m.md` dan laporan PDF di akhir S8 (hasil fase, kotak Approval dibiarkan kosong).
