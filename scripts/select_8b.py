#!/usr/bin/env python3
"""scripts/select_8b.py

Applies the 8b acceptance gate (test plan section 4) to each measured output width and the W1-versus-W2 selection rule (section 5), fixed before measuring, reading every value from files:

  - docs/evidence/phase08-keccak-stream/8b/quartus_SM<w>[-s<n>]_<date>.md (seed 1 = no suffix; w = 1 or 2); information: quartus_SM<w>-20_*.md and quartus_SM<w>-K0_*.md
  - docs/evidence/phase08-keccak-stream/8b/verification_status_W<w>.json: correct PASS/FAIL (V1-V10: both simulators, controls fail, formal, regression)
  - docs/evidence/phase08-keccak-stream/8b/cycles_w<w>_c5_<date>.json: cycle table of the C5 top (mean cycles per SampleNTT polynomial over the V5 set and the CBD count)
  - reference: S10 (NTT/INTT core) Fmax median recomputed from docs/evidence/phase06-scheduling/s10/quartus_S10[-s<n>]_*.md

Gate per width (ALL must hold): 1. correct PASS;  2. M10K = 0 and DSP = 0 at every seed;  3. ALM <= 12,573 at every seed and timing met at 40.000 ns at every seed;  4. median Fmax (seeds 1-6, lowest slow corner) >= S10 median.
Selection: W2 is chosen over W1 only if W2 passes the gate and t = c / F is lower for W2 than for W1 for SampleNTT and for CBD; otherwise W1 (if it passes the gate); if W1 fails and W2 passes, W2; if both fail, not accepted.
No tolerance. Usage: python3 scripts/select_8b.py
"""
import json
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from phase5_select_5b import parse_quartus  # noqa: E402

E8 = ROOT / "docs" / "evidence" / "phase08-keccak-stream" / "8b"
E6 = ROOT / "docs" / "evidence" / "phase06-scheduling" / "s10"
ALM_BUDGET = 12573


def load(folder, prefix, optional=False):
    rows = []
    for s in range(1, 7):
        rev = prefix + ("" if s == 1 else f"-s{s}")
        files = sorted(folder.glob(f"quartus_{rev}_*.md"))
        if not files:
            if optional:
                return None
            raise SystemExit(f"missing evidence for {rev} in {folder}")
        q = parse_quartus(files[-1])
        q["seed"] = s
        rows.append(q)
    return rows


def cycles(w):
    files = sorted(E8.glob(f"cycles_w{w}_c5_*.json"))
    if not files:
        return None
    pts = json.loads(files[-1].read_text())
    ntt = [p["cycles"] for p in pts if p["kind"] == "sample_ntt"]
    cbd = [p["cycles"] for p in pts if p["kind"] == "cbd"]
    return dict(ntt_mean=statistics.mean(ntt), ntt_n=len(ntt), cbd=sorted(set(cbd)), file=files[-1].name)


def gate(w, rows, status, ref_med):
    med = statistics.median(q["fmax"] for q in rows)
    checks = [
        ("correct (verification_status: V1-V10, both simulators, controls fail, formal, regression)", status.get("correct") == "PASS"),
        ("M10K = 0 and DSP = 0 at every seed", all(q["ram"] == 0 and q["dsp"] == 0 for q in rows)),
        (f"ALM <= {ALM_BUDGET:,} at every seed (working cap)", all(q["alm"] <= ALM_BUDGET for q in rows)),
        ("timing met at 40.000 ns at every seed", all(q["setup"] >= 0 and q["hold"] >= 0 for q in rows)),
        (f"median Fmax {med:.3f} MHz >= S10 median {ref_med:.3f} MHz", med >= ref_med),
    ]
    return med, checks


def main() -> int:
    s10 = load(E6, "S10")
    ref = statistics.median(q["fmax"] for q in s10)
    res = {}
    for w in (1, 2):
        rows = load(E8, f"SM{w}", optional=True)
        sf = E8 / f"verification_status_W{w}.json"
        if rows is None or not sf.exists():
            print(f"## W{w}: not measured (no evidence files)\n")
            continue
        status = json.loads(sf.read_text())
        med, checks = gate(w, rows, status, ref)
        cyc = cycles(w)
        res[w] = dict(rows=rows, med=med, checks=checks, ok=all(c for _, c in checks), cyc=cyc)
        print(f"## W{w}: per seed at 40.000 ns (MEASURED)")
        print("| Seed | ALM | Registers | M10K | DSP | Worst setup / hold (ns) | Timing met @ 40 ns | Fmax lowest slow corner (MHz) | Evidence |")
        print("|---|---|---|---|---|---|---|---|---|")
        for q in rows:
            print(f"| {q['seed']} | {q['alm']:,} | {q['reg']} | {q['ram']} | {q['dsp']} | {q['setup']:.3f} / {q['hold']:.3f} | {'yes' if q['setup'] >= 0 and q['hold'] >= 0 else 'no'} | {q['fmax']:.2f} | `{q['file']}` |")
        a = [q["alm"] for q in rows]
        f = [q["fmax"] for q in rows]
        r = [q["reg"] for q in rows]
        print(f"\nALM median (min-max): {statistics.median(a):,.1f} ({min(a):,}-{max(a):,}); registers {min(r)}-{max(r)}; Fmax median (min-max): {med:.3f} ({min(f):.2f}-{max(f):.2f}) MHz")
        print(f"\n### W{w} acceptance gate (test plan section 4)")
        for text, ok in checks:
            print(f"- {'PASS' if ok else 'FAIL'}: {text}")
        print(f"\n**W{w} gate result: {'PASSED' if res[w]['ok'] else 'NOT passed (no tolerance was added)'}.**\n")
        if cyc:
            print(f"Cycles (C5 top, `{cyc['file']}`; coef_ready always high): SampleNTT mean {cyc['ntt_mean']:.2f} cycles over {cyc['ntt_n']} polynomials; CBD {cyc['cbd']} cycles.\n")
        for name, pat in (("SM%d-20 (20.000 ns)" % w, f"quartus_SM{w}-20_*.md"), ("SM%d-K0 (K0 sponge)" % w, f"quartus_SM{w}-K0_*.md")):
            files = sorted(E8.glob(pat))
            if files:
                q = parse_quartus(files[-1])
                print(f"- information {name}, seed 1: ALM {q['alm']:,}, worst setup {q['setup']:.3f} ns ({'met' if q['setup'] >= 0 else 'NOT met'}), Fmax lowest slow corner {q['fmax']:.2f} MHz, `{q['file']}`")
        print()
    print(f"Reference: S10 (NTT/INTT core) Fmax median {ref:.3f} MHz over seeds 1-6 (recomputed from `docs/evidence/phase06-scheduling/s10/`).\n")
    print("## Selection W1 versus W2 (test plan section 5)")
    if 1 not in res:
        print("- W1 not measured yet.")
        return 0
    if 2 not in res:
        print(f"- W2 not measured yet. W1 gate: {'passed' if res[1]['ok'] else 'NOT passed'}.")
        return 0
    t = {}
    for w in (1, 2):
        c = res[w]["cyc"]
        if not c or len(c["cbd"]) != 1:
            print(f"- W{w}: cycle table missing or CBD count not unique; cannot apply the rule")
            return 1
        t[w] = (c["ntt_mean"] / res[w]["med"], c["cbd"][0] / res[w]["med"])
        print(f"- W{w}: t(SampleNTT) = {c['ntt_mean']:.2f} / {res[w]['med']:.3f} = {t[w][0]:.4f} us; t(CBD) = {c['cbd'][0]} / {res[w]['med']:.3f} = {t[w][1]:.4f} us")
    better = t[2][0] < t[1][0] and t[2][1] < t[1][1]
    if res[2]["ok"] and better:
        out = "W2 CHOSEN (passes the gate and t is lower than W1 for SampleNTT and for CBD)"
    elif res[1]["ok"]:
        out = "W1 stays (W2 " + ("does not pass the gate" if not res[2]["ok"] else "is not lower in t for both samplers") + ")"
    elif res[2]["ok"]:
        out = "W2 CHOSEN (W1 fails the gate, W2 passes)"
    else:
        out = "NEITHER passes the gate: 8b recorded as not accepted, the team decides"
    print(f"\n**Selection result: {out}.**")
    return 0


if __name__ == "__main__":
    sys.exit(main())
