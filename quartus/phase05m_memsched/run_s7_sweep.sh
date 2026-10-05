#!/usr/bin/env bash
# quartus/phase05m_memsched/run_s7_sweep.sh -- Phase 5M step S7: compiles S7 at seeds 1..6 (adoption rule of
# evidence/phase05m/test_plan_s7.md section 4), strictly one at a time (parallel runs corrupt the shared .qpf).
# Log per revision: compile_<rev>.log; progress: sweep_s7_status.log.
# Usage (from this folder, after . ../../scripts/env.sh): nohup ./run_s7_sweep.sh &
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > sweep_s7_status.log
for rev in S7 S7-s2 S7-s3 S7-s4 S7-s5 S7-s6; do
    cp phase05m_memsched.qpf .qpf.backup
    quartus_sh --flow compile phase05m_memsched -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> sweep_s7_status.log
    cmp -s phase05m_memsched.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> sweep_s7_status.log; cp .qpf.backup phase05m_memsched.qpf; }
done
rm -f .qpf.backup
echo done >> sweep_s7_status.log
