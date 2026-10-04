#!/usr/bin/env bash
# quartus/phase09m2_core/run_20.sh -- 9M-2 test plan section 6: compiles MC-20-s2..s6 and MW-20-s2..s6 at 20 ns, strictly one at a time (the revisions share one .qpf).
# Log per revision: compile_<rev>.log; progress: m2_status.log.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > m2_status.log
for rev in MC-20-s2 MC-20-s3 MC-20-s4 MC-20-s5 MC-20-s6 MW-20-s2 MW-20-s3 MW-20-s4 MW-20-s5 MW-20-s6; do
    cp phase09m2_core.qpf .qpf.backup
    quartus_sh --flow compile phase09m2_core -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> m2_status.log
    cmp -s phase09m2_core.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> m2_status.log; cp .qpf.backup phase09m2_core.qpf; }
done
rm -f .qpf.backup
echo done >> m2_status.log
