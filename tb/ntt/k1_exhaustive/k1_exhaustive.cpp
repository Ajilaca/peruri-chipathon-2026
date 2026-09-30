// tb/ntt/k1_exhaustive/k1_exhaustive.cpp
// Experiment K1, equivalence option 2: exhaustive RTL simulation. For every mode in {0,1} and every
// a, b, zeta in [0, Q) within the given a-range, evaluates rtl/ntt/butterfly.sv and
// rtl/ntt/butterfly_shared.sv (Verilated, unchanged RTL) and checks three-way agreement with the
// FIPS 203 Algorithm 9/10 butterfly step computed here in plain integer arithmetic.
// Usage: Vk1_butterfly_pair <a_begin> <a_end>     (a in [a_begin, a_end))
// Prints "RANGE a=[..) evals=<n> mismatches=<m>"; exit code 0 only if m == 0.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include "Vk1_butterfly_pair.h"

static const uint32_t Q = 3329;

int main(int argc, char** argv) {
    if (argc != 3) { std::fprintf(stderr, "usage: %s a_begin a_end\n", argv[0]); return 2; }
    const uint32_t a0 = std::strtoul(argv[1], nullptr, 10), a1 = std::strtoul(argv[2], nullptr, 10);
    if (a0 > a1 || a1 > Q) { std::fprintf(stderr, "bad range\n"); return 2; }
    Vk1_butterfly_pair top;
    uint64_t evals = 0, mism = 0;
    for (uint32_t mode = 0; mode < 2; ++mode) {
        top.mode_i = mode;
        for (uint32_t a = a0; a < a1; ++a) {
            top.a_i = a;
            for (uint32_t b = 0; b < Q; ++b) {
                top.b_i = b;
                const uint32_t diff = (b + Q - a) % Q;      // (b - a) mod q, inverse operand
                const uint32_t sum  = (a + b) % Q;
                for (uint32_t z = 0; z < Q; ++z) {
                    top.zeta_i = z;
                    top.eval();
                    uint32_t ga, gb;
                    if (mode == 0) { const uint32_t t = (z * b) % Q; ga = (a + t) % Q; gb = (a + Q - t) % Q; }
                    else           { ga = sum; gb = (z * diff) % Q; }
                    ++evals;
                    if (top.ref_a_o != ga || top.ref_b_o != gb || top.dut_a_o != ga || top.dut_b_o != gb) {
                        if (mism < 10)
                            std::printf("MISMATCH mode=%u a=%u b=%u zeta=%u golden=(%u,%u) ref=(%u,%u) dut=(%u,%u)\n",
                                        mode, a, b, z, ga, gb, (unsigned)top.ref_a_o, (unsigned)top.ref_b_o,
                                        (unsigned)top.dut_a_o, (unsigned)top.dut_b_o);
                        ++mism;
                    }
                }
            }
        }
    }
    std::printf("RANGE a=[%u,%u) evals=%llu mismatches=%llu\n", a0, a1,
                (unsigned long long)evals, (unsigned long long)mism);
    return mism == 0 ? 0 : 1;
}
