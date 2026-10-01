// tb/arith/reducer_exhaustive/reducer_exhaustive.cpp
// Phase 5 test plan V2 (docs/evidence/phase05-arith/test_plan.md section 7, ADR 0011 D6): exhaustive check of a
// Phase 5 reducer (selected in reducer_pair.sv) against the frozen rtl/ntt/modmul_reduce.sv and the integer
// formula (a*b) % 3329. Same driving scheme as tb/ntt/p4_reducer/modmul_staged_exhaustive.cpp: every 12-bit pair
// (a, b) in [0, 4096)^2 is applied back-to-back, one pair per clock, and the reducer's output is compared LATENCY
// cycles later.
//   required  (V2):      0 mismatches over a, b in [0, 3329)  (3329^2 = 11,082,241 pairs)
//   reported  (V2-info): mismatches over the remaining 12-bit pairs (a >= 3329 or b >= 3329)
// The reference itself is checked against the formula for every pair.
// Usage: Vreducer_pair <latency>     exit code 0 only if V2 holds and the reference matches the formula.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <deque>
#include "Vreducer_pair.h"

static const uint32_t Q = 3329, M = 4096;

int main(int argc, char** argv) {
    if (argc != 2) { std::fprintf(stderr, "usage: %s latency\n", argv[0]); return 2; }
    const unsigned lat = std::strtoul(argv[1], nullptr, 10);
    Vreducer_pair top;
    struct Exp { uint32_t a, b, ref; };
    std::deque<Exp> pipe;
    uint64_t checked = 0, checked_in = 0, mism_in = 0, mism_out = 0, ref_vs_formula = 0;
    const uint64_t total = (uint64_t)M * M;
    top.clk_i = 0; top.a_i = 0; top.b_i = 0; top.eval();
    for (uint64_t n = 0; n < total + lat; ++n) {
        const bool live = n < total;
        const uint32_t a = live ? (uint32_t)(n / M) : 0, b = live ? (uint32_t)(n % M) : 0;
        top.a_i = a; top.b_i = b;
        top.eval();                                   // combinational view of this cycle's inputs
        if (live) {
            if (top.ref_o != (a * b) % Q) ++ref_vs_formula;
            pipe.push_back({a, b, (uint32_t)top.ref_o});
        }
        if ((live && pipe.size() == lat + 1) || (!live && !pipe.empty())) {
            // the pair applied `lat` cycles ago is now visible on dut_o (before this cycle's edge)
            const Exp e = pipe.front(); pipe.pop_front();
            const uint32_t formula = (e.a * e.b) % Q;
            const bool in = e.a < Q && e.b < Q;
            ++checked;
            if (in) ++checked_in;
            if (top.dut_o != e.ref || top.dut_o != formula) {
                if (in) {
                    if (mism_in < 10)
                        std::printf("MISMATCH a=%u b=%u dut=%u modmul_reduce=%u formula=%u\n",
                                    e.a, e.b, (unsigned)top.dut_o, e.ref, formula);
                    ++mism_in;
                } else {
                    ++mism_out;
                }
            }
        }
        top.clk_i = 1; top.eval();                    // rising edge: registers capture
        top.clk_i = 0; top.eval();
    }
    std::printf("latency=%u pairs_checked=%llu in_range(a,b<3329)=%llu mismatches_in_range=%llu "
                "mismatches_out_of_range(info)=%llu modmul_reduce_vs_formula_mismatches=%llu\n", lat,
                (unsigned long long)checked, (unsigned long long)checked_in, (unsigned long long)mism_in,
                (unsigned long long)mism_out, (unsigned long long)ref_vs_formula);
    return (mism_in == 0 && ref_vs_formula == 0 && checked == total && checked_in == (uint64_t)Q * Q) ? 0 : 1;
}
