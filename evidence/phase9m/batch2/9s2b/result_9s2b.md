<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Laporan Fase 9F langkah S2b: alamat issue terregister di inti NTT/INTT (konfigurasi K3)

- Status: SELESAI (STOP setelah langkah). Branch `phase9m-optimisation`, belum di-commit saat penulisan. RTL: parameter `AREG` (bawaan 0) pada `rtl/ntt/ntt_core_s10.sv`, diteruskan oleh pembungkus `ntt_core_s10_p5`, `NTT_AR` pada `kpke_smp_top_s10`, `kpke_smp_top_s10o`, dan `mlkem_core3` / `mlkem_core4` (semua bawaan 0). Rencana dan aturan: `test_plan_9s2b.md` (ditulis sebelum RTL dan kompilasi; amandemen A1: gerbang 40 ns tetap; A2: tiga seed tambahan dipilih setelah enam seed). Baseline K2 (`../9s2/`, `NTT_P6 = 1`). Timing statis kernel-only dengan virtual pin; bukan sistem di papan. Lima belas kompilasi Quartus (enam pada 15 ns, enam pada 40 ns, tiga seed tambahan pada 15 ns), semuanya `rc=0`, satu per satu (percobaan paralel pertama dimatikan oleh crash editor dan tidak ada keluarannya yang dipakai; satu run dihentikan karena salah dan dimulai ulang, lihat A1).

## 1. Hasil
Menurut aturan sebagaimana tertulis K3 TIDAK diadopsi, tetapi data menunjukkan kenaikan median. Alamat issue terregister bekerja sesuai desain: kelas `layer_q`-ke-port-memori K2 (+1.404 ns) hilang dari 300 jalur terburuk seed terlemah. Median Fmax pada 15 ns, enam seed: 77.555 MHz lawan 74.125 MHz milik K2 (+3.430 MHz); lima dari enam seed K3 (77.32-79.37 MHz) berada di atas setiap seed K2 (maksimum 76.03 MHz). Butir aturan 5 (kenaikan lebih besar dari sebaran seed yang lebih besar, atau seed terendah K3 di atas tertinggi K2) tidak terpenuhi sebagaimana tertulis: sebaran K3 adalah 6.35 MHz, lebih besar dari kenaikan, dan seed 4 (73.02 MHz) di bawah seed tertinggi K2. Tiga seed tambahan (amandemen A2; dipilih setelah melihat hasil, dilaporkan di sampingnya, tidak ada yang dibuang) memberi median sembilan seed 77.320 MHz (72.80-79.37), 6 dari 9 seed di atas seed tertinggi K2. Latensi pada 15 ns (siklus / median Fmax, perhitungan tim): 108.5 / 132.2 / 201.4 us lawan 113.5 / 138.3 / 210.7 us milik K2 (-4.4 % untuk ketiganya; siklus sama). Penyebab seed rendah ditemukan kemudian di laporan jalur K4: suku `start_go` S2b (bagian 6, INFERENCE untuk K3 sendiri).

## 2. Parameter yang diukur (MEASURED; `selection_worksheet.md`, ekstrak `quartus_K3*.md`, K2 dari `../9s2/`)
| Parameter | K2 | K3 | Selisih |
|---|---|---|---|
| Parameter | `NTT_P6 = 1`, `NTT_AR = 0` | `NTT_P6 = 1`, `NTT_AR = 1` | alamat stage issue (`j_r`, `jlen_r`: 8 lajur x 2 x 8 bit = 128 register) dihitung satu siklus lebih awal dan diregister |
| Median ALM, 40 ns, seed 1-6 (min-maks) | 14,213.0 (14,171-14,235) | 14,115.5 (14,081-14,153) | -97.5 |
| Median ALM pada 15 ns | 14,349.5 (14,301-14,454) | 14,293.0 (14,139-14,359) | -56.5 |
| Register, 40 ns / 15 ns | 8,327-8,375 / 8,343-8,430 | 8,462-8,508 / 8,400-8,472 | sekitar +40 sampai +135 |
| Blok RAM / DSP | 54 / 28 (53 pada 15 ns) | 54 / 28 (53 pada 15 ns) | 0 |
| Timing terpenuhi pada 40.000 ns | 6 dari 6 | 6 dari 6 | |
| Slack setup terburuk, 40 ns / 15 ns (semua corner) | +20.136 ns / +1.236 ns | +20.302 ns / +1.305 ns | |
| Timing terpenuhi pada 15.000 ns | 6 dari 6 | 6 dari 6 (9 dari 9 dengan seed tambahan) | |
| Fmax slow corner terendah pada 15 ns, median (min-maks) | 74.125 MHz (72.65-76.03) | 77.555 MHz (73.02-79.37); sembilan seed 77.320 (72.80-79.37) | +3.430 MHz (enam seed) |
| Fmax pada 40 ns, median | 52.055 MHz | 51.760 MHz | tidak dipakai |
| Siklus per transformasi (NTT, INTT) | 119 | 119 | 0 |
| Siklus KeyGen / Encaps / Decaps (masukan profil) | 8,416 / 10,250 / 15,619 | 8,416 / 10,250 / 15,619 | 0 |
| Latensi pada 15 ns (median Fmax; perhitungan tim) | 113.5 / 138.3 / 210.7 us | 108.5 / 132.2 / 201.4 us | -4.42 % untuk ketiganya |
| Latensi pada 15 ns (Fmax terendah dari 6) | 115.8 / 141.1 / 215.0 us | 115.3 / 140.4 / 213.9 us | |
| Peringatan kritis per kompilasi | 1 | 1 | peringatan clock virtual pin di setiap kompilasi kernel-only |
Fmax seed K3 pada 15 ns: s1 77.71, s2 79.28, s3 77.40, s4 73.02, s5 77.32, s6 79.37, s7 77.03, s8 75.47, s9 72.80 MHz. Denominator fitter: 41,910 ALM, 553 blok RAM, 112 DSP: K3 memakai sekitar 34 % ALM, 28 DSP.

## 3. Test (MEASURED; `sim.md`, `formal.md`)
| # | Hasil | Evidence |
|---|---|---|
| V1 lint | Verilator `-Wall` dan slang pembungkus, `kpke_smp_top_s10`, dan `mlkem_core3` pada `NTT_AR` 0 dan 1: tanpa peringatan, tanpa error (dijalankan saat build; keluaran tidak disimpan sebagai file) | laporan ini |
| V2, V3 inti NTT pada P = 6 dengan `AREG = 1` | 6/6 NTT dan INTT bit-exact, tepat 119 / 119 siklus, 0 stall, Verilator dan Icarus; kontrol NC-A1 (`ncar`, alamat diambil satu siklus terlambat) gagal seperti disyaratkan di keduanya | `sim.md` |
| V4 formal | bukti kendali S10 pada P = 6 dengan `AREG = 1` (H, O, R, A, B, C): PASS (base case dan induksi); NC-O dan NC-A FAIL seperti disyaratkan | `formal.md` |
| V5 test sequencer, `NTT_P6 = 1`, `NTT_AR = 1` | 3/3 program bit-exact, siklus konstan; kontrol `nchaz` gagal seperti disyaratkan; kedua simulator | `sim.md` |
| V6 inti K3 | ACVP keyGen 25, enkapsulasi 25, dekapsulasi 10 sama; 20 kasus acak sama; rantai, protokol, siklus konstan lulus; Verilator 9/9 (dengan `nclen`, `ncoff`, `ncrom` seperti disyaratkan), Icarus 7/7; siklus identik dengan K2 (Encaps 10,194, Decaps 15,563) | sama |
| V7 regresi bawaan | profil `NTT_AR = 0` sama dengan K2 dan K1b; `run_s10_tests.py` bawaan 13/13 dengan 118 / 118; `mlkem_core` bawaan 6/6; formal `mlkem_core3` (9f1b) masih dielaborasi dengan parameter stub | sama, `../9s2/` |
| V8 Quartus | K3 seed 1-6 pada 40 ns, K3-15 seed 1-6 pada 15 ns, seed tambahan 7-9 pada 15 ns: semuanya `rc=0`; terpenuhi 6 dari 6 pada 40 ns dan 9 dari 9 pada 15 ns | `quartus_K3*.md` |
| V9 jalur kritis K3-15-s4 | terburuk +1.666 ns (slow 100 C): delay posisi-baca ke reducer Barrett (144 jalur) dan delay operand-samping ke M10K (126 jalur); kelas `layer_q` K2 hilang | `critical_paths_K3-15.md` |

## 4. Aturan rencana (bagian 5), diterapkan pada file
1. V1-V7 lulus: terpenuhi.
2. Timing pada 40 ns di setiap seed: terpenuhi (6 dari 6).
3. Median ALM paling banyak 20,000: terpenuhi (14,115.5).
4. Latensi tiap operasi lebih rendah dari K2 pada 15 ns: terpenuhi (-4.42 %, -4.42 %, -4.42 %).
5. Kenaikan median (+3.430 MHz) lebih besar dari sebaran yang lebih besar (K3 6.35 MHz, K2 3.38 MHz), atau seed terendah K3 di atas tertinggi K2: TIDAK terpenuhi sebagaimana tertulis (73.02 MHz di bawah 76.03 MHz).
6. Seed terpenuhi pada 15 ns dilaporkan: 6 dari 6 (K2: 6 dari 6); 9 dari 9 dengan seed tambahan.
Hasil aturan: tidak diadopsi sebagaimana tertulis; K2 akan tetap. Amandemen A2 menambahkan, tanpa mengubah aturan, bahwa 5 dari 6 seed (6 dari 9) berada di atas setiap seed K2 dan median +3.4 MHz. Tim memutuskan (ADR 0042 Proposed; K3 juga basis pengukuran K4, ADR 0043).

## 5. Estimasi lawan pengukuran (ditulis di rencana sebelum pengukuran)
- Siklus per transformasi 119, operasi sama dengan K2: terpenuhi.
- ALM dalam +-150 dari K2: terpenuhi (-97.5 pada 40 ns, -56.5 pada 15 ns).
- Register +100 sampai +200: terpenuhi sebagian: +40 sampai +135 menurut corner dan batasan (fitter membagi sebagian register).
- Fmax 75 sampai 79 MHz, keyakinan rendah: terpenuhi (77.555 MHz; median sembilan seed 77.320).
- Latensi 107-112 / 130-137 / 198-208 us: terpenuhi (108.5 / 132.2 / 201.4 us).

## 6. Temuan
1. Jalur alamat diperbaiki: kelas `layer_q`-ke-memori (+1.404 ns di K2) tidak termasuk 300 jalur terburuk seed K3 terlemah; penghalang berikutnya adalah delay posisi-baca ke reducer (+1.666 ns) dan operand samping ke M10K (+2.368 ns).
2. Ekor seed rendah (seed 4 pada 73.02, seed 8 pada 75.47, seed 9 pada 72.80 MHz di samping enam seed pada 77.0-79.4 MHz) menghalangi aturan terpenuhi. INFERENCE (ditemukan di laporan K4, `../9i4/critical_paths_K4-15.md`, tidak diperiksa pada seed K3 dengan laporan jalur): suku `start_go` logika S2b membuat alamat terregister bergantung pada `host_we_i`, yang digerakkan sequencer dari `cnt_q != 0`; jalur `cnt_q` -> `core_hwe_o` -> `mode_n` -> penjumlah alamat -> `jlen_r` adalah jalur terburuk seed terlemah K4 (+0.736 ns).
3. Biaya S2b: tanpa siklus tambahan, sekitar +40 sampai +135 register, ALM sama dalam sebaran; tanpa blok RAM atau DSP.
4. Kenaikan bergantung pada S2 (register setelah reducer): K2 sendiri memberi +0.27 MHz, K3 memberi +3.43 MHz di atas K2 (+3.70 MHz di atas K1b).

## 7. Yang tidak ditunjukkan ini
Tidak ada hasil papan; tidak ada klaim kecepatan terhadap perangkat lunak; timing statis kernel-only dengan virtual pin; derau seed 3 MHz (lebih besar untuk K3) membatasi pernyataan di bawah ukuran itu; tiga seed tambahan dipilih setelah hasil; K2 hanya punya enam seed; waktu-konstan berarti invarian jumlah siklus saja; ACVP adalah simulasi; bukti formal mencakup kendali dan kapasitas bank, bukan nilai alamat. Satu seed (K3-15-s4) dianalisis untuk jalurnya.

## 8. File
`test_plan_9s2b.md` (dengan amandemen A1 dan A2), `selection_worksheet.md`, `sim.md`, `formal.md`, `critical_paths_K3-15.md`, `profile_k3_verilator.json`, `cycles_*_k3.json`, lima belas ekstrak `quartus_K3*.md`, `quartus/phase09s2b_core/` (runner `run_k3.sh`, `run_k3_15.sh`, `run_k3_40.sh`, `run_k3_x.sh`), `scripts/quartus/select_9s2b.py`, `formal/run/run_formal_phase9s2b.py`, `formal/phase09m-optimisation/9s2b/`, runner test yang berubah.
