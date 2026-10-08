# MEASURED (formal, hanya properti kendali dan bank): S10, formal/run/run_formal_s10.py pada git 8d8cb6f, 2026-10-03

| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| A S10 | s10 (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 35.1 | ya |
| B Kontrol negatif | NC-O s10: peta bank tanpa bit XOR (dua port di satu bank) | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_s10_formal_top.sv:129 | 22.0 | ya |
| B Kontrol negatif | NC-A s10: model delay properti A kurang satu siklus | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_s10_formal_top.sv:130 | 28.3 | ya |

OVERALL: semua hasil sesuai harapan (3/3)
