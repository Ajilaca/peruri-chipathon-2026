#!/usr/bin/env python3
"""formal/run_formal_phase8b.py

Phase 8b formal run (docs/evidence/phase08-keccak-stream/8b/test_plan_8b.md, V9), same flow as formal/run_formal_phase8a.py:
  A. formal/phase08-keccak-stream/8b/sample_ntt_core_safety.sby -- S1-S5 of sample_ntt_core_formal_top.sv. Expected: PASS.
  A. formal/phase08-keccak-stream/8b/cbd2_core_safety.sby       -- S1-S5 of cbd2_core_formal_top.sv (at most 16 words taken). Expected: PASS.
  B. Negative controls on deliberately corrupted COPIES (repository RTL never modified):
       NC-S1  sample_ntt_core accepts d <= q (the value 3329 reaches the output)           -> S1 must FAIL
       NC-S2  sample_ntt_core counts coefficients from 1 instead of 0 (the count relation behind S2: last on the 256th) -> S2 must FAIL
Control and range properties only, not coefficient values (simulation against the golden covers those).
Usage: . scripts/env.sh && python3 formal/run_formal_phase8b.py      Work directory: formal/work/phase8b/ (git-ignored).
"""
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import run_formal_slang as base  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
PM = HERE / "phase08-keccak-stream" / "8b"
WORK = HERE / "work" / "phase8b"
RTL = HERE.parent / "rtl" / "sample"


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
    ntt, cbd = PM / "sample_ntt_core_safety.sby", PM / "cbd2_core_safety.sby"
    st, det, sec = base.run_sby(ntt, ntt.stem)
    rows.append(("A Phase 8b", "sample_ntt_core (S1, S2, S3, S4, S5)", "PASS", st, det, sec))
    st, det, sec = base.run_sby(cbd, cbd.stem)
    rows.append(("A Phase 8b", "cbd2_core (S1, S2 with at most 16 words, S3, S4, S5)", "PASS", st, det, sec))
    d, sby = mutant("negctl_S1", ntt, "sample_ntt_core.sv", [("a1_q    <= (nd1 < Q);", "a1_q    <= (nd1 <= Q);"), ("a2_q    <= (nd2 < Q);", "a2_q    <= (nd2 <= Q);")])
    st, det, sec = base.run_sby(sby, d.name + "_run")
    rows.append(("B Negative control", "NC-S1: a candidate equal to q is accepted (S1 range)", "FAIL", st, det, sec))
    d, sby = mutant("negctl_S2", ntt, "sample_ntt_core.sv", [("busy_q  <= 1'b1;\n          fin_q   <= 1'b0;\n          n_q     <= 9'd0;", "busy_q  <= 1'b1;\n          fin_q   <= 1'b0;\n          n_q     <= 9'd1;")])
    st, det, sec = base.run_sby(sby, d.name + "_run")
    rows.append(("B Negative control", "NC-S2: the coefficient count starts at 1 (S2 count relation: last on the 256th)", "FAIL", st, det, sec))
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
