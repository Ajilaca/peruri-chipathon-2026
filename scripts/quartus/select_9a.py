#!/usr/bin/env python3
"""scripts/quartus/select_9a.py -- Phase 9a worksheet (evidence/phase09/9a/test_plan_9a.md section 5): reads the Quartus evidence files of the revisions CD, CD-s2 .. CD-s6 and CD-20 and
the cycle tables of the simulations, writes evidence/phase09/9a/selection_worksheet_<date>.md. Nothing is computed from slack: every value is copied from the evidence file.
Usage: python3 scripts/quartus/select_9a.py <cycles_dir> [date YYYY-MM-DD]
"""
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EV = ROOT / "evidence" / "phase09" / "9a"
REVS = [("CD", 1), ("CD-s2", 2), ("CD-s3", 3), ("CD-s4", 4), ("CD-s5", 5), ("CD-s6", 6)]


def num(s):
    return float(s.replace(",", ""))


def parse(rev):
    f = EV / f"quartus_{rev}.md"
    t = f.read_text()
    alm = int(num(re.search(r"Logic utilization \(in ALMs\) \| ([\d,]+)", t).group(1)))
    regs = int(num(re.search(r"Total registers \| ([\d,]+)", t).group(1)))
    m10k = int(num(re.search(r"Total block memory bits \| ([\d,]+)", t).group(1)))
    dsp = int(num(re.search(r"Total DSP Blocks \| ([\d,]+)", t).group(1)))
    setup = num(re.search(r"Worst setup slack: \*\*(-?[\d.]+) ns", t).group(1))
    hold = num(re.search(r"Worst hold slack: \*\*(-?[\d.]+) ns", t).group(1))
    fm = [num(x) for x in re.findall(r"Slow 1100mV [-\d]+C Model Fmax Summary \| ([\d.]+) MHz", t)]
    crit = int(re.search(r"Critical warnings: (\d+)", t).group(1))
    return dict(alm=alm, regs=regs, membits=m10k, dsp=dsp, setup=setup, hold=hold, fmax=min(fm), crit=crit, file=f.name)


def main():
    cyc_dir = Path(sys.argv[1])
    date = sys.argv[2] if len(sys.argv) > 2 else "2026-10-03"
    rows = [(rev, seed, parse(rev)) for rev, seed in REVS]
    out = ["## Per seed at 40.000 ns (MEASURED)", "| Seed | ALM | Registers | Block memory bits | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Critical warnings | Evidence |", "|---|---|---|---|---|---|---|---|---|---|"]
    for rev, seed, r in rows:
        met = "yes" if r["setup"] >= 0 and r["hold"] >= 0 else "**NO**"
        out.append(f"| {seed} | {r['alm']:,} | {r['regs']} | {r['membits']} | {r['dsp']} | {r['setup']:.3f} / {r['hold']:.3f} | {met} | {r['fmax']:.2f} | {r['crit']} | `{r['file']}` |")
    alms, fms = [r["alm"] for _, _, r in rows], [r["fmax"] for _, _, r in rows]
    out.append("")
    out.append(f"ALM median (min-max): {statistics.median(alms):,.1f} ({min(alms):,}-{max(alms):,}); registers {min(r['regs'] for _, _, r in rows)}-{max(r['regs'] for _, _, r in rows)}; DSP {min(r['dsp'] for _, _, r in rows)}-{max(r['dsp'] for _, _, r in rows)}; "
               f"Fmax median (min-max): {statistics.median(fms):.3f} ({min(fms):.2f}-{max(fms):.2f}) MHz")
    out.append("")
    out.append("### Pass rule (test plan section 5, items 2 and 3)")
    fit_ok = all(r["alm"] > 0 for _, _, r in rows)
    met_all = all(r["setup"] >= 0 and r["hold"] >= 0 for _, _, r in rows)
    out.append(f"- {'PASS' if fit_ok else 'FAIL'}: the fit succeeded at every seed")
    out.append(f"- {'PASS' if met_all else 'FAIL'}: timing met at 40.000 ns at every seed (worst setup and hold slack of all corners non-negative)")
    out.append("- reported as MEASURED: resource counts and Fmax (median of the lowest slow-corner Fmax over seeds 1-6) above; DSP is reported and not limited")
    r20 = parse("CD-20")
    out.append("")
    out.append(f"- information CD-20 (20.000 ns), seed 1: ALM {r20['alm']:,}, worst setup {r20['setup']:.3f} ns ({'met' if r20['setup'] >= 0 and r20['hold'] >= 0 else 'NOT met'}), Fmax lowest slow corner {r20['fmax']:.2f} MHz, `{r20['file']}`")
    cyc = {}
    for f in sorted(cyc_dir.glob("cycles_*_*.json")):
        d = json.loads(f.read_text())
        for k, v in d.items():
            cyc.setdefault(k, {})[f.stem.split("_")[1]] = v
    out.append("")
    out.append("## Cycles per polynomial (MEASURED in simulation, always-ready sink, no input gaps; identical for every data value of one d: test V7)")
    out.append("| d | pack, Icarus | pack, Verilator | unpack, Icarus | unpack, Verilator |")
    out.append("|---|---|---|---|---|")
    for d in ("1", "4", "10", "12"):
        out.append(f"| {d} | {cyc['pack_cycles']['icarus'][d]} | {cyc['pack_cycles']['verilator'][d]} | {cyc['unpack_cycles']['icarus'][d]} | {cyc['unpack_cycles']['verilator'][d]} |")
    (EV / f"selection_worksheet.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))
    return 0 if fit_ok and met_all else 1


if __name__ == "__main__":
    sys.exit(main())
