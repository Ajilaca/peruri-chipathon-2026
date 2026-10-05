# MEASURED (formal, control and bank properties only): S10, formal/run/run_formal_s10.py at git 8d8cb6f, 2026-10-03

| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |
|---|---|---|---|---|---|---|
| A S10 | s10 (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 35.1 | yes |
| B Negative control | NC-O s10: bank map without the XOR bit (two ports on one bank) | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_s10_formal_top.sv:129 | 22.0 | yes |
| B Negative control | NC-A s10: delay model of property A one cycle short | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_s10_formal_top.sv:130 | 28.3 | yes |

OVERALL: all results as expected (3/3)
