#!/usr/bin/env bash
# scripts/phase9b_verify.sh -- Phase 9b verification (docs/evidence/phase09-integration/9b/test_plan_9b.md V1-V8, V10), both simulators.
# V8 (formal) is formal/run_formal_phase9b.py, run at the end unless P9B_FORMAL=0.
# Usage: . scripts/env.sh && scripts/phase9b_verify.sh
set -u
cd "$(dirname "${BASH_SOURCE[0]}")/.."
export HF_BUILD_DIR="${HF_BUILD_DIR:-$(mktemp -d -t chip2026_9b_XXXX)}"
export HF_CYCLES_OUT_DIR="${HF_CYCLES_OUT_DIR:-$HF_BUILD_DIR}"
overall=0
step() {
    local h=$1; shift
    echo "## $h"
    "$@" 2>&1 | grep -E "^\[(icarus|verilator)\]|passed|failed|^%Error|^%Warning|Build succeeded|errors|ALL AS EXPECTED|UNEXPECTED|^\| |cycles \(" | grep -v "^\s*$"
    local rc=${PIPESTATUS[0]}
    echo "rc=$rc"
    [ "$rc" -eq 0 ] || overall=1
}
KECCAK="rtl/keccak/keccak_pkg.sv rtl/keccak/keccak_round.sv rtl/keccak/keccak_f1600.sv rtl/keccak/keccak_sponge.sv rtl/keccak/keccak_f1600_r2.sv rtl/keccak/keccak_sponge_r2.sv"
MK="rtl/mlkem/mlkem_hash.sv rtl/mlkem/mlkem_fo_cmp.sv rtl/mlkem/mlkem_hash_fo_top.sv"
step "V1 verilator --lint-only -Wall mlkem_hash (CORE_R2 = 1)" verilator --lint-only -Wall -GCORE_R2=1 $KECCAK rtl/mlkem/mlkem_hash.sv --top-module mlkem_hash
step "V1 verilator --lint-only -Wall mlkem_hash (CORE_R2 = 0)" verilator --lint-only -Wall -GCORE_R2=0 $KECCAK rtl/mlkem/mlkem_hash.sv --top-module mlkem_hash
step "V1 verilator --lint-only -Wall mlkem_fo_cmp" verilator --lint-only -Wall rtl/mlkem/mlkem_fo_cmp.sv --top-module mlkem_fo_cmp
step "V1 verilator --lint-only -Wall mlkem_hash_fo_top" verilator --lint-only -Wall $KECCAK $MK --top-module mlkem_hash_fo_top
step "V1 slang mlkem_hash_fo_top" slang $KECCAK $MK --top mlkem_hash_fo_top
step "V2 golden FO model against the unmodified golden Decaps" python3 -m pytest -q tb/golden/tests/test_fo_model.py
for sim in verilator icarus; do
    step "V3-V7, V10 $sim" python3 tb/mlkem/run_hashfo_tests.py "$sim"
done
if [ "${P9B_FORMAL:-1}" != "0" ]; then
    step "V8 formal: formal/run_formal_phase9b.py" python3 formal/run_formal_phase9b.py all
fi
[ "$overall" -eq 0 ] && echo "OVERALL: PASS" || echo "OVERALL: FAIL"
exit "$overall"
