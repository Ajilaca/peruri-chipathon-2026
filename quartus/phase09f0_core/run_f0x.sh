#!/usr/bin/env bash
# quartus/phase09f0_core/run_f0x.sh -- S0 test plan amendment A2 (Faza Dzil, chat 2026-10-04): extends the sweep to 13, 12, 11, 10 ns (defaults, seeds 1 and 2), one constraint at a time, strictly one compile at a time.
# Rule: after both seeds of a constraint, stop if either seed has a negative setup or hold slack in any corner of its sta.summary (the constraint then is the first not met); stop after 10 ns if it is still met.
# Log per revision: compile_<rev>.log; progress: f0x_status.log.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > f0x_status.log
for per in 13 12 11 10; do
    bad=0
    for seed in 1 2; do
        rev="F${per}-s${seed}"
        cp phase09f0_core.qpf .qpf.backup
        quartus_sh --flow compile phase09f0_core -c "$rev" > "compile_${rev}.log" 2>&1
        echo "$rev rc=$?" >> f0x_status.log
        cmp -s phase09f0_core.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> f0x_status.log; cp .qpf.backup phase09f0_core.qpf; }
        if awk '/^Slack/ { if ($3 + 0 < 0) neg = 1 } END { exit neg ? 0 : 1 }' "output_files_${rev}/${rev}.sta.summary"; then
            echo "$rev: NEGATIVE SLACK (timing not met)" >> f0x_status.log
            bad=1
        else
            echo "$rev: met" >> f0x_status.log
        fi
    done
    if [ "$bad" = 1 ]; then echo "stop: ${per} ns is the first constraint not met at one or both seeds" >> f0x_status.log; break; fi
done
rm -f .qpf.backup
echo done >> f0x_status.log
