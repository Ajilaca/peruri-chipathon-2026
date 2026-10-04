#!/usr/bin/env python3
"""formal/run_formal_phase9i4.py

Phase 9I item 4 formal run (docs/evidence/phase09m-optimisation/9i4/test_plan_9i4.md V8), same flow as formal/run_formal_phase9f1b.py for rtl/mlkem/mlkem_core4.sv (protocol stubs of the engine variant and of the loader in formal/phase09m-optimisation/9i4/stubs_9i4.sv):
  A. mlkem_core4_safety.sby   E1 non-interference (including the interlock register and the sticky done flag), S1-S7, B1-B7 (induction)
  P. mlkem_core4_bmc.sby on the real RTL  P1 the engine is not busy in STP and SDL (bounded model check, depth 160)
  C. mlkem_core4_cover.sby   reachability (a load while the engine is busy and a slot is marked; RUNJ with the engine done)
  B. negative controls on copies: NC-JOIN4 (RUNJ does not wait) -> P1 must FAIL; NC-E1-4 (the interlock mask depends on a data bit) -> E1 must FAIL
Usage: . scripts/env.sh && python3 formal/run_formal_phase9i4.py [all|proofs|cover|retry]   (retry: only P1 and NC-E1-4 with a 4 h limit, after both timed out at 1800 s in the proofs run)      Work directory: formal/work/phase9i4/ (git-ignored).
"""
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import run_formal_slang as base  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
PM = HERE / "phase09m-optimisation" / "9i4"
MODE = sys.argv[1] if len(sys.argv) > 1 else "all"      # all | proofs (safety and controls) | cover | retry
WORK = HERE / "work" / ("phase9i4" if MODE == "all" else f"phase9i4_{MODE}")
RTL = HERE.parent / "rtl" / "mlkem"


def mutant(name, sby_src, rel, edits):
    d = WORK / name
    mut = d / "mutant" / rel
    mut.parent.mkdir(parents=True, exist_ok=True)
    src = (RTL / rel).read_text()
    for old, new in edits:
        assert src.count(old) == 1, f"{rel}: pattern {old!r} found {src.count(old)} times"
        src = src.replace(old, new)
    mut.write_text(src)
    return d, base.make_slang_sby(sby_src, d, replace={rel: mut})


def main() -> int:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    base.WORK = WORK
    rows = []
    sf, cv, bm = PM / "mlkem_core4_safety.sby", PM / "mlkem_core4_cover.sby", PM / "mlkem_core4_bmc.sby"
    if MODE in ("all", "cover"):
        st, det, sec = base.run_sby(cv, cv.stem, timeout=14400)
        rows.append(("C Reachability", "mlkem_core4: a load runs while the engine is busy and a slot is marked; RUNJ with the engine done; the earlier covers of 9f1b", "PASS", st, det, sec))
    if MODE == "cover":
        return report(rows)
    TMO = 14400 if MODE == "retry" else None      # retry: P1 and NC-E1-4 only, 4 h limit
    kw = {"timeout": TMO} if TMO else {}
    if MODE != "retry":
        st, det, sec = base.run_sby(sf, sf.stem)
        rows.append(("A Phase 9I item 4", "mlkem_core4 controller (E1 non-interference including pend_q and eng_dn_q, S1-S7, B1-B7)", "PASS", st, det, sec))
    st, det, sec = base.run_sby(bm, bm.stem + "_p1", **kw)
    rows.append(("P Bounded", "mlkem_core4: P1 no STP or SDL while the engine is busy (bounded model check, depth 160, real RTL)", "PASS", st, det, sec))
    for nm, edits, txt in (
        ("negctl_JOIN4", [("        S_RUNJ: if (eng_dn_q || eng_done) begin", "        S_RUNJ: begin")], "NC-JOIN4: RUNJ does not wait for the engine (P1)"),
        ("negctl_E1", [("              pend_q   <= f_pm;", "              pend_q   <= f_pm | 12'(rf_q[0][0]);")], "NC-E1-4: the interlock mask depends on a data bit of the register file (E1)"),
    ):
        if MODE == "retry" and nm != "negctl_E1":
            continue
        d, sby = mutant(nm, bm, "mlkem_core4.sv", edits)
        st, det, sec = base.run_sby(sby, d.name + "_run", **kw)
        rows.append(("B Negative control", txt, "FAIL", st, det, sec))
    return report(rows)


def report(rows) -> int:
    ok = True
    print("| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |")
    print("|---|---|---|---|---|---|---|")
    for grp, name, exp, st, det, sec in rows:
        good = st == exp
        ok &= good
        print(f"| {grp} | {name} | {exp} | {st} | {det} | {sec:.1f} | {'yes' if good else '**NO**'} |")
    print()
    print("ALL AS EXPECTED" if ok else "UNEXPECTED RESULT")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
