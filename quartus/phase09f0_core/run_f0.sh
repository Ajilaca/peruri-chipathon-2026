#!/usr/bin/env bash
# quartus/phase09f0_core/run_f0.sh -- S0 test plan section 6: compiles F16-s1 F16-s2 F15-s1 F15-s2 F14-s1 F14-s2 H14-s1 H14-s2 strictly one at a time (the revisions share one .qpf).
# Log per revision: compile_<rev>.log; progress: f0_status.log.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > f0_status.log
for rev in F16-s1 F16-s2 F15-s1 F15-s2 F14-s1 F14-s2 H14-s1 H14-s2; do
    cp phase09f0_core.qpf .qpf.backup
    quartus_sh --flow compile phase09f0_core -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> f0_status.log
    cmp -s phase09f0_core.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> f0_status.log; cp .qpf.backup phase09f0_core.qpf; }
done
rm -f .qpf.backup
echo done >> f0_status.log
