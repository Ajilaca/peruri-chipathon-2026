# Phase 9c formal run (CRG-8), `formal/run/run_formal_phase9c.py all`, 2026-10-04

MEASURED with SymbiYosys (yosys-slang, boolector). Group C is a cover-mode run (every covered state must be reached; it shows the proof is not vacuous), depth 260. The controller is proved with protocol stubs of the sub-blocks (`formal/phase09-integration/9c/stubs_9c.sv`; test plan 9c, Amendment A2). E1 is a two-copy non-interference property: two copies of the controller with different data and identical handshakes keep identical control state. Control and range properties only; values are covered by simulation (ACVP). Decaps done and the S_CMPK state are not reached at depth 260 (the hash-feed state needs 136-148 words); the separate deep cover run (`formal_deep_cover.md`, depth 480) reaches both. Work directory `formal/work/phase9c/` (git-ignored).

| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |
|---|---|---|---|---|---|---|
| C Reachability | mlkem_core: KeyGen done, Encaps done and a digest word written are reachable (the proof is not vacuous) | PASS | PASS | bmc=pass | 1134.8 | yes |
| A Phase 9c | mlkem_core controller (E1 non-interference, S1 ranges, S2 busy / done, S3 no host write while busy, S4 strobes, S5 engine ports, S6 addresses, S7 counters) | PASS | PASS | basecase=pass, induction=pass | 5.0 | yes |
| B Negative control | NC-E1: the program counter depends on a data bit (E1 non-interference) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_core_formal_top.sv:70 | 3.9 | yes |
| B Negative control | NC-S3: a host write is accepted while busy, in the state LDP (S3) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_core_formal_top.sv:97 | 3.4 | yes |
| B Negative control | NC-S4: the store task starts together with the load task (S4) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_core_formal_top.sv:99 | 3.3 | yes |

ALL AS EXPECTED
