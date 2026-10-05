#!/usr/bin/env python3
"""formal/run/run_formal_phase9m3.py

Phase 9M-3 formal run (evidence/phase9m/batch1/9m3/test_plan_9m3.md V5): the Phase 9b hash wrapper proof for the K0 sponge instance (CORE_R2 = 0), same flow as formal/run/run_formal_phase9b.py. (Phase 9b plan, V8), same flow as formal/run/run_formal_phase9a.py:
  A. formal/phase09m-optimisation/9m3/mlkem_hash_k0_safety.sby -- H1-H5 of mlkem_hash_k0_formal_top.sv (mlkem_hash with CORE_R2 = 0; the K0 sponge is replaced by the protocol stub keccak_sponge_stub.sv). Expected: PASS.
  C. Reachability: formal/phase09m-optimisation/9m3/mlkem_hash_k0_cover.sby (cover mode: the covered states must all be reached). Expected: PASS.
  B. Negative controls on deliberately corrupted COPIES (repository RTL never modified):
       NC-H1  mlkem_hash: G stops after 4 digest words (last_idx always 3)     -> H1 must FAIL
       NC-H5  mlkem_hash: J never stops the squeeze (sp_stop = 0)             -> H5 must FAIL
Control and result properties only, not digest values (simulation against hashlib covers those). The comparison module is independent of the sponge and is not rerun here.
Usage: . scripts/env.sh && python3 formal/run/run_formal_phase9m3.py [hash|all]      Work directory: formal/work/phase9m3/ (git-ignored).
"""
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import run_formal_slang as base  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent.parent  # formal/
PM = HERE / "phase09m-optimisation" / "9m3"
WORK = HERE / "work" / "phase9m3"
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
    hs = PM / "mlkem_hash_k0_safety.sby"
    if which in ("all", "hash"):
        hc = PM / "mlkem_hash_k0_cover.sby"
        st, det, sec = base.run_sby(hc, hc.stem)
        rows.append(("C Reachability", "mlkem_hash (K0 stub): a digest word after 3 accepted words and done_o for H, G and J are reachable (the proof is not vacuous)", "PASS", st, det, sec))
        st, det, sec = base.run_sby(hs, hs.stem)
        rows.append(("A Phase 9M-3", "mlkem_hash with the K0 stub (H1 digest word count, H2 done, H3 held word, H4 idle, H5 sponge idle after the last word)", "PASS", st, det, sec))
        for nm, edits, txt in (("negctl_H1", [("wire [3:0]  last_idx = is_g ? 4'd7 : 4'd3;", "wire [3:0]  last_idx = 4'd3;")], "NC-H1: G stops after 4 digest words (H1 last word)"),
                               ("negctl_H5", [("wire   sp_stop     = take && last_word && is_j;", "wire   sp_stop     = 1'b0;")], "NC-H5: J never stops the squeeze (H5 sponge idle)")):
            d, sby = mutant(nm, hs, "mlkem_hash.sv", edits)
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
