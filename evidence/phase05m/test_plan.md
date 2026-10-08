<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Fase 5M, langkah S6: INTT tanpa pass skala - test plan dan aturan adopsi

Ditulis 2026-10-02, sebelum RTL S6 apa pun dan sebelum pengukuran S6 apa pun (CRG-4). Lingkup dan aturan: ADR 0017 (Accepted). Konfigurasi
basis: C4b-B (Barrett, ADR 0013 Accepted), `rtl/ntt/ntt_core_c4b_b.sv`, P = 6, potongan seperti C4b-B. Label: MEASURED,
INFERENCE, ESTIMATE, NOT MEASURED.

## 1. Perubahannya (satu perubahan)
FIPS 203 Algoritma 10 menjalankan 7 layer Gentleman-Sande lalu mengalikan setiap koefisien dengan 3303 (= 128^-1 mod q). C4b-B melakukan
perkalian itu sebagai pass terpisah atas 256 alamat (`S_SCALE`, satu pengali tambahan, 256 siklus). S6 menghapus pass itu dengan membagi dua
di setiap layer (3303 = 2^-7 mod q dan INTT punya 7 layer):

| | per butterfly INTT, masukan a, b < q | konstanta |
|---|---|---|
| FIPS 203 / C4b-B | a' = (a + b) mod q;  b' = (zeta * (b - a)) mod q | pass skala sesudahnya: x * 3303 mod q |
| S6 | a' = half_mod((a + b) mod q);  b' = (zeta' * (b - a)) mod q, zeta' = zeta * 1665 mod q | tidak ada; tabel zeta' dibangkitkan oleh skrip |

dengan `half_mod(x) = (x + (x[0] ? q : 0)) >> 1` untuk x dalam [0, q). Mode NTT tidak berubah (entri ROM sama, persamaan butterfly sama).
Inti kehilangan state `S_SCALE`, pengali skala, dan reducer Barrett-nya; INTT lalu punya jadwal yang sama dengan NTT.

### Argumen ekuivalensi (matematika tidak diubah, C1)
1. q ganjil, jadi 2 punya invers mod q: 2 * 1665 = 3330 = 1 (mod q). Untuk x dalam [0, q), x/2 mod q adalah x/2 bila x genap dan (x + q)/2 bila x
   ganjil; keduanya < q (x < q memberi (x + q)/2 < q), jadi `half_mod` persis perkalian dengan 2^-1 mod q pada [0, q).
2. zeta * (b - a) * 2^-1 = (zeta * 1665 mod q) * (b - a) (mod q), jadi keluaran b' butterfly yang dibagi dua adalah 2^-1 kali b' standar.
3. Karena itu satu layer yang dibagi dua sama dengan layer standar dikalikan 2^-1 (peta linear atas Z_q kali skalar). Tujuh layer tersusun menjadi
   2^-7 kali INTT standar tanpa skala. 128 * 3303 = 422,784 = 127 * 3329 + 1, jadi 2^-7 = 128^-1 = 3303 (mod q) dan hasilnya sama dengan
   Algoritma 10 termasuk baris akhirnya, untuk setiap masukan dalam [0, q)^256.
4. Rentang nilai: semua nilai tersimpan tetap dalam [0, q) (half_mod, add_mod, keluaran reducer), jadi kontrak operand D6 reducer
   ([0, q) x [0, q), ADR 0011) tidak berubah.
Diperiksa, tidak diasumsikan: bagian 3 V2-V7.

## 2. Kasus sudut (didaftar sebelum test)
- half_mod: x = 0, 1, 2, q-2, q-1 (tepi ganjil/genap), setiap x dalam [0, q) secara menyeluruh (3,329 nilai).
- Masukan INTT: semua 256 vektor satuan e_i; semua 256 vektor (q-1) * e_i; semua-nol; semua-(q-1); bergantian 0 / q-1; semua-1; ramp 0..255 mod q;
  1,000 vektor acak di test golden; 100 acak + polinomial sudut Fase 4 di test RTL (test Fase 4 tidak berubah).
- ROM: setiap entri zeta' untuk 127 indeks yang dialamati INTT, pada batas layer (indeks 127, 64, 63, 32, 31, 16, 15, 8, 7, 4, 3, 2, 1).
- Jadwal: tidak berubah dari C4b-B selain pass skala yang dihapus (scoreboard bahaya Fase 4 dipakai ulang, 0 pelanggaran disyaratkan).

## 3. Test
| ID | Pemeriksaan | Alat | Disyaratkan |
|---|---|---|---|
| V1 | Lint | Verilator `-Wall`, slang, untuk inti dan pembungkus baru | 0 peringatan, 0 error |
| V2 | `half_mod` menyeluruh, modul RTL `rtl/arith/half_mod.sv` | cocotb di Verilator dan Icarus | 3,329/3,329: hasil < q dan 2 * hasil = x (mod q); kontrol negatif (mutan menambah q untuk masukan genap) harus gagal |
| V3 | Golden: `intt_halving()` (tb/golden/intt_halving.py) sama dengan `intt()` | pytest | semua vektor bagian 2 sama; kontrol negatif: varian yang melewati pembagian dua di satu layer (kedua keluaran layer itu) harus berbeda |
| V4 | ROM zeta' dibangkitkan dari model golden | `scripts/build/gen_twiddle_rom_half.py` dijalankan ulang mereproduksi file byte demi byte; skrip pemeriksa membandingkan setiap entri dengan `zeta * 1665 mod q` dan separuh NTT dengan `twiddle_rom.sv` yang beku | 0 selisih |
| V5 | Inti lawan golden, test Fase 4 tidak berubah `tb/ntt/test_ntt_core_c3.py`: NTT, INTT (dibandingkan dengan `intt()` asli yang mencakup skala 3303), round trip, data terarah-batas, siklus konstan, scoreboard, `bank_overflow_o` | cocotb di Verilator dan Icarus | semua PASS; siklus konstan; NTT = INTT = 119 |
| V6 | INTT inti atas 256 vektor satuan dan 256 vektor satuan (q-1), dibandingkan dengan `intt()` dan `intt_halving()` | cocotb `tb/phase5m/test_m6_basis.py`, kedua simulator | 512/512 sama dengan keduanya |
| V7 | Kontrol negatif RTL (salinan khusus test, RTL repository tidak tersentuh): NCH `half_mod` dilewati di jalur-a INTT; NCR entri zeta' INTT satu layer diganti zeta (pembagian dua dibuang di sisi b); NCM mutan `half_mod` | cocotb | INTT bit-exact harus FAIL pada masing-masing |
| V8 | Properti kendali dan bank formal H, O, R, A, B, C pada pembungkus baru (top Fase 5 dipakai ulang sebagai salinan dengan encoding baru), dengan NC-O dan NC-A | SymbiYosys | PASS; kontrol negatif FAIL |
| V9 | Regresi: `scripts/test/phase5_regression.sh` dan `scripts/test/phase5_verify.sh` tidak berubah | skrip | OVERALL PASS |
| V10 | Quartus: revisi `M6` (seed 1) dan `M6-s2` .. `M6-s6`, 40.000 ns, bawaan Quartus, satu per satu, latar belakang | `quartus_sh --flow compile` | file evidence diekstrak oleh `extract_quartus_report.py` |

## 4. Aturan adopsi (ditetapkan sebelum mengukur)
S6 (revisi `M6`, seed 1-6) diadopsi sebagai basis untuk S7 hanya bila semua berikut berlaku:
1. benar: V1-V9 PASS, kedua simulator, V7 dan kontrol negatif V2/V3 gagal seperti disyaratkan;
2. siklus konstan dan tepat NTT 119 / INTT 119 (pass skala INTT hilang; INTT = siklus NTT);
3. ALM inti NTT <= 12,573 di setiap seed, dan timing terpenuhi pada 40.000 ns di setiap seed (setup terburuk >= 0, hold terburuk >= 0);
4. ADR 0012 terhadap langkah sebelumnya C4b-B pada median Fmax seed 1-6-nya (34.515 MHz; t_NTT = 3.448 us, t_INTT = 10.865 us,
   `evidence/phase05/5b/selection_worksheet.md`): dengan F median atas seed 1-6 dari Fmax slow corner
   terendah M6, t_NTT = 119 / F < 3.448 us dan t_INTT = 119 / F < 10.865 us.
Catatan yang ditetapkan sekarang, agar tidak dapat diperdebatkan setelah pengukuran:
- t_INTT membaik dari 375 ke 119 siklus menurut konstruksi (INFERENCE); bagian yang mengikat dari kondisi 4 adalah bagian NTT, yaitu
  F > 34.515 MHz, karena mode NTT tidak berubah dalam siklus. Bagian itu ditentukan oleh Fmax terukur, yang bervariasi menurut seed sekitar
  +-0.7 MHz (C4b-B 33.46-34.84 MHz): kerugian di sana mungkin terjadi tanpa perubahan pada jalur NTT.
- Tanpa toleransi pada kondisi 4. Bila M6 gagal hanya karena bagian NTT, M6 dilaporkan sebagai terukur dan tidak diadopsi oleh
  aturan; apakah aturan lain berlaku adalah keputusan baru tim (C5), tidak dibuat di sini.
- Bila M6 tidak diadopsi, S7 tidak dimulai sampai tim memutuskan basisnya (C4b-B atau M6).

## 5. Harapan (ESTIMATE, ditulis sebelum mengukur; hanya kompilasi yang bisa memastikan)
- Siklus: INTT 375 -> 119 (aritmetika jadwal: 7 layer x 16 siklus + 1 + P = 119, sama dengan NTT; pass skala 256 siklus hilang).
- DSP: diharapkan 18 -> 16 (pengali skala dihapus). ALM: tanda tidak diketahui. Dihapus: satu reducer dan datapath skala. Ditambah: 8 unit `half_mod`
  dan ROM twiddle 256-entri per lajur sebagai ganti 128 entri. Register: kira-kira tidak berubah.
- Fmax: jalur-a INTT memindahkan `half_mod` ke segmen tulis (slack lebih banyak dari segmen baca, slack MEASURED C4b-B: segmen tulis
  17.1 ns lawan segmen baca 11.0 ns pada 40 ns), jadi tidak diharapkan ada kehilangan Fmax darinya; pemilih ROM pada jalur zeta tidak diharapkan kritis.

## 6. Tidak dicakup
- Perangkat keras (tanpa papan). Formal mencakup kendali dan kapasitas bank, bukan aritmetika; aritmetika bertumpu pada V2-V7.
- INTT atas nilai di luar [0, q) tidak dispesifikasikan (antarmuka host menulis nilai 12-bit; golden dan test memakai [0, q)).
- Seed selain 1-6, batasan selain 40.000 ns (kompilasi informasi 20 ns milik S8).

## 7. Tata letak evidence
`evidence/phase05m/s6/` (log verifikasi, formal, ekstrak Quartus, worksheet pemilihan, ringkasan);
`docs/results` mendapat file hasil Fase 5M hanya di akhir fase (tidak untuk S6 saja).

## Amandemen A1 (2026-10-02, diputuskan Jevan, Team J5, chat: "setuju usulan, kita lakukan verifikasi pada s8 saja")
- V9 (regresi penuh Fase 0-5, CRG-5) tidak dijalankan per langkah. Ia dijalankan sekali, di S8, pada pohon akhir urutan S6-S8 (dan lagi
  bila langkah berikutnya mengubah file yang ada). Alasan: S6 hanya menambah file; `git diff --name-status 288a78c HEAD` pada saat keputusan ini
  menunjukkan 33 file ditambah dan 0 file yang ada dimodifikasi, jadi RTL, test, dan bukti Fase 1-5 tidak tersentuh. Untuk S6, "benar" pada
  bagian 4 kondisi 1 karenanya berarti V1-V8 ditambah evidence `git diff` itu; V9 tidak dijalankan untuk S6 dan laporan S6 menyatakannya.
- Run regresi yang sedang berjalan saat ini diputuskan dihentikan dan keluaran parsialnya dibuang (bukan evidence).
- Ambang bagian 4 (kondisi 2-4) tidak berubah. Angka Quartus S6 sudah diketahui saat amandemen ini dibuat; amandemen
  hanya menyangkut kapan regresi dijalankan, bukan apa yang dibandingkan aturan adopsi.
- Test plan S7 dan S8 harus menyatakan file yang ada mana yang mereka modifikasi; regresi S8 mencakup S6, S7, dan S8 bersama.
