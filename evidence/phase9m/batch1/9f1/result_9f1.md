<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Laporan Fase 9F langkah S1: sampler K0 dan hash K0 (konfigurasi K1)

- Status: SELESAI (STOP setelah langkah, ADR 0036; S1b menyusul di batch yang sama, `../9f1b/`). Branch `phase9m-optimisation`, belum di-commit. RTL: modul baru `rtl/mlkem/mlkem_core2.sv` (salinan `mlkem_core.sv` dengan parameter `SMP_C5`; amandemen A1 rencana). Rencana dan aturan: `test_plan_9f1.md` (ditulis sebelum RTL dan kompilasi). Timing statis kernel-only dengan virtual pin; bukan sistem di papan. Dua belas kompilasi Quartus, semuanya `rc=0`.

## 1. Hasil
K1 lebih kecil, belum jelas lebih cepat. Menurut aturan rencana (bagian 5, ditetapkan sebelum mengukur) K1 diadopsi: test lulus, timing terpenuhi pada 40 ns di 6 dari 6 seed, median ALM 14,061.0 jauh di bawah anggaran 20,000, dan latensi pada 15 ns 7.5-9.8 % di bawah acuan yang dipilih di rencana (MW pada 20 ns). Tetapi S0 kemudian mengukur inti 9M-1 (MW) pada 15 ns dan menemukan 73.6 MHz; terhadap MW pada batasan 15 ns yang sama K1 lebih lambat 3-6 % (lebih banyak siklus, Fmax sama). Acuan aturan ditetapkan sebelum S0 ada; saya melaporkan keduanya dan tidak mengklaim K1 lebih cepat. Yang diberikan K1 adalah 3,593 ALM lebih sedikit (-20 %) dengan Fmax tidak berubah: penghalang desain adalah inti NTT / memori (bagian 4), bukan permutasi Keccak.

## 2. Parameter yang diukur (MEASURED; `selection_worksheet.md`, ekstrak `quartus_K1*.md`)
| Parameter | MW (9M-1: sampler dan hash C5) | K1 (sampler dan hash K0) | Selisih |
|---|---|---|---|
| Median ALM, 40 ns, seed 1-6 (min-maks) | 17,654.0 (17,641-17,683) | 14,061.0 (14,002-14,108) | -3,593.0 (-20.4 %) |
| ALM dalam % dari 41,910 fitter | 42 % | 34 % | |
| Register, 40 ns | 8,189-8,376 | 8,348-8,452 | hampir sama (K0 menghemat ALM, bukan register) |
| Blok RAM / DSP, 40 ns | 54 / 28 | 54 / 28 | 0 |
| Timing terpenuhi pada 40.000 ns | 6 dari 6 | 6 dari 6 | |
| Slack setup terburuk atas seed, 40 ns | +18.655 ns | +19.063 ns | |
| Fmax slow corner terendah, 40 ns, median (min-maks) | 48.855 MHz (46.85-52.15) | 51.765 MHz (47.76-53.40) | +2.9 MHz |
| Median ALM pada 15 ns | 17,948.5 (S0, 2 seed) | 14,211.5 (14,173-14,273, 6 seed) | -3,737.0 |
| Blok RAM pada 15 ns | 53 | 53 | |
| Timing terpenuhi pada 15.000 ns | 2 dari 2 seed (S0) | 6 dari 6 seed | |
| Slack setup terburuk pada 15 ns | +1.363 ns | +1.114 ns | |
| Fmax slow corner terendah pada 15 ns, median (min-maks) | 73.635 MHz (73.33-73.94, 2 seed) | 73.070 MHz (72.01-74.10, 6 seed) | -0.57 MHz, di dalam sebaran |
| Siklus KeyGen / Encaps / Decaps (masukan profil; simulasi) | 8,327 / 10,159 / 15,515 | 8,795 / 10,627 / 15,983 | +468 masing-masing (+5.6 %, +4.6 %, +3.0 %) |
| Latensi pada 15 ns (perhitungan tim; MW: Fmax lebih rendah dari 2 seed, K1: median dari 6) | 113.6 / 138.5 / 211.6 us | 120.4 / 145.4 / 218.7 us | +6.0 %, +5.0 %, +3.4 % |
| Acuan latensi aturan: MW pada 20 ns (median dari 6, 9M-2) | 130.1 / 158.8 / 242.5 us | K1 pada 15 ns 120.4 / 145.4 / 218.7 us | -7.5 %, -8.4 %, -9.8 % |
| Peringatan kritis per kompilasi | 1 | 1 | |
Detail siklus (profil, `profile_k1_verilator.json` lawan profil hash-K0 9M-3): hanya RUN yang berubah terhadap inti hash-K0, +348 per operasi; terhadap MW hash K0 menambah +120 (HFD +96, HGT +24, 9M-3) dan sampler K0 +348 (test mesin memberi +336: KeyGen 6,352 -> 6,688, Encrypt 7,653 -> 7,989; Decrypt tidak berubah).
Median Fmax pada 15 ns untuk K1 adalah median enam seed, untuk MW yang lebih rendah dari dua (S0): perbandingan bersifat indikatif, bukan setara.

## 3. Test (MEASURED)
| # | Hasil | Evidence |
|---|---|---|
| V1 lint | `verilator --lint-only -Wall` `mlkem_core2` pada K1 dan nilai bawaan: rc 0, tanpa peringatan; `slang`: 0 error, 0 peringatan (dijalankan saat build; keluaran tidak disimpan) | laporan ini |
| V2 test sequencer dengan sampler K0 (`KP_VAR=2 KP_CORE_R2=0`): 3 program bit-exact, siklus konstan untuk rho tetap, cakupan stall | 3/3 lulus di Verilator dan Icarus | `sim_verilator.md`, `sim_icarus.md`, `cycles_smp_v2_*` |
| V3 ACVP inti pada K1: keyGen 25, enkapsulasi 25, dekapsulasi 10, cross-check acak (20), rantai, protokol, siklus konstan | 6/6 lulus di Verilator dan Icarus | file yang sama |
| V4 profil | hanya RUN yang lebih panjang; setiap hitungan state lain sama dengan inti hash-K0 | `profile_k1_verilator.json` |
| V5 kontrol `nclen` pada K1 | `test_acvp_encaps` gagal seperti disyaratkan, kedua simulator | file yang sama |
| V6 formal: bukti sequencer Fase 8d pada `CORE_R2 = 0` | PASS, kontrol NC-F2 FAIL seperti disyaratkan; lemah: sampler adalah stub protokol yang mengabaikan `CORE_R2`; sampler K0 nyata dicakup V2 / V3 dan bukti Fase 8b (INFERENCE) | `formal.md` |
| V7 regresi pada nilai bawaan | `run_core_tests.py verilator core` 6/6 lulus; profil bawaan `mlkem_core` dan `mlkem_core2` (SMP_C5 = 1, HASH_C5 = 1, CODEC_W2 = 0) sama dengan profil Fase 9 (9,095 / 10,735 / 16,667); hanya Verilator (skrip Fase 9 `phase9c_verify.sh` tidak dijalankan ulang: tidak ada file RTL Fase 9 yang berubah di S1) | `regression_default.md` |
| V8 Quartus | K1 seed 1-6 pada 40 ns dan K1-15 seed 1-6 pada 15 ns, semuanya `rc=0`; 40 ns terpenuhi 6 dari 6, 15 ns terpenuhi 6 dari 6 | `quartus_K1*.md` |
| V9 jalur kritis K1 pada 15 ns (K1-15-s4, slack terkecil) | semua 300 jalur terburuk di kelas inti NTT / memori / PWM (+1.114 .. +2.447 ns) | `critical_paths_K1-15.md` |
Siklus konstan (V3): Encaps 10,571 dan Decaps 15,927 identik di semua masukan yang diuji (angka rentang ACVP); KeyGen atas seed ACVP 8,723-8,776 (rejection sampling publik A, seperti sebelumnya).

## 4. Temuan
1. Permutasi C5 bukan satu-satunya penghalang. Dengan K0 di kedua tempat tidak ada jalur Keccak di antara 300 terburuk pada 15 ns; jalur terburuk semuanya di kelas inti NTT / memori / PWM (S0 telah menunjukkannya dalam 0.2 ns dari permutasi pada 13 ns). Jadi Fmax tetap sekitar 73 MHz (slow corner terendah pada 15 ns) dan S1 membayar +468 siklus untuk area yang dihematnya.
2. Area: -3,593 ALM (-20 %) pada 40 ns. Register tidak turun. Dengan S1 inti memakai 34 % perangkat, bukan 42 %.
3. Apa artinya bagi rencana (ADR 0036): S1 membuat ruang (ALM 14,061 dari anggaran 20,000) tetapi tidak menaikkan Fmax. Tuas Fmax berikutnya adalah kelas NTT / memori (S2); S1b mengembalikan sekitar 390 siklus per operasi (`../9f1b/`).
4. Pembacaan jujur atas aturan: aturan berkata adopsi; perbandingan S0 berkata K1 adalah konfigurasi lebih kecil dengan latensi 3-6 % lebih banyak daripada MW pada batasan yang sama. Tim memutuskan (ADR 0033, 0035, 0037 mendaftar pilihan terkait).

## 5. Estimasi lawan pengukuran (ditulis di rencana sebelum pengukuran)
- Siklus sekitar 8,850 / 10,690 / 16,045: terukur 8,795 / 10,627 / 15,983 (-0.6 %, -0.6 %, -0.4 %): di dalam akurasi ESTIMATE.
- Siklus sampling +398 / +410 / +410: terukur +348 (RUN): lebih rendah dari estimasi (sebagian tersembunyi oleh tumpang tindih 8d).
- ALM sekitar 13,400 +/- 500: terukur 14,061: di luar (161 di atas batas atas); penghematan kedua sponge bersama sekitar 3,590, bukan sekitar 4,250.
- Register -1,000 sampai -1,500: tidak terpenuhi (hampir sama).
- Fmax pada 40 ns 52-60 MHz: 51.765 MHz: sedikit di bawah rentang. Fmax pada 15 ns 62-70 MHz: 73.07 MHz: di atas rentang (S0 telah menunjukkan inti dasar sudah mencapai 73.6 MHz).
- Latensi pada 15 ns 126-143 / 153-172 / 229-259 us: terukur 120.4 / 145.4 / 218.7 us: KeyGen dan Decaps di bawah rentang, Encaps di dalam.
- Timing pada 40 ns terpenuhi di setiap seed: terpenuhi. Blok RAM 54 dan DSP 28: terpenuhi pada 40 ns (53 pada 15 ns, seperti di S0).

## 6. Yang tidak ditunjukkan ini
Tidak ada hasil papan; tidak ada klaim kecepatan terhadap perangkat lunak; timing statis kernel-only dengan virtual pin; pohon clock DE10-Nano, PLL, dan HPS tidak ada di kompilasi ini; waktu-konstan berarti invarian jumlah siklus saja; ACVP adalah simulasi.

## 7. File
`test_plan_9f1.md` (dengan amandemen A1), `selection_worksheet.md`, `sim_verilator.md`, `sim_icarus.md`, `formal.md`, `regression_default.md`, `critical_paths_K1-15.md`, `profile_k1_verilator.json`, `cycles_*_k1_*.json`, dua belas ekstrak `quartus_K1*.md`, `quartus/phase09f1_core/` (dua belas revisi, `run_k1.sh`), `scripts/quartus/select_9f1.py`, `scripts/quartus/classify_paths_9f.py`, `formal/run/run_formal_phase9f1.py`, `formal/phase09m-optimisation/9f1/`.
