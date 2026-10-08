<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# S10 (di dalam Fase 6, ADR 0024): memori 16 x 1R1W bank tanpa arbitrasi slot - test plan dan aturan adopsi

Ditulis 2026-10-03, sebelum RTL S10 apa pun dan sebelum pengukuran S10 apa pun (CRG-4). Dasar: ADR 0022 opsi A (studi S9: peta `bank = (a1^a2^a3^a4, a7, a6, a5)`, `offset = a[3:0]` memberi paling banyak satu baca
dan satu tulis per bank per siklus sepanjang jadwal, `evidence/phase05m/s9/port_analysis.txt`) dan analisis jalur S7 (batas terukur S7 adalah riak arbitrasi slot
antara potongan A_4 dan A_11, `evidence/phase05m/fmax50/path_analysis.md`). Basis: S7 (`rtl/ntt/ntt_core_s7_p7.sv`). Label: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED.

## 1. Perubahannya (satu perubahan: memori)
- memori baru `rtl/mem/poly_mem_m10k.sv`: daftar port sama dengan `poly_mem_multiport_split.sv` (en, wr, addr per port, rdata, wdata, bank_overflow_o), 16 bank 16 x 12 bit, bank dan offset menurut peta di atas (XOR murni dan
  pemilihan bit, tanpa ROM, tanpa arbitrasi). Per bank: alamat baca dan alamat tulis / data / enable dipilih dari satu port yang banknya cocok (pilihan 16-arah); per port data baca dipilih
  dari banknya (pilihan 16-arah). Setiap bank ditulis sebagai RAM simple-dual-port baca-sinkron (`ramstyle` "M10K", read-during-write pada word yang sama tidak diandalkan); apakah Quartus memetakannya ke M10K
  dilaporkan, tidak diasumsikan.
- Timing: alamat permintaan diambil RAM di akhir siklus permintaan (baca fisik pada siklus permintaan), data baca dipilih dan diregister: data baca `RD_LAT = 2` siklus setelah
  permintaan; tulis sebuah permintaan mendarat di akhir siklus `request + RD_LAT + WR_DELAY` dengan bank dan offset permintaan (ditunda). `bank_overflow_o`: dua port aktif atau lebih pada satu bank dalam satu siklus permintaan,
  diregister (satu siklus kemudian).
- inti baru `rtl/ntt/ntt_core_s10.sv` (salinan `ntt_core_s7.sv`: instans memori diganti, `RdLat = RD_LAT`), pembungkus `rtl/ntt/ntt_core_s10_p5.sv` (RD_LAT 2, bit MUL_REG 0, 1, 2: P = 5). Jadwalnya adalah jadwal
  S7; P = 5 tidak butuh stall (tabel stall: tidak ada sampai P = 7). Siklus: 113 + 5 = 118 (ESTIMATE sampai disimulasikan).
- File yang sudah ada dimodifikasi: tidak ada.

## 2. Kasus sudut
- Setiap alamat melalui setiap port; lalu lintas terjadwal kedua arah beruntun (16 port, setiap bank sekali per siklus); baca pada siklus pendaratan (nilai lama) dan siklus sesudahnya (nilai baru).
- Dua port pada satu bank dalam satu siklus (harus mengaktifkan `bank_overflow_o`); satu port per bank (tidak boleh). Akses host lewat port 0 di IDLE (satu port).
- Tingkat inti: test inti Fase 4 / S7 tidak berubah isinya (NTT, INTT, round trip, data batas, siklus konstan, scoreboard, 512 vektor satuan INTT).

## 3. Test
| ID | Pemeriksaan | Alat | Disyaratkan |
|---|---|---|---|
| V1 | Lint memori, inti, pembungkus | Verilator `-Wall`, slang | 0 peringatan, 0 error |
| V2 | Memori lawan model Python akurat-siklus (salinan test memori S7 dengan latensi baru dan aturan konflik 16-bank) | cocotb `tb/s10/test_poly_mem_m10k.py`, kedua simulator | semua sama; overflow hanya bila dua port berbagi bank |
| V3 | Inti lawan golden (`tb/phase5m/test_ntt_core_s7.py` dengan C3_RDLAT 2, C3_RDPHYS 0, C3_WRDLY 3) | cocotb, kedua simulator | semua PASS; 0 pelanggaran scoreboard; siklus konstan 118 / 118 |
| V4 | Kontrol negatif (salinan khusus test): NC-M peta bank tanpa bit XOR (`bank = {a7, a6, a5, a4}`): overflow dan hasil salah; NC-W kontrol tulis kurang satu siklus | cocotb | FAIL bit-exact (NC-M juga mengaktifkan `bank_overflow_o`) |
| V5 | Formal: H, O, R, A, C dari salinan top formal S7 untuk memori baru (probe diganti nama) dengan NC-O (mutan peta) dan NC-A | SymbiYosys | PASS; kontrol FAIL |
| V6 | Top Fase 6 dengan inti S10 (CORE_RDLAT 2): test V5 Fase 6 | cocotb, kedua simulator | semua PASS (informasi: siklus per program) |
| V7 | Quartus `S10` seed 1-6 pada 40.000 ns, satu per satu; ditambah `S10-20` seed 1-6 pada 20.000 ns (informasi, sebanding dengan sapuan S7-20 pertanyaan 50 MHz) | `quartus_sh` | evidence diekstrak |

## 4. Aturan adopsi (ADR 0012, ditetapkan sebelum mengukur)
S10 menggantikan S7 sebagai memori inti hanya bila semua berikut berlaku: (1) V1-V6 PASS, kontrol gagal; (2) siklus tepat 118 / 118 dan konstan; (3) ALM <= 12,573 dan timing terpenuhi pada 40.000 ns di setiap seed; (4) dengan F median atas
seed 1-6 dari Fmax slow corner terendah pada 40 ns: 118 / F < 120 / F_S7 (F_S7 = 38.720 MHz dihitung ulang dari file S7), yaitu F > 38.075 MHz. Tanpa toleransi. Apakah hasil pada 20 ns memenuhi 50 MHz dilaporkan,
bukan bagian aturan.

## 5. Harapan (ESTIMATE, ditulis sebelum mengukur)
Riak arbitrasi (jalur S7 terburuk terukur, sekitar 25.6 ns) dihilangkan; jalur baru: aritmetika alamat -> peta XOR -> pilihan 16-arah -> alamat RAM (pendek), data RAM -> pilihan 16-arah -> register, pengali ->
pilihan tulis 16-arah -> RAM. Fmax dapat naik; ia juga dapat dibatasi oleh timing M10K atau oleh segmen butterfly / tulis (S7: pengali ke tulis sekitar 22.3 ns). M10K: 16 blok lebih banyak bila alat memetakan bank
ke sana; ALM: lebih rendah (tanpa 3,072 flip-flop penyimpanan, tanpa arbitrasi) atau lebih tinggi (crossbar), tidak dapat diprediksi dari studi (batas atas crossbar sekitar 1,920 ALM, ESTIMATE).

## Amandemen A1 (2026-10-03, setelah run inti S10 pertama, sebelum run Quartus apa pun)
Run pertama V3 dengan test S7 yang tidak diubah gagal hanya pada pemeriksaan latensi start (`start_i taken only after 6 cycles`, batas `WRDLY + 2` = 5). Batas itu mengodekan guard tulis host S7
(pendaratan dikurangi baca fisik = WRDLY + 1). Di S10 penyimpanan dibaca pada siklus permintaan, jadi guard adalah seluruh pipa (5) dan start memakan 6 siklus; inti benar menurut konstruksi guard
(tulis host harus mendarat sebelum baca transformasi pertama). V3 kini menjalankan `tb/s10/test_ntt_core_s10.py`, salinan test S7 yang batasnya `(RDLAT - RDPHYS + WRDLY) + 1` (5 untuk S7, 6 untuk S10); tidak ada hal lain di
test yang berubah. Ambang dan aturan adopsi tidak berubah.
