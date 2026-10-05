<!-- claim-lint: skip-file (internal study, not proposal text) -->
# Phase 5M S9: M10K / synchronous-read study (documentation only; no RTL, no Quartus run)

Plan: `evidence/phase05m/test_plan_s9.md` (with Amendment A1). Analysis output: `port_analysis.txt` (`scripts/test/phase5m_s9_port_analysis.py`). No adoption rule: the team chooses (C5).
Labels: **MEASURED** (Quartus report or simulation in this repo), **INFERENCE** (arithmetic or reasoning on measured values), **ESTIMATE** (method written next to it), **NOT VERIFIED / NOT MEASURED**.

## 1. Where the memory stands today
- Storage is **flip-flops**, not M10K: 256 x 12 bit = 3,072 bits in 8 banks of 32 words, asynchronous (combinational) read. MEASURED: the Phase 2 compile inferred 0 M10K for the banked memory
  (`evidence/phase02/quartus_C1_vs_C0.md`, Section 4; "M10K NOT achieved, async-read limitation"). The M10K counts of the later revisions (S7: 31, S8: 33, M6 29) are tool-inferred
  and were not attributed to a block in this study (INFERENCE: not the polynomial storage).
- Cost (MEASURED, Phase 4, `evidence/phase05/baseline/decision_package.md`): the memory entity was 6,964.6 ALM at P = 2 and 7,621.2 ALM at P = 4 (+39.5 from P = 4 to P = 6), i.e. about
  7,660 ALM at P = 6 (INFERENCE, sum) of 10,505 ALM for the whole C3-P6 core. Today's S7 core has 9,361-9,405 ALM in total (`s7/selection_worksheet.md`).
- Timing (MEASURED): the read segment (address decode, 16-port slot arbitration, read mux) was 21.292 ns of a 29.345 ns path in C3-P6 (`baseline/c3p6_critical_path.md`); splitting it with one register (S7)
  raised the median Fmax from 34.430 to 38.720 MHz; a write-path register (S8) did not help (37.99 MHz).

## 2. Port demand of the schedule (MEASURED by the model of the real address schedule, `port_analysis.txt`; perhitungan tim, no hardware)
| Case | reads / bank / cycle | writes / bank / cycle | reads + writes |
|---|---:|---:|---:|
| Current 8-bank map, NTT and INTT, writes P = 7 cycles after the reads | 2 | 2 | **4** |
| Candidate 2: 16 banks, `bank = (a1^a2^a3^a4, a7, a6, a5)`, `offset = a[3:0]` | **1** | **1** | 2 |
| Candidate 1 (first hand derivation) | 2 | 2 | 4 (refuted) |
| Negative control `bank = a[7:4]` | 2 | 2 | 4 |
| Negative control `bank = a[3:0]` | 16 | 16 | 16 |

Reading (INFERENCE): a true-dual-port M10K does two port operations per cycle (the repository's Phase 2 plan counts "<= 2 accesses per bank per cycle" against that capacity; the Intel handbook was **not** re-read in this
study: NOT VERIFIED here). The current map needs four per bank in some cycles (two reads and two writes), so it does **not** fit one M10K per bank. Candidate 2 needs exactly one read and one write per bank per cycle
over the whole timeline of both directions (every layer boundary included); it is bijective (256 distinct (bank, offset)) and balanced (16 words per bank). That is the **simple dual port (1 read + 1 write)** pattern
of an M10K.

## 3. Options (ADR 0017's list), with what each needs and costs
| Option | What it is | Evidence in this study | Cost (ESTIMATE, method) | What must be proved before RTL |
|---|---|---|---|---|
| **A. 16 x 1R1W banks (candidate 2)** | 16 banks of 16 x 12 bit, one M10K block per bank, synchronous read; read crossbar (bank -> butterfly port) and write crossbar (port -> bank) driven by a ROM from the golden address model; **no slot arbitration** (the arbitration ripple and its register cut disappear) | conflict-free over the whole timeline (section 2); controls conflict as required | M10K: 16 blocks (16 x 192 bits, about 2 % of each block's 10 Kbit) = 2.9 % of the fitter's 553 (perhitungan tim); the ~3,000 storage flip-flops go away (INFERENCE from 3,072 bits); crossbars: <= 5 ALM per output bit for a 16:1 mux (a 16:1 mux = four 4:1 + one 4:1; 6 inputs per 4:1; assumes one ALM per 6-input function) x 16 outputs x 12 bits = **<= 960 ALM per crossbar, <= 1,920 ALM for both** (upper bound, not measured) | synchronous-read latency and output register (NOT MEASURED); read-during-write behaviour of the M10K mode for the same address in one cycle (the schedule never does it: formal property C of S7/S8; the block mode must still be chosen deliberately, NOT VERIFIED); crossbar ROM generated from `addr_pair` and checked entry by entry; new formal bank property (<= 1 read and <= 1 write per bank); core vs golden, scoreboard, negative controls (a map with a conflict must fail); host access during IDLE/DONE on the same ports; Quartus must report 16 RAM blocks for the storage (the Phase 2 lesson) |
| B. Two coefficients per word (24-bit words, 128 deep) | a word holds a, a ^ (1 << m) | a butterfly needs j and j + len, which differ in exactly bit log2len; for any m only the layer with log2len = m (one layer per direction) finds both operands in one word | no ALM estimate: not useful | not pursued: six of seven layers still need two words per butterfly |
| C. Double-pumping (memory at 2x the core clock) | two memory accesses per core cycle | not evaluated: needs the M10K maximum frequency (NOT VERIFIED) and a second clock domain with a documented crossing (CLAUDE.md rule 7); with candidate 2 the need disappears | not estimated | only if A is rejected |
| D. Schedule change (fewer lanes) | lower port demand, L = 4 instead of 8 | cycles per layer = 128 / L doubles (INFERENCE); contradicts the cycle goal | not estimated | not pursued |
| E. Keep flip-flop storage (S7 today) | no change | MEASURED, `s7/selection_worksheet.md` | 0 | none (current verified state) |

## 4. What this study does and does not show
- Shows (model of the real address schedule): a 1R1W conflict-free 16-bank map exists for L = 8, P = 7 timeline, both directions. A hand derivation of the map was wrong once and was caught by the script (Amendment A1).
- Does not show: any Fmax, ALM or M10K number for an M10K-based memory (nothing was compiled); that the crossbars are faster than the current read mux; that the read-during-write behaviour is safe in the chosen M10K mode;
  anything about the stall pattern of S8 (the same one-issue-cycle-to-write structure holds, but it was not re-run for P = 8); the pointwise product (base-case multiply) memory traffic, which the NTT core does not include.
- Intel device facts (M10K capacity per block of about 10 Kbit is derived from the product table in `docs/proposal/references.md` [22]: 5,570 Kb over 557 blocks; port modes, read-during-write modes and maximum frequency are from
  general knowledge and **NOT VERIFIED here**: check the Cyclone V Device Handbook, Embedded Memory chapter, before any RTL).

## 5. Decision for the team (ADR 0022, Proposed)
1. Do nothing more with memory before the deadline (S7 is the measured best; Phase 6 / 7 continue). 2. Open one experiment "S10: 16 x 1R1W M10K banks (option A)" as its own step with a test plan and the ADR 0012
rule, **after** the deadline-critical blocks (Keccak, samplers); effort ESTIMATE 4-6 h including formal and a six-seed Quartus sweep (assumption: comparable to S7 plus S8 of this session). 3. Other.
