#!/usr/bin/env python3
"""formal/run_formal_phase8c.py

Phase 8c formal run (docs/evidence/phase08-keccak-stream/8c/test_plan_8c.md, V7), same flow as formal/run_formal_phase8b.py:
  A. kpke_sched_smp_safety.sby        -- F1-F5 of kpke_sched_smp_formal_top.sv, STREAM_A = 1, OVERLAP = 0 (the 8c build). Expected: PASS.
  A. kpke_sched_smp_safety_store.sby  -- the same with STREAM_A = 0 (the STORE build). Expected: PASS.
  B. Negative control on a deliberately corrupted COPY (repository RTL never modified):
       NC-F2  the seed registers are written even while the sequencer is busy (gate `idle_st` removed) -> F2 must FAIL
The NTT core is abstracted and the sampler is replaced by the protocol stub formal/phase08-keccak-stream/8c/keccak_sampler_stub.sv; control properties only, not values.
Usage: . scripts/env.sh && python3 formal/run_formal_phase8c.py      Work directory: formal/work/phase8c/ (git-ignored).
"""
import pathlib
import shutil
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import run_formal_slang as base  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
PM = HERE / "phase08-keccak-stream" / "8c"
WORK = HERE / "work" / "phase8c"
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
    stream, store = PM / "kpke_sched_smp_safety.sby", PM / "kpke_sched_smp_safety_store.sby"
    st, det, sec = base.run_sby(stream, stream.stem)
    rows.append(("A Phase 8c", "kpke_sched_smp STREAM_A=1 (F1-F5)", "PASS", st, det, sec))
    st, det, sec = base.run_sby(store, store.stem)
    rows.append(("A Phase 8c", "kpke_sched_smp STREAM_A=0, the STORE build (F1-F5)", "PASS", st, det, sec))
    d, sby = mutant("negctl_F2", stream, "kpke_sched_smp.sv", [("if (idle_st && seed_we_i) begin", "if (seed_we_i) begin")])
    st, det, sec = base.run_sby(sby, d.name + "_run")
    rows.append(("B Negative control", "NC-F2: seed write accepted while busy (F2)", "FAIL", st, det, sec))
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
