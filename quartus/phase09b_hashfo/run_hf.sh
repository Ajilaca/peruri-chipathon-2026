#!/usr/bin/env bash
# quartus/phase09b_hashfo/run_hf.sh -- 9b test plan V9: compiles HF seeds 1-6 at 40 ns, HF-20 (seed 1, 20 ns, information) and HF-K0 (seed 1, K0 sponge, information), strictly one at a time (the revisions share one .qpf).
# Log per revision: compile_<rev>.log; progress: hf_status.log.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > hf_status.log
for rev in HF HF-s2 HF-s3 HF-s4 HF-s5 HF-s6 HF-20 HF-K0; do
    cp phase09b_hashfo.qpf .qpf.backup
    quartus_sh --flow compile phase09b_hashfo -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> hf_status.log
    cmp -s phase09b_hashfo.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> hf_status.log; cp .qpf.backup phase09b_hashfo.qpf; }
done
rm -f .qpf.backup
echo done >> hf_status.log
