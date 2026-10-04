#!/usr/bin/env bash
# quartus/phase09m3_core/run_mk.sh -- 9M-3 test plan V7: compiles MK seeds 1-6 at 40 ns and MK-20 (seed 1, 20 ns, information), strictly one at a time (the revisions share one .qpf).
# Log per revision: compile_<rev>.log; progress: mk_status.log.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > mk_status.log
for rev in MK MK-s2 MK-s3 MK-s4 MK-s5 MK-s6 MK-20; do
    cp phase09m3_core.qpf .qpf.backup
    quartus_sh --flow compile phase09m3_core -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> mk_status.log
    cmp -s phase09m3_core.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> mk_status.log; cp .qpf.backup phase09m3_core.qpf; }
done
rm -f .qpf.backup
echo done >> mk_status.log
