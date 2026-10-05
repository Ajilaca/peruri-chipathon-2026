#!/usr/bin/env python3
"""formal/run/run_formal_phase8b.py

Phase 8b formal run (evidence/phase08/8b/test_plan_8b.md, V9), same flow as formal/run/run_formal_phase8a.py:
  A. formal/phase08-keccak-stream/8b/sample_ntt_core_safety.sby -- S1-S5 of sample_ntt_core_formal_top.sv. Expected: PASS.
  A. formal/phase08-keccak-stream/8b/cbd2_core_safety.sby       -- S1-S5 of cbd2_core_formal_top.sv (at most 16 words taken). Expected: PASS.
  A. The same two proofs with OUTW = 2 (stage W2): sample_ntt_core_safety_w2.sby (S1-S6, S6 = the carry) and cbd2_core_safety_w2.sby.
  B. Negative controls on deliberately corrupted COPIES (repository RTL never modified), W1 and W2:
       NC-S1  sample_ntt_core accepts d <= q (the value 3329 reaches the output)           -> S1 must FAIL
       NC-S2  sample_ntt_core counts coefficients from 1 instead of 0 (the count relation behind S2: last on the 256th) -> S2 must FAIL
Control and range properties only, not coefficient values (simulation against the golden covers those).
Usage: . scripts/env.sh && python3 formal/run/run_formal_phase8b.py [1|2|all]      Work directory: formal/work/phase8b/ (git-ignored).
"""
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import run_formal_slang as base  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent.parent  # formal/
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


# start-of-run counter reset, as spelled in each stage's branch of rtl/sample/sample_ntt_core.sv (the indentation differs)
S2_W1 = ("busy_q  <= 1'b1;\n          fin_q   <= 1'b0;\n          n_q     <= 9'd0;", "busy_q  <= 1'b1;\n          fin_q   <= 1'b0;\n          n_q     <= 9'd1;")
S2_W2 = ("busy_q  <= 1'b1;\n            fin_q   <= 1'b0;\n            n_q     <= 9'd0;", "busy_q  <= 1'b1;\n            fin_q   <= 1'b0;\n            n_q     <= 9'd1;")
LT = [("wire        acc1 = (nd1 < QC);", "wire        acc1 = (nd1 <= QC);"), ("wire        acc2 = (nd2 < QC);", "wire        acc2 = (nd2 <= QC);")]


def main() -> int:
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    base.WORK = WORK
    rows = []
    for w, sfx in ((1, ""), (2, "_w2")):
        if which not in ("all", str(w)):
            continue
        ntt, cbd = PM / f"sample_ntt_core_safety{sfx}.sby", PM / f"cbd2_core_safety{sfx}.sby"
        st, det, sec = base.run_sby(ntt, ntt.stem)
        rows.append((f"A Phase 8b W{w}", f"sample_ntt_core OUTW={w} (S1, S2, S3, S4, S5" + (", S6 carry)" if w == 2 else ")"), "PASS", st, det, sec))
        st, det, sec = base.run_sby(cbd, cbd.stem)
        rows.append((f"A Phase 8b W{w}", f"cbd2_core OUTW={w} (S1, S2 with at most 16 words, S3, S4, S5)", "PASS", st, det, sec))
        d, sby = mutant(f"negctl_S1_w{w}", ntt, "sample_ntt_core.sv", LT)
        st, det, sec = base.run_sby(sby, d.name + "_run")
        rows.append((f"B Negative control W{w}", f"NC-S1: a candidate equal to q is accepted (S1 range), OUTW={w}", "FAIL", st, det, sec))
        d, sby = mutant(f"negctl_S2_w{w}", ntt, "sample_ntt_core.sv", [S2_W1 if w == 1 else S2_W2])
        st, det, sec = base.run_sby(sby, d.name + "_run")
        rows.append((f"B Negative control W{w}", f"NC-S2: the coefficient count starts at 1 (S2 count relation: last on the last beat), OUTW={w}", "FAIL", st, det, sec))
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
