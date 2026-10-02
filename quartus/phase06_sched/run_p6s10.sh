#!/usr/bin/env bash
# quartus/phase06_sched/run_p6s10.sh -- information compiles of the Phase 6 top with the S10 core at 40 ns and 20 ns (seed 1), one at a time.
# Log per revision: compile_<rev>.log; progress: p6s10_status.log.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > p6s10_status.log
until grep -q '^done' p6_status.log 2>/dev/null; do sleep 15; done
for rev in P6S10 P6S10-20; do
    cp phase06_sched.qpf .qpf.backup
    quartus_sh --flow compile phase06_sched -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> p6s10_status.log
    cmp -s phase06_sched.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> p6s10_status.log; cp .qpf.backup phase06_sched.qpf; }
done
rm -f .qpf.backup
echo done >> p6s10_status.log
