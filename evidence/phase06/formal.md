# MEASURED (formal, control properties only): Phase 6, formal/run/run_formal_phase6.py at git 8133e08, 2026-10-03

| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |
|---|---|---|---|---|---|---|
| A Phase 6 | kpke_sched (H, T, C, R) | PASS | PASS | basecase=pass, induction=pass | 3.0 | yes |
| B Negative control | NC-T: testbench write reaches the store while busy | FAIL | FAIL | basecase=FAIL; failed assert kpke_sched_formal_top.sv:54 | 2.6 | yes |

OVERALL: all results as expected (2/2)
