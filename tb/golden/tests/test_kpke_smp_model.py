"""tb/golden/tests/test_kpke_smp_model.py

Phase 8c test plan V2: the programs with sampling (tb/golden/kpke_smp_model.py), STORE and STREAM, run with the golden primitives, equal the unmodified golden K-PKE (tb/golden/kpke.py):
KeyGen t_hat equals byte_decode(12, ek_PKE) and s_hat equals the decoded secret key; Encrypt u, v (compressed, encoded) equal the ciphertext of k_pke_encrypt; Decrypt returns the message; STREAM equals STORE in the logical slots 9-20;
operation counts: transforms and PWM as in Phase 6 (6/0/9, 3/4/12, 3/1/3), SMP 15 / 16 / 0 in STORE and 6 / 7 / 0 in STREAM.
"""
import random

import pytest

import kpke
from kpke_smp_model import OVERLAP, STORE, STREAM, STRESS, check_hazards, empty_slots, inputs, logical, phys, programs, run
from params import DU, DV, K
from primitives import byte_decode, byte_encode, compress

SEEDS = range(8)
VARS = (STORE, STREAM, OVERLAP, STRESS)


def _rand(rng, n=32):
    return bytes(rng.randrange(256) for _ in range(n))


@pytest.mark.parametrize("variant", VARS)
@pytest.mark.parametrize("seed", SEEDS)
def test_keygen_equals_golden(variant, seed):
    rng = random.Random(300 + seed)
    d = _rand(rng)
    ek, dk = kpke.k_pke_keygen(d)
    slots, rho, sd = inputs(variant, "keygen", d=d)
    counts = run(programs(variant)["keygen"], slots, rho, sd)
    assert [logical(variant, slots, 12 + i) for i in range(K)] == [byte_decode(12, ek[384 * i: 384 * (i + 1)]) for i in range(K)]
    assert [logical(variant, slots, 9 + i) for i in range(K)] == [byte_decode(12, dk[384 * i: 384 * (i + 1)]) for i in range(K)]
    assert counts == {"NTT": 6, "INTT": 0, "PWM": 9, "ADD": 3, "SUB": 0, "SMP": 15 if variant == STORE else 6}


@pytest.mark.parametrize("variant", VARS)
@pytest.mark.parametrize("seed", SEEDS)
def test_encrypt_equals_golden(variant, seed):
    rng = random.Random(400 + seed)
    ek, _ = kpke.k_pke_keygen(_rand(rng))
    m, r = _rand(rng), _rand(rng)
    c = kpke.k_pke_encrypt(ek, m, r)
    slots, rho, sd = inputs(variant, "encrypt", ek_pke=ek, m=m, r=r)
    counts = run(programs(variant)["encrypt"], slots, rho, sd)
    c1 = b"".join(byte_encode(DU, compress(DU, logical(variant, slots, 12 + i))) for i in range(K))
    c2 = byte_encode(DV, compress(DV, logical(variant, slots, 19)))
    assert c1 + c2 == c
    assert counts == {"NTT": 3, "INTT": 4, "PWM": 12, "ADD": 5, "SUB": 0, "SMP": 16 if variant == STORE else 7}


@pytest.mark.parametrize("variant", VARS)
@pytest.mark.parametrize("seed", SEEDS)
def test_decrypt_equals_golden(variant, seed):
    rng = random.Random(500 + seed)
    ek, dk = kpke.k_pke_keygen(_rand(rng))
    m, r = _rand(rng), _rand(rng)
    c = kpke.k_pke_encrypt(ek, m, r)
    slots, rho, sd = inputs(variant, "decrypt", dk_pke=dk, c=c)
    counts = run(programs(variant)["decrypt"], slots, rho, sd)
    assert byte_encode(1, compress(1, logical(variant, slots, 19))) == m
    assert counts == {"NTT": 3, "INTT": 1, "PWM": 3, "ADD": 0, "SUB": 1, "SMP": 0}


@pytest.mark.parametrize("variant", (OVERLAP, STRESS))
@pytest.mark.parametrize("seed", range(4))
def test_overlap_equals_stream_in_logical_slots(variant, seed):
    rng = random.Random(700 + seed)
    d = _rand(rng)
    a, rho, sd = inputs(STREAM, "keygen", d=d)
    b, _, _ = inputs(variant, "keygen", d=d)
    run(programs(STREAM)["keygen"], a, rho, sd)
    run(programs(variant)["keygen"], b, rho, sd)
    ek, _ = kpke.k_pke_keygen(d)
    m, r = _rand(rng), _rand(rng)
    a2, rho2, sd2 = inputs(STREAM, "encrypt", ek_pke=ek, m=m, r=r)
    b2, _, _ = inputs(variant, "encrypt", ek_pke=ek, m=m, r=r)
    run(programs(STREAM)["encrypt"], a2, rho2, sd2)
    run(programs(variant)["encrypt"], b2, rho2, sd2)
    assert all(logical(STREAM, a, s) == logical(variant, b, s) for s in range(9, 21))
    assert all(logical(STREAM, a2, s) == logical(variant, b2, s) for s in range(9, 21))


@pytest.mark.parametrize("seed", range(4))
def test_stream_equals_store_in_logical_slots(seed):
    rng = random.Random(600 + seed)
    d = _rand(rng)
    a, rho, sd = inputs(STORE, "keygen", d=d)
    b, _, _ = inputs(STREAM, "keygen", d=d)
    run(programs(STORE)["keygen"], a, rho, sd)
    run(programs(STREAM)["keygen"], b, rho, sd)
    assert all(logical(STORE, a, s) == logical(STREAM, b, s) for s in range(9, 21))
    ek, _ = kpke.k_pke_keygen(d)
    m, r = _rand(rng), _rand(rng)
    a, rho, sd = inputs(STORE, "encrypt", ek_pke=ek, m=m, r=r)
    b, _, _ = inputs(STREAM, "encrypt", ek_pke=ek, m=m, r=r)
    run(programs(STORE)["encrypt"], a, rho, sd)
    run(programs(STREAM)["encrypt"], b, rho, sd)
    assert all(logical(STORE, a, s) == logical(STREAM, b, s) for s in range(9, 21))


def test_slot_ranges_and_streamed_operands():
    for variant in VARS:
        for name, prog in programs(variant).items():
            for opc, d, a, b, f, l in prog:
                assert d < (24 if variant == STORE else 12)
    for variant in (STREAM, OVERLAP, STRESS):
        st = programs(variant)
        assert sum(1 for name in ("keygen", "encrypt") for op in st[name] if op[0] == 8) == 18   # nine streamed entries each
    assert phys(STREAM, 9) == 0 and phys(STREAM, 20) == 11


@pytest.mark.parametrize("variant", (OVERLAP, STRESS))
def test_overlap_programs_have_no_hazard_and_do_overlap(variant):
    for name, prog in programs(variant).items():
        assert check_hazards(prog) == [], (variant, name)
    ov = programs(variant)
    nb = {n: sum(1 for op in p if op[0] == 6 and op[4]) for n, p in ov.items()}
    assert nb["decrypt"] == 0
    assert (nb["keygen"], nb["encrypt"]) == ((5, 6) if variant == OVERLAP else (5, 1))


def test_hazard_checker_detects_a_read_before_wait():
    from kpke_smp_model import OP_NTT, OP_SMPN, OP_WAIT
    prog = [(OP_SMPN, 3, 0, 1, 1, 0), (OP_NTT, 3, 0, 0, 0, 0)]
    assert check_hazards(prog) == [(1, 3)]
    assert check_hazards([prog[0], (OP_WAIT, 0, 0, 0, 0, 0), prog[1]]) == []
