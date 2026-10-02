<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Phase 5M, step S9: M10K / synchronous-read study (documentation only, no RTL) — plan

Written 2026-10-03, **before the analysis script was written or run**. Scope: ADR 0017 (S9 = "M10K / synchronous-read study: documentation only, no RTL; port needs vs M10K, options (more 1R1W banks, two
coefficients per word, double-pumping, schedule change), conflict-free evidence conditions, ESTIMATE-labelled ALM / M10K; the team chooses; no adoption rule"). ADR 0019 had dropped S9 for the
deadline; it is done now because the team asked for it in chat on 2026-10-03 ("s9 sekalian dikerjain"); amendment note 3 of ADR 0019 records that. Labels: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED.

## 1. Questions the study answers
Q1. What does the NTT/INTT schedule at L = 8 demand from each memory bank per cycle (reads, writes, together), with the current 8-bank map and with the P of S7?
Q2. Does that fit an M10K block (true dual port: two port operations per cycle; simple dual port: one read and one write)? What does a 1R1W bank need from the address map?
Q3. Is there a bank map with conflict-free access for every layer, both directions and every cycle (one read and one write per bank per cycle)? Checked by exhaustive enumeration of the real address schedule, not by argument.
Q4. For each option of ADR 0017 (more 1R1W banks, two coefficients per word, double-pumping, schedule change): what does it need, what would it cost (ESTIMATE with method), what must be proved before RTL?

## 2. Method (fixed before running)
- `scripts/phase5m_s9_port_analysis.py`: pure Python on the existing model `tb/mem/bank_model.py` (`addr_pair`, `lane_p`, `bank_of`, `build_maps`), no RTL, no Quartus; deterministic output saved as
  `docs/evidence/phase05m-memsched/s9/port_analysis_2026-10-03.txt`. Timeline model: layer k issues one butterfly per lane per cycle for 16 cycles; the 16 addresses of a cycle are read in that cycle and
  written P cycles later (P = 7, the S7 value, as the no-stall reference); layers follow back to back; both directions; all 256 addresses.
- Checks: (1) current map: worst reads, writes and reads + writes per bank per cycle; (2) candidate 16-bank map `bank = (a7^a3^a2^a1, a6, a5, a4)`, `offset = a[3:0]` (derived by hand from the structure of
  `addr_pair`, to be confirmed or refuted by the script): bijective, balanced (16 words per bank), at most one read and one write per bank per cycle over the whole timeline; (3) negative controls that must
  conflict: `bank = a[7:4]` (no XOR), `bank = a[3:0]`, and the current 8-bank map used with 16 ports at one access per bank; (4) exhaustive count of conflict-free-ness failures for each.
- Resource figures: only MEASURED values already in the repo (Quartus evidence files) and ESTIMATEs whose method is written next to them. No Quartus run for S9 (no RTL). Intel device facts (M10K
  capacity, port modes, read-during-write behaviour, maximum frequency) are taken from the repository's cited sources or marked NOT VERIFIED here; none is invented.

## 3. Output and decision rule
`docs/evidence/phase05m-memsched/s9/study_m10k_2026-10-03.md` (options, evidence conditions, estimates) and an ADR (Proposed) that lists the options for the team. **No adoption rule: the team chooses**
(C5). S9 changes no RTL, so no regression is needed for it. If the analysis refutes the hand-derived map, that is reported as the result.
