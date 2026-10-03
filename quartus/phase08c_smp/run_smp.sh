#!/usr/bin/env bash
# quartus/phase08c_smp/run_smp.sh -- 8c test plan V9: compiles SMP0 (STORE, 8c baseline), SMP1 (STREAM, 8c) and SMP2 (OVERLAP, 8d), seeds 1-6 at 40 ns each (seed 1 of the three first), and the 20 ns information revisions (seed 1), strictly one at a time (the revisions share one .qpf).
# Log per revision: compile_<rev>.log; progress: smp_status.log.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > smp_status.log
for rev in SMP0 SMP1 SMP2 SMP0-s2 SMP1-s2 SMP2-s2 SMP0-s3 SMP1-s3 SMP2-s3 SMP0-s4 SMP1-s4 SMP2-s4 SMP0-s5 SMP1-s5 SMP2-s5 SMP0-s6 SMP1-s6 SMP2-s6 SMP0-20 SMP1-20 SMP2-20; do
    cp phase08c_smp.qpf .qpf.backup
    quartus_sh --flow compile phase08c_smp -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> smp_status.log
    cmp -s phase08c_smp.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> smp_status.log; cp .qpf.backup phase08c_smp.qpf; }
done
rm -f .qpf.backup
echo done >> smp_status.log
