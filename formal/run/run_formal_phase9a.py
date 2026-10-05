#!/usr/bin/env python3
"""formal/run/run_formal_phase9a.py

Phase 9a formal run (evidence/phase09/9a/test_plan_9a.md, V9), same flow as formal/run/run_formal_phase8b.py:
  A. formal/phase09-integration/9a/mlkem_pack_safety.sby   -- P1-P5 of mlkem_pack_formal_top.sv. Expected: PASS.
  A. formal/phase09-integration/9a/mlkem_unpack_safety.sby -- U1-U6 of mlkem_unpack_formal_top.sv. Expected: PASS.
  B. Negative controls on deliberately corrupted COPIES (repository RTL never modified):
       NC-P1  mlkem_pack accepts a 257th coefficient                    -> P1: UNKNOWN in the proof (the violation lies beyond the induction depth 40: the base case passes, the induction step fails)
                                                                           and FAIL in BMC at depth 300 (the violation is real and reachable), as NC-B of formal/run/run_formal_slang.py
       NC-P2  mlkem_pack output byte changes while it is held           -> P2 must FAIL
       NC-U1  mlkem_unpack accepts one byte more than 32 d              -> U1: UNKNOWN in the proof and FAIL in BMC at depth 300
       NC-U6  mlkem_unpack d = 12 without the reduction (value >= q)    -> U6 must FAIL
Control and range properties only, not values (simulation against the golden covers those).
Usage: . scripts/env.sh && python3 formal/run/run_formal_phase9a.py [pack|unpack|all]      Work directory: formal/work/phase9a/ (git-ignored).
"""
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import run_formal_slang as base  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent.parent  # formal/
PM = HERE / "phase09-integration" / "9a"
WORK = HERE / "work" / "phase9a"
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


BMC300 = "[options]\nmode bmc\ndepth 300\n\n[engines]\nsmtbmc boolector\n\n"


def main() -> int:
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    base.WORK = WORK
    rows = []
    pk, up = PM / "mlkem_pack_safety.sby", PM / "mlkem_unpack_safety.sby"
    if which in ("all", "pack"):
        st, det, sec = base.run_sby(pk, pk.stem)
        rows.append(("A Phase 9a", "mlkem_pack (P1 counts, P2 held output, P3 idle, P4 bit balance, P5 pipeline count)", "PASS", st, det, sec))
        d, sby = mutant("negctl_P1", pk, "mlkem_pack.sv", [("(cin_q != 9'd256)", "(cin_q != 9'd257)")])
        st, det, sec = base.run_sby(sby, d.name + "_run")
        rows.append(("B Negative control", "NC-P1: the packer accepts a 257th coefficient (P1 count); violation beyond depth 40, so the proof must not pass", "UNKNOWN", st, det, sec))
        sby2 = base.make_slang_sby(pk, d / "bmc", replace={"mlkem_pack.sv": d / "mutant" / "mlkem_pack.sv"}, options=BMC300)
        st, det, sec = base.run_sby(sby2, d.name + "_bmc300")
        rows.append(("B Negative control", "NC-P1 again in BMC at depth 300: the 257th coefficient is reachable (P1 count)", "FAIL", st, det, sec))
        d, sby = mutant("negctl_P2", pk, "mlkem_pack.sv", [("assign byte_data_o = acc_q[7:0];", "assign byte_data_o = acc_q[7:0] ^ {7'd0, ins};")])
        st, det, sec = base.run_sby(sby, d.name + "_run")
        rows.append(("B Negative control", "NC-P2: the output byte changes when a coefficient is inserted while it is held (P2)", "FAIL", st, det, sec))
    if which in ("all", "unpack"):
        st, det, sec = base.run_sby(up, up.stem)
        rows.append(("A Phase 9a", "mlkem_unpack (U1 counts, U2 held output, U3 idle, U4 bit balance, U5 output register, U6 range)", "PASS", st, det, sec))
        d, sby = mutant("negctl_U1", up, "mlkem_unpack.sv", [("(bin_q != nbytes_q)", "(bin_q != nbytes_q + 9'd1)")])
        st, det, sec = base.run_sby(sby, d.name + "_run")
        rows.append(("B Negative control", "NC-U1: the unpacker accepts one byte more than 32 d (U1 count); violation beyond depth 40, so the proof must not pass", "UNKNOWN", st, det, sec))
        sby2 = base.make_slang_sby(up, d / "bmc", replace={"mlkem_unpack.sv": d / "mutant" / "mlkem_unpack.sv"}, options=BMC300)
        st, det, sec = base.run_sby(sby2, d.name + "_bmc300")
        rows.append(("B Negative control", "NC-U1 again in BMC at depth 300: the extra byte is reachable (U1 count)", "FAIL", st, det, sec))
        d, sby = mutant("negctl_U6", up, "mlkem_unpack.sv", [("default: dec = (x >= 12'd3329) ? (x - 12'd3329) : x;", "default: dec = x;")])
        st, det, sec = base.run_sby(sby, d.name + "_run")
        rows.append(("B Negative control", "NC-U6: d = 12 without the reduction mod q (U6 range)", "FAIL", st, det, sec))
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
