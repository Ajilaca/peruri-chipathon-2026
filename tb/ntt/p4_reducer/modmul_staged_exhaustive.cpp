// tb/ntt/p4_reducer/modmul_staged_exhaustive.cpp
// Phase 4 test plan V2: exhaustive check that rtl/ntt/modmul_reduce_staged.sv computes exactly what the
// frozen rtl/ntt/modmul_reduce.sv computes. Every 12-bit pair (a, b) in [0, 4096)^2 (a superset of the
// operand range [0, 3329) the design uses) is applied back-to-back, one pair per clock, and the staged
// output is compared, LATENCY cycles later, with (1) modmul_reduce's output for that pair and (2) the
// integer formula (a*b) % 3329. Also reports the sub-range a, b < 3329 separately.
// Usage: Vmodmul_staged_pair <latency>     exit code 0 only if there are no mismatches.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <deque>
#include "Vmodmul_staged_pair.h"

static const uint32_t Q = 3329, M = 4096;

int main(int argc, char** argv) {
    if (argc != 2) { std::fprintf(stderr, "usage: %s latency\n", argv[0]); return 2; }
    const unsigned lat = std::strtoul(argv[1], nullptr, 10);
    Vmodmul_staged_pair top;
    struct Exp { uint32_t a, b, ref; };
    std::deque<Exp> pipe;
    uint64_t checked = 0, checked_inrange = 0, mism = 0, ref_vs_formula = 0;
    const uint64_t total = (uint64_t)M * M;
    top.clk_i = 0; top.a_i = 0; top.b_i = 0; top.eval();
    for (uint64_t n = 0; n < total + lat; ++n) {
        const bool live = n < total;
        const uint32_t a = live ? (uint32_t)(n / M) : 0, b = live ? (uint32_t)(n % M) : 0;
        top.a_i = a; top.b_i = b;
        top.eval();                                   // combinational view of this cycle's inputs
        if (live) {
            const uint32_t formula = (a * b) % Q;
            if (top.ref_o != formula) ++ref_vs_formula;
            pipe.push_back({a, b, (uint32_t)top.ref_o});
        }
        if (pipe.size() > lat || (!live && !pipe.empty())) {
            // the pair applied `lat` cycles ago is now visible on dut_o (before this cycle's edge)
            if ((live && pipe.size() == lat + 1) || !live) {
                const Exp e = pipe.front(); pipe.pop_front();
                const uint32_t formula = (e.a * e.b) % Q;
                ++checked;
                if (e.a < Q && e.b < Q) ++checked_inrange;
                if (top.dut_o != e.ref || top.dut_o != formula) {
                    if (mism < 10)
                        std::printf("MISMATCH a=%u b=%u staged=%u modmul_reduce=%u formula=%u\n",
                                    e.a, e.b, (unsigned)top.dut_o, e.ref, formula);
                    ++mism;
                }
            }
        }
        top.clk_i = 1; top.eval();                    // rising edge: registers capture
        top.clk_i = 0; top.eval();
    }
    std::printf("latency=%u pairs_checked=%llu (of which a,b<3329: %llu) mismatches=%llu "
                "modmul_reduce_vs_formula_mismatches=%llu\n", lat, (unsigned long long)checked,
                (unsigned long long)checked_inrange, (unsigned long long)mism,
                (unsigned long long)ref_vs_formula);
    return (mism == 0 && ref_vs_formula == 0 && checked == total) ? 0 : 1;
}
