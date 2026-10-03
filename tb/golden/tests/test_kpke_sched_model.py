"""tb/golden/tests/test_kpke_sched_model.py

Phase 6 test plan V2: the operation-level schedule (tb/golden/kpke_sched_model.py) run with the golden primitives equals the unmodified golden K-PKE (tb/golden/kpke.py) end to end, and its
operation counts equal the reproduced reference counts (tb/golden/op_counts.py).
"""
import random

import pytest

import kpke
from kpke_sched_model import PROGRAMS, decrypt_inputs, encrypt_inputs, keygen_inputs, run
from op_counts import EXPECTED
from params import DU, DV, K
from primitives import byte_decode, byte_encode, compress

SEEDS = range(8)


def _rand(rng, n=32):
    return bytes(rng.randrange(256) for _ in range(n))


@pytest.mark.parametrize("seed", SEEDS)
def test_keygen_equals_golden(seed):
    rng = random.Random(100 + seed)
    d = _rand(rng)
    ek, dk = kpke.k_pke_keygen(d)
    slots, rho = keygen_inputs(d)
    run(PROGRAMS["keygen"], slots)
    assert [slots[12 + i] for i in range(K)] == [byte_decode(12, ek[384 * i: 384 * (i + 1)]) for i in range(K)]
    assert [slots[9 + i] for i in range(K)] == [byte_decode(12, dk[384 * i: 384 * (i + 1)]) for i in range(K)]


@pytest.mark.parametrize("seed", SEEDS)
def test_encrypt_equals_golden(seed):
    rng = random.Random(200 + seed)
    ek, _ = kpke.k_pke_keygen(_rand(rng))
    m, r = _rand(rng), _rand(rng)
    c = kpke.k_pke_encrypt(ek, m, r)
    slots = encrypt_inputs(ek, m, r)
    run(PROGRAMS["encrypt"], slots)
    c1 = b"".join(byte_encode(DU, compress(DU, slots[12 + i])) for i in range(K))
    c2 = byte_encode(DV, compress(DV, slots[19]))
    assert c1 + c2 == c


@pytest.mark.parametrize("seed", SEEDS)
def test_decrypt_equals_golden(seed):
    rng = random.Random(300 + seed)
    ek, dk = kpke.k_pke_keygen(_rand(rng))
    m = _rand(rng)
    c = kpke.k_pke_encrypt(ek, m, _rand(rng))
    slots = decrypt_inputs(dk, c)
    run(PROGRAMS["decrypt"], slots)
    assert byte_encode(1, compress(1, slots[19])) == kpke.k_pke_decrypt(dk, c) == m


def test_counts_equal_reference():
    def c(name):
        counts = run(PROGRAMS[name], [[0] * 256 for _ in range(24)])
        return {"NTT": counts["NTT"], "INTT": counts["INTT"], "PWM": counts["PWM"]}
    assert c("keygen") == EXPECTED["KeyGen"]
    assert c("encrypt") == EXPECTED["Encaps"]
    dec, enc = c("decrypt"), c("encrypt")
    assert {k: dec[k] + enc[k] for k in dec} == EXPECTED["Decaps"]


def test_negative_control_wrong_program_differs():
    """A program with the INTT of the t_hat^T o y_hat sum dropped must give a different ciphertext."""
    rng = random.Random(400)
    ek, _ = kpke.k_pke_keygen(_rand(rng))
    m, r = _rand(rng), _rand(rng)
    c = kpke.k_pke_encrypt(ek, m, r)
    prog = list(PROGRAMS["encrypt"])
    idx = max(i for i, op in enumerate(prog) if op[0] == 2)      # last INTT
    del prog[idx]
    slots = encrypt_inputs(ek, m, r)
    run(prog, slots)
    c1 = b"".join(byte_encode(DU, compress(DU, slots[12 + i])) for i in range(K))
    assert c1 + byte_encode(DV, compress(DV, slots[19])) != c
