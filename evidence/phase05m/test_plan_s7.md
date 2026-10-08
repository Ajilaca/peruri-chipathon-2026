<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Fase 5M, langkah S7: pecah jalur baca memori (P = 6 -> 7) - test plan dan aturan adopsi

Ditulis 2026-10-02, sebelum RTL S7 apa pun dan sebelum pengukuran S7 apa pun (CRG-4). Lingkup dan aturan: ADR 0017, ADR 0019 (catatan amandemen 2: S7 dan S8
direncanakan sebelum Fase 7), ADR 0020 (M6 adalah basis). Konfigurasi basis: M6 (`rtl/ntt/ntt_core_m6_p6.sv`: Barrett, INTT tanpa pass skala,
P = 6, NTT = INTT = 119 siklus; median Fmax MEASURED seed 1-6 34.430 MHz, ALM 9,394-9,441, 16 DSP,
`evidence/phase05m/s6/selection_worksheet.md`). Label: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED.

## 1. Perubahannya (satu perubahan)
Jalur kritis C4b-B / M6 dimulai di stage baca `rtl/mem/poly_mem_multiport_pipe.sv`: register kendali (bank, offset, slot, setelah potongan M) ->
pemilih alamat baca per bank di antara 16 port -> baca penyimpanan (32 word per bank, flip-flop) -> pemilih keluaran (bank, sub-port) di antara 16 port baca ->
`sub_mod` -> pengali. MEASURED (baseline C3-P6, memori yang sama): dekode alamat baca dan mux baca 21.292 ns dari 29.345 ns
(`evidence/phase05/baseline/c3p6_critical_path.md`); untuk C4b-B 21.03 ns + `sub_mod` 4.22 ns + DSP 3.59 ns
(`evidence/phase05/5c/precheck_critical_path.md`). S7 menaruh satu stage register di tengah bacaan itu:

- modul baru `rtl/mem/poly_mem_multiport_split.sv` (`poly_mem_multiport_pipe.sv` yang beku tidak diedit): penyimpanan, peta bank, aturan slot, dan
  arbitrasi sama; parameter `RD_SPLIT` (0 atau 1). Dengan `RD_SPLIT = 1` data baca sub-port per bank (8 bank x 2 sub-port x 12 bit = 192 bit) dan pemilih
  keluaran (bank dan sub-port per port baca, 16 x 4 = 64 bit) diregister antara baca penyimpanan dan pemilih keluaran (register baru: sekitar 256
  bit, ESTIMATE dari lebar sinyal). `rdata_o` lalu muncul `RdLat + RD_SPLIT` siklus setelah permintaan. Kendali tulis ditunda satu siklus lagi
  (`WR_DELAY + RD_SPLIT`) agar tulis tetap mendarat setelah data permintaannya melewati jalur pengali; baca fisik penyimpanan
  tetap pada siklus akhir-arbitrasi.
- inti baru `rtl/ntt/ntt_core_s7.sv` (salinan `ntt_core_m6.sv`; `RdLat` mencakup `RD_SPLIT`, jadi P = RdLat + WrDly = 7), pembungkus `rtl/ntt/ntt_core_s7_p7.sv`
  (potongan sama seperti M6: bit ARB_REG 4, 11, 16; bit MUL_REG 0, 1, 2; `RD_SPLIT = 1`).
- File yang sudah ada dimodifikasi: tidak ada (semua file baru; M6, C4b-B, dan file Fase 1-5 tetap).
Dengan `RD_SPLIT = 0` memori baru harus berperilaku persis seperti yang beku (test V3).

## 2. Kasus sudut (didaftar sebelum test)
- Baca-setelah-tulis alamat sama melintasi batas layer (alamat slack-terketat `tb/mem/bank_model.py`), untuk NTT dan INTT; data terarah-batas dari
  test Fase 4.
- Permintaan beruntun yang mengenai bank sama (dua sub-port dipakai, ketiga = overflow ditandai), port nonaktif, permintaan dengan `wr_i = 0` (baca host), tulis
  host diikuti start (guard `hw_q`), latensi baca-balik host kini 4 siklus.
- Reset di tengah transformasi (tidak ada tulis setelah reset: rantai kendali di-reset), start saat drain.
- Bahaya maksimum: baca alamat yang tulisnya mendarat di siklus yang sama (tidak boleh terjadi; scoreboard) dan kontrol negatif dengan delay tulis lebih dalam.

## 3. Test
| ID | Pemeriksaan | Alat | Disyaratkan |
|---|---|---|---|
| V1 | Lint | Verilator `-Wall`, slang, memori baru, inti, pembungkus | 0 peringatan, 0 error |
| V2 | Unit test memori, `RD_SPLIT = 1`: aliran permintaan acak (baca, tulis, akses host) terhadap acuan Python penyimpanan; data baca pada `RdLat + 1`, waktu pendaratan tulis, `bank_overflow_o` | cocotb `tb/phase5m/test_poly_mem_split.py`, kedua simulator | semua sama dengan acuan; overflow ditandai hanya pada port ketiga per bank |
| V3 | Test diferensial, `RD_SPLIT = 0`: memori baru sama dengan `poly_mem_multiport_pipe.sv` yang beku siklus demi siklus (semua keluaran) pada aliran acak yang sama | cocotb | 0 selisih |
| V4 | Inti lawan golden: NTT, INTT (terhadap `intt()`), round trip, data terarah-batas, siklus konstan, `bank_overflow_o`, scoreboard bahaya, 512 vektor satuan INTT S6 (V6 rencana S6) | cocotb, test Fase 4 diadaptasi di `tb/phase5m/` (latensi baca 4, latensi baca fisik 3 untuk scoreboard), kedua simulator | semua PASS; scoreboard 0 pelanggaran; siklus konstan |
| V5 | Kontrol negatif (salinan khusus test): NCD kendali tulis ditunda `WR_DELAY + RD_SPLIT - 1` (kurang satu siklus, yaitu tidak ditunda oleh `RD_SPLIT`) dan NCS pemilih keluaran (bank, sub-port) TIDAK ditunda bersama data baca terregister | cocotb | hasil harus SALAH dan pemeriksaan scoreboard / bit-exact FAIL |
| V6 | Formal H, O, R, A, B, C `ntt_core_s7_formal_top.sv` (salinan top M6 dengan model delay untuk P = 7, RdLat = 4) dengan NC-O dan NC-A | SymbiYosys | PASS; kontrol FAIL |
| V7 | Regresi Fase 0-5 | tidak dijalankan untuk S7: Amandemen A1 `test_plan.md` (S7 tidak memodifikasi file yang ada; S8 menjalankan regresi sekali pada pohon akhir) | - |
| V8 | Revisi Quartus `S7` (seed 1) dan `S7-s2` .. `S7-s6`, 40.000 ns, bawaan Quartus, kompilasi penuh dari db bersih, satu per satu | `quartus_sh --flow compile` | file evidence diekstrak dari root repository |

## 4. Aturan adopsi (ditetapkan sebelum mengukur)
S7 (revisi `S7`, seed 1-6) diadopsi sebagai basis untuk S8 hanya bila semua berikut berlaku:
1. benar: V1-V6 PASS di kedua simulator, kontrol negatif V5 gagal seperti disyaratkan;
2. siklus konstan dan tepat NTT 120 / INTT 120 (P = 7, tanpa stall; NTT = 113 + 7, INTT = NTT; ESTIMATE sampai disimulasikan);
3. ALM inti NTT <= 12,573 di setiap seed; timing terpenuhi pada 40.000 ns di setiap seed (setup terburuk >= 0, hold terburuk >= 0);
4. ADR 0012 terhadap langkah sebelumnya M6 pada median Fmax seed 1-6-nya (34.430 MHz, t_NTT = t_INTT = 119 / 34.430 = 3.456 us): dengan F median atas
   seed 1-6 dari Fmax slow corner terendah S7, t_NTT = 120 / F < 3.456 us dan t_INTT = 120 / F < 3.456 us, yaitu F > 34.720 MHz (perhitungan tim).
Catatan yang ditetapkan sekarang:
- Tidak ada toleransi yang ditambahkan. Kenaikan S7, bila ada, harus melebihi sebaran seed agar terlihat (seed M6 32.35-35.04 MHz, C4b-B 33.46-34.84 MHz, INFERENCE); median di atas
  34.720 MHz kurang dari sebaran tetap lulus menurut aturan tetapi dilaporkan dengan catatan itu; kegagalan kurang dari sebaran tidak diadopsi menurut aturan dan
  tim memutuskan (C5), seperti untuk S6. Adopsi M6 oleh tim meskipun kurang 0.25 % (ADR 0020) bukan preseden dan tidak mengubah ambang apa pun.
- Bila stall diperlukan (siklus bukan 120 / 120), S7 sebagaimana didefinisikan gagal pada kondisi 2 dan dilaporkan; desain S8 berbasis stall lalu direncanakan ulang oleh tim.
- Kotak waktu yang diusulkan (tim boleh mengubah): vonis S7 paling lambat Sabtu 2026-10-03 malam, S8 paling lambat Senin 2026-10-05 siang; Fase 7 dimulai setelah vonis S8 atau pada
  waktu itu, mana yang lebih dulu (ADR 0019).

## 5. Harapan (ESTIMATE, ditulis sebelum mengukur; hanya kompilasi yang bisa memastikan)
- Siklus +1 (119 -> 120). Register ditaruh di dalam segmen baca 21 ns; bila kedua separuh kira-kira sama, segmen baca dapat menyusut sampai
  kira-kira separuh (INFERENCE, tidak terukur: laporan menggabungkan segmen baca sebagai satu delay 21.292 ns). Kelas jalur berikutnya (slack MEASURED, C4b-B pada 40 ns:
  segmen tulis 17.1 ns, jalur samping 12.1 ns) membatasi kenaikan yang dapat dicapai: jalur terburuk sekitar 25 ns berarti sekitar 40 MHz.
- ALM: 0 sampai sekitar 650 lebih banyak (paket keputusan, ESTIMATE; dibatasi rentang biaya per-stage terukur Fase 4), register sekitar +256. DSP tidak berubah di 16.
- Hasilnya bisa lulus atau gagal pada kondisi 4: derau seed (sekitar +-0.7 MHz) sebanding dengan kenaikan kecil.

## 6. Tidak dicakup
- Perangkat keras (tanpa papan). Formal mencakup kendali dan kapasitas bank, bukan data. Tanpa analisis jalur setelah S7 kecuali tim memintanya. Batasan selain 40.000 ns
  (kompilasi informasi 20 ns milik S8). Regresi Fase 0-5 (S8).

## 7. Tata letak evidence
`evidence/phase05m/s7/` (log verifikasi, formal, ekstrak Quartus, worksheet pemilihan, ringkasan); ADR untuk S7 (Proposed) dengan hasilnya.

## Amandemen A1 (2026-10-02, ditulis sebelum pengukuran S7 apa pun)
Test V5 sebagaimana ditulis pertama mendaftar dua kontrol negatif NCD dan NCW; dengan `RD_SPLIT = 1` keduanya adalah mutan yang sama (delay tulis `WR_DELAY + RD_SPLIT - 1` adalah
persis "tidak ditunda oleh `RD_SPLIT`"). NCW diganti NCS (pemilih keluaran tidak ditunda bersama data baca), kesalahan lain yang independen. Ambang
dan aturan adopsi tidak berubah. Formal V6 memakai RdLat = 3 (baca fisik) untuk properti C dan P = 7 untuk properti A.
