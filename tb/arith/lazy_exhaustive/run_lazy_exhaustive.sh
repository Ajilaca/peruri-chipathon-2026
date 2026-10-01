#!/usr/bin/env bash
# tb/arith/lazy_exhaustive/run_lazy_exhaustive.sh
# Phase 5c test plan A4 V2-lazy / V10: exhaustive check of rtl/arith/modmul_barrett_lazy.sv over every 12-bit a and
# 13-bit b (required: a < q, b < 2q), at REG_AFTER 0 and 7 (cuts X, S1, S2), plus a negative control (t*(q-1) instead
# of t*q in a copy of the RTL, build folder only) that must FAIL.
# Exit code 0 only if both real configurations pass and the negative control fails.
# Usage: . scripts/env.sh && tb/arith/lazy_exhaustive/run_lazy_exhaustive.sh
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$here/../../.."
rtl="$root/rtl/arith/modmul_barrett_lazy.sv"
fail=0
build_run() {  # reg lat rtlfile label
    local build="$here/sim_build_lazy_$1_$4"
    rm -rf "$build"
    verilator --cc --exe --build -O3 --x-assign fast --x-initial fast --no-timing -Wno-fatal -CFLAGS "-O3" \
        --Mdir "$build" --top-module lazy_pair -GREG_AFTER="$1" "$root/rtl/ntt/ntt_pkg.sv" "$3" \
        "$here/lazy_pair.sv" "$here/lazy_exhaustive.cpp" > "$build.log" 2>&1 || { cat "$build.log"; exit 2; }
    mv "$build.log" "$build/build.log"
    printf 'REG_AFTER=%-2s %-16s ' "$1" "$4"
    "$build/Vlazy_pair" "$2"
}
build_run 0 0 "$rtl" real || fail=1
build_run 7 3 "$rtl" real || fail=1
neg="$here/neg_barrett_lazy.sv"
sed -e "s/ + (PW'(t2) << 8) + PW'(t2);/ + (PW'(t2) << 8);/" "$rtl" > "$neg"
cmp -s "$neg" "$rtl" && { echo "negative control did not change the RTL"; exit 2; }
if build_run 7 3 "$neg" negative_control; then echo "NEGATIVE CONTROL PASSED (harness void)"; fail=1
else echo "negative control failed as required"; fi
rm -f "$neg"
[ "$fail" -eq 0 ] && echo "RESULT: PASS" || { echo "RESULT: FAIL"; exit 1; }
