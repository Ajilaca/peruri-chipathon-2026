<!-- claim-lint: skip-file (internal decision aid, not proposal text) -->
# Decision package for the 50 MHz work (input to ADR 0010 follow-up; nothing here is decided)

Labels: **MEASURED** (Quartus report or simulation log in this repo), **INFERENCE** (arithmetic on measured values),
**ESTIMATE** (projection; method stated). Two questions for the team: (a) how much cycle increase is acceptable if
stalls are needed; (b) whether the 12,573-ALM limit stays fixed for added registers.

## (a) Cycle increase - what matters is time per transform, t = cycles / Fmax
Starting point (MEASURED, C3-P6 default seed): NTT 119 cycles, INTT 375 cycles, lowest slow-corner Fmax 34.19 MHz →
t_NTT = 3.481 µs, t_INTT = 10.968 µs (INFERENCE).

Break-even (INFERENCE): at a clock F, a configuration is faster than C3-P6 today only if its cycle count stays below
3.481 µs × F (NTT) and 10.968 µs × F (INTT):

| Clock | NTT may take up to | INTT may take up to |
|---|---:|---:|
| 40 MHz | 139 cycles | 438 cycles |
| 45 MHz | 156 cycles | 493 cycles |
| 50 MHz | 174 cycles | 548 cycles |

Stall cycles per pipeline depth P (`stall_cycles.txt`, `scripts/test/phase5_stall_cycles.py`; minimum stall per
boundary found by search over the real L = 8 address schedule, then re-checked for all 256 addresses):

| P | Stalls NTT (per boundary) | Stalls INTT (per boundary + scaling) | NTT / INTT cycles | Increase vs C3-P6 | t_NTT at 40 / 45 / 50 MHz (µs, ESTIMATE) |
|---|---|---|---|---|---|
| 6 (today) | none | none | 119 / 375 (MEASURED) | - | 2.975 / 2.644 / 2.380 |
| 7 | none | none | 120 / 376 | +1 (0.8 %), +1 (0.3 %) | 3.000 / 2.667 / 2.400 |
| 8 | 1 at boundary 4 | 1 at boundary 3 | 122 / 378 | +3 (2.5 %), +3 (0.8 %) | 3.050 / 2.711 / 2.440 |
| 9 | 2 | 2 | 124 / 380 | +5 (4.2 %), +5 (1.3 %) | 3.100 / 2.756 / 2.480 |
| 10 | 3 | 3 | 126 / 382 | +7 (5.9 %), +7 (1.9 %) | 3.150 / 2.800 / 2.520 |
| 12 | 5 + 1 | 1 + 5 | 131 / 387 | +12 (10.1 %), +12 (3.2 %) | 3.275 / 2.911 / 2.620 |

- Cycle counts for P ≥ 7 are ESTIMATE: the Phase 4 measured relation (NTT = 113 + P, INTT = 369 + P, 0 stall for
  P ≤ 6) plus the stalls found here; they must be confirmed in simulation. The scaling pass needs no stall up to
  P = 15 (slack 15).
- Consistency check: Phase 4's negative control (depth 8 without stalls) produced wrong results
  (`evidence/phase04/cocotb_regression.txt`); this table says P = 8 needs exactly one stall
  per transform.
- **Constant cycles:** the stall count depends only on P, the direction and the fixed address schedule - never on
  polynomial data - so every input gives the same count (the CRG-7 rule is unchanged; only the value 119 / 375 would
  change, via an ADR).
- Times at 40 / 45 / 50 MHz are hypothetical clocks, not measured Fmax. A deeper P is worth it only if Fmax rises
  by more than the cycle increase: e.g. P = 8 needs Fmax > 34.19 × 122 / 119 = 35.05 MHz just to break even with today
  (INFERENCE).

**Plain reading:** if stalls add 3 cycles (2.5 %), NTT takes 2.440 µs at 50 MHz versus 3.481 µs today; even +12
cycles (10 %) gives 2.620 µs at 50 MHz. The cycle increases in this table are small compared with what a higher clock
would give - **but only if the clock really rises**, which only a compile can show.

## (b) ALM limit for added registers
MEASURED starting point: C3-P6 10,484–10,516 ALM over seeds 1–6 → margin to 12,573: 2,057–2,089 ALM (INFERENCE).
Seed-to-seed spread 32 ALM (P = 6) and 64 ALM (P = 4). Under the GHRD's global settings the same core needs 11,053 ALM
(+548; +993 for C3-P4), margin 1,520 ALM (INFERENCE) - compile settings are budget-relevant.

What one pipeline stage cost in Phase 4 (MEASURED totals and per-entity values from `quartus/phase04_pipeline_c3/
output_files_P{2,4,6}/C3-P*.fit.rpt`; differences INFERENCE):

| Step | Cuts | Δ ALM total | Δ registers | Δ memory entity ALM | Note |
|---|---|---:|---:|---:|---|
| P0 → P2 | + A_13, D_3 | −27 | +720 | (P0 is a different core file) | registers packed into ALMs already in use |
| P2 → P4 | A_13, D_3 → A_7, M, X, D_7 | +743 | +328 | +656.6 (6,964.6 → 7,621.2) | the cut M after slot arbitration is the expensive one |
| P4 → P6 | → A_4, A_11, M, X, D_5, D_11 | +66 | +23 | +39.5 | two arbitration cuts instead of one |

Per stage this is −13.5 to +371.5 ALM (INFERENCE, Δ/2). **The cost depends on where the register goes, not on its bit
count**: a stage after slot arbitration cost about 650 ALM; stages inside the reducer cost almost nothing.

Bits per proposed lever (ESTIMATE from signal widths in `rtl/mem/poly_mem_multiport_pipe.sv` and
`rtl/ntt/butterfly_shared_pipe.sv`; 8 banks × 32 words, 2 read slots per bank, 16 ports, 12-bit data):

| Lever (cheap → expensive) | New registers (ESTIMATE) | P change / cycles | ALM (ESTIMATE, bounded by the measured range above) |
|---|---|---|---|
| 1. Split the read mux (word inside bank, then bank/slot) | 8 banks × 2 slots × 12 bit = 192 data bits + per-port bank/slot select ≈ 64 bits | P → 7, no stall (+1 cycle) | 0 to about 650 |
| 2. Remove `sub_mod` from the critical segment (5c, lazy `b + q − a`) | none (1 bit wider multiplier input) | none | small; reducer must accept [0, 2q) |
| 3. Shorter reducer (5a/5b) so a reducer register can move to the read/write path | none (count stays 3) | none | reducer difference; today's reducers total 1,395.8 ALM (MEASURED, upper bound of any saving) |
| 4. Register in the write path before `add_mod` / write mux | 8 lanes × 24 data bits = 192 + delayed write address/slot ≈ 16 × 9 = 144 | P + 1 | 0 to about 650 |
| 5. P > 7 with stalls (table (a)) | as levers 1/4 per extra stage + stall control | +1 to +12 cycles | per stage as above |
| 6. Synchronous-read M10K memory | storage moves to M10K; 2R + 2W per bank per cycle does not fit one true-dual-port M10K | schedule change likely | not estimable without a design |

Plain reading: levers 1 and 4 together could cost up to about 1,300 ALM (ESTIMATE, worst case of the measured
range) against a margin of about 2,060 - they fit on paper, but with little room left and with seed and settings
effects of 32–993 ALM. A cheaper reducer from 5a/5b would give room back; how much is known only after 5a/5b are
compiled.

**Scope reminder:** the 12,573-ALM figure is the NTT-core design budget of ADR 0009, not a system budget. Keccak, the
samplers, the KEM controller, encode/compress, storage, the HPS bridge and SignalTap are NOT MEASURED, so nothing
here says the full ML-KEM system fits.

## Suggestions (only suggestions; the team decides)
- (a) Accept a cycle increase as long as t_NTT and t_INTT at the **measured** Fmax are better than C3-P6
  (3.481 / 10.968 µs) and the constant-cycle check passes; no fixed percentage.
- (b) Keep 12,573 ALM as the gate; if a needed lever would exceed it, bring that to the team as a decision instead of
  changing the limit silently; ALM saved by 5a/5b counts as room for added registers.

## Correction (2026-10-01, later the same day; nothing above was deleted)
The stall table in (a) uses the Phase 4 planning model (`scripts/test/pipeline_hazard_slack.py`), in which a butterfly
reads at the cycle it is issued, so the stall condition depends on the whole depth P. The first Phase 5 core
negative control showed that this is conservative: with RdLat 1 + WrDly 7 (P = 8) the results stayed correct on both
simulators (`../5a/negctl_first_attempt_rd1_wr7.txt`), because the memory reads RdLat cycles after the
request. On this evidence (INFERENCE, one configuration) the stall condition depends on **WrDly = P − RdLat**:
registers added before the read (e.g. lever 1, splitting the read mux) would need **no** stall (cycles still rise by
the drain, +1 per stage), and the table's stall counts apply to registers added after the read. The cycle-count table is therefore an upper bound; the memory
/ P phase must confirm the physical model in simulation. ADR 0012's rule (judge by measured time) is unaffected.
