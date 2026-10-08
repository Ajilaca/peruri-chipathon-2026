<!-- claim-lint: skip-file (generated worksheet) -->
# Aturan ADR 0007 dengan anggaran ADR 0009 (30% = 12,573 ALM) - dibangkitkan 2026-10-01

Perintah: `python3 scripts/quartus/phase4_select_p.py --alm-budget 12573` dan `python3 scripts/quartus/phase4_seed_sweep_summary.py --alm-budget 12573`. Masukan adalah file evidence MEASURED yang tidak berubah dan terdaftar di bawah; worksheet 25% historis adalah `selection_worksheet.md`.

## Seed bawaan (keempat P)

ALM budget yang dipakai untuk kondisi 3: 12,573

| P | bit-exact | siklus konstan | ALM | ≤ 12,573? | slack setup / hold terburuk @ 40.000 ns | timing terpenuhi? | cycles_NTT | cycles_INTT | Fmax per slow corner (MHz) | Fmax(P) = terendah | t_NTT (µs) | t_INTT (µs) | kandidat? | d(P) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | PASS | PASS | 9,723 / 41,910 | ya | -90.653 / 0.207 | tidak | 113 | 369 | Slow 1100mV 100C: 7.65; Slow 1100mV -40C: 7.68 | 7.65 | 14.771 | 48.235 | tidak | - |
| 2 | PASS | PASS | 9,696 / 41,910 | ya | -0.368 / 0.174 | tidak | 115 | 371 | Slow 1100mV 100C: 25.04; Slow 1100mV -40C: 24.77 | 24.77 | 4.643 | 14.978 | tidak | - |
| 4 | PASS | PASS | 10,439 / 41,910 | ya | 8.734 / 0.157 | ya | 117 | 373 | Slow 1100mV 100C: 32.60; Slow 1100mV -40C: 31.98 | 31.98 | 3.659 | 11.664 | ya | 0.0511 |
| 6 | PASS | PASS | 10,505 / 41,910 | ya | 10.753 / 0.140 | ya | 119 | 375 | Slow 1100mV 100C: 34.19; Slow 1100mV -40C: 34.50 | 34.19 | 3.481 | 10.968 | ya | 0.0000 |

Sumber daya lain (MEASURED): P=0: register 3097, DSP 9 / 112, blok RAM 0 / 553; P=2: register 3817, DSP 9 / 112, blok RAM 16 / 553; P=4: register 4145, DSP 9 / 112, blok RAM 26 / 553; P=6: register 4168, DSP 9 / 112, blok RAM 29 / 553
File evidence: quartus_C3-P0.md, quartus_C3-P2.md, quartus_C3-P4.md, quartus_C3-P6.md, verification_status.json

Himpunan kandidat C = {4, 6}
t_min = 3.480550 us; dalam 5% dari t_min: {6}
HASIL: P_selected = 6 (kandidat terkecil dengan d(P) <= 0.05). Dicatat dalam ADR baru oleh tim.

## Seed 1–6 (P = 4 dan P = 6)

ALM budget: 12,573

| P | Seed | ALM | <= 12,573? | Register | M10K | Slack setup / hold terburuk (ns) | Timing terpenuhi? | Fmax(P) slow corner terendah (MHz) | t_NTT (us) | Memenuhi semua kondisi ADR 0007? | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 1 (bawaan) | 10,439 | ya | 4145 | 26 / 553 | 8.734 / 0.157 | ya | 31.98 | 3.659 | ya | `evidence/phase04/quartus_C3-P4.md` |
| 4 | 2 | 10,503 | ya | 4160 | 26 / 553 | 9.482 / 0.143 | ya | 32.77 | 3.570 | ya | `evidence/phase04/seed_sweep/quartus_C3-P4-s2.md` |
| 4 | 3 | 10,479 | ya | 4151 | 26 / 553 | 7.324 / 0.129 | ya | 30.60 | 3.824 | ya | `evidence/phase04/seed_sweep/quartus_C3-P4-s3.md` |
| 4 | 4 | 10,472 | ya | 4166 | 26 / 553 | 8.555 / 0.120 | ya | 31.80 | 3.679 | ya | `evidence/phase04/seed_sweep/quartus_C3-P4-s4.md` |
| 4 | 5 | 10,467 | ya | 4160 | 26 / 553 | 7.580 / 0.118 | ya | 30.85 | 3.793 | ya | `evidence/phase04/seed_sweep/quartus_C3-P4-s5.md` |
| 4 | 6 | 10,468 | ya | 4149 | 26 / 553 | 9.701 / 0.130 | ya | 33.00 | 3.545 | ya | `evidence/phase04/seed_sweep/quartus_C3-P4-s6.md` |
| 6 | 1 (bawaan) | 10,505 | ya | 4168 | 29 / 553 | 10.753 / 0.140 | ya | 34.19 | 3.481 | ya | `evidence/phase04/quartus_C3-P6.md` |
| 6 | 2 | 10,508 | ya | 4153 | 29 / 553 | 9.773 / 0.139 | ya | 33.08 | 3.597 | ya | `evidence/phase04/seed_sweep/quartus_C3-P6-s2.md` |
| 6 | 3 | 10,511 | ya | 4160 | 29 / 553 | 9.328 / 0.132 | ya | 32.60 | 3.650 | ya | `evidence/phase04/seed_sweep/quartus_C3-P6-s3.md` |
| 6 | 4 | 10,516 | ya | 4152 | 29 / 553 | 10.756 / 0.128 | ya | 34.20 | 3.480 | ya | `evidence/phase04/seed_sweep/quartus_C3-P6-s4.md` |
| 6 | 5 | 10,504 | ya | 4139 | 29 / 553 | 9.824 / 0.144 | ya | 33.14 | 3.591 | ya | `evidence/phase04/seed_sweep/quartus_C3-P6-s5.md` |
| 6 | 6 | 10,484 | ya | 4162 | 29 / 553 | 9.764 / 0.131 | ya | 33.07 | 3.598 | ya | `evidence/phase04/seed_sweep/quartus_C3-P6-s6.md` |

| P | ALM min / median / maks | Seed dalam 12,573 | Fmax min / median / maks (MHz) | Seed yang memenuhi semua kondisi ADR 0007 |
|---|---|---|---|---|
| 4 | 10,439 / 10,470.0 / 10,503 | 6 dari 6 | 30.60 / 31.89 / 33.00 | 6 dari 6 |
| 6 | 10,484 / 10,506.5 / 10,516 | 6 dari 6 | 32.60 / 33.11 / 34.20 | 6 dari 6 |

Per seed, aturan ADR 0007 diterapkan hanya pada {P=4, P=6} (P=0 dan P=2 tidak disapu; pada seed bawaan keduanya gagal timing pada 40.000 ns):

| Seed | Kandidat di antara {4, 6} | Hasil aturan |
|---|---|---|
| 1 | {4, 6} | P = 6 |
| 2 | {4, 6} | P = 4 |
| 3 | {4, 6} | P = 4 |
| 4 | {4, 6} | P = 6 |
| 5 | {4, 6} | P = 6 |
| 6 | {4, 6} | P = 4 |
