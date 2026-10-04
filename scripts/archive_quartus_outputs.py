#!/usr/bin/env python3
"""scripts/archive_quartus_outputs.py -- moves the Quartus build products out of the repository tree into one archive directory (to be uploaded to the team drive); nothing in the archive is committed (C7: no large binaries in the public repository).

What moves (per project directory quartus/<project>/):
  reports/<revision>/   the directory output_files_<revision>/ (fit, map, sta, asm, flow reports, summaries, .pin, .sof)   [tier A, small, what the evidence extracts were read from]
  logs/                 compile_*.log, all_compiles.log and the *_status.log of the campaign scripts
  databases/            db/ and incremental_db/ (needed only to rerun quartus_sta or the fitter report queries; large; tier B)
  and, for the copies quartus/par_a .. par_d (parallel copies of the Phase 8c/8d project), the whole directory.
What stays in the repository (small inputs that reproduce the compiles): .qpf, .qsf, .sdc, run_*.sh, c5_pin_model_dump.txt is moved (generated). The evidence extracts under docs/evidence/ keep their text "Source directory: quartus/..."; this script writes MANIFEST.tsv that maps each of those paths to its new place.
The archive and the repository must be on the same file system for a move (a rename; no copy, no extra space). Default is a dry run; --apply performs the move. Nothing is deleted. Not for use while a Quartus compile is running in the project.
Usage: python3 scripts/archive_quartus_outputs.py [--apply] [--dest DIR] [--only PROJECT ...]
"""
import argparse
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
Q = ROOT / "quartus"
DEST_DEFAULT = ROOT.parent / "CHIPATON_quartus_archive"

# project directory -> (group folder, step label, repo evidence of the step)
GROUPS = {
    "phase01_ntt_c0": ("phase01-08_blocks", "Phase 1 NTT lane C0", "docs/results/result_phase1.md"),
    "phase02_mem_c1": ("phase01-08_blocks", "Phase 2 memory C1", "docs/results/result_phase2.md"),
    "phase03_multilane_c2": ("phase01-08_blocks", "Phase 3 multi-lane C2", "docs/results/result_phase3.md"),
    "phase04_pipeline_c3": ("phase01-08_blocks", "Phase 4 pipeline C3", "docs/results/result_phase4.md"),
    "phase05_arith_c4": ("phase01-08_blocks", "Phase 5 arithmetic C4", "docs/results/result_phase5.md"),
    "phase05m_memsched": ("phase01-08_blocks", "Phase 5M memory / scheduling S6-S9", "docs/results/result_phase5m.md"),
    "phase06_sched": ("phase01-08_blocks", "Phase 6 scheduling, S10", "docs/results/result_phase6.md"),
    "phase07_keccak": ("phase01-08_blocks", "Phase 7 Keccak", "docs/results/result_phase7.md"),
    "phase08_keccak": ("phase01-08_blocks", "Phase 8a Keccak C5", "docs/evidence/phase08-keccak-stream/"),
    "phase08b_sampler": ("phase01-08_blocks", "Phase 8b samplers", "docs/evidence/phase08-keccak-stream/8b/"),
    "phase08c_smp": ("phase01-08_blocks", "Phase 8c / 8d K-PKE sequencer", "docs/evidence/phase08-keccak-stream/8c/ and 8d/"),
    "par_a": ("phase08_parallel_copies", "parallel copy of phase08c_smp (2026-10-03)", "docs/evidence/phase08-keccak-stream/8c/, 8d/"),
    "par_b": ("phase08_parallel_copies", "parallel copy of phase08c_smp (2026-10-03)", "docs/evidence/phase08-keccak-stream/8c/, 8d/"),
    "par_c": ("phase08_parallel_copies", "parallel copy of phase08c_smp (2026-10-03)", "docs/evidence/phase08-keccak-stream/8c/, 8d/"),
    "par_d": ("phase08_parallel_copies", "parallel copy of phase08c_smp (2026-10-03)", "docs/evidence/phase08-keccak-stream/8c/, 8d/"),
    "phase09a_codec": ("phase09_core", "Phase 9a codec", "docs/evidence/phase09-integration/9a/"),
    "phase09b_hashfo": ("phase09_core", "Phase 9b hash and FO comparison", "docs/evidence/phase09-integration/9b/"),
    "phase09c_core": ("phase09_core", "Phase 9c core MC", "docs/evidence/phase09-integration/9c/"),
    "phase09m1_core": ("phase09M_optimisation", "9M-1 two-byte codec (MW)", "docs/evidence/phase09m-optimisation/9m1/"),
    "phase09m2_core": ("phase09M_optimisation", "9M-2 core at 20 ns", "docs/evidence/phase09m-optimisation/9m2/"),
    "phase09m3_core": ("phase09M_optimisation", "9M-3 K0 hash (MK)", "docs/evidence/phase09m-optimisation/9m3/"),
    "phase09f0_core": ("phase09F_fmax", "S0 9M-1 core at 16 .. 13 ns", "docs/evidence/phase09m-optimisation/9f0/"),
    "phase09f1_core": ("phase09F_fmax", "S1 K1 (K0 sampler and hash)", "docs/evidence/phase09m-optimisation/9f1/"),
    "phase09f1b_core": ("phase09F_fmax", "S1b K1b (background hash)", "docs/evidence/phase09m-optimisation/9f1b/"),
}


def size(p: Path) -> int:
    if p.is_file():
        return p.stat().st_size
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file())


def plan(only):
    items = []   # (kind, src, dst_rel)
    for proj in sorted(d for d in Q.iterdir() if d.is_dir()):
        if only and proj.name not in only:
            continue
        grp = GROUPS.get(proj.name)
        if not grp:
            print(f"skip {proj.name}: not in GROUPS", file=sys.stderr)
            continue
        base = Path(grp[0]) / proj.name
        if proj.name.startswith("par_"):
            items.append(("whole directory", proj, base))
            continue
        for d in sorted(proj.glob("output_files*")):
            rev = d.name[len("output_files_"):] if d.name.startswith("output_files_") else "default"
            items.append(("reports", d, base / "reports" / rev))
        for f in sorted(list(proj.glob("compile*.log")) + list(proj.glob("all_compiles.log")) + list(proj.glob("*_status.log")) + list(proj.glob("c5_pin_model_dump.txt"))):
            items.append(("logs", f, base / "logs" / f.name))
        for d in ("db", "incremental_db"):
            if (proj / d).is_dir():
                items.append(("databases", proj / d, base / "databases" / d))
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dest", default=str(DEST_DEFAULT))
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    dest = Path(a.dest)
    items = plan(set(a.only or []))
    tot = {}
    rows = ["kind\tproject\told path (as written in the evidence extracts)\tnew path in the archive\tbytes"]
    for kind, src, rel in items:
        n = size(src)
        tot[kind] = tot.get(kind, 0) + n
        rows.append(f"{kind}\t{src.name if kind == 'whole directory' else src.relative_to(Q).parts[0]}\t{src.relative_to(ROOT)}\t{rel}\t{n}")
    print("\n".join(f"{k:16s} {v / 1e9:8.2f} GB" for k, v in tot.items()))
    print(f"total {sum(tot.values()) / 1e9:.2f} GB in {len(items)} items -> {dest} ({'APPLY' if a.apply else 'dry run'})")
    if os.stat(ROOT).st_dev != os.stat(dest.parent).st_dev and a.apply:
        sys.exit("the archive is on another file system: a move would copy; refuse (choose --dest on the same file system)")
    dest.mkdir(parents=True, exist_ok=True) if a.apply else None
    if a.apply:
        mf = dest / "MANIFEST.tsv"
        old = mf.read_text().rstrip("\n").split("\n") if mf.exists() else []
        mf.write_text("\n".join(old + rows[1:] if old else rows) + "\n")      # a later run appends to the manifest of the earlier runs
    if a.apply:
        for kind, src, rel in items:
            tgt = dest / rel
            tgt.parent.mkdir(parents=True, exist_ok=True)
            if tgt.exists():
                sys.exit(f"target exists, stop: {tgt}")
            shutil.move(str(src), str(tgt))
        print("moved; MANIFEST.tsv written")


if __name__ == "__main__":
    main()
