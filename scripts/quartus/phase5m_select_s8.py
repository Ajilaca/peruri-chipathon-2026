#!/usr/bin/env python3
"""scripts/quartus/phase5m_select_s8.py

Applies the S8 adoption rule of evidence/phase05m/test_plan_s8.md section 4 (fixed before measuring) to the measured
S8 (write-path register, P = 8, one bubble per direction), reading every value from files:

  - evidence/phase05m/s8/quartus_S8[-s<n>].md (seed 1 = no suffix)
  - evidence/phase05m/s8/verification_status.json: correct PASS/FAIL (V1-V8), cycles NTT / INTT
  - baseline: evidence/phase05m/s7/quartus_S7[-s<n>].md (S7, the previous step; median recomputed here)
  - for the record only: M6 (s6/) and C4b-B (evidence/phase05/5b/)

Rule (adopt S8 only if ALL hold):
  1. correct PASS;  2. cycles exactly NTT 122 / INTT 122;  3. ALM <= 12,573 at every seed and timing met at 40.000 ns at every seed;
  4. ADR 0012: t = 122 / F < 120 / F_S7 for NTT and INTT, F = median over seeds 1-6 of the lowest slow-corner Fmax.
No tolerance. Usage: python3 scripts/quartus/phase5m_select_s8.py [--date YYYYMMDD]
"""
import argparse
import json
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "scripts" / g) for g in ("build", "quartus")]
from phase5_select_5b import parse_quartus  # noqa: E402

E8 = ROOT / "evidence" / "phase05m" / "s8"
E7 = ROOT / "evidence" / "phase05m" / "s7"
E6 = ROOT / "evidence" / "phase05m" / "s6"
E5B = ROOT / "evidence" / "phase05" / "5b"
ALM_BUDGET = 12573
CYCLES = (122, 122)
BASE_CYCLES = (120, 120)


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
    status = json.loads((E8 / "verification_status.json").read_text())
    m = load(E8, "S8", args.date)
    b = load(E7, "S7", None)
    m6 = load(E6, "M6", None)
    c4 = load(E5B, "C4b-B", None)
    b_med = statistics.median(q["fmax"] for q in b)
    m_med = statistics.median(q["fmax"] for q in m)
    correct = status["correct"] == "PASS"
    cyc_ok = (status["cycles_NTT"], status["cycles_INTT"]) == CYCLES
    alm_ok = all(q["alm"] <= ALM_BUDGET for q in m)
    tim_ok = all(q["setup"] >= 0 and q["hold"] >= 0 for q in m)
    tn_m, ti_m = CYCLES[0] / m_med, CYCLES[1] / m_med
    tn_b, ti_b = BASE_CYCLES[0] / b_med, BASE_CYCLES[1] / b_med
    ntt_ok, intt_ok = tn_m < tn_b, ti_m < ti_b
    print("## Per seed, S8 (MEASURED)")
    print("| Seed | ALM | Registers | M10K | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Evidence |")
    print("|---|---|---|---|---|---|---|---|---|")
    for q in m:
        print(f"| {q['seed']} | {q['alm']:,} | {q['reg']} | {q['ram']} | {q['dsp']} | {q['setup']:.3f} / {q['hold']:.3f} | "
              f"{'yes' if q['setup'] >= 0 and q['hold'] >= 0 else 'no'} | {q['fmax']:.2f} | `{q['file']}` |")
    print()
    print("## Comparison with the earlier steps (medians over seeds 1-6; INFERENCE; the rule compares with S7 only)")
    print("| | ALM median (min-max) | DSP | Fmax median (min-max) MHz | cycles NTT / INTT | t_NTT / t_INTT at median Fmax (us) |")
    print("|---|---|---|---|---|---|")
    m6_med, c4_med = statistics.median(q["fmax"] for q in m6), statistics.median(q["fmax"] for q in c4)
    for name, rows, med, cyc, tn, ti in (("C4b-B (Phase 5)", c4, c4_med, (119, 375), 119 / c4_med, 375 / c4_med),
                                        ("M6 (S6)", m6, m6_med, (119, 119), 119 / m6_med, 119 / m6_med),
                                        ("S7 (previous step)", b, b_med, BASE_CYCLES, tn_b, ti_b),
                                        ("S8 (write register, P = 8, one bubble)", m, m_med, CYCLES, tn_m, ti_m)):
        a = [q["alm"] for q in rows]
        f = [q["fmax"] for q in rows]
        print(f"| {name} | {statistics.median(a):,.1f} ({min(a):,}-{max(a):,}) | {rows[0]['dsp']} | {med:.3f} ({min(f):.2f}-{max(f):.2f}) | "
              f"{cyc[0]} / {cyc[1]} | {tn:.3f} / {ti:.3f} |")
    print()
    print("## Adoption rule (test plan section 4)")
    checks = [
        ("correct (verification_status.json: V1-V8, the regression V8 run once at S8 by Amendment A1)", correct),
        ("cycles exactly NTT 122 / INTT 122", cyc_ok),
        (f"ALM <= {ALM_BUDGET:,} at every seed", alm_ok),
        ("timing met at 40.000 ns at every seed", tim_ok),
        (f"ADR 0012, t_NTT {tn_m:.3f} < {tn_b:.3f} us (S7 median Fmax {b_med:.3f} MHz; S8 median {m_med:.3f} MHz must exceed {122 * b_med / 120:.3f} MHz)", ntt_ok),
        (f"ADR 0012, t_INTT {ti_m:.3f} < {ti_b:.3f} us", intt_ok),
    ]
    for text, ok in checks:
        print(f"- {'PASS' if ok else 'FAIL'}: {text}")
    ok_all = all(ok for _, ok in checks)
    print()
    print(f"**Rule result: S8 {'ADOPTED' if ok_all else 'NOT adopted by the rule (no tolerance was added)'}.**")
    spread = max(q["fmax"] for q in m) - min(q["fmax"] for q in m)
    print(f"Seed spread of S8 Fmax: {spread:.2f} MHz (min-max).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
