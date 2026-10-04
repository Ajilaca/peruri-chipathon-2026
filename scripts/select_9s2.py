#!/usr/bin/env python3
"""scripts/select_9s2.py -- Phase 9F step S2 worksheet (docs/evidence/phase09m-optimisation/9s2/test_plan_9s2.md sections 4 and 5, ADR 0039: 15 ns is the reporting limit): reads the Quartus evidence files of K2
(40.000 ns, seeds 1-6, and 15.000 ns, seeds 1-6) and, as the reference, K1b (9f1b); writes docs/evidence/phase09m-optimisation/9s2/selection_worksheet_<date>.md. Every value is copied from an evidence file;
t = cycles / Fmax is perhitungan tim.
Usage: python3 scripts/select_9s2.py [date YYYY-MM-DD]
"""
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import select_9f1 as S1  # noqa: E402

E9M = S1.E9M
E2 = E9M / "9s2"
EB = E9M / "9f1b"
CYC = {"K1b": (8404, 10236, 15597), "K2": (8416, 10250, 15619)}   # profile inputs: 9f1b/profile_k1b_verilator_2026-10-04.json and 9s2/profile_k2_verilator_2026-10-04.json


def main():
    date = sys.argv[1] if len(sys.argv) > 1 else "2026-10-04"
    out = []
    o, k40 = S1.table("K2 at 40.000 ns, seeds 1-6 (the gate)", E2, ["K2"] + [f"K2-s{s}" for s in range(2, 7)], 40.0)
    out += o
    o, k15 = S1.table("K2 at 15.000 ns, seeds 1-6 (reporting limit, ADR 0039)", E2, [f"K2-15-s{s}" for s in range(1, 7)], 15.0)
    out += o
    o, b40 = S1.table("Reference K1b at 40.000 ns, seeds 1-6", EB, ["K1b"] + [f"K1b-s{s}" for s in range(2, 7)], 40.0)
    out += o
    o, b15 = S1.table("Reference K1b at 15.000 ns, seeds 1-6", EB, [f"K1b-15-s{s}" for s in range(1, 7)], 15.0)
    out += o
    b15f = [S1.parse(EB, f"K1b-15-s{s}")["fmax"] for s in range(1, 7)]
    k15f = [S1.parse(E2, f"K2-15-s{s}")["fmax"] for s in range(1, 7)]
    L = S1.lat
    out += ["## Latency (perhitungan tim: profile-input cycles / Fmax; kernel-only static timing, not a board measurement)",
            "| Configuration | Cycles KeyGen / Encaps / Decaps | Fmax (MHz) | Latency KeyGen / Encaps / Decaps (us) |", "|---|---|---|---|",
            f"| K2 at 15 ns (median of 6) | {' / '.join(f'{c:,}' for c in CYC['K2'])} | {k15['fmax']:.3f} | {L(CYC['K2'], k15['fmax'])} |",
            f"| K2 at 15 ns (lowest of 6) | same | {k15['fmin']:.2f} | {L(CYC['K2'], k15['fmin'])} |",
            f"| K1b at 15 ns (median of 6) | {' / '.join(f'{c:,}' for c in CYC['K1b'])} | {b15['fmax']:.3f} | {L(CYC['K1b'], b15['fmax'])} |",
            f"| K1b at 15 ns (lowest of 6) | same | {b15['fmin']:.2f} | {L(CYC['K1b'], b15['fmin'])} |",
            f"| K2 at 40 ns (median of 6) | same as K2 | {k40['fmax']:.3f} | {L(CYC['K2'], k40['fmax'])} |", ""]
    r2, r3 = k40["nmet"] == 6, k40["alm"] <= 20000
    vs = [(CYC["K2"][i] / k15["fmax"]) / (CYC["K1b"][i] / b15["fmax"]) - 1 for i in range(3)]
    r4 = all(x < 0 for x in vs)
    gain = k15["fmax"] - b15["fmax"]
    spread_b = max(b15f) - min(b15f)
    spread_k = max(k15f) - min(k15f)
    out += ["### Rule (test plan section 5), items 2-5 (item 1 = tests, see result_9s2.md)",
            f"- 2. timing met at 40.000 ns at every seed: {'met' if r2 else 'NOT met'} ({k40['nmet']} of 6)",
            f"- 3. ALM median {k40['alm']:,.1f} at most 20,000: {'met' if r3 else 'NOT met'}",
            f"- 4. latency at 15 ns (median Fmax) of K2 against K1b: KeyGen {vs[0] * 100:+.2f} %, Encaps {vs[1] * 100:+.2f} %, Decaps {vs[2] * 100:+.2f} % (needs lower for each): {'met' if r4 else 'NOT met'}",
            f"- 5. at 15 ns timing met at {k15['nmet']} of 6 seeds (K1b: {b15['nmet']} of 6; stated)",
            f"- Fmax gain of the median at 15 ns: {gain:+.3f} MHz; spread over six seeds: K2 {spread_k:.2f} MHz, K1b {spread_b:.2f} MHz; the gain is {'larger' if gain > max(spread_b, spread_k) else 'NOT larger'} than the larger spread; K2 lowest {k15['fmin']:.2f} against K1b highest {max(b15f):.2f} MHz",
            f"- Information: ALM median K2 - K1b = {k40['alm'] - b40['alm']:+,.1f} (40 ns), {k15['alm'] - b15['alm']:+,.1f} (15 ns); Fmax at 40 ns median K2 - K1b = {k40['fmax'] - b40['fmax']:+.3f} MHz"]
    (E2 / f"selection_worksheet_{date}.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
