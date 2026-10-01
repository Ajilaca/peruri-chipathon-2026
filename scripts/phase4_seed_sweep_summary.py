#!/usr/bin/env python3
"""scripts/phase4_seed_sweep_summary.py

Summarises the Phase 4 fitter-seed sweep for P = 4 and P = 6 (input to ADR 0008). Reads only evidence files
written by extract_quartus_report.py:
  seed 1 (default, the measured revisions):  docs/evidence/phase04-pipeline/quartus_C3-P<p>_*.md
  seeds 2..6:                                docs/evidence/phase04-pipeline/seed_sweep/quartus_C3-P<p>-s<n>_*.md
and applies, per seed, the same per-revision conditions as ADR 0007 (ALM <= budget, default 10,478 = ADR 0004, `--alm-budget 12573` = ADR 0009; worst setup and hold
slack >= 0 at 40.000 ns). Cycle counts do not depend on the seed (same RTL), so t_NTT uses the simulated
cycles of verification_status.json. Nothing here changes the selection rule or the measured worksheet.

Usage: python3 scripts/phase4_seed_sweep_summary.py      (prints Markdown)
"""
import argparse
import json
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from phase4_select_p import ALM_BUDGET, EVID, NEAR_TIE, parse_quartus  # noqa: E402

SEEDS = (1, 2, 3, 4, 5, 6)


def evidence(p: int, seed: int) -> pathlib.Path:
    pat = f"quartus_C3-P{p}_*.md" if seed == 1 else f"seed_sweep/quartus_C3-P{p}-s{seed}_*.md"
    files = sorted(EVID.glob(pat))
    if not files:
        raise SystemExit(f"missing evidence for P={p} seed={seed} ({pat})")
    return files[-1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--alm-budget", type=int, default=ALM_BUDGET)
    budget = ap.parse_args().alm_budget
    status = json.loads((EVID / "verification_status.json").read_text())
    res = {}
    print(f"ALM budget: {budget:,}\n")
    print(f"| P | Seed | ALM | <= {budget:,}? | Registers | M10K | Worst setup / hold slack (ns) | Timing met? "
          "| Fmax(P) lowest slow corner (MHz) | t_NTT (us) | Meets all ADR 0007 conditions? | Evidence |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for p in (4, 6):
        cyc = int(status[str(p)]["cycles_NTT"])
        for s in SEEDS:
            f = evidence(p, s)
            q = parse_quartus(f)
            fl = min(v for _, v in q["fmax"])
            ok_alm = q["alm"] <= budget
            ok_t = q["setup"] >= 0 and q["hold"] >= 0
            res[(p, s)] = dict(alm=q["alm"], fmax=fl, t=cyc / fl, cand=ok_alm and ok_t)
            print(f"| {p} | {s}{' (default)' if s == 1 else ''} | {q['alm']:,} | {'yes' if ok_alm else 'no'} | {q['reg']} "
                  f"| {q['ram']} | {q['setup']:.3f} / {q['hold']:.3f} | {'yes' if ok_t else 'no'} | {fl:.2f} "
                  f"| {cyc / fl:.3f} | {'yes' if ok_alm and ok_t else 'no'} | `{f.relative_to(EVID.parents[2])}` |")
    print()
    print(f"| P | ALM min / median / max | Seeds within {budget:,} | Fmax min / median / max (MHz) | Seeds meeting all ADR 0007 conditions |")
    print("|---|---|---|---|---|")
    for p in (4, 6):
        a = [res[(p, s)]["alm"] for s in SEEDS]
        fm = [res[(p, s)]["fmax"] for s in SEEDS]
        n_alm = sum(x <= budget for x in a)
        n_c = sum(res[(p, s)]["cand"] for s in SEEDS)
        print(f"| {p} | {min(a):,} / {statistics.median(a):,.1f} / {max(a):,} | {n_alm} of {len(SEEDS)} "
              f"| {min(fm):.2f} / {statistics.median(fm):.2f} / {max(fm):.2f} | {n_c} of {len(SEEDS)} |")
    print()
    print("Per seed, the ADR 0007 rule applied to {P=4, P=6} only (P=0 and P=2 were not swept; at the default "
          "seed both miss timing at 40.000 ns):")
    print()
    print("| Seed | Candidates among {4, 6} | Rule result |")
    print("|---|---|---|")
    for s in SEEDS:
        c = [p for p in (4, 6) if res[(p, s)]["cand"]]
        if not c:
            r = "no candidate"
        else:
            tmin = min(res[(p, s)]["t"] for p in c)
            r = f"P = {min(p for p in c if (res[(p, s)]['t'] - tmin) / tmin <= NEAR_TIE)}"
        print(f"| {s} | {{{', '.join(map(str, c))}}} | {r} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
