# MEASURED (formal, hanya properti kendali dan bank): Fase 5M S6, formal/run/run_formal_phase5m.py pada git 4382a5f, 2026-10-02

| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| A Fase 5M | m6 (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 62.4 | ya |
| B Kontrol negatif | NC-O m6: salinan bank_map_rom, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_m6_formal_top.sv:129 | 11.7 | ya |
| B Kontrol negatif | NC-A m6: model delay properti A kurang satu siklus | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_m6_formal_top.sv:130 | 12.4 | ya |
OVERALL: semua hasil sesuai harapan (3/3)
