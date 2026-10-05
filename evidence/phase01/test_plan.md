# Phase 1 test plan - NTT/INTT baseline (C0), written before any test is coded (CRG-4)

Scope: `rtl/ntt/modmul_reduce.sv`, `rtl/ntt/base_case_multiply.sv`, `rtl/ntt/butterfly.sv`,
`rtl/ntt/twiddle_rom.sv`, `rtl/ntt/poly_mem.sv`, `rtl/ntt/ntt_core.sv`. Reference: `tb/golden/primitives.py`
(`ntt`, `intt`, `base_case_multiply`). No RTL below was written before this plan.

## Unit: modmul_reduce (a*b mod q)

- Exhaustive is 3329² ≈ 11.08M pairs - too slow for per-commit cocotb, so Phase 1 uses randomized
  coverage; the exhaustive sweep required by Phase 5 (`docs/ROADMAP.md` §5) is deferred there.
- Corner cases: a=0, b=0; a=q-1, b=q-1 (max product); a=1, b=anything (identity); a=q-1, b=1.
- 2000 random pairs a,b ∈ [0,q).

## Unit: base_case_multiply (Algorithm 12)

- Corner cases: all-zero inputs; a0=a1=q-1, b0=b1=q-1; gamma=0; gamma=q-1; gamma = an actual
  ζ^(2·BitRev7(i)+1) value taken from the golden model (i=0 and i=127, the two ends of the table).
- 500 random (a0,a1,b0,b1,gamma) tuples, gamma restricted to real values from the golden model's
  `_GAMMA` table (never an arbitrary value, since real hardware only ever uses those 128 constants).

## Unit: butterfly (CT forward / GS inverse)

- Corner cases: a=0,b=0; a=q-1,b=q-1; zeta=1 (i=0 entry, unused in practice but must not corrupt
  math if ever driven); zeta = the largest tabulated value; a=0,b=q-1 and a=q-1,b=0 (boundary of the
  subtraction-then-add-q path).
- 1000 random (a,b,zeta) tuples per mode (forward, inverse), zeta restricted to the golden model's
  `_ZETA_BITREV` table.

## Unit: ntt_core (top-level FSM, both directions)

- Corner cases (fed as the full 256-coefficient input polynomial):
  1. All-zero polynomial.
  2. All coefficients = q-1 (max value).
  3. Impulse: f[0]=1, rest 0.
  4. Impulse at the last coefficient: f[255]=1, rest 0.
  5. Alternating 0 / q-1.
  6. A polynomial whose NTT is itself an all-zero or all-(q-1) pattern is not assumed; only
     literal input patterns are used as corner cases, per the rule against inventing vectors.
- Property tests, cross-checked against `tb/golden/primitives.py` bit-exact:
  - `ntt(f)` matches `primitives.ntt(f)` for every corner case and 100 random polynomials.
  - `intt(f_hat)` matches `primitives.intt(f_hat)` for every corner case and 100 random polynomials.
  - `intt(ntt(f)) == f` for 50 random polynomials (round-trip through the RTL itself, not just
    each direction separately).
- **Constant-cycle check (CRG-7):** run `ntt_core` on every corner case and 20 random polynomials in
  the *same direction*; the number of clock cycles from `start_i` to `done_o` must be identical for
  all of them (the algorithm has no data-dependent branch, so this must hold by construction; the
  test makes that an explicit, logged fact rather than an assumption).
- Run twice: once under Verilator, once under Icarus Verilog (CRG-3); a mismatch between the two is
  investigated before trusting either result.

## Formal (CRG-8, SymbiYosys)

- FSM reaches `done_o` from any legal reset state within a bounded number of cycles (`cover`), and
  never deasserts `busy_o` without having asserted `done_o` for exactly one cycle first.
- All addresses driven into `poly_mem` (`j`, `j+len` for the butterfly pass; the scan address for the
  INTT scaling pass) stay in `[0, 255]` for every reachable state (`assert`).

## Explicitly out of scope for Phase 1 (see docs/ROADMAP.md "Not allowed yet")

Memory banking or multiple lanes, pipelining beyond one butterfly per cycle, Montgomery/Barrett
reduction, lazy reduction, Karatsuba, Keccak, HPS integration, any performance/speed-up claim.
