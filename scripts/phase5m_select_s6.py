#!/usr/bin/env python3
"""scripts/phase5m_select_s6.py

Applies the S6 adoption rule of docs/evidence/phase05m-memsched/test_plan.md section 4 (fixed before measuring) to the measured
M6 (INTT without the scaling pass), reading every value from files:

  - docs/evidence/phase05m-memsched/s6/quartus_M6[-s<n>]_<date>.md (extract_quartus_report.py; seed 1 = no suffix)
  - docs/evidence/phase05m-memsched/s6/verification_status.json: correct PASS/FAIL (V1-V9), cycles NTT / INTT
  - baseline: docs/evidence/phase05-arith/5b/quartus_C4b-B[-s<n>]_*.md (C4b-B, the previous step; median recomputed here)

Rule (adopt M6 only if ALL hold):
  1. correct PASS;  2. cycles exactly NTT 119 / INTT 119;  3. ALM <= 12,573 at every seed and timing met at 40.000 ns at every seed
  (worst setup >= 0, worst hold >= 0);  4. ADR 0012: t_NTT = 119 / F < 119 / F_C4b-B and t_INTT = 119 / F < 375 / F_C4b-B with F the
  median over seeds 1-6 of the lowest slow-corner Fmax (F_C4b-B = 34.515 MHz, recomputed from the files).
No tolerance. Usage: python3 scripts/phase5m_select_s6.py [--date YYYYMMDD]
"""
import argparse
import json
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from phase5_select_5b import parse_quartus  # noqa: E402

E6 = ROOT / "docs" / "evidence" / "phase05m-memsched" / "s6"
E5B = ROOT / "docs" / "evidence" / "phase05-arith" / "5b"
ALM_BUDGET = 12573
CYCLES = (119, 119)
BASE_CYCLES = (119, 375)


def load(folder, prefix, date):
    rows = []
    for s in range(1, 7):
        rev = prefix + ("" if s == 1 else f"-s{s}")
        files = sorted(folder.glob(f"quartus_{rev}_{date or '*'}.md"))
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
    status = json.loads((E6 / "verification_status.json").read_text())
    m = load(E6, "M6", args.date)
    b = load(E5B, "C4b-B", None)
    b_med = statistics.median(q["fmax"] for q in b)
    m_med = statistics.median(q["fmax"] for q in m)
    correct = status["correct"] == "PASS"
    cyc_ok = (status["cycles_NTT"], status["cycles_INTT"]) == CYCLES
    alm_ok = all(q["alm"] <= ALM_BUDGET for q in m)
    tim_ok = all(q["setup"] >= 0 and q["hold"] >= 0 for q in m)
    tn_m, ti_m = CYCLES[0] / m_med, CYCLES[1] / m_med
    tn_b, ti_b = BASE_CYCLES[0] / b_med, BASE_CYCLES[1] / b_med
    ntt_ok, intt_ok = tn_m < tn_b, ti_m < ti_b
    print("## Per seed, M6 (MEASURED)")
    print("| Seed | ALM | Registers | M10K | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Evidence |")
    print("|---|---|---|---|---|---|---|---|---|")
    for q in m:
        print(f"| {q['seed']} | {q['alm']:,} | {q['reg']} | {q['ram']} | {q['dsp']} | {q['setup']:.3f} / {q['hold']:.3f} | "
              f"{'yes' if q['setup'] >= 0 and q['hold'] >= 0 else 'no'} | {q['fmax']:.2f} | `{q['file']}` |")
    print()
    print("## Comparison with C4b-B (medians over seeds 1-6; INFERENCE)")
    print("| | ALM median (min-max) | DSP | Fmax median (min-max) MHz | cycles NTT / INTT | t_NTT / t_INTT at median Fmax (us) |")
    print("|---|---|---|---|---|---|")
    for name, rows, med, cyc, tn, ti in (("C4b-B (previous step)", b, b_med, BASE_CYCLES, tn_b, ti_b),
                                        ("M6 (INTT without scaling pass)", m, m_med, CYCLES, tn_m, ti_m)):
        a = [q["alm"] for q in rows]
        f = [q["fmax"] for q in rows]
        print(f"| {name} | {statistics.median(a):,.1f} ({min(a):,}-{max(a):,}) | {rows[0]['dsp']} | {med:.3f} ({min(f):.2f}-{max(f):.2f}) | "
              f"{cyc[0]} / {cyc[1]} | {tn:.3f} / {ti:.3f} |")
    print()
    print("## Adoption rule (test plan section 4)")
    checks = [
        ("correct (verification_status.json: V1-V8; V9 not run for S6, Amendment A1)", correct),
        ("cycles exactly NTT 119 / INTT 119", cyc_ok),
        (f"ALM <= {ALM_BUDGET:,} at every seed", alm_ok),
        ("timing met at 40.000 ns at every seed", tim_ok),
        (f"ADR 0012, t_INTT {ti_m:.3f} < {ti_b:.3f} us (C4b-B median Fmax {b_med:.3f} MHz)", intt_ok),
        (f"ADR 0012, t_NTT {tn_m:.3f} < {tn_b:.3f} us (needs M6 median Fmax {m_med:.3f} MHz > {b_med:.3f} MHz)", ntt_ok),
    ]
    for text, ok in checks:
        print(f"- {'PASS' if ok else 'FAIL'}: {text}")
    ok_all = all(ok for _, ok in checks)
    print()
    print(f"**Rule result: M6 {'ADOPTED' if ok_all else 'NOT adopted by the rule (no tolerance was added)'}.**")
    if not ok_all and correct and cyc_ok and alm_ok and tim_ok and intt_ok and not ntt_ok:
        print("Only the NTT part of ADR 0012 failed (NTT mode is unchanged in cycles; the margin is the median Fmax). "
              "Test plan section 4: reported as measured; any other rule is a new decision of the team.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
