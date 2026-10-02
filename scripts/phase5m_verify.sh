#!/usr/bin/env bash
# scripts/phase5m_verify.sh -- Phase 5M step S6 verification (docs/evidence/phase05m-memsched/test_plan.md V1-V7), both simulators.
# Prints one "## <step>" header per step, the step's summary lines and "rc=<n>"; the last line is "OVERALL: PASS" only if every step
# returned 0. V8 (formal) is formal/run_formal_phase5m.py; V9 is scripts/phase5_regression.sh and scripts/phase5_verify.sh.
# Usage: . scripts/env.sh && scripts/phase5m_verify.sh
set -u
cd "$(dirname "${BASH_SOURCE[0]}")/.."
export M6_BUILD_DIR="${M6_BUILD_DIR:-$(mktemp -d -t chip2026_m6_XXXX)}"
overall=0
step() {
    local h=$1; shift
    echo "## $h"
    "$@" 2>&1 | grep -E "^\[(icarus|verilator)\]|TOTAL|passed|failed|check_half_rom|^%|Build succeeded|verilator: 0 warnings|errors" \
        | grep -v "^\s*$"
    local rc=${PIPESTATUS[0]}
    echo "rc=$rc"
    [ "$rc" -eq 0 ] || overall=1
}
SRC="rtl/ntt/ntt_pkg.sv rtl/ntt/twiddle_rom.sv rtl/arith/twiddle_rom_half.sv rtl/mem/bank_map_rom.sv rtl/ntt/pipe_delay.sv
     rtl/ntt/modmul_reduce_staged.sv rtl/arith/modmul_fold.sv rtl/arith/modmul_barrett.sv rtl/arith/modmul_montgomery.sv
     rtl/arith/modmul_sel.sv rtl/arith/half_mod.sv rtl/arith/butterfly_m6.sv rtl/mem/poly_mem_multiport_pipe.sv
     rtl/ntt/ntt_core_m6.sv rtl/ntt/ntt_core_m6_p6.sv"
lint_v() { verilator --lint-only -Wall $SRC "$@"; }
step "V1 verilator --lint-only -Wall ntt_core_m6_p6" lint_v --top-module ntt_core_m6_p6
step "V1 slang ntt_core_m6_p6" slang $SRC --top ntt_core_m6_p6
step "V3 golden intt_halving vs intt (pytest)" python3 -m pytest -q tb/golden/tests/test_intt_halving.py
step "V4 twiddle_rom_half (generated, golden-derived)" python3 tb/phase5m/check_half_rom.py
for sim in verilator icarus; do
    step "V2/V5/V6/V7 $sim" python3 tb/phase5m/run_m6_tests.py "$sim"
done
[ "$overall" -eq 0 ] && echo "OVERALL: PASS" || echo "OVERALL: FAIL"
exit "$overall"
