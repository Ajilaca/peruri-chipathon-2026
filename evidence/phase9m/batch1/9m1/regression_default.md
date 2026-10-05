# Phase 9M-1 regression at the default parameter (V7), 2026-10-04

MEASURED. With `CODEC_W2 = 0` (the default) the core must behave exactly as in Phase 9. Run on the branch `phase9m-optimisation` (the core now has generate blocks and the new files exist, but the default instantiates the Phase 9 tasks): `scripts/test/phase9c_verify.sh` (lint, ROM check, golden model, whole ACVP set on both simulators, then `phase9a_verify.sh` and `phase9b_verify.sh` with formal, then the frozen-block check against main), `formal/run/run_formal_phase9c.py all`, and the profile of `../../profile.md` repeated at the default (identical to the Phase 9 profile: KeyGen 9,095, Encaps 10,735, Decaps 16,667 cycles, every per-state and per-operation count equal). Only section headers and result lines of the raw log are kept.

## scripts/test/phase9c_verify.sh
```
## V1 verilator --lint-only -Wall mlkem_core (whole design)
rc=0
## V1 slang mlkem_core (whole design)
rc=0
## V2 ROM equals the generated ROM, static checks
rc=0
## V2 golden control model against ACVP and the unmodified golden
rc=0
## V3-V8 verilator
[verilator] TOTAL: 11/11 passed
rc=0
## V3-V8 icarus
[icarus] TOTAL: 11/11 passed
rc=0
## V10 regression: scripts/test/phase9a_verify.sh (without formal)
rc=0
rc=0
rc=0
rc=0
rc=0
[verilator] TOTAL: 17/17 passed
rc=0
[icarus] TOTAL: 17/17 passed
rc=0
OVERALL: PASS
rc=0
## V10 regression: scripts/test/phase9b_verify.sh (with formal)
rc=0
rc=0
rc=0
rc=0
rc=0
rc=0
[verilator] TOTAL: 23/23 passed
rc=0
[icarus] TOTAL: 23/23 passed
rc=0
rc=0
OVERALL: PASS
rc=0
## V10 frozen blocks: files of rtl/sched rtl/ntt rtl/mem rtl/arith rtl/sample rtl/keccak that differ from main
differing files: 0
OVERALL: PASS
```

## formal/run/run_formal_phase9c.py all (default parameter)

| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |
|---|---|---|---|---|---|---|
| C Reachability | mlkem_core: KeyGen done, Encaps done and a digest word written are reachable (the proof is not vacuous) | PASS | PASS | bmc=pass | 926.3 | yes |
| A Phase 9c | mlkem_core controller (E1 non-interference, S1 ranges, S2 busy / done, S3 no host write while busy, S4 strobes, S5 engine ports, S6 addresses, S7 counters) | PASS | PASS | basecase=pass, induction=pass | 3.5 | yes |
| B Negative control | NC-E1: the program counter depends on a data bit (E1 non-interference) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_core_formal_top.sv:80 | 2.5 | yes |
| B Negative control | NC-S3: a host write is accepted while busy, in the state LDP (S3) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_core_formal_top.sv:107 | 2.3 | yes |
| B Negative control | NC-S4: the store task starts together with the load task (S4) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_core_formal_top.sv:109 | 2.4 | yes |

ALL AS EXPECTED
