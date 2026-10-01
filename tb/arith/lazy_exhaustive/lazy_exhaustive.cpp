// tb/arith/lazy_exhaustive/lazy_exhaustive.cpp
// Phase 5c test plan A4 V2-lazy (ADR 0014 §2): exhaustive check of rtl/arith/modmul_barrett_lazy.sv against
// (a * b) % 3329. Every pair a in [0, 4096), b in [0, 8192) is applied back-to-back, one per clock; the output is
// compared LATENCY cycles later.
//   required (ADR 0014):  0 mismatches for a < q, b < 2q   (3329 * 6658 = 22,164,482 pairs)
//   required (D6 subset): included in the above (b < q)    (reported separately)
//   reported (info):      mismatches for the other 12 x 13-bit pairs
// Usage: Vlazy_pair <latency>     exit code 0 only if the required domain has no mismatch.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <deque>
#include "Vlazy_pair.h"

static const uint32_t Q = 3329, MA = 4096, MB = 8192;

int main(int argc, char** argv) {
    if (argc != 2) { std::fprintf(stderr, "usage: %s latency\n", argv[0]); return 2; }
    const unsigned lat = std::strtoul(argv[1], nullptr, 10);
    Vlazy_pair top;
    struct Exp { uint32_t a, b; };
    std::deque<Exp> pipe;
    uint64_t checked = 0, in_lazy = 0, in_d6 = 0, mism_lazy = 0, mism_d6 = 0, mism_out = 0;
    const uint64_t total = (uint64_t)MA * MB;
    top.clk_i = 0; top.a_i = 0; top.b_i = 0; top.eval();
    for (uint64_t n = 0; n < total + lat; ++n) {
        const bool live = n < total;
        const uint32_t a = live ? (uint32_t)(n / MB) : 0, b = live ? (uint32_t)(n % MB) : 0;
        top.a_i = a; top.b_i = b;
        top.eval();
        if (live) pipe.push_back({a, b});
        if ((live && pipe.size() == lat + 1) || (!live && !pipe.empty())) {
            const Exp e = pipe.front(); pipe.pop_front();
            const uint32_t formula = (e.a * e.b) % Q;
            const bool lz = e.a < Q && e.b < 2 * Q, d6 = e.a < Q && e.b < Q;
            ++checked; if (lz) ++in_lazy; if (d6) ++in_d6;
            if (top.dut_o != formula) {
                if (lz) {
                    if (mism_lazy < 10) std::printf("MISMATCH a=%u b=%u dut=%u formula=%u\n", e.a, e.b,
                                                    (unsigned)top.dut_o, formula);
                    ++mism_lazy; if (d6) ++mism_d6;
                } else {
                    ++mism_out;
                }
            }
        }
        top.clk_i = 1; top.eval();
        top.clk_i = 0; top.eval();
    }
    std::printf("latency=%u pairs_checked=%llu lazy_domain(a<q,b<2q)=%llu mismatches_lazy=%llu "
                "d6_subset(a,b<q)=%llu mismatches_d6=%llu mismatches_other(info)=%llu\n", lat,
                (unsigned long long)checked, (unsigned long long)in_lazy, (unsigned long long)mism_lazy,
                (unsigned long long)in_d6, (unsigned long long)mism_d6, (unsigned long long)mism_out);
    return (mism_lazy == 0 && checked == total && in_lazy == (uint64_t)Q * 2 * Q) ? 0 : 1;
}
