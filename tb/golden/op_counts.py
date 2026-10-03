"""tb/golden/op_counts.py

Phase 6: counts the polynomial transforms of whole ML-KEM-768 operations by instrumenting the golden model (tb/golden/kpke.py, mlkem.py are not edited:
the names the K-PKE module imported are wrapped for the duration of one call). Reproduces the reference counts quoted in docs/ROADMAP.md Phase 6
(from an instrumented kyber-py run, 2026-09-28) from this repository's own golden model.

  NTT      calls of primitives.ntt             (one polynomial in, one polynomial out)
  INTT     calls of primitives.intt
  PWM      calls of primitives.multiply_ntts   (one pointwise polynomial product in T_q: 128 base-case multiplications)

Usage: python3 tb/golden/op_counts.py
"""
from __future__ import annotations

import os
import sys
from contextlib import contextmanager

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import kpke  # noqa: E402
import mlkem  # noqa: E402


@contextmanager
def counting():
    counts = {"NTT": 0, "INTT": 0, "PWM": 0}
    orig = (kpke.ntt, kpke.intt, kpke.multiply_ntts)

    def wrap(name, fn):
        def inner(*a, **k):
            counts[name] += 1
            return fn(*a, **k)
        return inner

    kpke.ntt = wrap("NTT", orig[0])
    kpke.intt = wrap("INTT", orig[1])
    kpke.multiply_ntts = wrap("PWM", orig[2])
    try:
        yield counts
    finally:
        kpke.ntt, kpke.intt, kpke.multiply_ntts = orig


def measure(seed: int = 1) -> dict[str, dict[str, int]]:
    import random
    rng = random.Random(seed)
    d, z, m = (bytes(rng.randrange(256) for _ in range(32)) for _ in range(3))
    out = {}
    with counting() as c:
        ek, dk = mlkem.ml_kem_keygen_internal(d, z)
    out["KeyGen"] = dict(c)
    with counting() as c:
        K, ct = mlkem.ml_kem_encaps_internal(ek, m)
    out["Encaps"] = dict(c)
    with counting() as c:
        K2 = mlkem.ml_kem_decaps_internal(dk, ct)
    out["Decaps"] = dict(c)
    assert K == K2
    return out


EXPECTED = {"KeyGen": {"NTT": 6, "INTT": 0, "PWM": 9},
            "Encaps": {"NTT": 3, "INTT": 4, "PWM": 12},
            "Decaps": {"NTT": 6, "INTT": 5, "PWM": 15}}

if __name__ == "__main__":
    got = measure()
    for op, c in got.items():
        print(f"{op}: NTT {c['NTT']}, INTT {c['INTT']}, PWM {c['PWM']}   expected {EXPECTED[op]}   {'OK' if c == EXPECTED[op] else 'MISMATCH'}")
    sys.exit(0 if got == EXPECTED else 1)
