#!/usr/bin/env python3
"""scripts/select_8a.py

Applies the 8a adoption rule of docs/evidence/phase08-keccak-stream/8a/test_plan_8a.md section 4 (fixed before measuring) to the measured C5 (Keccak-f[1600], two rounds per cycle),
reading every value from files:

  - docs/evidence/phase08-keccak-stream/8a/quartus_C5[-s<n>]_<date>.md (seed 1 = no suffix); information: quartus_C5-20_*.md
  - docs/evidence/phase08-keccak-stream/8a/verification_status.json: correct PASS/FAIL (V1-V9), busy cycles, permutation cycles in the sponge
  - baseline K0: docs/evidence/phase07-keccak/quartus_K0[-s<n>]_*.md (seeds 1-6; median recomputed here)

Rule (adopt C5 only if ALL hold):
  1. correct PASS;  2. busy exactly 12 cycles and 14 cycles per permutation in the sponge;  3. ALM <= 12,573 at every seed (working cap, see the test plan) and timing met at 40.000 ns at every seed;
  4. t = 14 / F_C5 < 26 / F_K0, F = median over seeds 1-6 of the lowest slow-corner Fmax.
No tolerance. Usage: python3 scripts/select_8a.py
"""
import json
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from phase5_select_5b import parse_quartus  # noqa: E402

E8 = ROOT / "docs" / "evidence" / "phase08-keccak-stream" / "8a"
E7 = ROOT / "docs" / "evidence" / "phase07-keccak"
ALM_BUDGET = 12573
BUSY, PERM = 12, 14
BASE_PERM = 26


def load(folder, prefix):
    rows = []
    for s in range(1, 7):
        rev = prefix + ("" if s == 1 else f"-s{s}")
        files = sorted(folder.glob(f"quartus_{rev}_*.md"))
        if not files:
            raise SystemExit(f"missing evidence for {rev} in {folder}")
        q = parse_quartus(files[-1])
        q["seed"] = s
        rows.append(q)
    return rows


def main() -> int:
    status = json.loads((E8 / "verification_status.json").read_text())
    m = load(E8, "C5")
    b = load(E7, "K0")
    b_med = statistics.median(q["fmax"] for q in b)
    m_med = statistics.median(q["fmax"] for q in m)
    correct = status["correct"] == "PASS"
    cyc_ok = (status["busy_cycles"], status["perm_cycles_sponge"]) == (BUSY, PERM)
    alm_ok = all(q["alm"] <= ALM_BUDGET for q in m)
    tim_ok = all(q["setup"] >= 0 and q["hold"] >= 0 for q in m)
    t_m, t_b = PERM / m_med, BASE_PERM / b_med
    perm_ok = t_m < t_b
    print("## Per seed at 40.000 ns (MEASURED)")
    print("| Seed | Config | ALM | Registers | M10K | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Evidence |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for name, rows in (("K0", b), ("C5", m)):
        for q in rows:
            print(f"| {q['seed']} | {name} | {q['alm']:,} | {q['reg']} | {q['ram']} | {q['dsp']} | {q['setup']:.3f} / {q['hold']:.3f} | "
                  f"{'yes' if q['setup'] >= 0 and q['hold'] >= 0 else 'no'} | {q['fmax']:.2f} | `{q['file']}` |")
    print()
    print("## Comparison with K0 (medians over seeds 1-6; INFERENCE)")
    print("| | ALM median (min-max) | Registers | Fmax median (min-max) MHz | cycles per permutation (sponge) | t per permutation at median Fmax (us) |")
    print("|---|---|---|---|---|---|")
    for name, rows, med, cyc, t in (("K0 (previous step)", b, b_med, BASE_PERM, t_b), ("C5 (two rounds per cycle)", m, m_med, PERM, t_m)):
        a = [q["alm"] for q in rows]
        f = [q["fmax"] for q in rows]
        r = [q["reg"] for q in rows]
        print(f"| {name} | {statistics.median(a):,.1f} ({min(a):,}-{max(a):,}) | {min(r)}-{max(r)} | {med:.3f} ({min(f):.2f}-{max(f):.2f}) | {cyc} | {t:.4f} |")
    print()
    print("## Adoption rule (test plan section 4)")
    checks = [
        ("correct (verification_status.json: V1-V9, both simulators, controls fail, formal)", correct),
        ("busy exactly 12 cycles and 14 cycles per permutation in the sponge", cyc_ok),
        (f"ALM <= {ALM_BUDGET:,} at every seed (working cap)", alm_ok),
        ("timing met at 40.000 ns at every seed", tim_ok),
        (f"ADR 0012 style: t = 14 / F_C5 = {t_m:.4f} us < 26 / F_K0 = {t_b:.4f} us (K0 median Fmax {b_med:.3f} MHz; C5 median {m_med:.3f} MHz must exceed {14 * b_med / 26:.3f} MHz)", perm_ok),
    ]
    for text, ok in checks:
        print(f"- {'PASS' if ok else 'FAIL'}: {text}")
    ok_all = all(ok for _, ok in checks)
    print()
    print(f"**Rule result: C5 {'ADOPTED' if ok_all else 'NOT adopted by the rule (no tolerance was added)'}.**")
    print(f"Seed spread of C5 Fmax: {max(q['fmax'] for q in m) - min(q['fmax'] for q in m):.2f} MHz (min-max); K0: {max(q['fmax'] for q in b) - min(q['fmax'] for q in b):.2f} MHz.")
    print()
    print("## Information: 20.000 ns compiles (not part of the rule)")
    for name, folder, pat in (("K0-20", E7, "quartus_K0-20_*.md"), ("C5-20", E8, "quartus_C5-20_*.md")):
        files = sorted(folder.glob(pat))
        if not files:
            print(f"- {name}: not compiled")
            continue
        q = parse_quartus(files[-1])
        print(f"- {name} (seed 1): ALM {q['alm']:,}, worst setup {q['setup']:.3f} ns ({'met' if q['setup'] >= 0 else 'NOT met'}), Fmax lowest slow corner {q['fmax']:.2f} MHz, `{q['file']}`")
    return 0


if __name__ == "__main__":
    sys.exit(main())
