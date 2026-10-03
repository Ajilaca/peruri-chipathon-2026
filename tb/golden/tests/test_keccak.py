"""tb/golden/tests/test_keccak.py

Phase 7 test plan V2: the golden Keccak (tb/golden/keccak.py) equals Python hashlib for every mode, the boundary lengths of the test plan (section 3) and
the ML-KEM-768 input and output lengths; the per-round trace composes to keccak_f1600; the generated tables match FIPS 202 known values.
Random inputs use the stdlib `random` with a fixed seed per test.
"""

import hashlib
import random

import pytest

import keccak as K

RATES = {"sha3_256": 136, "sha3_512": 72, "shake_128": 168, "shake_256": 136}
ML_KEM_LENGTHS = [32, 33, 34, 64, 1120, 1184]


def _ref(mode, msg, outlen):
    h = getattr(hashlib, mode)(msg)
    return h.digest() if mode.startswith("sha3") else h.digest(outlen)


def _mine(mode, msg, outlen):
    if mode == "sha3_256":
        return K.sha3_256(msg)
    if mode == "sha3_512":
        return K.sha3_512(msg)
    return getattr(K, mode)(msg, outlen)


def _lengths(rate):
    base = {0, 1, 7, 8, 9, rate - 1, rate, rate + 1, 2 * rate - 1, 2 * rate, 2 * rate + 1, 3 * rate, 3 * rate + 1}
    return sorted(base | set(range(0, 3 * rate + 2)) | set(ML_KEM_LENGTHS))


@pytest.mark.parametrize("mode", RATES)
def test_all_boundary_lengths_equal_hashlib(mode):
    rng = random.Random(700)
    outlen = {"sha3_256": 32, "sha3_512": 64, "shake_128": 168 * 2 + 5, "shake_256": 136 * 2 + 5}[mode]
    for n in _lengths(RATES[mode]):
        for msg in (bytes(rng.randrange(256) for _ in range(n)), bytes(n), b"\xff" * n):
            assert _mine(mode, msg, outlen) == _ref(mode, msg, outlen), (mode, n)


@pytest.mark.parametrize("mode", RATES)
def test_random_lengths_up_to_2000(mode):
    rng = random.Random(701)
    for _ in range(50):
        n = rng.randrange(2001)
        msg = bytes(rng.randrange(256) for _ in range(n))
        outlen = rng.randrange(1, 700)
        assert _mine(mode, msg, outlen) == _ref(mode, msg, outlen), (mode, n, outlen)


@pytest.mark.parametrize("mode", ["shake_128", "shake_256"])
def test_shake_output_lengths(mode):
    rng = random.Random(702)
    msg = bytes(rng.randrange(256) for _ in range(34))
    rate = RATES[mode]
    for out in list(range(0, 3 * rate + 2)) + [128, 504, 840, 3 * rate * 2]:
        assert _mine(mode, msg, out) == _ref(mode, msg, out), (mode, out)


def test_trace_composes_to_permutation():
    rng = random.Random(703)
    for _ in range(20):
        a = [rng.getrandbits(64) for _ in range(25)]
        tr = K.keccak_trace(a)
        assert len(tr) == 24
        b = a
        for ir in range(24):
            b = K.keccak_round(b, ir)
            assert b == tr[ir]
        assert tr[-1] == K.keccak_f1600(a)


def test_permutation_of_zero_state_known_value():
    # first lane of Keccak-f[1600] applied to the all-zero state (reference value of the Keccak team, as used by SHA3 KATs):
    # derived independently here through hashlib: the sponge with rate 136 of an empty message permutes one padded block, so
    # SHA3-256("") = first 32 bytes of the state after f(0x06 0 ... 0x80 0 ...), which pins every round on a nonzero input.
    blk = bytes([0x06]) + bytes(134) + bytes([0x80]) + bytes(64)
    st = K.state_to_bytes(K.keccak_f1600(K.bytes_to_state(blk)))
    assert st[:32] == hashlib.sha3_256(b"").digest()


def test_single_bit_states_state_after_each_round_are_a_bijection_chain():
    # all 1,600 single-bit states: pi, rho, theta, chi, iota are permutations of the state space, so distinct inputs give distinct outputs
    seen = set()
    for bit in range(1600):
        a = [0] * 25
        a[bit // 64] = 1 << (bit % 64)
        seen.add(tuple(K.keccak_f1600(a)))
    assert len(seen) == 1600


def test_round_constants_and_offsets_match_fips202():
    # FIPS 202 Table 1 (rho offsets) and the 24 round constants of the Keccak reference (values given in FIPS 202 Appendix / Keccak team tables)
    assert K.RHO == [0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39, 41, 45, 15, 21, 8, 18, 2, 61, 56, 14]
    assert K.RC[0] == 0x0000000000000001
    assert K.RC[1] == 0x0000000000008082
    assert K.RC[2] == 0x800000000000808A
    assert K.RC[23] == 0x8000000080008008
    # the reference table repeats two values (rounds 5 and 22: 0x80000001; rounds 6 and 20: 0x8000000080008081), so 22 distinct values
    assert K.RC[5] == K.RC[22] == 0x0000000080000001 and K.RC[6] == K.RC[20] == 0x8000000080008081
    assert len(set(K.RC)) == 22


def test_pad_forms():
    assert K.pad(136, 0x06, 135) == bytes([0x86])
    assert K.pad(136, 0x06, 136) == bytes([0x06]) + bytes(134) + b"\x80"
    assert K.pad(168, 0x1F, 0) == bytes([0x1F]) + bytes(166) + b"\x80"
    assert (135 + len(K.pad(136, 0x06, 135))) % 136 == 0


def test_permutation_counts_mlkem_calls():
    assert K.num_perms("sha3_256", 1184) == 9  # H(ek)
    assert K.num_perms("sha3_512", 64) == 1  # G
    assert K.num_perms("shake_256", 33, 128) == 1  # PRF eta = 2
    assert K.num_perms("shake_256", 1088 + 32, 32) == 9  # J
    assert K.num_perms("shake_128", 34, 840) == 5
    assert K.num_perms("shake_128", 0, 168) == 1 and K.num_perms("shake_128", 0, 169) == 2
