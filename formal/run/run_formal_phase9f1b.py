#!/usr/bin/env python3
"""formal/run/run_formal_phase9f1b.py

Phase 9F S1b formal run (evidence/phase9m/batch1/9f1b/test_plan_9f1b.md V7), same flow as formal/run/run_formal_phase9c.py:
  A. formal/phase09m-optimisation/9f1b/mlkem_core3_safety.sby -- E1 (non-interference, now including the sidecar registers), S1-S7 of 9c and B1-B7 of the sidecar (one owner of the hash unit, done only when the sidecar is idle, a main write is never lost on the bus, ranges). Expected: PASS.
  C. formal/phase09m-optimisation/9f1b/mlkem_core3_cover.sby -- reachability: a sidecar digest word is written and the sidecar issues a read (depth 200); whole-program completion is covered by the simulations. Expected: PASS.
  B. Negative controls on deliberately corrupted COPIES of rtl/mlkem/mlkem_core3.sv (bounded model check, mlkem_core3_bmc.sby, depth 160; repository RTL never modified):
       NC-B3  JN advances while the job runs                                      -> B3 must FAIL
       NC-B7  the digest write of the sidecar ignores a main write in the same cycle -> B7 must FAIL
       NC-E1  the program counter advances by 2 when a data bit of the register file is set -> E1 must FAIL
Control and range properties only; values are covered by simulation. The sub-blocks are protocol stubs (formal/phase09-integration/9c/stubs_9c.sv, formal/phase09m-optimisation/9m1/stubs_9m1.sv).
Usage: . scripts/env.sh && python3 formal/run/run_formal_phase9f1b.py [all|proofs|cover]      Work directory: formal/work/phase9f1b/ (git-ignored).
"""
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import run_formal_slang as base  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent.parent  # formal/
PM = HERE / "phase09m-optimisation" / "9f1b"
MODE = sys.argv[1] if len(sys.argv) > 1 else "all"      # all | proofs (safety and controls) | cover
WORK = HERE / "work" / ("phase9f1b" if MODE == "all" else f"phase9f1b_{MODE}")
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
    sf, cv, bm = PM / "mlkem_core3_safety.sby", PM / "mlkem_core3_cover.sby", PM / "mlkem_core3_bmc.sby"
    if MODE in ("all", "cover"):
        st, det, sec = base.run_sby(cv, cv.stem, timeout=14400)
        rows.append(("C Reachability", "mlkem_core3: a sidecar digest word written and a sidecar read issued are reachable (the proof is not vacuous)", "PASS", st, det, sec))
    if MODE == "cover":
        return report(rows)
    st, det, sec = base.run_sby(sf, sf.stem)
    rows.append(("A Phase 9F S1b", "mlkem_core3 controller (E1 non-interference with the sidecar, S1-S7, B1 one hash owner, B2 done only with the sidecar idle, B3 JN waits, B4 / B5 / B7 buses, B6 counters)", "PASS", st, det, sec))
    for nm, edits, txt in (
        ("negctl_B3", [("            OpJn: if (!bg_own) begin", "            OpJn: begin")], "NC-B3: JN advances while the job runs (B3)"),
        ("negctl_B7", [("    if (!fw_en && bg_take) begin", "    if (bg_take) begin")], "NC-B7: the sidecar's digest write ignores a main write in the same cycle (B7)"),
        ("negctl_E1", [("            OpBgs: if (!bg_own) begin\n              bpc_q   <= f_bpc;", "            OpBgs: if (!bg_own) begin\n              bpc_q   <= f_bpc + 6'(rf_q[0][0]);")], "NC-E1: the job start depends on a data bit (E1 non-interference)")):
        d, sby = mutant(nm, bm, "mlkem_core3.sv", edits)
        st, det, sec = base.run_sby(sby, d.name + "_run")
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
