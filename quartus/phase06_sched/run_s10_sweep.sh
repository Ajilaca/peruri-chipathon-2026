#!/usr/bin/env bash
# quartus/phase06_sched/run_s10_sweep.sh -- S10 test plan V7: waits for the P6 compile of this project to finish (shared .qpf), then compiles S10 seeds 1-6 at 40 ns and S10-20
# seeds 1-6 at 20 ns, strictly one at a time. Log per revision: compile_<rev>.log; progress: sweep_s10_status.log.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > sweep_s10_status.log
until grep -q '^done' p6_status.log 2>/dev/null; do sleep 15; done
for rev in S10 S10-s2 S10-s3 S10-s4 S10-s5 S10-s6 S10-20 S10-20-s2 S10-20-s3 S10-20-s4 S10-20-s5 S10-20-s6; do
    cp phase06_sched.qpf .qpf.backup
    quartus_sh --flow compile phase06_sched -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> sweep_s10_status.log
    cmp -s phase06_sched.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> sweep_s10_status.log; cp .qpf.backup phase06_sched.qpf; }
done
rm -f .qpf.backup
echo done >> sweep_s10_status.log
