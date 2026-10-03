#!/usr/bin/env python3
"""scripts/select_8cd.py

Applies the adoption rules of docs/evidence/phase08-keccak-stream/8c/test_plan_8c.md section 5 (STREAM against STORE) and 8d/test_plan_8d.md section 5 (OVERLAP against STREAM), fixed before measuring, reading every value from files:

  - Quartus: docs/evidence/phase08-keccak-stream/8c/quartus_SMP0[-s<n>]_<date>.md (STORE), quartus_SMP1[-s<n>]_*.md (STREAM); 8d/quartus_SMP2[-s<n>]_*.md (OVERLAP); seed 1 = no suffix; information: -20 revisions
  - cycles: 8c/cycles_v0_*.json, cycles_v1_*.json and 8d/cycles_v2_*.json (verification output: cycles per program for the same inputs, every variant), mean over the cases of each program
  - verification status: 8c/verification_status_8c.json and 8d/verification_status_8d.json (correct PASS/FAIL: V1-V8, both simulators, controls fail, formal)

Rule (candidate adopted over the reference only if ALL hold): 1. correct PASS;  2. the fit succeeded for both (evidence exists) and timing met at 40.000 ns at every seed for the candidate;
3. t = c / F lower for the candidate than for the reference for KeyGen and for Encrypt (F = median over seeds 1-6 of the lowest slow-corner Fmax at 40 ns, c = mean cycles over the same inputs);  4. M10K(candidate) <= M10K(reference) at every seed.
No tolerance. Usage: python3 scripts/select_8cd.py
"""
import json
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from phase5_select_5b import parse_quartus  # noqa: E402

E = ROOT / "docs" / "evidence" / "phase08-keccak-stream"


def load(folder, prefix):
    rows = []
    for s in range(1, 7):
        rev = prefix + ("" if s == 1 else f"-s{s}")
        files = sorted(folder.glob(f"quartus_{rev}_*.md"))
        if not files:
            return None
        q = parse_quartus(files[-1])
        q["seed"] = s
        rows.append(q)
    return rows


def cycles(folder, var):
    files = sorted(folder.glob(f"cycles_v{var}_*.json"))
    if not files:
        return None
    d = json.loads(files[-1].read_text())
    return {k: statistics.mean(v) for k, v in d["cycles"].items()}, d["cycles"], files[-1].name


def report(title, cand, ref, cn, rn, cand_rows, ref_rows, cand_cyc, ref_cyc, status):
    print(f"## {title}")
    print(f"| Seed | Config | ALM | Registers | M10K | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Evidence |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for name, rows in ((rn, ref_rows), (cn, cand_rows)):
        for q in rows:
            print(f"| {q['seed']} | {name} | {q['alm']:,} | {q['reg']} | {q['ram']} | {q['dsp']} | {q['setup']:.3f} / {q['hold']:.3f} | {'yes' if q['setup'] >= 0 and q['hold'] >= 0 else 'no'} | {q['fmax']:.2f} | `{q['file']}` |")
    fm = {n: statistics.median(q["fmax"] for q in rows) for n, rows in ((rn, ref_rows), (cn, cand_rows))}
    print()
    print("| | ALM median (min-max) | Registers | M10K | DSP | Fmax median (min-max) MHz | KeyGen cycles (mean) | Encrypt cycles (mean) | Decrypt cycles (mean) | t KeyGen (us) | t Encrypt (us) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    t = {}
    for n, rows, cyc in ((rn, ref_rows, ref_cyc), (cn, cand_rows, cand_cyc)):
        a = [q["alm"] for q in rows]
        f = [q["fmax"] for q in rows]
        r = [q["reg"] for q in rows]
        m = [q["ram"] for q in rows]
        d = [q["dsp"] for q in rows]
        c = cyc[0]
        t[n] = (c["keygen"] / fm[n], c["encrypt"] / fm[n])
        print(f"| {n} | {statistics.median(a):,.1f} ({min(a):,}-{max(a):,}) | {min(r)}-{max(r)} | {min(m)}-{max(m)} | {min(d)}-{max(d)} | {fm[n]:.3f} ({min(f):.2f}-{max(f):.2f}) | {c['keygen']:.1f} | {c['encrypt']:.1f} | {c['decrypt']:.1f} | {t[n][0]:.4f} | {t[n][1]:.4f} |")
    print(f"\nCycle sources: `{ref_cyc[2]}`, `{cand_cyc[2]}` (same inputs for every variant).")
    checks = [
        ("correct (verification_status: V1-V8, both simulators, controls fail, formal)", status.get("correct") == "PASS"),
        (f"fit succeeded for both and timing met at 40.000 ns at every seed for {cn}", all(q["setup"] >= 0 and q["hold"] >= 0 for q in cand_rows)),
        (f"t = c / F lower for {cn} than for {rn} for KeyGen ({t[cn][0]:.4f} < {t[rn][0]:.4f} us) and for Encrypt ({t[cn][1]:.4f} < {t[rn][1]:.4f} us)", t[cn][0] < t[rn][0] and t[cn][1] < t[rn][1]),
        (f"M10K({cn}) <= M10K({rn}) at every seed", all(c["ram"] <= r["ram"] for c, r in zip(cand_rows, ref_rows))),
    ]
    print(f"\n### Adoption rule ({cn} over {rn})")
    for text, ok in checks:
        print(f"- {'PASS' if ok else 'FAIL'}: {text}")
    ok_all = all(ok for _, ok in checks)
    print(f"\n**Rule result: {cn} {'ADOPTED' if ok_all else 'NOT adopted by the rule (no tolerance was added)'}.**\n")
    rev = {"STORE": "SMP0", "STREAM": "SMP1", "OVERLAP": "SMP2"}
    for n in (rn, cn):
        files = sorted((E / ("8d" if rev[n] == "SMP2" else "8c")).glob(f"quartus_{rev[n]}-20_*.md"))
        if files:
            q = parse_quartus(files[-1])
            print(f"- information {n} ({rev[n]}-20, 20.000 ns, seed 1): ALM {q['alm']:,}, M10K {q['ram']}, worst setup {q['setup']:.3f} ns ({'met' if q['setup'] >= 0 else 'NOT met'}), Fmax lowest slow corner {q['fmax']:.2f} MHz, `{q['file']}`")
    print()
    return ok_all


def main() -> int:
    store, stream = load(E / "8c", "SMP0"), load(E / "8c", "SMP1")
    cs, cm = cycles(E / "8c", 0), cycles(E / "8c", 1)
    sf = E / "8c" / "verification_status_8c.json"
    if store and stream and cs and cm and sf.exists():
        report("8c: STREAM (A_hat sampled straight into the PWM unit) against STORE (A_hat sampled into slots)", "SMP1", "SMP0", "STREAM", "STORE", stream, store, cm, cs, json.loads(sf.read_text()))
    else:
        print("## 8c: not complete (missing Quartus evidence, cycle tables or status)\n")
    over = load(E / "8d", "SMP2")
    co = cycles(E / "8d", 2)
    sf8 = E / "8d" / "verification_status_8d.json"
    if over and stream and co and cm and sf8.exists():
        report("8d: OVERLAP (noise sampling during the transforms) against STREAM", "SMP2", "SMP1", "OVERLAP", "STREAM", over, stream, co, cm, json.loads(sf8.read_text()))
    else:
        print("## 8d: not complete (missing Quartus evidence, cycle tables or status)\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
