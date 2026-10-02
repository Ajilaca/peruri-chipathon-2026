#!/usr/bin/env bash
# scripts/phase6_verify.sh -- Phase 6 verification (docs/evidence/phase06-scheduling/test_plan.md V1-V6), both simulators.
# Prints one "## <step>" header per step, the step's summary lines and "rc=<n>"; the last line is "OVERALL: PASS" only if every step returned 0.
# V7 (formal) is formal/run_formal_phase6.py. Usage: . scripts/env.sh && scripts/phase6_verify.sh
set -u
cd "$(dirname "${BASH_SOURCE[0]}")/.."
export P6_BUILD_DIR="${P6_BUILD_DIR:-$(mktemp -d -t chip2026_p6_XXXX)}"
export KS_SEEDS="${KS_SEEDS:-3}"
overall=0
step() {
    local h=$1; shift
    echo "## $h"
    "$@" 2>&1 | grep -E "^\[(icarus|verilator)\]|passed|failed|reproduced|DIFFERS|gamma entries|keygen:|encrypt:|decrypt:|pwm_unit:|negative control|^%Error|^%Warning|Build succeeded|errors" \
        | grep -v "^\s*$"
    local rc=${PIPESTATUS[0]}
    echo "rc=$rc"
    [ "$rc" -eq 0 ] || overall=1
}
SRC="rtl/ntt/ntt_pkg.sv rtl/ntt/twiddle_rom.sv rtl/arith/twiddle_rom_half.sv rtl/mem/bank_map_rom.sv rtl/ntt/pipe_delay.sv
     rtl/ntt/modmul_reduce_staged.sv rtl/arith/modmul_fold.sv rtl/arith/modmul_barrett.sv rtl/arith/modmul_montgomery.sv
     rtl/arith/modmul_sel.sv rtl/arith/half_mod.sv rtl/arith/butterfly_m6.sv rtl/mem/poly_mem_multiport_split.sv
     rtl/ntt/ntt_core_s7.sv rtl/ntt/ntt_core_s7_p7.sv rtl/sched/gamma_rom.sv rtl/sched/kpke_prog_rom.sv rtl/sched/poly_store.sv
     rtl/sched/pwm_unit.sv rtl/sched/kpke_sched.sv rtl/sched/kpke_sched_top.sv"
lint_v() { verilator --lint-only -Wall $SRC "$@"; }
step "V1 verilator --lint-only -Wall kpke_sched_top" lint_v --top-module kpke_sched_top
step "V1 slang kpke_sched_top" slang $SRC --top kpke_sched_top
step "V2 golden schedule model vs golden K-PKE (pytest)" python3 -m pytest -q tb/golden/tests/test_kpke_sched_model.py
step "V3 gamma and program ROMs (generated, golden-derived)" python3 scripts/gen_kpke_sched_roms.py --check
for sim in verilator icarus; do
    step "V4/V5/V6 $sim" python3 tb/sched/run_sched_tests.py "$sim"
done
[ "$overall" -eq 0 ] && echo "OVERALL: PASS" || echo "OVERALL: FAIL"
exit "$overall"
