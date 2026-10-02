#!/usr/bin/env bash
# quartus/phase06_sched/run_p6.sh -- Phase 6 V9: compiles P6 (own project folder, so it does not share a .qpf with another running sweep).
# Log: compile_P6.log; status: p6_status.log. Usage (from this folder, after . ../../scripts/env.sh): nohup ./run_p6.sh &
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > p6_status.log
cp phase06_sched.qpf .qpf.backup
quartus_sh --flow compile phase06_sched -c P6 > compile_P6.log 2>&1
echo "P6 rc=$?" >> p6_status.log
cmp -s phase06_sched.qpf .qpf.backup || { echo "P6: .qpf changed by the tool, restored" >> p6_status.log; cp .qpf.backup phase06_sched.qpf; }
rm -f .qpf.backup
echo done >> p6_status.log
