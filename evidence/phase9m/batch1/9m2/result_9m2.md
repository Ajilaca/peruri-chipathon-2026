<!-- claim-lint: skip-file (internal block report, not proposal text) -->
# Laporan Fase 9M butir 2 (9M-2): inti pada 20,000 ns, seed 1-6

- Status: SELESAI (STOP setelah butir, ADR 0034). Branch `phase9m-optimisation`, belum di-commit. Tidak ada perubahan RTL: sumbernya adalah Fase 9 dan 9M-1. Rencana dan aturan: `test_plan_9m2.md` (ditulis sebelum kompilasi). Timing statis kernel-only dengan virtual pin; bukan sistem di papan.

## 1. Hasil
Timing terpenuhi pada 20,000 ns (50 MHz) di 6 dari 6 seed untuk kedua konfigurasi (inti Fase 9 `CODEC_W2 = 0` dan inti 9M-1 `CODEC_W2 = 1`); aturan rencana (keenam seed) terpenuhi, jadi pernyataan boleh dibuat dengan label "timing statis kernel-only". Seed 1 berasal dari evidence Fase 9 / 9M-1, seed 2-6 baru (sepuluh kompilasi baru, satu per satu, semua `rc=0`).

## 2. Parameter yang diukur (MEASURED, `selection_worksheet.md`, ekstrak `quartus_*-20-s*.md`)
| Parameter | Inti Fase 9 pada 20 ns | Inti 9M-1 pada 20 ns | Inti Fase 9 pada 40 ns (acuan) |
|---|---|---|---|
| Timing terpenuhi pada 20,000 ns | 6 dari 6 seed | 6 dari 6 seed | (40 ns: 6 dari 6) |
| Slack setup terburuk atas seed / slack hold terburuk | +3.730 ns (seed 4) / +0.077 ns | +4.184 ns (seed 5) / +0.080 ns | +19.010 / +0.075 ns |
| Fmax, slow corner terendah, median (min-maks) | 63.645 MHz (61.46-64.66) | 63.990 MHz (63.23-66.54) | 49.280 MHz (47.64-51.74) |
| ALM, median (min-maks) | 17,708.5 (17,650-17,780) | 17,779.5 (17,728-17,845) | 17,620.5 |
| ALM dalam % dari 41,910 fitter | 42 % | 42 % | 42 % |
| Register | 8,369-8,504 | 8,407-8,487 | 8,210-8,365 |
| Blok RAM / DSP | 54 / 28 | 54 / 28 | 54 / 28 |
| Peringatan kritis per kompilasi | 1 (clock virtual pin, seperti semua kompilasi sebelumnya) | 1 | 1 |
| Siklus, masukan profil (KeyGen / Encaps / Decaps; simulasi) | 9,095 / 10,735 / 16,667 | 8,327 / 10,159 / 15,515 | sama |
| Latensi pada median Fmax tabel 20 ns (perhitungan tim) | 142.9 / 168.7 / 261.9 us | 130.1 / 158.8 / 242.5 us | pada median 40 ns: 184.6 / 217.8 / 338.2 us |
Latensi pada 20 ns adalah siklus dibagi Fmax slow corner terendah yang dicapai saat fitter diminta 20 ns. Ini bukan pengukuran sebuah operasi di papan.

## 3. Estimasi lawan pengukuran (ditulis di rencana sebelum kompilasi)
- Timing terpenuhi di sebagian besar atau semua seed: terpenuhi di semua 12 (6 + 6): di dalam. Satu kegagalan atau lebih mungkin terjadi; tidak ada yang terjadi.
- Fmax slow corner terendah 55-66 MHz: terukur 61.46-66.54 MHz: di dalam.
- Slack setup terburuk +1 sampai +5 ns: terukur +3.730 sampai +4.972 ns (terburuk per seed): di dalam.
- ALM dalam +/- 1 % dari median 40 ns: +0.5 % (inti Fase 9, 17,708.5 lawan 17,620.5) dan +0.7 % (inti 9M-1, 17,779.5 lawan 17,654.0): di dalam.

## 4. Temuan dan batas
1. Seed terendah pada 40 ns di bawah 50 MHz (47.64 MHz, inti Fase 9); pada batasan 20 ns setiap seed mencapai minimal 61.46 MHz. Selisihnya berasal dari upaya fitter di bawah batasan lebih ketat, bukan dari perubahan desain (INFERENCE; jalur kritis tidak diperiksa).
2. Hasilnya informasi, bukan gerbang (ADR 0010); pohon clock DE10-Nano, I/O, dan HPS tidak ada di kompilasi ini. Tidak ada klaim tentang papan.
3. 9M-1 lawan Fase 9 pada 20 ns: ALM +71.0 (median), median Fmax +0.345 MHz, di dalam sebaran seed; penghematan siklus 9M-1 tidak berubah.
4. Tidak ada masalah proses di butir ini: sepuluh kompilasi, semuanya berhasil, masalah `generate` pertama kali di 9M-1 tidak terulang.

## 5. Yang tidak ditunjukkan ini
Tidak ada hasil papan; tidak ada klaim kecepatan terhadap perangkat lunak; timing statis kernel-only dengan virtual pin pada satu batasan; waktu-konstan berarti invarian jumlah siklus saja.

## 6. File
`test_plan_9m2.md`, `selection_worksheet.md`, sepuluh ekstrak Quartus baru di direktori ini, `quartus/phase09m2_core/` (sepuluh revisi, `run_20.sh`), `scripts/quartus/select_9m2.py`.
