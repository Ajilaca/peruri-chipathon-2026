#!/usr/bin/env bash
# scripts/phase9a_verify.sh -- Phase 9a verification (docs/evidence/phase09-integration/9a/test_plan_9a.md V1-V9, V11), both simulators.
# V9 (formal) is formal/run_formal_phase9a.py, run at the end unless P9A_FORMAL=0 (the two BMC control runs at depth 300 take about 10 minutes each).
# Usage: . scripts/env.sh && scripts/phase9a_verify.sh
set -u
cd "$(dirname "${BASH_SOURCE[0]}")/.."
export CT_BUILD_DIR="${CT_BUILD_DIR:-$(mktemp -d -t chip2026_9a_XXXX)}"
export CT_CYCLES_OUT_DIR="${CT_CYCLES_OUT_DIR:-$CT_BUILD_DIR}"
overall=0
step() {
    local h=$1; shift
    echo "## $h"
    "$@" 2>&1 | grep -E "^\[(icarus|verilator)\]|passed|failed|^%Error|^%Warning|Build succeeded|errors|ALL AS EXPECTED|UNEXPECTED|^\| |cycles per polynomial" | grep -v "^\s*$"
    local rc=${PIPESTATUS[0]}
    echo "rc=$rc"
    [ "$rc" -eq 0 ] || overall=1
}
M="rtl/mlkem/mlkem_pack.sv rtl/mlkem/mlkem_unpack.sv rtl/mlkem/mlkem_codec_top.sv"
step "V1 verilator --lint-only -Wall mlkem_pack" verilator --lint-only -Wall rtl/mlkem/mlkem_pack.sv --top-module mlkem_pack
step "V1 verilator --lint-only -Wall mlkem_unpack" verilator --lint-only -Wall rtl/mlkem/mlkem_unpack.sv --top-module mlkem_unpack
step "V1 verilator --lint-only -Wall mlkem_codec_top" verilator --lint-only -Wall $M --top-module mlkem_codec_top
step "V1 slang mlkem_codec_top" slang $M --top mlkem_codec_top
step "V2 golden codec model against the unmodified golden primitives" python3 -m pytest -q tb/golden/tests/test_codec_model.py
for sim in verilator icarus; do
    step "V3-V8, V11 $sim" python3 tb/mlkem/run_codec_tests.py "$sim"
done
if [ "${P9A_FORMAL:-1}" != "0" ]; then
    step "V9 formal: formal/run_formal_phase9a.py" python3 formal/run_formal_phase9a.py all
fi
[ "$overall" -eq 0 ] && echo "OVERALL: PASS" || echo "OVERALL: FAIL"
exit "$overall"
