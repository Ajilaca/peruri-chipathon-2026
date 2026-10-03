#!/usr/bin/env python3
"""formal/run_formal_phase7.py

Phase 7 formal run (docs/evidence/phase07-keccak/test_plan.md, V8), same flow as formal/run_formal_s10.py:
  A. formal/phase07-keccak/keccak_sponge_safety.sby -- properties K1-K5 of keccak_sponge_formal_top.sv. Expected: PASS.
  B. Negative controls on deliberately corrupted COPIES (repository RTL never modified):
       NC-K1  keccak_f1600 with 23 rounds (rnd_q == ROUNDS - 2 ends the permutation)  -> K1 must FAIL
       NC-K4  keccak_sponge whose out_data_o depends on out_ready_i                   -> K4 must FAIL (BMC depth 40: the squeeze phase is reached after about 30 cycles, beyond the induction depth)
Control properties only, not digest values (simulation against hashlib covers those).
Usage: . scripts/env.sh && python3 formal/run_formal_phase7.py      Work directory: formal/work/phase7/ (git-ignored).
"""
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import run_formal_slang as base  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
PM = HERE / "phase07-keccak"
WORK = HERE / "work" / "phase7"
SBY = PM / "keccak_sponge_safety.sby"
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
    rows.append(("A Phase 7", "keccak_sponge + keccak_f1600 (K1, K2, K3, K4, K5)", "PASS", st, det, sec))
    d, sby = mutant("negctl_K1", "keccak_f1600.sv", "if (rnd_q == 5'(ROUNDS - 1)) begin", "if (rnd_q == 5'(ROUNDS - 2)) begin")
    st, det, sec = base.run_sby(sby, d.name + "_run")
    rows.append(("B Negative control", "NC-K1: 23 rounds per permutation (K1 busy length)", "FAIL", st, det, sec))
    d, sby = mutant("negctl_K4", "keccak_sponge.sv", "assign out_data_o = f_rd;", "assign out_data_o = f_rd ^ {63'd0, !out_ready_i};", options=BMC40)
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
