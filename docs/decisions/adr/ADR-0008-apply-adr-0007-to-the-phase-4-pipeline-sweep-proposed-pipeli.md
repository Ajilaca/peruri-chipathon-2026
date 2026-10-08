# ADR 0008: Menerapkan ADR 0007 pada sapuan pipeline Fase 4: kedalaman pipeline P yang diusulkan

- Status: Superseded by ADR 0009 (2026-10-01). Sebelumnya Proposed dan tidak pernah diterima; pengukurannya tetap
  bukti yang valid. Teks di bawah dibiarkan apa adanya.
- Tanggal: 2026-09-30
- Diputuskan oleh: (menunggu: Team J5; tidak diputuskan oleh asisten)

## Konteks
ADR 0007 menetapkan, sebelum apa pun diukur, kedalaman kandidat P dalam {0, 2, 4, 6}, empat syarat kandidat
(bit-exact PASS, siklus konstan PASS, ALM <= 10.478, timing terpenuhi pada 40,000 ns di setiap corner yang
dilaporkan) dan aturan seleksi (Fmax(P) = Fmax slow-corner terendah; t_NTT = siklus_NTT / Fmax; P terkecil dalam
5 % dari t_NTT minimum). ADR 0006 menetapkan batasan (40,000 ns, target milestone eksperimen, bukan persyaratan
perangkat keras atau sistem). Keempat revisi lalu dikompilasi dengan satu SDC dan seed bawaan
(`quartus/phase04_pipeline_c3/`), dan aturan diterapkan oleh `scripts/quartus/phase4_select_p.py`, yang membaca
file evidence (`evidence/phase04/selection_worksheet.md`).

## Opsi yang dipertimbangkan
Hasil terukur (MEASURED, `evidence/phase04/quartus_C3-P<n>.md`; siklus dari
simulasi, `cocotb_regression.txt`):

| P | ALM (dari 41.910) | <= 10.478? | Slack setup / hold terburuk @ 40,000 ns | Timing terpenuhi? | Fmax(P), slow corner terendah (MHz) | Siklus NTT / INTT | t_NTT / t_INTT (us) | Kandidat? |
|---|---|---|---|---|---|---|---|---|
| 0 | 9.723 | ya | -90,653 / 0,207 | tidak | 7,65 | 113 / 369 | 14,771 / 48,235 | tidak |
| 2 | 9.696 | ya | -0,368 / 0,174 | tidak (corner slow -40C; slow 100C +0,061) | 24,77 | 115 / 371 | 4,643 / 14,978 | tidak |
| 4 | 10.439 | ya (39 di bawah) | 8,734 / 0,157 | ya | 31,98 | 117 / 373 | 3,659 / 11,664 | ya |
| 6 | 10.505 | tidak (27 di atas) | 10,753 / 0,140 | ya | 34,19 | 119 / 375 | 3,481 / 10,968 | tidak (ALM) |

Register 3.097 / 3.817 / 4.145 / 4.168, DSP 9 / 112 di keempatnya, M10K 0 / 16 / 26 / 29 dari 553.
Himpunan kandidat C = {4}; t_min = t_NTT(4); aturan menghasilkan P_terpilih = 4. P = 6 akan punya t_NTT terendah
dari semuanya (3,481 us, 4,9 % di bawah P = 4; setara P = 4 adalah 5,1 % di atas P = 6) tetapi gugur oleh syarat
ALM sebesar 27 ALM.

## Keputusan
Tidak diputuskan. Aturan ADR 0007, diterapkan apa adanya, memberi P = 4. Catatan ini Proposed sampai tim
menerimanya, mengubahnya, atau meminta pengukuran lebih. Tidak ada hal lain di repository yang memperlakukan P = 4
sebagai terpilih.

## Konsekuensi
Hal-hal yang perlu ditimbang tim sebelum menerima (dinyatakan, tidak diselesaikan di sini):
- Margin tipis; sapuan seed dijalankan (2026-10-01) untuk mengukur setipis apa. Seed 1-6, yang lain identik
  (`evidence/phase04/seed_sweep.md`, MEASURED):
  - P = 6 melewati anggaran 10.478 ALM di setiap seed (10.484-10.516 ALM). Tidak pernah menjadi kandidat.
  - P = 4 dalam anggaran di 4 dari 6 seed (10.439-10.503 ALM); di seed 2 dan 3 melewati sebesar 25 dan 1 ALM, dan
    saat itu tidak ada P yang menjadi kandidat.
  - Kedua belas kompilasi memenuhi 40,000 ns. Fmax P = 4 (slow corner terendah) 30,60-33,00 MHz antar seed.
  - Aturan per seed memilih P = 4 atau tidak memilih apa pun; tidak pernah memilih P lain.
  Jadi pilihan antara P = 4 dan P = 6 ditetapkan oleh pengukuran, tetapi P = 4 memenuhi anggaran hanya dengan selisih
  beberapa puluh ALM dan tidak di setiap seed. Menerima P = 4 berarti menerima bahwa Fase 5 mulai dengan hampir tanpa
  ruang ALM (perubahan aritmetika Fase 5 diharapkan mengubah ALM; itu harus diukur, tidak diasumsikan).
- Efek alat mengubah gambaran sumber daya, bukan hanya pipeline. Dengan register di jalur memori Quartus
  menginferensi `bank_map_rom` dan beberapa rantai register (`altshift_taps`) ke blok M10K (16 / 26 / 29 blok; 0
  untuk P = 0). Inilah sebabnya P = 2 memakai ALM lebih sedikit dari P = 0 meski sekitar 700 register lebih banyak.
  Ini tidak dirancang atau diminta (pemetaan M10K di luar lingkup Fase 4) dan dilaporkan seperti teramati;
  inferensi berbeda di fase berikutnya akan mengubah angka ALM.
- Hampir-seri 5 % hanya pada t_NTT, dan tipis (seed bawaan). P = 6 gugur oleh syarat ALM, jadi aturan hampir-seri
  tidak dijalankan. Bila syarat ALM dilonggarkan, C akan {4, 6}, t_min = t_NTT(6) = 3,481 us dan
  d(4) = 0,051 > 0,05, jadi aturan akan memilih P = 6, bukan P = 4. Pada seed bawaan pemilihan bergantung pada
  selisih 27 ALM; sapuan seed menunjukkan P = 6 melewati anggaran di setiap seed, jadi ketergantungan itu hilang.
- 40,000 ns dipenuhi oleh P = 4 dan P = 6 hanya menurut analisis timing statis Quartus; tidak ada run papan dan
  tidak ada yang diklaim. Angka Fmax adalah kernel-only dengan virtual pin.
- Kekurangan P = 2 kecil (-0,368 ns di satu corner) dan diukur apa adanya; tidak ada pengecualian yang ditambahkan.
- Bila diterima, Fase 5 mulai dari C3-P4 dan tujuan akhir 20,000 ns (ADR 0006) adalah pemeriksaan terpisah:
  Fmax 31,98 MHz tidak mencapai 50 MHz.

## Bukti
- `evidence/phase04/seed_sweep.md`, `evidence/phase04/seed_sweep/`,
  `scripts/quartus/phase4_seed_sweep_summary.py`
- `evidence/phase04/selection_worksheet.md`, `scripts/quartus/phase4_select_p.py`,
  `evidence/phase04/verification_status.json`
- `evidence/phase04/quartus_C3-P0.md`, `quartus_C3-P2.md`,
  `quartus_C3-P4.md`, `quartus_C3-P6.md`
- `evidence/phase04/cocotb_regression.txt`,
  `evidence/phase04/v2_modmul_staged_exhaustive.txt`,
  `evidence/phase04/formal.md`, `evidence/phase04/regression.txt`
- `docs/decisions/adr/ADR-0006-phase-4-target-clock.md`, `docs/decisions/adr/ADR-0007-phase-4-pipeline-depth-p-and-selection-criterion.md`,
  `docs/decisions/adr/ADR-0004-phase-3-lane-count-l-selection-criterion.md`
