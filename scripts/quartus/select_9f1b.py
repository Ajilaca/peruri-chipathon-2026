#!/usr/bin/env python3
"""scripts/quartus/select_9f1b.py -- Phase 9F step S1b worksheet (evidence/phase9m/batch1/9f1b/test_plan_9f1b.md sections 4 and 5, ADR 0039: 15 ns is the reporting limit): reads the Quartus evidence files of K1b (40.000 ns, seeds 1-6) and K1b-15 (15.000 ns, seeds 1-6);
references: K1 (9f1), MW (9m1), F15 (S0). Writes evidence/phase9m/batch1/9f1b/selection_worksheet_<date>.md. Every value is copied from an evidence file; t = cycles / Fmax is perhitungan tim.
Usage: python3 scripts/quartus/select_9f1b.py [date YYYY-MM-DD]
"""
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import select_9f1 as S1  # noqa: E402

E9M = S1.E9M
EB = E9M / "batch1" / "9f1b"
CYC = {"MW": (8327, 10159, 15515), "K1": (8795, 10627, 15983), "K1b": (8404, 10236, 15597)}   # profile inputs: 9m1, 9f1, 9f1b profile JSON files


def main():
    date = sys.argv[1] if len(sys.argv) > 1 else "2026-10-04"
    out = []
    o, b40 = S1.table("K1b at 40.000 ns, seeds 1-6 (the gate)", EB, ["K1b"] + [f"K1b-s{s}" for s in range(2, 7)], 40.0)
    out += o
    o, b15 = S1.table("K1b at 15.000 ns, seeds 1-6 (reporting limit, ADR 0039)", EB, [f"K1b-15-s{s}" for s in range(1, 7)], 15.0)
    out += o
    o, k40 = S1.table("Reference K1 at 40.000 ns, seeds 1-6", S1.EF1, ["K1"] + [f"K1-s{s}" for s in range(2, 7)], 40.0)
    out += o
    o, k15 = S1.table("Reference K1 at 15.000 ns, seeds 1-6", S1.EF1, [f"K1-15-s{s}" for s in range(1, 7)], 15.0)
    out += o
    o, w15 = S1.table("Reference MW (9M-1 core) at 15.000 ns, seeds 1-2 (S0)", S1.E0, ["F15-s1", "F15-s2"], 15.0)
    out += o
    L = S1.lat
    out += ["## Latency (perhitungan tim: profile-input cycles / Fmax; kernel-only static timing, not a board measurement)",
            "| Configuration | Cycles KeyGen / Encaps / Decaps | Fmax (MHz) | Latency KeyGen / Encaps / Decaps (us) |", "|---|---|---|---|",
            f"| K1b at 15 ns (median of 6) | {' / '.join(f'{c:,}' for c in CYC['K1b'])} | {b15['fmax']:.3f} | {L(CYC['K1b'], b15['fmax'])} |",
            f"| K1b at 15 ns (lowest of 6) | same | {b15['fmin']:.2f} | {L(CYC['K1b'], b15['fmin'])} |",
            f"| K1 at 15 ns (median of 6) | {' / '.join(f'{c:,}' for c in CYC['K1'])} | {k15['fmax']:.3f} | {L(CYC['K1'], k15['fmax'])} |",
            f"| MW at 15 ns (lower of 2 seeds, S0) | {' / '.join(f'{c:,}' for c in CYC['MW'])} | {w15['fmin']:.2f} | {L(CYC['MW'], w15['fmin'])} |",
            f"| K1b at 40 ns (median of 6) | same as K1b | {b40['fmax']:.3f} | {L(CYC['K1b'], b40['fmax'])} |", ""]
    r2, r3 = b40["nmet"] == 6, b40["alm"] <= 20000
    vs_k1 = [(CYC["K1b"][i] / b15["fmax"]) / (CYC["K1"][i] / k15["fmax"]) - 1 for i in range(3)]
    r4 = all(x < 0 for x in vs_k1)
    vs_mw = [(CYC["K1b"][i] / b15["fmax"]) / (CYC["MW"][i] / w15["fmin"]) - 1 for i in range(3)]
    out += ["### Rule (test plan section 5), items 2-5 (item 1 = tests, see result_9f1b.md)",
            f"- 2. timing met at 40.000 ns at every seed: {'met' if r2 else 'NOT met'} ({b40['nmet']} of 6)",
            f"- 3. ALM median {b40['alm']:,.1f} at most 20,000: {'met' if r3 else 'NOT met'}",
            f"- 4. latency at 15 ns (median Fmax) of K1b against K1: KeyGen {vs_k1[0] * 100:+.2f} %, Encaps {vs_k1[1] * 100:+.2f} %, Decaps {vs_k1[2] * 100:+.2f} % (needs lower for each): {'met' if r4 else 'NOT met'}",
            f"- 5. at 15 ns timing met at {b15['nmet']} of 6 seeds (K1: {k15['nmet']} of 6; stated)",
            f"- Information: K1b against MW at 15 ns (S0, lower Fmax of two seeds): KeyGen {vs_mw[0] * 100:+.2f} %, Encaps {vs_mw[1] * 100:+.2f} %, Decaps {vs_mw[2] * 100:+.2f} %",
            f"- Information: ALM median K1b - K1 = {b40['alm'] - k40['alm']:+,.1f} (40 ns), {b15['alm'] - k15['alm']:+,.1f} (15 ns)"]
    (EB / f"selection_worksheet.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
