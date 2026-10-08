#!/usr/bin/env python3
"""scripts/quartus/select_9m1.py -- Phase 9M item 1 worksheet (evidence/phase9m/batch1/9m1/test_plan_9m1.md sections 5 and 6): reads the Quartus evidence files of the revisions MW, MW-s2 .. MW-s6 and MW-20 (9m1), the
Phase 9c files of MC (evidence/phase09/9c) and the two profile files, applies the numeric items 2-4 of the adoption rule and writes evidence/phase9m/batch1/9m1/selection_worksheet_<date>.md.
Items 1 and the correctness tests of the rule (V1-V3, V5-V7) are checked by their own logs and listed in result_9m1.md, not here. Nothing is computed from slack: every value is copied from the evidence file.
Usage: python3 scripts/quartus/select_9m1.py [date YYYY-MM-DD]
"""
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
E9C = ROOT / "evidence" / "phase09" / "9c"
E9M = ROOT / "evidence" / "phase9m"
E1 = E9M / "batch1" / "9m1"
REVS = [("MW", 1), ("MW-s2", 2), ("MW-s3", 3), ("MW-s4", 4), ("MW-s5", 5), ("MW-s6", 6)]
BASE_REVS = [("MC", 1), ("MC-s2", 2), ("MC-s3", 3), ("MC-s4", 4), ("MC-s5", 5), ("MC-s6", 6)]


def num(s):
    return float(s.replace(",", ""))


def parse(ev, rev):
    f = sorted(ev.glob(f"quartus_{rev}.md"))[-1]
    t = f.read_text()
    g = lambda pat: int(num(re.search(pat, t).group(1)))  # noqa: E731
    fm = [num(x) for x in re.findall(r"Slow 1100mV [-\d]+C Model Fmax Summary \| ([\d.]+) MHz", t)]
    return dict(alm=g(r"Logic utilization \(in ALMs\) \| ([\d,]+)"), regs=g(r"Total registers \| ([\d,]+)"), membits=g(r"Total block memory bits \| ([\d,]+)"), dsp=g(r"Total DSP Blocks \| ([\d,]+)"),
                m10k=g(r"Total RAM Blocks \| ([\d,]+)"),
                setup=num(re.search(r"Slack setup terburuk: \*\*(-?[\d.]+) ns", t).group(1)), hold=num(re.search(r"Slack hold terburuk: \*\*(-?[\d.]+) ns", t).group(1)), fmax=min(fm),
                crit=g(r"Peringatan kritis: (\d+)"), file=f.name)


def main():
    date = sys.argv[1] if len(sys.argv) > 1 else "2026-10-04"
    rows = [(rev, seed, parse(E1, rev)) for rev, seed in REVS]
    base = [parse(E9C, rev) for rev, _ in BASE_REVS]
    out = ["## Per seed at 40.000 ns (MEASURED), revision MW (CODEC_W2 = 1)",
           "| Seed | ALM | Registers | RAM blocks | Block memory bits | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Critical warnings | Evidence |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for rev, seed, r in rows:
        met = "yes" if r["setup"] >= 0 and r["hold"] >= 0 else "**NO**"
        out.append(f"| {seed} | {r['alm']:,} | {r['regs']} | {r['m10k']} | {r['membits']:,} | {r['dsp']} | {r['setup']:.3f} / {r['hold']:.3f} | {met} | {r['fmax']:.2f} | {r['crit']} | `{r['file']}` |")
    alms, fms = [r["alm"] for _, _, r in rows], [r["fmax"] for _, _, r in rows]
    balms, bfms = [r["alm"] for r in base], [r["fmax"] for r in base]
    mw_alm, mw_fmax = statistics.median(alms), statistics.median(fms)
    mc_alm, mc_fmax = statistics.median(balms), statistics.median(bfms)
    out += ["", f"MW: ALM median (min-max) {mw_alm:,.1f} ({min(alms):,}-{max(alms):,}); registers {min(r['regs'] for _, _, r in rows)}-{max(r['regs'] for _, _, r in rows)}; RAM blocks {min(r['m10k'] for _, _, r in rows)}-{max(r['m10k'] for _, _, r in rows)}; "
            f"DSP {min(r['dsp'] for _, _, r in rows)}-{max(r['dsp'] for _, _, r in rows)}; Fmax median (min-max) {mw_fmax:.3f} ({min(fms):.2f}-{max(fms):.2f}) MHz",
            f"Phase 9c baseline MC (`evidence/phase09/9c/`): ALM median {mc_alm:,.1f} ({min(balms):,}-{max(balms):,}); registers {min(r['regs'] for r in base)}-{max(r['regs'] for r in base)}; RAM blocks {min(r['m10k'] for r in base)}-{max(r['m10k'] for r in base)}; Fmax median {mc_fmax:.3f} ({min(bfms):.2f}-{max(bfms):.2f}) MHz",
            f"Difference MW - MC: ALM {mw_alm - mc_alm:+,.1f}, Fmax {mw_fmax - mc_fmax:+.3f} MHz"]
    r20 = parse(E1, "MW-20")
    out.append(f"Information MW-20 (20.000 ns), seed 1: ALM {r20['alm']:,}, registers {r20['regs']}, worst setup {r20['setup']:.3f} ns ({'met' if r20['setup'] >= 0 and r20['hold'] >= 0 else 'NOT met'}), Fmax lowest slow corner {r20['fmax']:.2f} MHz (`{r20['file']}`)")
    p0 = json.loads((E9M / "profile_verilator.json").read_text())
    p1 = json.loads((E1 / "profile_w2_verilator.json").read_text())
    out += ["", "## Cycles and time (profile inputs, MEASURED in simulation; t = cycles / median Fmax is INFERENCE / perhitungan tim, kernel-only static timing, not a board measurement)",
            "| Operation | Phase 9 cycles | 9M-1 cycles | Change | t Phase 9 (us) at median Fmax of MC | t 9M-1 (us) at median Fmax of MW | Lower? |", "|---|---|---|---|---|---|---|"]
    lower = True
    for n, label in (("keygen", "KeyGen"), ("encaps", "Encaps"), ("decaps", "Decaps")):
        c0, c1 = p0[n]["cycles"], p1[n]["cycles"]
        t0, t1 = c0 / mc_fmax, c1 / mw_fmax
        lower &= t1 < t0
        out.append(f"| {label} | {c0:,} | {c1:,} | {100 * (c1 / c0 - 1):+.1f} % | {t0:.1f} | {t1:.1f} | {'yes' if t1 < t0 else '**NO**'} |")
    met_all = all(r["setup"] >= 0 and r["hold"] >= 0 for _, _, r in rows)
    alm_ok = mw_alm <= mc_alm + 1000
    out += ["", "### Numeric items of the adoption rule (test plan section 6)",
            f"- {'PASS' if met_all else 'FAIL'}: item 2, timing met at 40.000 ns at every seed 1-6",
            f"- {'PASS' if lower else 'FAIL'}: item 3, t of KeyGen, Encaps and Decaps lower than Phase 9 (table above)",
            f"- {'PASS' if alm_ok else 'FAIL'}: item 4, ALM median of MW at most 1,000 above the Phase 9 median ({mw_alm - mc_alm:+,.1f})",
            "- items 1 (V1-V3, V5-V7) are the logs listed in `result_9m1.md`"]
    (E1 / f"selection_worksheet.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))
    return 0 if met_all and lower and alm_ok else 1


if __name__ == "__main__":
    sys.exit(main())
