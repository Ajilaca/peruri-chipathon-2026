#!/usr/bin/env python3
"""formal/run/run_formal_phase4.py

Phase 4 formal run (evidence/phase04/test_plan.md, V9), same flow as
formal/run/run_formal_slang.py (yosys-slang frontend, `memory_map -rom-only`):

  A. formal/phase04-pipeline/ntt_core_c3_p{2,4,6}_safety.sby -- properties H, O, R, A, B, C of
     ntt_core_c3_formal_top.sv on the three Quartus wrappers. Expected: PASS.
  B. Negative controls on deliberately corrupted COPIES (the repository RTL is never modified); each
     targets one property, so that a PASS in (A) is shown not to be vacuous:
       NC-O  bank_map_rom copy with one wrong bank            -> property O must FAIL (base case)
       NC-A  delay model of property A shifted by one cycle    -> property A must FAIL (base case)
       NC-B  ntt_core_c3 copy whose drain is one cycle short   -> not provable (induction fails; the
             violation is about 113 cycles from reset, beyond the base-case depth) and FAIL in a BMC
             deep enough to reach it
       NC-C  ntt_core_c3 copy whose scaling pass can repeat an address -> not provable (UNKNOWN)

These proofs cover control and bank-capacity properties only. They do NOT prove NTT/INTT bit-exactness
or memory data integrity (simulation covers those).

Usage: . scripts/env.sh && python3 formal/run/run_formal_phase4.py
Work directories: formal/work/phase04/ (git-ignored). Exit code 0 only if every result is as expected.
"""
import pathlib
import re
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import run_formal_slang as base  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent.parent  # formal/
ROOT = HERE.parent
P4 = HERE / "phase04-pipeline"
WORK = HERE / "work" / "phase04"


def mutate(src: pathlib.Path, dst: pathlib.Path, old: str, new: str) -> None:
    text = src.read_text()
    assert text.count(old) == 1, f"{src.name}: expected exactly one occurrence of {old!r}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text.replace(old, new))


def variant(p: int, tag: str, *, replace=None, options=None, extra_g=None) -> pathlib.Path:
    """A copy of the P=<p> .sby in WORK with absolute paths, optional file substitution / options / -G."""
    d = WORK / tag
    sby = base.make_slang_sby(P4 / f"ntt_core_c3_p{p}_safety.sby", d, replace=replace, options=options)
    if extra_g:
        s = sby.read_text()
        s2 = s.replace(f"-G P={p}", f"-G P={p} -G {extra_g}")
        assert s2 != s
        sby.write_text(s2)
    return sby


def main() -> int:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)
    base.WORK = WORK
    rows = []

    for p in (2, 4, 6):
        sby = P4 / f"ntt_core_c3_p{p}_safety.sby"
        st, det, sec = base.run_sby(sby, sby.stem)
        rows.append(("A Phase 4", f"C3 P={p} (H, O, R, A, B, C)", "PASS", st, det, sec))

    for p in (2, 6):
        d = WORK / f"negctl_O_p{p}"
        what = base.corrupt_bank_map(8, 128, d / "mutant" / "bank_map_rom.sv")
        sby = variant(p, d.name, replace={"bank_map_rom.sv": d / "mutant" / "bank_map_rom.sv"})
        st, det, sec = base.run_sby(sby, d.name + "_run")
        rows.append(("B Negative control", f"NC-O P={p}: {what}", "FAIL", st, det, sec))

    sby = variant(2, "negctl_A_p2", extra_g="F_SKEW=1")
    st, det, sec = base.run_sby(sby, "negctl_A_p2_run")
    rows.append(("B Negative control", "NC-A P=2: delay model of property A one cycle short", "FAIL", st, det, sec))

    d = WORK / "negctl_B_p2"
    mutate(ROOT / "rtl/ntt/ntt_core_c3.sv", d / "mutant" / "ntt_core_c3.sv",
           "if (drain_q == DW'(Pipe - 1)) state_d = S_DONE;", "if (drain_q == DW'(Pipe - 2)) state_d = S_DONE;")
    sby = variant(2, d.name, replace={"ntt_core_c3.sv": d / "mutant" / "ntt_core_c3.sv"})
    st, det, sec = base.run_sby(sby, d.name + "_run")
    rows.append(("B Negative control", "NC-B P=2: drain one cycle short (induction must fail)", "UNKNOWN", st, det, sec))
    bmc = "[options]\nmode bmc\ndepth 125\n\n[engines]\nsmtbmc boolector\n\n"
    sby = variant(2, "negctl_B_p2_bmc125", replace={"ntt_core_c3.sv": d / "mutant" / "ntt_core_c3.sv"}, options=bmc)
    st, det, sec = base.run_sby(sby, "negctl_B_p2_bmc125_run", timeout=3600)
    rows.append(("B Negative control", "NC-B/bmc125 P=2: same mutant, BMC depth 125 (violation reachable)", "FAIL", st, det, sec))

    d = WORK / "negctl_C_p2"
    mutate(ROOT / "rtl/ntt/ntt_core_c3.sv", d / "mutant" / "ntt_core_c3.sv",
           "scale_addr_d = scale_addr_q + 8'd1;", "scale_addr_d = scale_addr_q + {7'd0, scale_addr_q[1]};")
    sby = variant(2, d.name, replace={"ntt_core_c3.sv": d / "mutant" / "ntt_core_c3.sv"})
    st, det, sec = base.run_sby(sby, d.name + "_run")
    rows.append(("B Negative control", "NC-C P=2: scaling pass may repeat an address (induction must fail)", "UNKNOWN", st, det, sec))

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
