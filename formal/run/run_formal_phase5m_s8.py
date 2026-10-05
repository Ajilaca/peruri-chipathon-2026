#!/usr/bin/env python3
"""formal/run/run_formal_phase5m_s8.py

Phase 5M step S8 formal run (evidence/phase05m/test_plan_s8.md, V5), same flow as formal/run/run_formal_phase5.py:
  A. formal/phase05m-memsched/ntt_core_s8_safety.sby -- properties H, O, R, A, B, C of ntt_core_s8_formal_top.sv on
     rtl/ntt/ntt_core_s8_p8.sv. Expected: PASS.
  B. Negative controls on deliberately corrupted COPIES (repository RTL never modified):
       NC-O  bank_map_rom copy with one wrong bank          -> property O must FAIL
       NC-A  delay model of property A shifted by one cycle  -> property A must FAIL
Control and bank-capacity properties only, not NTT/INTT arithmetic (simulation and the exhaustive / basis tests cover that).
Usage: . scripts/env.sh && python3 formal/run/run_formal_phase5m_s8.py      Work directory: formal/work/phase05m_s8/ (git-ignored).
"""
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import run_formal_slang as base  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent.parent  # formal/
PM = HERE / "phase05m-memsched"
WORK = HERE / "work" / "phase05m_s8"
SBY = PM / "ntt_core_s8_safety.sby"


def main() -> int:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    base.WORK = WORK
    rows = []
    st, det, sec = base.run_sby(SBY, SBY.stem)
    rows.append(("A Phase 5M S8", "s8 (H, O, R, A, B, C)", "PASS", st, det, sec))
    d = WORK / "negctl_O_s8"
    what = base.corrupt_bank_map(8, 128, d / "mutant" / "bank_map_rom.sv")
    sby = base.make_slang_sby(SBY, d, replace={"bank_map_rom.sv": d / "mutant" / "bank_map_rom.sv"})
    st, det, sec = base.run_sby(sby, d.name + "_run")
    rows.append(("B Negative control", f"NC-O s8: {what}", "FAIL", st, det, sec))
    d = WORK / "negctl_A_s8"
    sby = base.make_slang_sby(SBY, d)
    s = sby.read_text()
    s2 = s.replace("--top ntt_core_s8_formal_top", "--top ntt_core_s8_formal_top -G F_SKEW=1")
    assert s2 != s
    sby.write_text(s2)
    st, det, sec = base.run_sby(sby, d.name + "_run")
    rows.append(("B Negative control", "NC-A s8: delay model of property A one cycle short", "FAIL", st, det, sec))
    ok = True
    print("| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |")
    print("|---|---|---|---|---|---|---|")
    for grp, name, exp, st, det, sec in rows:
        good = st == exp
        ok &= good
        print(f"| {grp} | {name} | {exp} | {st} | {det} | {sec:.1f} | {'yes' if good else '**NO**'} |")
    print()
    print(f"OVERALL: {'all results as expected' if ok else 'MISMATCH -- see table'} "
          f"({sum(1 for r in rows if r[3] == r[2])}/{len(rows)})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
