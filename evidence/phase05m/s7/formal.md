# MEASURED (formal, hanya properti kendali dan bank): Fase 5M S7, formal/run/run_formal_phase5m_s7.py pada git b53309d, 2026-10-02

| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| A Fase 5M S7 | s7 (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 65.7 | ya |
| B Kontrol negatif | NC-O s7: salinan bank_map_rom, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_s7_formal_top.sv:129 | 30.6 | ya |
| B Kontrol negatif | NC-A s7: model delay properti A kurang satu siklus | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_s7_formal_top.sv:130 | 33.3 | ya |

OVERALL: semua hasil sesuai harapan (3/3)
