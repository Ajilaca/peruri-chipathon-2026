#!/usr/bin/env python3
"""scripts/quartus/select_s10.py

Applies the S10 adoption rule of evidence/phase06/test_plan_s10.md section 4 (fixed before measuring) to the measured
S10 (16-bank 1R1W memory without slot arbitration, P = 5), reading every value from files:

  - evidence/phase06/s10/quartus_S10[-s<n>].md (seed 1 = no suffix); information: quartus_S10-20[-s<n>].md
  - evidence/phase06/s10/verification_status.json: correct PASS/FAIL (V1-V6), cycles NTT / INTT
  - baseline: evidence/phase05m/s7/quartus_S7[-s<n>].md (S7; median recomputed here); information: evidence/phase05m/fmax50/quartus_S7-20[-s<n>].md

Rule (adopt S10 only if ALL hold):
  1. correct PASS;  2. cycles exactly NTT 118 / INTT 118;  3. ALM <= 12,573 at every seed and timing met at 40.000 ns at every seed;
  4. ADR 0012: t = 118 / F < 120 / F_S7 for NTT and INTT, F = median over seeds 1-6 of the lowest slow-corner Fmax.
No tolerance. Usage: python3 scripts/quartus/select_s10.py [--date YYYYMMDD]
"""
import argparse
import json
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "scripts" / g) for g in ("build", "quartus")]
from phase5_select_5b import parse_quartus  # noqa: E402

E10 = ROOT / "evidence" / "phase06" / "s10"
E7 = ROOT / "evidence" / "phase05m" / "s7"
E50 = ROOT / "evidence" / "phase05m" / "fmax50"
ALM_BUDGET = 12573
CYCLES = (118, 118)
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
    status = json.loads((E10 / "verification_status.json").read_text())
    m = load(E10, "S10", args.date)
    b = load(E7, "S7", None)
    b_med = statistics.median(q["fmax"] for q in b)
    m_med = statistics.median(q["fmax"] for q in m)
    correct = status["correct"] == "PASS"
    cyc_ok = (status["cycles_NTT"], status["cycles_INTT"]) == CYCLES
    alm_ok = all(q["alm"] <= ALM_BUDGET for q in m)
    tim_ok = all(q["setup"] >= 0 and q["hold"] >= 0 for q in m)
    tn_m, ti_m = CYCLES[0] / m_med, CYCLES[1] / m_med
    tn_b, ti_b = BASE_CYCLES[0] / b_med, BASE_CYCLES[1] / b_med
    ntt_ok, intt_ok = tn_m < tn_b, ti_m < ti_b
    print("## Per seed, S10 at 40.000 ns (MEASURED)")
    print("| Seed | ALM | Registers | M10K | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Evidence |")
    print("|---|---|---|---|---|---|---|---|---|")
    for q in m:
        print(f"| {q['seed']} | {q['alm']:,} | {q['reg']} | {q['ram']} | {q['dsp']} | {q['setup']:.3f} / {q['hold']:.3f} | "
              f"{'yes' if q['setup'] >= 0 and q['hold'] >= 0 else 'no'} | {q['fmax']:.2f} | `{q['file']}` |")
    print()
    print("## Comparison with S7 (medians over seeds 1-6; INFERENCE)")
    print("| | ALM median (min-max) | DSP | Fmax median (min-max) MHz | cycles NTT / INTT | t_NTT / t_INTT at median Fmax (us) |")
    print("|---|---|---|---|---|---|")
    for name, rows, med, cyc, tn, ti in (("S7 (previous step)", b, b_med, BASE_CYCLES, tn_b, ti_b),
                                        ("S10 (16 x 1R1W, P = 5)", m, m_med, CYCLES, tn_m, ti_m)):
        a = [q["alm"] for q in rows]
        f = [q["fmax"] for q in rows]
        print(f"| {name} | {statistics.median(a):,.1f} ({min(a):,}-{max(a):,}) | {rows[0]['dsp']} | {med:.3f} ({min(f):.2f}-{max(f):.2f}) | "
              f"{cyc[0]} / {cyc[1]} | {tn:.3f} / {ti:.3f} |")
    print()
    print("## Adoption rule (test plan section 4)")
    checks = [
        ("correct (verification_status.json: V1-V6 incl. the Phase 6 top with S10)", correct),
        ("cycles exactly NTT 118 / INTT 118", cyc_ok),
        (f"ALM <= {ALM_BUDGET:,} at every seed", alm_ok),
        ("timing met at 40.000 ns at every seed", tim_ok),
        (f"ADR 0012, t_NTT {tn_m:.3f} < {tn_b:.3f} us (S7 median Fmax {b_med:.3f} MHz; S10 median {m_med:.3f} MHz must exceed {118 * b_med / 120:.3f} MHz)", ntt_ok),
        (f"ADR 0012, t_INTT {ti_m:.3f} < {ti_b:.3f} us", intt_ok),
    ]
    for text, ok in checks:
        print(f"- {'PASS' if ok else 'FAIL'}: {text}")
    ok_all = all(ok for _, ok in checks)
    print()
    print(f"**Rule result: S10 {'ADOPTED' if ok_all else 'NOT adopted by the rule (no tolerance was added)'}.**")
    spread = max(q["fmax"] for q in m) - min(q["fmax"] for q in m)
    print(f"Seed spread of S10 Fmax: {spread:.2f} MHz (min-max).")
    print()
    print("## Information: 20.000 ns compiles (not part of the rule; 50 MHz needs worst setup slack >= 0 at 20 ns)")
    print("| Revision | seeds | worst setup (ns) per seed | timing met at 20 ns | Fmax lowest slow corner per seed (MHz) | median |")
    print("|---|---|---|---|---|---|")
    for name, folder, prefix in (("S7-20", E50, "S7-20"), ("S10-20", E10, "S10-20")):
        try:
            rows = load(folder, prefix, None)
        except SystemExit as e:
            print(f"| {name} | - | {e} | - | - | - |")
            continue
        print(f"| {name} | 1-6 | {', '.join(f'{q['setup']:.3f}' for q in rows)} | "
              f"{sum(1 for q in rows if q['setup'] >= 0)}/6 | {', '.join(f'{q['fmax']:.2f}' for q in rows)} | "
              f"{statistics.median(q['fmax'] for q in rows):.3f} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
