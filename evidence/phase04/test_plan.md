# Test plan Fase 4 - sapuan pipeline butterfly P = 0 / 2 / 4 / 6 (C3), ditulis sebelum RTL apa pun dikodekan (CRG-4)

- Tanggal (UTC): 2026-09-30. Branch `phase4-pipeline`. Tidak ada RTL, testbench, atau proyek Quartus Fase 4 yang ada
  saat penulisan.
- Keputusan yang mengatur: ADR 0005 (mulai dari C2-K2-K1 pada L = 8), ADR 0006 (batasan dan
  milestone Fase 4: 40.000 ns; 25 MHz adalah target eksperimental, bukan persyaratan perangkat keras atau sistem; tujuan akhir
  20.000 ns setelah Fase 5), ADR 0007 (P ∈ {0, 2, 4, 6}; register diizinkan di dalam jalur akses memori
  dan pembagi; fungsi harus tetap bit-exact; aturan pemilihan). ADR 0004 tidak berubah (anggaran ALM
  10,478).
- Acuan: `tb/golden/primitives.py` (`ntt`, `intt`), `tb/mem/bank_model.py`.
- Evidence perencanaan: `k1_l8_worst_path_breakdown.md` (jalur MEASURED titik awal),
  `layer_boundary_slack.txt` (analisis jadwal, perhitungan tim).

## 1. Apa yang dibangun dan apa yang tetap beku
Beku, tidak diedit di Fase 4: `rtl/ntt/modmul_reduce.sv`, `butterfly.sv`, `butterfly_shared.sv`,
`twiddle_rom.sv`, `rtl/mem/bank_map_rom.sv`, `poly_mem_multiport.sv`, `ntt_core_c2*.sv` dan
pembungkusnya, semua evidence Fase 1–3.

P = 0 bukan RTL baru. Ia adalah `rtl/ntt/ntt_core_c2_k2_k1_l8.sv` yang beku dikompilasi ulang dengan batasan
Fase 4 (revisi `C3-P0`). Evidence simulasinya adalah regresi Fase 3 yang ada, dijalankan ulang.

File baru yang direncanakan (nama boleh disesuaikan; pemisahannya tidak):
| File | Isi |
|---|---|
| `rtl/ntt/modmul_reduce_staged.sv` | (a·b) mod q dengan reduksi ditulis sebagai stage kurangi-bersyarat eksplisit agar register dapat diletakkan di antara stage. Hasil sama dengan `modmul_reduce.sv` untuk setiap a, b dalam [0, q). Parameter: setelah stage mana register diletakkan |
| `rtl/ntt/butterfly_shared_pipe.sv` | persamaan `butterfly_shared.sv` dengan reducer staged dan operand yang melewati pengali ditunda sebanyak stage yang sama |
| `rtl/mem/poly_mem_multiport_pipe.sv` | Memori dengan pengalamatan baca dan tulis terpisah per port; arbitrasi slot dengan stage register opsional; (bank, offset, slot) yang dihitung untuk bacaan sebuah port ditunda dan dipakai ulang untuk tulisnya |
| `rtl/ntt/ntt_core_c3.sv` | FSM dan jadwal C2-K2-K1, parameter `PIPE ∈ {2, 4, 6}`, delay line valid/alamat, drain di akhir |
| `rtl/ntt/ntt_core_c3_p2.sv`, `_p4.sv`, `_p6.sv` | Pembungkus Quartus tipis, L = 8 tetap |

Pass skala INTT ×3303 menjaga pengali + reducer staged sendiri dan memakai port 0, dengan kedalaman
pipeline yang sama dengan butterfly. Berbagi pengali itu dengan sebuah lajur adalah optimasi lain dan
di luar lingkup.

## 2. Posisi register per P (ditetapkan di sini, sebelum apa pun diukur)
P menghitung stage register antara siklus alamat sebuah butterfly diterbitkan dan siklus
hasilnya ditulis (ADR 0007). Titik potong bernama, dari jalur terukur titik awal:

| Potongan | Di mana |
|---|---|
| A_k | di dalam riak arbitrasi slot, setelah ia memproses k dari 16 port (hanya kendali: bergantung pada `layer_q`, `t_q`, `mode_q`, tidak pernah pada data polinomial) |
| M | setelah arbitrasi slot selesai (bank, offset, slot per port diregister), sebelum mux baca |
| X | setelah pengali (hasil kali 24-bit), sebelum stage reduksi pertama |
| D_n | di dalam reducer, setelah n stage kurangi-bersyaratnya (13 pada pembagi hasil inferensi titik awal; jumlah stage persis N reducer staged ditetapkan saat ia ditulis, dan n diskalakan sebagai round(n·N/13)) |

| P | Potongan | Segmen terpanjang yang diharapkan (ESTIMATE dari satu jalur terukur; bukan prediksi Fmax) |
|---|---|---|
| 0 | tidak ada (C2-K2-K1 beku) | 129.6 ns delay data, MEASURED |
| 2 | A_13, D_3 | sekitar 45 ns - tidak diharapkan memenuhi 40.000 ns (tiga bagian sama jalur ini sekitar 44 ns); tetap diukur, seperti disyaratkan ADR 0007 |
| 4 | A_7, M, X, D_7 | sekitar 30 ns |
| 6 | A_4, A_11, M, X, D_5, D_11 | sekitar 24 ns (segmen mux baca + pengali) |

Aturan terhadap penyetelan setelah kejadian: posisi ini dipakai untuk revisi terukur. Bila sebuah posisi
harus berubah karena alasan kebenaran atau alat, rencana ini diamandemen dengan alasannya sebelum
revisi Quartus terkait dikompilasi. Bila sebuah posisi diubah setelah hasil Quartus terlihat,
penempatan baru adalah revisi bernama terpisah (misalnya `C3-P4b`), kedua hasil disimpan dan
dilaporkan, dan aturan pemilihan diterapkan pada revisi yang dinamai di tabel ini kecuali tim memutuskan
lain.

## 3. Bahaya dan jumlah siklus (harapan yang akan diperiksa, tidak diasumsikan)
- Dalam satu layer setiap alamat dibaca sekali dan ditulis sekali, jadi tidak ada bahaya baca-setelah-tulis untuk
  P mana pun. Pada batas layer jadwal yang ada punya paling sedikit 7 siklus slack pada L = 8 di kedua
  arah, dan 15 siklus sebelum pass skala INTT (`layer_boundary_slack.txt`), jadi
  P ≤ 6 tidak butuh stall. Ini analisis model jadwal Python; RTL harus mendemonstrasikannya.
- Jumlah siklus yang diharapkan (ESTIMATE): NTT = 113 + P, INTT = 369 + P (C2-K2-K1 terukur 113 / 369; pipeline
  menambah drain P siklus di akhir). Nilai terukur yang dicatat.
- Siklus stall per P dilaporkan sebagai: siklus terukur − (7 × 16 + [256 untuk INTT] + 1 + P). Diharapkan 0.
- Dengan P > 0 sebuah bank menerima hingga 2 baca dan 2 tulis alamat berbeda per siklus; jadwal baca
  dan jadwal tulis masing-masing menjaga properti "paling banyak 2 per bank" secara terpisah.

## 4. Verifikasi, per P ∈ {2, 4, 6} (dan regresi yang ada untuk P = 0)
Setiap butir dijalankan di kedua simulator (Icarus dan Verilator) kecuali dinyatakan lain; ketidaksepakatan di
antara keduanya diselidiki sebelum salah satunya dipercaya.

V1. Lint / elaborasi (CRG-1, CRG-2). `verilator --lint-only -Wall` dan `slang`, 0 peringatan, untuk
setiap nilai PIPE dan setiap pembungkus. Tidak ada baris komentar yang boleh diawali kata "synthesis" (jebakan pragma
Quartus yang ditemukan di Fase 3).

V2. Reducer staged sama dengan `modmul_reduce` (pemeriksaan "fungsi tidak boleh berubah").
- Menyeluruh: setiap (a, b) dalam [0, q)², 3329² = 11,082,241 pasangan, untuk setiap konfigurasi register yang dipakai
  P = 2, 4, 6, membandingkan keluaran staged (setelah latensinya) dengan `modmul_reduce` dan dengan
  rumus bilangan bulat (a·b) mod 3329. Harness C++ Verilator, pola sama dengan `tb/ntt/k1_exhaustive/`.
- Kasus sudut juga sebagai unit test cocotb: a = 0, b = 0; a = b = q−1; a = 1; b = 1; a = q−1, b = 1;
  hasil kali tepat di bawah dan di atas kelipatan q.
- Latensi: keluaran untuk masukan yang diberikan pada siklus t muncul tepat pada t + (jumlah stage), untuk
  masukan beruntun (tanpa gelembung di antaranya).

V3. Butterfly pipeline lawan langkah butterfly golden. Sudut (a = b = 0; a = b = q−1; a = 0, b = q−1;
a = q−1, b = 0; zeta = entri tabel pertama dan terakhir) dan 1,000 (a, b, zeta) acak per mode dengan zeta dari
tabel golden, dialirkan beruntun; setiap hasil dibandingkan pada latensi yang diharapkan.

V4. Varian memori. Tulis lalu baca balik setiap alamat melalui setiap port; baca dan
tulis bersamaan alamat berbeda pada bank yang sama dalam satu siklus; baca alamat pada siklus setelah
ia ditulis mengembalikan nilai baru; `bank_overflow_o` tidak pernah aktif untuk lalu lintas terjadwal.

V5. Inti bit-exact (CRG-3). Untuk setiap P: `ntt(f)` dan `intt(f)` sama dengan `tb/golden/primitives.py` untuk
lima polinomial sudut (semua nol; semua q−1; impuls di 0; impuls di 255; bergantian 0 / q−1) dan 100
polinomial acak per arah; `intt(ntt(f)) == f` untuk 50 polinomial acak.

V6. Jumlah siklus konstan (CRG-7). Untuk setiap P dan setiap arah jumlah siklus start-ke-done
identik untuk setiap sudut dan 20 polinomial acak; nilainya dicatat dan harus sama di kedua
simulator. Nilai ini adalah `cycles_NTT(P)` / `cycles_INTT(P)` aturan pemilihan.

V7. Test bahaya batas layer.
- Scoreboard testbench melacak, untuk setiap alamat, apakah sebuah tulis masih di pipeline; ia gagal bila
  ada baca diterbitkan untuk alamat seperti itu, atau bila baca dan tulis mengenai alamat sama dalam satu siklus.
  Ia berjalan selama semua test V5.
- Data terarah: polinomial yang koefisiennya berbeda hanya pada alamat dengan slack batas terketat
  (dari `scripts/test/pipeline_hazard_slack.py`), sehingga baca basi di sana mengubah hasil.
- Kontrol negatif: elaborasi khusus test dengan kedalaman melebihi slack (PIPE = 8, tidak pernah dikompilasi di
  Quartus, tidak pernah kandidat) harus memicu scoreboard dan gagal bit-exact. Bila tidak,
  scoreboard tidak melakukan tugasnya dan V7 batal.

V8. `bank_overflow_o` disampel setiap siklus setiap test inti dan harus tetap 0.

V9. Formal (CRG-8), dengan alur terkoreksi (`formal/run/run_formal_slang.py`: frontend yosys-slang,
`memory_map -rom-only`), per P: handshake busy/done; `bank_overflow_o` == 0; rentang counter; rantai
valid pipeline mengalir habis tepat P siklus setelah issue terakhir; tidak ada baca dan tulis alamat sama pada siklus yang sama. Kontrol negatif seperti di Fase 3 (salinan `bank_map_rom` yang dirusak harus gagal). Lingkup dinyatakan di
hasil: properti kendali dan kapasitas bank, bukan aritmetika.

V10. Regresi (CRG-5, CRG-6). pytest Fase 0, regresi cocotb Fase 1–3 (termasuk varian `k2` dan `k1`)
dan `check_params.py` tetap lulus; `run_formal_slang.py` tetap melaporkan setiap bukti yang ada sebagaimana
diharapkan.

V11. Acuan P = 0. `python3 tb/ntt/run_ntt_c2_tests.py <sim> k1` di kedua simulator; L = 8 harus
tetap memberi NTT 113 / INTT 369.

Sebuah nilai P punya "bit-exact: PASS" (kondisi 1 ADR 0007) hanya bila V2, V3, V5, dan V7 semuanya lulus di kedua
simulator, dan "siklus konstan: PASS" (kondisi 2) hanya bila V6 lulus.

## 5. Quartus (CRG-9), keempat revisi
- Proyek `quartus/phase04_pipeline_c3/`, revisi `C3-P0`, `C3-P2`, `C3-P4`, `C3-P6`. Device
  5CSEBA6U23I7, Quartus Prime Lite 25.1std, kernel-only dengan virtual pin, assignment sama dengan revisi
  Fase 3; QSF berbeda hanya pada top entity, folder keluaran, dan daftar file RTL.
- Satu SDC untuk keempatnya: `create_clock -name clk_i -period 40.000 [get_ports {clk_i}]`,
  `derive_clock_uncertainty`, `set_false_path -from [get_ports {rst_ni}]` - SDC Fase 3 dengan hanya
  periode yang diubah. Seed fitter: bawaan, seperti di Fase 1–3, sama untuk keempatnya.
- `C3-P0` dikompilasi pada sesi yang sama dengan yang lain; hasilnya tidak disalin dari evidence
  Fase 3 (itu pada 20.000 ns).
- Evidence, satu file per revisi, lewat ekstraktor `/quartus-report`:
  `evidence/phase04/quartus_C3-P<n>.md`, ditambah rincian per entitas
  (`scripts/quartus/quartus_entity_breakdown.py`, diperluas untuk nama modul baru).
- Dicatat per revisi: ALM (dengan denominator fitter), register, M10K, DSP; Fmax untuk setiap slow
  corner yang dilaporkan Fmax Summary; slack setup terburuk dan slack hold terburuk per corner; jumlah pesan.
- Timing terpenuhi pada 40.000 ns (kondisi 4 ADR 0007) = slack setup terburuk ≥ 0 dan slack hold terburuk ≥ 0
  di setiap corner yang dilaporkan. Slack negatif dilaporkan sebagai "timing tidak terpenuhi", tidak pernah dilunakkan.
- ALM ≤ 10,478 (kondisi 3) memakai angka "Logic utilization (in ALMs)" fitter.
- Peringatan kritis didaftar dan ditriase secara tertulis; jenis peringatan baru relatif terhadap Fase 3
  dijelaskan sebelum hasil dipakai. Tidak ada false path, multicycle, atau pengecualian lain yang ditambahkan agar sebuah
  revisi lulus.
- Informasi saja, tanpa kompilasi tambahan: apakah Fmax tiap revisi juga akan memenuhi tujuan akhir 20.000 ns.
  goal.

## 6. Pemilihan (ADR 0007) - diterapkan hanya setelah keempat P diukur
Worksheet diisi dari file evidence (tidak ada sel yang diisi dari ingatan atau estimasi):

| P | bit-exact | siklus konstan | ALM | ≤ 10,478? | slack setup / hold terburuk @ 40.000 ns | timing terpenuhi? | cycles_NTT | cycles_INTT | Fmax per slow corner (MHz) | Fmax(P) = terendah | t_NTT (µs) | t_INTT (µs) | kandidat? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | | | | | | | | | | | | | |
| 2 | | | | | | | | | | | | | |
| 4 | | | | | | | | | | | | | |
| 6 | | | | | | | | | | | | | |

1. Himpunan kandidat C = nilai P yang keempat kondisinya berlaku: bit-exact PASS, siklus konstan
   PASS, ALM ≤ 10,478, timing terpenuhi pada 40.000 ns (setup dan hold, semua corner).
2. Fmax(P) = Fmax terendah di antara hasil slow-corner yang dilaporkan Fmax Summary Timing Analyzer untuk
   revisi itu (nilai slow-corner kasus terburuk), sebagaimana dicetak, dalam MHz.
3. t_NTT(P) = cycles_NTT(P) / Fmax(P) dan t_INTT(P) = cycles_INTT(P) / Fmax(P), dalam mikrodetik; keduanya
   dihitung dan dilaporkan untuk setiap P, kandidat atau bukan. t_INTT tidak menggerakkan pemilihan.
4. t_min = min atas P dalam C dari t_NTT(P);  d(P) = (t_NTT(P) − t_min) / t_min.
   P_selected = P terkecil dalam C dengan d(P) ≤ 0.05 (hampir seri: dalam 5% dari minimum global; P
   yang lebih kecil menang). Hasil bagi yang tidak dibulatkan dibandingkan.
5. Jika C kosong, tidak ada P yang dipilih otomatis: setiap hasil terukur dilaporkan dan tim diminta
   memutuskan.
6. Aturan diterapkan oleh skrip kecil yang membaca nilai worksheet (agar aritmetika dapat
   direproduksi), dan P terpilih dicatat di ADR baru (kriteria PASS Fase 4 ROADMAP), bukan dengan
   mengedit ADR 0007.

Harapan yang dinyatakan di muka agar tidak dapat dikira hasil nanti: P = 0 dan mungkin P = 2 tidak akan
menjadi kandidat (timing pada 40.000 ns); P = 4 dan P = 6 mungkin atau tidak, tergantung timing terukur
dan anggaran ALM, yang marginnya pada titik awal adalah 724 ALM.

## 7. Urutan kerja dan titik berhenti
1. Rencana ini disetujui tim.
2. Reducer staged + V2 (menyeluruh) - tidak ada yang dibangun di atasnya sampai V2 lulus.
3. Varian memori + V4; butterfly pipeline + V3.
4. Inti untuk P = 2, 4, 6 + V1, V5–V8, V10, V11.
5. Formal V9.
6. Quartus: keempat revisi; evidence diekstrak; peringatan kritis ditriase.
7. Worksheet diisi; aturan pemilihan diterapkan; hasil dilaporkan ke tim.
8. ADR baru untuk P terpilih (atau laporan "tanpa kandidat"); `docs/results/phase04.md`; baris C3 ROADMAP.
   Kotak Approval dibiarkan untuk manusia.

Berhenti dan laporkan alih-alih melanjutkan bila: V2 menemukan ketidakcocokan; kontrol negatif di V7 tidak
gagal; ketidaksepakatan simulator tidak dapat dijelaskan; atau perubahan pada file beku tampak perlu.

## 8. Secara eksplisit di luar lingkup Fase 4
Perubahan apa pun pada hasil metode reduksi atau pada q, n, nilai twiddle, atau besaran FIPS 203 lain;
Barrett / Montgomery / reduksi malas (Fase 5); pemetaan M10K; penggabungan layer; Keccak; mengubah L atau
jadwal lajur; nilai P selain {0, 2, 4, 6} sebagai kandidat terukur; berbagi pengali skala;
mengubah batasan clock setelah sapuan dimulai; pengecualian timing untuk membuat hasil hijau; klaim
percepatan terhadap perangkat lunak atau literatur apa pun; klaim validasi perangkat keras apa pun (tanpa papan terpasang).
