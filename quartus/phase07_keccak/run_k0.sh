#!/usr/bin/env bash
# quartus/phase07_keccak/run_k0.sh -- Phase 7 K0 compiles (test plan V10): K0 at 40 ns, then K0-20 at 20 ns (information), seed 1, one at a time.
# Log per revision: compile_<rev>.log; progress: k0_status.log.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > k0_status.log
for rev in K0 K0-20; do
    cp phase07_keccak.qpf .qpf.backup
    quartus_sh --flow compile phase07_keccak -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> k0_status.log
    cmp -s phase07_keccak.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> k0_status.log; cp .qpf.backup phase07_keccak.qpf; }
done
rm -f .qpf.backup
echo done >> k0_status.log
