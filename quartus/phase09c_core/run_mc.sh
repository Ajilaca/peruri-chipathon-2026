#!/usr/bin/env bash
# quartus/phase09c_core/run_mc.sh -- 9c test plan V9: compiles MC seeds 1-6 at 40 ns and MC-20 (seed 1, 20 ns, information), strictly one at a time (the revisions share one .qpf).
# Log per revision: compile_<rev>.log; progress: mc_status.log.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > mc_status.log
for rev in MC MC-s2 MC-s3 MC-s4 MC-s5 MC-s6 MC-20; do
    cp phase09c_core.qpf .qpf.backup
    quartus_sh --flow compile phase09c_core -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> mc_status.log
    cmp -s phase09c_core.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> mc_status.log; cp .qpf.backup phase09c_core.qpf; }
done
rm -f .qpf.backup
echo done >> mc_status.log
