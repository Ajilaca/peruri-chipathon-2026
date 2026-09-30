#!/usr/bin/env bash
# tb/ntt/k1_exhaustive/run_k1_exhaustive.sh
# Experiment K1, equivalence option 2: builds the Verilator harness and runs the exhaustive
# butterfly.sv vs butterfly_shared.sv vs golden comparison over all 2 * 3329^3 inputs, split over
# JOBS processes by the range of `a`. Exit code 0 only if every range reports 0 mismatches and the
# total number of evaluations is exactly 2 * 3329^3.
# Usage: . scripts/env.sh && tb/ntt/k1_exhaustive/run_k1_exhaustive.sh [JOBS]   (default: nproc)
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
rtl="$here/../../../rtl/ntt"
build="$here/sim_build_k1_exhaustive"
jobs="${1:-$(nproc)}"
Q=3329

rm -rf "$build"
verilator --cc --exe --build -O3 --x-assign fast --x-initial fast --no-timing -Wno-fatal \
    -CFLAGS "-O3" --Mdir "$build" --top-module k1_butterfly_pair \
    "$rtl/ntt_pkg.sv" "$rtl/modmul_reduce.sv" "$rtl/butterfly.sv" "$rtl/butterfly_shared.sv" \
    "$here/k1_butterfly_pair.sv" "$here/k1_exhaustive.cpp" > "$build.build.log" 2>&1 \
    || { cat "$build.build.log"; exit 2; }
mv "$build.build.log" "$build/build.log"

start=$(date +%s)
pids=()
for ((i = 0; i < jobs; i++)); do
    lo=$((i * Q / jobs)); hi=$(((i + 1) * Q / jobs))
    "$build/Vk1_butterfly_pair" "$lo" "$hi" > "$build/range_$i.log" 2>&1 &
    pids+=($!)
done
fail=0
for p in "${pids[@]}"; do wait "$p" || fail=1; done

cat "$build"/range_*.log | sort -t'[' -k2 -n
evals=$(cat "$build"/range_*.log | sed -n 's/.*evals=\([0-9]*\) .*/\1/p' | paste -sd+ | bc)
mism=$(cat "$build"/range_*.log | sed -n 's/.*mismatches=\([0-9]*\).*/\1/p' | paste -sd+ | bc)
expect=$((2 * Q * Q * Q))
echo "TOTAL evals=$evals expected=$expect mismatches=$mism jobs=$jobs wall_seconds=$(( $(date +%s) - start ))"
[ "$fail" -eq 0 ] && [ "$evals" = "$expect" ] && [ "$mism" = "0" ] && echo "RESULT: PASS" || { echo "RESULT: FAIL"; exit 1; }
