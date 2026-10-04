"""tb/golden/tests/test_codec_model.py -- Phase 9a test plan V2: the division-free codec of tb/golden/codec_model.py equals the unmodified golden primitives
(compress, decompress, byte_encode, byte_decode) on the whole input domain and on random and special polynomials."""
import random

import codec_model as C
from params import N, Q
from primitives import byte_decode, byte_encode, compress, decompress


def test_compress_hw_equals_golden_on_every_input():
    for d in (1, 4, 10):
        for x in range(Q):
            assert C.compress_hw(d, x) == compress(d, x), (d, x)


def test_decompress_hw_equals_golden_on_every_input():
    for d in (1, 4, 10):
        for y in range(1 << d):
            assert C.decompress_hw(d, y) == decompress(d, y), (d, y)


def test_reduce12_equals_mod_q_on_every_12_bit_value():
    for v in range(4096):
        assert C.reduce12(v) == v % Q


def _polys():
    rng = random.Random(900)
    yield [0] * N
    yield [Q - 1] * N
    yield [0 if i % 2 else Q - 1 for i in range(N)]
    yield [i * 13 % Q for i in range(N)]
    yield [(Q + 1) // 2 + (i % 3) - 1 for i in range(N)]   # around the rounding ties
    for _ in range(200):
        yield [rng.randrange(Q) for _ in range(N)]


def test_pack_equals_byte_encode_of_compress():
    for p in _polys():
        for d in (1, 4, 10):
            assert C.pack_poly(d, p) == byte_encode(d, compress(d, p))
        assert C.pack_poly(12, p) == byte_encode(12, p)


def test_unpack_equals_decompress_of_byte_decode():
    rng = random.Random(901)
    for _ in range(200):
        for d in (1, 4, 10):
            data = bytes(rng.randrange(256) for _ in range(32 * d))
            assert C.unpack_poly(d, data) == decompress(d, byte_decode(d, data))
        data = bytes(rng.randrange(256) for _ in range(384))
        assert C.unpack_poly(12, data) == byte_decode(12, data)


def test_unpack_12_covers_values_at_and_above_q():
    # every 12-bit value 0..4095 appears as a coefficient: 256 values per polynomial, 16 polynomials
    for base in range(0, 4096, N):
        vals = list(range(base, base + N))
        acc, nbits, out = 0, 0, bytearray()
        for v in vals:
            acc |= v << nbits
            nbits += 12
            while nbits >= 8:
                out.append(acc & 255)
                acc >>= 8
                nbits -= 8
        assert C.unpack_poly(12, bytes(out)) == [v % Q for v in vals] == byte_decode(12, bytes(out))


def test_roundtrip_matches_golden_roundtrip():
    for p in list(_polys())[:20]:
        for d in (1, 4, 10):
            assert C.unpack_poly(d, C.pack_poly(d, p)) == decompress(d, compress(d, p))
        assert C.unpack_poly(12, C.pack_poly(12, p)) == p
