#!/usr/bin/env bash
# quartus/phase05_arith_c4/run_5b_sweep.sh -- Phase 5b: compiles C4b-B and C4b-M at seeds 1..6 (ADR 0011 D7),
# strictly one at a time (parallel runs corrupt the shared .qpf). Log per revision: compile_<rev>.log;
# progress: sweep_5b_status.log. Usage (from this folder, after . ../../scripts/env.sh): nohup ./run_5b_sweep.sh &
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > sweep_5b_status.log
for rev in C4b-B C4b-M C4b-B-s2 C4b-M-s2 C4b-B-s3 C4b-M-s3 C4b-B-s4 C4b-M-s4 C4b-B-s5 C4b-M-s5 C4b-B-s6 C4b-M-s6; do
    cp phase05_arith_c4.qpf .qpf.backup
    quartus_sh --flow compile phase05_arith_c4 -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> sweep_5b_status.log
    cmp -s phase05_arith_c4.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> sweep_5b_status.log; cp .qpf.backup phase05_arith_c4.qpf; }
done
rm -f .qpf.backup
echo done >> sweep_5b_status.log
