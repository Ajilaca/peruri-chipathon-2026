# MEASURED (formal, hanya properti kendali dan bank): Fase 5M S8, formal/run/run_formal_phase5m_s8.py pada git 300aaf3, 2026-10-03

| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| A Fase 5M S8 | s8 (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 39.6 | ya |
| B Kontrol negatif | NC-O s8: salinan bank_map_rom, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_s8_formal_top.sv:129 | 11.5 | ya |
| B Kontrol negatif | NC-A s8: model delay properti A kurang satu siklus | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_s8_formal_top.sv:130 | 16.8 | ya |

OVERALL: semua hasil sesuai harapan (3/3)
