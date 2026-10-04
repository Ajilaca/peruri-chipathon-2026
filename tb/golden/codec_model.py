"""tb/golden/codec_model.py

Golden model of the Phase 9a codec (docs/evidence/phase09-integration/9a/test_plan_9a.md), independent of any RTL.
Compress and Decompress are written without division, exactly as the hardware does (FIPS 203 Section 4.2.1); they are checked against the unmodified golden `primitives.compress` and `primitives.decompress` on the whole
input domain in tb/golden/tests/test_codec_model.py. `pack_poly` and `unpack_poly` follow the bit-buffer order of the RTL (ByteEncode_d / ByteDecode_d, Algorithms 5 and 6: bits LSB first).
"""
from params import N, Q

D_VALUES = (1, 4, 10, 12)          # dsel 0..3
# Compress_d(x) = (((x << d) + H) * M_d >> S_d) mod 2^d for x in [0, q-1]; constants found by search and proved on the whole domain by the tests
COMPRESS_H = 1664
COMPRESS_MS = {1: (315, 20), 4: (315, 20), 10: (161271, 29)}


def compress_hw(d: int, x: int) -> int:
    assert d in COMPRESS_MS and 0 <= x < Q
    m, s = COMPRESS_MS[d]
    return ((((x << d) + COMPRESS_H) * m) >> s) % (1 << d)


def decompress_hw(d: int, y: int) -> int:
    assert d in COMPRESS_MS and 0 <= y < (1 << d)
    return (Q * y + (1 << (d - 1))) >> d


def reduce12(v: int) -> int:
    """ByteDecode_12 reduction mod q for a 12-bit value (one conditional subtraction)."""
    assert 0 <= v < 4096
    return v - Q if v >= Q else v


def pack_poly(d: int, coeffs: list[int]) -> bytes:
    """256 coefficients in [0, q-1] -> 32 d bytes: Compress_d (d < 12) then ByteEncode_d."""
    assert len(coeffs) == N and d in D_VALUES
    acc, nbits, out = 0, 0, bytearray()
    for x in coeffs:
        c = x if d == 12 else compress_hw(d, x)
        acc |= c << nbits
        nbits += d
        while nbits >= 8:
            out.append(acc & 255)
            acc >>= 8
            nbits -= 8
    assert nbits == 0 and len(out) == 32 * d
    return bytes(out)


def unpack_poly(d: int, data: bytes) -> list[int]:
    """32 d bytes -> 256 coefficients: ByteDecode_d then Decompress_d (d < 12) or reduction mod q (d = 12)."""
    assert len(data) == 32 * d and d in D_VALUES
    acc, nbits, out = 0, 0, []
    for b in data:
        acc |= b << nbits
        nbits += 8
        while nbits >= d:
            v = acc & ((1 << d) - 1)
            acc >>= d
            nbits -= d
            out.append(reduce12(v) if d == 12 else decompress_hw(d, v))
    assert nbits == 0 and len(out) == N
    return out
