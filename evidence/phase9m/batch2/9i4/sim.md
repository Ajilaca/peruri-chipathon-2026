# Phase 9I item 4 simulator runs, 2026-10-05 (V1-V7)

MEASURED (simulation only). Environment of the K4 runs: `CORE_TOP=mlkem_core4 CORE_SMP0=1 CORE_K0=1 CORE_W2=1 CORE_P6=1 CORE_AR=1` (K3 parameters). Raw cycle files: `cycles_verilator_core_k4.json`, `cycles_icarus_core_k4.json`; profile `profile_k4_verilator.json`.

## V1 lint, V2 model (re-run 2026-10-05 for this report)
- `verilator --lint-only -Wall --top-module mlkem_core4 -GCODEC_W2=1 -GNTT_P6=1 -GNTT_AR={0,1} -GSMP_C5=0 -GHASH_C5=0` on the file list of `tb/mlkem/run_core_tests.py`: rc 0, **0 warnings** at both `NTT_AR` values. `slang --top mlkem_core4` (same parameters, `NTT_AR = 1`): `Build succeeded: 0 errors, 0 warnings`.
- `python3 scripts/build/gen_mlkem_ctl_rom3.py --check`: `rtl/mlkem/mlkem_ctl_rom3.sv equals the generated ROM; static checks passed` (`check_static3`). The comparison of `mlkem_ctl_model3` with `mlkem_ctl_model2` on the four operation variants was made while the model was built and is not re-run here.
- Note: the Verilator build of the profile run prints a `UNOPTFLAT` warning for `kpke_sched_smp4` (`tb_we_i` through the grant to `tb_wready_o`; a combinational loop in the build-time analysis, not an error: the simulation passes). It was not seen in the `--lint-only` runs above, which use `-Wall` without `--timing`.

## V3 core K4 (the whole `core` target)
Verilator and Icarus print the same values:
```
ACVP keyGen: 25 vectors equal
ACVP encapsulation: 25 vectors equal
ACVP decapsulation: 10 vectors equal
20 random cases equal (keygen, encaps, decaps valid and modified, chain)
constant cycles: Encaps [9555], Decaps [12933]; KeyGen over the ACVP seeds: min 8344, max 8397
[verilator] core: 6/6 PASS
[icarus] core: 6/6 PASS
[icarus] nclen: test_acvp_encaps failed as required: True
[icarus] TOTAL: 7/7 passed
```
Encaps and Decaps cycle counts are identical across the tested inputs (K3: 10,194 and 15,563; so -639 and -2,630 cycles on the test inputs, the same differences as on the profile inputs). The Icarus run is the full ACVP set (about 1 hour); the Verilator run is the same set.

## V4 profile at K4 (Verilator; cycles per controller state, fixed inputs)
| Operation | Total (cycles) | States with more than 100 cycles |
|---|---|---|
| KeyGen | 8,416 | RUN 6,740, STP 1,578 (unchanged from K3) |
| Encaps | 9,611 | RUNJ 6,245, LDP 2,068, STP 1,052 |
| Decaps | 12,989 | RUNJ 6,367, LDP 5,047, STP 1,315, CMP 138 |
The state `RUNJ` is the join: it counts the cycles the controller waits for the engine after the loads that ran behind it; the loads are counted in `LDP` as before. Cycle detail beyond these is in the json. K3 for comparison (`../9s2b/profile_k3_verilator.json`): Encaps RUN 8,060 + LDP 1,044; Decaps RUN 11,177 + LDP 2,871.

## V5 and V6 controls on `mlkem_core4` (Verilator; the repository RTL is never mutated, copies only)
```
[verilator] nclen:   failed as required: True
[verilator] ncoff:   failed as required: True
[verilator] ncrom:   failed as required: True
[verilator] ncprio:  failed as required: True
[verilator] ncwr:    failed as required: True
[verilator] ncjob:   failed as required: True
[verilator] ncthr:   throttled sidecar passes the whole core target: True
[verilator] ncilk:   (host port throttled, interlock removed) failed as required: True
[verilator] ncthrld: (host port granted one cycle in eight, interlock intact) passes the whole core target: True
[verilator] ncgrant: (host write written although the sequencer writes) failed as required: True
[verilator] ncjoin:  (RUNJ does not wait for the engine) failed as required: True
```
**Run note:** the first run of the item-4 controls (`ctl_v.log`) gave 9 of 11: `ncthrld` failed the constant-cycles test and `ncgrant` did not fail. Both were faults of the control, not of the design: the throttle counter of `ncthrld` ran free and was not reset when the controller was idle, so the cycle counts depended on the phase of the counter; and `ncgrant` mutated a gate that the loader already applies (the mutation was void). Both were fixed in `tb/mlkem/run_core_tests.py` (the counter resets in idle; the mutation moved into `mlkem_ldpoly2o.sv`) and the controls re-run (`ctl2_v.log`, 3 of 3 as listed above, with Encaps 11,559 and Decaps 27,444 cycles in the throttled `ncthrld` case, constant across inputs). The eleven results above are the second run for `ncilk`, `ncthrld` and `ncgrant` and the first run for the others.

## V7 regression
- `mlkem_core3` at K3 gives the K3 profile (8,416 / 10,250 / 15,619; `../9s2b/sim.md`), its files are not edited by item 4.
- `mlkem_core` at the defaults (Phase 9, Verilator): 6/6 PASS, Encaps 10,691 and Decaps 16,623 on the test inputs (`../9s2b/sim.md`); the defaults of the shared files (`NTT_P6 = 0`, `NTT_AR = 0`) are unchanged.
- The K-PKE engine sequencer test with the K3 parameters: 3/3 on both simulators (`../9s2b/sim.md`). The engine variant `kpke_sched_smp4` is exercised through `mlkem_core4` only; it has no separate sequencer unit test (stated).

## What this does not show
Simulation only. The interlock is tested by ACVP and the controls `ncilk` / `ncthrld`; the throttled host port tests one stall pattern (one grant in eight cycles), not all of them. The formal evidence is in `formal.md`.
