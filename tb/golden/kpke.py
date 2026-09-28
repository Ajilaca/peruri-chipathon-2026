"""tb/golden/kpke.py

Pure-Python transcription of the K-PKE component scheme (FIPS 203, Section
5): K-PKE.KeyGen (Algorithm 13), K-PKE.Encrypt (Algorithm 14), and
K-PKE.Decrypt (Algorithm 15), for ML-KEM-768 (k, eta1, eta2, du, dv fixed
by tb/golden/params.py).

K-PKE is NOT an approved stand-alone scheme (Section 3.3: "K-PKE.KeyGen,
K-PKE.Encrypt, and K-PKE.Decrypt are not approved for use as a public-key
encryption scheme"); it exists only as a subroutine of ML-KEM
(tb/golden/mlkem.py). This module performs no input checking of its own
(Section 5: "The algorithms in this section do not perform any input
checking because they are only invoked as subroutines of the main ML-KEM
algorithms"); the caller's asserts below only check data-type lengths.

This is a golden model, not a constant-time implementation: it makes no
claim about timing or side-channel behaviour.
"""

from __future__ import annotations

from params import DU, DV, ETA1, ETA2, K, N, Q
from primitives import (
    G,
    PRF,
    byte_decode,
    byte_encode,
    compress,
    decompress,
    intt,
    multiply_ntts,
    ntt,
    sample_ntt,
    sample_poly_cbd,
)

# ---------------------------------------------------------------------------
# Small linear-algebra helpers over T_q vectors/matrices (Sections 2.4.6-2.4.7)
# ---------------------------------------------------------------------------


def _poly_add(f: list[int], g: list[int]) -> list[int]:
    return [(a + b) % Q for a, b in zip(f, g)]


def _poly_sub(f: list[int], g: list[int]) -> list[int]:
    return [(a - b) % Q for a, b in zip(f, g)]


def _sample_matrix(rho: bytes, k: int) -> list[list[list[int]]]:
    """A_hat[i][j] <- SampleNTT(rho || j || i), for i,j in 0..k-1.

    Used identically in K-PKE.KeyGen (Alg 13, line 5) and K-PKE.Encrypt
    (Alg 14, line 6) so both regenerate the same matrix from the seed rho.
    """
    A_hat = [[None] * k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            A_hat[i][j] = sample_ntt(rho + bytes([j]) + bytes([i]))
    return A_hat


def _mat_vec_mul(A_hat, u_hat, k: int) -> list[list[int]]:
    """w_hat = A_hat o u_hat  (eq. 2.12): w[i] = sum_j A[i,j] *_Tq u[j]."""
    out = []
    for i in range(k):
        acc = [0] * N
        for j in range(k):
            acc = _poly_add(acc, multiply_ntts(A_hat[i][j], u_hat[j]))
        out.append(acc)
    return out


def _mat_transpose_vec_mul(A_hat, u_hat, k: int) -> list[list[int]]:
    """y_hat = A_hat^T o u_hat  (eq. 2.13): y[i] = sum_j A[j,i] *_Tq u[j]."""
    out = []
    for i in range(k):
        acc = [0] * N
        for j in range(k):
            acc = _poly_add(acc, multiply_ntts(A_hat[j][i], u_hat[j]))
        out.append(acc)
    return out


def _vec_dot(u_hat, v_hat, k: int) -> list[int]:
    """z_hat = u_hat^T o v_hat  (eq. 2.14): z = sum_j u[j] *_Tq v[j]."""
    acc = [0] * N
    for j in range(k):
        acc = _poly_add(acc, multiply_ntts(u_hat[j], v_hat[j]))
    return acc


# ---------------------------------------------------------------------------
# Algorithm 13: K-PKE.KeyGen(d)
# ---------------------------------------------------------------------------


def k_pke_keygen(d: bytes) -> tuple[bytes, bytes]:
    """K-PKE.KeyGen(d) -> (ek_PKE, dk_PKE).  (Section 5.1, Algorithm 13)"""
    assert len(d) == 32
    k = K
    rho, sigma = G(d + bytes([k]))  # line 1
    ctr = 0
    A_hat = _sample_matrix(rho, k)  # lines 3-7

    s = []
    for _ in range(k):  # lines 8-11
        s.append(sample_poly_cbd(ETA1, PRF(ETA1, sigma, ctr)))
        ctr += 1
    e = []
    for _ in range(k):  # lines 12-15
        e.append(sample_poly_cbd(ETA1, PRF(ETA1, sigma, ctr)))
        ctr += 1

    s_hat = [ntt(p) for p in s]  # line 16
    e_hat = [ntt(p) for p in e]  # line 17
    t_hat = [
        _poly_add(a, b) for a, b in zip(_mat_vec_mul(A_hat, s_hat, k), e_hat)
    ]  # line 18

    ek_pke = b"".join(byte_encode(12, t_hat[i]) for i in range(k)) + rho  # line 19
    dk_pke = b"".join(byte_encode(12, s_hat[i]) for i in range(k))  # line 20
    return ek_pke, dk_pke


# ---------------------------------------------------------------------------
# Algorithm 14: K-PKE.Encrypt(ek_PKE, m, r)
# ---------------------------------------------------------------------------


def k_pke_encrypt(ek_pke: bytes, m: bytes, r: bytes) -> bytes:
    """K-PKE.Encrypt(ek_PKE, m, r) -> c.  (Section 5.2, Algorithm 14)"""
    k = K
    assert len(ek_pke) == 384 * k + 32
    assert len(m) == 32
    assert len(r) == 32

    ctr = 0
    t_hat = [byte_decode(12, ek_pke[384 * i : 384 * (i + 1)]) for i in range(k)]  # line 2
    rho = ek_pke[384 * k : 384 * k + 32]  # line 3
    A_hat = _sample_matrix(rho, k)  # lines 4-8

    y = []
    for _ in range(k):  # lines 9-12
        y.append(sample_poly_cbd(ETA1, PRF(ETA1, r, ctr)))
        ctr += 1
    e1 = []
    for _ in range(k):  # lines 13-16
        e1.append(sample_poly_cbd(ETA2, PRF(ETA2, r, ctr)))
        ctr += 1
    e2 = sample_poly_cbd(ETA2, PRF(ETA2, r, ctr))  # line 17
    ctr += 1

    y_hat = [ntt(p) for p in y]  # line 18
    u = [
        _poly_add(a, b)
        for a, b in zip(
            [intt(p) for p in _mat_transpose_vec_mul(A_hat, y_hat, k)], e1
        )
    ]  # line 19
    mu = decompress(1, byte_decode(1, m))  # line 20
    v = _poly_add(_poly_add(intt(_vec_dot(t_hat, y_hat, k)), e2), mu)  # line 21

    c1 = b"".join(byte_encode(DU, compress(DU, u[i])) for i in range(k))  # line 22
    c2 = byte_encode(DV, compress(DV, v))  # line 23
    return c1 + c2  # line 24


# ---------------------------------------------------------------------------
# Algorithm 15: K-PKE.Decrypt(dk_PKE, c)
# ---------------------------------------------------------------------------


def k_pke_decrypt(dk_pke: bytes, c: bytes) -> bytes:
    """K-PKE.Decrypt(dk_PKE, c) -> m.  (Section 5.3, Algorithm 15)"""
    k = K
    assert len(dk_pke) == 384 * k
    assert len(c) == 32 * (DU * k + DV)

    c1 = c[: 32 * DU * k]  # line 1
    c2 = c[32 * DU * k : 32 * (DU * k + DV)]  # line 2
    u_prime = [
        decompress(DU, byte_decode(DU, c1[32 * DU * i : 32 * DU * (i + 1)]))
        for i in range(k)
    ]  # line 3
    v_prime = decompress(DV, byte_decode(DV, c2))  # line 4
    s_hat = [byte_decode(12, dk_pke[384 * i : 384 * (i + 1)]) for i in range(k)]  # line 5

    u_hat = [ntt(p) for p in u_prime]
    # line 6: w <- v' - NTT^-1(s_hat^T o NTT(u'))
    # (Note: the algorithm's own inline comment in FIPS 203 erroneously says
    # "decode plaintext m from polynomial v" on the next line; the body
    # uses w, matching errata item #2, see
    # docs/evidence/golden/fips203_errata_2026-09-28.md.)
    w = _poly_sub(v_prime, intt(_vec_dot(s_hat, u_hat, k)))
    m = byte_encode(1, compress(1, w))  # line 7
    return m
