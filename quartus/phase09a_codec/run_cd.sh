#!/usr/bin/env bash
# quartus/phase09a_codec/run_cd.sh -- 9a test plan V10: compiles CD seeds 1-6 at 40 ns and CD-20 (seed 1, 20 ns, information), strictly one at a time (the revisions share one .qpf).
# Log per revision: compile_<rev>.log; progress: cd_status.log.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")"
: > cd_status.log
for rev in CD CD-s2 CD-s3 CD-s4 CD-s5 CD-s6 CD-20; do
    cp phase09a_codec.qpf .qpf.backup
    quartus_sh --flow compile phase09a_codec -c "$rev" > "compile_${rev}.log" 2>&1
    echo "$rev rc=$?" >> cd_status.log
    cmp -s phase09a_codec.qpf .qpf.backup || { echo "$rev: .qpf changed by the tool, restored" >> cd_status.log; cp .qpf.backup phase09a_codec.qpf; }
done
rm -f .qpf.backup
echo done >> cd_status.log
