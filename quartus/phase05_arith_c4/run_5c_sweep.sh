#!/usr/bin/env bash
# quartus/phase05_arith_c4/run_5c_sweep.sh -- Phase 5c: compiles C4c at seeds 1..6 (ADR 0014 adoption rule), strictly
# one at a time (parallel runs corrupt the shared .qpf). Log per revision: compile_<rev>.log; progress:
# sweep_5c_status.log. Usage (from this folder, after . ../../scripts/env.sh): nohup ./run_5c_sweep.sh &
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > sweep_5c_status.log
for rev in C4c C4c-s2 C4c-s3 C4c-s4 C4c-s5 C4c-s6; do
    cp phase05_arith_c4.qpf .qpf.backup
    quartus_sh --flow compile phase05_arith_c4 -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> sweep_5c_status.log
    cmp -s phase05_arith_c4.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> sweep_5c_status.log; cp .qpf.backup phase05_arith_c4.qpf; }
done
rm -f .qpf.backup
echo done >> sweep_5c_status.log
