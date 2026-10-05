#!/usr/bin/env python3
"""formal/run/run_formal_phase8a.py

Phase 8a formal run (evidence/phase08/8a/test_plan_8a.md, V8), same flow as formal/run/run_formal_phase7.py:
  A. formal/phase08-keccak-stream/keccak_sponge_r2_safety.sby -- properties K1-K5 of keccak_sponge_r2_formal_top.sv. Expected: PASS.
  B. Negative controls on deliberately corrupted COPIES (repository RTL never modified):
       NC-K1  keccak_f1600_r2 with 11 cycles (rnd_q == ROUNDS / 2 - 2 ends the permutation)  -> K1 must FAIL
       NC-K4  keccak_sponge_r2 whose out_data_o depends on out_ready_i                   -> K4 must FAIL (BMC depth 40: the squeeze phase is reached after about 30 cycles, beyond the induction depth)
Control properties only, not digest values (simulation against hashlib covers those).
Usage: . scripts/env.sh && python3 formal/run/run_formal_phase8a.py      Work directory: formal/work/phase8a/ (git-ignored).
"""
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import run_formal_slang as base  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent.parent  # formal/
PM = HERE / "phase08-keccak-stream"
WORK = HERE / "work" / "phase8a"
SBY = PM / "keccak_sponge_r2_safety.sby"
RTL = HERE.parent / "rtl" / "keccak"


BMC40 = "[options]\nmode bmc\ndepth 40\n\n[engines]\nsmtbmc boolector\n\n"


def mutant(name, rel, old, new, options=None):
    d = WORK / name
    mut = d / "mutant" / rel
    mut.parent.mkdir(parents=True, exist_ok=True)
    src = (RTL / rel).read_text()
    assert src.count(old) == 1, f"{rel}: pattern found {src.count(old)} times"
    mut.write_text(src.replace(old, new))
    return d, base.make_slang_sby(SBY, d, replace={rel: mut}, options=options)


def main() -> int:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    base.WORK = WORK
    rows = []
    st, det, sec = base.run_sby(SBY, SBY.stem)
    rows.append(("A Phase 8a", "keccak_sponge_r2 + keccak_f1600_r2 (K1, K2, K3, K4, K5)", "PASS", st, det, sec))
    d, sby = mutant("negctl_K1", "keccak_f1600_r2.sv", "if (rnd_q == 4'(ROUNDS / 2 - 1)) begin", "if (rnd_q == 4'(ROUNDS / 2 - 2)) begin")
    st, det, sec = base.run_sby(sby, d.name + "_run")
    rows.append(("B Negative control", "NC-K1: 11 cycles per permutation (K1 busy length)", "FAIL", st, det, sec))
    d, sby = mutant("negctl_K4", "keccak_sponge_r2.sv", "assign out_data_o = f_rd;", "assign out_data_o = f_rd ^ {63'd0, !out_ready_i};", options=BMC40)
    st, det, sec = base.run_sby(sby, d.name + "_run")
    rows.append(("B Negative control", "NC-K4: output data depends on out_ready_i (K4 hold; BMC depth 40: the squeeze phase is reached after about 30 cycles)", "FAIL", st, det, sec))
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
