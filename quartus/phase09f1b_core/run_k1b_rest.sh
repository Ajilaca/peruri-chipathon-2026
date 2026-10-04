#!/usr/bin/env bash
# quartus/phase09f1b_core/run_k1b_rest.sh -- reruns K1b-15-s5 and K1b-15-s6 after the first attempt of K1b-15-s5 was killed by a restart of the session (18:41, no result used); same procedure as run_k1b.sh.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
for rev in K1b-15-s5 K1b-15-s6; do
    cp phase09f1b_core.qpf .qpf.backup
    quartus_sh --flow compile phase09f1b_core -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$? (rerun)" >> k1b_status.log
    cmp -s phase09f1b_core.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> k1b_status.log; cp .qpf.backup phase09f1b_core.qpf; }
done
rm -f .qpf.backup
echo done >> k1b_status.log
