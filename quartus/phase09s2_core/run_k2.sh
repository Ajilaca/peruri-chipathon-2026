#!/usr/bin/env bash
# quartus/phase09s2_core/run_k2.sh -- S2 test plan V9: compiles K2 K2-s2 K2-s3 K2-s4 K2-s5 K2-s6 K2-15-s1 K2-15-s2 K2-15-s3 K2-15-s4 K2-15-s5 K2-15-s6 strictly one at a time (the revisions share one .qpf).
# Log per revision: compile_<rev>.log; progress: k2_status.log.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > k2_status.log
for rev in K2 K2-s2 K2-s3 K2-s4 K2-s5 K2-s6 K2-15-s1 K2-15-s2 K2-15-s3 K2-15-s4 K2-15-s5 K2-15-s6; do
    cp phase09s2_core.qpf .qpf.backup
    quartus_sh --flow compile phase09s2_core -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> k2_status.log
    cmp -s phase09s2_core.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> k2_status.log; cp .qpf.backup phase09s2_core.qpf; }
done
rm -f .qpf.backup
echo done >> k2_status.log
