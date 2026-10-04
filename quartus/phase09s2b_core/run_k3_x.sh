#!/usr/bin/env bash
# quartus/phase09s2b_core/run_k3_x.sh -- S2b amendment A2: three additional 15 ns seeds (K3-15-s7, s8, s9), after run_k3_40.sh has finished; one at a time.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
while ps -eo args | grep -q "[r]un_k3_40.sh"; do sleep 15; done
for rev in K3-15-s7 K3-15-s8 K3-15-s9; do
    cp phase09s2b_core.qpf .qpf.backup
    quartus_sh --flow compile phase09s2b_core -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> k3_status.log
    cp .qpf.backup phase09s2b_core.qpf
done
rm -f .qpf.backup
echo donex >> k3_status.log
