#!/usr/bin/env python3
"""scripts/phase4_select_p.py

Applies the ADR 0007 selection rule (docs/evidence/phase04-pipeline/test_plan.md section 6) to the
Phase 4 sweep, reading every value from files, never from memory:

  - docs/evidence/phase04-pipeline/quartus_C3-P<n>_<date>.md  (written by extract_quartus_report.py):
    ALM ("Logic utilization (in ALMs)"), worst setup / hold slack, the slow-corner rows of the Fmax
    Summary panels;
  - docs/evidence/phase04-pipeline/verification_status.json: per P, bit-exact PASS/FAIL, constant-cycle
    PASS/FAIL and the measured cycle counts, each with the evidence file it was taken from.

Rule:
  candidate(P)  = bit-exact PASS and constant-cycle PASS and ALM <= 10,478 and timing met at 40.000 ns
                  (worst setup slack >= 0 and worst hold slack >= 0 over all corners reported)
  Fmax(P)       = lowest Fmax among the slow-corner Fmax Summary rows, as printed (MHz)
  t_NTT(P)      = cycles_NTT(P) / Fmax(P)  [us];  t_INTT(P) likewise (reported, does not drive selection)
  t_min         = min over candidates of t_NTT;  d(P) = (t_NTT(P) - t_min) / t_min
  P_selected    = smallest candidate P with d(P) <= 0.05
  no candidate  -> nothing is selected; the team decides.

Usage: python3 scripts/phase4_select_p.py [--date YYYYMMDD]      (prints a Markdown worksheet)
"""
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
EVID = ROOT / "docs" / "evidence" / "phase04-pipeline"
ALM_BUDGET = 10478          # ADR 0004 (historical default: reproduces selection_worksheet_2026-09-30.md);
                            # ADR 0009 (2026-10-01) uses 12,573 for the NTT core: run with --alm-budget 12573
NEAR_TIE = 0.05             # ADR 0007
P_VALUES = (0, 2, 4, 6)


def parse_quartus(path: pathlib.Path) -> dict:
    s = path.read_text()
    alm = re.search(r"\| Logic utilization \(in ALMs\) \| ([\d,]+) / ([\d,]+)", s)
    reg = re.search(r"\| Total registers \| (\d+)", s)
    dsp = re.search(r"\| Total DSP Blocks \| (\d+) / (\d+)", s)
    ram = re.search(r"\| Total RAM Blocks \| (\d+) / (\d+)", s)
    setup = re.search(r"Worst setup slack: \*\*(-?[\d.]+) ns\*\* \(([^)]*)\)", s)
    hold = re.search(r"Worst hold slack: \*\*(-?[\d.]+) ns\*\* \(([^)]*)\)", s)
    fmax = re.findall(r"\| (Slow [^|]*?) Model Fmax Summary \| ([\d.]+) MHz \|", s)
    if not (alm and reg and dsp and ram and setup and hold and fmax):
        raise SystemExit(f"{path}: could not read every field; fix the parser or the evidence file")
    return {
        "alm": int(alm.group(1).replace(",", "")), "alm_den": alm.group(2),
        "reg": int(reg.group(1)), "dsp": f"{dsp.group(1)} / {dsp.group(2)}", "ram": f"{ram.group(1)} / {ram.group(2)}",
        "setup": float(setup.group(1)), "setup_corner": setup.group(2),
        "hold": float(hold.group(1)), "hold_corner": hold.group(2),
        "fmax": [(c, float(v)) for c, v in fmax],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=None, help="UTC date suffix of the evidence files (default: newest)")
    ap.add_argument("--alm-budget", type=int, default=ALM_BUDGET,
                    help="ALM limit of candidate condition 3 (default 10478 = ADR 0004; ADR 0009: 12573)")
    args = ap.parse_args()
    budget = args.alm_budget

    status = json.loads((EVID / "verification_status.json").read_text())
    rows = {}
    for p in P_VALUES:
        files = sorted(EVID.glob(f"quartus_C3-P{p}_{args.date or '*'}.md"))
        if not files:
            raise SystemExit(f"no Quartus evidence for P={p}: the rule is applied only after all four P are measured")
        q = parse_quartus(files[-1])
        v = status[str(p)]
        q.update(file=files[-1].name, bit_exact=v["bit_exact"], const=v["constant_cycle"],
                 cyc_ntt=int(v["cycles_NTT"]), cyc_intt=int(v["cycles_INTT"]))
        q["fmax_low"] = min(f for _, f in q["fmax"])
        q["t_ntt"] = q["cyc_ntt"] / q["fmax_low"]
        q["t_intt"] = q["cyc_intt"] / q["fmax_low"]
        q["alm_ok"] = q["alm"] <= budget
        q["timing_met"] = q["setup"] >= 0 and q["hold"] >= 0
        q["candidate"] = (q["bit_exact"] == "PASS" and q["const"] == "PASS" and q["alm_ok"] and q["timing_met"])
        rows[p] = q

    cands = [p for p in P_VALUES if rows[p]["candidate"]]
    t_min = min(rows[p]["t_ntt"] for p in cands) if cands else None

    yn = lambda b: "yes" if b else "no"
    print(f"ALM budget used for condition 3: {budget:,}\n")
    print(f"| P | bit-exact | constant cycle | ALM | ≤ {budget:,}? | worst setup / hold slack @ 40.000 ns | timing met? "
          "| cycles_NTT | cycles_INTT | Fmax per slow corner (MHz) | Fmax(P) = lowest | t_NTT (µs) | t_INTT (µs) "
          "| candidate? | d(P) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for p in P_VALUES:
        q = rows[p]
        fm = "; ".join(f"{c}: {v:.2f}" for c, v in q["fmax"])
        d = f"{(q['t_ntt'] - t_min) / t_min:.4f}" if q["candidate"] else "—"
        print(f"| {p} | {q['bit_exact']} | {q['const']} | {q['alm']:,} / {q['alm_den']} | {yn(q['alm_ok'])} "
              f"| {q['setup']:.3f} / {q['hold']:.3f} | {yn(q['timing_met'])} | {q['cyc_ntt']} | {q['cyc_intt']} "
              f"| {fm} | {q['fmax_low']:.2f} | {q['t_ntt']:.3f} | {q['t_intt']:.3f} | {yn(q['candidate'])} | {d} |")
    print()
    print("Other resources (MEASURED): " + "; ".join(
        f"P={p}: registers {rows[p]['reg']}, DSP {rows[p]['dsp']}, RAM blocks {rows[p]['ram']}" for p in P_VALUES))
    print("Evidence files: " + ", ".join(rows[p]["file"] for p in P_VALUES) + ", verification_status.json")
    print()
    print(f"Candidate set C = {{{', '.join(str(p) for p in cands)}}}")
    if not cands:
        print("RESULT: no candidate. Nothing is selected automatically (ADR 0007); the team decides.")
        return 0
    near = [p for p in cands if (rows[p]["t_ntt"] - t_min) / t_min <= NEAR_TIE]
    print(f"t_min = {t_min:.6f} us; within {NEAR_TIE:.0%} of t_min: {{{', '.join(str(p) for p in near)}}}")
    print(f"RESULT: P_selected = {min(near)} (smallest candidate with d(P) <= {NEAR_TIE}). "
          "To be recorded in a new ADR by the team.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
