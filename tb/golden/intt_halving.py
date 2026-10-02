"""tb/golden/intt_halving.py

Phase 5M step S6 (docs/evidence/phase05m-memsched/test_plan.md): the inverse NTT of FIPS 203 Algorithm 10 computed WITHOUT
the final multiplication by 3303 = 128^-1 mod q, by halving in every one of the 7 layers (2^-7 = 3303 mod q):

    a' = (a + b) / 2 mod q          b' = (zeta / 2) * (b - a) mod q,      zeta / 2 = zeta * 1665 mod q  (2 * 1665 = 1 mod q)

It is an independent integer model (it does not call primitives.intt); tb/golden/tests/test_intt_halving.py proves
intt_halving(f) == intt(f) for the vectors listed in the test plan. primitives.py itself is not modified.
`drop_layer` (0..6, test only) skips the halving of that layer (both outputs): the negative control of test plan V3.
"""

from params import N, Q
from primitives import _ZETA_BITREV

INV2 = 1665                      # 2^-1 mod q
assert (2 * INV2) % Q == 1


def half_mod(x: int) -> int:
    """x / 2 mod q for x in [0, q): (x + (x odd ? q : 0)) >> 1, the same expression as rtl/arith/half_mod.sv."""
    assert 0 <= x < Q
    return (x + (Q if x & 1 else 0)) >> 1


def intt_halving(f_hat: list[int], drop_layer: int | None = None) -> list[int]:
    """Algorithm 10 with halving in every layer and no final scaling pass."""
    assert len(f_hat) == N
    f = f_hat[:]
    i = 127
    length = 2
    layer = 0
    while length <= 128:
        halve = drop_layer != layer
        start = 0
        while start < 256:
            zeta = _ZETA_BITREV[i]
            zeta_h = (zeta * INV2) % Q if halve else zeta
            i -= 1
            for j in range(start, start + length):
                t = f[j]
                s = (t + f[j + length]) % Q
                f[j] = half_mod(s) if halve else s
                f[j + length] = (zeta_h * (f[j + length] - t)) % Q
            start += 2 * length
        length *= 2
        layer += 1
    return f
