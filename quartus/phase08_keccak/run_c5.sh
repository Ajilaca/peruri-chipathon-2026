#!/usr/bin/env bash
# quartus/phase08_keccak/run_c5.sh -- 8a test plan V10: waits for the K0 baseline seeds (quartus/phase07_keccak/run_k0_seeds.sh), then compiles C5 seeds 1-6 at 40 ns and C5-20 (seed 1, 20 ns, information),
# strictly one at a time. Log per revision: compile_<rev>.log; progress: c5_status.log.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > c5_status.log
until grep -q '^done' ../phase07_keccak/k0_seeds_status.log 2>/dev/null; do sleep 15; done
for rev in C5 C5-s2 C5-s3 C5-s4 C5-s5 C5-s6 C5-20; do
    cp phase08_keccak.qpf .qpf.backup
    quartus_sh --flow compile phase08_keccak -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> c5_status.log
    cmp -s phase08_keccak.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> c5_status.log; cp .qpf.backup phase08_keccak.qpf; }
done
rm -f .qpf.backup
echo done >> c5_status.log
