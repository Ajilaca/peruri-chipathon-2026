#!/usr/bin/env python3
"""scripts/select_9i4.py -- Phase 9I item 4 worksheet (docs/evidence/phase09m-optimisation/9i4/test_plan_9i4.md sections 4 and 5; ADR 0039): K4 (mlkem_core4, K3 parameters) at 15.000 ns and 40.000 ns, seeds 1-6; reference K3 (9s2b).
Writes docs/evidence/phase09m-optimisation/9i4/selection_worksheet_<date>.md. Every value is copied from an evidence file; t = cycles / Fmax is perhitungan tim.
Usage: python3 scripts/select_9i4.py [date YYYY-MM-DD]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import select_9f1 as S1  # noqa: E402

E9M = S1.E9M
E4, E3 = E9M / "9i4", E9M / "9s2b"
CYC = {"K3": (8416, 10250, 15619), "K4": (8416, 9611, 12989)}   # profile inputs: 9s2b/profile_k3_verilator_2026-10-05.json and 9i4/profile_k4_verilator_2026-10-05.json


def main():
    date = sys.argv[1] if len(sys.argv) > 1 else "2026-10-05"
    out = []
    o, k15 = S1.table("K4 at 15.000 ns, seeds 1-6 (reporting limit, ADR 0039)", E4, [f"K4-15-s{s}" for s in range(1, 7)], 15.0)
    out += o
    o, k40 = S1.table("K4 at 40.000 ns, seeds 1-6 (the gate)", E4, ["K4"] + [f"K4-s{s}" for s in range(2, 7)], 40.0)
    out += o
    o, b15 = S1.table("Reference K3 at 15.000 ns, seeds 1-6", E3, [f"K3-15-s{s}" for s in range(1, 7)], 15.0)
    out += o
    o, b40 = S1.table("Reference K3 at 40.000 ns, seeds 1-6", E3, ["K3"] + [f"K3-s{s}" for s in range(2, 7)], 40.0)
    out += o
    f4 = [S1.parse(E4, f"K4-15-s{s}")["fmax"] for s in range(1, 7)]
    f3 = [S1.parse(E3, f"K3-15-s{s}")["fmax"] for s in range(1, 7)]
    L = S1.lat
    out += ["## Latency (perhitungan tim: profile-input cycles / Fmax; kernel-only static timing, not a board measurement)",
            "| Configuration | Cycles KeyGen / Encaps / Decaps | Fmax (MHz) | Latency KeyGen / Encaps / Decaps (us) |", "|---|---|---|---|",
            f"| K4 at 15 ns (median of 6) | {' / '.join(f'{c:,}' for c in CYC['K4'])} | {k15['fmax']:.3f} | {L(CYC['K4'], k15['fmax'])} |",
            f"| K4 at 15 ns (lowest of 6) | same | {k15['fmin']:.2f} | {L(CYC['K4'], k15['fmin'])} |",
            f"| K3 at 15 ns (median of 6) | {' / '.join(f'{c:,}' for c in CYC['K3'])} | {b15['fmax']:.3f} | {L(CYC['K3'], b15['fmax'])} |",
            f"| K3 at 15 ns (lowest of 6) | same | {b15['fmin']:.2f} | {L(CYC['K3'], b15['fmin'])} |", ""]
    r2 = k40["nmet"] == 6 and k15["nmet"] == 6
    r3 = k40["alm"] <= 20000 and k15["alm"] <= 20000
    t = [(CYC["K4"][i] / k15["fmax"]) / (CYC["K3"][i] / b15["fmax"]) - 1 for i in range(3)]
    r4 = t[1] < 0 and t[2] < 0 and t[0] <= 0.03
    drop = b15["fmax"] - k15["fmax"]
    sp4, sp3 = max(f4) - min(f4), max(f3) - min(f3)
    out += ["### Rule (test plan section 5), items 2-5 (item 1 = tests and controls, see result_9i4.md)",
            f"- 2. timing met at 40.000 ns at {k40['nmet']} of 6 seeds and at 15.000 ns at {k15['nmet']} of 6 seeds: {'met' if r2 else 'NOT met'}",
            f"- 3. ALM median {k40['alm']:,.1f} (40 ns) and {k15['alm']:,.1f} (15 ns) at most 20,000: {'met' if r3 else 'NOT met'}",
            f"- 4. latency at 15 ns (median Fmax) of K4 against K3: KeyGen {t[0] * 100:+.2f} % (at most +3 %), Encaps {t[1] * 100:+.2f} %, Decaps {t[2] * 100:+.2f} % (needs lower): {'met' if r4 else 'NOT met'}",
            f"- 5. median Fmax K4 {k15['fmax']:.3f} against K3 {b15['fmax']:.3f} MHz ({-drop:+.3f} MHz); spread K4 {sp4:.2f} MHz, K3 {sp3:.2f} MHz; K4 lowest {k15['fmin']:.2f}, highest {max(f4):.2f}; K3 lowest {b15['fmin']:.2f}, highest {max(f3):.2f}; an Fmax drop larger than the larger spread: {'YES' if drop > max(sp4, sp3) else 'no'}; seeds met at 15 ns {k15['nmet']} of 6",
            f"- Information: ALM median K4 - K3 = {k40['alm'] - b40['alm']:+,.1f} (40 ns), {k15['alm'] - b15['alm']:+,.1f} (15 ns); Fmax of the K4 seeds: " + ", ".join(f"s{i+1} {x:.2f}" for i, x in enumerate(f4))]
    (E4 / f"selection_worksheet_{date}.md").write_text("\n".join(out) + "\n")
    print("\n".join(out[-14:]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
