#!/usr/bin/env python3
"""formal/run_formal_phase9c.py

Phase 9c formal run (docs/evidence/phase09-integration/9c/test_plan_9c.md, Amendment A2), same flow as formal/run_formal_phase9b.py:
  A. formal/phase09-integration/9c/mlkem_core_safety.sby -- E1 (non-interference of the control: two copies of the controller with different data and the same handshakes keep identical control state), S1-S7 of mlkem_core_formal_top.sv. Expected: PASS.
  C. formal/phase09-integration/9c/mlkem_core_cover.sby -- the covered states (KeyGen and Encaps complete, a digest word is written) are reachable (depth 260). Expected: PASS. (mlkem_core_cover_deep.sby, depth 480, is a separate long run: Decaps done and CMPK;
     run it with `python3 formal/run_formal_phase9c.py deep`.)
  B. Negative controls on deliberately corrupted COPIES of rtl/mlkem/mlkem_core.sv (repository RTL never modified):
       NC-E1  the program counter advances by 2 when a data bit of the register file is set (data-dependent control) -> E1 must FAIL
       NC-S3  a host write is accepted in the state LDP (while busy)                                             -> S3 must FAIL
       NC-S4  the store task is started together with the load task                                              -> S4 must FAIL
Control and range properties only; values are covered by simulation. The sub-blocks are protocol stubs (formal/phase09-integration/9c/stubs_9c.sv).
Usage: . scripts/env.sh && python3 formal/run_formal_phase9c.py [all|deep]      Work directory: formal/work/phase9c/ (git-ignored).
"""
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import run_formal_slang as base  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
PM = HERE / "phase09-integration" / "9c"
WORK = HERE / "work" / "phase9c"
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
    sf, cv, dp = PM / "mlkem_core_safety.sby", PM / "mlkem_core_cover.sby", PM / "mlkem_core_cover_deep.sby"
    if which == "deep":
        st, det, sec = base.run_sby(dp, dp.stem, timeout=14400)
        rows.append(("C Reachability (deep)", "mlkem_core: Decaps done and the state CMPK are reachable (depth 480)", "PASS", st, det, sec))
    else:
        st, det, sec = base.run_sby(cv, cv.stem, timeout=7200)
        rows.append(("C Reachability", "mlkem_core: KeyGen done, Encaps done and a digest word written are reachable (the proof is not vacuous)", "PASS", st, det, sec))
        st, det, sec = base.run_sby(sf, sf.stem)
        rows.append(("A Phase 9c", "mlkem_core controller (E1 non-interference, S1 ranges, S2 busy / done, S3 no host write while busy, S4 strobes, S5 engine ports, S6 addresses, S7 counters)", "PASS", st, det, sec))
        for nm, edits, txt in (
            ("negctl_E1", [("pc_q    <= pc_q + 6'd1;\n              state_q <= S_FETCH;\n            end\n            OpHfd: begin", "pc_q    <= pc_q + 6'd1 + 6'(rf_q[0][0]);\n              state_q <= S_FETCH;\n            end\n            OpHfd: begin")],
             "NC-E1: the program counter depends on a data bit (E1 non-interference)"),
            ("negctl_S3", [("      S_STP: begin\n        wr_en   = st_wr_en;", "      S_LDP: begin\n        wr_en   = h_we_i;\n        wr_rgn  = h_addr_i[11:10];\n        wr_addr = h_addr_i[8:0];\n        wr_data = h_wdata_i;\n      end\n      S_STP: begin\n        wr_en   = st_wr_en;")],
             "NC-S3: a host write is accepted while busy, in the state LDP (S3)"),
            ("negctl_S4", [("assign st_start = disp && (opc == OpStp);", "assign st_start = disp && (opc == OpStp || opc == OpLdp);")],
             "NC-S4: the store task starts together with the load task (S4)")):
            d, sby = mutant(nm, sf, "mlkem_core.sv", edits)
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
