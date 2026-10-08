<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Test plan Fase 5 - aritmetika modular untuk q = 3329 (C4), ditulis sebelum RTL apa pun dikodekan (CRG-4)

- Tanggal (UTC): 2026-10-01. Branch `phase5-arith` (dari `main` pada 5a1eec0). Tidak ada RTL, testbench, atau proyek Quartus
  Fase 5 yang ada saat penulisan.
- Status: FINAL (2026-10-01). Keputusan D0–D8 Bagian 13 dijawab tim: D0 = ADR 0010, D1–D8 dan
  aturan pemilihan 5b = ADR 0011 (semua saran diterima); batas untuk pekerjaan timing berikutnya = ADR 0012. Butir bertanda
  *[D<n>]* di bawah mengikuti ADR itu. Posisi register di dalam setiap reducer baru ditambahkan sebagai amandemen (Bagian 14)
  sebelum revisi Quartus terkait dikompilasi.
- Keputusan yang mengatur: ADR 0009 (mulai dari C3-P6: L = 8, P = 6; anggaran desain inti NTT 12,573 ALM), ADR 0006
  (tujuan akhir 20.000 ns / 50 MHz "setelah Fase 5"; milestone Fase 4 40.000 ns), ADR 0007 (fungsi bit-exact; posisi register
  P = 6), ADR 0002 / C1 (matematika terkunci).
- Lingkup dari `docs/ROADMAP.md` Fase 5: 5a reduksi khusus q; 5b Montgomery lawan Barrett di balik antarmuka yang sama,
  keduanya diukur, pilihan lewat ADR; 5c (opsional) reduksi malas dengan batas terbukti; 5d (opsional) perkalian base-case gaya Karatsuba.
  Jadwal, memori, L, dan P tetap. Tidak boleh: perubahan q atau aritmetika FIPS 203, reduksi
  aproksimasi tanpa bukti, perubahan penjadwalan, Keccak.
- Model acuan: `tb/golden/primitives.py` (`ntt`, `intt`, `base_case_multiply`), rumus bilangan bulat (a·b) mod 3329.

## 1. Titik awal (MEASURED kecuali ditandai)
| Butir | Nilai | Evidence |
|---|---|---|
| C3-P6, seed bawaan | 10,505 ALM, 4,168 register, 29 M10K, 9 DSP; setup +10.753 ns @ 40 ns; Fmax 34.19 MHz (slow corner terendah) | `evidence/phase04/quartus_C3-P6.md` |
| C3-P6, seed 1–6 | 10,484–10,516 ALM; Fmax 32.60–34.20 MHz | `evidence/phase04/seed_sweep.md` |
| Siklus | NTT 119, INTT 375, 0 stall (simulation) | `evidence/phase04/cocotb_regression.txt` |
| Reducer di C3-P6 | 8 × `modmul_reduce_staged` (153.2–157.2 ALM, masing-masing 1 DSP) + 1 reducer skala (148.9 ALM, 1 DSP); jumlah 1,395.8 ALM (INFERENCE) | `baseline/c3p6_critical_path.md` |
| GHRD + C3-P6 (setelan GHRD) | 12,375 ALM gabungan; inti sendirian dengan setelan GHRD 11,053 | `evidence/phase04/ghrd_plus_c3p6_integration.md` |

Beku, tidak diedit di Fase 5: setiap file Fase 1–4 di bawah `rtl/`, `tb/`, `formal/`, `quartus/` dan semua evidence Fase
1–4 - khususnya `modmul_reduce.sv`, `modmul_reduce_staged.sv`, `butterfly*.sv`, `twiddle_rom.sv`,
`base_case_multiply.sv`, `poly_mem_multiport_pipe.sv`, `ntt_core_c3*.sv`.

## 2. Temuan baseline yang membentuk rencana ini (`baseline/c3p6_critical_path.md`)
- MEASURED: 300 jalur setup terburuk C3-P6 (Slow 100C) semuanya dimulai di register arbitrasi slot memori
  (potongan M). Jalur terburuk (slack 10.753 ns) adalah: dekode baca memori + mux baca ≈ 21.3 ns → butterfly `sub_mod(b, a)`
  ≈ 4.3 ns → pengali DSP ≈ 3.7 ns → potongan X. Tidak ada jalur internal reducer di antara 300.
- MEASURED slack per segmen reducer: X → D_5 +24.457 ns, D_5 → D_11 +23.592 ns, D_11 → memori +16.382 ns.
- INFERENCE: dengan memori, jadwal, L, dan P tetap, perubahan aritmetika Fase 5 tidak dapat mencapai 20.000 ns: bagian baca
  memori saja lebih panjang dari 20 ns. Aritmetika dapat memengaruhi sekitar 8 ns `sub_mod` + pengali pada segmen
  kritis, segmen D_11 → memori, dan ALM (paling banyak sekitar 1,395.8 ALM reducer hari ini bila reducer baru
  gratis). Ini dilaporkan ke tim sebagai keputusan D0 sebelum pekerjaan apa pun.

## 3. Sub-langkah, desain kandidat, dan batas 5a / 5b *[D4]*
Reducer saat ini bukan perkalian dengan q: ia 13 pengurangan bersyarat konstanta q·2^k
(k = 12..0) dari hasil kali 24-bit. Kata roadmap untuk 5a ("perkalian dengan konstanta q sebagai shift-and-add
di dalam metode reduksi saat ini") karenanya hanya berlaku sebagian. Tiga pembacaan (D4):

| Pembacaan | Apa yang dibangun 5a | Batas ke 5b |
|---|---|---|
| (i) | metode restoring yang sama dengan stage lebih sedikit, memakai batas operand a, b < q (hasil kali ≤ (q−1)² = 11,075,584 < 2^24) | 5b mengganti metodenya |
| (ii) (saran) | reducer fold khusus q: q = 2^11 + 2^10 + 2^8 + 1, jadi 2^12 ≡ 767 (mod q) dengan 767 = 2^10 − 2^8 − 1; x = x_h·2^12 + x_l dilipat menjadi 767·x_h + x_l hanya dengan shift dan add, diulang sampai nilai di bawah kelipatan kecil q, lalu sejumlah tetap pengurangan bersyarat | 5b = Barrett dan Montgomery, masing-masing memakai perkalian dengan invers aproksimasi; pada keduanya, perkalian dengan q ditulis sebagai shift-and-add (teknik 5a) |
| (iii) | hanya pengali skala INTT ×3303 sebagai pengali konstanta shift-and-add (3303 = 0b1100_1110_0111) | 5b mengganti reducer lajur |

Parameter kandidat (perhitungan tim, dikonfirmasi hanya oleh test menyeluruh V2):
- Barrett, k = 24, m = ⌊2^24 / q⌋ = 5039 (13 bit): t = ⌊x·m / 2^24⌋, r = x − t·q; untuk setiap x ≤ (q−1)²
  sisa memenuhi r < 2q (diperiksa atas semua x oleh skrip), jadi satu pengurangan bersyarat mengikuti. k lebih kecil
  (22 / 23) butuh 2–3 pengurangan.
- Montgomery, R = 2^12, q' = −q⁻¹ mod 2^12 = 3327: m = (x mod R)·q' mod R, t = (x + m·q) / R < 2q karena
  x ≤ (q−1)² < q·R = 13,635,584; satu pengurangan bersyarat. Keluaran = x·R⁻¹ mod q. Agar fungsi butterfly
  (a·b mod q) tidak berubah, operand yang selalu konstanta disimpan dalam bentuk Montgomery: twiddle
  ζ·R mod q di ROM baru yang dibangkitkan (`scripts/build/gen_twiddle_rom_mont.py` dari `tb/golden/primitives.py`;
  `twiddle_rom.sv` tetap beku) dan konstanta skala INTT 3303·R mod q. Setiap pengali di C3 punya satu operand
  dari tabel atau konstanta (`zeta_i` di butterfly, 3303 di pass skala - diperiksa di
  `rtl/ntt/butterfly_shared_pipe.sv` dan `rtl/ntt/ntt_core_c3.sv`), jadi tidak perlu konversi data polinomial.
- Apakah perkalian tambahan (x·m di Barrett, (x mod R)·q' di Montgomery) memakai DSP atau shift-and-add ALM adalah
  parameter desain; kedua varian dapat dibangun bila D2 mengizinkan DSP tambahan.

5c (opsional, [D3]) - reduksi malas. Satu-satunya titik malas yang cocok dengan memori tetap (word 12-bit, nilai < q
ditulis kembali) adalah di dalam butterfly. Kandidat konkret yang menyasar segmen kritis terukur: umpankan
`b + q − a` (13 bit, dalam [1, 2q)) ke pengali sebagai ganti `sub_mod(b, a)`, menghapus pengurangan bersyarat
(bagian dari ~4.3 ns) dari segmen M → X. Rentang masukan pengali menjadi [0, 2q) dan hasil kali melebihi
2^24 (maks 2q·(q−1) ≈ 22.2 M), jadi reducer harus dibuktikan untuk domain yang lebih lebar itu (Barrett dengan k lebih besar, atau
Montgomery dengan R = 2^13). Diizinkan hanya dengan bukti batas formal Bagian 8.

5d (opsional, [D3]) - base case gaya Karatsuba: c1 = (a0 + a1)(b0 + b1) − a0·b0 − a1·b1, c0 = a0·b0 + γ·(a1·b1),
4 perkalian modular sebagai ganti 5. Temuan: `base_case_multiply.sv` bukan bagian C3-P6: tidak ada inti yang menginstansiasinya
(ia hanya terdaftar sebagai file sumber di beberapa QSF Fase 1–4; inti C3 hanya melakukan NTT/INTT). C4d karenanya tidak dapat berupa perubahan kernel C3-P6;
ia unit mandiri yang dibandingkan dengan kompilasi mandiri `base_case_multiply.sv` yang beku *[D3]*.

## 4. Kontrak antarmuka dan domain operand (diperiksa di RTL)
- Pengali lajur: `a_i = zeta_i` dari `twiddle_rom` (semua 128 entri < q), `b_i = mul_in` = `b` (maju) atau
  `sub_mod(b, a)` (mundur). Pengali skala: word memori × 3303. Dengan koefisien polinomial < q, setiap
  operand pengali ada dalam [0, q).
- Koefisien ≥ q yang ditulis host berada di luar kontrak: `add_mod` / `sub_mod` sudah mengasumsikan masukan < q, jadi
  inti C3 tidak memberi hasil yang dispesifikasikan cocok FIPS 203 untuknya hari ini. Kontrak yang diusulkan *[D6]*: reducer baru harus sama dengan (a·b) mod q
  untuk semua a, b dalam [0, q); perilaku untuk operand 12-bit ≥ q diukur dan dilaporkan (V2-info) tetapi tidak
  disyaratkan. Reducer staged beku kebetulan eksak untuk semua 2^24 pasangan 12-bit; reducer baru mungkin tidak.
- Setiap reducer punya daftar port yang sama dengan `modmul_reduce_staged` (`clk_i`, `a_i`, `b_i`, `p_o`, parameter untuk posisi
  register) agar butterfly C4 dapat memilih reducer lewat parameter.

## 5. Latensi dan posisi register (P = 6 tetap)
- Di C3-P6 jalur pengali membawa 3 dari 6 register pipeline (`MUL_REG` = X, D_5, D_11; memori membawa
  A_4, A_11, M). Setiap reducer C4 yang dipakai di inti punya latensi tepat 3 agar P = 6, jadwal, dan
  jumlah siklus (NTT 119, INTT 375) tidak berubah.
- Aturan bawaan: satu register tepat setelah hasil kali (potongan X, tidak berubah) dan dua di dalam reducer baru, ditaruh untuk
  membagi logikanya kira-kira rata. Posisi persis per reducer ditulis ke amandemen rencana ini
  sebelum revisi Quartus terkait dikompilasi (aturan Fase 4 terhadap penyetelan setelah kejadian). Mengubah sebuah
  posisi setelah hasil Quartus terlihat membuat revisi bernama terpisah (misalnya `C4b-M2`); keduanya disimpan.
- Memindahkan register keluar dari jalur pengali (misalnya ke jalur baca memori atau sebelum pengali) mengubah
  posisi P = 6 yang ditetapkan rencana Fase 4 dan butuh keputusan tim *[D5]*.

## 6. Kasus sudut (CRG-4), didaftar sebelum test apa pun ditulis
Tingkat unit (setiap reducer):
- a = 0 atau b = 0; a = b = 1; a = 1, b = q−1; a = b = q−1 (hasil kali terbesar 11,075,584).
- Hasil kali tepat k·q dan k·q ± 1 untuk k = 1, 2, q−2, q−1 (setiap hasil kali yang dapat dicapai dekat kelipatan q).
- Hasil kali pada kasus batas Barrett / Montgomery yang ditemukan skrip: x dengan r terbesar sebelum pengurangan
  akhir, dan x tepat di bawah dan di atas setiap batas fold 2^12·j yang dipakai reducer fold.
- Semua 128 konstanta twiddle (dan bentuk Montgomery-nya) × {0, 1, q−1} dan konstanta skala × {0, 1, q−1}.
- Masukan beruntun setiap siklus (tanpa gelembung) dan satu masukan terisolasi, untuk memeriksa latensi tepat 3.
Tingkat inti: polinomial semua-nol; semua q−1; impuls di 0; impuls di 255; bergantian 0 / q−1; 100 acak per arah;
50 round trip `intt(ntt(f)) == f`; data bahaya terarah-batas Fase 4.
5c: masukan ekstrem rentang malas (b + q − a dengan a = 0, b = q−1 → 2q−1; a = q−1, b = 0 → 1) dengan setiap
twiddle; 5d: (a0, a1, b0, b1) ∈ {0, 1, q−1}^4 dengan setiap γ.

## 7. Verifikasi per sub-langkah (setiap butir di Icarus dan Verilator kecuali dinyatakan lain)
V1 Lint / elaborasi (CRG-1, CRG-2). `verilator --lint-only -Wall` dan `slang`, 0 peringatan, setiap file baru dan
pembungkus; `default_nettype none` di atas dan `wire` dipulihkan di akhir; tidak ada baris komentar yang diawali kata
"synthesis"; tidak ada variabel `automatic` di blok prosedural (Icarus).

V2 Test reducer menyeluruh (syarat roadmap). Harness C++ Verilator mengikuti `tb/ntt/p4_reducer/`:
setiap (a, b) dalam [0, q)², 11,082,241 pasangan, pada konfigurasi register yang benar-benar dipakai, membandingkan keluaran (setelah
latensinya) dengan (a·b) mod 3329 dan dengan `modmul_reduce_staged` yang beku. Untuk Montgomery harness menggerakkan
b dalam bentuk Montgomery (b·R mod q, bijeksi pada [0, q)) sehingga pembandingan tetap terhadap (a·b) mod q untuk setiap
pasangan. 0 ketidakcocokan disyaratkan. V2-info [D6]: hal sama atas semua 2^24 pasangan 12-bit, hasil hanya dilaporkan.

V3 Unit test cocotb. Sudut Bagian 6 ditambah 10,000 pasangan acak yang dialirkan beruntun; latensi diperiksa.

V4 Butterfly (varian C4). Sudut V3 Fase 4 dan 1,000 (a, b, ζ) acak per mode terhadap langkah butterfly
golden, beruntun, pada latensi yang diharapkan.

V5 Inti bit-exact (CRG-3). Daftar inti Bagian 6 terhadap `tb/golden/primitives.py`; scoreboard bahaya Fase 4
dan pemeriksaan `bank_overflow_o` berjalan selama setiap test inti (harus tetap 0 / 0).

V6 Siklus konstan (CRG-7). Siklus start-ke-done identik untuk setiap masukan dan di kedua simulator, dan sama dengan
119 / 375 milik C3-P6; nilai lain berarti P atau jadwal berubah dan merupakan kegagalan lingkup fase ini.

V7 Tabel yang dibangkitkan. Bila ROM atau konstanta Montgomery dipakai: skrip pembangkit menghitung ulang setiap entri dari
`tb/golden/primitives.py`; sebuah test memeriksa setiap ζ_M[i] · R⁻¹ ≡ ζ[i] (mod q) terhadap nilai ROM beku.

V8 Formal (CRG-8). Tidak ada logika kendali baru yang direncanakan; alur formal Fase 4 dijalankan ulang pada inti C4 untuk menunjukkan
properti kendali tetap berlaku (pola `formal/run/run_formal_phase4.py`, top baru). 5c menambah Bagian 8.

V9 Regresi (CRG-5, CRG-6). pytest Fase 0, regresi cocotb dan formal Fase 1–4, `check_params.py`.

V10 Kontrol negatif. Satu konstanta reducer yang sengaja salah (misalnya m − 1 untuk Barrett, q' salah untuk
Montgomery) pada build khusus test harus membuat V2 gagal; entri ROM yang salah harus membuat V7 dan V5 gagal. Bila tidak, test
batal.

Sebuah sub-langkah benar hanya bila V1–V7, V9, V10 lulus (dan Bagian 8 untuk 5c) di kedua simulator.

## 8. Rencana formal untuk 5c (reduksi malas) - disyaratkan sebelum desain malas apa pun dipakai
- SymbiYosys dengan frontend yosys-slang (tanpa `bind`, port vektor packed), pada pembungkus kombinasional datapath lajur:
  asumsikan a, b < q dan ζ < q; buktikan (mode `prove`) bahwa (1) masukan pengali < 2q, (2) hasil kali
  muat dalam lebar masukan reducer, (3) keluaran reducer dan setiap nilai yang ditulis ke memori < q, (4) tidak ada sinyal
  antara yang meluap dari lebar yang dideklarasikan.
- Kesamaan dengan hasil eksak: masukan pengali malas u = b + q − a ≡ b − a (mod q) berada dalam [1, 2q), jadi
  reducer yang diperluas diuji menyeluruh untuk setiap ζ dalam [0, q) dan u dalam [0, 2q) (3,329 × 6,658 = 22,164,482 pasangan,
  harness V2 dengan masukan lebih lebar) terhadap (ζ·u) mod q, dan butterfly terhadap langkah golden (V4). Tanpa
  reduksi aproksimasi.
- Kontrol negatif: bukti yang sama dengan batas dilemahkan di RTL (misalnya satu bit lebih sempit) harus gagal.

## 9. Quartus (CRG-9)
- Proyek baru `quartus/phase05_arith_c4/`; revisi `C4a`, `C4b-B` (Barrett), `C4b-M` (Montgomery), `C4c`, dan untuk
  5d `C4d` + `BCM-ref` (`base_case_multiply.sv` beku, mandiri) *[D3]*. Device, virtual pin, dan assignment QSF yang sama
  dengan `C3-P6.qsf`; hanya top entity, folder keluaran, dan daftar RTL yang berbeda.
- Batasan *[D1]*: saran - `create_clock -period 40.000` untuk setiap revisi C4 (sebanding dengan C3-P6), ditambah
  satu kompilasi tambahan konfigurasi C4 akhir dan C3-P6 pada 20.000 ns, dilaporkan sebagai informasi.
- Setelan *[D2]*: saran - bawaan Quartus seperti di Fase 4; opsional satu kompilasi setelan-GHRD untuk C4 akhir
  (bandingkan dengan C3-P6-ghrdset 11,053 ALM).
- Seed *[D7]*: saran - seed bawaan untuk setiap revisi; seed 1–6 untuk dua kandidat 5b (12 kompilasi) agar
  pilihan 5b tidak bertumpu pada satu seed; seed 1–6 C3-P6 sudah ada.
- Satu kompilasi sekali, di latar belakang; laporan diekstrak dengan skill `/quartus-report`; ALM per entitas
  setiap reducer dan laporan kelas jalur teratas (`scripts/quartus/phase5_top_paths.tcl` pada salinan proyek,
  `scripts/quartus/phase5_path_classes.py`) untuk setiap revisi, agar perubahan jalur kritis terlihat.

## 10. Kriteria sukses per sub-langkah (PASS roadmap: "setiap sub-langkah yang dicoba benar dan terukur")
| Sub-langkah | Disyaratkan (PASS) | Dilaporkan (bukan syarat lulus) |
|---|---|---|
| 5a | benar (Bagian 7); revisi `C4a` dikompilasi; siklus NTT/INTT 119/375; timing pada batasan D1 terpenuhi atau kegagalan didokumentasikan | Δ ALM, Δ register, Δ DSP, Δ Fmax, dan Δ slack lawan C3-P6 (batasan, setelan, seed sama); ALM reducer per entitas; kelas jalur |
| 5b | kedua kandidat benar dan dikompilasi; aturan pemilihan (ADR, ditulis sebelum mengompilasi) diterapkan; ADR dicatat | selisih sama untuk kedua kandidat (dan per seed bila D7) |
| 5c | bukti batas formal PASS dengan kontrol negatif; benar; `C4c` dikompilasi - atau "tidak dicoba" | perubahan slack segmen M → X |
| 5d | benar (menyeluruh atau terbatas menurut D3); `C4d` dan `BCM-ref` dikompilasi - atau "tidak dicoba" | DSP dan ALM lawan `BCM-ref` |
Revisi mana pun di atas 12,573 ALM atau tidak memenuhi batasan D1 dilaporkan demikian; ia tidak disembunyikan dan tidak
"diperbaiki" dengan waiver, false path, atau pemeriksaan yang dilemahkan.

## 11. Aturan pemilihan 5b - usulan, diterima sebagai ADR sebelum kompilasi 5b apa pun *[D8]*
Langkah 1. Bangun, verifikasi, dan kompilasi kedua kandidat (dan seed menurut D7) sebelum menerapkan aturan.
Langkah 2 - kondisi kandidat (semua harus berlaku): benar (Bagian 7); siklus tepat 119 / 375; ALM ≤ 12,573
("ALMs needed" fitter); timing terpenuhi pada batasan D1 (setup dan hold non-negatif di setiap corner yang dilaporkan).
Langkah 3 - metrik. Fmax(c) = Fmax slow corner terendah (median atas seed bila D7 memberi beberapa). Siklus sama
menurut kondisi, jadi waktu per NTT sebanding dengan 1/Fmax.
Langkah 4 - pemilihan. Fmax tertinggi menang, kecuali kandidat lain dalam 5% darinya (hampir seri); pada
hampir seri kandidat dengan ALM lebih sedikit menang; bila ALM keduanya juga berbeda kurang dari sebaran seed terukur C3-P6
(32 ALM), tim memutuskan (pemutus seri yang disarankan: Barrett, karena tidak butuh tabel bentuk-Montgomery).
Langkah 5. Bila tidak ada kandidat yang memenuhi syarat, tidak ada yang dipilih otomatis; hasil dilaporkan dan tim memutuskan.
Harapan yang dinyatakan di muka (INFERENCE dari Bagian 2): Fmax kemungkinan seri karena jalur kritis berada di
jalur baca memori; aturan lalu menyusut menjadi ALM.

## 12. Tata letak evidence
`evidence/phase05/`: `test_plan.md` (file ini), `baseline/` (analisis jalur kritis), `5a/` … `5d/`
(log test menyeluruh, log cocotb, log formal, file evidence Quartus, laporan kelas jalur, worksheet),
`docs/results/phase05.md` (satu bagian per sub-langkah; kotak Approval dibiarkan kosong), ADR untuk 5b, baris C4 (satu sub-baris
per sub-langkah) di matriks ablasi `docs/ROADMAP.md`, `docs/reports/CHIPATON_Phase5_Report.pdf` (Bahasa
Indonesia, dibangkitkan oleh skrip yang meniru `scripts/build/build_phase4_report.py`), `HANDOFF.md` baru.

## 13. Keputusan tim (dijawab 2026-10-01, Faza Dzil, Team J5)
| # | Pertanyaan | Keputusan |
|---|---|---|
| D0 | Tujuan Fase 5 mengingat Bagian 2 | ADR 0010: 50 MHz dipertahankan sebagai target proyek upaya-terbaik, bukan gerbang Fase 5; ekspektasi ADR 0006 dikoreksi; pekerjaan memori / P / jadwal di fase atau sub-fase terpisah setelah 5a/5b (nama dan posisi terbuka, PENDING #19) |
| D1 | Batasan untuk revisi C4 | ADR 0011: 40.000 ns untuk setiap revisi C4; C4 akhir dan C3-P6 juga dikompilasi pada 20.000 ns (informasi) |
| D2 | Anggaran, setelan, DSP | ADR 0011: 12,573 ALM tidak berubah; bawaan Quartus; DSP dilaporkan, tanpa batas DSP |
| D3 | 5c dan 5d | ADR 0011: diputuskan setelah hasil 5a / 5b; rencana disimpan |
| D4 | Pembacaan 5a | ADR 0011: pembacaan (ii), batas ke 5b seperti Bagian 3 |
| D5 | Posisi register di dalam P = 6 | ADR 0011: tidak ada perpindahan antara memori dan jalur pengali di Fase 5; jalur pengali menjaga tepat 3 register |
| D6 | Kontrak operand | ADR 0011: eksak untuk a, b dalam [0, q); operand ≥ q dilaporkan, tidak disyaratkan |
| D7 | Seed | ADR 0011: seed bawaan untuk semua; seed 1–6 untuk dua kandidat 5b |
| D8 | Aturan pemilihan 5b | ADR 0011 (aturan Bagian 11, dibuat tepat di sana: kualifikasi per seed, median Fmax dan median ALM) |

Pekerjaan timing berikutnya (di luar Fase 5): ADR 0012 - lebih banyak siklus hanya bila t_NTT dan t_INTT pada Fmax terukur mengalahkan
C3-P6 dan siklus-konstan berlaku; inti NTT ≤ 12,573 ALM tetap menjadi batas.

## 14. Amandemen (posisi register dan detail desain ditetapkan sebelum tiap kompilasi)

A1 - 5a, revisi C4a (2026-10-01, sebelum kompilasi C4a apa pun).
- Reducer `rtl/arith/modmul_fold.sv`: stage F_1..F_5 (fold v → 767·(v >> 12) + (v mod 2^12), lebar 22, 20, 17,
  15, 14 bit) dan S (satu pilihan di antara v, v − q, v − 2q, kedua pengurangan paralel). Batas atas untuk setiap
  masukan 24-bit (perhitungan tim, lalu dikonfirmasi oleh V2 atas semua 2^24 pasangan 12-bit): 3,144,960 → 592,384 → 114,543
  → 24,804 → 8,697 < 3q.
- Posisi register (jalur pengali, 3 register, ADR 0011 D5): X, F_3, F_5 (`REG_AFTER` bit 0, 3, 5 = 41).
  Segmen: hasil kali → X; F_1–F_3 → reg; F_4–F_5 → reg; S + butterfly `add_mod`/`sub_mod` + tulis memori.
  Alasan: segmen C3-P6 D_11 → memori (2 stage reduksi + butterfly + tulis) adalah yang terpanjang kedua (≈ 23.6 ns,
  `baseline/c3p6_critical_path.md`); menaruh hanya satu stage pilihan di sana memendekkannya; dua
  segmen pertama memuat tiga dan dua stage fold. Potongan memori tidak berubah (A_4, A_11, M).
- Pembungkus `rtl/ntt/ntt_core_c4a.sv` (top revisi C4a); inti `rtl/ntt/ntt_core_c4.sv` = `ntt_core_c3.sv` dengan
  instans reducer / butterfly diganti lewat `rtl/arith/modmul_sel.sv` dan `rtl/arith/butterfly_c4.sv` (diff
  terbatas pada baris-baris itu).
- Quartus: proyek `quartus/phase05_arith_c4/`, revisi `C4a`; QSF = `C3-P6.qsf` dengan hanya top entity, folder
  keluaran, dan daftar RTL yang berubah; SDC = `C3.sdc` (40.000 ns) disalin tanpa perubahan; seed dan setelan bawaan.

A2 - kontrol negatif inti (2026-10-01, setelah run inti pertama, sebelum hasil Quartus apa pun).
- V5/V7 memakai ulang test inti Fase 4 `tb/ntt/test_ntt_core_c3.py` tanpa perubahan (runner `tb/arith/run_c4_core_tests.py`).
- Kontrol negatif C4 pertama (reducer fold, RdLat 1 + WrDly 7, P = 8) bukan kontrol negatif yang valid: scoreboard
  memicu, tetapi 0 dari 5 hasil NTT salah di kedua simulator
  (`5a/negctl_first_attempt_rd1_wr7.txt`). Alasan (INFERENCE): memori melakukan baca RdLat siklus setelah
  permintaan, jadi bahaya baca-setelah-tulis fisik bergantung pada WrDly (register setelah baca),
  bukan pada P; WrDly 7 berada dalam slack jadwal 7. Pemeriksaan scoreboard (a) menandai pada saat permintaan dan karenanya
  konservatif.
- Kontrol negatif kini RED_KIND 0 dengan RdLat 0 + WrDly 8 (reducer fold hanya punya 7 batas stage),
  yaitu kontrol negatif Fase 4 lewat inti C4; ia harus memicu scoreboard dan memberi 5/5 hasil salah.
- Konsekuensi di luar Fase 5 (dilaporkan ke tim; tidak ada yang diubah di Fase 5): tabel stall
  `baseline/decision_package.md` (a) mengasumsikan bahaya bergantung pada P dan karenanya konservatif;
  register yang ditambahkan sebelum baca (RdLat) tidak akan butuh stall menurut evidence ini. Fase memori / P berikutnya
  harus mengonfirmasi ini dalam simulasi dan butuh scoreboard yang memodelkan baca pada request + RdLat (file test baru; test
  Fase 4 tetap beku).

A3 - kandidat 5b, revisi C4b-B dan C4b-M (2026-10-01, sebelum kompilasi 5b apa pun).
- Barrett `rtl/arith/modmul_barrett.sv` (RED_KIND 2): stage S_1 estimasi hasil bagi t = (x·5039) >> 24 (hasil kali
  x·M diserahkan ke alat), S_2 sisa r = x − t·q (t·q shift-and-add), S_3 pilih r atau r − q. r < 2q untuk setiap
  x 24-bit (r terbesar = 5,713, perhitungan tim atas semua 2^24 nilai; dikonfirmasi oleh V2).
- Montgomery `rtl/arith/modmul_montgomery.sv` (RED_KIND 3, R = 2^12): S_1 m = −769·(x mod 2^12) mod 2^12 (q' = 3327 ≡
  −769, shift-and-add), S_2 t = (x + m·q) >> 12 (m·q shift-and-add), S_3 pilih. t < 2q karena x ≤ (q−1)² < q·R.
  Operand konstanta dalam bentuk Montgomery: `rtl/arith/twiddle_rom_mont.sv` dibangkitkan oleh
  `scripts/build/gen_twiddle_rom_mont.py` dari `tb/golden/primitives.py`; konstanta skala INTT 3303·2^12 mod q = 32
  (dihitung saat elaborasi di `ntt_core_c4.sv`). V7 = `tb/arith/check_mont_rom.py`.
- Posisi register untuk keduanya (3 register, ADR 0011 D5): X, S_1, S_2 (`REG_AFTER` bit 0, 1, 2 = 7). Segmen:
  hasil kali → X; S_1 → reg; S_2 → reg; S_3 + butterfly `add_mod`/`sub_mod` + tulis memori. Aturan penempatan sama dengan A1
  (satu stage pilihan sebelum jalur tulis). Potongan memori tidak berubah.
- V2/V3 untuk Montgomery menggerakkan operand kedua dalam bentuk Montgomery lewat pembungkus khusus simulasi
  (`tb/arith/c4_tb_wrappers.sv`), jadi hasil tetap dibandingkan terhadap (a·b) mod q untuk setiap pasangan; test butterfly
  mengonversi ζ dengan cara sama.
- Pembungkus `rtl/ntt/ntt_core_c4b_b.sv`, `rtl/ntt/ntt_core_c4b_m.sv`; revisi Quartus `C4b-B`, `C4b-M` dan salinan seed-nya
  `C4b-B-s2..s6`, `C4b-M-s2..s6` (hanya `SEED` dan folder keluaran yang berbeda), semuanya pada 40.000 ns, bawaan Quartus.

A4 - reduksi malas 5c, revisi C4c (2026-10-01, ADR 0014, sebelum RTL atau kompilasi 5c apa pun).
- Desain: `rtl/arith/lazy_bfly_io.sv` (logika masukan / keluaran kombinasional butterfly INTT malas: u = b + q − a,
  s = a + b, keluaran a' = s ≥ q ? s − q : s, b' = t; mode NTT seperti sebelumnya), `rtl/arith/modmul_barrett_lazy.sv` (Barrett dengan
  operand kedua 13-bit, hasil kali 25-bit, konstanta M = 5039 dan stage S_1..S_3 yang sama; r < 2q untuk setiap hasil kali sampai
  (q−1)·(2q−1) = 22,154,496, perhitungan tim atas semua nilai), `rtl/arith/butterfly_c4_lazy.sv` (logika I/O + reducer + delay
  samping 13-bit), parameter `LAZY` `rtl/ntt/ntt_core_c4.sv` (bawaan 0 = tidak berubah), pembungkus `rtl/ntt/ntt_core_c4c.sv`
  (RED_KIND 2 untuk pengali skala, LAZY 1). Posisi register seperti C4b-B: X, S_1, S_2; potongan memori A_4, A_11, M.
- Test (kedua simulator bila berlaku):
  - V2-lazy: `modmul_barrett_lazy` menyeluruh atas z dalam [0, q) dan u dalam [0, 2q) (22,164,482 pasangan) terhadap (z·u) mod q
    pada REG_AFTER 0 dan 7; info: semua z 12-bit × u 13-bit; kontrol negatif (t·(q−1)) harus gagal;
  - V2 (domain D6) juga untuk `modmul_barrett_lazy` dibatasi pada u < q, sebagai regresi 5b;
  - V4: test butterfly Fase 4 (`tb/ntt/test_butterfly_pipe.py`) tidak berubah pada `butterfly_c4_lazy`, ditambah sudut INTT
    a = 0, b = q−1 (u = 2q−1); a = q−1, b = 0 (u = 1); a = b = q−1 (s = 2q−2) dengan setiap twiddle;
  - V5–V7: test inti tidak berubah pada `ntt_core_c4c` (bit-exact, scoreboard, siklus tepat 119 / 375) dan C4a / C4b-B /
    C4b-M / RED_KIND 0 lagi setelah perubahan inti; kontrol negatif seperti sebelumnya;
  - V8-lazy (formal, §8): `lazy_bfly_io` dengan asumsi a, b, t < q, buktikan u < 2q, s < 2q, (u ≥ q ? u − q : u) =
    sub_mod(b, a), a' < q, b' < q, a' = add_mod(a, b) di INTT; keluaran NTT = add_mod / sub_mod dari (a, t); kontrol
    negatif: salinan yang keluarannya tidak mereduksi s harus gagal. Reducer sendiri dicakup V2-lazy (menyeluruh), bukan
    oleh bukti formal (dinyatakan sebagai lingkup bukti);
  - V8 (kontrol), V9 (regresi) seperti sebelumnya.
- Quartus: `C4c`, `C4c-s2..s6`; adopsi menurut aturan ADR 0014 §4, diterapkan oleh skrip dari file evidence.
