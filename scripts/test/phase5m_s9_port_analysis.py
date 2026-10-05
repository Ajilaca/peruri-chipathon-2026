#!/usr/bin/env python3
"""scripts/test/phase5m_s9_port_analysis.py

Phase 5M step S9 (evidence/phase05m/test_plan_s9.md): port demand of the L = 8 NTT/INTT schedule per memory bank, for the current
8-bank map and for candidate 16-bank maps, from the real address schedule (tb/mem/bank_model.py). Pure Python: no RTL, no Quartus.

Timeline model: layer k (0..6) issues in cycles 16k .. 16k+15; in cycle c the 8 lanes read 16 addresses (j and j + len of butterfly p = lane * 16 + t); the same 16 addresses are
written P cycles later (P = 7, the S7 reference without stall). Both directions. Demand per bank per cycle: reads, writes and reads + writes.

Usage: python3 scripts/test/phase5m_s9_port_analysis.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tb" / "mem"))
from bank_model import addr_pair, bank_of, lane_p  # noqa: E402

L = 8
T = 128 // L          # cycles per layer
P = 7
N = 256


def issue_sets(mode):
    """list over issue cycles of the 16 addresses accessed in that cycle."""
    out = []
    for layer in range(7):
        for t in range(T):
            addrs = []
            for lane in range(L):
                j, jl = addr_pair(layer, mode, lane_p(L, lane, t))
                addrs += [j, jl]
            out.append(addrs)
    return out


def demand(bank_fn, mode):
    """worst reads, writes, reads+writes per bank per cycle over the whole timeline; also the number of (cycle, bank) cells above 1 read / 1 write."""
    sets = issue_sets(mode)
    ncyc = len(sets) + P
    worst_r = worst_w = worst_rw = 0
    over_r = over_w = 0
    for c in range(ncyc):
        r, w = {}, {}
        if c < len(sets):
            for a in sets[c]:
                r[bank_fn(a)] = r.get(bank_fn(a), 0) + 1
        if 0 <= c - P < len(sets):
            for a in sets[c - P]:
                w[bank_fn(a)] = w.get(bank_fn(a), 0) + 1
        for b in set(r) | set(w):
            rr, ww = r.get(b, 0), w.get(b, 0)
            worst_r, worst_w, worst_rw = max(worst_r, rr), max(worst_w, ww), max(worst_rw, rr + ww)
            over_r += rr > 1
            over_w += ww > 1
    return worst_r, worst_w, worst_rw, over_r, over_w


def check_map(name, bank_fn, offset_fn, nbanks):
    cells = {(bank_fn(a), offset_fn(a)) for a in range(N)}
    bij = len(cells) == N
    sizes = {}
    for a in range(N):
        sizes[bank_fn(a)] = sizes.get(bank_fn(a), 0) + 1
    balanced = len(sizes) == nbanks and len(set(sizes.values())) == 1
    print(f"--- {name} ---")
    print(f"banks used = {len(sizes)}, words per bank = {sorted(set(sizes.values()))}, bijective (bank, offset) = {bij}, balanced = {balanced}")
    ok = True
    for mode, mname in ((0, "NTT"), (1, "INTT")):
        wr, ww, wrw, orr, oww = demand(bank_fn, mode)
        print(f"{mname}: worst reads/bank/cycle = {wr}, writes/bank/cycle = {ww}, reads+writes = {wrw}; cells over 1 read = {orr}, over 1 write = {oww}")
        ok &= (wr <= 1 and ww <= 1)
    print(f"RESULT {name}: {'1R1W conflict-free over the whole timeline' if (ok and bij and balanced) else 'NOT conflict-free as 1R1W'}")
    print()
    return ok and bij and balanced


def main():
    print("Phase 5M S9 port analysis (perhitungan tim from tb/mem/bank_model.py; no RTL, no Quartus)")
    print(f"Timeline: 7 layers x {T} issue cycles, 16 addresses per cycle, writes P = {P} cycles after the reads, both directions\n")

    # 1. current map (8 banks, ROM-generated bank_of with parity groups)
    cur = lambda a: bank_of(a, 8)  # noqa: E731
    wr, ww, wrw, _, _ = (max(x) for x in zip(demand(cur, 0), demand(cur, 1)))
    print("--- current 8-bank map (rtl/mem/bank_map_rom.sv, generated from bank_model.bank_of) ---")
    print(f"worst over NTT and INTT: reads/bank/cycle = {wr}, writes/bank/cycle = {ww}, reads+writes = {wrw}")
    print("M10K true dual port = 2 port operations per cycle; the schedule needs up to "
          f"{wrw} per bank in some cycle -> does not fit one true-dual-port M10K per bank; 1R1W (simple dual port) needs <= 1 read and <= 1 write.\n")

    # 2. candidate 16-bank maps. Candidate 1 was derived by hand with a wrong bit position (the plan, section 2, said the script would confirm or refute it): refuted below.
    cand1 = lambda a: (((a >> 7) ^ (a >> 3) ^ (a >> 2) ^ (a >> 1)) & 1) << 3 | ((a >> 4) & 7)  # noqa: E731
    off = lambda a: a & 15  # noqa: E731
    ok_c1 = check_map("candidate 1 (first hand derivation, refuted): bank = (a7^a3^a2^a1, a6, a5, a4), offset = a[3:0]", cand1, off, 16)
    # Candidate 2: butterfly index p bit k (k = 4..6, the lane) lands on address bit k if k < log2len else k + 1; the partner is address bit log2len. So the 16 addresses of a cycle span
    # {5,6,7,log2len} for log2len = 1..4 and {4,5,6,7} for log2len = 5..7; bank bits (a1^a2^a3^a4, a7, a6, a5) map every one of these sets onto 4 independent bank bits.
    cand2 = lambda a: ((((a >> 1) ^ (a >> 2) ^ (a >> 3) ^ (a >> 4)) & 1) << 3) | ((a >> 5) & 7)  # noqa: E731
    ok_c2 = check_map("candidate 2: bank = (a1^a2^a3^a4, a7, a6, a5), offset = a[3:0]", cand2, off, 16)
    ok_c = ok_c2

    # 3. negative controls
    ok_n1 = check_map("negative control: bank = a[7:4] (no XOR)", lambda a: a >> 4, lambda a: a & 15, 16)
    ok_n2 = check_map("negative control: bank = a[3:0]", lambda a: a & 15, lambda a: a >> 4, 16)

    # 4. option "two coefficients per word": a word holds the addresses {a, a ^ (1 << m)}; a butterfly needs j and j + len, which differ in exactly bit log2len (pos < len)
    print("--- option: two coefficients per word (word = addresses a and a with bit m flipped) ---")
    for m in range(8):
        layers = []
        for mode in (0, 1):
            for layer in range(7):
                same = all((j ^ jl) == (1 << m) for j, jl in (addr_pair(layer, mode, p) for p in range(128)))
                if same:
                    layers.append((("NTT", "INTT")[mode], layer))
        print(f"pairing bit m = {m}: (direction, layer) pairs whose two butterfly operands share one word for every butterfly: {layers if layers else 'none'}")
    print("-> at most one layer per direction (log2len == m) gets both operands from one word; the other six layers need two words per butterfly.\n")

    print("SUMMARY")
    print(f"candidate 1 conflict-free as 1R1W: {ok_c1} (refuted by this script)")
    print(f"candidate 2 conflict-free as 1R1W: {ok_c2}")
    print(f"negative control a[7:4] conflict-free: {ok_n1} (must be False)")
    print(f"negative control a[3:0] conflict-free: {ok_n2} (must be False)")
    return 0 if (ok_c and not ok_c1 and not ok_n1 and not ok_n2) else 1


if __name__ == "__main__":
    sys.exit(main())
