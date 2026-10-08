<!-- claim-lint: skip-file (internal analysis, not proposal text) -->
# Kedalaman pipeline butterfly P: batas bebas-stall jadwal lajur dan efeknya pada inti, 2026-10-04

Analisis perencanaan (perhitungan tim, tanpa RTL, tanpa kompilasi Quartus P = 16): keluaran `scripts/test/pipeline_hazard_slack.py` (alat bantu Fase 4; slack read-after-write di batas layer jadwal lajur `tb/mem/bank_model.py`), ditambah aritmetika dari Fase 4 (`docs/results/phase04.md`: siklus NTT / INTT = 113 / 369 + P), inti S10 (118 siklus pada P = 5, Fase 6) dan profil inti (`profile.md`). INFERENCE: model mengasumsikan inti S10 punya ketergantungan batas layer yang sama dengan inti Fase 4 (jadwal lajur sama).

```
Layer-boundary slack (cycles) of the current lane schedule; a pipeline of depth P needs no
stall at a boundary iff slack >= P.
L=1 NTT  T=128: slack per boundary [63, 95, 111, 119, 123, 125] -> largest stall-free P = 63
L=1 INTT T=128: slack per boundary [125, 123, 119, 111, 95, 63] -> largest stall-free P = 63
L=1 INTT last layer -> scaling pass: slack 127 (no stall before the scaling pass iff slack >= P)
L=2 NTT  T= 64: slack per boundary [63, 31, 47, 55, 59, 61] -> largest stall-free P = 31
L=2 INTT T= 64: slack per boundary [61, 59, 55, 47, 31, 63] -> largest stall-free P = 31
L=2 INTT last layer -> scaling pass: slack 63 (no stall before the scaling pass iff slack >= P)
L=4 NTT  T= 32: slack per boundary [31, 31, 15, 23, 27, 29] -> largest stall-free P = 15
L=4 INTT T= 32: slack per boundary [29, 27, 23, 15, 31, 31] -> largest stall-free P = 15
L=4 INTT last layer -> scaling pass: slack 31 (no stall before the scaling pass iff slack >= P)
L=8 NTT  T= 16: slack per boundary [15, 15, 15, 7, 11, 13] -> largest stall-free P = 7
L=8 INTT T= 16: slack per boundary [13, 11, 7, 15, 15, 15] -> largest stall-free P = 7
L=8 INTT last layer -> scaling pass: slack 15 (no stall before the scaling pass iff slack >= P)
```

## Pembacaan (L = 8)
- P bebas-stall terbesar = 7. Untuk P = 16 stall di batas adalah P - slack: batas NTT (slack 15, 15, 15, 7, 11, 13) stall 1 + 1 + 1 + 9 + 5 + 3 = 20 siklus; batas INTT (13, 11, 7, 15, 15, 15) stall 3 + 5 + 9 + 1 + 1 + 1 = 20 siklus, ditambah 1 sebelum lintasan skala (slack 15).
- Siklus per transformasi: 118 pada P = 5 (MEASURED, S10). Pada P = 16: +11 (latensi) + 20 stall = sekitar 149 (NTT); INTT sekitar 170 (ESTIMATE).
- Transformasi per operasi (counter program): KeyGen 6 NTT; Encaps 3 NTT + 4 INTT; Decaps 11 transformasi (dekripsi 3 NTT + 1 INTT, enkripsi ulang 3 NTT + 4 INTT). Pada 118 siklus masing-masing inti NTT sibuk 708 / 826 / 1.298 siklus = 8,5 % / 8,1 % / 8,4 % dari 8.327 / 10.159 / 15.515 (inti 9M-1).
- P = 16 menambah sekitar 186 / 301 / 446 siklus (+2,2 % / +3,0 % / +2,9 %).
