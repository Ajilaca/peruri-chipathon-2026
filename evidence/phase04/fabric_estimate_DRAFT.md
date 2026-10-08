<!-- claim-lint: skip-file (internal planning draft, not proposal text; every number below is labelled) -->
# DRAFT - Estimasi isi fabric untuk Fase 5–10 (masukan untuk peninjauan anggaran ALM ADR 0004 / ADR 0008)

- Status: DRAFT untuk diskusi tim. Bukan keputusan, bukan persyaratan, bukan angka proposal.
- Tanggal (UTC): 2026-10-01. Ditulis atas permintaan tim setelah peninjauan anggaran ALM 25%.
- Setiap angka diberi label MEASURED (path ke laporan Quartus di repository ini) atau ESTIMATE (metode dan
  asumsi dinyatakan). Tidak ada angka yang diambil dari literatur: draft ini tidak punya sumber yang dikutip untuk blok
  mana pun yang belum ada. Bila angka yang dikutip akan membantu, barisnya menyatakannya.
- Keyakinan baris ESTIMATE rendah. Rentangnya sengaja lebar; maksudnya menunjukkan keputusan mana yang
  menggeser total, bukan memprediksinya.

## 1. Mengapa estimasi ini ada
ADR 0004 mencadangkan 75% perangkat untuk "Keccak, sampler, atau logika protokol yang berbagi fabric yang sama",
tetapi tidak pernah ditulis estimasi isi itu (peninjauan 2026-10-01). Anggaran untuk inti NTT saja
hanya masuk akal sebagai total tersedia − semua yang lain. Draft ini adalah percobaan pertama untuk "semua yang lain".

## 2. Kalibrasi dari pengukuran kami sendiri (MEASURED)
Sumber: `quartus/phase04_pipeline_c3/output_files_P4/C3-P4.fit.rpt`, "Fitter Resource Utilization by
Entity" (ringkasan yang diekstrak adalah `evidence/phase04/quartus_C3-P4.md`).

| Bagian C3-P4 (L = 8, P = 4) | ALM | Comb. ALUT | Register | DSP | Catatan |
|---|---|---|---|---|---|
| Seluruh inti | 10,439 | 13,047 | 4,145 | 9 | |
| `poly_mem_multiport_pipe` (256 × 12 bit, 8 bank, 16 port, penyimpanan flip-flop) | 7,621 | 8,019 | 3,660 | 0 | 73% inti |
| 8 × `butterfly_shared_pipe` (termasuk pengali + reducer staged) | ~2,097 (257–277 masing-masing) | ~3,862 | ~394 | 8 | |
| `modmul_reduce_staged` (pengali skala, sendirian) | 151 | 303 | 21 | 1 | satu pengali + reducer 13-stage |
| 8 × `twiddle_rom` | ~240 (30 masing-masing) | 288 | 0 | 0 | ROM 128 × 12 bit dalam logika |
| FSM, counter, pembangkit alamat (logika sendiri inti) | ~296 | 567 | 30 | 0 | |

Rasio yang dipakai di bawah (perhitungan tim dari baris di atas): ~1.25 ALUT kombinasional per ALM untuk gaya
desain ini; penyimpanan satu koefisien 12-bit dalam flip-flop dengan akses 16-port memakan ~30 ALM
(7,621 / 256). Rasio kedua adalah alasan teknologi penyimpanan mendominasi segalanya di Bagian 4.

## 3. Blok yang akan berbagi fabric (ESTIMATE kecuali ditandai)

| # | Blok (fase) | ALM rendah | ALM tinggi | M10K | DSP | Metode dan asumsi |
|---|---|---|---|---|---|---|
| 1 | Inti NTT/INTT C3-P4 (Fase 4) | 10,439 | 10,503 | 26 | 9 | MEASURED, seed 1–6, `evidence/phase04/seed_sweep.md` |
| 2 | Perubahan aritmetika Fase 5 (selisih terhadap baris 1) | −700 | +300 | 0 | 0 sampai +9 | ESTIMATE. Sembilan pengali+reducer sekitar 150 ALM masing-masing menurut baris "modmul_reduce_staged" (~1,350 total). Barrett/Montgomery dapat memindahkan sebagian reducer ke blok DSP (menghemat ALM) atau menambah logika koreksi (menambah ALM). Tanda tidak diketahui. |
| 3 | Perkalian base-case pointwise + penjadwal operasi (Fase 6) | 500 | 2,000 | 0–4 | 2–10 | ESTIMATE. Base case: 4–5 perkalian modular (masing-masing ~150 ALM menurut baris "modmul_reduce_staged", lebih sedikit bila dipetakan ke DSP) ditambah akumulasi; penjadwal adalah FSM / sequencer mikrokode, berukuran 1–5 × logika kendali inti sendiri (~300 ALM). |
| 4 | Keccak-f[1600], 1 ronde/siklus, sponge untuk SHA3/SHAKE (Fase 7, K0) | 3,000 | 5,000 | 0 | 0 | ESTIMATE, hitungan LUT prinsip-pertama: 1,600 register state (≥ 800 ALM pada 2 register/ALM, tidak mengikat); paritas kolom θ 320 × satu XOR 5-masukan; θ+ρ+π+χ per bit state butuh 9 masukan → ~2 level LUT → ~3,200 LUT; XOR absorb dan mux load/hold pada bagian rate (sampai 1,344 bit) ~1 LUT per bit; total ~5,000–6,500 ALUT → ÷ 1.25–1.7 ALUT/ALM. Angka yang dikutip untuk Keccak iteratif di Cyclone V akan menggantikan baris ini (belum ada di `docs/proposal/references.md`). |
| 5 | Keccak 2 ronde/siklus (Fase 8a, opsional) - selisih | +2,500 | +4,000 | 0 | 0 | ESTIMATE: salinan kedua logika ronde (baris 4 dikurangi state dan logika absorb). Hanya bila 8a diadopsi. |
| 6 | Sampler: SampleNTT (rejection, dari aliran XOF) + CBD η = 2 (Fase 8b) | 200 | 800 | 0–2 | 0 | ESTIMATE: ekstraksi field 12-bit dari aliran squeeze, dua perbandingan dengan q, counter kecil; CBD = hitungan bit pada 2 + 2 bit dan pengurangan mod q. Lebar antarmuka aliran adalah ketidakpastian utama. |
| 7 | Pengendali KEM tingkat atas: KeyGen / Encaps / Decaps (Fase 9) | 500 | 2,000 | 0–2 | 0 | ESTIMATE: FSM sequencing atau mikrokode dengan ROM kecil; berukuran 2–7 × logika kendali inti. |
| 8 | Encode/decode, compress/decompress tanpa pembagian (du = 10, dv = 4, d = 1) (Fase 9) | 500 | 2,000 | 0 | 0–4 | ESTIMATE: compress butuh perkalian dengan resiprokal konstan dan pembulatan per koefisien (≈ satu pengali konstan masing-masing, LUT atau DSP); pengepakan byte adalah jaringan shift/mux yang ukurannya bergantung pada lebar bus yang dipilih. |
| 9 | Transformasi FO: perbandingan ciphertext waktu-konstan (1,088 B) + pemilihan implicit-rejection (Fase 9) | 100 | 300 | 0 | 0 | ESTIMATE: perbandingan streaming dengan akumulator OR dan pemilihan 32-byte; enkripsi ulang memakai ulang baris 1–8. |
| 10 | Penyimpanan kunci dan polinomial (Fase 9), di M10K | 200 | 800 | 20 | 0 | ESTIMATE (hitungan adalah inferensi dari aliran data K-PKE, belum diinstrumentasi): ~20–30 polinomial hidup sekaligus (s, e, t̂, r, e1, e2, u, v, u′, v′ …; Â dibangkitkan on the fly menurut 8c) pada 3,072 bit masing-masing → satu M10K masing-masing (10,240 bit) ditambah dk (19,200 bit) dan ek (9,472 bit) → ~20–40 M10K dari 553; ALM hanya untuk logika alamat/port. |
| 10′ | Penyimpanan yang sama dalam flip-flop (alternatif baris 10) | lihat metode | - | 0 | 0 | ESTIMATE menurut rasio kalibrasi. Penyimpanan FF port-tunggal: 61,000–92,000 register untuk 20–30 polinomial (37–55% dari 166,036 register perangkat) ditambah multiplekser baca lebar - besar, tetapi tidak ditunjukkan mustahil. Penyimpanan FF multi-port seperti baris 1 (~30 ALM per koefisien): 20 polinomial ≈ 153,600 ALM, lebih dari perangkat. Didaftar untuk menunjukkan mengapa teknologi penyimpanan harus diputuskan sebelum Fase 9. |
| 11 | Pemeriksaan masukan FIPS 203 di perangkat keras (Fase 9, hanya bila tim menaruhnya di fabric) | 0 | 400 | 0 | 0 | ESTIMATE: pemeriksaan modulus = perbandingan streaming 768 koefisien dengan q; pemeriksaan hash memakai ulang Keccak. 0 bila dikerjakan di HPS (keputusan tim terbuka, ROADMAP Fase 9). |
| 12 | Bridge HPS, interkoneksi Platform Designer, CSR, counter siklus, crossing clock (Fase 10) | 300 | 2,000 | 0–4 | 0 | ESTIMATE. Dapat di-MEASURED sekarang tanpa papan dengan mengompilasi GHRD Intel DE10-Nano (`intel/de10-nano-hardware`, sudah dikutip di ADR 0006) dengan dan tanpa slave stub; itu akan menggantikan baris ini. Bergantung pada PENDING #3 (DMA atau memory-mapped). |
| 13 | SignalTap untuk bitstream demo (Fase 10) | 0 | 1,500 | 5–30 | 0 | ESTIMATE: bergantung pada jumlah sinyal yang disadap dan kedalaman sampel; ROADMAP membatasi tap pada sinyal kendali non-rahasia. Hanya build debug. |

## 4. Total (ESTIMATE, jumlah baris; persentase dari 41,910 ALM milik fitter)

| Skenario | ALM | % perangkat | Porsi inti NTT (baris 1) dari total |
|---|---|---|---|
| Rendah (baris 1–4, 6–12 pada "rendah"; tanpa 8a; tanpa SignalTap) | ~15,000 | ~36% | ~70% |
| Tinggi tanpa butir opsional (baris 1–4, 6–12 pada "tinggi") | ~26,100 | ~62% | ~40% |
| Tinggi dengan 8a dan SignalTap | ~31,600 | ~75% | ~33% |
| Skenario apa pun dengan penyimpanan FF multi-port (baris 10′) sebagai ganti baris 10 | > 41,910 | > 100% | - |

Aritmetika (perhitungan tim): rendah = 10,439 − 700 + 500 + 3,000 + 200 + 500 + 500 + 100 + 200 + 0 + 300 + 0 = 15,039;
tinggi = 10,503 + 300 + 2,000 + 5,000 + 800 + 2,000 + 2,000 + 300 + 800 + 400 + 2,000 = 26,103; ditambah 4,000 (8a) dan
1,500 (SignalTap) = 31,603. M10K tetap di bawah ~100 dari 553 di setiap skenario; DSP di bawah ~40 dari 112 (ESTIMATE).

## 5. Apa yang dikatakan dan tidak dikatakan estimasi ini
- Inti NTT mungkin blok tunggal terbesar, tetapi kemungkinan besar bukan mayoritas isi
  fabric akhir. Bagian "semua yang lain" berkisar dari ~4,600 sampai ~21,100 ALM (ESTIMATE) - faktor
  ~4.6 antar ujungnya. Sebaran itu, bukan pertanyaan 25-lawan-35%, adalah ketidakpastian utama.
- Teknologi penyimpanan menentukan kelayakan. Penyimpanan flip-flop multi-port untuk data tingkat-operasi (baris 10′) akan melampaui seluruh perangkat; penyimpanan M10K (baris 10) memakan beberapa ratus ALM. Memori kerja
  inti NTT sendiri (7,621 ALM, MEASURED) adalah butir tunggal terbesar di skenario rendah; apakah
  sebagian darinya dapat pindah ke M10K adalah celah terbuka Fase 2 (baca asinkron). C3 kini punya stage baca
  terregister, yang disebut ADR 0007 sebagai prasyarat M10K, tetapi memori butuh 2 baca + 2 tulis per bank per
  siklus dan M10K punya dua port - jadi ini tidak ditunjukkan mungkin (inferensi, bukan evidence).
- Anggaran inti NTT yang diturunkan dari angka ini adalah (total yang bersedia diisi tim) −
  (baris 2–13). Draft ini tidak mengusulkan "total yang bersedia diisi tim"; itu tetap keputusan
  tim (C5).
- Tidak ada di sini yang merupakan klaim tentang routing, timing, atau muat tidaknya sistem terintegrasi. Hanya kompilasi sistem penuh
  (inti Fase 9, SoC Fase 10) yang mengukurnya.

## 6. Cara mengganti estimasi dengan evidence (termurah dulu)
1. Baris 12 - kompilasi GHRD DE10-Nano di Quartus 25.1std (tanpa papan): ALM / M10K MEASURED
   shell sistem HPS dan interkoneksinya.
2. Baris 4 - acuan yang dikutip untuk Keccak-f[1600] iteratif di Cyclone V (tambahkan ke `references.md`), dan
   nanti kompilasi K0 Fase 7 itu sendiri.
3. Baris 10 / 10′ - putuskan lebih awal bahwa penyimpanan tingkat-operasi berbasis M10K (masukan desain Fase 6/9),
   dan periksa apakah sebagian memori kerja NTT dapat berupa M10K.
4. Baris 7–9 - sketsa tingkat-blok datapath Fase 9 (lebar bus, unit mana yang dibagi) untuk mempersempit
   rentang 500–2,000.
5. Jalankan ulang tabel ini setelah masing-masing di atas; jaga label setiap baris tetap jujur (ESTIMATE → MEASURED).
