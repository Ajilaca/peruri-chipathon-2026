#!/usr/bin/env python3
"""scripts/quartus/select_9m2.py -- Phase 9M item 2 worksheet (evidence/phase9m/batch1/9m2/test_plan_9m2.md sections 4 and 5): reads the Quartus evidence files of the 20.000 ns revisions of the Phase 9 core (MC-20 from 9c, MC-20-s2 .. s6)
and of the 9M-1 core (MW-20 from 9m1, MW-20-s2 .. s6), and writes evidence/phase9m/batch1/9m2/selection_worksheet_<date>.md. Every value is copied from an evidence file; t = cycles / Fmax is perhitungan tim.
Usage: python3 scripts/quartus/select_9m2.py [date YYYY-MM-DD]
"""
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
E9C = ROOT / "evidence" / "phase09" / "9c"
E9M = ROOT / "evidence" / "phase9m"
E1, E2 = E9M / "batch1" / "9m1", E9M / "batch1" / "9m2"
CYC = {"MC": (9095, 10735, 16667), "MW": (8327, 10159, 15515)}      # profile inputs, ../profile_verilator.json and batch1/9m1/profile_w2_verilator.json
CONF = {"MC": ("Phase 9 core (`CODEC_W2 = 0`)", [("MC-20", E9C, 1)] + [(f"MC-20-s{s}", E2, s) for s in range(2, 7)]),
        "MW": ("9M-1 core (`CODEC_W2 = 1`)", [("MW-20", E1, 1)] + [(f"MW-20-s{s}", E2, s) for s in range(2, 7)])}


def num(s):
    return float(s.replace(",", ""))


def parse(ev, rev):
    f = sorted(ev.glob(f"quartus_{rev}.md"))[-1]
    t = f.read_text()
    g = lambda pat: int(num(re.search(pat, t).group(1)))  # noqa: E731
    fm = [num(x) for x in re.findall(r"Slow 1100mV [-\d]+C Model Fmax Summary \| ([\d.]+) MHz", t)]
    return dict(alm=g(r"Logic utilization \(in ALMs\) \| ([\d,]+)"), regs=g(r"Total registers \| ([\d,]+)"), dsp=g(r"Total DSP Blocks \| ([\d,]+)"), m10k=g(r"Total RAM Blocks \| ([\d,]+)"),
                setup=num(re.search(r"Slack setup terburuk: \*\*(-?[\d.]+) ns", t).group(1)), hold=num(re.search(r"Slack hold terburuk: \*\*(-?[\d.]+) ns", t).group(1)), fmax=min(fm), crit=g(r"Peringatan kritis: (\d+)"), file=f.relative_to(ROOT))


def main():
    date = sys.argv[1] if len(sys.argv) > 1 else "2026-10-04"
    out, ok_all = [], True
    for key, (label, revs) in CONF.items():
        rows = [(rev, seed, parse(ev, rev)) for rev, ev, seed in revs]
        out += [f"## {label} at 20.000 ns (MEASURED, kernel-only, virtual pins)",
                "| Seed | ALM | Registers | RAM blocks | DSP | Worst setup / hold (ns) | Timing met @ 20 ns | Fmax lowest slow corner (MHz) | Critical warnings | Evidence |", "|---|---|---|---|---|---|---|---|---|---|"]
        for rev, seed, r in rows:
            met = r["setup"] >= 0 and r["hold"] >= 0
            out.append(f"| {seed} | {r['alm']:,} | {r['regs']} | {r['m10k']} | {r['dsp']} | {r['setup']:.3f} / {r['hold']:.3f} | {'yes' if met else '**NO**'} | {r['fmax']:.2f} | {r['crit']} | `{r['file']}` |")
        alms, fms = [r["alm"] for _, _, r in rows], [r["fmax"] for _, _, r in rows]
        nmet = sum(1 for _, _, r in rows if r["setup"] >= 0 and r["hold"] >= 0)
        failing = [str(s) for _, s, r in rows if not (r["setup"] >= 0 and r["hold"] >= 0)]
        fmed = statistics.median(fms)
        out += ["", f"ALM median (min-max) {statistics.median(alms):,.1f} ({min(alms):,}-{max(alms):,}); registers {min(r['regs'] for _, _, r in rows)}-{max(r['regs'] for _, _, r in rows)}; RAM blocks {min(r['m10k'] for _, _, r in rows)}-{max(r['m10k'] for _, _, r in rows)}; DSP {min(r['dsp'] for _, _, r in rows)}-{max(r['dsp'] for _, _, r in rows)}",
                f"Worst setup slack over seeds {min(r['setup'] for _, _, r in rows):.3f} ns; Fmax lowest slow corner median (min-max) {fmed:.3f} ({min(fms):.2f}-{max(fms):.2f}) MHz",
                f"**Timing met at 20.000 ns at {nmet} of 6 seeds**" + (f" (failing seeds: {', '.join(failing)})" if failing else ""), ""]
        c = CYC[key]
        out += ["Latency at the median Fmax of this table (perhitungan tim; profile-input cycles; kernel-only static timing, not a board measurement):",
                f"KeyGen {c[0]:,} cycles = {c[0] / fmed:.1f} us; Encaps {c[1]:,} = {c[1] / fmed:.1f} us; Decaps {c[2]:,} = {c[2] / fmed:.1f} us", ""]
        ok_all &= nmet == 6
    out += ["### Rule (test plan section 5)", f"- {'met' if ok_all else 'NOT met'}: the statement 'timing met at 20.000 ns' holds for a configuration only if all six seeds meet it; see the line 'Timing met at 20.000 ns at k of 6 seeds' of each table"]
    (E2 / f"selection_worksheet.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
