#!/usr/bin/env bash
# scripts/phase8b_verify.sh -- Phase 8b verification (docs/evidence/phase08-keccak-stream/8b/test_plan_8b.md V1-V10), both simulators.
# V10 regression: scripts/phase8a_verify.sh (which runs scripts/phase7_verify.sh first) and the formal runs of Phases 7 and 8a, unless KS_REGRESS=0.
# V9 (formal for the samplers) is formal/run_formal_phase8b.py, run here at the end. KS_OUTW selects the output width under test (1 = stage W1, 2 = stage W2); the W1 test set is rerun in stage W2 with KS_OUTW=1.
# Usage: . scripts/env.sh && scripts/phase8b_verify.sh
set -u
cd "$(dirname "${BASH_SOURCE[0]}")/.."
export KS_BUILD_DIR="${KS_BUILD_DIR:-$(mktemp -d -t chip2026_8b_XXXX)}"
export KS_OUTW="${KS_OUTW:-1}"
export KS_N="${KS_N:-500}"
export KS_CYCLES_OUT_DIR="${KS_CYCLES_OUT_DIR:-$KS_BUILD_DIR}"
overall=0
step() {
    local h=$1; shift
    echo "## $h"
    "$@" 2>&1 | grep -E "^\[(icarus|verilator)\]|passed|failed|^%Error|^%Warning|Build succeeded|errors|differences|all locked|OVERALL|ALL AS EXPECTED|UNEXPECTED|^\| |cocotb\.(sample_ntt_core|cbd2_core|keccak_sampler) " | grep -v "^\s*$"
    local rc=${PIPESTATUS[0]}
    echo "rc=$rc"
    [ "$rc" -eq 0 ] || overall=1
}
KECCAK="rtl/keccak/keccak_pkg.sv rtl/keccak/keccak_round.sv rtl/keccak/keccak_f1600.sv rtl/keccak/keccak_sponge.sv rtl/keccak/keccak_f1600_r2.sv rtl/keccak/keccak_sponge_r2.sv"
SMP="rtl/sample/sample_ntt_core.sv rtl/sample/cbd2_core.sv rtl/sample/keccak_sampler.sv"
echo "KS_OUTW=$KS_OUTW KS_N=$KS_N"
if [ "${KS_REGRESS:-1}" != "0" ]; then
    step "V10 regression: scripts/phase8a_verify.sh (K0 and C5)" scripts/phase8a_verify.sh
    step "V10 regression: formal/run_formal_phase7.py" python3 formal/run_formal_phase7.py
    step "V10 regression: formal/run_formal_phase8a.py" python3 formal/run_formal_phase8a.py
fi
step "V1 verilator --lint-only -Wall sample_ntt_core (OUTW = $KS_OUTW)" verilator --lint-only -Wall -GOUTW=$KS_OUTW rtl/sample/sample_ntt_core.sv --top-module sample_ntt_core
step "V1 verilator --lint-only -Wall cbd2_core (OUTW = $KS_OUTW)" verilator --lint-only -Wall -GOUTW=$KS_OUTW rtl/sample/cbd2_core.sv --top-module cbd2_core
step "V1 verilator --lint-only -Wall keccak_sampler (CORE_R2 = 1, OUTW = $KS_OUTW)" verilator --lint-only -Wall -GCORE_R2=1 -GOUTW=$KS_OUTW $KECCAK $SMP --top-module keccak_sampler
step "V1 verilator --lint-only -Wall keccak_sampler (CORE_R2 = 0, OUTW = $KS_OUTW)" verilator --lint-only -Wall -GCORE_R2=0 -GOUTW=$KS_OUTW $KECCAK $SMP --top-module keccak_sampler
step "V1 slang keccak_sampler (OUTW = $KS_OUTW)" slang -G OUTW=$KS_OUTW $KECCAK $SMP --top keccak_sampler
step "V2 golden sampler model against the unmodified golden primitives" python3 -m pytest -q tb/golden/tests/test_sampler_model.py
for sim in verilator icarus; do
    step "V3-V8 $sim (OUTW = $KS_OUTW)" python3 tb/sample/run_sample_tests.py "$sim"
done
if [ "$KS_OUTW" = "2" ]; then
    for sim in verilator icarus; do
        step "V10 rerun of the W1 test set against the current RTL (OUTW = 1) $sim" env KS_OUTW=1 python3 tb/sample/run_sample_tests.py "$sim"
    done
fi
step "V9 formal: formal/run_formal_phase8b.py (W1 and W2 rows)" python3 formal/run_formal_phase8b.py all
[ "$overall" -eq 0 ] && echo "OVERALL: PASS" || echo "OVERALL: FAIL"
exit "$overall"
