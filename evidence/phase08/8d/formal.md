<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Phase 8d formal run (test plan V7), 2026-10-03

Command: `. scripts/env.sh && python3 formal/run/run_formal_phase8d.py`. Label: MEASURED (SymbiYosys, boolector, induction depth 12; OVERLAP = 1; the NTT core abstracted, the sampler replaced by the protocol stub). Control properties only, not values.

| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |
|---|---|---|---|---|---|---|
| A Phase 8d | kpke_sched_smp STREAM_A=1 OVERLAP=1 (F1-F5) | PASS | PASS | basecase=pass, induction=pass | 3.0 | yes |
| B Negative control | NC-F2: seed write accepted while busy (F2), OVERLAP=1 | FAIL | FAIL | basecase=FAIL; failed assert kpke_sched_smp_formal_top.sv:87 | 1.4 | yes |

ALL AS EXPECTED
