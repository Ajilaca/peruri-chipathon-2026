#!/usr/bin/env bash
# scripts/test/phase8a_verify.sh -- Phase 8a verification (evidence/phase08/8a/test_plan_8a.md V1, V4-V7, V9), both simulators.
# V9 regression: runs scripts/test/phase7_verify.sh first (K0 with the parameterised tests, defaults unchanged). V8 (formal) is formal/run/run_formal_phase8a.py.
# Usage: scripts/test/phase8a_verify.sh
set -u
cd "$(dirname "${BASH_SOURCE[0]}")/../.."
export KK_BUILD_DIR="${KK_BUILD_DIR:-$(mktemp -d -t chip2026_k0_XXXX)}"
export KK_SEEDS="${KK_SEEDS:-20}"
export KK_CYCLES_OUT_DIR="${KK_CYCLES_OUT_DIR:-$KK_BUILD_DIR}"
overall=0
step() {
    local h=$1; shift
    echo "## $h"
    "$@" 2>&1 | grep -E "^\[(icarus|verilator)\]|passed|failed|^%Error|^%Warning|Build succeeded|errors|differences|all locked|OVERALL" | grep -v "^\s*$"
    local rc=${PIPESTATUS[0]}
    echo "rc=$rc"
    [ "$rc" -eq 0 ] || overall=1
}
SRC="rtl/keccak/keccak_pkg.sv rtl/keccak/keccak_round.sv rtl/keccak/keccak_f1600_r2.sv rtl/keccak/keccak_sponge_r2.sv"
step "V9 regression: scripts/test/phase7_verify.sh (K0)" scripts/test/phase7_verify.sh
step "V1 verilator --lint-only -Wall keccak_f1600_r2" verilator --lint-only -Wall $SRC --top-module keccak_f1600_r2
step "V1 verilator --lint-only -Wall keccak_sponge_r2" verilator --lint-only -Wall $SRC --top-module keccak_sponge_r2
step "V1 slang keccak_sponge_r2" slang $SRC --top keccak_sponge_r2
for sim in verilator icarus; do
    step "V4-V7 $sim (C5, two rounds per cycle)" env KK_RPC=2 python3 tb/keccak/run_keccak_tests.py "$sim"
done
[ "$overall" -eq 0 ] && echo "OVERALL: PASS" || echo "OVERALL: FAIL"
exit "$overall"
