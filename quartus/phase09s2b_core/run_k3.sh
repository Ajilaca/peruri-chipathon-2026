#!/usr/bin/env bash
# quartus/phase09s2b_core/run_k3.sh -- S2b test plan V8: compiles K3-15-s1 K3-15-s2 K3-15-s3 K3-15-s4 K3-15-s5 K3-15-s6 K3 K3-s2 K3-s3 K3-s4 K3-s5 K3-s6 strictly one at a time (the revisions share one .qpf; the 15 ns ones first, they decide the rule).
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
for rev in K3-15-s1 K3-15-s2 K3-15-s3 K3-15-s4 K3-15-s5 K3-15-s6 K3 K3-s2 K3-s3 K3-s4 K3-s5 K3-s6; do
    cp phase09s2b_core.qpf .qpf.backup
    quartus_sh --flow compile phase09s2b_core -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> k3_status.log
    cp .qpf.backup phase09s2b_core.qpf
done
rm -f .qpf.backup
echo done >> k3_status.log
