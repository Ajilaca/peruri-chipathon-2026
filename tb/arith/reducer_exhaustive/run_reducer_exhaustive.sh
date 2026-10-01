#!/usr/bin/env bash
# tb/arith/reducer_exhaustive/run_reducer_exhaustive.sh
# Phase 5 test plan V2 / V10: exhaustive check of the Phase 5 reducers against the frozen modmul_reduce.sv,
# for every register configuration used, plus negative controls (a deliberately wrong copy of the RTL, built in
# the build folder only, must FAIL; if it passes, the harness is void).
# Kinds use the RED_KIND numbering of rtl/arith/modmul_sel.sv:
#   kind 1 = rtl/arith/modmul_fold.sv (5a):        REG_AFTER 0 (combinational), 41 = cuts X, F3, F5 (latency 3, P = 6)
#   kind 2 = rtl/arith/modmul_barrett.sv (5b):     REG_AFTER 0, 7 = cuts X, S1, S2 (latency 3)
#   kind 3 = rtl/arith/modmul_montgomery.sv (5b):  REG_AFTER 0, 7 (b driven in Montgomery form by the TB wrapper)
# Exit code 0 only if every real configuration passes and every negative control fails.
# Usage: . scripts/env.sh && tb/arith/reducer_exhaustive/run_reducer_exhaustive.sh [kind ...]
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="$here/../../.."
kinds=("${@:-1}")
fail=0

src_of() {   # kind -> RTL file of the reducer
    case "$1" in
        1) echo "$root/rtl/arith/modmul_fold.sv" ;;
        2) echo "$root/rtl/arith/modmul_barrett.sv" ;;
        3) echo "$root/rtl/arith/modmul_montgomery.sv" ;;
        *) echo "unknown kind $1" >&2; exit 2 ;;
    esac
}
cfgs_of() {  # kind -> "REG_AFTER latency" pairs
    case "$1" in
        1) echo "0:0 41:3" ;;
        2|3) echo "0:0 7:3" ;;
    esac
}
break_of() { # kind -> sed expression that makes a wrong copy (negative control)
    case "$1" in
        1) echo 's/- (h << 8) - h + l;/- (h << 8) + l;/' ;;   # 768*h + l instead of 767*h + l
        2) echo 's/ + (PW'"'"'(t2) << 8) + PW'"'"'(t2);/ + (PW'"'"'(t2) << 8);/' ;;   # t*(q-1) instead of t*q
        3) echo 's/((xl << 9) + (xl << 8) + xl)/((xl << 9) + (xl << 8))/' ;;    # wrong q'
    esac
}

reducer_sources() {  # kind, file to use for that kind -> every source modmul_sel needs
    local all="$root/rtl/ntt/ntt_pkg.sv $root/rtl/ntt/modmul_reduce.sv $root/rtl/ntt/modmul_reduce_staged.sv"
    local f
    for f in $root/rtl/arith/modmul_fold.sv $root/rtl/arith/modmul_barrett.sv $root/rtl/arith/modmul_montgomery.sv; do
        [ "$f" = "$(src_of "$1")" ] && all="$all $2" || all="$all $f"
    done
    echo "$all $root/rtl/arith/modmul_sel.sv $root/tb/arith/c4_tb_wrappers.sv"
}

build_run() {  # kind reg lat rtlfile label -> 0 if the harness reports PASS
    local kind=$1 reg=$2 lat=$3 rtl=$4 label=$5
    local build="$here/sim_build_k${kind}_${reg}_${label}"
    rm -rf "$build"
    verilator --cc --exe --build -O3 --x-assign fast --x-initial fast --no-timing -Wno-fatal \
        -CFLAGS "-O3" --Mdir "$build" --top-module reducer_pair -GKIND="$kind" -GREG_AFTER="$reg" \
        $(reducer_sources "$kind" "$rtl") "$here/reducer_pair.sv" "$here/reducer_exhaustive.cpp" > "$build.log" 2>&1 \
        || { cat "$build.log"; exit 2; }
    mv "$build.log" "$build/build.log"
    printf 'kind=%s REG_AFTER=%-4s %-16s ' "$kind" "$reg" "$label"
    "$build/Vreducer_pair" "$lat"
}

for kind in "${kinds[@]}"; do
    rtl="$(src_of "$kind")"
    for cfg in $(cfgs_of "$kind"); do
        reg=${cfg%%:*}; lat=${cfg##*:}
        build_run "$kind" "$reg" "$lat" "$rtl" real || fail=1
    done
    # negative control at the latency-3 configuration: wrong copy must fail
    neg="$here/neg_k${kind}.sv"
    sed -e "$(break_of "$kind")" "$rtl" > "$neg"
    if cmp -s "$neg" "$rtl"; then echo "negative control for kind $kind did not change the RTL"; exit 2; fi
    cfg=$(cfgs_of "$kind" | tr ' ' '\n' | tail -1); reg=${cfg%%:*}; lat=${cfg##*:}
    if build_run "$kind" "$reg" "$lat" "$neg" negative_control; then
        echo "NEGATIVE CONTROL PASSED (harness void)"; fail=1
    else
        echo "negative control failed as required"
    fi
    rm -f "$neg"
done
[ "$fail" -eq 0 ] && echo "RESULT: PASS" || { echo "RESULT: FAIL"; exit 1; }
