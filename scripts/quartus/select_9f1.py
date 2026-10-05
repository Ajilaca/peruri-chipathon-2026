#!/usr/bin/env python3
"""scripts/quartus/select_9f1.py -- Phase 9F step S1 worksheet (evidence/phase9m/batch1/9f1/test_plan_9f1.md sections 4 and 5): reads the Quartus evidence files of K1 (40.000 ns, seeds 1-6) and K1-15 (15.000 ns, seeds 1-6),
and, as references, MW (40 ns, 9m1), MW-20 (20 ns, 9m1 / 9m2) and F15 (15 ns, S0, two seeds); writes evidence/phase9m/batch1/9f1/selection_worksheet_<date>.md. Every value is copied from an evidence file;
t = cycles / Fmax is perhitungan tim.
Usage: python3 scripts/quartus/select_9f1.py [date YYYY-MM-DD]
"""
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
E9M = ROOT / "evidence" / "phase9m"
E1, E2, E0, EF1 = E9M / "batch1" / "9m1", E9M / "batch1" / "9m2", E9M / "batch1" / "9f0", E9M / "batch1" / "9f1"
CYC = {"MW": (8327, 10159, 15515), "K1": (8795, 10627, 15983)}   # profile inputs: batch1/9m1/profile_w2_verilator.json and batch1/9f1/profile_k1_verilator.json
MW20_LAT = (130.1, 158.8, 242.5)                                 # batch1/9m2/selection_worksheet.md, MW at 20 ns (median Fmax 63.990 MHz)


def num(s):
    return float(s.replace(",", ""))


def parse(ev, rev):
    f = sorted(ev.glob(f"quartus_{rev}.md"))[-1]
    t = f.read_text()
    g = lambda pat: int(num(re.search(pat, t).group(1)))  # noqa: E731
    fm = [num(x) for x in re.findall(r"Slow 1100mV [-\d]+C Model Fmax Summary \| ([\d.]+) MHz", t)]
    return dict(alm=g(r"Logic utilization \(in ALMs\) \| ([\d,]+)"), regs=g(r"Total registers \| ([\d,]+)"), dsp=g(r"Total DSP Blocks \| ([\d,]+)"), m10k=g(r"Total RAM Blocks \| ([\d,]+)"),
                setup=num(re.search(r"Worst setup slack: \*\*(-?[\d.]+) ns", t).group(1)), hold=num(re.search(r"Worst hold slack: \*\*(-?[\d.]+) ns", t).group(1)), fmax=min(fm), crit=g(r"Critical warnings: (\d+)"), file=f.relative_to(ROOT))


def table(title, ev, revs, per):
    rows = [(rev, parse(ev, rev)) for rev in revs]
    out = [f"## {title} (MEASURED, kernel-only, virtual pins)", "| Revision | ALM | Registers | RAM blocks | DSP | Worst setup / hold (ns) | Timing met | Fmax lowest slow corner (MHz) | Critical warnings | Evidence |", "|---|---|---|---|---|---|---|---|---|---|"]
    for rev, r in rows:
        met = r["setup"] >= 0 and r["hold"] >= 0
        out.append(f"| {rev} | {r['alm']:,} | {r['regs']} | {r['m10k']} | {r['dsp']} | {r['setup']:.3f} / {r['hold']:.3f} | {'yes' if met else '**NO**'} | {r['fmax']:.2f} | {r['crit']} | `{r['file']}` |")
    alms, fms = [r["alm"] for _, r in rows], [r["fmax"] for _, r in rows]
    nmet = sum(1 for _, r in rows if r["setup"] >= 0 and r["hold"] >= 0)
    st = dict(alm=statistics.median(alms), fmax=statistics.median(fms), nmet=nmet, n=len(rows), fmin=min(fms))
    out += ["", f"ALM median (min-max) {st['alm']:,.1f} ({min(alms):,}-{max(alms):,}); registers {min(r['regs'] for _, r in rows)}-{max(r['regs'] for _, r in rows)}; RAM blocks {min(r['m10k'] for _, r in rows)}-{max(r['m10k'] for _, r in rows)}; DSP {min(r['dsp'] for _, r in rows)}-{max(r['dsp'] for _, r in rows)}",
            f"Worst setup slack over seeds {min(r['setup'] for _, r in rows):.3f} ns; Fmax lowest slow corner median (min-max) {st['fmax']:.3f} ({st['fmin']:.2f}-{max(fms):.2f}) MHz",
            f"**Timing met at {per:.3f} ns at {nmet} of {len(rows)} seeds**", ""]
    return out, st


def lat(c, f):
    return " / ".join(f"{x / f:.1f}" for x in c)


def main():
    date = sys.argv[1] if len(sys.argv) > 1 else "2026-10-04"
    out = []
    o, k40 = table("K1 at 40.000 ns, seeds 1-6 (the gate)", EF1, ["K1"] + [f"K1-s{s}" for s in range(2, 7)], 40.0)
    out += o
    o, k15 = table("K1 at 15.000 ns, seeds 1-6 (information, ADR 0036 point 3)", EF1, [f"K1-15-s{s}" for s in range(1, 7)], 15.0)
    out += o
    o, w40 = table("Reference MW (9M-1 core) at 40.000 ns, seeds 1-6", E1, ["MW"] + [f"MW-s{s}" for s in range(2, 7)], 40.0)
    out += o
    o, w15 = table("Reference MW (9M-1 core) at 15.000 ns, seeds 1-2 (S0)", E0, ["F15-s1", "F15-s2"], 15.0)
    out += o
    out += ["## Latency (perhitungan tim: profile-input cycles / Fmax; kernel-only static timing, not a board measurement)",
            "| Configuration | Cycles KeyGen / Encaps / Decaps | Fmax (MHz) | Latency KeyGen / Encaps / Decaps (us) |", "|---|---|---|---|",
            f"| K1 at 15 ns (median of 6) | {' / '.join(f'{c:,}' for c in CYC['K1'])} | {k15['fmax']:.3f} | {lat(CYC['K1'], k15['fmax'])} |",
            f"| K1 at 15 ns (lowest of 6) | same | {k15['fmin']:.2f} | {lat(CYC['K1'], k15['fmin'])} |",
            f"| K1 at 40 ns (median of 6) | same | {k40['fmax']:.3f} | {lat(CYC['K1'], k40['fmax'])} |",
            f"| MW at 15 ns (lower of 2 seeds, S0) | {' / '.join(f'{c:,}' for c in CYC['MW'])} | {w15['fmin']:.2f} | {lat(CYC['MW'], w15['fmin'])} |",
            f"| MW at 20 ns (median of 6, 9M-2; rule reference) | same | 63.990 | {' / '.join(f'{x}' for x in MW20_LAT)} |",
            f"| MW at 40 ns (median of 6) | same | {w40['fmax']:.3f} | {lat(CYC['MW'], w40['fmax'])} |", ""]
    r2, r3 = k40["nmet"] == 6, k40["alm"] <= 20000
    ratios = [(CYC["K1"][i] / k15["fmax"]) / MW20_LAT[i] - 1 for i in range(3)]
    r4 = all(x <= 0.03 for x in ratios)
    out += ["### Rule (test plan section 5), items 2-5 (item 1 = tests, see result_9f1.md)",
            f"- 2. timing met at 40.000 ns at every seed: {'met' if r2 else 'NOT met'} ({k40['nmet']} of 6)",
            f"- 3. ALM median {k40['alm']:,.1f} at most 20,000: {'met' if r3 else 'NOT met'}",
            f"- 4. latency of K1 at the median Fmax at 15 ns against MW at 20 ns (130.1 / 158.8 / 242.5 us): KeyGen {ratios[0] * 100:+.2f} %, Encaps {ratios[1] * 100:+.2f} %, Decaps {ratios[2] * 100:+.2f} % (needs <= +3 % each): {'met' if r4 else 'NOT met'}",
            f"- 5. at 15 ns timing met at {k15['nmet']} of 6 seeds (stated, not a pass/fail item)"]
    (EF1 / f"selection_worksheet.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
