"""tb/golden/primitives.py

Pure-Python (stdlib only) transcription of the FIPS 203 auxiliary algorithms
used by ML-KEM-768: conversion/compression (Section 4.2.1), sampling
(Section 4.2.2), the number-theoretic transform (Section 4.3), and
multiplication in the NTT domain (Section 4.3.1), plus the cryptographic
function wrappers (Section 4.1).

Each function is transcribed algorithm-by-algorithm from the FIPS 203 final
PDF (SHA-256 fe1f12f32a7e44ec9fdebbf400cda843a40b506dee676725234dc6f7923b6cac,
accessed 2026-09-28 UTC; see evidence/phase00/fips203_errata.md).
It is independent of any RTL and is the reference against which RTL blocks
are compared block-by-block (mlkem-guard SKILL.md, "Verification process").

Coefficient arrays are plain Python lists of int, always reduced mod q (or
mod 2^d, as appropriate) after every assignment, matching the standard's
"implicit reduction on assignment" convention (Section 2.4.1).
"""

from __future__ import annotations

import hashlib

from params import N, Q, ZETA

# ---------------------------------------------------------------------------
# 4.1 Cryptographic Functions
# ---------------------------------------------------------------------------


def H(s: bytes) -> bytes:
    """H(s) := SHA3-256(s).  (Section 4.1, eq. 4.4)"""
    return hashlib.sha3_256(s).digest()


def J(s: bytes) -> bytes:
    """J(s) := SHAKE256(s, 8*32).  (Section 4.1, eq. 4.4)"""
    return hashlib.shake_256(s).digest(32)


def G(c: bytes) -> tuple[bytes, bytes]:
    """G(c) := SHA3-512(c), split into two 32-byte halves (a, b) = G(c).

    (Section 4.1, eq. 4.5)
    """
    d = hashlib.sha3_512(c).digest()
    return d[:32], d[32:]


def PRF(eta: int, s: bytes, b: int) -> bytes:
    """PRF_eta(s, b) := SHAKE256(s || b, 8*64*eta).  (Section 4.1, eq. 4.3)

    eta in {2, 3}; s is 32 bytes; b is a single byte value (0..255).
    """
    assert eta in (2, 3)
    assert len(s) == 32
    assert 0 <= b <= 255
    return hashlib.shake_256(s + bytes([b])).digest(64 * eta)


def xof(seed: bytes, length: int) -> bytes:
    """XOF wrapper over SHAKE128 (Section 4.1).

    The standard's incremental Init/Absorb/Squeeze API is equivalent, for a
    single absorb call, to reading `length` bytes sequentially off one
    SHAKE128 squeeze stream (eq. 4.6). hashlib's shake_128().digest(length)
    computes exactly that stream, so a single call with the full length
    needed reproduces repeated XOF.Squeeze calls byte-for-byte.
    """
    return hashlib.shake_128(seed).digest(length)


# ---------------------------------------------------------------------------
# 4.2.1 Conversion and Compression Algorithms
# ---------------------------------------------------------------------------


def bits_to_bytes(bits: list[int]) -> bytes:
    """Algorithm 3, BitsToBytes(b). len(bits) must be a multiple of 8."""
    assert len(bits) % 8 == 0
    out = bytearray(len(bits) // 8)
    for i, bit in enumerate(bits):
        out[i // 8] += bit * (2 ** (i % 8))
    return bytes(out)


def bytes_to_bits(B: bytes) -> list[int]:
    """Algorithm 4, BytesToBits(B)."""
    bits = [0] * (8 * len(B))
    for i, byte in enumerate(B):
        c = byte
        for j in range(8):
            bits[8 * i + j] = c % 2
            c //= 2
    return bits


def _round_div(num: int, den: int) -> int:
    """Round num/den to the nearest integer, ties rounding up.

    Matches the standard's rounding-to-nearest-integer notation (Section
    2.3): "if x = y + 1/2 for some y in Z, then round(x) = y + 1". num and
    den must both be non-negative with den > 0.
    """
    assert num >= 0 and den > 0
    q, r = divmod(num, den)
    if 2 * r >= den:
        q += 1
    return q


def compress(d: int, x):
    """Compress_d(x) = round((2^d / q) * x) mod 2^d.  (Section 4.2.1, eq. 4.7)

    x may be a single int mod q, or a list of such ints (applied
    elementwise per Section 2.4.8).
    """
    if isinstance(x, list):
        return [compress(d, v) for v in x]
    assert 1 <= d < 12
    m = 1 << d
    return _round_div(m * (x % Q), Q) % m


def decompress(d: int, y):
    """Decompress_d(y) = round((q / 2^d) * y).  (Section 4.2.1, eq. 4.8)

    y may be a single int mod 2^d, or a list of such ints.
    """
    if isinstance(y, list):
        return [decompress(d, v) for v in y]
    assert 1 <= d < 12
    m = 1 << d
    return _round_div(Q * (y % m), m)


def byte_encode(d: int, F: list[int]) -> bytes:
    """Algorithm 5, ByteEncode_d(F), for 1 <= d <= 12.

    F: length-256 int array, entries mod 2^d (d<12) or mod q (d==12).
    Returns a byte array of length 32*d.
    """
    assert len(F) == N
    assert 1 <= d <= 12
    bits = [0] * (N * d)
    for i in range(N):
        a = F[i]
        for j in range(d):
            bits[i * d + j] = a % 2
            a = (a - bits[i * d + j]) // 2
    return bits_to_bytes(bits)


def byte_decode(d: int, B: bytes) -> list[int]:
    """Algorithm 6, ByteDecode_d(B), for 1 <= d <= 12.

    B: byte array of length 32*d. Returns a length-256 int array, entries
    mod 2^d (d<12) or mod q (d==12).
    """
    assert len(B) == 32 * d
    assert 1 <= d <= 12
    m = Q if d == 12 else (1 << d)
    bits = bytes_to_bits(B)
    F = [0] * N
    for i in range(N):
        val = 0
        for j in range(d):
            val += bits[i * d + j] << j
        F[i] = val % m
    return F


# ---------------------------------------------------------------------------
# 4.2.2 Sampling Algorithms
# ---------------------------------------------------------------------------


def sample_ntt(B: bytes) -> list[int]:
    """Algorithm 7, SampleNTT(B): rejection-sample a uniform element of T_q.

    B: 34-byte input (32-byte seed || 2 index bytes). Returns the
    length-256 coefficient array a_hat in Z_q^256.
    """
    assert len(B) == 34
    a = [0] * N
    j = 0
    # Squeeze from the XOF stream lazily, doubling the buffer if the
    # rejection loop needs more bytes than first requested.
    size = 3 * 192  # generous starting guess; grown on demand below
    buf = xof(B, size)
    pos = 0
    while j < N:
        if pos + 3 > len(buf):
            size *= 2
            buf = xof(B, size)
        C = buf[pos : pos + 3]
        pos += 3
        d1 = C[0] + 256 * (C[1] % 16)
        d2 = (C[1] // 16) + 16 * C[2]
        if d1 < Q:
            a[j] = d1
            j += 1
        if d2 < Q and j < N:
            a[j] = d2
            j += 1
    return a


def sample_poly_cbd(eta: int, B: bytes) -> list[int]:
    """Algorithm 8, SamplePolyCBD_eta(B): sample from the centered binomial
    distribution D_eta(R_q).

    B: byte array of length 64*eta. Returns a length-256 array in Z_q^256.
    """
    assert len(B) == 64 * eta
    bits = bytes_to_bits(B)
    f = [0] * N
    for i in range(N):
        x = sum(bits[2 * i * eta + j] for j in range(eta))
        y = sum(bits[2 * i * eta + eta + j] for j in range(eta))
        f[i] = (x - y) % Q
    return f


# ---------------------------------------------------------------------------
# 4.3 The Number-Theoretic Transform
# ---------------------------------------------------------------------------


def _bitrev7(r: int) -> int:
    """BitRev7(r): bit-reversal of a 7-bit integer.  (Section 2.3)"""
    assert 0 <= r < 128
    out = 0
    for i in range(7):
        out |= ((r >> i) & 1) << (6 - i)
    return out


# zeta^BitRev7(i) mod q for i = 0..127 (i=0 gives zeta^0 = 1; Appendix A
# includes this entry too - see errata item #1 in
# evidence/phase00/fips203_errata.md - computed here directly
# from the BitRev7 formula, not copied from the Appendix A table).
_ZETA_BITREV = [pow(ZETA, _bitrev7(i), Q) for i in range(128)]

# zeta^(2*BitRev7(i)+1) mod q for i = 0..127, used by MultiplyNTTs
# (Algorithm 11) as the quadratic-modulus constant gamma_i.
_GAMMA = [pow(ZETA, 2 * _bitrev7(i) + 1, Q) for i in range(128)]

# Multiplicative inverse of 128 mod q, used by NTT^-1 (Algorithm 10, line 14).
_INV_128 = 3303
assert (128 * _INV_128) % Q == 1


def ntt(f: list[int], trace: list[int] | None = None) -> list[int]:
    """Algorithm 9, NTT(f): compute the NTT representation f_hat of f.

    f: length-256 coefficient array of a polynomial in R_q.
    trace: if given, the sequence of "len" values used by the 7 layers is
    appended to it (for testing the "incomplete NTT" layer structure).
    """
    assert len(f) == N
    f = f[:]
    i = 1
    length = 128
    while length >= 2:
        if trace is not None:
            trace.append(length)
        start = 0
        while start < 256:
            zeta = _ZETA_BITREV[i]
            i += 1
            for j in range(start, start + length):
                t = (zeta * f[j + length]) % Q
                f[j + length] = (f[j] - t) % Q
                f[j] = (f[j] + t) % Q
            start += 2 * length
        length //= 2
    return f


def intt(f_hat: list[int], trace: list[int] | None = None) -> list[int]:
    """Algorithm 10, NTT^-1(f_hat): compute the polynomial f corresponding
    to the given NTT representation f_hat.
    """
    assert len(f_hat) == N
    f = f_hat[:]
    i = 127
    length = 2
    while length <= 128:
        if trace is not None:
            trace.append(length)
        start = 0
        while start < 256:
            zeta = _ZETA_BITREV[i]
            i -= 1
            for j in range(start, start + length):
                t = f[j]
                f[j] = (t + f[j + length]) % Q
                f[j + length] = (zeta * (f[j + length] - t)) % Q
            start += 2 * length
        length *= 2
    return [(x * _INV_128) % Q for x in f]


# ---------------------------------------------------------------------------
# 4.3.1 Multiplication in the NTT Domain
# ---------------------------------------------------------------------------


def base_case_multiply(a0: int, a1: int, b0: int, b1: int, gamma: int) -> tuple[int, int]:
    """Algorithm 12, BaseCaseMultiply(a0, a1, b0, b1, gamma).

    Computes the coefficients (c0, c1) of (a0 + a1*X)(b0 + b1*X) mod
    (X^2 - gamma).
    """
    c0 = (a0 * b0 + a1 * b1 * gamma) % Q
    c1 = (a0 * b1 + a1 * b0) % Q
    return c0, c1


def multiply_ntts(f_hat: list[int], g_hat: list[int]) -> list[int]:
    """Algorithm 11, MultiplyNTTs(f_hat, g_hat): product of two NTT
    representations, i.e. h_hat = f_hat *_{T_q} g_hat.
    """
    assert len(f_hat) == N and len(g_hat) == N
    h_hat = [0] * N
    for i in range(128):
        c0, c1 = base_case_multiply(
            f_hat[2 * i], f_hat[2 * i + 1], g_hat[2 * i], g_hat[2 * i + 1], _GAMMA[i]
        )
        h_hat[2 * i] = c0
        h_hat[2 * i + 1] = c1
    return h_hat
