# Phase 2 test plan — memory banking (C1), written before any test is coded (CRG-4)

Scope: `rtl/mem/bank_map_rom.sv`, `rtl/mem/poly_mem_banked.sv`, `rtl/mem/ntt_core_c1.sv`.
Reference: `tb/mem/bank_model.py` (bank/offset scheme), `tb/golden/primitives.py` (`ntt`, `intt`).
No RTL below was written before this plan.

## Bank-mapping conflict-freedom proof (not a cocotb test; a standalone exhaustive/formal check)

Required by `docs/ROADMAP.md` Phase 2: "for every L ∈ {1, 2, 4, 8}, every layer and every cycle,
no two accesses target the same bank port" plus "no out-of-range address".

- **Own-pair check**: for every L, every of the 7 NTT layers and 7 INTT layers, every butterfly
  index p (0..127): `bank(j) != bank(jlen)` (trivially true for L=1, one bank).
- **Bank balance**: every bank holds exactly 256/L addresses, for every L.
- **Offset bijectivity**: `(bank(addr), offset(addr))` is a bijection with `addr` for every L
  (so no address is lost or aliased).
- **Multi-lane capacity**: for every L, every layer, every "sub-cycle" t (0..128/L-1), the 2·L
  addresses produced by the L lanes active that cycle hit no bank more than **2** times (the
  Cyclone V M10K true-dual-port capacity) -- checked for both the contiguous-block lane grouping
  (`tb/mem/bank_model.py:lane_p`) and, as a documented negative control, round-robin/interleaved
  grouping (expected and confirmed to fail for L=4 and L=8 -- recorded, not hidden).
- **Range check**: `bank < L` and `offset < 256/L` for every address, every L (structural, but
  checked, not just assumed).
- **Formal**: the own-pair property re-checked on the actual generated ROM contents
  (`rtl/mem/bank_map_rom.sv`, L=8 instance -- the case that must distinguish the most layers)
  via SymbiYosys, independently of the Python golden model, to catch a generator bug that
  Python-vs-Python could not.

## Unit: bank_map_rom (all four L instances)

- Corner cases: addr=0, addr=255, addr=128 (crosses the L=2 bank boundary), addr=127/129
  (adjacent to that boundary).
- Exhaustive: all 256 addresses, for each of L ∈ {1, 2, 4, 8}, bit-exact against
  `tb/mem/bank_model.py:bank_of` / the offset table from `build_maps`.

## Unit: poly_mem_banked (NUM_BANKS=1, the only configuration built this phase)

- Corner cases: write then immediate read-back of address 0 and address 255; write all 256
  addresses then read all 256 back in a different order.
- Property: with NUM_BANKS=1, behaviour must be identical to `rtl/ntt/poly_mem.sv` (Phase 1) for
  the same sequence of operations -- checked indirectly via the `ntt_core_c1` regression below,
  which is a stronger, whole-core check.

## Regression: ntt_core_c1 (config C1 = C0's FSM/butterfly + banked memory at NUM_BANKS=1)

Same tests as Phase 1's `tb/ntt/test_ntt_core.py`, run against the new top `ntt_core_c1`, to
prove the memory change does not change behaviour or cycle count (roadmap PASS criterion:
"measured stall cycles = 0 at L = 1"; "constant cycle count"; "bit-exact"):

- `ntt(f)` and `intt(f)` bit-exact vs `tb/golden/primitives.py`, same 5 corner polynomials +
  100 random each direction as Phase 1.
- `intt(ntt(f)) == f`, 50 random polynomials.
- Constant-cycle check: cycle count from `busy_o` rising to `done_o` rising must equal Phase 1's
  measured values **exactly** (NTT 897, INTT 1153, per
  `docs/evidence/phase01-ntt-baseline/cocotb_regression_2026-09-29.txt`) for every corner case
  and 20 random polynomials per direction -- any deviation means the banked memory introduced a
  stall cycle, which is a FAIL per the roadmap's own criterion, not something to explain away.
- Run twice (Icarus and Verilator), same as Phase 1 (CRG-3).

## Explicitly out of scope for Phase 2 (see docs/ROADMAP.md "Not allowed yet")

Activating more than one lane in the actual datapath (L stays 1 in `ntt_core_c1`); pipeline
changes; arithmetic changes (the Phase 1 timing failure in `modmul_reduce.sv` is untouched here,
on purpose -- it is Phase 4/5 scope); Keccak.
