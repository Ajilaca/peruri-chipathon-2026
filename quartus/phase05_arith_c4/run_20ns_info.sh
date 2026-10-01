#!/usr/bin/env bash
# quartus/phase05_arith_c4/run_20ns_info.sh -- Phase 5 closure: information compiles at 20.000 ns (ADR 0011 D1) of the final
# C4 configuration (C4b-B) and of C3-P6, one at a time. Log per revision: compile_<rev>.log; progress: sweep_20ns_status.log.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > sweep_20ns_status.log
for rev in C4b-B-20 C3-P6-20; do
    cp phase05_arith_c4.qpf .qpf.backup
    quartus_sh --flow compile phase05_arith_c4 -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> sweep_20ns_status.log
    cmp -s phase05_arith_c4.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> sweep_20ns_status.log; cp .qpf.backup phase05_arith_c4.qpf; }
done
rm -f .qpf.backup
echo done >> sweep_20ns_status.log
