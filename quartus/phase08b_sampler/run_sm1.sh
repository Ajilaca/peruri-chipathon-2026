#!/usr/bin/env bash
# quartus/phase08b_sampler/run_sm1.sh -- 8b test plan V11, stage W1: compiles SM1 seeds 1-6 at 40 ns, SM1-20 (seed 1, 20 ns, information) and SM1-K0 (seed 1, K0 sponge, information),
# strictly one at a time (the revisions share one .qpf). Log per revision: compile_<rev>.log; progress: sm1_status.log.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > sm1_status.log
for rev in SM1 SM1-s2 SM1-s3 SM1-s4 SM1-s5 SM1-s6 SM1-20 SM1-K0; do
    cp phase08b_sampler.qpf .qpf.backup
    quartus_sh --flow compile phase08b_sampler -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> sm1_status.log
    cmp -s phase08b_sampler.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> sm1_status.log; cp .qpf.backup phase08b_sampler.qpf; }
done
rm -f .qpf.backup
echo done >> sm1_status.log
