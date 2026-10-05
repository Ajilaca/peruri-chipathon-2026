#!/usr/bin/env bash
# scripts/test/phase5m_verify_s8.sh -- Phase 5M step S8 verification (evidence/phase05m/test_plan_s8.md V1-V4, V6), both simulators.
# Prints one "## <step>" header per step, the step's summary lines and "rc=<n>"; the last line is "OVERALL: PASS" only if every step returned 0.
# V5 (formal) is formal/run/run_formal_phase5m_s8.py; V7 and V8 (re-runs of S6 / S7 and the Phase 0-5 regression) are scripts/test/phase5m_final_regression.sh.
# Usage: . scripts/env.sh && scripts/test/phase5m_verify_s8.sh
set -u
cd "$(dirname "${BASH_SOURCE[0]}")/../.."
export S8_BUILD_DIR="${S8_BUILD_DIR:-$(mktemp -d -t chip2026_s8_XXXX)}"
overall=0
step() {
    local h=$1; shift
    echo "## $h"
    "$@" 2>&1 | grep -E "^\[(icarus|verilator)\]|TOTAL|passed|failed|^%Error|^%Warning-(WIDTH|UNUSED|LATCH|CASE)|Build succeeded|errors" | grep -v "^\s*$"
    local rc=${PIPESTATUS[0]}
    echo "rc=$rc"
    [ "$rc" -eq 0 ] || overall=1
}
SRC="rtl/ntt/ntt_pkg.sv rtl/ntt/twiddle_rom.sv rtl/arith/twiddle_rom_half.sv rtl/mem/bank_map_rom.sv rtl/ntt/pipe_delay.sv
     rtl/ntt/modmul_reduce_staged.sv rtl/arith/modmul_fold.sv rtl/arith/modmul_barrett.sv rtl/arith/modmul_montgomery.sv
     rtl/arith/modmul_sel.sv rtl/arith/half_mod.sv rtl/arith/butterfly_m6.sv rtl/mem/poly_mem_multiport_split.sv
     rtl/ntt/ntt_core_s8.sv rtl/ntt/ntt_core_s8_p8.sv"
lint_v() { verilator --lint-only -Wall $SRC "$@"; }
step "V1 verilator --lint-only -Wall ntt_core_s8_p8" lint_v --top-module ntt_core_s8_p8
step "V1 slang ntt_core_s8_p8" slang $SRC --top ntt_core_s8_p8
for sim in verilator icarus; do
    step "V2/V3/V4/V6 $sim" python3 tb/phase5m/run_s8_tests.py "$sim"
done
[ "$overall" -eq 0 ] && echo "OVERALL: PASS" || echo "OVERALL: FAIL"
exit "$overall"
