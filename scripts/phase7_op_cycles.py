#!/usr/bin/env python3
"""scripts/phase7_op_cycles.py

Phase 7: Keccak cycles of one ML-KEM-768 operation with the K0 sponge (perhitungan tim; no measurement). Each hash call of FIPS 203 Algorithms 16-18 is costed with the cycle
formula that test V6 verified at 306 points (tb/keccak/test_keccak_sponge.py::_formula), the K0 sponge restarting for every call and no overlap with any other block.
SampleNTT: the number of XOF bytes actually consumed for each of the nine matrix entries (rejection sampling, FIPS 203 Algorithm 7) is taken from the golden SHAKE128 stream
for NRHO random rho values (fixed seed); the squeeze is ceil(bytes / 8) 64-bit words.
Call inventory (ML-KEM-768, FIPS 203): KeyGen_internal G(d||k) 33 B, 9 SampleNTT, 6 PRF 33 B -> 128 B, H(ek) 1184 B; Encaps_internal H(ek) 1184 B, G(m||h) 64 B, 9 SampleNTT, 7 PRF;
Decaps_internal G(m'||h) 64 B, J(z||c) 1120 B -> 32 B, 9 SampleNTT, 7 PRF (h is stored in dk, not recomputed).
Usage: python3 scripts/phase7_op_cycles.py [NRHO]   (prints a markdown table)
"""
import hashlib
import random
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tb" / "golden"))
sys.path.insert(0, str(ROOT / "tb" / "keccak"))
import types  # noqa: E402

from params import N, Q  # noqa: E402

RATE = {"sha3_256": 136, "sha3_512": 72, "shake_128": 168, "shake_256": 136}
PERM = 26


def cycles(mode, ln, ow):
    rate, rw = RATE[mode], RATE[mode] // 8
    pad2 = 0 if (ln % rate) // 8 == rw - 1 else 1
    return 1 + (ln // 8 + 1) + pad2 + PERM * (ln // rate + 1) + ow + PERM * ((ow - 1) // rw)


def perms(mode, ln, ow):
    rate, rw = RATE[mode], RATE[mode] // 8
    return ln // rate + 1 + (ow - 1) // rw


def sample_ntt_bytes(b):
    buf = hashlib.shake_128(b).digest(2000)
    j = pos = 0
    while j < N:
        c = buf[pos: pos + 3]
        pos += 3
        d1 = c[0] + 256 * (c[1] % 16)
        d2 = c[1] // 16 + 16 * c[2]
        if d1 < Q:
            j += 1
        if d2 < Q and j < N:
            j += 1
    return pos


def main():
    nrho = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    rng = random.Random(7)
    fixed = {
        "G 33 B (KeyGen)": ("sha3_512", 33, 8), "G 64 B": ("sha3_512", 64, 8), "H(ek) 1184 B": ("sha3_256", 1184, 4),
        "PRF 33 B -> 128 B": ("shake_256", 33, 16), "J 1120 B -> 32 B": ("shake_256", 1120, 4),
    }
    print("| Call | Mode | Message bytes | Output words | Permutations | Cycles (formula) |")
    print("|---|---|---|---|---|---|")
    for k, (m, ln, ow) in fixed.items():
        print(f"| {k} | {m} | {ln} | {ow} | {perms(m, ln, ow)} | {cycles(m, ln, ow)} |")
    sn_c, sn_p = [], []
    for _ in range(nrho):
        rho = bytes(rng.randrange(256) for _ in range(32))
        c = p = 0
        for i in range(3):
            for j in range(3):
                nb = sample_ntt_bytes(rho + bytes([j, i]))
                ow = -(-nb // 8)
                c += cycles("shake_128", 34, ow)
                p += perms("shake_128", 34, ow)
        sn_c.append(c)
        sn_p.append(p)
    print(f"| SampleNTT x 9 (matrix), {nrho} random rho | shake_128 | 34 each | by rejection | min {min(sn_p)}, median {int(statistics.median(sn_p))}, max {max(sn_p)} "
          f"| min {min(sn_c)}, median {int(statistics.median(sn_c))}, max {max(sn_c)} |")
    print()
    g = lambda k: fixed[k]
    def tot(items):
        c = sum(cycles(*g(k)) * n for k, n in items)
        p = sum(perms(*g(k)) * n for k, n in items)
        return c, p
    ops = {
        "KeyGen": [("G 33 B (KeyGen)", 1), ("PRF 33 B -> 128 B", 6), ("H(ek) 1184 B", 1)],
        "Encaps": [("H(ek) 1184 B", 1), ("G 64 B", 1), ("PRF 33 B -> 128 B", 7)],
        "Decaps": [("G 64 B", 1), ("J 1120 B -> 32 B", 1), ("PRF 33 B -> 128 B", 7)],
    }
    print("| Operation | Keccak cycles without SampleNTT | + SampleNTT (min / median / max) | Total Keccak cycles (min / median / max) | Permutations (median total) |")
    print("|---|---|---|---|---|")
    for op, items in ops.items():
        c, p = tot(items)
        print(f"| {op} | {c} | {min(sn_c)} / {int(statistics.median(sn_c))} / {max(sn_c)} | {c + min(sn_c)} / {c + int(statistics.median(sn_c))} / {c + max(sn_c)} | {p + int(statistics.median(sn_p))} |")


if __name__ == "__main__":
    main()
