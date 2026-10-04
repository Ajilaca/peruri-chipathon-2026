#!/usr/bin/env bash
# quartus/phase09f1b_core/run_k1b.sh -- S1b test plan V9: compiles K1b K1b-s2 K1b-s3 K1b-s4 K1b-s5 K1b-s6 K1b-15-s1 K1b-15-s2 K1b-15-s3 K1b-15-s4 K1b-15-s5 K1b-15-s6 strictly one at a time (the revisions share one .qpf).
# Log per revision: compile_<rev>.log; progress: k1b_status.log.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > k1b_status.log
for rev in K1b K1b-s2 K1b-s3 K1b-s4 K1b-s5 K1b-s6 K1b-15-s1 K1b-15-s2 K1b-15-s3 K1b-15-s4 K1b-15-s5 K1b-15-s6; do
    cp phase09f1b_core.qpf .qpf.backup
    quartus_sh --flow compile phase09f1b_core -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> k1b_status.log
    cmp -s phase09f1b_core.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> k1b_status.log; cp .qpf.backup phase09f1b_core.qpf; }
done
rm -f .qpf.backup
echo done >> k1b_status.log
