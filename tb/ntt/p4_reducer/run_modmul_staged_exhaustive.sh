#!/usr/bin/env bash
# tb/ntt/p4_reducer/run_modmul_staged_exhaustive.sh
# Phase 4 test plan V2: builds and runs the exhaustive modmul_reduce_staged vs modmul_reduce check for
# every register configuration used by the P sweep, plus the purely combinational one.
#   REG_AFTER    8 (cut D_3)            latency 1   -> P = 2
#   REG_AFTER  129 (cuts X, D_7)        latency 2   -> P = 4
#   REG_AFTER 2081 (cuts X, D_5, D_11)  latency 3   -> P = 6
#   REG_AFTER    0                      latency 0   -> no registers
# Exit code 0 only if every configuration reports 0 mismatches over all 4096^2 pairs.
# Usage: . scripts/env.sh && tb/ntt/p4_reducer/run_modmul_staged_exhaustive.sh
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
rtl="$here/../../../rtl/ntt"
fail=0
for cfg in "0 0" "8 1" "129 2" "2081 3"; do
    set -- $cfg; reg=$1; lat=$2
    build="$here/sim_build_modmul_staged_$reg"
    rm -rf "$build"
    verilator --cc --exe --build -O3 --x-assign fast --x-initial fast --no-timing -Wno-fatal \
        -CFLAGS "-O3" --Mdir "$build" --top-module modmul_staged_pair -GREG_AFTER="$reg" \
        "$rtl/ntt_pkg.sv" "$rtl/modmul_reduce.sv" "$rtl/modmul_reduce_staged.sv" \
        "$here/modmul_staged_pair.sv" "$here/modmul_staged_exhaustive.cpp" > "$build.log" 2>&1 \
        || { cat "$build.log"; exit 2; }
    mv "$build.log" "$build/build.log"
    printf 'REG_AFTER=%-5s ' "$reg"
    "$build/Vmodmul_staged_pair" "$lat" || fail=1
done
[ "$fail" -eq 0 ] && echo "RESULT: PASS" || { echo "RESULT: FAIL"; exit 1; }
