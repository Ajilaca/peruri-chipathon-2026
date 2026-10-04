#!/usr/bin/env bash
# quartus/phase09i4_core/run_k4.sh -- item 4 test plan V9: compiles K4-15-s1 K4-15-s2 K4-15-s3 K4-15-s4 K4-15-s5 K4-15-s6 K4 K4-s2 K4-s3 K4-s4 K4-s5 K4-s6 strictly one at a time (15 ns first), after the compiles of the project phase09s2b_core have finished.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
while ps -eo args | grep -q "[r]un_k3_x.sh"; do sleep 20; done
for rev in K4-15-s1 K4-15-s2 K4-15-s3 K4-15-s4 K4-15-s5 K4-15-s6 K4 K4-s2 K4-s3 K4-s4 K4-s5 K4-s6; do
    cp phase09i4_core.qpf .qpf.backup
    quartus_sh --flow compile phase09i4_core -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> k4_status.log
    cp .qpf.backup phase09i4_core.qpf
done
rm -f .qpf.backup
echo done >> k4_status.log
