# Bank-map specification (Phase 2, configuration C1)

Required by `docs/ROADMAP.md` Phase 2 evidence artifact: "bank-map specification, proof and
enumeration logs". This file is the specification; the proofs/logs are the other files in this
directory (`bank_scheme_exploration.txt`, `formal_bank_map.txt`,
`formal_ntt_core_c1_safety.txt`, `cocotb_regression.txt`).

## Problem

`rtl/ntt/ntt_core.sv` (C0, Phase 1) stores all 256 polynomial coefficients in one unbanked
256x12 array (`rtl/ntt/poly_mem.sv`). Splitting this into `L` independent banks (for a future
`L`-lane datapath, Phase 3) requires an address-to-(bank, offset) mapping such that, at every
point in the algorithm, the addresses accessed **at the same time** never collide on the same
physical bank more often than that bank's port count allows.

This is harder than it first looks because the algorithm is **in-place**: address `j` (0..255)
*is* the physical storage location for the whole run, across all 7 layers -- it is not
reinterpreted per layer. So the bank-assignment function must be a single, fixed function of the
address, chosen once, that happens to work for every layer's very different access pattern.

For a fixed layer with block-length `len = 2^log2len`, the NTT/INTT butterfly pair processed
together is always `(j, j + len)` -- two addresses differing in **exactly one bit**, at position
`log2len`. Across the 7 layers, `log2len` takes every value in `{1, ..., 7}` (never 0, since the
smallest length is 2). A *fixed, small* bit-slice bank function (e.g. `addr mod L`, or addr's top
`log2(L)` bits) only ever covers a handful of those 7 bit positions, so it collides completely on
every layer whose distinguishing bit falls outside the slice -- confirmed empirically, not just
argued, in `bank_scheme_exploration.txt`'s "own-pair" check for the naive schemes tried
first during design exploration.

## Scheme: XOR-group ("skewed storage") bank assignment

Implemented in `tb/mem/bank_model.py:bank_of` (the golden model) and generated into
`rtl/mem/bank_map_rom.sv` by `scripts/build/gen_bank_map.py`.

For `L` banks (`log2L = log2(L)` output bits): split address bits `{1, ..., 7}` (bit 0 is never
used) into `log2L` round-robin groups; bank output bit `i` is the XOR-parity of all address bits
in group `i`. Because every one of bits 1-7 belongs to exactly one group, flipping *any* single
one of them flips exactly one output bit, so `bank(addr) != bank(addr XOR 2^d)` for every `d` in
`1..7` -- this is the "own-pair" property, and it holds regardless of which layer produced the
`2^d` difference.

`offset(addr)` is defined as addr's rank (0-based, ascending) among all 256 addresses sharing its
bank -- this makes `(bank(addr), offset(addr))` a bijection with `addr` by construction, so no
address is lost or aliased; `scripts/build/gen_bank_map.py` turns this directly into the ROM contents
(never a separately hand-derived formula).

## Lane grouping (for future Phase 3 use)

For `L`-lane parallel processing, the 128 butterflies of a layer are split into `L` **contiguous
blocks** of `128/L` each: lane `m` (0..L-1) handles butterfly indices `p = m*(128/L) + t` for
`t = 0..(128/L - 1)` (`tb/mem/bank_model.py:lane_p`). This was chosen over round-robin/interleaved
grouping (`p = t*L + m`) because it is the one that keeps bank contention within the Cyclone V
M10K true-dual-port capacity (see below); interleaved grouping was tried, found to exceed that
capacity for L=4 and L=8, and is documented as a rejected negative control in
`bank_scheme_exploration.txt`, not silently dropped.

## What was checked, and how (all in `bank_scheme_exploration.txt`)

| Property | Method | Result |
|---|---|---|
| Own-pair: `bank(j) != bank(jlen)`, every L, every layer, every p | Exhaustive Python (`tb/mem/bank_model.py` + `scripts/build/gen_bank_map.py`) | 0 collisions, all L |
| Same property, on the actual generated ROM contents | Formal (SymbiYosys, L=8, BMC depth 1 over free `addr_i`/`d_i`) | PASS (`formal_bank_map.txt`) |
| Bank balance: every bank holds exactly `256/L` addresses | Exhaustive Python | balanced, all L |
| `(bank, offset)` <-> `addr` bijection, values in range | Exhaustive Python | bijective, all L |
| Multi-lane: <=2 accesses/bank/cycle (M10K true-dual-port), contiguous-block grouping | Exhaustive Python, every L, every layer, every `t` | worst case exactly 2, all L |
| Same, interleaved grouping (negative control) | Exhaustive Python | exceeds 2 for L=4 (worst 4), L=8 (worst 4) -- confirms the grouping choice matters, not assumed harmless |

## What is NOT built or claimed this phase

- `rtl/mem/poly_mem_banked.sv` is only **exercised** at `NUM_BANKS=1` this phase
  (`rtl/mem/ntt_core_c1.sv`, configuration C1); it compiles (lint-clean, CRG-1/CRG-2) for
  `NUM_BANKS` in `{2,4,8}` too, but the multi-bank read/write crossbar for those values has **no
  cocotb test** this phase -- only the standalone `bank_map_rom` address function is tested and
  proven for all four `L` values. Building and testing the actual `L>1` parallel datapath is
  Phase 3 scope (`docs/ROADMAP.md`).
- No claim is made that `L=2/4/8` hardware is measured or even fully verified end-to-end; only
  that its addressing is proven conflict-free in isolation.
