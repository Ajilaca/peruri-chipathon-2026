#!/usr/bin/env bash
# scripts/test/phase9c_verify.sh -- Phase 9c verification (evidence/phase09/9c/test_plan_9c.md V1-V8, V10), both simulators.
# V10 regression: scripts/test/phase9a_verify.sh and scripts/test/phase9b_verify.sh (unless P9C_REGRESS=0), and a check that no file of the frozen blocks (rtl/sched, rtl/ntt, rtl/mem, rtl/arith, rtl/sample, rtl/keccak) differs from main.
# P9C_SIMS=0 skips the two simulator runs (about 3 minutes on Verilator and about an hour on Icarus; run them separately with tb/mlkem/run_core_tests.py).
# Usage: . scripts/env.sh && scripts/test/phase9c_verify.sh
set -u
cd "$(dirname "${BASH_SOURCE[0]}")/../.."
export CORE_BUILD_DIR="${CORE_BUILD_DIR:-$(mktemp -d -t chip2026_9c_XXXX)}"
export CORE_CYCLES_OUT_DIR="${CORE_CYCLES_OUT_DIR:-$CORE_BUILD_DIR}"
overall=0
step() {
    local h=$1; shift
    echo "## $h"
    "$@" 2>&1 | grep -E "^\[(icarus|verilator)\]|passed|failed|^%Error|^%Warning|Build succeeded|errors|equals the generated|ALL AS EXPECTED|UNEXPECTED|OVERALL|^rc=|^\| |ACVP|random cases|constant cycles|^DIFFERENT" | grep -v "^\s*$"
    local rc=${PIPESTATUS[0]}
    echo "rc=$rc"
    [ "$rc" -eq 0 ] || overall=1
}
ENG=$(grep "SYSTEMVERILOG_FILE" quartus/phase09c_core/MC.qsf | sed 's#.*SYSTEMVERILOG_FILE ##; s#^\.\./\.\./##' | grep -v "^rtl/mlkem" | tr '\n' ' ')
MK="rtl/mlkem/mlkem_pack.sv rtl/mlkem/mlkem_unpack.sv rtl/mlkem/mlkem_hash.sv rtl/mlkem/mlkem_fo_cmp.sv rtl/mlkem/mlkem_ram.sv rtl/mlkem/mlkem_fifo4.sv rtl/mlkem/mlkem_wordbytes.sv rtl/mlkem/mlkem_bytedst.sv rtl/mlkem/mlkem_ldpoly.sv rtl/mlkem/mlkem_stpoly.sv rtl/mlkem/mlkem_ctl_rom.sv rtl/mlkem/mlkem_core.sv"
step "V1 verilator --lint-only -Wall mlkem_core (whole design)" verilator --lint-only -Wall --top-module mlkem_core $ENG $MK
step "V1 slang mlkem_core (whole design)" slang --top mlkem_core $ENG $MK
step "V2 ROM equals the generated ROM, static checks" python3 scripts/build/gen_mlkem_ctl_rom.py --check
step "V2 golden control model against ACVP and the unmodified golden" python3 -m pytest -q tb/golden/tests/test_mlkem_ctl_model.py
if [ "${P9C_SIMS:-1}" != "0" ]; then
    for sim in verilator icarus; do
        step "V3-V8 $sim" python3 tb/mlkem/run_core_tests.py "$sim"
    done
fi
if [ "${P9C_REGRESS:-1}" != "0" ]; then
    step "V10 regression: scripts/test/phase9a_verify.sh (without formal)" env P9A_FORMAL=0 scripts/test/phase9a_verify.sh
    step "V10 regression: scripts/test/phase9b_verify.sh (with formal)" scripts/test/phase9b_verify.sh
    echo "## V10 frozen blocks: files of rtl/sched rtl/ntt rtl/mem rtl/arith rtl/sample rtl/keccak that differ from main"
    d=$(git diff --name-only main -- rtl/sched rtl/ntt rtl/mem rtl/arith rtl/sample rtl/keccak | wc -l)
    echo "differing files: $d"
    [ "$d" -eq 0 ] || overall=1
fi
[ "$overall" -eq 0 ] && echo "OVERALL: PASS" || echo "OVERALL: FAIL"
exit "$overall"
