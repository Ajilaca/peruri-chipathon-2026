<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Laporan Fase 9F langkah S2: register setelah reducer Barrett di inti NTT (P = 5 -> 6, konfigurasi K2)

- Status: SELESAI (STOP setelah langkah, ADR 0036). Branch `phase9m-optimisation`, belum di-commit saat penulisan. RTL: parameter `P6` pada `rtl/ntt/ntt_core_s10_p5.sv` (potongan pengali keempat, bit `MUL_REG` 3), diteruskan oleh `NTT_P6` pada `kpke_smp_top_s10` dan `mlkem_core3`; semua bawaan 0 (amandemen A1: tanpa file pembungkus baru). Rencana dan aturan: `test_plan_9s2.md` (ditulis sebelum RTL dan kompilasi). Timing statis kernel-only dengan virtual pin; bukan sistem di papan. Dua belas kompilasi Quartus, semuanya `rc=0`; percobaan pertama kompilasi 15 ns dalam dua salinan paralel dimatikan oleh crash editor dan tidak ada keluarannya yang dipakai.

## 1. Hasil
Aturan rencana mengadopsi K2, tetapi S2 tidak memberi kenaikan Fmax yang terukur. Register bekerja sesuai desain: jalur reducer-ke-memori yang membatasi K1b (+1.170 ns, 182 dari 300 jalur terburuk) berada di +2.349 ns pada K2. Tetapi jalur lain sudah ada di belakangnya, counter layer lewat aritmetika alamat stage issue ke port memori (+1.910 ns di K1b, +1.404 ns pada seed K2 yang dianalisis), dan kini ia yang membatasi K2. Median Fmax pada 15 ns: 74.125 MHz lawan 73.855 MHz milik K1b (+0.27 MHz), di dalam sebaran seed (K2 3.38 MHz, K1b 2.94 MHz); seed terendah K2 72.65 MHz di bawah tertinggi K1b 74.40 MHz. Latensi pada 15 ns 0.2 % lebih rendah untuk ketiga operasi (lebih banyak siklus, Fmax sama): itu di bawah derau seed dan tidak dilaporkan sebagai kenaikan. Area tidak berubah dalam sebaran (median ALM -122.0 pada 40 ns, -85.5 pada 15 ns). ESTIMATE rencana (Fmax 76 sampai 80 MHz) tidak terpenuhi.

## 2. Parameter yang diukur (MEASURED; `selection_worksheet.md`, ekstrak `quartus_K2*.md`, `../../batch1/9f1b/quartus_K1b*.md`)
| Parameter | K1b | K2 | Selisih |
|---|---|---|---|
| Median ALM, 40 ns, seed 1-6 (min-maks) | 14,335.0 (14,329-14,376) | 14,213.0 (14,171-14,235) | -122.0 |
| Median ALM pada 15 ns | 14,435.0 (14,390-14,459) | 14,349.5 (14,301-14,454) | -85.5 |
| Register, 40 ns / 15 ns | 8,211-8,258 / 8,213-8,276 | 8,327-8,375 / 8,343-8,430 | sekitar +120 |
| Blok RAM / DSP | 54 / 28 (53 pada 15 ns) | 54 / 28 (53 pada 15 ns) | 0 |
| Timing terpenuhi pada 40.000 ns | 6 dari 6 | 6 dari 6 | |
| Slack setup terburuk, 40 ns (semua corner) | +18.043 ns | +20.136 ns | |
| Timing terpenuhi pada 15.000 ns | 6 dari 6 | 6 dari 6 | |
| Slack setup terburuk, 15 ns (semua corner) | +1.007 ns | +1.236 ns | |
| Fmax slow corner terendah pada 15 ns, median (min-maks) | 73.855 MHz (71.46-74.40) | 74.125 MHz (72.65-76.03) | +0.270 MHz, di dalam sebaran |
| Fmax pada 40 ns, median | 51.730 MHz | 52.055 MHz | +0.325 MHz |
| Siklus per transformasi (NTT, INTT; test inti) | 118 | 119 | +1 |
| Siklus KeyGen / Encaps / Decaps (masukan profil; simulasi) | 8,404 / 10,236 / 15,597 | 8,416 / 10,250 / 15,619 | +12 / +14 / +22 |
| Latensi pada 15 ns (median Fmax; perhitungan tim) | 113.8 / 138.6 / 211.2 us | 113.5 / 138.3 / 210.7 us | -0.22 % / -0.23 % / -0.22 % |
| Latensi pada 15 ns (Fmax terendah dari 6) | 117.6 / 143.2 / 218.3 us | 115.8 / 141.1 / 215.0 us | |
| Peringatan kritis per kompilasi | 1 | 1 | peringatan clock virtual pin di setiap kompilasi kernel-only |
Detail siklus: hanya hitungan RUN yang berubah (+12 / +14 / +22 = 2 per transformasi untuk 6 / 7 / 11 transformasi). INFERENCE untuk penyebabnya (tidak diukur terpisah): satu siklus hold-off `hw_q` setelah tulis host terakhir sebelum start, dan satu siklus drain, keduanya ditetapkan oleh `Pipe`.

## 3. Test (MEASURED, simulasi dan formal; `sim.md`, `formal.md`)
| # | Hasil | Evidence |
|---|---|---|
| V1 lint | `verilator --lint-only -Wall` `mlkem_core3` (parameter K1b) pada `NTT_P6` 0 dan 1 serta `kpke_smp_top_s10` pada 1: rc 0, tanpa peringatan; `slang`: 0 error, 0 peringatan (dijalankan saat build; keluaran tidak disimpan sebagai file) | laporan ini |
| V2-V4 inti NTT dan memori pada P = 6 | memori 4/4; inti 6/6 NTT dan INTT bit-exact, tepat 119 / 119 siklus, 0 stall; kontrol NC-M dan NC-W gagal seperti disyaratkan; Verilator dan Icarus, 12/12 masing-masing | `sim.md` |
| V5 formal | bukti kendali S10 pada P = 6 (H, O, R, A, B, C): PASS; NC-O dan NC-A FAIL seperti disyaratkan | `formal.md` |
| V6 test sequencer, `NTT_P6 = 1` | 3/3 program bit-exact, siklus konstan; kontrol `nchaz` gagal seperti disyaratkan; kedua simulator | `sim.md` |
| V7 ACVP inti pada K2 | keyGen 25, enkapsulasi 25, dekapsulasi 10 sama; 20 kasus acak sama; rantai, protokol, siklus konstan lulus; Verilator 9/9 (dengan kontrol `nclen`, `ncoff`, `ncrom` seperti disyaratkan), Icarus 7/7 | sama |
| V8 regresi bawaan | profil `NTT_P6 = 0` 8,404 / 10,236 / 15,597 (= K1b); bawaan `mlkem_core` 9,095 / 10,735 / 16,667 (= Fase 9); `run_s10_tests.py` bawaan 13/13 dengan 118 / 118; `run_core_tests.py core` 6/6 (hanya Verilator) | sama, `profile_*.json` |
| V9 Quartus | K2 seed 1-6 pada 40 ns dan K2-15 seed 1-6 pada 15 ns, semuanya `rc=0`; terpenuhi pada 40 ns 6 dari 6, pada 15 ns 6 dari 6 | `quartus_K2*.md` |
| V10 jalur kritis K2-15-s5 | terburuk +1.404 ns: counter layer ke port memori; reducer ke memori kini +2.349 ns | `critical_paths_K2-15.md` |
Siklus konstan (V7): Encaps 10,194 dan Decaps 15,563 identik di semua masukan yang diuji (K1b 10,180 dan 15,541); KeyGen atas seed ACVP 8,344-8,397 (rejection sampling publik A, seperti sebelumnya).

## 4. Aturan rencana (bagian 5), diterapkan pada file
1. V1-V8 lulus: terpenuhi.
2. Timing pada 40 ns di setiap seed: terpenuhi (6 dari 6).
3. Median ALM paling banyak 20,000: terpenuhi (14,213.0).
4. Latensi tiap operasi lebih rendah dari K1b pada 15 ns (siklus / median Fmax): terpenuhi menurut angka (-0.22 %, -0.23 %, -0.22 %).
5. Seed yang terpenuhi pada 15 ns dilaporkan: 6 dari 6 (K1b 6 dari 6).
Pernyataan yang disyaratkan aturan: kenaikan Fmax (+0.270 MHz) tidak lebih besar dari sebaran seed, jadi tidak disebut kenaikan. Aturan mengadopsi; evidence berkata langkah ini netral. Tim memutuskan (ADR 0041 Proposed).

## 5. Estimasi lawan pengukuran (ditulis di rencana sebelum pengukuran)
- Siklus per transformasi 119: terpenuhi (terukur 119 / 119). Siklus operasi +6 / +7 / +11: meleset, terukur +12 / +14 / +22 (rencana menghitung satu siklus per transformasi; hold-off dan drain masing-masing menambah satu, INFERENCE).
- ALM +0 sampai +250: meleset ke arah lain (-122.0 pada 40 ns, -85.5 pada 15 ns; di dalam sebaran seed; fitter menghapus bit tak terpakai vektor stage reducer 37-bit, INFERENCE). Register +250 sampai +450: tidak terpenuhi (sekitar +120).
- Fmax pada 15 ns 76 sampai 80 MHz: meleset, 74.125 MHz. Rencana berkata kelas berikutnya berada 0.7 sampai 1.1 ns di belakang jalur terburuk K1b; itu berlaku untuk jalur reducer, tetapi kelas counter layer (+1.910 ns di K1b) adalah yang pertama di belakangnya dan kini menjadi penghalang, dan pada seed K2 ia berada di +1.404 .. sekitar +1.8 ns.
- Latensi 104-111 / 127-135 / 194-206 us: meleset, 113.5 / 138.3 / 210.7 us.

## 6. Temuan
1. Jalur reducer-ke-memori bukan lagi penghalang (+1.170 -> +2.349 ns): efek yang dimaksud nyata dan terukur pada tingkat jalur.
2. Penghalang berikutnya adalah jalur alamat stage issue: `layer_q` (dan `mode_q`) lewat `log2len`, `len`, shift untuk blok dan posisi, dan peta bank ke alamat M10K dan port tulis. Ia sudah ada di K1b pada +1.910 ns. Ia aritmetika kombinasional pada nilai yang berubah sekali per layer (setiap 16 siklus pada L = 8), jadi dapat diregister tanpa perubahan jadwal (INFERENCE; ini kandidat untuk langkah S2b dengan rencana dan aturan sendiri, tidak dilakukan di sini).
3. Biaya S2: +12 / +14 / +22 siklus (+0.14 % siklus KeyGen, Encaps, dan Decaps) dan sekitar +120 register; ALM tidak berubah.
4. S2 sendirian tidak menaikkan Fmax desain; apakah ia menaikkannya bersama S2b tidak diukur.

## 7. Yang tidak ditunjukkan ini
Tidak ada hasil papan; tidak ada klaim kecepatan terhadap perangkat lunak; timing statis kernel-only dengan virtual pin; derau seed sekitar 3 MHz membatasi pernyataan di bawah ukuran itu; waktu-konstan berarti invarian jumlah siklus saja; ACVP adalah simulasi. Satu seed (K2-15-s5) dianalisis untuk jalurnya.

## 8. File
`test_plan_9s2.md` (dengan amandemen A1), `selection_worksheet.md`, `sim.md`, `formal.md`, `critical_paths_K2-15.md`, `profile_k2_verilator.json`, `profile_k1b_default_verilator.json`, `profile_default_verilator.json`, `cycles_*_k2_*.json`, dua belas ekstrak `quartus_K2*.md`, `quartus/phase09s2_core/` (dua belas revisi, `run_k2.sh`, `run_k2_15.sh`), `scripts/quartus/select_9s2.py`, `formal/run/run_formal_phase9s2.py`, `formal/phase09m-optimisation/9s2/`, runner test yang berubah `tb/s10/run_s10_tests.py`, `tb/smp/run_smp_tests.py`, `tb/mlkem/run_core_tests.py`.
