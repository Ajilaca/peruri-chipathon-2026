#!/usr/bin/env python3
"""formal/run/run_formal_phase9f1.py

Phase 9F S1 formal run (evidence/phase9m/batch1/9f1/test_plan_9f1.md, V6): the Phase 8d proof (formal/run/run_formal_phase8d.py) with the sequencer instantiated at CORE_R2 = 0, same flow:
  A. 8d/kpke_sched_smp_safety_overlap.sby -- F1-F5 of ../8c/kpke_sched_smp_formal_top.sv with STREAM_A = 1 and OVERLAP = 1 (arbitration, non-blocking SMPN, WAIT). Expected: PASS.
  B. Negative control on a deliberately corrupted COPY (repository RTL never modified):
       NC-F2  the seed registers are written even while the sequencer is busy (gate `idle_st` removed) -> F2 must FAIL
The NTT core is abstracted and the sampler is replaced by the protocol stub formal/phase08-keccak-stream/8c/keccak_sampler_stub.sv; control properties only, not values.
Usage: . scripts/env.sh && python3 formal/run/run_formal_phase9f1.py      Work directory: formal/work/phase9f1/ (git-ignored).
"""
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import run_formal_slang as base  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent.parent  # formal/
PM = HERE / "phase09m-optimisation" / "9f1"
WORK = HERE / "work" / "phase9f1"
RTL = HERE.parent / "rtl" / "sched"


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
    ovl = PM / "kpke_sched_smp_safety_overlap_k0.sby"
    st, det, sec = base.run_sby(ovl, ovl.stem)
    rows.append(("A Phase 9F S1", "kpke_sched_smp STREAM_A=1 OVERLAP=1 CORE_R2=0 (F1-F5)", "PASS", st, det, sec))
    d, sby = mutant("negctl_F2", ovl, "kpke_sched_smp.sv", [("if (idle_st && seed_we_i) begin", "if (seed_we_i) begin")])
    st, det, sec = base.run_sby(sby, d.name + "_run")
    rows.append(("B Negative control", "NC-F2: seed write accepted while busy (F2), OVERLAP=1", "FAIL", st, det, sec))
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
