#!/usr/bin/env python3
"""scripts/phase5_stall_cycles.py

Decision aid (no RTL involved): for the existing L = 8 lane schedule (tb/mem/bank_model.py: lane_p, addr_pair)
and a butterfly pipeline of depth P, find the minimum number of stall cycles needed at each layer boundary (and
before the INTT x3303 scaling pass) so that no address is read before its write from the previous layer is
readable, then the resulting NTT / INTT cycle counts and times per transform at given clock frequencies.

Model (same as scripts/pipeline_hazard_slack.py): layer k issues at sub-cycles t = 0..T-1 (T = 16 at L = 8); a
butterfly issued at t writes at t + P, readable from t + P + 1. A stall of s cycles before layer k+1 delays all its
reads by s. Address a, written by layer k at t_w and read by layer k+1 at t_r, is safe iff T + s + t_r - t_w - 1 >= P.
The minimum s per boundary is found by direct search over s (not by formula) and then re-checked for all 256
addresses.

Cycle counts: the Phase 4 measured relation NTT = 113 + P, INTT = 369 + P with 0 stall for P <= 6
(docs/evidence/phase04-pipeline/cocotb_regression_2026-09-30.txt), plus the stall cycles found here. For P >= 7 the
totals are an ESTIMATE until simulated.

Constant-cycle argument: every quantity below depends only on (P, mode, layer, lane, t) through the fixed address
schedule; no polynomial data enters, so the stall count of a boundary is a compile-time constant.

Usage: python3 scripts/phase5_stall_cycles.py [P ...]     (default P = 6..12)
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tb" / "mem"))
from bank_model import addr_pair, lane_p  # noqa: E402

L = 8
T = 128 // L
BASE = {"NTT": 113, "INTT": 369}                 # measured at P = 0 .. 6: cycles = BASE + P, 0 stall
F_MEASURED = 34.19                               # C3-P6 default seed, lowest slow-corner Fmax (MEASURED)
F_HYPO = (40.0, 45.0, 50.0)                      # hypothetical clocks (ESTIMATE)


def write_read_times(mode, layer_w, layer_r):
    t_w, t_r = {}, {}
    for t in range(T):
        for lane in range(L):
            p = lane_p(L, lane, t)
            for a in addr_pair(layer_w, mode, p):
                t_w[a] = t
            if layer_r is not None:
                for a in addr_pair(layer_r, mode, p):
                    t_r[a] = t
    if layer_r is None:                          # x3303 scaling pass reads address a at cycle a
        t_r = {a: a for a in range(256)}
    assert len(t_w) == 256 and len(t_r) == 256
    return t_w, t_r


def min_stall(t_w, t_r, p):
    s = 0
    while not all(T + s + t_r[a] - t_w[a] - 1 >= p for a in range(256)):
        s += 1
    return s


def main(ps):
    rows = []
    for p in ps:
        stalls = {}
        for mode, name in ((0, "NTT"), (1, "INTT")):
            per = [min_stall(*write_read_times(mode, k, k + 1), p) for k in range(6)]
            if name == "INTT":
                per.append(min_stall(*write_read_times(1, 6, None), p))
            stalls[name] = per
        rows.append((p, stalls))
    print("Minimum stall cycles per boundary (NTT: 6 layer boundaries; INTT: 6 layer boundaries + scaling pass)")
    for p, st in rows:
        print(f"P={p:2d}  NTT {st['NTT']}  INTT {st['INTT']}")
    print()
    t0 = {k: (BASE[k] + 6) / F_MEASURED for k in BASE}
    hdr = "P  | cycles NTT / INTT | +cycles vs P=6 (NTT, INTT) | t_NTT / t_INTT (us) at " + \
          " / ".join(f"{f:g}" for f in (F_MEASURED,) + F_HYPO) + " MHz"
    print(hdr)
    for p, st in rows:
        c = {k: BASE[k] + p + sum(st[k]) for k in BASE}
        d = {k: c[k] - (BASE[k] + 6) for k in BASE}
        times = "  ".join(f"{c['NTT'] / f:.3f}/{c['INTT'] / f:.3f}" for f in (F_MEASURED,) + F_HYPO)
        print(f"{p:2d} | {c['NTT']:4d} / {c['INTT']:4d}       | +{d['NTT']} ({100 * d['NTT'] / (BASE['NTT'] + 6):.1f}%),"
              f" +{d['INTT']} ({100 * d['INTT'] / (BASE['INTT'] + 6):.1f}%) | {times}")
    print()
    print(f"Reference C3-P6 (MEASURED cycles, measured Fmax {F_MEASURED} MHz): t_NTT = {t0['NTT']:.3f} us, "
          f"t_INTT = {t0['INTT']:.3f} us")
    for f in F_HYPO:
        print(f"Break-even cycles at {f:g} MHz (same time as C3-P6 today): NTT <= {int(t0['NTT'] * f)}, "
              f"INTT <= {int(t0['INTT'] * f)}")
    return 0


if __name__ == "__main__":
    sys.exit(main([int(x) for x in sys.argv[1:]] or list(range(6, 13))))
