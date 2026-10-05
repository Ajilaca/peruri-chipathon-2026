# Phase 9c deep cover (depth 480), 2026-10-04

MEASURED with SymbiYosys (yosys-slang, boolector), `formal/phase09-integration/9c/mlkem_core_cover_deep.sby` (cover mode, depth 480, `-D DEEP`), run by hand in a copy of the work directory; the same five cover statements of `mlkem_core_formal_top.sv` as the depth-260 run plus the two that need the longest program. Result: **DONE (PASS, rc=0): all five covered states are reached**, so the safety proof of `formal.md` is not vacuous for the Decaps program either. Elapsed 0:28:07 (1,687 s). Control and range only; this shows reachability with the sub-blocks replaced by protocol stubs that finish at once, not a timing of the real core.

| Cover statement | First step reached |
|---|---|
| a digest word is taken from the hash stub (state S_HGT, `hg_take`) | 18 |
| KeyGen done (`done_a_o` with op 0) | 233 |
| Encaps done (`done_a_o` with op 1) | 233 |
| state S_CMPK (comparison of the re-encrypted ciphertext) | 266 |
| Decaps done (`done_a_o` with op 2) | 272 |

(INFERENCE: SymbiYosys prints the source positions of the DEEP build with an offset, so the table assigns the five reached statements to their meaning by the length of each statement at the printed position (37 characters: the two `done_a_o` covers, 35: the digest word, 21: S_CMPK) and by the step order; the five distinct statements, all reached, are the point of this run.)

Raw summary lines of the run:

```
SBY  2:21:27 [out] summary: Elapsed clock time [H:MM:SS (secs)]: 0:28:07 (1687)
SBY  2:21:27 [out] summary: Elapsed process time [H:MM:SS (secs)]: 0:28:54 (1734)
SBY  2:21:27 [out] summary: engine_0 (smtbmc boolector) returned pass
SBY  2:21:27 [out] summary: cover trace: out/engine_0/trace0.vcd
SBY  2:21:27 [out] summary:   reached cover statement mlkem_core_formal_top._witness_.check_1285 at mlkem_core_formal_top.sv:154.7-154.42 step 18
SBY  2:21:27 [out] summary: cover trace: out/engine_0/trace1.vcd
SBY  2:21:27 [out] summary:   reached cover statement mlkem_core_formal_top._witness_.check_1270 at mlkem_core_formal_top.sv:150.7-150.44 step 233
SBY  2:21:27 [out] summary: cover trace: out/engine_0/trace2.vcd
SBY  2:21:27 [out] summary:   reached cover statement mlkem_core_formal_top._witness_.check_1274 at mlkem_core_formal_top.sv:151.7-151.44 step 233
SBY  2:21:27 [out] summary: cover trace: out/engine_0/trace3.vcd
SBY  2:21:27 [out] summary:   reached cover statement mlkem_core_formal_top._witness_.check_1282 at mlkem_core_formal_top.sv:153.7-153.28 step 266
SBY  2:21:27 [out] summary: cover trace: out/engine_0/trace4.vcd
SBY  2:21:27 [out] summary:   reached cover statement mlkem_core_formal_top._witness_.check_1278 at mlkem_core_formal_top.sv:152.7-152.44 step 272
```
