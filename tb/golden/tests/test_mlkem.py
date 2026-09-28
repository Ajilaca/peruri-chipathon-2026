"""tb/golden/tests/test_mlkem.py

End-to-end property tests for the ML-KEM-768 golden model
(tb/golden/mlkem.py, tb/golden/kpke.py), independent of official KAT
vectors (those come in a later Phase 0 step). Uses ml_kem_keygen(), which
draws randomness from os.urandom, so each test run uses fresh random key
pairs, not a fixed seed.
"""

import random

import pytest

from params import CT_BYTES, DK_BYTES, EK_BYTES, SS_BYTES
from mlkem import ml_kem_decaps, ml_kem_decaps_internal, ml_kem_encaps, ml_kem_keygen

N_TRIALS = 500


# ---------------------------------------------------------------------------
# Decaps(dk, Encaps(ek)) == K, for 500 random seeds (each ml_kem_keygen()
# call and each ml_kem_encaps() call draws a fresh os.urandom seed).
# ---------------------------------------------------------------------------


def test_decaps_recovers_encaps_key_500_trials():
    for _ in range(N_TRIALS):
        ek, dk = ml_kem_keygen()
        K, c = ml_kem_encaps(ek)
        K_prime = ml_kem_decaps(dk, c)
        assert K_prime == K


# ---------------------------------------------------------------------------
# A one-bit-flipped ciphertext deterministically yields a K-bar different
# from K (implicit rejection, Algorithm 18 lines 9-11).
# ---------------------------------------------------------------------------


def test_bit_flipped_ciphertext_triggers_deterministic_implicit_rejection():
    rng = random.Random(42)
    for _ in range(20):
        ek, dk = ml_kem_keygen()
        K, c = ml_kem_encaps(ek)

        byte_idx = rng.randrange(len(c))
        bit_idx = rng.randrange(8)
        flipped = bytearray(c)
        flipped[byte_idx] ^= 1 << bit_idx
        c_bad = bytes(flipped)

        K_bar_1 = ml_kem_decaps(dk, c_bad)
        K_bar_2 = ml_kem_decaps(dk, c_bad)

        # Different from the real shared secret.
        assert K_bar_1 != K
        # Implicit rejection is deterministic for a fixed (dk, c_bad).
        assert K_bar_1 == K_bar_2
        # And matches calling the internal algorithm directly.
        assert K_bar_1 == ml_kem_decaps_internal(dk, c_bad)


# ---------------------------------------------------------------------------
# Lengths match EK_BYTES, DK_BYTES, CT_BYTES, SS_BYTES (Section 8, Table 3).
# ---------------------------------------------------------------------------


def test_key_and_ciphertext_lengths_match_table_3():
    ek, dk = ml_kem_keygen()
    assert len(ek) == EK_BYTES
    assert len(dk) == DK_BYTES
    K, c = ml_kem_encaps(ek)
    assert len(c) == CT_BYTES
    assert len(K) == SS_BYTES
    K_prime = ml_kem_decaps(dk, c)
    assert len(K_prime) == SS_BYTES


# ---------------------------------------------------------------------------
# check_params.py must still pass (locked parameters untouched by this work).
# ---------------------------------------------------------------------------


def test_check_params_script_still_passes():
    import pathlib
    import subprocess
    import sys

    repo_root = pathlib.Path(__file__).resolve().parents[3]
    script = repo_root / ".claude" / "skills" / "mlkem-guard" / "scripts" / "check_params.py"
    result = subprocess.run(
        [sys.executable, str(script)], capture_output=True, text=True, cwd=repo_root
    )
    assert result.returncode == 0, result.stdout + result.stderr
