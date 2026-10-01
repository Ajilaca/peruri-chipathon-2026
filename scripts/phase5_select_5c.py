#!/usr/bin/env python3
"""scripts/phase5_select_5c.py

Applies the 5c adoption rule of ADR 0014 §4 to the measured C4c (lazy INTT inputs), reading every value from files:

  - docs/evidence/phase05-arith/5c/quartus_C4c[-s<n>]_<date>.md (extract_quartus_report.py; seed 1 = no suffix)
  - docs/evidence/phase05-arith/5c/verification_status.json: correct PASS/FAIL (test plan A4 incl. exhaustive,
    formal bound proof with negative control, both simulators), cycles NTT / INTT
  - baseline: the Barrett 5b worksheet inputs, docs/evidence/phase05-arith/5b/quartus_C4b-B[-s<n>]_*.md

Rule (adopt C4c only if ALL hold):
  correct PASS; cycles exactly 119 / 375; ALM <= 12,573 at every seed; timing met at 40.000 ns at every seed
  (worst setup >= 0, worst hold >= 0); median over seeds 1-6 of the lowest slow-corner Fmax > 34.84 MHz (top of
  Barrett's 5b seed range); ADR 0012: t_NTT < 119 / 34.515 us and t_INTT < 375 / 34.515 us at the C4c median Fmax,
  where 34.515 MHz is Barrett's 5b median (recomputed here from the files, not typed).
Otherwise C4c is reported and not adopted. Usage: python3 scripts/phase5_select_5c.py [--date YYYYMMDD]
"""
import argparse
import json
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from phase5_select_5b import parse_quartus  # noqa: E402  (same parser, same fields)

E5B = ROOT / "docs" / "evidence" / "phase05-arith" / "5b"
E5C = ROOT / "docs" / "evidence" / "phase05-arith" / "5c"
ALM_BUDGET = 12573
CYCLES = (119, 375)
BARRETT_TOP = 34.84          # ADR 0014 §4: top of Barrett's 5b seed range (also recomputed below as a check)


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
    status = json.loads((E5C / "verification_status.json").read_text())
    c = load(E5C, "C4c", args.date)
    b = load(E5B, "C4b-B", None)
    b_med = statistics.median(q["fmax"] for q in b)
    b_top = max(q["fmax"] for q in b)
    c_med = statistics.median(q["fmax"] for q in c)
    correct = status["correct"] == "PASS"
    cyc_ok = (status["cycles_NTT"], status["cycles_INTT"]) == CYCLES
    alm_ok = all(q["alm"] <= ALM_BUDGET for q in c)
    tim_ok = all(q["setup"] >= 0 and q["hold"] >= 0 for q in c)
    fmax_ok = c_med > BARRETT_TOP
    tn_c, ti_c = CYCLES[0] / c_med, CYCLES[1] / c_med
    tn_b, ti_b = CYCLES[0] / b_med, CYCLES[1] / b_med
    adr12_ok = tn_c < tn_b and ti_c < ti_b
    print("## Per seed, C4c (MEASURED)")
    print("| Seed | ALM | Registers | M10K | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Evidence |")
    print("|---|---|---|---|---|---|---|---|---|")
    for q in c:
        print(f"| {q['seed']} | {q['alm']:,} | {q['reg']} | {q['ram']} | {q['dsp']} | {q['setup']:.3f} / {q['hold']:.3f} | "
              f"{'yes' if q['setup'] >= 0 and q['hold'] >= 0 else 'no'} | {q['fmax']:.2f} | `{q['file']}` |")
    print()
    print("## Comparison with Barrett 5b (C4b-B, medians over seeds 1-6; INFERENCE)")
    print("| | ALM median (min-max) | Fmax median (min-max) MHz | t_NTT / t_INTT at median Fmax (us) |")
    print("|---|---|---|---|")
    for name, rows, med, tn, ti in (("C4b-B (Barrett, 5b)", b, b_med, tn_b, ti_b), ("C4c (lazy INTT inputs)", c, c_med, tn_c, ti_c)):
        a = [q["alm"] for q in rows]
        f = [q["fmax"] for q in rows]
        print(f"| {name} | {statistics.median(a):,.1f} ({min(a):,}-{max(a):,}) | {med:.3f} ({min(f):.2f}-{max(f):.2f}) | {tn:.3f} / {ti:.3f} |")
    print()
    print("## Adoption rule (ADR 0014 §4)")
    checks = [
        ("correct (verification_status.json)", correct),
        ("cycles exactly 119 / 375", cyc_ok),
        (f"ALM <= {ALM_BUDGET:,} at every seed", alm_ok),
        ("timing met at 40.000 ns at every seed", tim_ok),
        (f"median Fmax {c_med:.3f} MHz > {BARRETT_TOP} MHz (Barrett 5b top; recomputed top {b_top:.2f})", fmax_ok),
        (f"ADR 0012: t_NTT {tn_c:.3f} < {tn_b:.3f} us and t_INTT {ti_c:.3f} < {ti_b:.3f} us", adr12_ok),
    ]
    for text, ok in checks:
        print(f"- {'PASS' if ok else 'FAIL'}: {text}")
    ok_all = all(ok for _, ok in checks)
    print()
    print(f"**Rule result: C4c {'ADOPTED' if ok_all else 'NOT adopted (C4b-B stays the C4 configuration)'}.**")
    return 0


if __name__ == "__main__":
    sys.exit(main())
