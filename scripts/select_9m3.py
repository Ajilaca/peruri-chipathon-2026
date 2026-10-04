#!/usr/bin/env python3
"""scripts/select_9m3.py -- Phase 9M item 3 worksheet (docs/evidence/phase09m-optimisation/9m3/test_plan_9m3.md sections 4 and 5): reads the Quartus evidence files of MW (9M-1 core, C5 hash, 9m1) and MK (same with the K0 hash, 9m3)
and writes docs/evidence/phase09m-optimisation/9m3/selection_worksheet_<date>.md. Every value is copied from an evidence file; t = cycles / Fmax is perhitungan tim.
Usage: python3 scripts/select_9m3.py [date YYYY-MM-DD]
"""
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
E9M = ROOT / "docs" / "evidence" / "phase09m-optimisation"
E1, E3 = E9M / "9m1", E9M / "9m3"
CYC = {"MW": (8327, 10159, 15515), "MK": (8447, 10279, 15635)}      # profile inputs: 9m1/profile_w2_verilator_2026-10-04.json and 9m3/profile_k0_w2_verilator_2026-10-04.json
CONF = {"MW": ("9M-1 core, C5 hash (`HASH_C5 = 1`, `CODEC_W2 = 1`)", E1, ["MW"] + [f"MW-s{s}" for s in range(2, 7)], "MW-20"),
        "MK": ("9M-1 core, K0 hash (`HASH_C5 = 0`, `CODEC_W2 = 1`)", E3, ["MK"] + [f"MK-s{s}" for s in range(2, 7)], "MK-20")}


def num(s):
    return float(s.replace(",", ""))


def parse(ev, rev):
    f = sorted(ev.glob(f"quartus_{rev}-2026*.md"))[-1]
    t = f.read_text()
    g = lambda pat: int(num(re.search(pat, t).group(1)))  # noqa: E731
    fm = [num(x) for x in re.findall(r"Slow 1100mV [-\d]+C Model Fmax Summary \| ([\d.]+) MHz", t)]
    return dict(alm=g(r"Logic utilization \(in ALMs\) \| ([\d,]+)"), regs=g(r"Total registers \| ([\d,]+)"), dsp=g(r"Total DSP Blocks \| ([\d,]+)"), m10k=g(r"Total RAM Blocks \| ([\d,]+)"),
                setup=num(re.search(r"Worst setup slack: \*\*(-?[\d.]+) ns", t).group(1)), hold=num(re.search(r"Worst hold slack: \*\*(-?[\d.]+) ns", t).group(1)), fmax=min(fm), crit=g(r"Critical warnings: (\d+)"), file=f.relative_to(ROOT))


def main():
    date = sys.argv[1] if len(sys.argv) > 1 else "2026-10-04"
    out, st = [], {}
    for key, (label, ev, revs, rev20) in CONF.items():
        rows = [(rev, parse(ev, rev)) for rev in revs]
        out += [f"## {label} at 40.000 ns, seeds 1-6 (MEASURED, kernel-only, virtual pins)",
                "| Revision | ALM | Registers | RAM blocks | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Critical warnings | Evidence |", "|---|---|---|---|---|---|---|---|---|---|"]
        for rev, r in rows:
            met = r["setup"] >= 0 and r["hold"] >= 0
            out.append(f"| {rev} | {r['alm']:,} | {r['regs']} | {r['m10k']} | {r['dsp']} | {r['setup']:.3f} / {r['hold']:.3f} | {'yes' if met else '**NO**'} | {r['fmax']:.2f} | {r['crit']} | `{r['file']}` |")
        alms, fms = [r["alm"] for _, r in rows], [r["fmax"] for _, r in rows]
        nmet = sum(1 for _, r in rows if r["setup"] >= 0 and r["hold"] >= 0)
        fmed = statistics.median(fms)
        out += ["", f"ALM median (min-max) {statistics.median(alms):,.1f} ({min(alms):,}-{max(alms):,}); registers {min(r['regs'] for _, r in rows)}-{max(r['regs'] for _, r in rows)}; RAM blocks {min(r['m10k'] for _, r in rows)}-{max(r['m10k'] for _, r in rows)}; DSP {min(r['dsp'] for _, r in rows)}-{max(r['dsp'] for _, r in rows)}",
                f"Worst setup slack over seeds {min(r['setup'] for _, r in rows):.3f} ns; Fmax lowest slow corner median (min-max) {fmed:.3f} ({min(fms):.2f}-{max(fms):.2f}) MHz", f"**Timing met at 40.000 ns at {nmet} of 6 seeds**", ""]
        c = CYC[key]
        out += ["Latency at the median Fmax of this table (perhitungan tim; profile-input cycles):", f"KeyGen {c[0]:,} cycles = {c[0] / fmed:.1f} us; Encaps {c[1]:,} = {c[1] / fmed:.1f} us; Decaps {c[2]:,} = {c[2] / fmed:.1f} us", ""]
        r20 = parse(ev if key == "MK" else E9M / "9m1", rev20)
        out += [f"Information, {rev20} (seed 1, 20.000 ns): ALM {r20['alm']:,}; worst setup / hold {r20['setup']:.3f} / {r20['hold']:.3f} ns; Fmax lowest slow corner {r20['fmax']:.2f} MHz; `{r20['file']}`", ""]
        st[key] = dict(alm=statistics.median(alms), fmax=fmed, nmet=nmet)
    w, k = st["MW"], st["MK"]
    lat = [(CYC["MK"][i] / k["fmax"]) / (CYC["MW"][i] / w["fmax"]) - 1 for i in range(3)]
    r2, r3, r4 = k["nmet"] == 6, w["alm"] - k["alm"] >= 1500, all(x <= 0.02 for x in lat)
    out += ["### Rule (test plan section 5), items 2-4 (items 1 = tests, see result_9m3.md)",
            f"- 2. timing met at 40.000 ns at every seed: {'met' if r2 else 'NOT met'} ({k['nmet']} of 6)",
            f"- 3. ALM median MW - MK = {w['alm'] - k['alm']:,.1f} (needs >= 1,500): {'met' if r3 else 'NOT met'}",
            f"- 4. latency of MK relative to MW (cycles / median Fmax): KeyGen {lat[0] * 100:+.2f} %, Encaps {lat[1] * 100:+.2f} %, Decaps {lat[2] * 100:+.2f} % (needs <= +2 % each): {'met' if r4 else 'NOT met'}"]
    (E3 / f"selection_worksheet_{date}.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
