<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Fase 9F langkah S1: sponge K0 di kedua tempat (instans hash dan sampler mesin) - test plan dan aturan adopsi

Ditulis 2026-10-04 sebelum perubahan RTL S1 apa pun dan sebelum kompilasi S1 apa pun. Lingkup: ADR 0036 (Accepted, Faza Dzil), langkah S1. Baseline: inti 9M-1 (`CODEC_W2 = 1`, C5 di mana-mana), laporan `../9m1/result_9m1.md`; laporan jalur kritis `../../critical_paths_MW.md` (semua 300 jalur terburuk pada 20 ns berada di dalam dua permutasi C5). Label: MEASURED, ESTIMATE, INFERENCE, perhitungan tim. Matematika terkunci (C1): K0 dan C5 menghitung Keccak-f[1600] yang sama; hanya ronde per siklus yang berbeda.

## 1. Apa yang berubah
- `rtl/mlkem/mlkem_core.sv`: satu parameter baru `SMP_C5` (bawaan 1) diteruskan ke `CORE_R2` mesin (kini ditulis sebagai konstanta `1'b1`). Pada nilai bawaan perilakunya persis seperti Fase 9 / 9M-1. File mesin (Fase 6-8, beku) tidak diedit: `kpke_smp_top_s10`, `kpke_sched_smp`, dan `keccak_sampler` sudah punya parameter `CORE_R2` (sampler K0 diverifikasi di Fase 8b; sequencer penuh dengan sampler K0 belum dijalankan di Fase 8c/8d: itulah yang ditambahkan V2 dan V3).
- Konfigurasi K1: `HASH_C5 = 0`, `SMP_C5 = 0`, `CODEC_W2 = 1` (instans hash K0 adalah butir 3).

## 2. Estimasi yang ditulis sebelum mengukur (ESTIMATE; sumber: siklus per polinomial 8b, siklus per hash 9b, area blok 8b dan 9b)
| Besaran | MW (C5, MEASURED) | K1 ESTIMATE |
|---|---|---|
| Siklus sampling di dalam satu operasi (perhitungan tim, 8b: KeyGen 2,770 -> 3,168, Encaps dan enkripsi ulang Decaps 2,922 -> 3,332) | | +398 (KeyGen), +410 (Encaps, Decaps), sebagian tersembunyi oleh tumpang tindih 8d |
| Siklus KeyGen / Encaps / Decaps (masukan profil) | 8,327 / 10,159 / 15,515 | sekitar 8,850 / 10,690 / 16,045 (hash +120 dan sampling sekitar +400 masing-masing, tanpa asumsi tersembunyi) |
| Median ALM | 17,654.0 | sekitar 13,400 (instans hash -2,513 dari 9b, sampler -1,739 dari 8b; +/- 500) |
| Register | 8,189-8,376 | sekitar -1,000 sampai -1,500 |
| Blok RAM / DSP | 54 / 28 | 54 / 28 |
| Fmax pada gerbang 40 ns (slow corner terendah, median) | 48.855 MHz | 52-60 MHz (permutasi Keccak keluar dari daftar kritis; batas berikutnya belum teridentifikasi) |
| Fmax pada batasan 15 ns (median, seed 1-6) | tidak diukur (S0 memberi baseline) | 62-70 MHz |
| Latensi pada Fmax batasan 15 ns | MW pada 20 ns: 8,327 / 10,159 / 15,515 siklus pada 63.990 MHz = 130.1 / 158.8 / 242.5 us | sekitar 126-143 / 153-172 / 229-259 us: sama dengan MW dalam rentang estimasi, tidak jelas lebih rendah |
Harapan yang jujur: Fmax lebih tinggi dan sekitar 4,200 ALM lebih sedikit, dengan latensi kira-kira sama dengan MW pada 20 ns karena siklus bertambah (ADR 0036 butir 2: aturan memakai latensi).

## 3. Test (kedua simulator; RTL repository tidak pernah dimutasi)
| # | Test | Syarat lulus |
|---|---|---|
| V1 | lint Verilator `-Wall` dan slang inti pada `SMP_C5 = 0`, `HASH_C5 = 0`, `CODEC_W2 = 1` dan pada nilai bawaan | 0 peringatan, 0 error |
| V2 | test sequencer Fase 8c/8d dengan sampler K0: `tb/smp/test_kpke_smp.py` (3 program bit-exact, counter, siklus konstan untuk rho tetap, cakupan stall PWMS, STRESS) dibangun dengan `CORE_R2 = 0` (env `KP_CORE_R2=0` di runner) | semua lulus, kedua simulator; kelas stall tercakup (sampler K0 lebih lambat: lebih banyak tunggu di PWMS) |
| V3 | inti pada `SMP_C5 = 0`, `HASH_C5 = 0`, `CODEC_W2 = 1`: seluruh target `core` 9c (ACVP keyGen 25, enkapsulasi 25, dekapsulasi 10, cross-check acak, rantai, protokol, siklus konstan) | 100 % sama, kedua simulator |
| V4 | profil (`tb/mlkem/profile_core.py`, masukan sama) pada K1 | dicatat; state RUN, HFD, dan HGT lebih panjang, setiap hitungan state lain sama dengan MW |
| V5 | kontrol bahwa sampler K0 benar-benar dipakai dan diuji: `nclen` pada K1 | `test_acvp_encaps` gagal, kedua simulator |
| V6 | formal: bukti sequencer 8c dan 8d (F1-F5) pada `CORE_R2 = 0` dengan stub protokol sampler (stub tidak bergantung pada sponge: INFERENCE; dijalankan untuk menunjukkan bukti berlaku pada nilai parameter) dan bukti pengendali 9c (tidak bergantung parameter) | seperti 8c/8d, SEMUA SESUAI HARAPAN |
| V7 | regresi pada nilai bawaan: `scripts/test/phase9c_verify.sh` dan profil sama dengan profil Fase 9 | PASS |
| V8 | Quartus: revisi K1 seed 1-6 pada 40.000 ns (gerbang) dan K1-15 seed 1-6 pada 15.000 ns (informasi, ADR 0036 butir 3), satu per satu, kernel-only | ekstrak; timing pada 40 ns terpenuhi di setiap seed; pada 15 ns: jumlah seed yang terpenuhi dan Fmax dilaporkan |
| V9 | klasifikasi jalur kritis K1 pada batasan paling ketat yang terpenuhi (skrip `scripts/quartus/phase5m_top_paths.tcl` pada salinan) | menyebut blok yang membatasi timing (masukan untuk S2) |

## 4. Parameter yang dilaporkan
ALM (median, min-maks, % dari denominator fitter, terhadap anggaran 20,000), register, blok RAM, bit memori blok, DSP, slack setup dan hold terburuk, timing terpenuhi per seed, Fmax slow corner terendah (median, min-maks) pada 40 ns dan 15 ns; siklus per operasi (masukan profil dan rentang ACVP); latensi t = siklus / median Fmax pada tiap batasan (perhitungan tim); jumlah ACVP; hasil formal; peringatan kritis; blok pembatas.

## 5. Aturan adopsi (ditetapkan sebelum mengukur; ADR 0036: menurut latensi)
K1 diadopsi sebagai konfigurasi Fmax tinggi / area kecil hanya bila semua berikut berlaku:
1. V1-V7 lulus seperti dinyatakan (ketidakcocokan ACVP apa pun menolaknya).
2. Timing terpenuhi pada 40.000 ns di setiap seed 1-6.
3. Median ALM paling banyak 20,000 (anggaran).
4. Untuk masing-masing KeyGen, Encaps, dan Decaps, t = siklus / median Fmax pada batasan 15 ns (seed 1-6, slow corner terendah) K1 paling banyak 3 % di atas latensi MW pada hasil 20 ns-nya (`../9m2/selection_worksheet.md`: 130.1 / 158.8 / 242.5 us).
5. Pada 15 ns timing terpenuhi di setiap seed 1-6 atau seed yang gagal disebut namanya dan Fmax dilaporkan untuk seed yang memenuhinya (pernyataannya lalu berbunyi "terpenuhi di k dari 6 seed").
Bila butir 4 gagal tetapi butir 1-3 berlaku, K1 dilaporkan sebagai konfigurasi yang lebih kecil, bukan lebih cepat dan tim memutuskan (ADR 0033 dan 0035 mendaftar pilihannya); latensi tidak pernah diklaim lebih rendah dari yang terukur. Hasilnya adalah ADR Proposed.

## 6. Bukan bagian langkah ini
Tanpa perubahan S2 (batas berikutnya hanya diidentifikasi, V9); tanpa hasil papan; tanpa klaim clock untuk DE10-Nano (keputusan PLL milik Fase 10); waktu-konstan berarti invarian jumlah siklus saja.

## 7. Amandemen A1 (2026-10-04, ditulis saat membangun; tidak ada di atas yang diedit dan aturan bagian 5 tidak berubah)
1. Modul baru, bukan mengedit `mlkem_core.sv`: bagian 1 berkata parameter `SMP_C5` ditambahkan ke `rtl/mlkem/mlkem_core.sv`. Kampanye Quartus S0 (`quartus/phase09f0_core`, sumber `mlkem_core.sv`) masih berkompilasi, dan sebuah edit akan mengubah apa yang dibaca revisi berikutnya. Parameter itu karenanya ditambahkan pada salinan, `rtl/mlkem/mlkem_core2.sv` (modul `mlkem_core2`; selisih dari `mlkem_core.sv`: nama modul, komentar header, parameter `SMP_C5` bawaan 1, dan `.CORE_R2(SMP_C5)` pada instans mesin). Pada `SMP_C5 = 1` ia adalah desain yang sama dengan `mlkem_core`. Revisi Quartus K1 memakai `mlkem_core2.sv`. S1b dibangun di atas file ini (ROM baru).
2. Skrip test: `tb/mlkem/run_core_tests.py` dan `profile_core.py` menerima `CORE_TOP=mlkem_core2` dan `CORE_SMP0=1`; `tb/smp/run_smp_tests.py` menerima `KP_CORE_R2`. Pada nilai bawaan mereka berperilaku seperti sebelumnya (V7 mengulang regresi bawaan).
3. `mlkem_core.sv` bawaan tetap tidak berubah; konfigurasi Fase 9 / 9M diukur seperti sebelumnya.
