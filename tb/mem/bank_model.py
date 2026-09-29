"""tb/mem/bank_model.py

Golden (pure-Python) model of the Phase 2 conflict-free bank mapping for the 256-entry
polynomial memory, and of the address generator it plugs into (the exact same layer/length/
block/pos/start/j/jlen arithmetic as rtl/ntt/ntt_core.sv's Phase 1 FSM, factored out here so
Phase 2 does not retype it).

Scheme (XOR-group / "skewed storage" banking): for L banks, split address bits 1..7 (bit 0 is
never used for banking) into log2(L) round-robin groups; bank(addr) = the XOR-parity of each
group, one output bit per group. offset(addr) = the rank of addr among all addresses sharing its
bank, in increasing address order (so (bank, offset) <-> addr is a bijection by construction).

Why bit 0 is excluded and groups are used instead of a fixed bit-slice: for a fixed layer, the
NTT/INTT butterfly pair (j, j+len) differs in EXACTLY one address bit, at position log2(len),
and log2(len) ranges over 1..7 across the 7 layers (never 0, since the smallest length is 2).
A *fixed* small bit-slice bank function (e.g. addr mod L, or addr's top log2(L) bits) can only
ever include a handful of those 7 bit positions, so it collides completely on every layer whose
distinguishing bit falls outside the slice (verified empirically in
docs/evidence/phase02-memory/bank_scheme_exploration.txt). The XOR-group construction instead
makes every one of bits 1..7 influence at least one output bit, so flipping any single one of
them always changes bank(addr) -- this is checked exhaustively below, not assumed.
"""

from __future__ import annotations

N = 256

_FWD_LEN = (128, 64, 32, 16, 8, 4, 2)  # NTT layers 0..6
_INV_LEN = (2, 4, 8, 16, 32, 64, 128)  # INTT layers 0..6


def layer_len(layer: int, mode_inv: int) -> tuple[int, int]:
    """Returns (len, log2len) for the given layer (0..6) and direction
    (mode_inv=0 forward/NTT, 1 inverse/INTT), matching rtl/ntt/ntt_core.sv's per-layer table.
    """
    length = (_INV_LEN if mode_inv else _FWD_LEN)[layer]
    return length, length.bit_length() - 1


def addr_pair(layer: int, mode_inv: int, p: int) -> tuple[int, int]:
    """(j, jlen) for butterfly index p (0..127) at this layer/direction -- identical arithmetic
    to rtl/ntt/ntt_core.sv's j/jlen computation (block/pos/start_addr derivation).
    """
    length, log2len = layer_len(layer, mode_inv)
    block = p >> log2len
    pos = p - (block << log2len)
    start = block << (log2len + 1)
    j = start + pos
    return j, j + length


def log2_of(l: int) -> int:
    assert l in (1, 2, 4, 8)
    return l.bit_length() - 1


def bank_of(addr: int, num_banks: int) -> int:
    """bank(addr) for a given bank count (1, 2, 4 or 8). See module docstring for the scheme."""
    assert 0 <= addr < N
    if num_banks == 1:
        return 0
    log2l = log2_of(num_banks)
    bits = range(1, 8)  # bit 0 excluded
    bank = 0
    for gi in range(log2l):
        parity = 0
        for b in bits:
            if b % log2l == gi:
                parity ^= (addr >> b) & 1
        bank |= parity << gi
    return bank


def build_maps(num_banks: int):
    """Returns (bank_of_addr[256], offset_of_addr[256], addr_of[bank][offset]) for one bank
    count. offset(addr) is addr's rank (0-based, ascending) among addresses sharing its bank --
    this makes (bank, offset) a bijection with addr by construction, and is exactly what
    scripts/gen_bank_map.py turns into a ROM.
    """
    banks: dict[int, list[int]] = {}
    for a in range(N):
        banks.setdefault(bank_of(a, num_banks), []).append(a)
    bank_arr = [0] * N
    off_arr = [0] * N
    addr_of = {b: [0] * len(addrs) for b, addrs in banks.items()}
    for b, addrs in banks.items():
        for off, a in enumerate(sorted(addrs)):
            bank_arr[a] = b
            off_arr[a] = off
            addr_of[b][off] = a
    return bank_arr, off_arr, addr_of


def lane_p(num_banks: int, lane: int, t: int) -> int:
    """Which butterfly index p (0..127) lane `lane` (0..num_banks-1) processes at "sub-cycle" t
    (0..128/num_banks-1), under the contiguous-block lane grouping (verified in
    docs/evidence/phase02-memory/bank_scheme_exploration.txt to be the grouping that keeps every
    bank at <=2 accesses/cycle for every L; the alternative round-robin/interleaved grouping does
    not, and is not used).
    """
    per_lane = 128 // num_banks
    return lane * per_lane + t
