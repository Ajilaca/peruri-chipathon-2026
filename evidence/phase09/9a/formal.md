# Phase 9a formal run (V9), `formal/run/run_formal_phase9a.py`, 2026-10-03

MEASURED with SymbiYosys (yosys-slang, boolector). Work directory `formal/work/phase9a/` (git-ignored).

| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |
|---|---|---|---|---|---|---|
| A Phase 9a | mlkem_pack (P1 counts, P2 held output, P3 idle, P4 bit balance, P5 pipeline count) | PASS | PASS | basecase=pass, induction=pass | 17.4 | yes |
| B Negative control | NC-P1: the packer accepts a 257th coefficient (P1 count); violation beyond depth 40, so the proof must not pass | UNKNOWN | UNKNOWN | basecase=pass, induction=FAIL; failed assert mlkem_pack_formal_top.sv:87 | 441.6 | yes |
| B Negative control | NC-P1 again in BMC at depth 300: the 257th coefficient is reachable (P1 count) | FAIL | FAIL | bmc=FAIL; failed assert mlkem_pack_formal_top.sv:87 | 548.2 | yes |
| B Negative control | NC-P2: the output byte changes when a coefficient is inserted while it is held (P2) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_pack_formal_top.sv:98 | 0.6 | yes |
| A Phase 9a | mlkem_unpack (U1 counts, U2 held output, U3 idle, U4 bit balance, U5 output register, U6 range) | PASS | PASS | basecase=pass, induction=pass | 11.9 | yes |
| B Negative control | NC-U1: the unpacker accepts one byte more than 32 d (U1 count); violation beyond depth 40, so the proof must not pass | UNKNOWN | UNKNOWN | basecase=pass, induction=FAIL; failed assert mlkem_unpack_formal_top.sv:85 | 192.0 | yes |
| B Negative control | NC-U1 again in BMC at depth 300: the extra byte is reachable (U1 count) | FAIL | FAIL | bmc=FAIL; failed assert mlkem_unpack_formal_top.sv:85 | 377.5 | yes |
| B Negative control | NC-U6: d = 12 without the reduction mod q (U6 range) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_unpack_formal_top.sv:105 | 0.6 | yes |

ALL AS EXPECTED
