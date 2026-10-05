#!/usr/bin/env python3
"""scripts/quartus/phase5m_select_s7.py

Applies the S7 adoption rule of evidence/phase05m/test_plan_s7.md section 4 (fixed before measuring) to the measured
S7 (memory read path split, RD_SPLIT = 1, P = 7), reading every value from files:

  - evidence/phase05m/s7/quartus_S7[-s<n>].md (seed 1 = no suffix)
  - evidence/phase05m/s7/verification_status.json: correct PASS/FAIL (V1-V6), cycles NTT / INTT
  - baseline: evidence/phase05m/s6/quartus_M6[-s<n>].md (M6, the previous step; median recomputed here)

Rule (adopt S7 only if ALL hold):
  1. correct PASS;  2. cycles exactly NTT 120 / INTT 120;  3. ALM <= 12,573 at every seed and timing met at 40.000 ns at every seed;
  4. ADR 0012: t = 120 / F < 119 / F_M6 for NTT and INTT, F = median over seeds 1-6 of the lowest slow-corner Fmax.
No tolerance. Usage: python3 scripts/quartus/phase5m_select_s7.py [--date YYYYMMDD]
"""
import argparse
import json
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "scripts" / g) for g in ("build", "quartus")]
from phase5_select_5b import parse_quartus  # noqa: E402

E7 = ROOT / "evidence" / "phase05m" / "s7"
E6 = ROOT / "evidence" / "phase05m" / "s6"
ALM_BUDGET = 12573
CYCLES = (120, 120)
BASE_CYCLES = (119, 119)


def load(folder, prefix, date):
    rows = []
    for s in range(1, 7):
        rev = prefix + ("" if s == 1 else f"-s{s}")
        files = sorted(folder.glob(f"quartus_{rev}.md"))
        if not files:
            raise SystemExit(f"missing evidence for {rev} in {folder}")
        q = parse_quartus(files[-1])
        q["seed"] = s
        rows.append(q)
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=None)
    args = ap.parse_args()
    status = json.loads((E7 / "verification_status.json").read_text())
    m = load(E7, "S7", args.date)
    b = load(E6, "M6", None)
    b_med = statistics.median(q["fmax"] for q in b)
    m_med = statistics.median(q["fmax"] for q in m)
    correct = status["correct"] == "PASS"
    cyc_ok = (status["cycles_NTT"], status["cycles_INTT"]) == CYCLES
    alm_ok = all(q["alm"] <= ALM_BUDGET for q in m)
    tim_ok = all(q["setup"] >= 0 and q["hold"] >= 0 for q in m)
    tn_m, ti_m = CYCLES[0] / m_med, CYCLES[1] / m_med
    tn_b, ti_b = BASE_CYCLES[0] / b_med, BASE_CYCLES[1] / b_med
    ntt_ok, intt_ok = tn_m < tn_b, ti_m < ti_b
    print("## Per seed, S7 (MEASURED)")
    print("| Seed | ALM | Registers | M10K | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Evidence |")
    print("|---|---|---|---|---|---|---|---|---|")
    for q in m:
        print(f"| {q['seed']} | {q['alm']:,} | {q['reg']} | {q['ram']} | {q['dsp']} | {q['setup']:.3f} / {q['hold']:.3f} | "
              f"{'yes' if q['setup'] >= 0 and q['hold'] >= 0 else 'no'} | {q['fmax']:.2f} | `{q['file']}` |")
    print()
    print("## Comparison with M6 (medians over seeds 1-6; INFERENCE)")
    print("| | ALM median (min-max) | DSP | Fmax median (min-max) MHz | cycles NTT / INTT | t_NTT / t_INTT at median Fmax (us) |")
    print("|---|---|---|---|---|---|")
    for name, rows, med, cyc, tn, ti in (("M6 (previous step)", b, b_med, BASE_CYCLES, tn_b, ti_b),
                                        ("S7 (RD_SPLIT = 1, P = 7)", m, m_med, CYCLES, tn_m, ti_m)):
        a = [q["alm"] for q in rows]
        f = [q["fmax"] for q in rows]
        print(f"| {name} | {statistics.median(a):,.1f} ({min(a):,}-{max(a):,}) | {rows[0]['dsp']} | {med:.3f} ({min(f):.2f}-{max(f):.2f}) | "
              f"{cyc[0]} / {cyc[1]} | {tn:.3f} / {ti:.3f} |")
    print()
    print("## Adoption rule (test plan section 4)")
    checks = [
        ("correct (verification_status.json: V1-V6; V7 not run for S7, Amendment A1)", correct),
        ("cycles exactly NTT 120 / INTT 120", cyc_ok),
        (f"ALM <= {ALM_BUDGET:,} at every seed", alm_ok),
        ("timing met at 40.000 ns at every seed", tim_ok),
        (f"ADR 0012, t_NTT {tn_m:.3f} < {tn_b:.3f} us (M6 median Fmax {b_med:.3f} MHz; needs S7 median {m_med:.3f} MHz > {120 * b_med / 119:.3f} MHz)", ntt_ok),
        (f"ADR 0012, t_INTT {ti_m:.3f} < {ti_b:.3f} us", intt_ok),
    ]
    for text, ok in checks:
        print(f"- {'PASS' if ok else 'FAIL'}: {text}")
    ok_all = all(ok for _, ok in checks)
    print()
    print(f"**Rule result: S7 {'ADOPTED' if ok_all else 'NOT adopted by the rule (no tolerance was added)'}.**")
    spread = max(q["fmax"] for q in m) - min(q["fmax"] for q in m)
    print(f"Seed spread of S7 Fmax: {spread:.2f} MHz (min-max).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
