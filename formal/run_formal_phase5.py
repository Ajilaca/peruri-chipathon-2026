#!/usr/bin/env python3
"""formal/run_formal_phase5.py

Phase 5 formal run (docs/evidence/phase05-arith/test_plan.md, V8), same flow as formal/run_formal_phase4.py
(yosys-slang frontend, `memory_map -rom-only`):

  A. formal/phase05-arith/ntt_core_c4<x>_safety.sby -- properties H, O, R, A, B, C of ntt_core_c4_formal_top.sv
     on the Phase 5 Quartus wrappers. Expected: PASS.
  B. Negative controls on deliberately corrupted COPIES (the repository RTL is never modified), as in Phase 4:
       NC-O  bank_map_rom copy with one wrong bank        -> property O must FAIL
       NC-A  delay model of property A shifted by one cycle -> property A must FAIL

These proofs cover control and bank-capacity properties only, not NTT/INTT arithmetic or memory data
(simulation and the exhaustive reducer test cover those).

Usage: . scripts/env.sh && python3 formal/run_formal_phase5.py [c4a ... | lazy]   (default: all wrappers + lazy)
Work directories: formal/work/phase05/ (git-ignored). Exit code 0 only if every result is as expected.
"""
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import run_formal_slang as base  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
P5 = HERE / "phase05-arith"
WORK = HERE / "work" / "phase05"
WRAPPERS = {"c4a": 0, "c4b_b": 1, "c4b_m": 2, "c4c": 3}


def variant(name: str, tag: str, *, replace=None, extra_g=None) -> pathlib.Path:
    sby = base.make_slang_sby(P5 / f"ntt_core_{name}_safety.sby", WORK / tag, replace=replace)
    if extra_g:
        s = sby.read_text()
        v = WRAPPERS[name]
        s2 = s.replace(f"-G V={v}", f"-G V={v} -G {extra_g}")
        assert s2 != s
        sby.write_text(s2)
    return sby


def lazy_bounds():
    """5c (ADR 0014 §3): value bounds of rtl/arith/lazy_bfly_io.sv, plus a negative control on a copy whose INTT output
    does not reduce the lazy side value (must FAIL)."""
    rows = []
    sby = P5 / "lazy_bfly_io_bounds.sby"
    st, det, sec = base.run_sby(sby, sby.stem)
    rows.append(("A Phase 5c", "lazy_bfly_io bounds (P1-P3)", "PASS", st, det, sec))
    d = WORK / "negctl_lazy_noreduce"
    src = (HERE.parent / "rtl" / "arith" / "lazy_bfly_io.sv").read_text()
    old = "      a_o = side_red[CW-1:0];"
    assert src.count(old) == 1
    (d / "mutant").mkdir(parents=True, exist_ok=True)
    (d / "mutant" / "lazy_bfly_io.sv").write_text(src.replace(old, "      a_o = side_d_i[CW-1:0];"))
    sby = base.make_slang_sby(P5 / "lazy_bfly_io_bounds.sby", d, replace={"lazy_bfly_io.sv": d / "mutant" / "lazy_bfly_io.sv"})
    st, det, sec = base.run_sby(sby, d.name + "_run")
    rows.append(("B Negative control", "NC-L: INTT output side value not reduced", "FAIL", st, det, sec))
    return rows


def main(names) -> int:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    base.WORK = WORK
    rows = []
    for name in [n for n in names if n in WRAPPERS]:
        sby = P5 / f"ntt_core_{name}_safety.sby"
        st, det, sec = base.run_sby(sby, sby.stem)
        rows.append(("A Phase 5", f"{name} (H, O, R, A, B, C)", "PASS", st, det, sec))
        d = WORK / f"negctl_O_{name}"
        what = base.corrupt_bank_map(8, 128, d / "mutant" / "bank_map_rom.sv")
        sby = variant(name, d.name, replace={"bank_map_rom.sv": d / "mutant" / "bank_map_rom.sv"})
        st, det, sec = base.run_sby(sby, d.name + "_run")
        rows.append(("B Negative control", f"NC-O {name}: {what}", "FAIL", st, det, sec))
        sby = variant(name, f"negctl_A_{name}", extra_g="F_SKEW=1")
        st, det, sec = base.run_sby(sby, f"negctl_A_{name}_run")
        rows.append(("B Negative control", f"NC-A {name}: delay model of property A one cycle short", "FAIL",
                     st, det, sec))
    if not names or "lazy" in names or set(names) == set(WRAPPERS):
        rows += lazy_bounds()
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
    sys.exit(main(sys.argv[1:] or list(WRAPPERS)))
