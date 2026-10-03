# ADR 0025: S10 (inside Phase 6): 16 x 1R1W bank memory without slot arbitration - rule result

- Status: Proposed
- Date: 2026-10-03
- Decided by: pending team decision

## Context
- ADR 0024 (Accepted): S10 is done inside Phase 6 after the Phase 6 block. ADR 0022 (Proposed) option A: a 16-bank map `bank = (a1^a2^a3^a4, a7, a6, a5)`, `offset = a[3:0]` is conflict-free (one read, one write per bank per
  cycle) over the whole schedule. The S7 path analysis (team request "jalankan opsi 1 dan 2") showed the slot-arbitration ripple as the limit of S7 (`docs/evidence/phase05m-memsched/fmax50/path_analysis_2026-10-03.md`).
- Test plan and rule written before RTL and measurement: `docs/evidence/phase06-scheduling/test_plan_s10.md` (Amendment A1: the start-latency bound of the core test derived from the host-write guard; no threshold changed).
- New files only: `rtl/mem/poly_mem_m10k.sv`, `rtl/ntt/ntt_core_s10.sv`, `ntt_core_s10_p5.sv`, `rtl/sched/kpke_sched_top_s10.sv`.

## Options considered
(a) Adopt S10 as the NTT/INTT core for the following phases (and the Phase 6 top with S10). (b) Keep S7. (c) Other.

## Decision
Result of the pre-fixed rule (`scripts/select_s10.py`, no tolerance): **S10 is adopted by the rule** (all conditions PASS). Acceptance as the configuration is the team's (C5): this record stays Proposed.

## Consequences
- MEASURED (Quartus, seeds 1-6, 40.000 ns; `docs/evidence/phase06-scheduling/s10/selection_worksheet_2026-10-03.md`): ALM 5,045-5,091 (median 5,077.0; S7 9,391.0), registers 543-555 (S7 4,296-4,324; the storage moved
  into RAM blocks), M10K 24 (S7 31), DSP 16, timing met at every seed, **Fmax median 44.320 MHz (42.34-46.65)** versus S7 38.720 (37.89-40.29); cycles NTT = INTT = 118 (simulation). t = 118 / 44.320 = 2.662 us versus
  3.099 us (perhitungan tim, -14 %).
- MEASURED at 20.000 ns (information, seeds 1-6): **timing met at 6 of 6 seeds** (worst setup +0.792 to +1.718 ns, lowest-corner Fmax 52.06-54.70 MHz); S7 at 20 ns met 0 of 6. This is a kernel-only compile with virtual
  pins (no board, no system clock): it shows the core meets a 20 ns constraint in this flow, not a system running at 50 MHz.
- The lowest S10 seed at 40 ns (42.34 MHz) is above the highest S7 seed (40.29 MHz): the gain is larger than the seed spread (INFERENCE).
- Verification: memory, core, negative controls (map without the XOR bit, write one cycle short), the Phase 6 top with S10 (KeyGen 5,475 / Encrypt 6,789 / Decrypt 3,109 cycles) on Verilator and Icarus; formal 3/3.
- Critical warnings: 15725 (virtual pin clock) only, at every 20 ns and 40 ns compile; nothing waived.
- Not covered: hardware, a path analysis after S10, the M10K read-during-write mode on hardware (the schedule never reads and writes one word in one cycle: formal property C).

## Evidence
- `docs/evidence/phase06-scheduling/test_plan_s10.md`, `s10/verify_2026-10-03.md`, `s10/formal_2026-10-03.md`, `s10/verification_status.json`, `s10/selection_worksheet_2026-10-03.md`, `s10/quartus_S10[-s2..s6]_20261002.md`,
  `s10/quartus_S10-20[-s2..s6]_20261002.md`, `docs/evidence/phase05m-memsched/fmax50/` (S7 at 20 ns, path analysis), `scripts/select_s10.py`.
