#!/usr/bin/env bash
# Phase 4 fitter-seed sweep for P=4 and P=6 (seeds 2..6; the measured revisions C3-P4 / C3-P6 use the default seed 1).
# Compiles every seed revision ONE AT A TIME: running two quartus_sh in parallel on this project made them rewrite
# the shared .qpf concurrently and lose a revision (2026-10-01). Run from this directory
# after `. scripts/env.sh`. Logs: compile_P<p>_s<seed>.log (git-ignored).
set -u
for p in 4 6; do
  for s in 2 3 4 5 6; do
    quartus_sh --flow compile phase04_pipeline_c3 -c C3-P$p-s$s > compile_P${p}_s$s.log 2>&1
    echo "P$p s$s exit $?"
  done
done
