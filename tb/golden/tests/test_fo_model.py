"""tb/golden/tests/test_fo_model.py -- Phase 9b test plan V2: the hardware-form comparison and selection of tb/golden/fo_model.py equals the unmodified golden Decaps."""
import random

import fo_model as F
from kpke import k_pke_decrypt, k_pke_encrypt
from mlkem import ml_kem_decaps_internal, ml_kem_encaps_internal, ml_kem_keygen_internal
from params import CT_BYTES, K
from primitives import G, J


def _decaps_with_model(dk: bytes, c: bytes) -> bytes:
    dk_pke, ek_pke = dk[: 384 * K], dk[384 * K: 768 * K + 32]
    h, z = dk[768 * K + 32: 768 * K + 64], dk[768 * K + 64: 768 * K + 96]
    m_prime = k_pke_decrypt(dk_pke, c)
    k_prime, r_prime = G(m_prime + h)
    k_bar = J(z + c)
    c_prime = k_pke_encrypt(ek_pke, m_prime, r_prime)
    return F.fo_select(c, c_prime, k_prime, k_bar)


def test_select_for_equal_and_every_single_bit_change():
    rng = random.Random(940)
    c = bytes(rng.randrange(256) for _ in range(CT_BYTES))
    kg, kb = bytes(rng.randrange(256) for _ in range(32)), bytes(rng.randrange(256) for _ in range(32))
    assert F.fo_select(c, c, kg, kb) == kg
    for bit in range(8 * CT_BYTES):
        d = bytearray(c)
        d[bit // 8] ^= 1 << (bit % 8)
        assert F.ct_differs(c, bytes(d)) == 1
        assert F.fo_select(c, bytes(d), kg, kb) == kb, bit


def test_select_with_complementary_and_special_keys():
    c = bytes(CT_BYTES)
    d = bytes([1]) + bytes(CT_BYTES - 1)
    for kg, kb in ((bytes(32), bytes([255]) * 32), (bytes([255]) * 32, bytes(32)), (bytes(range(32)), bytes(255 - i for i in range(32)))):
        assert F.fo_select(c, c, kg, kb) == kg
        assert F.fo_select(c, d, kg, kb) == kb


def test_end_to_end_equals_golden_decaps_valid_and_changed_ciphertexts():
    rng = random.Random(941)
    dseed, zseed, m = bytes(rng.randrange(256) for _ in range(32)), bytes(rng.randrange(256) for _ in range(32)), bytes(rng.randrange(256) for _ in range(32))
    ek, dk = ml_kem_keygen_internal(dseed, zseed)
    key, c = ml_kem_encaps_internal(ek, m)
    assert _decaps_with_model(dk, c) == ml_kem_decaps_internal(dk, c) == key
    for _ in range(40):
        bit = rng.randrange(8 * CT_BYTES)
        d = bytearray(c)
        d[bit // 8] ^= 1 << (bit % 8)
        assert _decaps_with_model(dk, bytes(d)) == ml_kem_decaps_internal(dk, bytes(d)) != key
