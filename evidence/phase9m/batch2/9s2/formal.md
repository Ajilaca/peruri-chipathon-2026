# Phase 9F S2 formal run, 2026-10-04 (V5)

MEASURED (formal, control and bank capacity only). Command: `. scripts/env.sh && python3 formal/run/run_formal_phase9s2.py` (depth 9 = P + 3, `smtbmc boolector`, work directory `formal/work/phase9s2/`, not stored). Properties H, O, R, A, B, C of `formal/phase09m-optimisation/9s2/ntt_core_s10_p6_formal_top.sv` (a copy of `formal/s10/ntt_core_s10_formal_top.sv` with P = 6 and the wrapper parameter `P6 = 1`) on `rtl/ntt/ntt_core_s10_p5.sv`. Nothing here proves NTT/INTT arithmetic or memory data (simulation V2 covers that).

```
| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |
|---|---|---|---|---|---|---|
| A S2 | s10 at P = 6 (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 15.6 | yes |
| B Negative control | NC-O p6: bank map without the XOR bit (two ports on one bank) | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_s10_p6_formal_top.sv:131 | 7.3 | yes |
| B Negative control | NC-A p6: delay model of property A one cycle short | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_s10_p6_formal_top.sv:132 | 9.9 | yes |

OVERALL: all results as expected (3/3)
```

Reading: the three-row table is the S10 flow at P = 6. The proofs hold at P = 6 (every write fires exactly 6 cycles after its request, drained at S_DONE, no read and write of one location in the same cycle, no bank overflow); both negative controls fail as required (NC-O the bank map without the XOR bit; NC-A the delay model one cycle short). Limit: control and bank capacity only (base case and induction at depth 9, as in S10); the arithmetic path through the new register is covered by the bit-exact simulations (V2, V7), not by this proof.
