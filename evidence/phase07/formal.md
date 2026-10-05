<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Phase 7 formal run (test plan V8), 2026-10-03

Command: `. scripts/env.sh && python3 formal/run/run_formal_phase7.py` (SymbiYosys, yosys-slang frontend, engine smtbmc boolector). Properties K1-K5 of `formal/phase07-keccak/keccak_sponge_formal_top.sv` on
`rtl/keccak/keccak_sponge.sv` with `keccak_f1600.sv`, all inputs free, induction depth 30. Control properties only; digest values are covered by simulation against hashlib (`verify.md`).
Label: MEASURED (formal tool output of this run; RTL as committed after the Icarus enum fix).

| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |
|---|---|---|---|---|---|---|
| A Phase 7 | keccak_sponge + keccak_f1600 (K1, K2, K3, K4, K5) | PASS | PASS | basecase=pass, induction=pass | 22.5 | yes |
| B Negative control | NC-K1: 23 rounds per permutation (K1 busy length) | FAIL | FAIL | basecase=FAIL; failed assert keccak_sponge_formal_top.sv:105 | 38.4 | yes |
| B Negative control | NC-K4: output data depends on out_ready_i (K4 hold; BMC depth 40: the squeeze phase is reached after about 30 cycles) | FAIL | FAIL | bmc=FAIL; failed assert keccak_sponge_formal_top.sv:122 | 38.6 | yes |

ALL AS EXPECTED

Reading: A passes by induction (base case and step), so K1 (busy_o exactly 24 cycles, counter 0..23, done pulse only after round 23), K2 (no xor while busy), K3 (word index below the rate, xor lane below the rate,
fixed-output index within the digest), K4 (a pending output word is held) and K5 (legal state, stop reaches IDLE) hold for every input sequence. NC-K1 (23 rounds) and NC-K4 (data depends on `out_ready_i`) fail as
required, so the proof is not vacuous. NC-K4 runs as BMC to depth 40 because the squeeze phase is reached only after about 30 cycles (one absorb word, one padding word, one 26-cycle permutation), beyond the
induction depth; the same device as NC-B of Phase 3.
