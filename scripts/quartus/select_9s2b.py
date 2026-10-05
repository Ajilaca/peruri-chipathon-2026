#!/usr/bin/env python3
"""scripts/quartus/select_9s2b.py -- Phase 9F step S2b worksheet (evidence/phase9m/batch2/9s2b/test_plan_9s2b.md sections 4, 5, 7, 8; ADR 0039): K3 (S2b) at 15.000 ns, seeds 1-6 (the rule) and 1-9 (amendment A2, information), at 40.000 ns, seeds 1-6; reference K2 (9s2).
Writes evidence/phase9m/batch2/9s2b/selection_worksheet_<date>.md. Every value is copied from an evidence file; t = cycles / Fmax is perhitungan tim.
Usage: python3 scripts/quartus/select_9s2b.py [date YYYY-MM-DD]
"""
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import select_9f1 as S1  # noqa: E402

E9M = S1.E9M
E3, E2 = E9M / "batch2" / "9s2b", E9M / "batch2" / "9s2"
CYC = (8416, 10250, 15619)   # K2 = K3 profile inputs: batch2/9s2b/profile_k3_verilator.json (equal to batch2/9s2/profile_k2_verilator.json)


def main():
    date = sys.argv[1] if len(sys.argv) > 1 else "2026-10-05"
    out = []
    o, k6 = S1.table("K3 at 15.000 ns, seeds 1-6 (the rule of the plan)", E3, [f"K3-15-s{s}" for s in range(1, 7)], 15.0)
    out += o
    o, k9 = S1.table("K3 at 15.000 ns, seeds 1-9 (amendment A2: three additional seeds chosen after the result of the first six)", E3, [f"K3-15-s{s}" for s in range(1, 10)], 15.0)
    out += o
    o, k40 = S1.table("K3 at 40.000 ns, seeds 1-6 (the gate)", E3, ["K3"] + [f"K3-s{s}" for s in range(2, 7)], 40.0)
    out += o
    o, b15 = S1.table("Reference K2 at 15.000 ns, seeds 1-6", E2, [f"K2-15-s{s}" for s in range(1, 7)], 15.0)
    out += o
    o, b40 = S1.table("Reference K2 at 40.000 ns, seeds 1-6", E2, ["K2"] + [f"K2-s{s}" for s in range(2, 7)], 40.0)
    out += o
    f3 = [S1.parse(E3, f"K3-15-s{s}")["fmax"] for s in range(1, 10)]
    f2 = [S1.parse(E2, f"K2-15-s{s}")["fmax"] for s in range(1, 7)]
    L = S1.lat
    out += ["## Latency (perhitungan tim: profile-input cycles / Fmax; cycles equal in K2 and K3; kernel-only static timing, not a board measurement)",
            "| Configuration | Cycles KeyGen / Encaps / Decaps | Fmax (MHz) | Latency KeyGen / Encaps / Decaps (us) |", "|---|---|---|---|",
            f"| K3 at 15 ns (median of 6) | {' / '.join(f'{c:,}' for c in CYC)} | {k6['fmax']:.3f} | {L(CYC, k6['fmax'])} |",
            f"| K3 at 15 ns (median of 9) | same | {k9['fmax']:.3f} | {L(CYC, k9['fmax'])} |",
            f"| K3 at 15 ns (lowest of 6) | same | {k6['fmin']:.2f} | {L(CYC, k6['fmin'])} |",
            f"| K2 at 15 ns (median of 6) | same | {b15['fmax']:.3f} | {L(CYC, b15['fmax'])} |",
            f"| K2 at 15 ns (lowest of 6) | same | {b15['fmin']:.2f} | {L(CYC, b15['fmin'])} |", ""]
    r2, r3 = k40["nmet"] == 6, k40["alm"] <= 20000
    vs = [(CYC[i] / k6["fmax"]) / (CYC[i] / b15["fmax"]) - 1 for i in range(3)]
    r4 = all(x < 0 for x in vs)
    gain6 = k6["fmax"] - b15["fmax"]
    sp3, sp2, sp9 = max(f3[:6]) - min(f3[:6]), max(f2) - min(f2), max(f3) - min(f3)
    r5 = gain6 > max(sp3, sp2) or min(f3[:6]) > max(f2)
    above = sum(1 for x in f3[:6] if x > max(f2))
    above9 = sum(1 for x in f3 if x > max(f2))
    out += ["### Rule (test plan section 5), items 2-6 (item 1 = tests, see result_9s2b.md)",
            f"- 2. timing met at 40.000 ns at every seed: {'met' if r2 else 'NOT met'} ({k40['nmet']} of 6)",
            f"- 3. ALM median {k40['alm']:,.1f} (40 ns) at most 20,000: {'met' if r3 else 'NOT met'}",
            f"- 4. latency at 15 ns (median Fmax of 6 seeds) of K3 against K2: KeyGen {vs[0] * 100:+.2f} %, Encaps {vs[1] * 100:+.2f} %, Decaps {vs[2] * 100:+.2f} % (needs lower for each): {'met' if r4 else 'NOT met'}",
            f"- 5. median Fmax gain over K2 (six seeds): {gain6:+.3f} MHz; spread of K3 {sp3:.2f} MHz, of K2 {sp2:.2f} MHz; K3 lowest {min(f3[:6]):.2f} against K2 highest {max(f2):.2f} MHz: **{'met' if r5 else 'NOT met as written'}**",
            f"- 6. at 15 ns timing met at {k6['nmet']} of 6 seeds (K2: {b15['nmet']} of 6)",
            f"- Information (amendment A2): seeds of K3 above the highest seed of K2 ({max(f2):.2f} MHz): {above} of 6, {above9} of 9; K3 nine seeds median {k9['fmax']:.3f} MHz, spread {sp9:.2f} MHz, met at {k9['nmet']} of 9; Fmax of the seeds: " + ", ".join(f"s{i+1} {x:.2f}" for i, x in enumerate(f3)),
            f"- Information: ALM median K3 - K2 = {k40['alm'] - b40['alm']:+,.1f} (40 ns), {k6['alm'] - b15['alm']:+,.1f} (15 ns, six seeds); registers 15 ns K3 {min(S1.parse(E3, f'K3-15-s{s}')['regs'] for s in range(1, 7))}-{max(S1.parse(E3, f'K3-15-s{s}')['regs'] for s in range(1, 7))}"]
    (E3 / f"selection_worksheet.md").write_text("\n".join(out) + "\n")
    print("\n".join(out[-12:]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
