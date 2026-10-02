"""tb/golden/tests/test_intt_halving.py

Phase 5M S6, test plan V3: intt_halving() (no scaling pass, halving in every layer) equals the FIPS 203 intt() for the unit
vectors, (q-1) times the unit vectors, edge vectors and random vectors; half_mod is exact on all of [0, q); a variant that
drops the halving in one layer differs (negative control).
"""

import random

import pytest

from intt_halving import INV2, half_mod, intt_halving
from params import N, Q
from primitives import intt


def test_half_mod_exhaustive():
    for x in range(Q):
        h = half_mod(x)
        assert 0 <= h < Q
        assert (2 * h) % Q == x
    assert INV2 == 1665


def test_scaling_constant_identity():
    assert (128 * 3303) % Q == 1 and pow(2, -7, Q) == 3303


def test_unit_vectors():
    for i in range(N):
        for scale in (1, Q - 1):
            f = [0] * N
            f[i] = scale
            assert intt_halving(f) == intt(f), (i, scale)


def _edge_vectors():
    return [
        [0] * N,
        [Q - 1] * N,
        [1] * N,
        [0 if i % 2 == 0 else Q - 1 for i in range(N)],
        [i % Q for i in range(N)],
        [(Q - 1) if i == 0 else 0 for i in range(N)],
        [(Q - 1) if i == N - 1 else 0 for i in range(N)],
    ]


def test_edge_vectors():
    for f in _edge_vectors():
        assert intt_halving(f) == intt(f)


def test_random_vectors():
    rng = random.Random(51)
    for _ in range(1000):
        f = [rng.randrange(Q) for _ in range(N)]
        assert intt_halving(f) == intt(f)


@pytest.mark.parametrize("layer", range(7))
def test_negative_control_dropped_halving_differs(layer):
    rng = random.Random(52 + layer)
    f = [rng.randrange(Q) for _ in range(N)]
    assert intt_halving(f, drop_layer=layer) != intt(f), f"dropping the halving of layer {layer} went undetected"
