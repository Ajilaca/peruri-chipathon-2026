#!/usr/bin/env python3
"""scripts/select_9f0.py -- Phase 9F step S0 worksheet (docs/evidence/phase09m-optimisation/9f0/test_plan_9f0.md sections 4 and 5): reads the Quartus evidence files F16 / F15 / F14 / H14 / F13 (seeds 1 and 2) of the 9M-1 core
and writes docs/evidence/phase09m-optimisation/9f0/selection_worksheet_<date>.md. Every value is copied from an evidence file; t = cycles / Fmax is perhitungan tim.
Usage: python3 scripts/select_9f0.py [date YYYY-MM-DD]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
E0 = ROOT / "docs" / "evidence" / "phase09m-optimisation" / "9f0"
CYC = (8327, 10159, 15515)      # 9M-1 core profile inputs: 9m1/profile_w2_verilator_2026-10-04.json
GROUPS = [("F16", 16.0), ("F15", 15.0), ("F14", 14.0), ("H14", 14.0), ("F13", 13.0)]   # F13: amendment A2 (the sweep stopped at 13 ns: first constraint not met)


def num(s):
    return float(s.replace(",", ""))


def parse(rev):
    f = sorted(E0.glob(f"quartus_{rev}-2026*.md"))[-1]
    t = f.read_text()
    g = lambda pat: int(num(re.search(pat, t).group(1)))  # noqa: E731
    fm = [num(x) for x in re.findall(r"Slow 1100mV [-\d]+C Model Fmax Summary \| ([\d.]+) MHz", t)]
    return dict(alm=g(r"Logic utilization \(in ALMs\) \| ([\d,]+)"), regs=g(r"Total registers \| ([\d,]+)"), dsp=g(r"Total DSP Blocks \| ([\d,]+)"), m10k=g(r"Total RAM Blocks \| ([\d,]+)"),
                setup=num(re.search(r"Worst setup slack: \*\*(-?[\d.]+) ns", t).group(1)), hold=num(re.search(r"Worst hold slack: \*\*(-?[\d.]+) ns", t).group(1)), fmax=min(fm), crit=g(r"Critical warnings: (\d+)"), file=f.relative_to(ROOT))


def main():
    date = sys.argv[1] if len(sys.argv) > 1 else "2026-10-04"
    out = ["## S0: the 9M-1 core (`CODEC_W2 = 1`, C5 hash and sampler) under tighter constraints (MEASURED, kernel-only, virtual pins)",
           "| Revision | Constraint (ns) | Effort | ALM | Registers | RAM blocks | DSP | Worst setup / hold (ns) | Timing met | Fmax lowest slow corner (MHz) | Critical warnings | Evidence |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    summ = []
    for grp, per in GROUPS:
        rs = []
        for seed in (1, 2):
            rev = f"{grp}-s{seed}"
            r = parse(rev)
            met = r["setup"] >= 0 and r["hold"] >= 0
            out.append(f"| {rev} | {per:.3f} | {'high performance' if grp[0] == 'H' else 'defaults'} | {r['alm']:,} | {r['regs']} | {r['m10k']} | {r['dsp']} | {r['setup']:.3f} / {r['hold']:.3f} | {'yes' if met else '**NO**'} | {r['fmax']:.2f} | {r['crit']} | `{r['file']}` |")
            rs.append((met, r))
        summ.append((grp, per, rs))
    out += ["", "### Per constraint", "| Group | Constraint (ns) | Met at k of 2 seeds | Lower Fmax of the two (MHz) | Worst setup of the two (ns) | ALM (min-max) | Latency KeyGen / Encaps / Decaps at the lower Fmax (us, perhitungan tim) |", "|---|---|---|---|---|---|---|"]
    for grp, per, rs in summ:
        k = sum(1 for m, _ in rs if m)
        fl = min(r["fmax"] for _, r in rs)
        out.append(f"| {grp} | {per:.3f} | {k} of 2 | {fl:.2f} | {min(r['setup'] for _, r in rs):.3f} | {min(r['alm'] for _, r in rs):,}-{max(r['alm'] for _, r in rs):,} | " + " / ".join(f"{c / fl:.1f}" for c in CYC) + " |")
    both = [(g, p) for g, p, rs in summ if all(m for m, _ in rs)]
    out += ["", "### Rule (test plan section 5)", "- Information, no adoption. The limit of the existing design is the tightest constraint met at both seeds: " + (", ".join(f"{g} ({p:.0f} ns)" for g, p in both) if both else "none") + ".",
            "- Amendment A2 (extended sweep, rule: stop at the first constraint not met): the sweep stopped at 13 ns (seed 1 met, seed 2 not met); the limit lies between 13 and 14 ns for this design and these settings."]
    (E0 / f"selection_worksheet_{date}.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
