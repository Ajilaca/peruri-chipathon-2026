#!/usr/bin/env python3
"""formal/run/run_formal_s10.py

S10 formal run (evidence/phase06/test_plan_s10.md, V5), same flow as formal/run/run_formal_phase5.py:
  A. formal/s10/ntt_core_s10_safety.sby -- properties H, O, R, A, B, C of ntt_core_s10_formal_top.sv on
     rtl/ntt/ntt_core_s10_p5.sv. Expected: PASS.
  B. Negative controls on deliberately corrupted COPIES (repository RTL never modified):
       NC-O  bank map without the XOR bit (copy of poly_mem_m10k.sv) -> property O must FAIL
       NC-A  delay model of property A shifted by one cycle  -> property A must FAIL
Control and bank-capacity properties only, not NTT/INTT arithmetic (simulation and the exhaustive / basis tests cover that).
Usage: . scripts/env.sh && python3 formal/run/run_formal_s10.py      Work directory: formal/work/s10/ (git-ignored).
"""
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import run_formal_slang as base  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent.parent  # formal/
PM = HERE / "s10"
WORK = HERE / "work" / "s10"
SBY = PM / "ntt_core_s10_safety.sby"


def main() -> int:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    base.WORK = WORK
    rows = []
    st, det, sec = base.run_sby(SBY, SBY.stem)
    rows.append(("A S10", "s10 (H, O, R, A, B, C)", "PASS", st, det, sec))
    d = WORK / "negctl_O_s10"
    mem = HERE.parent / "rtl" / "mem" / "poly_mem_m10k.sv"
    mut = d / "mutant" / "poly_mem_m10k.sv"
    mut.parent.mkdir(parents=True, exist_ok=True)
    src = mem.read_text()
    old = "f_bank = {a[1] ^ a[2] ^ a[3] ^ a[4], a[7], a[6], a[5]};"
    assert src.count(old) == 1
    mut.write_text(src.replace(old, "f_bank = {a[4], a[7], a[6], a[5]};"))
    sby = base.make_slang_sby(SBY, d, replace={"poly_mem_m10k.sv": mut})
    st, det, sec = base.run_sby(sby, d.name + "_run")
    rows.append(("B Negative control", "NC-O s10: bank map without the XOR bit (two ports on one bank)", "FAIL", st, det, sec))
    d = WORK / "negctl_A_s10"
    sby = base.make_slang_sby(SBY, d)
    s = sby.read_text()
    s2 = s.replace("--top ntt_core_s10_formal_top", "--top ntt_core_s10_formal_top -G F_SKEW=1")
    assert s2 != s
    sby.write_text(s2)
    st, det, sec = base.run_sby(sby, d.name + "_run")
    rows.append(("B Negative control", "NC-A s10: delay model of property A one cycle short", "FAIL", st, det, sec))
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
