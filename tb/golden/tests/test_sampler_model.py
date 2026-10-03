"""tb/golden/tests/test_sampler_model.py -- Phase 8b test plan V2: the stream samplers of tb/golden/sampler_model.py equal the unmodified golden primitives.sample_ntt and primitives.sample_poly_cbd
(for real XOF / PRF streams), report the consumed bytes, and handle the crafted boundary streams of the test plan section 2."""
import hashlib
import random

import pytest

import sampler_model as M
from params import N, Q
from primitives import PRF, sample_ntt, sample_poly_cbd


def _xof(b, n=4096):
    return hashlib.shake_128(b).digest(n)


def test_sample_ntt_equals_golden_on_xof_streams():
    rng = random.Random(800)
    consumed = []
    for _ in range(300):
        rho = bytes(rng.randrange(256) for _ in range(32))
        i, j = rng.randrange(3), rng.randrange(3)
        b = rho + bytes([j, i])
        coeffs, nbytes, ntrip = M.sample_ntt_stream(_xof(b))
        assert coeffs == sample_ntt(b)
        assert nbytes == 3 * ntrip and 3 * 128 <= nbytes
        consumed.append(nbytes)
    assert min(consumed) >= 384 and max(consumed) < 1000  # sanity of the distribution (informational: min 128 triples, mean about 158)


def test_consumed_bytes_is_what_the_loop_needs():
    # the stream cut right after the reported byte count is enough, one triple less is not
    rng = random.Random(801)
    for _ in range(50):
        b = bytes(rng.randrange(256) for _ in range(34))
        s = _xof(b)
        coeffs, nbytes, _ = M.sample_ntt_stream(s)
        assert M.sample_ntt_stream(s[:nbytes])[0] == coeffs
        with pytest.raises(ValueError):
            M.sample_ntt_stream(s[: nbytes - 3])


def test_crafted_boundary_streams():
    # all zero bytes: d1 = d2 = 0, every candidate accepted, 128 triples
    c, nb, nt = M.sample_ntt_stream(bytes(3 * 128))
    assert c == [0] * N and nt == 128
    # j = 255 with both candidates acceptable: 127 triples accept both (254), one triple accepts only d1 (255), then a triple accepts both but only d1 is used
    both = bytes([1, 0, 0])                       # d1 = 1, d2 = 0 + 16*0 = 0
    only_d1 = bytes([2, 0xF0 | 0x00, 0xFF])       # d1 = 2 + 256*0 = 2 (accepted), d2 = 15 + 16*255 = 4095 (rejected)
    last = bytes([7, 0x50, 0x00])                 # d1 = 7 + 256*0 = 7, d2 = 5 + 0 = 5 (both acceptable, only d1 is used)
    s = both * 127 + only_d1 + last + bytes([9, 9, 9]) * 4
    c, nb, nt = M.sample_ntt_stream(s)
    assert len(c) == N and c[254] == 2 and c[255] == 7 and nt == 129 and nb == 387
    # d == q is rejected (d1 = 3329 = 0xD01: b0 = 0x01, b1 low nibble = 0xD)
    s = bytes([0x01, 0x0D, 0x00]) + bytes(3 * 128)  # d1 = 1 + 256*13 = 3329 rejected, d2 = 0 + 16*0 = 0 accepted
    c, nb, nt = M.sample_ntt_stream(s)
    assert c[0] == 0 and nt == 129
    # d = 3328 accepted (0xD00)
    c, _, _ = M.sample_ntt_stream(bytes([0x00, 0x0D, 0xFF]) + bytes(3 * 130))  # d1 = 3328 accepted, d2 = 0 + 16*255 = 4080 rejected
    assert c[0] == 3328
    # all 0xFF: every candidate 4095 >= q: never completes
    with pytest.raises(ValueError):
        M.sample_ntt_stream(b"\xff" * 3000)


def test_cbd2_equals_golden():
    rng = random.Random(802)
    for _ in range(300):
        b = bytes(rng.randrange(256) for _ in range(128))
        assert M.cbd2(b) == sample_poly_cbd(2, b)
    for fill in (0x00, 0xFF, 0x55, 0xAA, 0x0F, 0xF0):
        b = bytes([fill]) * 128
        assert M.cbd2(b) == sample_poly_cbd(2, b)


def test_cbd2_every_nibble_value():
    # all 16 nibbles in both positions: byte = low | high << 4 covers all 256 byte values
    b = bytes(range(256))[:128] + bytes(0)
    full = bytes(range(128))
    assert M.cbd2(full) == sample_poly_cbd(2, full)
    full2 = bytes(range(128, 256))
    assert M.cbd2(full2) == sample_poly_cbd(2, full2)
    vals = {c for byte in range(256) for c in M.cbd2(bytes([byte]) * 128)}
    assert vals == {0, 1, 2, Q - 1, Q - 2}


def test_cbd2_on_prf_streams():
    rng = random.Random(803)
    for _ in range(50):
        sigma = bytes(rng.randrange(256) for _ in range(32))
        n = rng.randrange(256)
        assert M.cbd2(PRF(2, sigma, n)) == sample_poly_cbd(2, PRF(2, sigma, n))
