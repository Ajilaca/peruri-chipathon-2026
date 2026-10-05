# MEASURED (formal, control and bank properties only): Phase 5M S8, formal/run/run_formal_phase5m_s8.py at git 300aaf3, 2026-10-03

| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |
|---|---|---|---|---|---|---|
| A Phase 5M S8 | s8 (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 39.6 | yes |
| B Negative control | NC-O s8: bank_map_rom copy, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_s8_formal_top.sv:129 | 11.5 | yes |
| B Negative control | NC-A s8: delay model of property A one cycle short | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_s8_formal_top.sv:130 | 16.8 | yes |

OVERALL: all results as expected (3/3)
