#!/usr/bin/env bash
# quartus/phase09m1_core/run_mw.sh -- 9M-1 test plan V8: compiles MW seeds 1-6 at 40 ns and MW-20 (seed 1, 20 ns, information), strictly one at a time (the revisions share one .qpf).
# Log per revision: compile_<rev>.log; progress: mw_status.log.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > mw_status.log
for rev in MW MW-s2 MW-s3 MW-s4 MW-s5 MW-s6 MW-20; do
    cp phase09m1_core.qpf .qpf.backup
    quartus_sh --flow compile phase09m1_core -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> mw_status.log
    cmp -s phase09m1_core.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> mw_status.log; cp .qpf.backup phase09m1_core.qpf; }
done
rm -f .qpf.backup
echo done >> mw_status.log
