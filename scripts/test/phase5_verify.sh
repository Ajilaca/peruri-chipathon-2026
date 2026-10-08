#!/usr/bin/env bash
# scripts/test/phase5_verify.sh -- Phase 5 test plan V1, V2, V3/V4, V5/V6 (+ negative controls) for the C4 RTL, both
# simulators. Prints one "## <step>" header per step, the step's summary lines and "rc=<n>"; the last line is
# "OVERALL: PASS" only if every step returned 0. V8 (formal) is formal/run/run_formal_phase5.py; V9 is
# scripts/test/phase5_regression.sh.
# Usage: scripts/test/phase5_verify.sh [wrapper ...]   (default: every C4 wrapper; exhaustive kinds 1 2 3)
set -u
cd "$(dirname "${BASH_SOURCE[0]}")/../.."
export C4_BUILD_DIR="${C4_BUILD_DIR:-$(mktemp -d -t chip2026_c4_XXXX)}"
wrappers=("$@")
[ $# -eq 0 ] && wrappers=(ntt_core_c4a ntt_core_c4b_b ntt_core_c4b_m ntt_core_c4c)
overall=0
step() {
    local h=$1; shift
    echo "## $h"
    "$@" 2>&1 | grep -E "^\[(icarus|verilator)\]|TOTAL|kind=|latency=|negative control|RESULT|Build succeeded|^%|warning lines|^check " \
        | grep -v "^\s*$"
    local rc=${PIPESTATUS[0]}
    echo "rc=$rc"
    [ "$rc" -eq 0 ] || overall=1
}
SRC="rtl/ntt/ntt_pkg.sv rtl/ntt/twiddle_rom.sv rtl/arith/twiddle_rom_mont.sv rtl/mem/bank_map_rom.sv rtl/ntt/pipe_delay.sv
     rtl/ntt/modmul_reduce_staged.sv rtl/arith/modmul_fold.sv rtl/arith/modmul_barrett.sv rtl/arith/modmul_montgomery.sv
     rtl/arith/modmul_sel.sv rtl/arith/lazy_bfly_io.sv rtl/arith/modmul_barrett_lazy.sv rtl/arith/butterfly_c4_lazy.sv rtl/arith/butterfly_c4.sv rtl/mem/poly_mem_multiport_pipe.sv
     rtl/ntt/ntt_core_c4.sv"
lint_v() { verilator --lint-only -Wall $SRC "$@"; }
for w in "${wrappers[@]}" ntt_core_c4; do
    extra=""; [ "$w" != ntt_core_c4 ] && extra="rtl/ntt/$w.sv"
    step "V1 verilator --lint-only -Wall $w" lint_v $extra --top-module "$w"
    step "V1 slang $w" slang $SRC $extra --top "$w"
done
step "V2 exhaustive reducer (tb/arith/reducer_exhaustive)" tb/arith/reducer_exhaustive/run_reducer_exhaustive.sh 1 2 3
step "V2-lazy exhaustive Barrett lazy (tb/arith/lazy_exhaustive)" tb/arith/lazy_exhaustive/run_lazy_exhaustive.sh
step "V7 Montgomery ROM (tb/arith/check_mont_rom.py)" python3 tb/arith/check_mont_rom.py
for sim in verilator icarus; do
    step "V3/V4 unit tests $sim" python3 tb/arith/run_c4_unit_tests.py "$sim"
    step "V5/V6/V7 core tests $sim" python3 tb/arith/run_c4_core_tests.py "$sim"
done
[ "$overall" -eq 0 ] && echo "OVERALL: PASS" || echo "OVERALL: FAIL"
exit "$overall"
