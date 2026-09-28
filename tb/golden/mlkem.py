"""tb/golden/mlkem.py

Pure-Python transcription of the ML-KEM key-encapsulation mechanism (FIPS
203, Sections 6-7) for ML-KEM-768: the deterministic internal algorithms
(KeyGen_internal, Encaps_internal, Decaps_internal, Algorithms 16-18), the
required input checks (Section 7.2, 7.3), and the randomized public
wrappers (KeyGen, Encaps, Decaps, Algorithms 19-21) that draw fresh
randomness from os.urandom.

This is a golden model for verification, not a constant-time
implementation: branches here (e.g. the ciphertext-comparison / implicit
rejection in ml_kem_decaps_internal, and the `if` in the input-check
wrappers) depend on secret or attacker-controlled data. No claim is made,
and none should be inferred, about timing or side-channel behaviour of
this Python code; constant-time behaviour is an RTL-level property to be
measured later (mlkem-guard SKILL.md).
"""

from __future__ import annotations

import os

from kpke import k_pke_decrypt, k_pke_encrypt, k_pke_keygen
from params import CT_BYTES, DK_BYTES, DU, DV, EK_BYTES, K, SS_BYTES
from primitives import G, H, J, byte_decode, byte_encode

# ---------------------------------------------------------------------------
# 7.2 / 7.3 Input checks (must run before Encaps / Decaps are used publicly)
# ---------------------------------------------------------------------------


def check_encapsulation_key(ek: bytes) -> bool:
    """Section 7.2, "Encapsulation key check" (Algorithm 20 precondition).

    1. Type check: ek must be 384*k + 32 bytes.
    2. Modulus check: re-encoding the decoded coefficients must reproduce
       ek byte-for-byte, i.e. every encoded coefficient is in [0, q-1].
    """
    k = K
    if len(ek) != 384 * k + 32:
        return False
    test = b"".join(
        byte_encode(12, byte_decode(12, ek[384 * i : 384 * (i + 1)])) for i in range(k)
    )
    return test == ek[: 384 * k]


def check_decapsulation_input(dk: bytes, c: bytes) -> bool:
    """Section 7.3, "Decapsulation input check" (Algorithm 21 precondition).

    1. Ciphertext type check: c must be 32*(du*k + dv) bytes.
    2. Decapsulation key type check: dk must be 768*k + 96 bytes.
    3. Hash check: dk's stored hash of ek_PKE must match H(ek_PKE).

    (This standard also defines a separate, optional "key pair check" in
    Section 7.1 for freshly generated key pairs; that check is not part of
    the mandatory per-call Decaps input check and is not implemented here.)
    """
    k = K
    if len(c) != 32 * (DU * k + DV):
        return False
    if len(dk) != 768 * k + 96:
        return False
    ek_pke = dk[384 * k : 768 * k + 32]
    test = H(ek_pke)
    return test == dk[768 * k + 32 : 768 * k + 64]


# ---------------------------------------------------------------------------
# Algorithm 16: ML-KEM.KeyGen_internal(d, z)
# ---------------------------------------------------------------------------


def ml_kem_keygen_internal(d: bytes, z: bytes) -> tuple[bytes, bytes]:
    """ML-KEM.KeyGen_internal(d, z) -> (ek, dk).  (Section 6.1, Algorithm 16)

    Deterministic: all randomness is the caller-supplied seeds d, z.
    """
    assert len(d) == 32
    assert len(z) == 32
    ek_pke, dk_pke = k_pke_keygen(d)  # line 1
    ek = ek_pke  # line 2
    dk = dk_pke + ek + H(ek) + z  # line 3
    assert len(ek) == EK_BYTES
    assert len(dk) == DK_BYTES
    return ek, dk


# ---------------------------------------------------------------------------
# Algorithm 17: ML-KEM.Encaps_internal(ek, m)
# ---------------------------------------------------------------------------


def ml_kem_encaps_internal(ek: bytes, m: bytes) -> tuple[bytes, bytes]:
    """ML-KEM.Encaps_internal(ek, m) -> (K, c).  (Section 6.2, Algorithm 17)

    Deterministic: all randomness is the caller-supplied m.
    """
    assert len(m) == 32
    K_, r = G(m + H(ek))  # line 1
    c = k_pke_encrypt(ek, m, r)  # line 2
    assert len(c) == CT_BYTES
    return K_, c  # line 3


# ---------------------------------------------------------------------------
# Algorithm 18: ML-KEM.Decaps_internal(dk, c)
# ---------------------------------------------------------------------------


def ml_kem_decaps_internal(dk: bytes, c: bytes) -> bytes:
    """ML-KEM.Decaps_internal(dk, c) -> K'.  (Section 6.3, Algorithm 18)

    Deterministic; performs FIPS 203's "implicit rejection": if the
    re-encrypted ciphertext c' does not match c, the output is replaced by
    a hash of (z, c) instead of the derived key K', so a decapsulation
    failure still returns a well-defined (but useless to the attacker)
    32-byte value rather than an error.
    """
    k = K
    assert len(dk) == DK_BYTES
    assert len(c) == CT_BYTES

    dk_pke = dk[: 384 * k]  # line 1
    ek_pke = dk[384 * k : 768 * k + 32]  # line 2
    h = dk[768 * k + 32 : 768 * k + 64]  # line 3
    z = dk[768 * k + 64 : 768 * k + 96]  # line 4

    m_prime = k_pke_decrypt(dk_pke, c)  # line 5
    K_prime, r_prime = G(m_prime + h)  # line 6
    K_bar = J(z + c)  # line 7
    c_prime = k_pke_encrypt(ek_pke, m_prime, r_prime)  # line 8

    if c != c_prime:  # lines 9-11: implicit rejection
        K_prime = K_bar
    return K_prime  # line 12


# ---------------------------------------------------------------------------
# Algorithms 19-21: public wrappers, randomness from os.urandom
# ---------------------------------------------------------------------------


def ml_kem_keygen() -> tuple[bytes, bytes]:
    """ML-KEM.KeyGen() -> (ek, dk).  (Section 7.1, Algorithm 19)

    os.urandom never returns the standard's NULL / RBG-failure sentinel
    (it raises instead if the OS source is unavailable), so the "return
    the failure indicator" branch of Algorithm 19 (lines 3-5) has no
    representable case here and is not modelled.
    """
    d = os.urandom(32)  # line 1
    z = os.urandom(32)  # line 2
    return ml_kem_keygen_internal(d, z)  # line 6


def ml_kem_encaps(ek: bytes) -> tuple[bytes, bytes]:
    """ML-KEM.Encaps(ek) -> (K, c).  (Section 7.2, Algorithm 20)

    Runs the mandatory encapsulation-key check first ("ML-KEM.Encaps shall
    not be run with an encapsulation key that has not been checked").
    """
    if not check_encapsulation_key(ek):
        raise ValueError("ek failed the FIPS 203 Section 7.2 encapsulation key check")
    m = os.urandom(32)  # line 1
    return ml_kem_encaps_internal(ek, m)  # line 5


def ml_kem_decaps(dk: bytes, c: bytes) -> bytes:
    """ML-KEM.Decaps(dk, c) -> K'.  (Section 7.3, Algorithm 21)

    Runs the mandatory decapsulation input check first ("Ciphertext
    checking shall be performed with every execution of ML-KEM.Decaps").
    """
    if not check_decapsulation_input(dk, c):
        raise ValueError("dk/c failed the FIPS 203 Section 7.3 decapsulation input check")
    return ml_kem_decaps_internal(dk, c)  # line 1
