# Phase 5b formal (test plan V8) - 2026-10-01

Command: `. scripts/env.sh && python3 formal/run/run_formal_phase5.py` (yosys-slang frontend, `memory_map -rom-only`, SymbiYosys, smtbmc boolector). Run after the 5b RTL was added; C4a is re-proven with the extended source list.
Scope: control and bank-capacity properties H, O, R, A, B, C of `formal/phase05-arith/ntt_core_c4_formal_top.sv` on the Quartus wrappers `rtl/ntt/ntt_core_c4a.sv`, `ntt_core_c4b_b.sv`, `ntt_core_c4b_m.sv` (P = 6), with two negative controls each on corrupted copies. **Not** arithmetic (covered by the exhaustive reducer test and the bit-exact simulations).

| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |
|---|---|---|---|---|---|---|
| A Phase 5 | c4a (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 15.0 | yes |
| B Negative control | NC-O c4a: bank_map_rom copy, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:142 | 12.8 | yes |
| B Negative control | NC-A c4a: delay model of property A one cycle short | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:143 | 11.2 | yes |
| A Phase 5 | c4b_b (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 28.3 | yes |
| B Negative control | NC-O c4b_b: bank_map_rom copy, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:142 | 17.3 | yes |
| B Negative control | NC-A c4b_b: delay model of property A one cycle short | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:143 | 23.0 | yes |
| A Phase 5 | c4b_m (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 20.1 | yes |
| B Negative control | NC-O c4b_m: bank_map_rom copy, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:142 | 16.5 | yes |
| B Negative control | NC-A c4b_m: delay model of property A one cycle short | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:143 | 19.2 | yes |
OVERALL: all results as expected (9/9)
