"""tb/golden/kpke_smp_model.py

Phases 8c and 8d (evidence/phase08/8c/test_plan_8c.md): the Phase 6 K-PKE programs (tb/golden/kpke_sched_model.py, unmodified) extended with the sampling of the matrix and of the noise polynomials,
run with the golden primitives. The same program lists are turned into the RTL program ROM by scripts/build/gen_kpke_smp_roms.py.

Operations added to the Phase 6 list (one polynomial = 256 coefficients in [0, q)):
  SMPN d ctr     slot d <- SamplePolyCBD_2(PRF(seed, ctr))                       (FIPS 203 Algorithm 8; first = 1: non-blocking in the variant OVERLAP)
  SMPA d m       slot d <- SampleNTT(rho || j || i), m = 3i + j                  (Algorithm 7; the matrix entry A_hat[i][j])
  PWMS d m b F L like PWM d a b F L, but operand a is the sampler stream of A_hat[i][j] (m = 3i + j) instead of slot a: A_hat is never stored
  WAIT           wait until the sampler is idle                                  (variant OVERLAP only)
Variants: STORE (0): the nine entries are sampled into the slots 0-8 and the Phase 6 PWM ops are used; slot numbers as in Phase 6 (24 slots). STREAM (1): PWMS; the matrix slots do not exist, so the Phase 6 slots 9-20
are renumbered 0-11 (12 slots). OVERLAP (2): STREAM with non-blocking noise sampling overlapped with the transforms (8d). STRESS (3, test only): OVERLAP with one noise sample started right before an ADD pass so that sampler beats and sequencer writes collide (arbitration test). The *logical* slot numbers (Phase 6) are used by the tests; `phys` maps them to the hardware slots.
Seeds: `rho` (32 bytes, matrix) and `sd` (32 bytes: sigma in KeyGen, r in Encrypt, noise).
"""
from __future__ import annotations

from kpke_sched_model import (NPOLY as NPOLY_P6, OP_ADD, OP_END, OP_INTT, OP_NTT, OP_PWM, OP_SUB, PROGRAMS as P6, TMP, _matrix, _op, decrypt_inputs, encrypt_inputs, keygen_inputs)  # noqa: F401
from params import ETA1, ETA2, K, N, Q
from primitives import PRF, intt, multiply_ntts, ntt, sample_ntt, sample_poly_cbd

OP_SMPN, OP_SMPA, OP_PWMS, OP_WAIT = 6, 7, 8, 9
OPNAME = {OP_NTT: "NTT", OP_INTT: "INTT", OP_PWM: "PWM", OP_ADD: "ADD", OP_SUB: "SUB", OP_SMPN: "SMPN", OP_SMPA: "SMPA", OP_PWMS: "PWMS", OP_WAIT: "WAIT"}
STORE, STREAM, OVERLAP, STRESS = 0, 1, 2, 3
VARIANTS = {"store": STORE, "stream": STREAM, "overlap": OVERLAP, "stress": STRESS}
PROG_ID = {"keygen": 0, "encrypt": 1, "decrypt": 2}
NPOLY = {STORE: 24, STREAM: 12, OVERLAP: 12, STRESS: 12}   # slots of the hardware store per variant
FIRST_VEC = 9                                   # the first logical slot that exists in every variant (Phase 6: vectors start at slot 9)


def phys(variant: int, s: int) -> int:
    """Hardware slot of the logical (Phase 6) slot s."""
    if variant == STORE:
        return s
    assert s >= FIRST_VEC, "the matrix slots do not exist in STREAM / OVERLAP"
    return s - FIRST_VEC


def msg_ji(m: int) -> tuple[int, int]:
    """Bytes (j, i) appended to rho for the matrix entry m = 3i + j (A_hat[i][j] = SampleNTT(rho || j || i))."""
    return m % K, m // K


def _noise_prefix(name: str, nonblocking: bool = False):
    """SMPN operations of a program: slot, counter. KeyGen: s (9-11, ctr 0-2) and e (12-14, ctr 3-5); Encrypt: y, e1 likewise and e2 (19, ctr 6); Decrypt: none."""
    if name == "decrypt":
        return []
    ops = [(9 + j, j) for j in range(K)] + [(12 + j, K + j) for j in range(K)]
    if name == "encrypt":
        ops.append((19, 2 * K))
    return [_op(OP_SMPN, d, 0, ctr, int(nonblocking), 0) for d, ctr in ops]


def _renumber(op, variant):
    opc, d, a, b, first, last = op
    if variant == STORE:
        return op
    if opc == OP_PWM and a < 9:   # matrix operand: streamed, a becomes the matrix index (unchanged number)
        return (OP_PWMS, phys(variant, d), a, phys(variant, b), first, last)
    if opc in (OP_NTT, OP_INTT):
        return (opc, phys(variant, d), 0, 0, first, last)
    return (opc, phys(variant, d), phys(variant, a), phys(variant, b), first, last)


def programs(variant: int) -> dict:
    """The programs of one variant, in hardware slot numbers."""
    out = {}
    for name in PROG_ID:
        base = P6[name]
        if variant == STORE:
            pre = []
            if name != "decrypt":
                pre = [_op(OP_SMPA, m, m, 0, 0, 0) for m in range(K * K)] + _noise_prefix(name)
            out[name] = pre + list(base)
        elif variant == STREAM:
            pre = [(opc, phys(variant, d), a, b, f, l) for opc, d, a, b, f, l in _noise_prefix(name)]
            out[name] = pre + [_renumber(op, variant) for op in base]
        elif variant == OVERLAP:
            out[name] = _overlap(name, stress=False)
        else:
            out[name] = _overlap(name, stress=True)
    return out


def _to_phys(ops, variant):
    out = []
    for opc, d, a, b, first, last in ops:
        if opc == OP_WAIT:
            out.append((opc, 0, 0, 0, 0, 0))
        elif opc == OP_SMPN:
            out.append((opc, phys(variant, d), a, b, first, last))
        elif opc == OP_PWMS:
            out.append((opc, phys(variant, d), a, phys(variant, b), first, last))
        else:
            out.append(_renumber((opc, d, a, b, first, last), variant))
    return out


def _stream_tail(name):
    """The Phase 6 arithmetic of a program in logical slots with the matrix operands as PWMS."""
    return [(OP_PWMS, d, a, b, f, l) if (opc == OP_PWM and a < 9) else (opc, d, a, b, f, l) for opc, d, a, b, f, l in P6[name]]


def _overlap(name, stress):
    """Programs of the variants OVERLAP and STRESS in hardware slot numbers (the logical program is built first)."""
    smpn = lambda d, ctr, nb: (OP_SMPN, d, 0, ctr, int(nb), 0)  # noqa: E731
    wait = (OP_WAIT, 0, 0, 0, 0, 0)
    tail = _stream_tail(name)
    if name == "decrypt":
        return _to_phys(tail, OVERLAP)
    if name == "keygen":
        slots = [9, 10, 11, 12, 13, 14]
        ops = [smpn(slots[0], 0, False)]
        for k in range(6):
            if k < 5:
                ops.append(smpn(slots[k + 1], k + 1, True))
            ops.append((OP_NTT, slots[k], 0, 0, 0, 0))
            if k < 5:
                ops.append(wait)
        return _to_phys(ops + tail[6:], OVERLAP)
    # encrypt: tail = NTT 9, 10, 11, then three blocks of five operations (PWMS x3, INTT 15, ADD 12 + i), then PWMS x3 (t_hat), INTT 15, ADD 19, ADD 19
    ntt, rest = tail[:3], tail[3:]
    blocks = [rest[5 * i: 5 * i + 5] for i in range(3)]
    fin = rest[15:]
    if stress:
        ops = [smpn(9, 0, False), smpn(10, 1, False), smpn(11, 2, False), smpn(12, 3, False), smpn(13, 4, False), smpn(19, 6, False)] + ntt
        for i in range(3):
            ops += blocks[i][:4]                      # PWMS x3, INTT 15
            if i == 0:
                ops.append(smpn(14, 5, True))         # collides with the ADD pass below
            if i == 2:
                ops.append(wait)
            ops.append(blocks[i][4])                  # ADD 12 + i
        return _to_phys(ops + fin, OVERLAP)
    ops = [smpn(9, 0, False), smpn(10, 1, True), ntt[0], wait, smpn(11, 2, True), ntt[1], wait, smpn(12, 3, True), ntt[2], wait]
    extra = {0: smpn(13, 4, True), 1: smpn(14, 5, True), 2: smpn(19, 6, True)}
    for i in range(3):
        ops += blocks[i][:3] + [extra[i]] + [blocks[i][3], wait, blocks[i][4]]
    return _to_phys(ops + fin, OVERLAP)


def check_hazards(program) -> list:
    """Static data-flow check of a program with non-blocking SMPN: returns the list of (pc, slot) where an operation reads or writes a slot while a non-blocking sample of it may still be running.
    A WAIT, a PWMS, a PWM... no: only WAIT, PWMS and any sampling operation (they wait for an idle sampler) end the pending state."""
    pending, bad = set(), []
    for pc, (opc, d, a, b, first, last) in enumerate(program):
        if opc == OP_WAIT or opc in (OP_PWMS, OP_SMPA) or (opc == OP_SMPN and not first):
            pending.clear()
        if opc == OP_SMPN:
            if first:
                pending = {d}
            continue
        reads = {OP_NTT: {d}, OP_INTT: {d}, OP_PWM: {a, b}, OP_PWMS: {b}, OP_ADD: {a, b}, OP_SUB: {a, b}}.get(opc, set())
        writes = {d} if opc in (OP_NTT, OP_INTT, OP_ADD, OP_SUB) or (opc == OP_PWM and last) else set()
        for sl in (reads | writes) & pending:
            bad.append((pc, sl))
    return bad


def run(program, slots, rho: bytes, sd: bytes):
    """Runs a program on a list of hardware slots (modified in place). Returns the op counts (SMP counts SMPN and SMPA, PWM counts PWM and PWMS)."""
    counts = {"NTT": 0, "INTT": 0, "PWM": 0, "ADD": 0, "SUB": 0, "SMP": 0}
    acc = [0] * N
    for opc, d, a, b, first, last in program:
        if opc == OP_WAIT:
            continue
        counts[{OP_PWMS: "PWM", OP_SMPN: "SMP", OP_SMPA: "SMP"}.get(opc, OPNAME[opc])] += 1
        if opc == OP_NTT:
            slots[d] = ntt(slots[d])
        elif opc == OP_INTT:
            slots[d] = intt(slots[d])
        elif opc in (OP_PWM, OP_PWMS):
            if opc == OP_PWMS:
                j, i = msg_ji(a)
                av = sample_ntt(rho + bytes([j]) + bytes([i]))
            else:
                av = slots[a]
            prod = multiply_ntts(av, slots[b])
            acc = [((0 if first else x) + y) % Q for x, y in zip(acc, prod)]
            if last:
                slots[d] = list(acc)
        elif opc == OP_ADD:
            slots[d] = [(x + y) % Q for x, y in zip(slots[a], slots[b])]
        elif opc == OP_SUB:
            slots[d] = [(x - y) % Q for x, y in zip(slots[a], slots[b])]
        elif opc == OP_SMPN:
            eta = ETA1 if b < K else ETA2
            slots[d] = sample_poly_cbd(eta, PRF(eta, sd, b))
        elif opc == OP_SMPA:
            j, i = msg_ji(a)
            slots[d] = sample_ntt(rho + bytes([j]) + bytes([i]))
    return counts


def empty_slots(variant: int):
    return [[0] * N for _ in range(NPOLY[variant])]


def inputs(variant: int, name: str, ek_pke: bytes | None = None, m: bytes | None = None, r: bytes | None = None, dk_pke: bytes | None = None, c: bytes | None = None, d: bytes | None = None):
    """(hardware slots before the program, rho, sd). Only data the testbench writes in the hardware are present: KeyGen none; Encrypt t_hat (16-18) and the decompressed message (20); Decrypt the Phase 6 inputs."""
    slots = empty_slots(variant)
    rho = sd = bytes(32)
    if name == "keygen":
        from primitives import G
        rho, sd = G(d + bytes([K]))
    elif name == "encrypt":
        ref = encrypt_inputs(ek_pke, m, r)
        for s in (16, 17, 18, 20):
            slots[phys(variant, s)] = ref[s]
        rho, sd = ek_pke[384 * K: 384 * K + 32], r
    else:
        ref = decrypt_inputs(dk_pke, c)
        for s in (9, 10, 11, 12, 13, 14, 19):
            slots[phys(variant, s)] = ref[s]
    return slots, rho, sd


def logical(variant: int, slots, s: int):
    return slots[phys(variant, s)]


assert Q == 3329 and N == 256
