"""tb/golden/kpke_sched_model.py

Phase 6 (docs/evidence/phase06-scheduling/test_plan.md): the K-PKE arithmetic of KeyGen, Encrypt and Decrypt as fixed programs of polynomial operations on numbered slots, run with the golden
primitives (ntt, intt, multiply_ntts). The same program list is turned into the RTL program ROM by scripts/gen_kpke_prog.py, so the hardware runs exactly this schedule.

Operations (one polynomial = 256 coefficients in [0, q)):
  NTT   s           slot s <- NTT(slot s)
  INTT  s           slot s <- NTT^-1(slot s)               (FIPS 203 Algorithm 10, including the final scaling)
  PWM   d a b F L   acc <- (F ? 0 : acc) + slot a o slot b  (MultiplyNTTs, Algorithm 11); when L: slot d <- acc
  ADD   d a b       slot d <- slot a + slot b
  SUB   d a b       slot d <- slot a - slot b
Slots: A_hat[i][j] in 3i + j (0-8); 9-11, 12-14 vectors; 15 temporary; 16-18 t_hat (Encrypt); 19, 20 single polynomials.
Inputs come from the golden K-PKE's own sampling (same calls, same order), outputs are compared with the unmodified golden K-PKE (tb/golden/tests/test_kpke_sched_model.py).
"""
from __future__ import annotations

from params import DU, DV, ETA1, ETA2, K, N, Q
from primitives import G, PRF, byte_decode, decompress, intt, multiply_ntts, ntt, sample_ntt, sample_poly_cbd

NPOLY = 24
TMP = 15
OP_END, OP_NTT, OP_INTT, OP_PWM, OP_ADD, OP_SUB = range(6)
OPNAME = {OP_NTT: "NTT", OP_INTT: "INTT", OP_PWM: "PWM", OP_ADD: "ADD", OP_SUB: "SUB"}


def _op(opc, d=0, a=0, b=0, first=0, last=0):
    return (opc, d, a, b, first, last)


def _pwm_sum(dst, pairs):
    """PWM passes accumulating sum over (a, b) pairs into dst."""
    n = len(pairs)
    return [_op(OP_PWM, dst, a, b, int(i == 0), int(i == n - 1)) for i, (a, b) in enumerate(pairs)]


def _keygen():
    p = [_op(OP_NTT, 9 + j) for j in range(K)] + [_op(OP_NTT, 12 + j) for j in range(K)]
    for i in range(K):
        p += _pwm_sum(TMP, [(3 * i + j, 9 + j) for j in range(K)])
        p.append(_op(OP_ADD, 12 + i, TMP, 12 + i))
    return p


def _encrypt():
    p = [_op(OP_NTT, 9 + j) for j in range(K)]
    for i in range(K):
        p += _pwm_sum(TMP, [(3 * j + i, 9 + j) for j in range(K)])        # A_hat^T o y_hat
        p.append(_op(OP_INTT, TMP))
        p.append(_op(OP_ADD, 12 + i, TMP, 12 + i))
    p += _pwm_sum(TMP, [(16 + j, 9 + j) for j in range(K)])               # t_hat^T o y_hat
    p.append(_op(OP_INTT, TMP))
    p.append(_op(OP_ADD, 19, TMP, 19))
    p.append(_op(OP_ADD, 19, 19, 20))
    return p


def _decrypt():
    p = [_op(OP_NTT, 12 + j) for j in range(K)]
    p += _pwm_sum(TMP, [(9 + j, 12 + j) for j in range(K)])               # s_hat^T o u_hat
    p.append(_op(OP_INTT, TMP))
    p.append(_op(OP_SUB, 19, 19, TMP))
    return p


PROGRAMS = {"keygen": _keygen(), "encrypt": _encrypt(), "decrypt": _decrypt()}
PROG_ID = {"keygen": 0, "encrypt": 1, "decrypt": 2}


def run(program, slots):
    """Runs a program on a dict / list of slots (modified in place). Returns the op counts."""
    counts = {"NTT": 0, "INTT": 0, "PWM": 0, "ADD": 0, "SUB": 0}
    acc = [0] * N
    for opc, d, a, b, first, last in program:
        counts[OPNAME[opc]] += 1
        if opc == OP_NTT:
            slots[d] = ntt(slots[d])
        elif opc == OP_INTT:
            slots[d] = intt(slots[d])
        elif opc == OP_PWM:
            prod = multiply_ntts(slots[a], slots[b])
            acc = [((0 if first else x) + y) % Q for x, y in zip(acc, prod)]
            if last:
                slots[d] = list(acc)
        elif opc == OP_ADD:
            slots[d] = [(x + y) % Q for x, y in zip(slots[a], slots[b])]
        elif opc == OP_SUB:
            slots[d] = [(x - y) % Q for x, y in zip(slots[a], slots[b])]
    return counts


def _matrix(rho):
    return {3 * i + j: sample_ntt(rho + bytes([j]) + bytes([i])) for i in range(K) for j in range(K)}


def keygen_inputs(d: bytes):
    """Slots before the KeyGen program (Alg. 13 lines 1-15)."""
    rho, sigma = G(d + bytes([K]))
    slots = [[0] * N for _ in range(NPOLY)]
    for s, p in _matrix(rho).items():
        slots[s] = p
    for j in range(K):
        slots[9 + j] = sample_poly_cbd(ETA1, PRF(ETA1, sigma, j))
    for j in range(K):
        slots[12 + j] = sample_poly_cbd(ETA1, PRF(ETA1, sigma, K + j))
    return slots, rho


def encrypt_inputs(ek_pke: bytes, m: bytes, r: bytes):
    """Slots before the Encrypt program (Alg. 14 lines 2-17 and the decompressed message of line 20)."""
    slots = [[0] * N for _ in range(NPOLY)]
    for j in range(K):
        slots[16 + j] = byte_decode(12, ek_pke[384 * j: 384 * (j + 1)])
    for s, p in _matrix(ek_pke[384 * K: 384 * K + 32]).items():
        slots[s] = p
    ctr = 0
    for j in range(K):
        slots[9 + j] = sample_poly_cbd(ETA1, PRF(ETA1, r, ctr))
        ctr += 1
    for j in range(K):
        slots[12 + j] = sample_poly_cbd(ETA2, PRF(ETA2, r, ctr))
        ctr += 1
    slots[19] = sample_poly_cbd(ETA2, PRF(ETA2, r, ctr))
    slots[20] = decompress(1, byte_decode(1, m))
    return slots


def decrypt_inputs(dk_pke: bytes, c: bytes):
    """Slots before the Decrypt program (Alg. 15 lines 1-5)."""
    slots = [[0] * N for _ in range(NPOLY)]
    c1, c2 = c[: 32 * DU * K], c[32 * DU * K: 32 * (DU * K + DV)]
    for j in range(K):
        slots[12 + j] = decompress(DU, byte_decode(DU, c1[32 * DU * j: 32 * DU * (j + 1)]))
    slots[19] = decompress(DV, byte_decode(DV, c2))
    for j in range(K):
        slots[9 + j] = byte_decode(12, dk_pke[384 * j: 384 * (j + 1)])
    return slots


assert Q == 3329 and N == 256
