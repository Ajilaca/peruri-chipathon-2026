<!-- claim-lint: skip-file (internal analysis, not proposal text) -->
# Butterfly pipeline depth P: stall-free limit of the lane schedule and effect on the core, 2026-10-04

Planning analysis (perhitungan tim, no RTL, no Quartus run of P = 16): output of `scripts/pipeline_hazard_slack.py` (Phase 4 aid; read-after-write slack at the layer boundaries of the lane schedule `tb/mem/bank_model.py`), plus arithmetic from Phase 4 (`docs/results/result_phase4.md`: NTT / INTT cycles = 113 / 369 + P), the S10 core (118 cycles at P = 5, Phase 6) and the profile of the core (`profile_2026-10-04.md`). INFERENCE: the model assumes the S10 core has the same layer-boundary dependency as the Phase 4 core (same lane schedule).

```
Layer-boundary slack (cycles) of the current lane schedule; a pipeline of depth P needs no
stall at a boundary iff slack >= P.
L=1 NTT  T=128: slack per boundary [63, 95, 111, 119, 123, 125] -> largest stall-free P = 63
L=1 INTT T=128: slack per boundary [125, 123, 119, 111, 95, 63] -> largest stall-free P = 63
L=1 INTT last layer -> scaling pass: slack 127 (no stall before the scaling pass iff slack >= P)
L=2 NTT  T= 64: slack per boundary [63, 31, 47, 55, 59, 61] -> largest stall-free P = 31
L=2 INTT T= 64: slack per boundary [61, 59, 55, 47, 31, 63] -> largest stall-free P = 31
L=2 INTT last layer -> scaling pass: slack 63 (no stall before the scaling pass iff slack >= P)
L=4 NTT  T= 32: slack per boundary [31, 31, 15, 23, 27, 29] -> largest stall-free P = 15
L=4 INTT T= 32: slack per boundary [29, 27, 23, 15, 31, 31] -> largest stall-free P = 15
L=4 INTT last layer -> scaling pass: slack 31 (no stall before the scaling pass iff slack >= P)
L=8 NTT  T= 16: slack per boundary [15, 15, 15, 7, 11, 13] -> largest stall-free P = 7
L=8 INTT T= 16: slack per boundary [13, 11, 7, 15, 15, 15] -> largest stall-free P = 7
L=8 INTT last layer -> scaling pass: slack 15 (no stall before the scaling pass iff slack >= P)
```

## Reading (L = 8)
- Largest stall-free P = 7. For P = 16 the stall at a boundary is P - slack: NTT boundaries (slack 15, 15, 15, 7, 11, 13) stall 1 + 1 + 1 + 9 + 5 + 3 = 20 cycles; INTT boundaries (13, 11, 7, 15, 15, 15) stall 3 + 5 + 9 + 1 + 1 + 1 = 20 cycles, plus 1 before the scaling pass (slack 15).
- Cycles per transform: 118 at P = 5 (MEASURED, S10). At P = 16: +11 (latency) + 20 stalls = about 149 (NTT); INTT about 170 (ESTIMATE).
- Transforms per operation (counters of the programs): KeyGen 6 NTT; Encaps 3 NTT + 4 INTT; Decaps 11 transforms (decrypt 3 NTT + 1 INTT, re-encryption 3 NTT + 4 INTT). At 118 cycles each the NTT core is busy 708 / 826 / 1,298 cycles = 8.5 % / 8.1 % / 8.4 % of 8,327 / 10,159 / 15,515 (9M-1 core).
- P = 16 adds about 186 / 301 / 446 cycles (+2.2 % / +3.0 % / +2.9 %).
