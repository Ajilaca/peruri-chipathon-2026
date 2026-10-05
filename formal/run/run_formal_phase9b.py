#!/usr/bin/env python3
"""formal/run/run_formal_phase9b.py

Phase 9b formal run (evidence/phase09/9b/test_plan_9b.md, V8), same flow as formal/run/run_formal_phase9a.py:
  A. formal/phase09-integration/9b/mlkem_hash_safety.sby   -- H1-H5 of mlkem_hash_formal_top.sv (C5 sponge inside). Expected: PASS.
  A. formal/phase09-integration/9b/mlkem_fo_cmp_safety.sby -- F1-F4 of mlkem_fo_cmp_formal_top.sv (WORDS = 8). Expected: PASS.
  C. Reachability: formal/phase09-integration/9b/mlkem_hash_cover.sby and mlkem_fo_cmp_cover.sby (cover mode: the covered states must all be reached). Expected: PASS.
  B. Negative controls on deliberately corrupted COPIES (repository RTL never modified):
       NC-H1  mlkem_hash: G stops after 4 digest words (last_idx always 3)     -> H1 must FAIL
       NC-H5  mlkem_hash: J never stops the squeeze (sp_stop = 0)             -> H5 must FAIL
       NC-F3  mlkem_fo_cmp: the compare looks at the low 32 bits only         -> the accumulator invariant / F3 must FAIL
       NC-F4  mlkem_fo_cmp: the key select is inverted                        -> F4 must FAIL
       NC-F1  mlkem_fo_cmp: the compare ends at the first difference          -> F1 must FAIL
Control and result properties only, not digest values (simulation against hashlib covers those).
Usage: . scripts/env.sh && python3 formal/run/run_formal_phase9b.py [hash|fo|all]      Work directory: formal/work/phase9b/ (git-ignored).
"""
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import run_formal_slang as base  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent.parent  # formal/
PM = HERE / "phase09-integration" / "9b"
WORK = HERE / "work" / "phase9b"
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
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    base.WORK = WORK
    rows = []
    hs, fo = PM / "mlkem_hash_safety.sby", PM / "mlkem_fo_cmp_safety.sby"
    if which in ("all", "hash"):
        hc = PM / "mlkem_hash_cover.sby"
        st, det, sec = base.run_sby(hc, hc.stem)
        rows.append(("C Reachability", "mlkem_hash: a digest word after 3 accepted words and done_o for H, G and J are reachable (the proof is not vacuous)", "PASS", st, det, sec))
        st, det, sec = base.run_sby(hs, hs.stem)
        rows.append(("A Phase 9b", "mlkem_hash (H1 digest word count, H2 done, H3 held word, H4 idle, H5 sponge idle after the last word)", "PASS", st, det, sec))
        for nm, edits, txt in (("negctl_H1", [("wire [3:0]  last_idx = is_g ? 4'd7 : 4'd3;", "wire [3:0]  last_idx = 4'd3;")], "NC-H1: G stops after 4 digest words (H1 last word)"),
                               ("negctl_H5", [("wire   sp_stop     = take && last_word && is_j;", "wire   sp_stop     = 1'b0;")], "NC-H5: J never stops the squeeze (H5 sponge idle)")):
            d, sby = mutant(nm, hs, "mlkem_hash.sv", edits)
            st, det, sec = base.run_sby(sby, d.name + "_run")
            rows.append(("B Negative control", txt, "FAIL", st, det, sec))
    if which in ("all", "fo"):
        fc = PM / "mlkem_fo_cmp_cover.sby"
        st, det, sec = base.run_sby(fc, fc.stem)
        rows.append(("C Reachability", "mlkem_fo_cmp: done_o with neq_o = 1 and with neq_o = 0 are reachable (the proof is not vacuous)", "PASS", st, det, sec))
        st, det, sec = base.run_sby(fo, fo.stem)
        rows.append(("A Phase 9b", "mlkem_fo_cmp (F1 beats and done, F2 held result, F3 accumulator and neq, F4 mask select)", "PASS", st, det, sec))
        for nm, edits, txt in (("negctl_F3", [("wire [63:0]  diff_next = diff_q | (a_data_i ^ b_data_i);", "wire [63:0]  diff_next = diff_q | ((a_data_i ^ b_data_i) & 64'h0000_0000_FFFF_FFFF);")], "NC-F3: the compare looks at the low 32 bits only (F3 accumulator)"),
                               ("negctl_F4", [("k_q   <= (kgood_i & ~mask) | (kbad_i & mask);", "k_q   <= (kgood_i & mask) | (kbad_i & ~mask);")], "NC-F4: the key select is inverted (F4)"),
                               ("negctl_F1", [("wire last    = take && (cnt_q == CNTW'(WORDS - 1));", "wire last    = take && ((cnt_q == CNTW'(WORDS - 1)) || (|(diff_q | (a_data_i ^ b_data_i))));")], "NC-F1: the compare ends at the first difference (F1 done after exactly WORDS beats)")):
            d, sby = mutant(nm, fo, "mlkem_fo_cmp.sv", edits)
            st, det, sec = base.run_sby(sby, d.name + "_run")
            rows.append(("B Negative control", txt, "FAIL", st, det, sec))
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
