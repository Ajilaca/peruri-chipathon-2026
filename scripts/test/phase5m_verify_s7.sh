#!/usr/bin/env bash
# scripts/test/phase5m_verify_s7.sh -- Phase 5M step S7 verification (evidence/phase05m/test_plan_s7.md V1-V5), both simulators.
# Prints one "## <step>" header per step, the step's summary lines and "rc=<n>"; the last line is "OVERALL: PASS" only if every step returned 0.
# V6 (formal) is formal/run/run_formal_phase5m_s7.py; V7 (regression) is not run for S7 (Amendment A1 of evidence/phase05m/test_plan.md).
# Usage: . scripts/env.sh && scripts/test/phase5m_verify_s7.sh
set -u
cd "$(dirname "${BASH_SOURCE[0]}")/../.."
export S7_BUILD_DIR="${S7_BUILD_DIR:-$(mktemp -d -t chip2026_s7_XXXX)}"
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
     rtl/ntt/ntt_core_s7.sv rtl/ntt/ntt_core_s7_p7.sv"
lint_v() { verilator --lint-only -Wall $SRC "$@"; }
step "V1 verilator --lint-only -Wall ntt_core_s7_p7" lint_v --top-module ntt_core_s7_p7
step "V1 slang ntt_core_s7_p7" slang $SRC --top ntt_core_s7_p7
for sim in verilator icarus; do
    step "V2/V3/V4/V5 $sim" python3 tb/phase5m/run_s7_tests.py "$sim"
done
[ "$overall" -eq 0 ] && echo "OVERALL: PASS" || echo "OVERALL: FAIL"
exit "$overall"
