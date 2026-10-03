#!/usr/bin/env python3
"""formal/run_formal_phase6.py

Phase 6 V7 (docs/evidence/phase06-scheduling/test_plan.md), same flow as formal/run_formal_phase5m_s7.py:
  A. formal/phase06-scheduling/kpke_sched_safety.sby -- properties H, T, C, R. Expected: PASS.
  B. Negative control on a deliberately corrupted COPY of rtl/sched/kpke_sched.sv (repository RTL never modified):
       NC-T  the testbench write enable reaches the store also while busy -> property T must FAIL
Usage: . scripts/env.sh && python3 formal/run_formal_phase6.py      Work directory: formal/work/phase06/ (git-ignored).
"""
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import run_formal_slang as base  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
WORK = HERE / "work" / "phase06"
SBY = HERE / "phase06-scheduling" / "kpke_sched_safety.sby"
RTL = HERE.parent / "rtl" / "sched" / "kpke_sched.sv"


def main() -> int:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    base.WORK = WORK
    rows = []
    st, det, sec = base.run_sby(SBY, SBY.stem)
    rows.append(("A Phase 6", "kpke_sched (H, T, C, R)", "PASS", st, det, sec))
    d = WORK / "negctl_T"
    m = d / "mutant" / "kpke_sched.sv"
    m.parent.mkdir(parents=True, exist_ok=True)
    t = RTL.read_text()
    old = "    end else if (unl_wr) begin"
    assert t.count(old) == 1
    m.write_text(t.replace(old, "    end else if (tb_we_i) begin\n      we_e = 1'b1;\n" + old.replace("    end else if", "    end\n    if")))
    sby = base.make_slang_sby(SBY, d, replace={"kpke_sched.sv": m})
    st, det, sec = base.run_sby(sby, d.name + "_run")
    rows.append(("B Negative control", "NC-T: testbench write reaches the store while busy", "FAIL", st, det, sec))
    ok = True
    print("| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |")
    print("|---|---|---|---|---|---|---|")
    for grp, name, exp, st, det, sec in rows:
        good = st == exp
        ok &= good
        print(f"| {grp} | {name} | {exp} | {st} | {det} | {sec:.1f} | {'yes' if good else '**NO**'} |")
    print()
    print(f"OVERALL: {'all results as expected' if ok else 'MISMATCH -- see table'} ({sum(1 for r in rows if r[3] == r[2])}/{len(rows)})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
