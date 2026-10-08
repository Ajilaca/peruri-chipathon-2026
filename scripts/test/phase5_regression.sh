#!/usr/bin/env bash
# scripts/test/phase5_regression.sh -- Phase 5 test plan V9 (CRG-5, CRG-6): every earlier-phase check, unchanged,
# run after the Phase 5 RTL was added. Prints one "## <step>" header per step, the step's summary lines and
# "rc=<n>"; the last line is "OVERALL: PASS" only if every step returned 0.
# Usage: scripts/test/phase5_regression.sh > <log>
set -u
cd "$(dirname "${BASH_SOURCE[0]}")/../.."
export P4_BUILD_DIR="${P4_BUILD_DIR:-$(mktemp -d -t chip2026_reg_XXXX)}"
overall=0
step() {  # header, command...
    local h=$1; shift
    echo "## $h"
    "$@" 2>&1 | grep -E "^\[(icarus|verilator)\]|TOTAL|passed|failed|check_params|OVERALL|RESULT|REG_AFTER=|cycles:|^\| " \
        | grep -v "^\s*$"
    local rc=${PIPESTATUS[0]}
    echo "rc=$rc"
    [ "$rc" -eq 0 ] || overall=1
}
step "check_params" python3 .claude/skills/mlkem-guard/scripts/check_params.py
step "pytest tb/golden" python3 -m pytest -q tb/golden
for sim in verilator icarus; do
    step "run_ntt_tests $sim"        python3 tb/ntt/run_ntt_tests.py "$sim"
    step "run_mem_tests $sim"        python3 tb/mem/run_mem_tests.py "$sim"
    for v in c2 k2 k1; do
        step "run_ntt_c2_tests $sim $v" python3 tb/ntt/run_ntt_c2_tests.py "$sim" "$v"
    done
    step "run_k1_unit_tests $sim"    python3 tb/ntt/run_k1_unit_tests.py "$sim"
    step "run_p4_unit_tests $sim"    python3 tb/ntt/run_p4_unit_tests.py "$sim"
    step "run_ntt_c3_tests $sim"     python3 tb/ntt/run_ntt_c3_tests.py "$sim"
done
step "Phase 4 exhaustive staged reducer" tb/ntt/p4_reducer/run_modmul_staged_exhaustive.sh
step "formal Phase 1-3 (run_formal_slang.py)" python3 formal/run/run_formal_slang.py
step "formal Phase 4 (run_formal_phase4.py)"  python3 formal/run/run_formal_phase4.py
[ "$overall" -eq 0 ] && echo "OVERALL: PASS" || echo "OVERALL: FAIL"
exit "$overall"
