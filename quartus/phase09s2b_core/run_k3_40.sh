#!/usr/bin/env bash
# quartus/phase09s2b_core/run_k3_40.sh -- S2b test plan V8, the 40 ns part (the gate of section 5): waits until run_k3_15.sh has finished, then compiles K3 K3-s2 .. K3-s6 one at a time.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
while ps -eo args | grep -q "[r]un_k3_15.sh"; do sleep 15; done
for rev in K3 K3-s2 K3-s3 K3-s4 K3-s5 K3-s6; do
    cp phase09s2b_core.qpf .qpf.backup
    quartus_sh --flow compile phase09s2b_core -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> k3_status.log
    cp .qpf.backup phase09s2b_core.qpf
done
rm -f .qpf.backup
echo done40 >> k3_status.log
