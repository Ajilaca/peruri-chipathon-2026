"""tb/golden/fo_model.py

Golden model of the Phase 9b comparison and key selection of ML-KEM.Decaps_internal (FIPS 203 Algorithm 18 lines 8-11, docs/evidence/phase09-integration/9b/test_plan_9b.md), written in the form of the hardware:
the two ciphertexts are compared word by word (64-bit words, byte k of word w is byte 8w + k) as the OR of all XORs, with no early exit, and the key is selected with a 256-bit mask, not with a branch.
Independent of any RTL; checked against the unmodified golden `mlkem.ml_kem_decaps_internal` in tb/golden/tests/test_fo_model.py.
"""

WORD = 8
MASK256 = (1 << 256) - 1


def words(b: bytes) -> list[int]:
    assert len(b) % WORD == 0
    return [int.from_bytes(b[i: i + WORD], "little") for i in range(0, len(b), WORD)]


def ct_differs(c: bytes, c_prime: bytes) -> int:
    """1 if the ciphertexts differ, else 0: the OR of the XORs of all words (every word is visited)."""
    assert len(c) == len(c_prime)
    acc = 0
    for a, b in zip(words(c), words(c_prime)):
        acc |= a ^ b
    return int(acc != 0)


def fo_select(c: bytes, c_prime: bytes, k_good: bytes, k_bad: bytes) -> bytes:
    """K = K_bar if c != c' else K', by mask: (k_good & ~m) | (k_bad & m) with m all ones when the ciphertexts differ."""
    assert len(k_good) == len(k_bad) == 32
    m = MASK256 * ct_differs(c, c_prime)
    g, b = int.from_bytes(k_good, "little"), int.from_bytes(k_bad, "little")
    return (((g & ~m) | (b & m)) & MASK256).to_bytes(32, "little")
