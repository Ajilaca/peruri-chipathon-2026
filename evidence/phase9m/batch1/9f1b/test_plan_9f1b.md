<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Phase 9F step S1b: hash running beside other work (background hash) — test plan and adoption rule

Written 2026-10-04 before any S1b RTL and before any S1b measurement. Scope: ADR 0036 (Accepted, Faza Dzil, step S1b of the Fmax plan) and the batch plan of chat 2026-10-04 ("s1b (batch 1) baru masuk batch 2": S1b belongs to Batch 1, S2 + S3 + item 4 are Batch 2). Baseline: K1 (S1, `test_plan_9f1.md`: K0 sampler, K0 hash, two-byte codec) in `rtl/mlkem/mlkem_core2.sv`. Labels: MEASURED, ESTIMATE, INFERENCE, perhitungan tim. The mathematics is locked (C1): the same hashes of the same bytes are computed; only when they run changes.

## 1. Why (from the K1 profile, MEASURED in simulation, `../9f1/profile_k1_verilator.json`)
The hash unit is used by the controller one micro-operation at a time. Three hashes do not depend on the work next to them:
- KeyGen: `H(ek)` (HST, HFD 148 words, HGT, about 395 cycles at K0) needs t_hat and rho only; it can run during the three stores of s_hat (STP 0, 1, 2, 3 x 265 cycles), which touch other words of the same memory.
- Encaps: `H(ek)` (about 394 cycles) needs ek only; the loads of t_hat and of the message (RD32, LDP 7, 8, 9, 11, about 1,070 cycles) do not need it. Only the following `G(m || H(ek))` needs it.
- Decaps: `J(z || c)` (about 390 cycles) needs z and the ciphertext only; it can run during the first loads and the decryption run (RUN 2, 3,111 cycles). Its result is first used by the final comparison.
`G(d || k)` of KeyGen and `G(m' || h)` of Decaps are on the dependency chain and stay in the foreground.

## 2. Design (new text only in `rtl/mlkem/mlkem_core2.sv`, a new ROM and the golden model; the Phase 9 / 9M / S1 files keep their behaviour)
1. **Sidecar sequencer:** a second small state machine (B_IDLE, B_FETCH, B_DISP, B_HFD, B_HGT) with its own program counter and instruction register runs a *hash job*: the words HST, HFD..., HGT, END stored in the program memory after the main program. It has its own copy of the feeder and digest counters. The main controller gets two micro-operations: `BGS pc` (start the job at word `pc`; the main controller continues at once) and `JN` (wait until the job has finished, including the write of the digest). The main micro-operations are unchanged.
2. **One hash unit:** while a job runs it is owned by the sidecar; the main controller must not start a hash then (guaranteed by the program and checked statically in the model, by a hardware check below, and by a formal property). The inputs and outputs of `mlkem_hash` are multiplexed by the owner.
3. **Read bus (one read port per memory, data valid the cycle after the address):** a request of the main controller always wins; the sidecar issues a request only in a cycle in which the main controller issues none; the memory region select follows the request granted in the previous cycle. The main controller is never delayed by the sidecar (its cycle counts do not depend on the job).
4. **Write bus (one write port):** the digest words of the sidecar go to the register file only in a cycle in which the main controller does not write (`out_ready` of the hash is low otherwise).
5. **Safety in hardware:** `END` of the main program waits until the sidecar is idle (the result registers are complete when `done_o` rises); the main `HST` is ignored while a job runs only if the ROM is wrong (flagged by a formal property, not corrected).
6. **ROM and model:** `tb/golden/mlkem_ctl_model2.py` builds the new programs from the Phase 9 model (same golden primitives; ops BGS and JN, job words after END); `scripts/build/gen_mlkem_ctl_rom2.py` generates `rtl/mlkem/mlkem_ctl_rom2.sv` (`--check`). The new programs: KeyGen: `... STP 3, 4, 5; WR32 rho; BGS(H(ek)); STP 0, 1, 2; JN; WR32 H(ek); WR32 z`. Encaps: `BGS(H(ek)); RD32 rho; LDP 7, 8, 9, 11; JN; G; SDL; RUN; STP ...`. Decaps: `BGS(J); LDP 3, 4, 5, 10, 0, 1, 2; RUN 2; STP 10; JN; G; RD32 rho; re-encryption; CMP; END` (J is done long before the end of the 3,111-cycle decryption run, so JN does not wait; it stands before `G` because `G` needs the hash unit). In general `JN` is placed immediately before the first main hash or the first use of the job's result.
7. **Static checks of the model** (`check_static2`): every job is HST / HFD / HGT / END with the HFD words covering the hash length; between `BGS` and `JN` the main program issues no HST, HFD, HGT, no read or write of the job's destination registers, and no write into a word range that the job reads; every `BGS` has its `JN` before `END`; the golden outputs of the new programs equal those of the Phase 9 programs.
Program words: the largest program stays below the 64-word address space (pc is 6 bits).

## 3. Estimates written before measuring (ESTIMATE; the hash costs are MEASURED in the K1 profile: KeyGen 395, Encaps 394, Decaps 390 cycles for the hash micro-operations that move to the background)
| Quantity | K1 (MEASURED) | K1b ESTIMATE |
|---|---|---|
| Cycles KeyGen / Encaps / Decaps (profile inputs) | 8,795 / 10,627 / 15,983 | about 8,410 / 10,240 / 15,600 (about -385 each: the moved hash minus BGS, JN and one wait cycle) |
| ALM median | to be measured in S1 (ESTIMATE of S1 was about 13,400; first two seeds 14,066 / 14,106) | S1 + 150 to 450 (second sequencer, second ROM instance, multiplexers) |
| Registers | S1 | S1 + 100 to 250 |
| RAM blocks / DSP | 54 / 28 | 54 / 28 |
| Fmax | S1 | within 2 % of S1 (new multiplexers on the read address and the hash input; INFERENCE: not on the critical path of S1 at 15 ns, V9 checks) |
| Cycles seen by the main controller of LDP and STP | 263 / 265 | equal (the sidecar never delays it) |

## 4. Tests (both simulators; the repository RTL is never mutated)
| # | Test | Pass condition |
|---|---|---|
| V1 | lint Verilator `-Wall` and slang of `mlkem_core2` with the new ROM at K1 and at the defaults | 0 warnings, 0 errors |
| V2 | model: `check_static2`; the new programs give the same keygen / encaps / decaps outputs as the Phase 9 programs for the ACVP vectors and 200 random cases; `gen_mlkem_ctl_rom2.py --check` | all pass |
| V3 | core K1b: the whole 9c `core` target (ACVP keyGen 25, encapsulation 25, decapsulation 10, random cross-check, chain, protocol, constant cycles) | 100 % equal, both simulators |
| V4 | profile at K1b | recorded; the per-state counts of LDP, STP, RUN, SDL, WR32, RD32, CMP equal to K1; the hash states disappear from the main program except G (HFD / HGT of G) |
| V5 | constant cycles: Encaps identical for different m and ek-independent; Decaps identical for valid and rejected ciphertexts; KeyGen spread only from public sampling | as 9c V6 |
| V6 | negative controls on copies: NC-PRIO (the sidecar read wins over a main request) -> V3 ACVP must FAIL; NC-WR (the digest write ignores a main write in the same cycle) -> V3 ACVP must FAIL; NC-ROM (the job reads word offset + 1) -> FAIL; NC-JOIN: a **throttled** copy (the sidecar issues one read every 16 cycles so that the job outlasts the main work) must PASS with the join, and the same throttled copy with `JN` removed must FAIL (shows that the join is effective, not only never needed) | each as stated |
| V7 | formal (sby, protocol stubs as 9c): the 9c properties E1 (two copies, different data, equal control: non-interference) and S1-S7 for `mlkem_core2`; new: B1 the main controller never starts the hash while a job runs; B2 `done_o` only when the sidecar is idle; B3 the main controller leaves JN only when the sidecar is idle; B4 the sidecar writes only the register file, only addresses of its destination registers; B5 the sidecar read address stays inside its memory; controls (a mutant that removes the check of B1 / B3 must make them FAIL) | PASS, controls FAIL |
| V8 | regression at the defaults: `mlkem_core` default profile equals the Phase 9 profile, and `mlkem_core2` at SMP_C5 = 1, HASH_C5 = 1, ROM old equals `mlkem_core` (cycles) | PASS |
| V9 | Quartus K1b seeds 1-6 at 40.000 ns (the gate) and K1b-15 seeds 1-6 at 15.000 ns (information, ADR 0036 point 3), one at a time; critical-path classification at 15 ns | extracts; timing met at 40 ns at every seed; at 15 ns the number of seeds met and the Fmax reported |
Batch rule (chat): V1-V8 are the fast gates after each step; V9 (slow gate) runs once for the final design of Batch 1.

## 5. Adoption rule (fixed before measuring; ADR 0036: by latency)
S1b is **adopted** on top of S1 only if all hold:
1. V1-V8 pass as stated (any ACVP mismatch rejects it).
2. Timing met at 40.000 ns at every seed 1-6.
3. ALM median at most 20,000 (the budget).
4. For each of KeyGen, Encaps and Decaps, t = cycles / median Fmax at the 15 ns constraint (lowest slow corner, seeds 1-6) of K1b is lower than that of K1 (from the S1 campaign).
5. At 15 ns: the number of seeds that meet it is reported (statement "met at k of 6 seeds"); if K1b meets fewer seeds than K1 the rule is applied to the seeds that meet it in both and the difference is stated.
Otherwise K1b is reported as not adopted and the S1 configuration stays. The result is a Proposed ADR.

## 6. Not in this step
No change to the engine (frozen), no overlap of loads and stores with the engine (item 4, Batch 2), no second sampler (S3), no S2 change; no board result; constant time means cycle-count invariance only.

## 7. Amendment A1 (2026-10-04, written while building; nothing above is edited and the rule of section 5 is unchanged)
1. **New module `rtl/mlkem/mlkem_core3.sv`** instead of editing `mlkem_core2.sv` (section 2 and the header of section 4 say "in mlkem_core2"): the Quartus campaign of S1 (`quartus/phase09f1_core`, twelve revisions) reads `mlkem_core2.sv` while it runs. `mlkem_core3` is `mlkem_core2` plus the sidecar and `mlkem_ctl_rom2` instead of `mlkem_ctl_rom`; the parameters are those of `mlkem_core2` (SMP_C5, HASH_C5, CODEC_W2). Quartus revisions K1b use `mlkem_core3.sv` and `mlkem_ctl_rom2.sv`.
2. **Hardware guards beyond section 2 item 5:** a main `HST`, `BGS` or `JN` that meets a running job waits in DISP (the program is then slower but its hash is still correct); `END` waits for the job. They cost nothing in a correct program. Register hazards (reading a job's destination register before `JN`) are not detected in hardware; they are excluded by `check_static2` and by simulation.
3. **Write bus detail:** the digest write of the sidecar goes to the register file only when the main controller does not write in that cycle (`fw_en`); in the same cycle the hash output is stalled (`out_ready` low).
4. **Test runner:** `CORE_TOP=mlkem_core3` selects the module and the ROM; the control `nclen` mutates `.len_i(hx_len)`.
