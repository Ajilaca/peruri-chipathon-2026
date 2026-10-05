#!/usr/bin/env python3
"""scripts/quartus/select_9b.py -- Phase 9b worksheet (evidence/phase09/9b/test_plan_9b.md section 5): reads the Quartus evidence files of the revisions HF, HF-s2 .. HF-s6, HF-20 and HF-K0 and the cycle tables of the
simulations, writes evidence/phase09/9b/selection_worksheet_<date>.md. Nothing is computed from slack: every value is copied from the evidence file.
Usage: python3 scripts/quartus/select_9b.py <cycles_dir> [date YYYY-MM-DD]
"""
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EV = ROOT / "evidence" / "phase09" / "9b"
REVS = [("HF", 1), ("HF-s2", 2), ("HF-s3", 3), ("HF-s4", 4), ("HF-s5", 5), ("HF-s6", 6)]


def num(s):
    return float(s.replace(",", ""))


def parse(rev):
    f = EV / f"quartus_{rev}.md"
    t = f.read_text()
    g = lambda pat: int(num(re.search(pat, t).group(1)))  # noqa: E731
    fm = [num(x) for x in re.findall(r"Slow 1100mV [-\d]+C Model Fmax Summary \| ([\d.]+) MHz", t)]
    return dict(alm=g(r"Logic utilization \(in ALMs\) \| ([\d,]+)"), regs=g(r"Total registers \| ([\d,]+)"), membits=g(r"Total block memory bits \| ([\d,]+)"), dsp=g(r"Total DSP Blocks \| ([\d,]+)"),
                setup=num(re.search(r"Worst setup slack: \*\*(-?[\d.]+) ns", t).group(1)), hold=num(re.search(r"Worst hold slack: \*\*(-?[\d.]+) ns", t).group(1)), fmax=min(fm),
                crit=g(r"Critical warnings: (\d+)"), file=f.name)


def main():
    cyc_dir = Path(sys.argv[1])
    date = sys.argv[2] if len(sys.argv) > 2 else "2026-10-03"
    rows = [(rev, seed, parse(rev)) for rev, seed in REVS]
    out = ["## Per seed at 40.000 ns, C5 sponge (MEASURED)", "| Seed | ALM | Registers | Block memory bits | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Critical warnings | Evidence |", "|---|---|---|---|---|---|---|---|---|---|"]
    for rev, seed, r in rows:
        met = "yes" if r["setup"] >= 0 and r["hold"] >= 0 else "**NO**"
        out.append(f"| {seed} | {r['alm']:,} | {r['regs']} | {r['membits']} | {r['dsp']} | {r['setup']:.3f} / {r['hold']:.3f} | {met} | {r['fmax']:.2f} | {r['crit']} | `{r['file']}` |")
    alms, fms = [r["alm"] for _, _, r in rows], [r["fmax"] for _, _, r in rows]
    out.append("")
    out.append(f"ALM median (min-max): {statistics.median(alms):,.1f} ({min(alms):,}-{max(alms):,}); registers {min(r['regs'] for _, _, r in rows)}-{max(r['regs'] for _, _, r in rows)}; DSP {min(r['dsp'] for _, _, r in rows)}-{max(r['dsp'] for _, _, r in rows)}; "
               f"Fmax median (min-max): {statistics.median(fms):.3f} ({min(fms):.2f}-{max(fms):.2f}) MHz")
    fit_ok = all(r["alm"] > 0 for _, _, r in rows)
    met_all = all(r["setup"] >= 0 and r["hold"] >= 0 for _, _, r in rows)
    out += ["", "### Pass rule (test plan section 5, items 2 and 3)",
            f"- {'PASS' if fit_ok else 'FAIL'}: the fit succeeded at every seed",
            f"- {'PASS' if met_all else 'FAIL'}: timing met at 40.000 ns at every seed (worst setup and hold slack of all corners non-negative)",
            "- reported as MEASURED: resource counts and Fmax (median of the lowest slow-corner Fmax over seeds 1-6) above; no alternative is chosen in this block"]
    for rev, what in (("HF-20", "20.000 ns, C5 sponge"), ("HF-K0", "40.000 ns, K0 sponge (the second hash instance with the smaller core)")):
        r = parse(rev)
        out.append(f"- information {rev} ({what}), seed 1: ALM {r['alm']:,}, registers {r['regs']}, worst setup {r['setup']:.3f} ns ({'met' if r['setup'] >= 0 and r['hold'] >= 0 else 'NOT met'}), Fmax lowest slow corner {r['fmax']:.2f} MHz, `{r['file']}`")
    cyc = {}
    for f in sorted(cyc_dir.glob("cycles_*_*.json")):
        sim, name = f.stem.split("_")[1], f.stem.split("_")[2]
        cyc.setdefault(name, {})[sim] = json.loads(f.read_text())
    out += ["", "## Cycles (MEASURED in simulation, always-ready sink, no input gaps; identical for every data value of one operation: test V6)",
            "| Operation | C5 sponge, Icarus | C5 sponge, Verilator | K0 sponge, Icarus | K0 sponge, Verilator |", "|---|---|---|---|---|"]
    for op in ("G_33", "G_64", "H_1184", "J_1120"):
        out.append(f"| {op.replace('_', ' of ')} bytes | " + " | ".join(str(cyc[n][s]["hash_cycles"][op]) for n in ("hash1", "hash0") for s in ("icarus", "verilator")) + " |")
    out.append(f"| compare of 1,088 bytes (136 beats) | {cyc['fo']['icarus']['fo_cycles']} | {cyc['fo']['verilator']['fo_cycles']} | - | - |")
    (EV / f"selection_worksheet.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))
    return 0 if fit_ok and met_all else 1


if __name__ == "__main__":
    sys.exit(main())
