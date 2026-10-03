#!/usr/bin/env python3
"""scripts/phase8b_cycles.py [W]

Summarises the 8b cycle tables (docs/evidence/phase08-keccak-stream/8b/cycles_w<W>_{c5,k0}_*.json: cycles from start_i to done_o with coef_ready_i always high, one point per polynomial)
and derives the sampling cycles per ML-KEM-768 operation (perhitungan tim: sums of per-polynomial means, not a measurement of an operation): KeyGen 9 SampleNTT + 6 CBD, Encaps 9 + 7, Decaps repeats the Encaps sampling.
Usage: python3 scripts/phase8b_cycles.py 1
"""
import json
import pathlib
import statistics
import sys

E8 = pathlib.Path(__file__).resolve().parents[1] / "docs" / "evidence" / "phase08-keccak-stream" / "8b"
w = sys.argv[1] if len(sys.argv) > 1 else "1"
print(f"# Phase 8b W{w}: cycles per polynomial (MEASURED in simulation, coef_ready_i always high; operation sums are perhitungan tim)\n")
print("| Sponge | Kind | Polynomials | Mean | Min | Max | Distinct values |")
print("|---|---|---|---|---|---|---|")
ops = {}
for core in ("c5", "k0"):
    files = sorted(E8.glob(f"cycles_w{w}_{core}_*.json"))
    if not files:
        continue
    pts = json.loads(files[-1].read_text())
    for kind in ("sample_ntt", "cbd"):
        c = [p["cycles"] for p in pts if p["kind"] == kind]
        print(f"| {core.upper()} | {kind} | {len(c)} | {statistics.mean(c):.2f} | {min(c)} | {max(c)} | {len(set(c))} |")
        ops[(core, kind)] = statistics.mean(c)
    print()
    rtab = {}
    for p in pts:
        if p["kind"] == "sample_ntt":
            base = p["sum_max"] if w == "1" else p["triples"]
            rtab.setdefault(p["blocks"], set()).add(p["cycles"] - base)
    print(f"{core.upper()}: r = cycles - {'sum of max(1, accepted)' if w == '1' else 'triples consumed'} per XOF blocks B: " + ", ".join(f"B={b}: {sorted(v)}" for b, v in sorted(rtab.items())) + "\n")
print("## Sampling cycles per operation (perhitungan tim)")
print("| Sponge | KeyGen (9 SampleNTT + 6 CBD) | Encaps (9 + 7) | Decaps (repeats the Encaps sampling) |")
print("|---|---|---|---|")
for core in ("c5", "k0"):
    if (core, "cbd") in ops:
        n, c = ops[(core, "sample_ntt")], ops[(core, "cbd")]
        print(f"| {core.upper()} | {9 * n + 6 * c:,.0f} | {9 * n + 7 * c:,.0f} | {9 * n + 7 * c:,.0f} |")
