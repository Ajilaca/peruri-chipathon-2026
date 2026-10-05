#!/usr/bin/env bash
# scripts/test/phase7_verify.sh -- Phase 7 verification (evidence/phase07/test_plan.md V1-V7, V9 parameters), both simulators. V8 (formal) is formal/run/run_formal_phase7.py.
# Usage: . scripts/env.sh && scripts/test/phase7_verify.sh
set -u
cd "$(dirname "${BASH_SOURCE[0]}")/../.."
export KK_BUILD_DIR="${KK_BUILD_DIR:-$(mktemp -d -t chip2026_k0_XXXX)}"
export KK_SEEDS="${KK_SEEDS:-20}"
export KK_CYCLES_OUT_DIR="${KK_CYCLES_OUT_DIR:-$KK_BUILD_DIR}"
overall=0
step() {
    local h=$1; shift
    echo "## $h"
    "$@" 2>&1 | grep -E "^\[(icarus|verilator)\]|passed|failed|^%Error|^%Warning|Build succeeded|errors|differences|all locked" | grep -v "^\s*$"
    local rc=${PIPESTATUS[0]}
    echo "rc=$rc"
    [ "$rc" -eq 0 ] || overall=1
}
SRC="rtl/keccak/keccak_pkg.sv rtl/keccak/keccak_round.sv rtl/keccak/keccak_f1600.sv rtl/keccak/keccak_sponge.sv"
step "V1 verilator --lint-only -Wall keccak_f1600" verilator --lint-only -Wall $SRC --top-module keccak_f1600
step "V1 verilator --lint-only -Wall keccak_sponge" verilator --lint-only -Wall $SRC --top-module keccak_sponge
step "V1 slang keccak_sponge" slang $SRC --top keccak_sponge
step "V2 pytest tb/golden/tests/test_keccak.py (golden vs hashlib)" python3 -m pytest tb/golden/tests/test_keccak.py -q
step "V3 gen_keccak_consts.py --check" python3 scripts/build/gen_keccak_consts.py --check
for sim in verilator icarus; do
    step "V4-V7 $sim" python3 tb/keccak/run_keccak_tests.py "$sim"
done
step "V9 check_params" python3 .claude/skills/mlkem-guard/scripts/check_params.py
[ "$overall" -eq 0 ] && echo "OVERALL: PASS" || echo "OVERALL: FAIL"
exit "$overall"
