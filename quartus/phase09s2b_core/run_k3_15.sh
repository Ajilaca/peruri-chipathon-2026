#!/usr/bin/env bash
# quartus/phase09s2b_core/run_k3_15.sh -- S2b test plan V8 after amendment A1 (no 40 ns compiles): waits for the running compile of the project (K3-15-s2, started by run_k3.sh, whose loop was stopped), then compiles K3-15-s3 .. K3-15-s6 one at a time.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
while ps -eo args | grep -q "[q]uartus_sh --flow compile"; do sleep 15; done
echo "K3-15-s2 finished (waited for by run_k3_15.sh; its rc was not recorded: check compile_K3-15-s2.log and the .done file)" >> k3_status.log
for rev in K3-15-s3 K3-15-s4 K3-15-s5 K3-15-s6; do
    cp phase09s2b_core.qpf .qpf.backup
    quartus_sh --flow compile phase09s2b_core -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> k3_status.log
    cp .qpf.backup phase09s2b_core.qpf
done
rm -f .qpf.backup
echo done >> k3_status.log
