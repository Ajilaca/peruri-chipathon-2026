#!/usr/bin/env python3
"""scripts/quartus/select_9c.py -- Phase 9c worksheet (evidence/phase09/9c/test_plan_9c.md section 5): reads the Quartus evidence files of the revisions MC, MC-s2 .. MC-s6 and MC-20 and the cycle tables of the simulations,
writes evidence/phase09/9c/selection_worksheet_<date>.md. Nothing is computed from slack: every value is copied from the evidence file.
Usage: python3 scripts/quartus/select_9c.py <cycles_dir> [date YYYY-MM-DD]
"""
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EV = ROOT / "evidence" / "phase09" / "9c"
REVS = [("MC", 1), ("MC-s2", 2), ("MC-s3", 3), ("MC-s4", 4), ("MC-s5", 5), ("MC-s6", 6)]


def num(s):
    return float(s.replace(",", ""))


def parse(rev):
    f = sorted(EV.glob(f"quartus_{rev}.md"))[-1]
    t = f.read_text()
    g = lambda pat: int(num(re.search(pat, t).group(1)))  # noqa: E731
    fm = [num(x) for x in re.findall(r"Slow 1100mV [-\d]+C Model Fmax Summary \| ([\d.]+) MHz", t)]
    return dict(alm=g(r"Logic utilization \(in ALMs\) \| ([\d,]+)"), regs=g(r"Total registers \| ([\d,]+)"), membits=g(r"Total block memory bits \| ([\d,]+)"), dsp=g(r"Total DSP Blocks \| ([\d,]+)"),
                m10k=g(r"Total RAM Blocks \| ([\d,]+)"),
                setup=num(re.search(r"Slack setup terburuk: \*\*(-?[\d.]+) ns", t).group(1)), hold=num(re.search(r"Slack hold terburuk: \*\*(-?[\d.]+) ns", t).group(1)), fmax=min(fm),
                crit=g(r"Peringatan kritis: (\d+)"), file=f.name)


def main():
    cyc_dir = Path(sys.argv[1])
    date = sys.argv[2] if len(sys.argv) > 2 else "2026-10-03"
    rows = [(rev, seed, parse(rev)) for rev, seed in REVS]
    out = ["## Per seed at 40.000 ns (MEASURED)", "| Seed | ALM | Registers | M10K blocks | Block memory bits | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Critical warnings | Evidence |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for rev, seed, r in rows:
        met = "yes" if r["setup"] >= 0 and r["hold"] >= 0 else "**NO**"
        out.append(f"| {seed} | {r['alm']:,} | {r['regs']} | {r['m10k']} | {r['membits']:,} | {r['dsp']} | {r['setup']:.3f} / {r['hold']:.3f} | {met} | {r['fmax']:.2f} | {r['crit']} | `{r['file']}` |")
    alms, fms = [r["alm"] for _, _, r in rows], [r["fmax"] for _, _, r in rows]
    out.append("")
    out.append(f"ALM median (min-max): {statistics.median(alms):,.1f} ({min(alms):,}-{max(alms):,}); registers {min(r['regs'] for _, _, r in rows)}-{max(r['regs'] for _, _, r in rows)}; M10K {min(r['m10k'] for _, _, r in rows)}-{max(r['m10k'] for _, _, r in rows)}; "
               f"DSP {min(r['dsp'] for _, _, r in rows)}-{max(r['dsp'] for _, _, r in rows)}; Fmax median (min-max): {statistics.median(fms):.3f} ({min(fms):.2f}-{max(fms):.2f}) MHz")
    fit_ok = all(r["alm"] > 0 for _, _, r in rows)
    met_all = all(r["setup"] >= 0 and r["hold"] >= 0 for _, _, r in rows)
    out += ["", "### Pass rule (test plan section 5, items 2 and 3)",
            f"- {'PASS' if fit_ok else 'FAIL'}: the fit succeeded at every seed",
            f"- {'PASS' if met_all else 'FAIL'}: timing met at 40.000 ns at every seed (worst setup and hold slack of all corners non-negative)",
            "- reported as MEASURED: resource counts and Fmax (median of the lowest slow-corner Fmax over seeds 1-6) above"]
    r = parse("MC-20")
    out.append(f"- information MC-20 (20.000 ns), seed 1: ALM {r['alm']:,}, registers {r['regs']}, worst setup {r['setup']:.3f} ns ({'met' if r['setup'] >= 0 and r['hold'] >= 0 else 'NOT met'}), Fmax lowest slow corner {r['fmax']:.2f} MHz, `{r['file']}`")
    cyc = {}
    for f in sorted(cyc_dir.glob("cycles_*_core.json")):
        cyc[f.stem.split("_")[1]] = json.loads(f.read_text())
    out += ["", "## Cycles per operation (MEASURED in simulation; no host stalls; one operation from start_i to done_o as seen by the test driver)",
            "| Operation | Icarus | Verilator |", "|---|---|---|"]
    for sim_key in ("icarus", "verilator"):
        assert sim_key in cyc, sim_key
    out.append(f"| Encaps (constant for every m with the same ek) | {cyc['icarus']['encaps']} | {cyc['verilator']['encaps']} |")
    out.append(f"| Decaps (constant for valid and rejected ciphertexts and for different secret keys with the same ek) | {cyc['icarus']['decaps']} | {cyc['verilator']['decaps']} |")
    out.append(f"| KeyGen over the {cyc['icarus']['keygen_n']} ACVP seeds (depends on the public rho only), min - max | {cyc['icarus']['keygen_min']} - {cyc['icarus']['keygen_max']} | {cyc['verilator']['keygen_min']} - {cyc['verilator']['keygen_max']} |")
    out.append(f"| Encaps over the ACVP vectors (different ek), min - max | {cyc['icarus']['encaps_acvp_min']} - {cyc['icarus']['encaps_acvp_max']} | {cyc['verilator']['encaps_acvp_min']} - {cyc['verilator']['encaps_acvp_max']} |")
    out.append(f"| Decaps over the ACVP vectors (different dk), min - max | {cyc['icarus']['decaps_acvp_min']} - {cyc['icarus']['decaps_acvp_max']} | {cyc['verilator']['decaps_acvp_min']} - {cyc['verilator']['decaps_acvp_max']} |")
    (EV / f"selection_worksheet.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))
    return 0 if fit_ok and met_all else 1


if __name__ == "__main__":
    sys.exit(main())
