#!/usr/bin/env bash
# quartus/phase08b_sampler/run_sm2.sh -- 8b test plan V11, stage W2: compiles SM2 seeds 1-6 at 40 ns, SM2-20 (seed 1, 20 ns, information) and SM2-K0 (seed 1, K0 sponge, information),
# strictly one at a time (the revisions share one .qpf). Log per revision: compile_<rev>.log; progress: sm2_status.log.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > sm2_status.log
for rev in SM2 SM2-s2 SM2-s3 SM2-s4 SM2-s5 SM2-s6 SM2-20 SM2-K0; do
    cp phase08b_sampler.qpf .qpf.backup
    quartus_sh --flow compile phase08b_sampler -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> sm2_status.log
    cmp -s phase08b_sampler.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> sm2_status.log; cp .qpf.backup phase08b_sampler.qpf; }
done
rm -f .qpf.backup
echo done >> sm2_status.log
