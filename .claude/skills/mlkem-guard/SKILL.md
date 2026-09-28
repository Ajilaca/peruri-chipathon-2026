---
name: mlkem-guard
description: Guardrails for designing, modelling, or reviewing the ML-KEM-768 (FIPS 203) accelerator, covering locked parameters, NTT structure, Keccak, constant-time rules, golden model and known-answer-test process, and Cyclone V mapping. Use for any work on NTT/INTT, butterfly, Keccak/SHAKE, sampler, compress/encode, FO transform, KAT vectors, or when the user proposes changing a modulus, root, or arithmetic.
---

# mlkem-guard

**The mathematics is locked; the architecture is free.** (ADR 0002.) We implement the
standard scheme exactly. Innovation happens in the hardware architecture, never in the
cryptography. Changing q, n, the root of unity, the sampling distribution or the
compression parameters produces a *different, unproven scheme* and voids the security
argument; it also fails the proposal's claim of FIPS 203 conformance. If the user
suggests such a change, explain this and offer an architectural alternative.

## Locked parameters (ML-KEM-768)

| Item | Value | Status |
|---|---|---|
| q, n | 3329, 256 | verified (IETF draft-cfrg-schwabe-kyber-03) |
| Root of unity | ζ = 17 (order 256 mod q) | verified (tcgcrest notes; 17^128 ≡ −1 mod q checked) |
| k, η1, η2, du, dv | 3, 2, 2, 10, 4 | FIPS 203 Table 2; **re-confirm in Phase 0** |
| Sizes (bytes) | ek 1184, dk 2400, ct 1088, ss 32 | verified (IETF draft-sfluhrer Table 1) |

Machine check: `python3 .claude/skills/mlkem-guard/scripts/check_params.py`
(reads `tb/golden/params.py` with `ast`; mismatch = exit 1). Keep those constants in that
file with exactly these names: `Q N ZETA K ETA1 ETA2 DU DV EK_BYTES DK_BYTES CT_BYTES SS_BYTES`.

## Structure you must respect

- Ring R_q = Z_q[X]/(X^256+1). **N must stay a power of two**: X^N+1 is the clean
  cyclotomic polynomial only then, and the radix-2 butterfly needs repeated halving.
- **The NTT is "incomplete"**: 256 divides q−1 but 512 does not, so X^256+1 splits only
  into 128 *quadratic* factors. Consequences: 7 butterfly layers (not 8), and the
  "pointwise" product is a product of degree-1 binomials modulo (X² − ζ^j), not scalar
  multiplication. Building an 8-layer NTT or scalar pointwise product is a bug.
- Keccak-f[1600] underlies SHA3-256/512 and SHAKE128/256. Software spends >50% of cycles
  there, and once Keccak is accelerated the critical path moves to NTT [refs 14, 15 in the
  proposal]. Both blocks are in scope.
- Coefficients are 12 bits (< 3329); a polynomial is 256 x 12 = 3,072 bits.
  Cyclone V DSP blocks offer 18x18 mode (two per block), which fits 12x12 products.

## Constant-time rules (the proposal's core claim)

1. No branch, address, or loop count may depend on secret data (s, e, r, m, dk, K).
2. No division or modulo operator on secret data. Use multiply-by-constant and shifts for
   Compress/Decompress and Barrett/Montgomery reduction. (Division on secrets caused
   KyberSlash.)
3. Rejection sampling of matrix **A** depends only on the public seed ρ, so its variable
   length is acceptable; CBD sampling of secrets is fixed-time.
4. Decaps: re-encrypt, compare ciphertexts in constant time, and select K or the
   implicit-rejection key with a mux/mask, not a branch.
5. **Prove it, do not assume it**: the cycle count of every operation must be identical
   across inputs (test with random and adversarial inputs, including failure-path
   ciphertexts). Record it as evidence.
6. Constant-time is not side-channel resistance. Do not claim power/EM protection; that
   is later stage (TVLA, masking).

## Verification process

1. **Golden model first** (`tb/golden/`, Python, independent of RTL). Cross-check it
   against at least one independent implementation and official NIST known-answer
   vectors. Do not invent vectors. If official vectors cannot be fetched, say so and stop.
2. **Check FIPS 203 errata first.** NIST's publication page carries a planning note
   (17 Nov 2025) about an issue to be corrected; read its errata spreadsheet before
   locking vectors, and record what you found in `docs/decisions/`.
3. Block by block, bit-exact against the golden model: NTT/INTT, pointwise, Keccak
   (against `hashlib` SHA3/SHAKE), samplers, compress/encode, then full KeyGen/Encaps/Decaps.
4. Only after a block passes: measure with `quartus-report`. Never optimise first.
5. Old CRYSTALS-Kyber (round 3) vectors are **not** FIPS 203 vectors. Do not mix them.

## Free to explore (architecture only)

Butterfly count and scheduling, Keccak iterative vs unrolled, memory banking in M10K,
DSP packing, HPS-FPGA transfer strategy, fault-detection logic inside the datapath,
optional masking/shuffling (later stage). Each choice is judged by MEASURED area,
Fmax, latency, and cycle-count invariance.
