# Open decisions (team to decide; Claude must not assume an answer)

Update this list whenever something is decided (move it to an ADR) or discovered.

| # | Question | Why it matters | Blocks |
|---|---|---|---|
| 1 | **Target side**: accelerator for the *card / secure element* or the *reader*? | Sources place the bottleneck on the card chip (8-12 KB RAM); the DE10-Nano's HPS is far stronger than a card chip. Changes Sections 1-3 wording and the demo. | Phase 4; proposal Section 3 |
| 2 | **Declared subtheme** (02 Hardware Crypto Accelerator? 01 Secure Identity? other) and how to relate to the reference baselines | ML-KEM uses SHA-3/Keccak, not SHA-256, so the TT07 SHA-256 baseline is not reused directly; subtheme 02 stresses small, area-efficient blocks | Registration text |
| 3 | **Transfer mechanism**: DMA or plain memory-mapped access | A polynomial is only 3,072 bits; DMA setup may cost more than it saves | Phase 3 (decide by measurement) |
| 4 | **Randomness source** for prototype: HPS or an FPGA TRNG | TRNG needs its own statistical validation; currently out of scope | Phase 3 |
| 5 | **Hybrid mode** (classical ECDH + ML-KEM at the HPS): include? | BSI requires hybrid for production; adds scope | Phase 6 |
| 6 | **Second software baseline** (e.g. soft core in fabric at a low clock) | Cortex-A9 baseline may show little or negative speed-up | Phase 5 |
| 7 | **Emulated protocol / message flow** ("PQ-PACE" is not a standard; ICAO is still specifying) | Needed to define latency at protocol level | Phase 4 |
| 8 | **Board availability**: is a DE10-Nano provided or owned? (`jtagconfig` showed none on 2026-09-24; an older Cyclone III board is not a target: no HPS, Quartus II 13.1 only) | Without a board only simulation + Quartus evidence exist | Phases 3-5 |
| 10 | **Prior-art search** extension (IEEE Xplore, IACR ePrint, Google Patents) | Needed before any novelty wording beyond the current scoped claim | Before submission |
| 12 | Does the **Appendix** count toward the 6-page limit? | Decides where figures go | Section 3 layout |
| 13 | **Activate `rtl-agent-team` hooks** by running `/rtl-agent-team:rat-init-project` (creates `.rat/`)? The original blocker ("idea not chosen") is resolved by ADR 0001 | Its Stop-gates block ending a session after unverified RTL edits, which mechanically enforces verify-before-claim; but it also adds structure to the repo | Before Phase 1 |
| 33 | **ADR 0033 (Phase 9, C7-core as built):** accept the ML-KEM-768 core of Phase 9 (all pinned ACVP vectors pass in simulation; 17,620.5 ALM, 54 RAM blocks, 28 DSP, 49.280 MHz median, timing met at 40 ns at every seed; KeyGen 9,035-9,076, Encaps 10,691, Decaps 16,623 cycles) with the hash instance on the C5 sponge, or on the K0 sponge (about 2,500 ALM fewer, 26 cycles per permutation), and decide whether an optimisation (overlapped encode / decode) is wanted | Fixes the architecture for Section 3 of the proposal and for Phase 10 | Section 3, Phase 10 |
| 34 | **ADR 0035 (Phase 9M-1, two-byte codec path):** accept `CODEC_W2 = 1` as the configuration of the later Phase 9M items (adopted by its rule: KeyGen 8,327, Encaps 10,159, Decaps 15,515 cycles against 9,095, 10,735, 16,667 for the profile inputs; ALM median 17,654.0 against 17,620.5; median Fmax 48.855 against 49.280 MHz; timing met at 40 ns at every seed; ACVP 100 % on both simulators; MEASURED in simulation and kernel-only Quartus, `docs/evidence/phase09m-optimisation/9m1/result_9m1.md`). The default of the parameter stays 0 until accepted. | Decides the base configuration for items 2, 3 and 4 of Phase 9M (ADR 0034) | Phase 9M items 2-4, proposal numbers |

Closed: #9 FIPS 203 errata — accepted as ADR 0003 (2026-09-29, decided by Faza Dzil, Team J5).
Closed: #14 Phase 3 lane-count (L) selection criterion — accepted as ADR 0004 (2026-09-29,
decided by Faza Dzil, Team J5): primary = min cycle count within a 25% ALM budget
(10,478 ALM); secondary = informational AT re-check once timing is valid.
Closed: #15 Use the C2-K2-K1 supplementary configuration for the ADR 0004 L-selection — accepted
as ADR 0005 (2026-09-30, decided by Faza Dzil, Team J5): C2-K2-K1 adopted, L = 8 selected
(9,754 ALM, within the 10,478 ALM budget); Phase 4 starts from C2-K2-K1 at L = 8.
Closed: #16 Phase 4 target clock — accepted as ADR 0006 (2026-09-30, decided by Faza Dzil, Team J5):
two-tier; Phase 4 milestone 40.000 ns (25 MHz) as an experimental target, not a hardware or system
requirement; end goal 20.000 ns (50 MHz) after Phase 5, not a Phase 4 gate; one constraint for every
Phase 4 revision including the re-compiled P = 0 reference.
Closed: #17 Phase 4 pipeline depth P and selection rule — accepted as ADR 0007 (2026-09-30, decided by
Faza Dzil, Team J5): P in {0, 2, 4, 6}; registers allowed inside the memory access path and the divider;
function bit-exact; candidates must be bit-exact, constant-cycle, ALM <= 10,478 and meet timing at
40.000 ns; select minimum t_NTT = cycles_NTT/Fmax (lowest reported slow-corner Fmax), smaller P within
5% of the global minimum; no automatic selection if there is no candidate.
Closed: Phase 4 final selection (ADR 0008 proposed P = 4 under 25%; never accepted) — decided as ADR 0009 (2026-10-01,
decided by Faza Dzil, Team J5): L = 8, P = 6 (C3-P6); NTT-core design budget 30% = 12,573 ALM (replaces 25% for the
NTT core from Phase 4 on; not a system-level limit); targets per ADR 0006 unchanged (40 ns met, 50 MHz for Phase 5).
Closed: #18 Phase 5 timing objective — accepted as ADR 0010 (2026-10-01, Faza Dzil, Team J5): 50 MHz kept as a
best-effort project target, not a Phase 5 gate; ADR 0006 expectation corrected (C3-P6 critical path in the memory read
path, MEASURED); memory / P / schedule work in a separate phase or sub-phase after 5a/5b (name and position: #19).
Closed: #22 Phase 5 plan decisions D1–D8 and the 5b selection rule — accepted as ADR 0011 (2026-10-01, Faza Dzil,
Team J5): all suggestions of test plan §13 (40 ns for C4 revisions + 20 ns information compiles of final C4 and C3-P6;
12,573 ALM, Quartus defaults, DSP reported; 5c/5d after 5b; reading (ii) of 5a; no register moves in Phase 5; operand
contract [0, q); seeds 1–6 for 5b; 5b rule).
Closed: #20 acceptable cycle increase and #21 ALM limit for added registers — accepted as ADR 0012 (2026-10-01, Faza
Dzil, Team J5): more cycles only if t_NTT and t_INTT at the measured Fmax beat C3-P6 and constant-cycle holds; NTT
core ≤ 12,573 ALM stays the limit, exceeding it needs a new team decision.
Closed: #11 Repository licence — accepted as ADR 0016 (2026-10-02, Faza Dzil, Team J5): MIT License (`LICENSE`).
Closed: #19 Memory / schedule phase — accepted as ADR 0017 (2026-10-02, Jevan, Team J5): separate phase between Phase 5 and Phase 6, working name "Phase 5M", steps S6-S9; branch `phase5m-memory-schedule`.
Closed: #23 ADR 0013 (Phase 5b) — accepted 2026-10-02 (Jevan, Team J5): Barrett is the C4 reducer (DSP 9 -> 18 recorded).
Closed: #24 ADR 0015 (Phase 5d) — accepted 2026-10-02 (Jevan, Team J5): 5d not attempted in Phase 5, moves to Phase 6.
Closed: #28 S10 — ADR 0025 accepted 2026-10-03 (Jevan, Team J5, chat 2026-10-03: 'kan udah di adaptasi dan kita menggambil s10'): S10 (16 x 1R1W banks, P = 5, 118 cycles) is the NTT/INTT core for the next phases; Phase 6 top with S10.
Closed: #27 Phase 5M configuration — moot after ADR 0025 (as #28 stated): ADR 0021 (S7), 0022 (S9 study) and 0023 (S8) marked superseded by 0025 (2026-10-03, Jevan, Team J5).
Closed: scope of Phase 8 — ADR 0026 accepted 2026-10-03 (Jose, Team J5): 8a, 8b, 8c and 8d all go ahead (supersedes the skip of 8a/8c/8d in ADR 0019 point 2).
Closed: #29 C5 (ADR 0027), #30 W2 sampler (ADR 0028), #31 STREAM (ADR 0029), #32 OVERLAP (ADR 0030) — all accepted 2026-10-03 (Jo, Team J5, chat 2026-10-03: 'ya terima'); each was adopted by its rule and is MEASURED (docs/results/result_phase8.md).
Closed: #25 FIPS 203 input checks — accepted as ADR 0031 (2026-10-03, Jo, Team J5, chat 2026-10-03: 'HPS untuk sekarang karena papan tidak ada aksesnya'): the checks are done by the HPS, not in the RTL; not tested on a board.
Closed: #26 Checkpoint protocol — accepted as ADR 0032 (2026-10-03, Jo, Team J5, chat 2026-10-03: 'b'): one STOP per block; commits are made at the end of the work.
