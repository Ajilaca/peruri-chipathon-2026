#!/usr/bin/env python3
"""scripts/quartus/phase5_select_5b.py

Applies the 5b selection rule of ADR 0011 (D8) to the measured Barrett / Montgomery candidates, reading every value
from files, never from memory:

  - evidence/phase05/5b/quartus_C4b-<B|M>[-s<n>]_<date>.md (written by extract_quartus_report.py; seed 1
    is the revision without suffix): ALM ("Logic utilization (in ALMs)"), worst setup / hold slack over all corners,
    the slow-corner rows of the Fmax Summary panels;
  - evidence/phase05/5b/verification_status.json: per candidate, correct PASS/FAIL (test plan section 7
    incl. exhaustive and negative controls, both simulators) and the measured NTT / INTT cycles.

Rule (ADR 0011):
  qualifies at a seed = correct PASS and cycles exactly 119 / 375 and ALM <= 12,573 and timing met at 40.000 ns
                        (worst setup >= 0 and worst hold >= 0)
  qualifier           = qualifies at every seed 1..6
  Fmax(c)             = median over seeds of the lowest slow-corner Fmax (MHz, as printed)
  winner              = higher Fmax, unless the other qualifier is within 5 % (near tie): then lower median ALM;
                        if the median ALM also differ by < 32 ALM: no automatic choice, the team decides
  no qualifier        -> nothing is selected; the team decides.

Usage: python3 scripts/quartus/phase5_select_5b.py [--date YYYYMMDD]      (prints a Markdown worksheet)
"""
import argparse
import json
import pathlib
import re
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
EVID = ROOT / "evidence" / "phase05" / "5b"
ALM_BUDGET = 12573          # ADR 0009 / ADR 0011 D2
NEAR_TIE = 0.05             # ADR 0011 D8
ALM_TIE = 32                # C3-P6 seed spread, evidence/phase04/seed_sweep.md
CYCLES = (119, 375)         # ADR 0011 D5
SEEDS = range(1, 7)
CANDS = {"B": "Barrett", "M": "Montgomery"}


def parse_quartus(path: pathlib.Path) -> dict:
    s = path.read_text()
    alm = re.search(r"\| Logic utilization \(in ALMs\) \| ([\d,]+) / ([\d,]+)", s)
    reg = re.search(r"\| Total registers \| (\d+)", s)
    dsp = re.search(r"\| Total DSP Blocks \| (\d+) / (\d+)", s)
    ram = re.search(r"\| Total RAM Blocks \| (\d+) / (\d+)", s)
    setup = re.search(r"Slack setup terburuk: \*\*(-?[\d.]+) ns\*\*", s)
    hold = re.search(r"Slack hold terburuk: \*\*(-?[\d.]+) ns\*\*", s)
    fmax = re.findall(r"\| (Slow [^|]*?) Model Fmax Summary \| ([\d.]+) MHz \|", s)
    if not (alm and reg and dsp and ram and setup and hold and fmax):
        raise SystemExit(f"{path}: could not read every field; fix the parser or the evidence file")
    return {"alm": int(alm.group(1).replace(",", "")), "reg": int(reg.group(1)),
            "dsp": int(dsp.group(1)), "ram": int(ram.group(1)),
            "setup": float(setup.group(1)), "hold": float(hold.group(1)),
            "fmax": min(float(v) for _, v in fmax), "file": path.name}


def find(rev: str, date: str | None) -> pathlib.Path:
    files = sorted(EVID.glob(f"quartus_{rev}.md"))
    if not files:
        raise SystemExit(f"no evidence file for {rev} in {EVID}")
    return files[-1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=None)
    args = ap.parse_args()
    status = json.loads((EVID / "verification_status.json").read_text())
    rows, summary = [], {}
    for c, name in CANDS.items():
        st = status[c]
        correct = st["correct"] == "PASS"
        cyc_ok = (st["cycles_NTT"], st["cycles_INTT"]) == CYCLES
        per = []
        for s in SEEDS:
            rev = f"C4b-{c}" + ("" if s == 1 else f"-s{s}")
            q = parse_quartus(find(rev, args.date))
            q["seed"] = s
            q["timing"] = q["setup"] >= 0 and q["hold"] >= 0
            q["qual"] = correct and cyc_ok and q["alm"] <= ALM_BUDGET and q["timing"]
            per.append(q)
            rows.append((name, q))
        summary[c] = {
            "qualifier": all(q["qual"] for q in per),
            "fmax_med": statistics.median(q["fmax"] for q in per),
            "alm_med": statistics.median(q["alm"] for q in per),
            "fmax_rng": (min(q["fmax"] for q in per), max(q["fmax"] for q in per)),
            "alm_rng": (min(q["alm"] for q in per), max(q["alm"] for q in per)),
            "correct": st["correct"], "cycles": (st["cycles_NTT"], st["cycles_INTT"]), "evidence": st["evidence"],
        }

    print("## Per seed (MEASURED; qualification per ADR 0011 D8)")
    print("| Candidate | Seed | ALM | Registers | M10K | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | "
          "Fmax lowest slow corner (MHz) | t_NTT (us) | Qualifies | Evidence |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for name, q in rows:
        c = "B" if name == "Barrett" else "M"
        t = summary[c]["cycles"][0] / q["fmax"]
        print(f"| {name} | {q['seed']} | {q['alm']:,} | {q['reg']} | {q['ram']} | {q['dsp']} | "
              f"{q['setup']:.3f} / {q['hold']:.3f} | {'yes' if q['timing'] else 'no'} | {q['fmax']:.2f} | {t:.3f} | "
              f"{'yes' if q['qual'] else 'no'} | `{q['file']}` |")
    print()
    print("## Per candidate (medians over seeds 1-6; INFERENCE from the rows above)")
    print("| Candidate | Correct | Cycles NTT / INTT | Qualifier (all seeds) | ALM median (min-max) | "
          "Fmax median (min-max) MHz | t_NTT at median Fmax (us) |")
    print("|---|---|---|---|---|---|---|")
    for c, name in CANDS.items():
        s = summary[c]
        print(f"| {name} | {s['correct']} | {s['cycles'][0]} / {s['cycles'][1]} | {'yes' if s['qualifier'] else 'no'} | "
              f"{s['alm_med']:,.1f} ({s['alm_rng'][0]:,}-{s['alm_rng'][1]:,}) | {s['fmax_med']:.3f} "
              f"({s['fmax_rng'][0]:.2f}-{s['fmax_rng'][1]:.2f}) | {s['cycles'][0] / s['fmax_med']:.3f} |")
    print()
    quals = [c for c in CANDS if summary[c]["qualifier"]]
    print("## Rule result")
    if not quals:
        print("No candidate qualifies at every seed: nothing is selected; the team decides (ADR 0011 D8 step 5).")
        return 0
    if len(quals) == 1:
        print(f"Only {CANDS[quals[0]]} qualifies: **{CANDS[quals[0]]}** (ADR 0011 D8).")
        return 0
    hi = max(quals, key=lambda c: summary[c]["fmax_med"])
    lo = [c for c in quals if c != hi][0]
    d = (summary[hi]["fmax_med"] - summary[lo]["fmax_med"]) / summary[hi]["fmax_med"]
    print(f"Higher median Fmax: {CANDS[hi]} ({summary[hi]['fmax_med']:.3f} MHz); {CANDS[lo]} is {100 * d:.2f} % lower.")
    if d > NEAR_TIE:
        print(f"Not a near tie (> 5 %): **{CANDS[hi]}** is selected by the rule.")
        return 0
    da = summary[hi]["alm_med"] - summary[lo]["alm_med"]
    print(f"Near tie (<= 5 %). Median ALM: {CANDS[hi]} {summary[hi]['alm_med']:,.1f}, "
          f"{CANDS[lo]} {summary[lo]['alm_med']:,.1f} (difference {abs(da):,.1f}).")
    if abs(da) < ALM_TIE:
        print(f"ALM medians differ by less than {ALM_TIE}: **no automatic choice; the team decides** "
              "(suggested tie-break in ADR 0011: Barrett).")
    else:
        win = hi if da < 0 else lo
        print(f"Lower median ALM wins: **{CANDS[win]}** is selected by the rule.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
