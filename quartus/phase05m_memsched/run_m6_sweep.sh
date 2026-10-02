#!/usr/bin/env bash
# quartus/phase05m_memsched/run_m6_sweep.sh -- Phase 5M step S6: compiles M6 at seeds 1..6 (adoption rule of
# docs/evidence/phase05m-memsched/test_plan.md section 4), strictly one at a time (parallel runs corrupt the shared .qpf).
# Log per revision: compile_<rev>.log; progress: sweep_m6_status.log.
# Usage (from this folder, after . ../../scripts/env.sh): nohup ./run_m6_sweep.sh &
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > sweep_m6_status.log
for rev in M6 M6-s2 M6-s3 M6-s4 M6-s5 M6-s6; do
    cp phase05m_memsched.qpf .qpf.backup
    quartus_sh --flow compile phase05m_memsched -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> sweep_m6_status.log
    cmp -s phase05m_memsched.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> sweep_m6_status.log; cp .qpf.backup phase05m_memsched.qpf; }
done
rm -f .qpf.backup
echo done >> sweep_m6_status.log
