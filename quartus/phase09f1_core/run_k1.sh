#!/usr/bin/env bash
# quartus/phase09f1_core/run_k1.sh -- S1 test plan V8: compiles K1 K1-s2 K1-s3 K1-s4 K1-s5 K1-s6 K1-15-s1 K1-15-s2 K1-15-s3 K1-15-s4 K1-15-s5 K1-15-s6 strictly one at a time (the revisions share one .qpf).
# Log per revision: compile_<rev>.log; progress: k1_status.log.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > k1_status.log
for rev in K1 K1-s2 K1-s3 K1-s4 K1-s5 K1-s6 K1-15-s1 K1-15-s2 K1-15-s3 K1-15-s4 K1-15-s5 K1-15-s6; do
    cp phase09f1_core.qpf .qpf.backup
    quartus_sh --flow compile phase09f1_core -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> k1_status.log
    cmp -s phase09f1_core.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> k1_status.log; cp .qpf.backup phase09f1_core.qpf; }
done
rm -f .qpf.backup
echo done >> k1_status.log
