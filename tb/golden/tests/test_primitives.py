"""tb/golden/tests/test_primitives.py

Property-based tests for tb/golden/primitives.py, independent of any KAT
vector (Phase 0, docs/ROADMAP.md). Each test cites the FIPS 203 section or
property it checks. Random inputs use Python's stdlib `random` seeded per
test for reproducibility; no external test-vector files are used here.
"""

import random

import pytest

from params import DU, DV, ETA1, ETA2, N, Q
from primitives import (
    _round_div,
    byte_decode,
    byte_encode,
    compress,
    decompress,
    intt,
    ntt,
    sample_poly_cbd,
)


def _random_poly(rng: random.Random) -> list[int]:
    return [rng.randrange(Q) for _ in range(N)]


def _schoolbook_negacyclic_multiply(f: list[int], g: list[int]) -> list[int]:
    """Reference (non-NTT) multiplication in R_q = Z_q[X]/(X^256+1), used
    only here as an independent check of the NTT-domain product (Section
    4.3, eq. 4.9: f *_Rq g = NTT^-1(f_hat *_Tq g_hat)). O(n^2), test-only.
    """
    n = len(f)
    out = [0] * n
    for i, fi in enumerate(f):
        if fi == 0:
            continue
        for j, gj in enumerate(g):
            k = i + j
            val = fi * gj
            if k >= n:
                k -= n
                val = -val
            out[k] = (out[k] + val) % Q
    return out


def _cyclic_dist(a: int, b: int, m: int) -> int:
    d = abs(a - b) % m
    return min(d, m - d)


# ---------------------------------------------------------------------------
# (a) intt(ntt(f)) == f
# ---------------------------------------------------------------------------


def test_ntt_intt_roundtrip():
    rng = random.Random(0)
    for _ in range(50):
        f = _random_poly(rng)
        assert intt(ntt(f)) == f


# ---------------------------------------------------------------------------
# (b) NTT-domain multiplication == negacyclic schoolbook multiplication
#     (Section 4.3, eq. 4.9)
# ---------------------------------------------------------------------------


def test_ntt_multiplication_matches_schoolbook():
    from primitives import multiply_ntts

    rng = random.Random(1)
    for _ in range(20):
        f = _random_poly(rng)
        g = _random_poly(rng)
        expected = _schoolbook_negacyclic_multiply(f, g)
        actual = intt(multiply_ntts(ntt(f), ntt(g)))
        assert actual == expected


# ---------------------------------------------------------------------------
# (c) NTT uses exactly 7 layers with block lengths 128,64,32,16,8,4,2
#     ("incomplete NTT", Section 4.3 / mlkem-guard SKILL.md)
# ---------------------------------------------------------------------------


def test_ntt_is_incomplete_seven_layers():
    rng = random.Random(2)
    f = _random_poly(rng)
    trace: list[int] = []
    ntt(f, trace=trace)
    assert trace == [128, 64, 32, 16, 8, 4, 2]


def test_intt_is_incomplete_seven_layers():
    rng = random.Random(3)
    f_hat = _random_poly(rng)
    trace: list[int] = []
    intt(f_hat, trace=trace)
    assert trace == [2, 4, 8, 16, 32, 64, 128]


# ---------------------------------------------------------------------------
# (d) byte_decode(byte_encode(f)) == f, for the d values ML-KEM-768 uses:
#     d=1 (message encoding), d=DV=4, d=DU=10, d=12 (ByteEncode12 for keys).
#     (Algorithms 5-6, Section 4.2.1)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("d", [1, DV, DU, 12])
def test_byte_encode_decode_roundtrip(d):
    rng = random.Random(100 + d)
    m = Q if d == 12 else (1 << d)
    for _ in range(20):
        F = [rng.randrange(m) for _ in range(N)]
        B = byte_encode(d, F)
        assert len(B) == 32 * d
        assert byte_decode(d, B) == F


# ---------------------------------------------------------------------------
# (e) Compress/Decompress: exact and bounded-error properties
#     (Section 4.2.1, eq. 4.7-4.8)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("d", [1, DV, DU, 11])
def test_compress_of_decompress_is_exact(d):
    """FIPS 203, Section 4.2.1: "decompression followed by compression
    preserves the input. That is, Compress_d(Decompress_d(y)) = y for all
    y in Z_{2^d} and all d < 12." This is an EXACT equality, not a bound.
    """
    m = 1 << d
    for y in range(m):
        assert compress(d, decompress(d, y)) == y


@pytest.mark.parametrize("d", [1, DV, DU, 11])
def test_decompress_of_compress_error_bound(d):
    """FIPS 203, Section 4.2.1 states only qualitatively that "if d is
    large ... compression followed by decompression does not significantly
    alter the value" -- it gives no explicit numeric bound. The bound
    checked here, |Decompress_d(Compress_d(x)) - x| (mod q, cyclic
    distance) <= round(q / 2^(d+1)), is DERIVED by us from the rounding
    definitions in eq. 4.7-4.8 (perhitungan tim), not copied from an
    explicit formula in the standard; it is the standard's own
    justification for why Compress/Decompress is usable at all.
    """
    bound = _round_div(Q, 1 << (d + 1))
    rng = random.Random(200 + d)
    for _ in range(200):
        x = rng.randrange(Q)
        y = compress(d, x)
        x_rec = decompress(d, y)
        assert _cyclic_dist(x_rec, x, Q) <= bound


# ---------------------------------------------------------------------------
# (f) SamplePolyCBD_eta: coefficients in [-eta, eta] (mod q), correct input
#     length (Algorithm 8, Section 4.2.2)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("eta", [ETA1, ETA2])
def test_sample_poly_cbd_coefficient_range(eta):
    rng = random.Random(300 + eta)
    valid = set(range(0, eta + 1)) | set(range(Q - eta, Q))
    for _ in range(20):
        B = bytes(rng.randrange(256) for _ in range(64 * eta))
        f = sample_poly_cbd(eta, B)
        assert len(f) == N
        assert all(coef in valid for coef in f)


def test_sample_poly_cbd_requires_standard_input_length():
    """Algorithm 8 input: byte array B in B^{64*eta} -- any other length is
    not a valid input for this parameter set.
    """
    eta = ETA1
    with pytest.raises(AssertionError):
        sample_poly_cbd(eta, bytes(64 * eta - 1))
