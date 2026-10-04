"""tb/mlkem/test_mlkem_fo_cmp.py -- Phase 9b tests V5, V6 (compare), V10 of rtl/mlkem/mlkem_fo_cmp.sv against the hardware-form model tb/golden/fo_model.py (checked against the unmodified golden Decaps in V2)."""
import json
import os
import random

import cocotb
from hashfo_tb import MODES, WORDS, clock_reset, fo_run, idle  # sets sys.path to tb/golden

import fo_model as F

NB = 8 * WORDS


def rb(rng, n):
    return bytes(rng.randrange(256) for _ in range(n))


def check(r, a, b, kg, kb, what):
    neq = F.ct_differs(a, b)
    exp = F.fo_select(a, b, kg.to_bytes(32, "little"), kb.to_bytes(32, "little"))
    assert r["done"] == 1, f"{what}: done_o pulsed {r['done']} times"
    assert r["taken"] == WORDS, f"{what}: {r['taken']} beats accepted, expected {WORDS}"
    assert r["neq"] == neq, f"{what}: neq_o = {r['neq']}, expected {neq}"
    assert r["k"].to_bytes(32, "little") == exp, f"{what}: selected key differs from the model"


def flip(b: bytes, bit: int) -> bytes:
    d = bytearray(b)
    d[bit // 8] ^= 1 << (bit % 8)
    return bytes(d)


@cocotb.test()
async def test_equal_and_random_pairs_with_gaps(dut):
    """V5: equal pairs, random different pairs, every input-gap mode, random keys."""
    await clock_reset(dut)
    rng = random.Random(960)
    for k in range(30):
        a = rb(rng, NB)
        b = a if k % 2 == 0 else rb(rng, NB)
        kg, kb = rng.getrandbits(256), rng.getrandbits(256)
        src = MODES[k % 3]
        check(await fo_run(dut, a, b, kg, kb, rng, src=src), a, b, kg, kb, f"pair {k} src={src}")


@cocotb.test()
async def test_every_single_bit_difference(dut):
    """V5: c' differs from c in exactly one bit: every one of the WORDS * 64 positions gives neq = 1 and K_bar."""
    await clock_reset(dut)
    rng = random.Random(961)
    a = rb(rng, NB)
    for bit in range(8 * NB):
        kg, kb = rng.getrandbits(256), rng.getrandbits(256)
        check(await fo_run(dut, a, flip(a, bit), kg, kb, rng), a, flip(a, bit), kg, kb, f"bit {bit}")


@cocotb.test()
async def test_first_last_all_beats_and_special_keys(dut):
    """V5: differences in the first beat only, the last beat only and in every beat; keys all-zero, all-one and bitwise complements."""
    await clock_reset(dut)
    rng = random.Random(962)
    a = rb(rng, NB)
    cases = {
        "first": bytes([a[0] ^ 0xFF]) + a[1:],
        "last": a[:-1] + bytes([a[-1] ^ 0x01]),
        "all": bytes(x ^ 0xFF for x in a),
        "equal": a,
    }
    keys = [(0, (1 << 256) - 1), ((1 << 256) - 1, 0), (0x5555 << 240 | 0x1234, ((1 << 256) - 1) ^ (0x5555 << 240 | 0x1234)), (0, 0)]
    for name, b in cases.items():
        for kg, kb in keys:
            check(await fo_run(dut, a, b, kg, kb, rng), a, b, kg, kb, f"{name} keys {kg:x}/{kb:x}")


@cocotb.test()
async def test_start_while_busy_ignored_reset_and_hold(dut):
    """V5: a start while busy is ignored; reset in the middle then a clean run; neq_o and k_o are held after done_o while the inputs change."""
    await clock_reset(dut)
    rng = random.Random(963)
    a = rb(rng, NB)
    b = flip(a, 77)
    kg, kb = rng.getrandbits(256), rng.getrandbits(256)
    check(await fo_run(dut, a, b, kg, kb, rng, src="rand", start_noise=True), a, b, kg, kb, "start noise")
    await idle(dut)
    dut.f_start_i.value = 1
    await idle(dut, 1)
    dut.f_start_i.value = 0
    for i in range(40):
        dut.f_in_valid_i.value = 1
        dut.f_a_data_i.value = rng.getrandbits(64)
        dut.f_b_data_i.value = rng.getrandbits(64)
        await idle(dut, 1)
    dut.rst_ni.value = 0
    await idle(dut, 2)
    dut.rst_ni.value = 1
    dut.f_in_valid_i.value = 0
    await idle(dut, 2)
    assert int(dut.f_busy_o.value) == 0 and int(dut.f_in_ready_o.value) == 0, "not idle after reset"
    r = await fo_run(dut, a, a, kg, kb, rng)
    check(r, a, a, kg, kb, "after reset")
    held = (int(dut.f_neq_o.value), int(dut.f_k_o.value))
    for _ in range(30):
        dut.f_kgood_i.value = rng.getrandbits(256)
        dut.f_kbad_i.value = rng.getrandbits(256)
        dut.f_a_data_i.value = rng.getrandbits(64)
        dut.f_in_valid_i.value = 1
        await idle(dut, 1)
        assert (int(dut.f_neq_o.value), int(dut.f_k_o.value)) == held, "result changed after done_o"
    dut.f_in_valid_i.value = 0


@cocotb.test()
async def test_constant_cycles_and_cycle_table(dut):
    """V6 and V10: the cycle count is the same for equal inputs, any single-bit difference (first, middle, last beat), many differences, and any data and keys."""
    await clock_reset(dut)
    rng = random.Random(964)
    cyc = set()
    for k in range(60):
        a = rb(rng, NB)
        if k % 6 == 0:
            b = a
        elif k % 6 == 1:
            b = flip(a, 0)
        elif k % 6 == 2:
            b = flip(a, 8 * NB - 1)
        elif k % 6 == 3:
            b = flip(a, rng.randrange(8 * NB))
        elif k % 6 == 4:
            b = rb(rng, NB)
        else:
            b = bytes(x ^ 0xFF for x in a)
        kg, kb = rng.getrandbits(256), rng.getrandbits(256)
        r = await fo_run(dut, a, b, kg, kb, rng)
        check(r, a, b, kg, kb, f"cycles k={k}")
        cyc.add(r["cycles"])
    assert len(cyc) == 1, f"cycle counts {sorted(cyc)} depend on the data"
    n = cyc.pop()
    dut._log.info(f"compare cycles (no gaps), WORDS={WORDS}: {n}")
    out = os.environ.get("HF_CYCLES_OUT")
    if out:
        with open(out, "w") as f:
            json.dump({"fo_cycles": n, "words": WORDS}, f)
