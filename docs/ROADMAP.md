# Roadmap: akselerator ML-KEM-768 di DE10-Nano

## Status saat ini

Diperbarui hanya dari bukti yang sudah diverifikasi. Rincian ada di `docs/results/phaseNN.md`.

| Fase | Isi | Status | Hasil utama (MEASURED, kernel-only) |
|---|---|---|---|
| 0 | Model acuan FIPS 203 | DONE | model cocok dengan vektor ACVP; `evidence/phase00/` |
| 1 | NTT satu lajur (C0) | DONE | 7.010 ALM, Fmax 14,64 MHz, slack setup −48,323 ns pada 20 ns (timing tidak terpenuhi, didokumentasikan); `evidence/phase01/` |
| 2 | Banking memori (C1) | DONE | peta bank bebas konflik untuk L = 1, 2, 4, 8; 6.749 ALM, slack −46,720 ns; M10K tidak tercapai (pembacaan asinkron); `evidence/phase02/` |
| 3 | Multi-lane (C2) | DONE | L = 8 pada C2-K2-K1 (ADR 0005): 9.754 ALM, NTT 113 / INTT 369 siklus; `evidence/phase03/` |
| 4 – 8 | Pipeline, aritmetika, memori, K-PKE, Keccak | DONE | lihat file hasil dan matriks ablasi di bawah |
| 9 | Inti ML-KEM-768 penuh (simulasi) | DONE | ACVP 100 % di dua simulator; `docs/results/phase09.md` |
| 9M | Optimasi inti | PARTIAL | K4: 8.416 / 9.611 / 12.989 siklus; tiga bukti formal habis waktu; `docs/results/phase9m.md` |
| 10 – 12 | HPS, benchmark, fitur keamanan | belum dimulai | Fase 10 terblokir: belum ada papan (PENDING #8) |

Fase 1 sampai 3 awalnya disetujui sebagai baseline dengan timing tidak terpenuhi. Pada 2026-10-05 tim menetapkannya DONE
karena tujuannya dipenuhi oleh fase-fase akhir. Angka ukur tidak berubah.

Detail Fase 3: L = 1, 2, 4, 8 menghasilkan 6.018 / 5.728 / 7.629 / 11.446 ALM dan NTT/INTT 897/1153, 449/705, 225/481, 113/369 siklus
(L = 8 melewati anggaran ADR 0004). Aturan ADR 0004 memberi L = 4 pada C2 biasa. Eksperimen tambahan K2 (lebar counter) dan K1 (satu pengali
bersama per butterfly) menghasilkan C2-K2-K1 dengan 5.566 / 5.374 / 6.775 / 9.754 ALM dan siklus yang sama. Titik operasi terpilih:
C2-K2-K1 pada L = 8 (ADR 0005, Accepted, Faza Dzil, 2026-09-30). Formal (k-induction) lolos untuk L = 1, 2, 4, 8 pada properti
`bank_overflow_o == 0`, handshake busy/done dan rentang counter (bukan bit-exactness). Hasil UNKNOWN awal untuk L = 2, 4, 8 adalah artefak harness
formal, diperbaiki di harness saja dengan kontrol negatif (`evidence/phase03/formal_rerun.md`).

Lingkungan: Quartus 25.1std terverifikasi dengan kompilasi smoke. Belum ada DE10-Nano yang terpasang (`jtagconfig` kosong, 2026-09-24).
Jadwal lomba belum diketahui.

> Bila `docs/results/phase00.md` hilang, gagal `check_result.py`, atau kotak Approval-nya kosong, status Fase 0 di atas salah:
> berhenti, laporkan, dan jangan mulai Fase 1.

## Cara roadmap ini bekerja

- Gerbang ketat. Fase berjalan berurutan. Fase baru dimulai setelah file hasil fase sebelumnya lolos `check_result.py`
  dan anggota tim mencentang kotak Approval-nya. Skill: `/phase-gate`.
- Baseline yang benar dulu. Tidak ada fase optimasi yang dimulai sebelum konfigurasi yang diubahnya bit-exact terhadap
  model acuan dan sudah diukur.
- Satu perubahan besar sekali waktu. Fase dengan langkah bagian (5, 6, 8) mengukur dan mencatat tiap langkah sendiri;
  manusia meninjau tiap titik henti sebelum langkah berikutnya. Jangan menggabung dua optimasi dalam satu pengukuran.
- Tidak ada angka karangan. Setiap angka sumber daya, timing, atau kinerja berstatus `MEASURED` (laporan Quartus atau log
  simulasi/papan di repository ini, dengan path-nya) atau berlabel `ESTIMATE` beserta metode dan asumsinya. Angka dari literatur hanya konteks.
- Gerbang gagal = berhenti. Jangan lanjut setelah gerbang gagal. Tulis file hasil dengan Status `NOT DONE` atau `PARTIAL`,
  catat kegagalan dan path lognya, lalu tanyakan ke tim. Jangan melemahkan test, toleransi, assertion, atau batasan timing agar lolos.
- Setiap fase berakhir dengan file hasil `docs/results/phase<NN>.md` (templat `docs/results/TEMPLATE.md`), divalidasi oleh
  `python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/phase<NN>.md`.
- Bukti fase N ada di `evidence/phaseNN/` (Fase 5M di `evidence/phase05m/`, Fase 9M di `evidence/phase9m/`).

## Persyaratan FIPS 203 yang dikunci (berlaku untuk semua fase, tidak pernah diubah)

Matematika dikunci; hanya arsitektur perangkat keras yang berubah (ADR 0002, `/mlkem-guard`).

| Persyaratan | Nilai / aturan | Sumber |
|---|---|---|
| Ring | R_q = Z_q[X]/(X^256 + 1), q = 3329, n = 256 | FIPS 203; `/mlkem-guard` |
| Parameter ML-KEM-768 | k = 3, η1 = 2, η2 = 2, du = 10, dv = 4 | FIPS 203 Tabel 2 (dikonfirmasi di Fase 0) |
| Ukuran | ek 1184 B, dk 2400 B, ct 1088 B, shared key 32 B | FIPS 203; vektor NIST ACVP |
| NTT | ζ = 17; NTT incomplete: 7 layer (panjang blok 128 → 2), 128 butterfly per layer | FIPS 203 Alg. 9/10 |
| Perkalian titik | 128 perkalian base-case polinomial derajat 1 modulo (X² − ζ^(2·BitRev7(i)+1)), bukan perkalian skalar | FIPS 203 Alg. 11/12 |
| Hash / XOF | SHA3-256, SHA3-512, SHAKE128, SHAKE256 di atas Keccak-f[1600] | FIPS 203; FIPS 202 |
| Compress / Decompress, encode | persis seperti di FIPS 203; tanpa pembagian pada data rahasia | FIPS 203 |
| Pemeriksaan masukan dan implicit rejection | pemeriksaan kunci enkapsulasi dan dekapsulasi; Decaps mengenkripsi ulang, membandingkan dalam waktu konstan, dan memilih K atau kunci implicit-rejection | FIPS 203 |
| Acuan kebenaran | model acuan Python di `tb/golden/` (Fase 0), konstanta terkunci diperiksa oleh `check_params.py` | Fase 0 |

## Definisi umum

### Metrik yang dicatat (per konfigurasi)

| Metrik | Definisi | Sumber |
|---|---|---|
| ALM | Pemakaian logika dalam ALM | Fitter summary |
| Register | Total register | Fitter summary |
| M10K | Total blok RAM | Fitter summary |
| DSP | Total blok DSP | Fitter summary |
| Utilisasi | Terpakai / tersedia, dengan penyebut yang dicetak fitter | Fitter summary |
| Fmax | Per clock, dari "Fmax Summary" Timing Analyzer (model slow) | Laporan STA |
| Slack | Slack setup dan hold terburuk, semua corner, pada clock yang dibatasi | STA summary |
| Siklus/op | Siklus clock per operasi dari counter siklus (simulasi dulu, papan kemudian) | Log test |
| Siklus stall | Siklus hilang karena konflik bank atau hazard pipeline | Log test |
| Latensi | siklus ÷ f_clk, dengan f_clk adalah clock terbatas yang memenuhi timing (bukan Fmax); sebutkan clock bersama tiap latensi | Turunan dari nilai MEASURED |
| Area-time (AT) | ALM × latensi (DSP dan M10K dilaporkan di sampingnya; tidak dilebur ke AT) | Turunan dari nilai MEASURED |

Kapasitas acuan device 5CSEBA6U23I7 seperti dicetak fitter pada kompilasi smoke tim (MEASURED): 41.910 ALM, 553 blok RAM
(5.662.720 bit memori blok) dan 112 blok DSP. Selalu kutip penyebut dari laporan fitter yang sedang dipakai.

Siklus/op punya dua cakupan. Cakupan kernel: siklus per NTT, per INTT, per perkalian titik (satu polinomial), per permutasi Keccak-f.
Cakupan operasi: siklus per KeyGen, Encaps, Decaps. Bandingkan konfigurasi hanya dalam cakupan yang sama.

### Protokol pengukuran (setiap pengukuran Quartus)

- Versi Quartus sama (25.1std kecuali ADR mengubahnya), device sama, metode batasan timing sama, seed fitter dicatat. Satu revisi Quartus
  per konfigurasi; nama revisi = ID konfigurasi dari matriks ablasi.
- Kompilasi kernel-only memakai virtual pin agar I/O tidak mengganggu area atau timing.
- Clock target: keputusan tim yang dicatat sebagai ADR (ADR 0006). Sebelum itu, batasi dengan periode sementara yang terdokumentasi dan laporkan Fmax.
  Jangan menyebut latensi tanpa clock-nya.
- Ekstrak bukti dengan skill `/quartus-report`, tulis ke folder fase:
  `extract_quartus_report.py <output_files> <revisi> --log <compile.log> --out evidence/phaseNN/quartus_<revisi>.md --note "<git sha, parameter, clock>"`.
  File `.rpt` mentah dan `output_files/` tidak di-commit.
- Critical warning dibahas tertulis di file hasil.

### Common RTL gate (CRG): wajib di setiap fase RTL

| ID | Pemeriksaan | Alat |
|---|---|---|
| CRG-1 | Lint bersih | `verilator --lint-only -Wall` |
| CRG-2 | Elaborasi bersih | `slang` |
| CRG-3 | Bit-exact terhadap model acuan, di kedua simulator | cocotb di Verilator dan Icarus |
| CRG-4 | Kasus sudut ditulis di test plan sebelum test dibuat (nol, semua koefisien q−1, impuls, nilai maksimum, panjang batas) | Test plan di folder evidence fase |
| CRG-5 | Regresi: semua test fase sebelumnya tetap lolos | pytest / cocotb |
| CRG-6 | Parameter terkunci | `check_params.py` |
| CRG-7 | Bukti siklus konstan bila berlaku: jumlah siklus sama untuk masukan rahasia berbeda dengan masukan publik sama | Log hitungan siklus |
| CRG-8 | Properti formal untuk logika kendali/alamat baru (FSM mencapai done, tidak ada alamat di luar rentang, dan properti khusus fase) | SymbiYosys |
| CRG-9 | Bukti Quartus bila fase memerlukannya; tidak ada slack terburuk negatif pada clock terbatas, atau kegagalannya didokumentasikan | `/quartus-report` |
| CRG-10 | File hasil tervalidasi; teks untuk juri lolos pemeriksa klaim | `check_result.py`; `claim_lint.py` |

## Catatan penomoran ulang (2026-09-29)

Revisi ini menggantikan daftar fase 0-6 sebelumnya. Lama → baru: lama 1 (NTT) → baru 1-6; lama 2 (Keccak) → baru 7-8;
lama 3 (integrasi) → baru 9-10; lama 4 (demonstrasi protokol) → baru 10 (fungsional) dan 11 (terukur); lama 5 (pengukuran) → baru 11;
lama 6 (lanjutan) → baru 12. File lain yang masih memakai nomor lama harus diperbarui terpisah.

---

## Fase 0: Model acuan / FIPS 203 (SELESAI, terverifikasi, disetujui tim)

1. Tujuan. Acuan Python yang mandiri dan tepercaya untuk ML-KEM-768, pembanding semua gerbang berikutnya.
2. Lingkup implementasi (selesai). `tb/golden/`: konstanta terkunci (`params.py`), primitif (NTT, INTT, perkalian titik, sampling, encode,
   compress), K-PKE dan ML-KEM tingkat atas; errata FIPS 203 ditinjau.
3. Test / verifikasi (selesai). Property test; vektor NIST ACVP ML-KEM-768 (commit dan sha256 terpatok di
   `.claude/skills/mlkem-guard/reference/kat_sources.md`; set sampel NIST, 25 kasus per grup); uji silang acak terhadap kyber-py di virtualenv sementara.
4. Quartus. Tidak berlaku.
5. Kriteria PASS (terpenuhi). `check_params.py` lolos dan k/η/du/dv dikonfirmasi terhadap FIPS 203; model acuan mereproduksi vektor terpatok;
   errata dicatat (bukti + ADR); log uji silang ada; `phase00.md` tervalidasi dan disetujui.
6. Tidak boleh mulai sekarang. Mengubah model acuan tanpa ADR dan ulang penuh Fase 0; memakai vektor CRYSTALS-Kyber lama;
   menganggap vektor sampel sebagai cakupan menyeluruh.
7. Artefak evidence. `evidence/phase00/`, `docs/results/phase00.md`.
8. Gerbang persetujuan. Disetujui (lihat kotak Approval di `phase00.md`).

## Fase 1: Baseline RTL minimal, NTT/INTT L = 1 + perkalian titik

1. Tujuan. Acuan perangkat keras pertama yang benar dan terukur untuk kernel aritmetika (konfigurasi C0). Semua optimasi berikutnya dibandingkan dengannya.
2. Lingkup implementasi. `rtl/ntt/`: satu unit butterfly (mode Cooley-Tukey maju dan Gentleman-Sande mundur), satu pengali modular dengan metode reduksi
   sederhana yang terdokumentasi, pengali base-case bentuk langsung 5 perkalian, ROM twiddle dibangkitkan skrip dari model acuan (tidak diketik tangan),
   penskalaan akhir INTT seperti di FIPS 203, memori polinomial sederhana (tanpa banking), kendali start/done, jadwal tetap.
3. Test / verifikasi. CRG-1 sampai CRG-10. Bit-exact terhadap `ntt`, `intt` dan perkalian domain-NTT di `tb/golden` untuk polinomial acak dan kasus sudut;
   `intt(ntt(f)) = f`; keluaran reduksi selalu < q (assertion); formal: FSM selesai, alamat dalam rentang.
4. Quartus. Kompilasi kernel-only C0: ALM, register, M10K, DSP, Fmax, slack setup/hold terburuk, warning dibahas. Siklus per NTT, INTT dan perkalian titik dari simulasi.
5. Kriteria PASS. Semua CRG lolos; jumlah siklus sama untuk semua masukan yang diuji; satu file evidence Quartus untuk C0; ADR clock target tercatat;
   baris C0 di matriks ablasi terisi nilai MEASURED.
6. Belum boleh. Lebih dari satu lajur; banking memori; pipeline di luar kebutuhan kebenaran; trik reduksi khusus q, perbandingan Montgomery lawan Barrett,
   reduksi malas, Karatsuba; Keccak; integrasi HPS; klaim kinerja atau percepatan apa pun.
7. Artefak evidence. `evidence/phase01/` (test plan, log simulasi dan siklus untuk kedua simulator, log lint/slang, log formal, `quartus_C0.md`); `docs/results/phase01.md`.
8. Gerbang persetujuan. Anggota tim meninjau dan mencentang Approval di `phase01.md` sebelum Fase 2.

## Fase 2: Arsitektur memori, penyimpanan M10K, banking, pembangkit alamat

1. Tujuan. Memori polinomial dan pembangkit alamat yang dapat menyuplai L lajur tanpa konflik bank, diukur pada L = 1 agar hanya perubahan memori yang terlihat (konfigurasi C1).
2. Lingkup implementasi. `rtl/mem/`: penyimpanan polinomial M10K dengan pengemasan terdokumentasi (mis. dua koefisien per word) dan beberapa polinomial per bank;
   fungsi pemetaan bank berparameter untuk L ∈ {1, 2, 4, 8}; pembangkit alamat untuk 7 layer NTT, 7 layer INTT dan perkalian titik, tanpa lintasan bit-reversal terpisah;
   organisasi ROM twiddle per lajur; ping-pong buffering hanya bila jadwal terdokumentasi memerlukannya. Datapath tetap L = 1.
3. Test / verifikasi. CRG-1 sampai CRG-10. Regresi bit-exact Fase 1; bukti bebas konflik: untuk setiap L ∈ {1, 2, 4, 8}, setiap layer dan setiap siklus,
   tidak ada dua akses ke port bank yang sama (properti formal pada pembangkit ditambah enumerasi menyeluruh di model Python); tidak ada alamat di luar rentang;
   siklus stall dihitung di simulasi.
4. Quartus. Kompilasi C1: metrik sama seperti C0, dengan perubahan M10K dan ALM dinyatakan terhadap C0.
5. Kriteria PASS. Bebas konflik terbukti untuk keempat L; siklus stall terukur = 0 pada L = 1; bit-exact; jumlah siklus konstan; baris C1 terisi.
6. Belum boleh. Mengaktifkan lebih dari satu lajur; perubahan pipeline; perubahan aritmetika; Keccak.
7. Artefak evidence. `evidence/phase02/` (spesifikasi peta bank, log bukti dan enumerasi, log simulasi, `quartus_C1.md`); `docs/results/phase02.md`.
8. Gerbang persetujuan. Persetujuan manusia di `phase02.md` sebelum Fase 3.

## Fase 3: Eksplorasi multi-lane, L = 1 / 2 / 4 / 8

1. Tujuan. Mengukur trade-off sumber daya lawan kinerja butterfly paralel di atas memori Fase 2, dan membiarkan tim memilih titik operasi (konfigurasi C2).
2. Lingkup implementasi. Jumlah lajur sebagai parameter; butterfly, aritmetika dan memori seperti Fase 2. Kriteria seleksi (mis. AT terendah dalam anggaran sumber daya tertentu)
   ditulis di ADR sebelum sapuan diukur.
3. Test / verifikasi. CRG-1 sampai CRG-10 untuk tiap L: bit-exact, jumlah siklus konstan, siklus stall = 0, siklus per NTT, INTT dan perkalian titik.
4. Quartus. Satu revisi per L (`C2-L1`, `C2-L2`, `C2-L4`, `C2-L8`), batasan dan seed identik.
5. Kriteria PASS. Keempat konfigurasi benar; empat file evidence Quartus; tabel perbandingan lengkap; ADR pemilihan L (atau L tetap berparameter) ditandatangani tim.
6. Belum boleh. L > 8; perubahan pipeline atau aritmetika; memilih L tanpa pengukuran; membandingkan dengan perangkat lunak atau literatur seolah satu platform.
7. Artefak evidence. `evidence/phase03/` (log per L, `quartus_C2-L<n>.md`, tabel perbandingan); `docs/results/phase03.md`.
8. Gerbang persetujuan. Persetujuan manusia di `phase03.md` (termasuk L terpilih) sebelum Fase 4.

## Fase 4: Optimasi pipeline butterfly

1. Tujuan. Menaikkan Fmax, dan throughput bila mungkin, pada L terpilih dengan mem-pipeline butterfly (konfigurasi C3).
2. Lingkup implementasi. Kedalaman pipeline P sebagai parameter pada himpunan kecil terdokumentasi; penanganan hazard antar layer NTT (stall atau jadwal), dengan biaya stall dihitung.
   Tanpa perubahan aritmetika; tanpa penggabungan layer.
3. Test / verifikasi. CRG-1 sampai CRG-10; test hazard khusus di batas layer; siklus dan siklus stall per P; jumlah siklus konstan.
4. Quartus. Satu revisi per P: Fmax, slack dan register dibandingkan dengan konfigurasi Fase 3.
5. Kriteria PASS. Benar untuk setiap P; perbandingan terukur lengkap; ADR untuk P terpilih; baris C3 terisi.
6. Belum boleh. Optimasi aritmetika; penggabungan layer radix-4; Keccak.
7. Artefak evidence. `evidence/phase04/`; `docs/results/phase04.md`.
8. Gerbang persetujuan. Persetujuan manusia di `phase04.md` sebelum Fase 5.

## Fase 5: Optimasi aritmetika modular

1. Tujuan. Aritmetika modular untuk q = 3329 yang lebih murah dan cepat tanpa mengubah hasil FIPS 203 apa pun (konfigurasi C4). Langkah bagian, masing-masing diukur dan
   ditinjau sendiri, berurutan:
   - 5a reduksi khusus q: memanfaatkan struktur q (perkalian dengan konstanta q sebagai penjumlahan geser di ALM) di dalam metode reduksi yang ada.
   - 5b Montgomery lawan Barrett di balik antarmuka yang sama, keduanya diukur; pilihan lewat ADR. Tabel dalam bentuk Montgomery (bila dipilih) dibangkitkan skrip dari model acuan.
   - 5c (opsional) reduksi malas, hanya dengan batas nilai yang terbukti.
   - 5d (opsional) perkalian base-case ala Karatsuba (4 perkalian, bukan 5).
2. Lingkup implementasi. Hanya unit `rtl/arith/`; jadwal, memori, L dan P tetap.
3. Test / verifikasi. CRG-1 sampai CRG-10 setelah tiap langkah. Pengali-reducer modular diuji menyeluruh untuk semua pasangan masukan a, b dalam [0, q) (layak pada ukuran ini);
   reduksi malas memerlukan bukti formal overflow/batas; regresi bit-exact kernel penuh.
4. Quartus. Satu revisi per langkah (`C4a` sampai `C4d`): DSP, ALM, Fmax dan slack terhadap langkah sebelumnya.
5. Kriteria PASS. Setiap langkah yang dicoba benar dan terukur; pilihan 5b tercatat di ADR; langkah opsional selesai dengan evidence atau ditandai eksplisit "tidak dicoba".
6. Belum boleh. Mengubah q atau aritmetika FIPS 203; reduksi aproksimasi tanpa bukti; perubahan jadwal; Keccak.
7. Artefak evidence. `evidence/phase05/5a/` sampai `5d/` (log uji menyeluruh, bukti formal, file Quartus); `docs/results/phase05.md` dengan satu bagian per langkah.
8. Gerbang persetujuan. Tinjauan manusia atas tiap titik henti; persetujuan `phase05.md` sebelum Fase 6.

## Fase 6: Penjadwalan NTT di tingkat operasi

1. Tujuan. Meminimalkan transformasi dan perpindahan data di seluruh operasi ML-KEM sementara masukan yang nanti datang dari Keccak masih disuplai testbench.
2. Lingkup implementasi. Penjadwal untuk aritmetika K-PKE pada KeyGen, Encrypt dan Decrypt: operand tetap di domain NTT bila FIPS 203 mengizinkan; produk matriks-vektor
   diakumulasi di domain NTT dengan satu INTT per polinomial keluaran; tanpa lintasan pengurutan ulang eksplisit. Langkah opsional 6b: penggabungan layer radix-4, diukur terpisah.
   Hitungan transformasi yang diharapkan (hitungan model acuan dari kyber-py yang diinstrumentasi, 2026-09-28; harus direproduksi dengan menginstrumentasi `tb/golden` sebelum dipakai):
   KeyGen 6 NTT / 0 INTT / 9 polinomial pointwise; Encaps 3 / 4 / 12; Decaps 6 / 5 / 15.
3. Test / verifikasi. CRG-1 sampai CRG-10. Aritmetika tingkat operasi bit-exact terhadap model acuan dengan matriks dan polinomial noise disuntikkan dari model acuan;
   counter transformasi sama dengan hitungan yang direproduksi; jumlah siklus konstan.
4. Quartus. Kernel plus penjadwal: metrik dibandingkan dengan C4; revisi terpisah untuk 6b.
5. Kriteria PASS. Bit-exact; hitungan cocok; siklus dan evidence Quartus tercatat.
6. Belum boleh. Keccak atau sampler di perangkat keras; streaming; mengubah urutan operasi sehingga mengubah keluaran FIPS 203 apa pun.
7. Artefak evidence. `evidence/phase06/`; `docs/results/phase06.md`.
8. Gerbang persetujuan. Persetujuan manusia di `phase06.md` sebelum Fase 7.

## Fase 7: Baseline Keccak-f[1600] + SHA3/SHAKE

1. Tujuan. Baseline Keccak yang benar dan terukur (konfigurasi K0) sebelum optimasi Keccak apa pun.
2. Lingkup implementasi. `rtl/keccak/`: Keccak-f[1600] iteratif, satu ronde per siklus, permutasi tetap 24 siklus; mode sponge SHA3-256, SHA3-512, SHAKE128, SHAKE256 dengan
   absorb dan squeeze multi-blok. Bila `tb/golden` belum punya acuan Keccak-f tingkat permutasi, tambahkan `tb/golden/keccak.py` lebih dulu dan verifikasi terhadap `hashlib`.
3. Test / verifikasi. CRG-1 sampai CRG-10. Keluaran terhadap `hashlib` untuk panjang acak dan panjang batas (0, rate − 1, rate, rate + 1, kelipatan) untuk tiap rate
   (SHA3-256 136 B, SHA3-512 72 B, SHAKE128 168 B, SHAKE256 136 B); squeeze multi-blok; test tingkat permutasi; siklus per permutasi tidak bergantung data
   (total siklus hanya boleh bergantung pada panjang pesan yang publik).
4. Quartus. Revisi K0 mandiri: ALM, register, Fmax, slack.
5. Kriteria PASS. Semua mode bit-exact; latensi permutasi tetap ditunjukkan; baris K0 terisi.
6. Belum boleh. Dua ronde per siklus atau unrolling; sampler streaming; sambungan ke kernel aritmetika.
7. Artefak evidence. `evidence/phase07/`; `docs/results/phase07.md`.
8. Gerbang persetujuan. Persetujuan manusia di `phase07.md` sebelum Fase 8.

## Fase 8: Optimasi Keccak dan streaming

1. Tujuan. Menyingkirkan Keccak dari jalur kritis. Langkah bagian, masing-masing diukur dan ditinjau sendiri:
   - 8a dua ronde per siklus lawan satu (konfigurasi C5).
   - 8b sampler streaming: CBD langsung dari aliran PRF; SampleNTT langsung dari aliran XOF.
   - 8c matriks A dibangkitkan on the fly (Â tidak disimpan).
   - 8d tumpang-tindih Keccak dengan aritmetika (sampling berjalan saat kernel menghitung).
   Langkah 8b sampai 8d bersama membentuk konfigurasi C6 (dicatat sebagai C6b, C6c, C6d).
2. Lingkup implementasi. `rtl/keccak/`, `rtl/sample/`, antarmuka penjadwal; kernel aritmetika tidak berubah.
3. Test / verifikasi. CRG-1 sampai CRG-10 setelah tiap langkah. SampleNTT bit-exact terhadap model acuan termasuk jumlah byte XOF yang dikonsumsi tepat; CBD bit-exact;
   matriks yang dibangkitkan bit-exact. Aturan siklus konstan untuk rejection sampling: dengan ρ tetap dan masukan rahasia bervariasi, jumlah siklus identik;
   dengan ρ bervariasi, variasi jumlah siklus sepenuhnya dijelaskan oleh jumlah penolakan model acuan untuk ρ itu (data publik saja).
4. Quartus. Satu revisi per langkah: ALM, register, M10K, Fmax, slack, dan siklus kernel/operasi.
5. Kriteria PASS. Tiap langkah yang dicoba benar, terukur dan ditinjau; baris C5 dan C6 terisi.
6. Belum boleh. Kendali KEM penuh; compress/encode/FO di perangkat keras; integrasi HPS.
7. Artefak evidence. `evidence/phase08/8a/` sampai `8d/`; `docs/results/phase08.md`.
8. Gerbang persetujuan. Tinjauan manusia atas tiap titik henti; persetujuan `phase08.md` sebelum Fase 9.

## Fase 9: Integrasi RTL ML-KEM-768 penuh (simulasi)

1. Tujuan. KeyGen, Encaps dan Decaps lengkap di RTL, bit-exact terhadap vektor resmi (konfigurasi C7-core).
2. Lingkup implementasi. `rtl/mlkem/`: pengendali tingkat atas untuk KeyGen_internal, Encaps_internal dan Decaps_internal (keacakan masuk lewat port masukan); encode/decode;
   compress/decompress tanpa pembagian; enkripsi ulang FO, pembandingan waktu konstan dan pemilihan implicit-rejection; penyimpanan kunci; pemeriksaan masukan FIPS 203.
   Apakah pemeriksaan masukan berjalan di perangkat keras atau di HPS adalah keputusan tim (ADR) sebelum fase ini dimulai (ADR 0031: HPS).
3. Test / verifikasi. CRG-1 sampai CRG-10. Semua grup ML-KEM-768 dari vektor NIST ACVP terpatok: keyGen (25), enkapsulasi (25), dekapsulasi (10, termasuk ciphertext yang dimodifikasi),
   dan grup key-check (10 + 10) bila pemeriksaan ada di perangkat keras. Uji silang acak terhadap model acuan pada jumlah kasus terdokumentasi dengan seed tetap.
   Bukti siklus konstan untuk Decaps: siklus identik untuk ciphertext valid dan ditolak dan untuk kunci rahasia berbeda (masukan publik tetap). Regresi penuh.
4. Quartus. Kompilasi inti penuh (virtual pin): semua metrik.
5. Kriteria PASS. 100 % vektor yang berlaku lolos di kedua simulator; bukti siklus konstan ada; evidence Quartus; baris C7-core terisi.
6. Belum boleh. Klaim tentang papan; integrasi HPS; perbandingan dengan perangkat lunak; klaim protokol.
7. Artefak evidence. `evidence/phase09/` (log uji vektor per grup, log uji silang, log invariansi siklus, `quartus_C7-core.md`); `docs/results/phase09.md`.
8. Gerbang persetujuan. Persetujuan manusia di `phase09.md` sebelum Fase 10.

## Fase 10: Integrasi HPS-FPGA di DE10-Nano

1. Tujuan. Akselerator bekerja di papan nyata di bawah kendali HPS (konfigurasi C7-soc). Terblokir sampai DE10-Nano tersedia (PENDING #8); alur protokol
   memerlukan PENDING #1 (sisi target) dan PENDING #7 (alur pesan yang diemulasi).
2. Lingkup implementasi. Sistem Platform Designer dengan HPS; jembatan dipilih lewat pengukuran (mekanisme transfer lewat ADR, PENDING #3); antarmuka tingkat perintah
   (HPS memberi perintah KeyGen/Encaps/Decaps, bukan NTT satuan); kunci rahasia dan polinomial antara tetap di fabric; encode/decode di fabric; counter siklus fabric yang bisa dibaca HPS;
   penghapusan kunci saat reset; driver dan program uji di `sw/hps/`; emulasi fungsional alur pertukaran kunci gaya PACE yang dijelaskan di proposal.
   Tap SignalTap hanya pada sinyal kendali non-rahasia di bitstream demo.
3. Test / verifikasi. Vektor NIST terpatok yang sama dijalankan di papan dari HPS; uji silang acak terhadap model acuan; soak test pada banyak iterasi; persilangan domain clock ditinjau;
   tangkapan SignalTap atas handshake kendali; overhead transfer diukur terpisah dari waktu inti.
4. Quartus. Kompilasi sistem penuh dengan semua clock dibatasi: semua metrik, slack tiap domain clock.
5. Kriteria PASS. 100 % vektor lolos di papan; timing terpenuhi untuk tiap clock; ADR jembatan/transfer tercatat; log papan dan tangkapan tersimpan. Tanpa papan, fase ini tetap `NOT DONE`.
6. Belum boleh. Klaim kinerja akhir; perbandingan dengan baseline perangkat lunak (Fase 11); klaim keamanan di luar perilaku siklus konstan.
7. Artefak evidence. `evidence/phase10-hps-integration/` (log papan, tangkapan SignalTap, `quartus_C7-soc.md`, pengukuran transfer); `docs/results/phase10.md`.
8. Gerbang persetujuan. Persetujuan manusia di `phase10.md` sebelum Fase 11.

## Fase 11: Benchmark akhir dan perbandingan dengan baseline perangkat lunak

1. Tujuan. Angka ujung-ke-ujung yang jujur untuk proposal dan demo.
2. Lingkup implementasi. Baseline perangkat lunak di HPS pada papan yang sama (implementasi, compiler dan flag dicatat; baseline kedua hanya bila tim memutuskan, PENDING #6);
   metode benchmark tertulis (pemanasan, jumlah run, median dan sebaran, sumber timer) ditetapkan sebelum mengukur.
3. Test / verifikasi. Per KeyGen/Encaps/Decaps: siklus inti (counter fabric), waktu ujung-ke-ujung (HPS), overhead transfer, throughput; latensi tingkat protokol pada
   pertukaran kunci yang diemulasi; invariansi siklus diulang di papan; uji vektor diulang pada bitstream akhir.
4. Quartus. Evidence bitstream akhir (konfigurasi yang benar-benar diukur), semua metrik.
5. Kriteria PASS. Setiap sel matriks ablasi MEASURED atau ditandai eksplisit "tidak diukur" beserta alasan; `docs/proposal/CLAIMS_REGISTER.md` diperbarui;
   angka proposal berubah dari ESTIMATE hanya bila ada evidence; pemeriksa klaim bersih.
6. Tidak boleh. Memilih run yang menguntungkan; membandingkan dengan angka literatur dari platform lain seolah setara; klaim daya atau energi tanpa pengukuran daya;
   klaim keamanan di luar siklus konstan.
7. Artefak evidence. `evidence/phase11-benchmark/` (metode, log waktu mentah, tabel ringkasan, file Quartus akhir); `docs/results/phase11.md`.
8. Gerbang persetujuan. Persetujuan manusia di `phase11.md` sebelum apa pun diterbitkan sebagai hasil atau sebelum Fase 12.

## Fase 12: Fitur keamanan lanjutan (opsional)

1. Tujuan. Penguatan opsional: masking/shuffling, deteksi kesalahan (mis. perbandingan FO ganda, paritas memori), TVLA dengan osiloskop tim,
   parameterisasi ML-KEM-512/1024, hibrida ECDH + ML-KEM di HPS.
2. Lingkup implementasi. Satu fitur sekali waktu, masing-masing dengan ADR sendiri yang menyatakan ancaman, metode dan klaim yang akan didukungnya.
3. Test / verifikasi. CRG penuh dan regresi vektor penuh setelah tiap fitur; TVLA dengan setup akuisisi dan jumlah trace terdokumentasi; overhead diukur ulang.
4. Quartus. Satu revisi per fitur: overhead terhadap konfigurasi Fase 11.
5. Kriteria PASS. Kriteria khusus fitur ditulis di ADR-nya sebelum implementasi.
6. Tidak boleh. Klaim ketahanan side-channel atau kesalahan tanpa evidence; melemahkan sifat siklus konstan desain inti.
7. Artefak evidence. `evidence/phase12-security/<fitur>/`; `docs/results/phase12.md`.
8. Gerbang persetujuan. Persetujuan manusia per fitur.

---

## Matriks ablasi optimasi

Setiap baris berbeda satu perubahan dari baris pembandingnya. Semua sel kosong sampai laporan Quartus atau log test di repository ini
mengisinya; lalu sel berisi nilainya dan kolom Evidence berisi path. Baris yang memburuk tetap disimpan dan dibahas di file hasil fasenya;
ADR yang memutuskan perubahan itu dipertahankan atau tidak.

| ID | Konfigurasi | Perubahan terhadap baris pembanding | Fase | Dibandingkan dengan | Cakupan | ALM | Register | M10K | DSP | Fmax (MHz) | Slack terburuk (ns) | Siklus/op | Latensi (µs @ f_clk) | AT (ALM × µs) | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C0 | Baseline | — (L = 1, memori sederhana) | 1 | — | Kernel | 7,010 / 41,910 | 3104 | 0 / 553 | 3 / 112 | 14.64 (Slow 100C) | -48.323 @ 20.000 ns (TIDAK terpenuhi) | NTT 897, INTT 1153 (simulasi) | tidak dinyatakan: timing tidak terpenuhi pada clock terbatas | tidak dinyatakan | `evidence/quartus/C0.md`, `evidence/phase01/quartus_C0_timing_analysis.md`, `evidence/phase01/cocotb_regression.txt` |
| C1 | + Banking memori | banking M10K + pembangkit alamat | 2 | C0 | Kernel | 6,749 / 41,910 (-261 terhadap C0) | 3,105 | 0 / 553 (M10K NOT achieved, async-read limitation -- lihat evidence) | 3 / 112 | 14.99 (Slow 100C) | -46.720 @ 20.000 ns (TIDAK terpenuhi) | NTT 897, INTT 1153 (simulasi, identik dengan C0, 0 stall) | tidak dinyatakan: timing tidak terpenuhi pada clock terbatas | tidak dinyatakan | `evidence/quartus/C1.md`, `evidence/phase02/quartus_C1_vs_C0.md`, `evidence/phase02/cocotb_regression.txt` |
| C2-L1 | + Multi-lane (L=1) | Datapath lajur dibangun ulang di atas memori multi-port (pemeriksaan paritas terhadap C0/C1) | 3 | C1 | Kernel | 6,018 / 41,910 | 3100 | 0 / 553 | 3 / 112 | 14.76 (Slow 100C) | -47.733 @ 20.000 ns (TIDAK terpenuhi) | NTT 897, INTT 1153 (simulasi, identik dengan C0/C1) | tidak dinyatakan: timing tidak terpenuhi pada clock terbatas | tidak dinyatakan | `evidence/quartus/C2-L1.md`, `evidence/phase03/cocotb_regression.txt` |
| C2-L2 | + Multi-lane (L=2) | 2 butterfly/siklus | 3 | C1 | Kernel | 5,728 / 41,910 | 3098 | 0 / 553 | 5 / 112 | 13.54 (Slow 100C) | -54.644 @ 20.000 ns (TIDAK terpenuhi) | NTT 449, INTT 705 (simulasi) | tidak dinyatakan: timing tidak terpenuhi pada clock terbatas | tidak dinyatakan | `evidence/quartus/C2-L2.md`, `evidence/phase03/cocotb_regression.txt` |
| C2-L4 | + Multi-lane (L=4) | 4 butterfly/siklus | 3 | C1 | Kernel | 7,629 / 41,910 | 3102 | 0 / 553 | 9 / 112 | 11.60 (Slow 100C) | -66.690 @ 20.000 ns (TIDAK terpenuhi) | NTT 225, INTT 481 (simulasi) | tidak dinyatakan: timing tidak terpenuhi pada clock terbatas | tidak dinyatakan | `evidence/quartus/C2-L4.md`, `evidence/phase03/cocotb_regression.txt` |
| C2-L8 | + Multi-lane (L=8) | 8 butterfly/siklus | 3 | C1 | Kernel | 11,446 / 41,910 (melewati anggaran 10,478 ALM ADR 0004) | 3100 | 0 / 553 | 17 / 112 | 7.62 (Slow 100C) | -111.219 @ 20.000 ns (TIDAK terpenuhi) | NTT 113, INTT 369 (simulasi) | tidak dinyatakan: timing tidak terpenuhi pada clock terbatas | tidak dinyatakan | `evidence/quartus/C2-L8.md`, `evidence/phase03/cocotb_regression.txt` |
| C2-K2-K1-L1 | + K2, K1 (L=1) | DUA perubahan terhadap C2-L1, pengecualian aturan satu-perubahan: ukuran t_q per L (K2) + satu pengali bersama per butterfly (K1); langkah satu-perubahan C2 -> C2-K2 diukur di `evidence/quartus/C2-L1-K2.md`. Tambahan, di luar lingkup Fase 3 yang tertulis | 3 | C2-L1 | Kernel | 5,566 / 41,910 | 3099 | 0 / 553 | 2 / 112 | 14.33 (Slow 100C) | -49.804 @ 20.000 ns (TIDAK terpenuhi) | NTT 897, INTT 1153 (simulasi, identik dengan C2-L1) | tidak dinyatakan: timing tidak terpenuhi pada clock terbatas | tidak dinyatakan | `evidence/quartus/C2-K2-K1-L1.md`, `evidence/phase03/k1_cocotb_regression.txt` |
| C2-K2-K1-L2 | + K2, K1 (L=2) | DUA perubahan terhadap C2-L2, pengecualian aturan satu-perubahan: ukuran t_q per L (K2) + satu pengali bersama per butterfly (K1); langkah satu-perubahan C2 -> C2-K2 diukur di `evidence/quartus/C2-L2-K2.md`. Tambahan, di luar lingkup Fase 3 yang tertulis | 3 | C2-L2 | Kernel | 5,374 / 41,910 | 3095 | 0 / 553 | 3 / 112 | 12.63 (Slow 100C) | -59.148 @ 20.000 ns (TIDAK terpenuhi) | NTT 449, INTT 705 (simulasi, identik dengan C2-L2) | tidak dinyatakan: timing tidak terpenuhi pada clock terbatas | tidak dinyatakan | `evidence/quartus/C2-K2-K1-L2.md`, `evidence/phase03/k1_cocotb_regression.txt` |
| C2-K2-K1-L4 | + K2, K1 (L=4) | DUA perubahan terhadap C2-L4, pengecualian aturan satu-perubahan: ukuran t_q per L (K2) + satu pengali bersama per butterfly (K1); langkah satu-perubahan C2 -> C2-K2 diukur di `evidence/quartus/C2-L4-K2.md`. Tambahan, di luar lingkup Fase 3 yang tertulis | 3 | C2-L4 | Kernel | 6,775 / 41,910 | 3098 | 0 / 553 | 5 / 112 | 10.89 (Slow 100C) | -71.868 @ 20.000 ns (TIDAK terpenuhi) | NTT 225, INTT 481 (simulasi, identik dengan C2-L4) | tidak dinyatakan: timing tidak terpenuhi pada clock terbatas | tidak dinyatakan | `evidence/quartus/C2-K2-K1-L4.md`, `evidence/phase03/k1_cocotb_regression.txt` |
| C2-K2-K1-L8 | + K2, K1 (L=8) | DUA perubahan terhadap C2-L8, pengecualian aturan satu-perubahan: ukuran t_q per L (K2) + satu pengali bersama per butterfly (K1); langkah satu-perubahan C2 -> C2-K2 diukur di `evidence/quartus/C2-L8-K2.md`. Tambahan, di luar lingkup Fase 3 yang tertulis | 3 | C2-L8 | Kernel | 9,754 / 41,910 (terpilih, ADR 0005; dalam anggaran 10,478 ALM) | 3094 | 0 / 553 | 9 / 112 | 7.68 (Slow 100C) | -110.494 @ 20.000 ns (TIDAK terpenuhi) | NTT 113, INTT 369 (simulasi, identik dengan C2-L8) | tidak dinyatakan: timing tidak terpenuhi pada clock terbatas | tidak dinyatakan | `evidence/quartus/C2-K2-K1-L8.md`, `evidence/phase03/k1_cocotb_regression.txt` |
| C3-P0 | + Pipeline (P=0, acuan) | C2-K2-K1-L8 yang dibekukan dikompilasi ulang pada 40.000 ns | 4 | C2-K2-K1-L8 (ADR 0005) | Kernel | 9,723 / 41,910 | 3097 | 0 / 553 | 9 / 112 | 7.65 (Slow 100C) | -90.653 @ 40.000 ns (TIDAK terpenuhi) | NTT 113, INTT 369 (simulasi) | tidak dinyatakan: Fmax kernel-only, tanpa papan | tidak dinyatakan | `evidence/phase04/quartus_C3-P0.md`, `evidence/phase04/cocotb_regression.txt` |
| C3-P2 | + Pipeline (P=2) | Potongan A_13, D_3 | 4 | C2-K2-K1-L8 (ADR 0005) | Kernel | 9,696 / 41,910 | 3,817 | 16 / 553 (disimpulkan alat) | 9 / 112 | 24.77 (slow corner terendah) | -0.368 @ 40.000 ns (TIDAK terpenuhi) | NTT 115, INTT 371 (simulasi) | tidak dinyatakan: Fmax kernel-only, tanpa papan | tidak dinyatakan | `evidence/phase04/quartus_C3-P2.md`, `evidence/phase04/cocotb_regression.txt` |
| C3-P4 | + Pipeline (P=4) | Potongan A_7, M, X, D_7 -- diusulkan ADR 0008 di bawah anggaran 25 % historis (tidak pernah diterima, digantikan ADR 0009); baseline integrasi untuk GHRD + C3-P4 (`evidence/phase04/ghrd_plus_c3p4_integration.md`) | 4 | C2-K2-K1-L8 (ADR 0005) | Kernel | 10,439 / 41,910 (seed 1–6: 10,439–10,503; dalam anggaran 30 % / 12,573 ADR 0009) | 4,145 | 26 / 553 (disimpulkan alat) | 9 / 112 | 31.98 (slow corner terendah) | +8.734 @ 40.000 ns (terpenuhi) | NTT 117, INTT 373 (simulasi) | tidak dinyatakan: Fmax kernel-only, tanpa papan | tidak dinyatakan | `evidence/phase04/quartus_C3-P4.md`, `evidence/phase04/cocotb_regression.txt` |
| C3-P6 | + Pipeline (P=6) | Potongan A_4, A_11, M, X, D_5, D_11 -- TERPILIH (ADR 0009, 2026-10-01): L = 8, P = 6; integrasi dengan GHRD: `evidence/phase04/ghrd_plus_c3p6_integration.md` (12,375 ALM gabungan, NTT 40 ns terpenuhi, MEASURED) | 4 | C2-K2-K1-L8 (ADR 0005) | Kernel | 10,505 / 41,910 (seed 1–6: 10,484–10,516; melewati anggaran 25 % historis, dalam anggaran 30 % / 12,573 ADR 0009) | 4,168 | 29 / 553 (disimpulkan alat) | 9 / 112 | 34.19 (slow corner terendah) | +10.753 @ 40.000 ns (terpenuhi) | NTT 119, INTT 375 (simulasi) | tidak dinyatakan: Fmax kernel-only, tanpa papan | tidak dinyatakan | `evidence/phase04/quartus_C3-P6.md`, `evidence/phase04/cocotb_regression.txt` |
| C4a | + Aritmetika 5a (reducer fold) | reduksi khusus q: 2^12 = 767 (mod q), fold penjumlahan geser + pemilihan; cuts A_4, A_11, M, X, F_3, F_5 (P = 6) | 5 | C3-P6 | Kernel | 9,847 / 41,910 | 4,109 | 29 / 553 (disimpulkan alat) | 9 / 112 | 33.73 (slow corner terendah) | +10.352 @ 40.000 ns (terpenuhi) | NTT 119, INTT 375 (simulasi) | tidak dinyatakan: Fmax kernel-only, tanpa papan | tidak dinyatakan | `evidence/phase05/5a/quartus_C4a.md`, `evidence/phase05/5a/summary_5a.md`, `evidence/phase05/5a/verify.txt` |
| C4b-B | + Aritmetika 5b (Barrett) | reducer Barrett (k = 24, M = 5039), potongan X, S_1, S_2; dipilih aturan ADR 0011, ADR 0013 (sebelumnya Proposed, PENDING #23): ini konfigurasi C4 | 5 | C4a | Kernel | 9,208 / 41,910 (seed 1-6: 9,166-9,208; median 9,171) | 4,115 | 29 / 553 (disimpulkan alat) | 18 / 112 (C3-P6: 9) | 34.54 (seed 1; median over seed 1-6 34.515, range 33.46-34.84) | +11.044 @ 40.000 ns (terpenuhi di setiap seed) | NTT 119, INTT 375 (simulasi) | t_NTT 3.448 us, t_INTT 10.865 us pada Fmax median (perhitungan tim); kernel-only, tanpa papan | tidak dinyatakan | `evidence/phase05/5b/quartus_C4b-B.md` (+ `-s2..s6`), `evidence/phase05/5b/selection_worksheet.md`, `evidence/phase05/5b/verify.txt` |
| C4b-M | + Aritmetika 5b (Montgomery, pembanding) | reducer Montgomery (R = 2^12), ROM twiddle bentuk Montgomery; tidak dipilih | 5 | C4a | Kernel | 9,249 / 41,910 (seed 1-6: 9,249-9,297; median 9,286.5) | 4,297 | 29 / 553 (disimpulkan alat) | 9 / 112 | 32.81 (seed 1; median 33.780, range 32.81-34.25) | +9.526 @ 40.000 ns (terpenuhi di setiap seed) | NTT 119, INTT 375 (simulasi) | tidak dinyatakan: Fmax kernel-only, tanpa papan | tidak dinyatakan | `evidence/phase05/5b/quartus_C4b-M.md` (+ `-s2..s6`), `evidence/phase05/5b/selection_worksheet.md` |
| C4c | + Aritmetika 5c (masukan INTT malas) | masukan pengali INTT b + q - a di [1, 2q), operand sisi a + b di [0, 2q), direduksi sekali di keluaran (ADR 0014; D6 diubah hanya untuk eksperimen ini); TIDAK diadopsi (median Fmax 33.100 MHz, aturan butuh > 34.84; ADR 0012 tidak terpenuhi) | 5 | C4b-B | Kernel | 9,043 / 41,910 (seed 1-6: 9,032-9,094; median 9,059.5) | 4,076 | 29 / 553 (disimpulkan alat) | 18 / 112 | 32.98 (seed 1; median 33.100, range 32.27-35.26) | +9.682 @ 40.000 ns (terpenuhi di setiap seed) | NTT 119, INTT 375 (simulasi) | tidak dinyatakan: tidak diadopsi | tidak dinyatakan | `evidence/phase05/5c/quartus_C4c.md` (+ `-s2..s6`), `evidence/phase05/5c/selection_worksheet.md`, `evidence/phase05/5c/summary_5c.md` |
| C4d | + Aritmetika 5d (base case ala Karatsuba) | Tidak dicoba di Fase 5 (diusulkan pindah ke Fase 6: `base_case_multiply.sv` bukan bagian inti C3-P6 / C4; ADR 0015) | 5 | C4b-B | Kernel | tidak dicoba | tidak dicoba | tidak dicoba | tidak dicoba | tidak dicoba | tidak dicoba | tidak dicoba | tidak dicoba | tidak dicoba | `docs/decisions/adr/ADR-0015-phase-5d-karatsuba-style-base-case-not-attempted-in-phase-5-.md` |
| C4b-B-20 | Kompilasi informasi pada 20.000 ns (C4 akhir) | RTL sama dengan C4b-B; batasan 20.000 ns, seed bawaan; bukan gerbang (ADR 0010, ADR 0011 D1) | 5 | C3-P6-20 | Kernel | 9,305 / 41,910 | 4,272 | 29 / 553 (disimpulkan alat) | 18 / 112 | 44.33 (slow corner terendah) | -2.557 @ 20.000 ns (TIDAK terpenuhi) | NTT 119, INTT 375 (simulasi) | tidak dinyatakan: timing tidak terpenuhi pada clock terbatas | tidak dinyatakan | `evidence/phase05/closure/quartus_C4b-B-20.md`, `evidence/phase05/closure/info_20ns.md` |
| C3-P6-20 | Kompilasi informasi pada 20.000 ns (acuan C3-P6) | RTL Fase 4 tidak berubah; batasan 20.000 ns, seed bawaan; bukan gerbang | 5 | C3-P6 | Kernel | 10,557 / 41,910 | 4,316 | 29 / 553 (disimpulkan alat) | 9 / 112 | 45.33 (slow corner terendah) | -2.059 @ 20.000 ns (TIDAK terpenuhi) | NTT 119, INTT 375 (simulasi) | tidak dinyatakan: timing tidak terpenuhi pada clock terbatas | tidak dinyatakan | `evidence/phase05/closure/quartus_C3-P6-20.md`, `evidence/phase05/closure/info_20ns.md` |
| M6 | + Memori/jadwal S6 (INTT tanpa lintasan skala) | Pembagian dua di setiap layer INTT (3303 = 2^-7 mod q), ROM zeta/2, tanpa lintasan skala atau pengali; tidak diadopsi aturan (ADR 0012), basis S7/S8 atas keputusan tim (ADR 0020 Accepted) | 5M | C4b-B | Kernel | 9,394 / 41,910 (seed 1-6: 9,394-9,441; median 9,421.5) | 4,030-4,080 | 29 / 553 (disimpulkan alat) | 16 / 112 | 34.430 (median seed 1-6, rentang 32.35-35.04) | terpenuhi pada 40.000 ns di setiap seed | NTT 119, INTT 119 (simulasi) | t = 3.456 us pada Fmax median (perhitungan tim) | tidak dinyatakan | `evidence/phase05m/s6/selection_worksheet.md` |
| S7 | + Memori/jadwal S7 (pembacaan memori terbelah, RD_SPLIT, P = 7) | Satu tahap register di dalam pembacaan memori (192 bit data + 64 bit pemilih); diadopsi aturan (ADR 0021, digantikan 0025) | 5M | M6 | Kernel | 9,394 / 41,910 (seed 1-6: 9,361-9,405; median 9,391.0) | 4,296-4,324 | 31 / 553 (disimpulkan alat) | 16 / 112 | 38.720 (median seed 1-6, rentang 37.89-40.29) | terpenuhi pada 40.000 ns di setiap seed | NTT 120, INTT 120 (simulasi) | t = 3.099 us pada Fmax median (perhitungan tim) | tidak dinyatakan | `evidence/phase05m/s7/selection_worksheet.md` |
| S8 | + Memori/jadwal S8 (register jalur tulis, P = 8, satu bubble per arah) | Satu register pada keluaran butterfly, bubble setelah layer NTT 3 dan layer INTT 2; tidak diadopsi aturan (ADR 0023, digantikan 0025) | 5M | S7 | Kernel | 9,464 / 41,910 (seed 1-6: 9,402-9,471; median 9,443.5) | 4,130-4,144 | 33 / 553 (disimpulkan alat) | 16 / 112 | 37.990 (median seed 1-6, rentang 36.76-40.22) | terpenuhi pada 40.000 ns di setiap seed | NTT 122, INTT 122 (simulasi) | t = 3.211 us pada Fmax median (perhitungan tim) | tidak dinyatakan | `evidence/phase05m/s8/selection_worksheet.md` |
| S8-20 | Kompilasi informasi pada 20.000 ns (S8) | RTL sama dengan S8, seed 1; bukan gerbang | 5M | C4b-B-20 | Kernel | 9,443 / 41,910 | 4,142 | 33 / 553 (disimpulkan alat) | 16 / 112 | 44.96 (slow corner terendah) | -2.242 @ 20.000 ns (TIDAK terpenuhi) | NTT 122, INTT 122 (simulasi) | tidak dinyatakan: timing tidak terpenuhi pada clock terbatas | tidak dinyatakan | `evidence/phase05m/s8/quartus_S8-20.md` |
| S9 | Studi memori (M10K, pembacaan sinkron) | Hanya dokumentasi, tanpa RTL, tanpa Quartus: peta 16 bank 1R1W bebas konflik di seluruh jadwal; opsi A dibangun sebagai S10 (ADR 0022, digantikan 0025) | 5M | S7 | Studi | tidak diukur | tidak diukur | tidak diukur | tidak diukur | tidak diukur | tidak diukur | tidak berlaku | tidak berlaku | tidak dinyatakan | `evidence/phase05m/s9/study_m10k.md` |
| S7-20 | Kompilasi informasi pada 20.000 ns (S7), seed 1-6 | RTL sama dengan S7 (pertanyaan 50 MHz, opsi 2) | 5M | S8-20 | Kernel | 9,355-9,383 / 41,910 | tidak dinyatakan | tidak dinyatakan | 16 / 112 | median 45.885 (44.58-46.76) | -1.388 sampai -2.431 @ 20.000 ns (TIDAK terpenuhi di seed mana pun) | NTT 120, INTT 120 (simulasi) | tidak dinyatakan: timing tidak terpenuhi | tidak dinyatakan | `evidence/phase05m/fmax50/path_analysis.md` |
| S10 | + Memori: 16 bank 1R1W tanpa arbitrasi slot (P = 5) | Peta bank (a1^a2^a3^a4, a7, a6, a5), offset a[3:0], blok RAM, pemilih 16 arah; diadopsi aturan; inti NTT/INTT untuk fase berikutnya (ADR 0025 Accepted 2026-10-03) | 6 | S7 | Kernel | 5,091 / 41,910 (seed 1-6: 5,045-5,091; median 5,077.0) | 543-555 | 24 / 553 | 16 / 112 | 44.320 (median seed 1-6, rentang 42.34-46.65) | terpenuhi pada 40.000 ns di setiap seed | NTT 118, INTT 118 (simulasi) | t = 2.662 us pada Fmax median (perhitungan tim) | tidak dinyatakan | `evidence/phase06/s10/selection_worksheet.md` |
| S10-20 | Kompilasi informasi pada 20.000 ns (S10), seed 1-6 | RTL sama dengan S10 | 6 | S7-20 | Kernel | lihat evidence | 543-555 (40 ns) | 24 / 553 | 16 / 112 | median 52.945 (52.06-54.70) | +0.792 sampai +1.718 @ 20.000 ns (terpenuhi di 6 dari 6 seed, kernel-only) | NTT 118, INTT 118 (simulasi) | tidak dinyatakan: kernel-only, tanpa papan | tidak dinyatakan | `evidence/phase06/s10/selection_worksheet.md` |
| S1 / P6 | Penjadwalan NTT di tingkat operasi (Fase 6) | sequencer aritmetika K-PKE (program KeyGen, Encrypt, Decrypt), unit perkalian-akumulasi pointwise, 24 slot polinomial, inti S7; hitungan 6/0/9, 3/4/12, 3/1/3; 6b tidak dicoba | 6 | S7 | Kernel + penjadwal | 9,840 / 41,910 (seed 1) | 4,589 | 58 / 553 | 26 / 112 | 37.59 (seed 1) | +13.395 @ 40.000 ns (terpenuhi) | KeyGen 5,493, Encrypt 6,810, Decrypt 3,121 (simulasi; dengan S10: 5,475 / 6,789 / 3,109) | tidak dinyatakan: kernel-only | tidak dinyatakan | `evidence/phase06/quartus_P6.md`, `docs/results/phase06.md` |
| P6S10 | Top Fase 6 dengan inti S10 (informasi) | Sequencer sama, inti S10; 40 ns dan 20 ns, seed 1 | 6 | S1 / P6 | Kernel + penjadwal | 5,553 / 41,910 (40 ns); 5,643 (20 ns) | 840 | 51 / 553 | 26 / 112 | 43.26 @ 40 ns; 51.60 @ 20 ns | +16.886 @ 40.000 ns; +0.619 @ 20.000 ns (terpenuhi) | KeyGen 5,475, Encrypt 6,789, Decrypt 3,109 (simulasi) | tidak dinyatakan: kernel-only | tidak dinyatakan | `evidence/phase06/quartus_P6S10-20.md` |
| K0 | Baseline Keccak *(baris acuan)* | Keccak-f[1600] iteratif, 1 ronde/siklus (24 siklus sibuk); sponge SHA3-256, SHA3-512, SHAKE128, SHAKE256 (`keccak_sponge`) | 7 | — | Keccak | 3,572 / 41,910 (seed 1) | 1,653 | 0 / 553 | 0 / 112 | 56.99 (seed 1, terendah dari enam; median seed 1-6 67.675, rentang 56.99-70.39) | +22.452 @ 40.000 ns seed 1 (terpenuhi di setiap seed 1-6) | permutasi 24 siklus sibuk, 26 di sponge; H(ek) 1184 B 389 siklus (simulasi) | 0.456 us per permutasi pada 56,99 MHz (perhitungan tim) | tidak dinyatakan | `evidence/phase07/quartus_K0.md`, `docs/results/phase07.md` |
| K0-20 | Kompilasi informasi pada 20.000 ns (K0) | RTL sama dengan K0, seed 1; bukan gerbang | 7 | K0 | Keccak | 3,573 / 41,910 | 1,653 | 0 / 553 | 0 / 112 | 76.30 (slow corner terendah) | +6.893 @ 20.000 ns (terpenuhi, kernel-only) | seperti K0 | tidak dinyatakan: kernel-only, tanpa papan | tidak dinyatakan | `evidence/phase07/quartus_K0-20.md` |
| C5 | + Optimasi Keccak (8a) | 2 ronde/siklus (`keccak_f1600_r2`, `keccak_sponge_r2`): 12 siklus sibuk, 14 per permutasi di sponge; diadopsi aturan (ADR 0027) | 8a | K0 | Keccak | 6,167 / 41,910 median (seed 1-6: 6,152-6,169) | 1,652 | 0 / 553 | 0 / 112 | 50.655 (median seed 1-6, rentang 47.38-51.67) | terpenuhi pada 40.000 ns di setiap seed | permutasi 14 siklus di sponge (K0: 26); H(ek) 1184 B 281 siklus (K0: 389) (simulasi) | 0.2764 us per permutasi pada Fmax median (K0: 0.3842) (perhitungan tim) | tidak dinyatakan | `evidence/phase08/8a/selection_worksheet.md`, `docs/results/phase08.md` |
| C5-20 | Kompilasi informasi pada 20.000 ns (C5) | RTL sama dengan C5, seed 1; bukan gerbang | 8a | K0-20 | Keccak | 6,178 / 41,910 | 1,652 | 0 / 553 | 0 / 112 | 64.90 (slow corner terendah) | +4.591 @ 20.000 ns (terpenuhi, kernel-only) | seperti C5 | tidak dinyatakan: kernel-only, tanpa papan | tidak dinyatakan | `evidence/phase08/8a/quartus_C5-20.md` |
| C6b-W1 | + Sampler streaming, satu koefisien per siklus (8b tahap W1) | SampleNTT dan CBD2 langsung dari aliran word Keccak, tanpa penyimpanan antara sponge dan sampler (`rtl/sample/`, `OUTW` = 1); lolos gerbang 8b; tidak dipilih aturan 8b | 8b | C5 | Sampler + Keccak | MEASURED: 5,279.0 / 41,910 median (seed 1-6: 5,271-5,311) | 1,913 | 0 / 553 | 0 / 112 | 51.220 (median seed 1-6, rentang 50.10-55.79) | terpenuhi pada 40.000 ns di setiap seed | SampleNTT 305.23 siklus (rerata 500), CBD 280 (simulasi) | SampleNTT 5.959 us, CBD 5.467 us pada Fmax median (perhitungan tim) | tidak dinyatakan | `evidence/phase08/8b/selection_worksheet.md`, `docs/decisions/adr/ADR-0028-*.md` |
| C6b-W2 | + Sampler streaming, dua koefisien per siklus (8b tahap W2) | File sama dengan `OUTW` = 2: satu triple per siklus, kolam 0-3 kandidat dengan satu koefisien terbawa; lolos gerbang; dipilih aturan atas W1 (ADR 0028) | 8b | C6b-W1 | Sampler + Keccak | MEASURED: 5,290.0 / 41,910 median (seed 1-6: 5,282-5,308) | 1,947 | 0 / 553 | 0 / 112 | 50.220 (median seed 1-6, rentang 48.46-53.42) | terpenuhi pada 40.000 ns di setiap seed | SampleNTT 206.48 siklus (= triple + 49 untuk 3 blok XOF, + 61 untuk 4), CBD 152 (simulasi) | SampleNTT 4.111 us, CBD 3.027 us pada Fmax median (perhitungan tim) | tidak dinyatakan | `evidence/phase08/8b/selection_worksheet.md`, `docs/decisions/adr/ADR-0028-*.md` |
| C6c-STORE | Acuan untuk 8c: matriks A disampel ke 9 slot | `SMPA` ke slot 0-8, lalu lintasan PWM Fase 6; 24 slot; S10 core, W2 sampler, C5 sponge (`kpke_smp_top_s10`, `VAR` = 0) | 8c | C6b-W2 + P6S10 | Operasi | MEASURED: 10,958.0 / 41,910 median (seed 1-6: 10,941-10,969) | 3,342-3,378 | 55 / 553 | 26 / 112 | 42.270 (median seed 1-6, rentang 41.21-44.28) | terpenuhi pada 40.000 ns di setiap seed; 20 ns (seed 1) terpenuhi, +0.992 ns | KeyGen 8,268.1, Encrypt 9,727.6, Decrypt 3,109 (simulasi, rerata) | KeyGen 195.6 us, Encrypt 230.1 us pada Fmax median (perhitungan tim) | tidak dinyatakan | `evidence/phase08/8c/selection_worksheet.md` |
| C6c | + Streaming 8c: matriks A tidak disimpan | `PWMS`: beat sampler mengisi unit PWM; operand b, word akumulator dan gamma dialamati satu beat lebih awal; 12 slot; diadopsi aturan (ADR 0029) | 8c | C6c-STORE | Operasi | MEASURED: 10,995.5 / 41,910 median (seed 1-6: 10,958-11,032) | 3,377-3,395 | 44 / 553 | 26 / 112 | 43.355 (median seed 1-6, rentang 40.37-45.66) | terpenuhi pada 40.000 ns di setiap seed; 20 ns (seed 1) terpenuhi, +1.783 ns | KeyGen 7,089.1, Encrypt 8,548.6, Decrypt 3,109 (simulasi, rerata) | KeyGen 163.5 us, Encrypt 197.2 us pada Fmax median (perhitungan tim) | tidak dinyatakan | `evidence/phase08/8c/selection_worksheet.md`, `docs/decisions/adr/ADR-0029-*.md` |
| C6d | + Streaming 8d: sampling ditumpangkan dengan transformasi | `SMPN` tanpa blokir, `WAIT`, arbitrasi port penyimpanan (sequencer lebih dulu); 5 dari 6 (KeyGen) dan 6 dari 7 (Encrypt) polinomial noise tersembunyi; diadopsi aturan (ADR 0030) | 8d | C6c | Operasi | MEASURED: 10,992.5 / 41,910 median (seed 1-6: 10,954-11,012) | 3,368-3,414 | 44 / 553 | 26 / 112 | 43.755 (median seed 1-6, rentang 42.14-46.38) | terpenuhi pada 40.000 ns di setiap seed; 20 ns (seed 1) terpenuhi, +1.535 ns | KeyGen 6,344.1, Encrypt 7,654.6, Decrypt 3,109 (simulasi, rerata) | KeyGen 145.0 us, Encrypt 174.9 us pada Fmax median (perhitungan tim) | tidak dinyatakan | `evidence/phase08/8d/selection_worksheet.md`, `docs/decisions/adr/ADR-0030-*.md` |
| C7a | + Codec (9a): Compress / ByteEncode dan ByteDecode / Decompress | `mlkem_pack`, `mlkem_unpack` (d = 1, 4, 10, 12), Compress tanpa pembagian dengan konstanta dibuktikan pada semua 3.329 masukan; 256 koefisien dan 32·d byte per run | 9a | — | Blok | MEASURED: 299.0 / 41,910 median (seed 1-6: 298-299) | 192-193 | 0 / 553 | 2 / 112 | 105.630 (median seed 1-6, rentang 100.46-110.38) | terpenuhi pada 40.000 ns di setiap seed; 20 ns (seed 1) terpenuhi, +10.952 ns | pack 261 / 261 / 325 / 389 dan unpack 259 / 259 / 323 / 387 siklus per polinomial untuk d = 1 / 4 / 10 / 12 (simulasi, konstan) | tidak dinyatakan | tidak dinyatakan | `evidence/phase09/9a/selection_worksheet.md`, `evidence/phase09/9a/result_9a.md` |
| C7b | + Pembungkus hash dan pembanding FO (9b) | `mlkem_hash` (H, G, J pada word 64 bit; sponge C5) dan `mlkem_fo_cmp` (pembanding waktu konstan 136 beat, pemilihan mask K' atau K_bar) | 9b | C7a | Blok | MEASURED: 6,734.5 / 41,910 median (seed 1-6: 6,712-6,745); dengan sponge K0 4,221 (seed 1, informasi) | 1,976 | 0 / 553 | 0 / 112 | 50.625 (median seed 1-6, rentang 47.84-52.07) | terpenuhi pada 40.000 ns di setiap seed; 20 ns (seed 1) terpenuhi, +3.843 ns | G 30 / 33, H(ek) 282, J(z, c) 274 siklus (C5; K0 42 / 45 / 390 / 382), pembanding 137 (simulasi, konstan) | tidak dinyatakan | tidak dinyatakan | `evidence/phase09/9b/selection_worksheet.md`, `evidence/phase09/9b/result_9b.md` |
| C7-core | + Inti ML-KEM-768 di simulasi (9c): KeyGen, Encaps, Decaps | `mlkem_core`: pengendali micro-program, buffer dan register file, mesin K-PKE 8d, codec dan blok hash / FO; pemeriksaan masukan FIPS 203 di HPS (ADR 0031); semua vektor ACVP terpatok ML-KEM-768 lolos (keyGen 25, enkapsulasi 25, dekapsulasi 10) di kedua simulator | 9c | C6d + C7a + C7b | Operasi | MEASURED: 17,620.5 / 41,910 median (seed 1-6: 17,608-17,636) | 8,210-8,365 | 54 / 553 | 28 / 112 | 49.280 (median seed 1-6, rentang 47.64-51.74) | terpenuhi pada 40.000 ns di setiap seed; 20 ns (seed 1) terpenuhi, +4.419 ns | KeyGen 9,035-9,076 (25 seed ACVP), Encaps 10,691 (konstan untuk satu ek), Decaps 16,623 (konstan untuk satu ek: ciphertext valid atau ditolak, kunci rahasia apa pun) (simulasi) | KeyGen sekitar 184 us, Encaps sekitar 217 us, Decaps sekitar 337 us pada Fmax median timing statis, bukan pengukuran papan (perhitungan tim) | tidak dinyatakan | `evidence/phase09/9c/selection_worksheet.md`, `evidence/phase09/9c/result_9c.md`, `docs/results/phase09.md` |
| C6 | + Streaming | 8b / 8c / 8d: sub-baris C6b-W1, C6b-W2, C6c-STORE, C6c, C6d di atas (semua diukur 2026-10-03) | 8 | C5 + S1 | Operasi | — | — | — | — | — | — | — | — | — | — |
| C7 | Integrasi penuh | KEM lengkap (C7-core di simulasi; C7-soc di papan) | 9, 10 | C6 | Operasi / sistem | — | — | — | — | — | — | — | — | — | — |

Baris S1 dan K0 adalah titik acuan yang ditambahkan agar C5 dan C6 tetap berbeda satu perubahan. Siklus/op:
baris kernel melaporkan siklus per NTT, INTT dan perkalian titik; baris Keccak melaporkan siklus per permutasi
dan per panggilan hash; baris operasi melaporkan siklus per KeyGen, Encaps dan Decaps. Latensi memakai
clock terbatas yang memenuhi timing. Salinan akhir matriks ini yang terukur masuk ke
`evidence/phase11-benchmark/ablation_matrix.md`.

## Halaman proposal (sampul dan referensi tidak dihitung; batas 6 halaman)
- Halaman 1-3: Bagian 1-2 (sudah ditulis).
- Halaman 4-6: Bagian 3 "Proposed Chip Design" (diagram blok, daftar modul RTL, tabel sumber daya, alat,
  test plan, metrik keberhasilan). Belum ditulis. Sel sumber daya tetap `ESTIMATE` atau `[...]` sampai
  fase terkait menghasilkan evidence Quartus (nilai kernel mulai Fase 1, nilai inti penuh mulai Fase 9,
  nilai sistem mulai Fase 10); setiap angka menyebut file evidence-nya.
- Kesalahan templat yang harus dihindari: templat menyebut 415.000 flip-flop, sedangkan tabel Intel menyebut 166.036.
