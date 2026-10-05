#!/usr/bin/env bash
# scripts/test/s10_verify.sh -- S10 verification (evidence/phase06/test_plan_s10.md V1-V4, V6), both simulators. V5 (formal) is formal/run/run_formal_s10.py.
# Usage: . scripts/env.sh && scripts/test/s10_verify.sh
set -u
cd "$(dirname "${BASH_SOURCE[0]}")/../.."
export S10_BUILD_DIR="${S10_BUILD_DIR:-$(mktemp -d -t chip2026_s10_XXXX)}"
export KS_SEEDS="${KS_SEEDS:-2}"
overall=0
step() {
    local h=$1; shift
    echo "## $h"
    "$@" 2>&1 | grep -E "^\[(icarus|verilator)\]|keygen:|encrypt:|decrypt:|^%Error|^%Warning|Build succeeded|errors" | grep -v "^\s*$"
    local rc=${PIPESTATUS[0]}
    echo "rc=$rc"
    [ "$rc" -eq 0 ] || overall=1
}
SRC="rtl/ntt/ntt_pkg.sv rtl/ntt/twiddle_rom.sv rtl/arith/twiddle_rom_half.sv rtl/ntt/pipe_delay.sv rtl/ntt/modmul_reduce_staged.sv
     rtl/arith/modmul_fold.sv rtl/arith/modmul_barrett.sv rtl/arith/modmul_montgomery.sv rtl/arith/modmul_sel.sv rtl/arith/half_mod.sv
     rtl/arith/butterfly_m6.sv rtl/mem/poly_mem_m10k.sv rtl/ntt/ntt_core_s10.sv rtl/ntt/ntt_core_s10_p5.sv"
SCH="rtl/sched/gamma_rom.sv rtl/sched/kpke_prog_rom.sv rtl/sched/poly_store.sv rtl/sched/pwm_unit.sv rtl/sched/kpke_sched.sv rtl/sched/kpke_sched_top_s10.sv"
lint_v() { verilator --lint-only -Wall $SRC "$@"; }
lint_t() { verilator --lint-only -Wall $SRC $SCH "$@"; }
step "V1 verilator --lint-only -Wall ntt_core_s10_p5" lint_v --top-module ntt_core_s10_p5
step "V1 slang ntt_core_s10_p5" slang $SRC --top ntt_core_s10_p5
step "V1 verilator --lint-only -Wall kpke_sched_top_s10" lint_t --top-module kpke_sched_top_s10
for sim in verilator icarus; do
    step "V2/V3/V4/V6 $sim" python3 tb/s10/run_s10_tests.py "$sim"
done
[ "$overall" -eq 0 ] && echo "OVERALL: PASS" || echo "OVERALL: FAIL"
exit "$overall"
