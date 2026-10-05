#!/usr/bin/env bash
# quartus/phase07_keccak/run_k0_seeds.sh -- baseline for the 8a rule (evidence/phase08/8a/test_plan_8a.md V10): K0 seeds 2-6 at 40 ns, one at a time (seed 1 = revision K0).
# Log per revision: compile_<rev>.log; progress: k0_seeds_status.log.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > k0_seeds_status.log
for rev in K0-s2 K0-s3 K0-s4 K0-s5 K0-s6; do
    cp phase07_keccak.qpf .qpf.backup
    quartus_sh --flow compile phase07_keccak -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> k0_seeds_status.log
    cmp -s phase07_keccak.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> k0_seeds_status.log; cp .qpf.backup phase07_keccak.qpf; }
done
rm -f .qpf.backup
echo done >> k0_seeds_status.log
