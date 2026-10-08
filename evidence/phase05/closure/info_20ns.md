<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Penutup Fase 5: kompilasi informasi pada 20,000 ns (ADR 0011 D1, ADR 0010)

Bukan gerbang Fase 5: 50 MHz adalah target terbaik-upaya (ADR 0010). Satu kompilasi per konfigurasi, seed bawaan 1,
bawaan Quartus, device dan penugasan QSF sama; satu-satunya perubahan adalah `quartus/phase05_arith_c4/C4-20.sdc`
(20,000 ns sebagai ganti 40,000 ns). Revisi: `C4b-B-20` (konfigurasi C4 akhir) dan `C3-P6-20` (RTL Fase 4, tidak berubah).

| Besaran (MEASURED) | C3-P6 pada 20,000 ns | C4b-B pada 20,000 ns |
|---|---|---|
| ALM (dari 41,910) | 10,557 | 9,305 |
| Register / M10K / DSP | 4,316 / 29 / 9 | 4,272 / 29 / 18 |
| Slack setup terburuk (corner) | -2.059 ns (Slow -40C) | -2.557 ns (Slow 100C) |
| Slack hold terburuk | +0.147 ns | +0.151 ns |
| Timing terpenuhi pada 20,000 ns | tidak | tidak |
| Fmax, slow corner terendah (MHz) | 45.33 | 44.33 |
| Evidence | `quartus_C3-P6-20.md` | `quartus_C4b-B-20.md` |

Pembacaan (INFERENCE, satu seed masing-masing, jadi selisih sebesar ini ada di dalam sebaran seed yang terukur pada 40 ns):
- Tidak satu pun konfigurasi memenuhi 20,000 ns. Kekurangannya 2.06 ns (C3-P6) dan 2.56 ns (C4b-B).
- Di bawah batasan 20 ns fitter bekerja lebih keras, jadi Fmax yang dilaporkan (44-45 MHz) lebih tinggi dari pada 40 ns
  (33-35 MHz); kedua nilai Fmax tidak sebanding antar batasan.
- Konfigurasi C4 akhir 1,252 ALM lebih kecil dari C3-P6 pada 20 ns (10,557 - 9,305) dan punya 9 DSP lebih banyak, tetapi Fmax-nya
  tidak lebih tinggi (44.33 lawan 45.33 MHz). Ini sesuai ADR 0010: perubahan aritmetika tidak mencapai 20 ns selagi jalur pembacaan memori
  mendominasi (`evidence/phase05/baseline/c3p6_critical_path.md`).
- Peringatan kritis (3 per kompilasi, sama di keduanya): 15725 (clock diberi makan virtual pin `clk_i`, wajar untuk kompilasi
  kernel-only, seperti di Fase 1-4) dan 332148 x2 (persyaratan timing tidak terpenuhi, hasil 20 ns di atas). Dibahas,
  tidak diabaikan; tidak ada penugasan yang ditambahkan.
- Tidak ada analisis jalur yang dijalankan pada 20 ns (tidak diminta).
