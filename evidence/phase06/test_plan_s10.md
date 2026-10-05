<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# S10 (inside Phase 6, ADR 0024): 16 x 1R1W bank memory without slot arbitration - test plan and adoption rule

Written 2026-10-03, **before any S10 RTL and before any S10 measurement** (CRG-4). Basis: ADR 0022 option A (S9 study: the map `bank = (a1^a2^a3^a4, a7, a6, a5)`, `offset = a[3:0]` gives at most one read
and one write per bank per cycle over the whole schedule, `evidence/phase05m/s9/port_analysis.txt`) and the S7 path analysis (the measured limit of S7 is the slot-arbitration ripple
between the cuts A_4 and A_11, `evidence/phase05m/fmax50/path_analysis.md`). Base: S7 (`rtl/ntt/ntt_core_s7_p7.sv`). Labels: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED.

## 1. The change (one change: the memory)
- new memory `rtl/mem/poly_mem_m10k.sv`: same port list as `poly_mem_multiport_split.sv` (en, wr, addr per port, rdata, wdata, bank_overflow_o), 16 banks of 16 x 12 bit, bank and offset by the map above (pure XOR and
  bit selection, no ROM, no arbitration). Per bank: the read address and the write address / data / enable are selected from the one port whose bank matches (16-way select); per port the read data is selected
  from its bank (16-way select). Each bank is written as a synchronous-read simple-dual-port RAM (`ramstyle` "M10K", read-during-write of the same word not relied on); whether Quartus maps it to M10K is
  reported, not assumed.
- Timing: the request's address is taken by the RAM at the end of the request cycle (physical read in the request cycle), the read data are selected and registered: read data `RD_LAT = 2` cycles after the
  request; the write of a request lands at the end of cycle `request + RD_LAT + WR_DELAY` with the bank and offset of the request (delayed). `bank_overflow_o`: two or more enabled ports on one bank in one request
  cycle, registered (one cycle later).
- new core `rtl/ntt/ntt_core_s10.sv` (copy of `ntt_core_s7.sv`: the memory instance replaced, `RdLat = RD_LAT`), wrapper `rtl/ntt/ntt_core_s10_p5.sv` (RD_LAT 2, MUL_REG bits 0, 1, 2: P = 5). The schedule is the S7
  schedule; P = 5 needs no stall (stall table: none up to P = 7). Cycles: 113 + 5 = **118** (ESTIMATE until simulated).
- **Existing files modified: none.**

## 2. Corner cases
- Every address through every port; the scheduled traffic of both directions back to back (16 ports, every bank once per cycle); read in the landing cycle (old value) and the cycle after (new value).
- Two ports on one bank in one cycle (must raise `bank_overflow_o`); one port per bank (must not). Host access through port 0 in IDLE (one port).
- Core level: the Phase 4 / S7 core test unchanged in content (NTT, INTT, round trip, boundary data, constant cycles, scoreboard, 512 INTT unit vectors).

## 3. Tests
| ID | Check | Tool | Required |
|---|---|---|---|
| V1 | Lint of the memory, core, wrapper | Verilator `-Wall`, slang | 0 warnings, 0 errors |
| V2 | Memory vs a cycle-accurate Python model (copy of the S7 memory test with the new latencies and the 16-bank conflict rule) | cocotb `tb/s10/test_poly_mem_m10k.py`, both simulators | all equal; overflow only when two ports share a bank |
| V3 | Core vs golden (`tb/phase5m/test_ntt_core_s7.py` with C3_RDLAT 2, C3_RDPHYS 0, C3_WRDLY 3) | cocotb, both simulators | all PASS; 0 scoreboard violations; constant cycles 118 / 118 |
| V4 | Negative controls (test-only copies): NC-M bank map without the XOR bit (`bank = {a7, a6, a5, a4}`): overflow and wrong results; NC-W write control one cycle short | cocotb | bit-exact FAIL (NC-M also raises `bank_overflow_o`) |
| V5 | Formal: H, O, R, A, C of a copy of the S7 formal top for the new memory (probes renamed) with NC-O (map mutant) and NC-A | SymbiYosys | PASS; controls FAIL |
| V6 | Phase 6 top with the S10 core (CORE_RDLAT 2): the Phase 6 test V5 | cocotb, both simulators | all PASS (information: cycles per program) |
| V7 | Quartus `S10` seeds 1-6 at 40.000 ns, one at a time; plus `S10-20` seeds 1-6 at 20.000 ns (information, comparable to the S7-20 sweep of the 50 MHz question) | `quartus_sh` | evidence extracted |

## 4. Adoption rule (ADR 0012, fixed before measuring)
S10 replaces S7 as the core memory only if **all** hold: (1) V1-V6 PASS, controls fail; (2) cycles exactly 118 / 118 and constant; (3) ALM <= 12,573 and timing met at 40.000 ns at every seed; (4) with F the median over
seeds 1-6 of the lowest slow-corner Fmax at 40 ns: **118 / F < 120 / F_S7** (F_S7 = 38.720 MHz recomputed from the S7 files), i.e. F > 38.075 MHz. No tolerance. Whether a result at 20 ns meets 50 MHz is reported,
not part of the rule.

## 5. Expectation (ESTIMATE, written before measuring)
The arbitration ripple (the measured worst S7 path, about 25.6 ns) is removed; new paths: address arithmetic -> XOR map -> 16-way select -> RAM address (short), RAM data -> 16-way select -> register, multiplier ->
16-way write select -> RAM. Fmax may rise; it may also be limited by the M10K timing or by the butterfly / write segments (S7: multiplier to write about 22.3 ns). M10K: 16 blocks more if the tool maps the banks
there; ALM: lower (no 3,072 storage flip-flops, no arbitration) or higher (crossbars), not predictable from the study (upper bound of the crossbars about 1,920 ALM, ESTIMATE).

## Amendment A1 (2026-10-03, after the first S10 core run, before any Quartus run)
The first run of V3 with the unmodified S7 test failed only on its start-latency check (`start_i taken only after 6 cycles`, bound `WRDLY + 2` = 5). That bound encodes the S7 host-write guard
(landing minus physical read = WRDLY + 1). In S10 the storage is read in the request cycle, so the guard is the whole pipe (5) and the start takes 6 cycles; the core is correct by construction of the guard
(a host write must land before the first transform read). V3 now runs `tb/s10/test_ntt_core_s10.py`, a copy of the S7 test whose bound is `(RDLAT - RDPHYS + WRDLY) + 1` (5 for S7, 6 for S10); nothing else in
the test changed. Thresholds and the adoption rule are unchanged.
