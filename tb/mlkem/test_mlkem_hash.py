"""tb/mlkem/test_mlkem_hash.py -- Phase 9b tests V3, V4, V6 (hash), V10 of rtl/mlkem/mlkem_hash.sv against the unmodified golden primitives H, G, J (hashlib)."""
import json
import os
import random

import cocotb
from hashfo_tb import G, H, J, MODES, clock_reset, digest_bytes, hash_run, idle
from primitives import G as gold_g, H as gold_h, J as gold_j

NWORDS = {H: 4, G: 8, J: 4}
CORE_R2 = int(os.environ.get("HF_CORE_R2", "1"))


def golden(sel, msg) -> bytes:
    if sel == H:
        return gold_h(msg)
    if sel == G:
        a, b = gold_g(msg)
        return a + b
    return gold_j(msg)


def check(r, sel, msg, what):
    exp = golden(sel, msg)
    assert r["done"] == 1, f"{what}: done_o pulsed {r['done']} times"
    assert len(r["words"]) == NWORDS[sel], f"{what}: {len(r['words'])} digest words"
    assert r["last_at"] == [NWORDS[sel] - 1], f"{what}: out_last_o on words {r['last_at']}"
    assert r["taken"] == (len(msg) + 7) // 8, f"{what}: {r['taken']} message words taken, expected {(len(msg) + 7) // 8}"
    got = digest_bytes(r["words"])
    assert got == exp, f"{what}: digest differs from the golden at byte {next(i for i in range(len(exp)) if got[i] != exp[i])}"


def rmsg(rng, n):
    return bytes(rng.randrange(256) for _ in range(n))


REQUIRED = [(G, 33), (G, 64), (H, 1184), (J, 1120)]
BOUNDARY = [0, 1, 7, 8, 9, 71, 72, 73, 135, 136, 137, 143, 144, 271, 272, 273]


@cocotb.test()
async def test_required_lengths_all_modes(dut):
    """V3: the four hash operations of Algorithms 16-18 with their lengths, every back-pressure mode pair."""
    await clock_reset(dut)
    rng = random.Random(950)
    for sel, n in REQUIRED:
        for src in MODES:
            for sink in MODES:
                msg = rmsg(rng, n)
                check(await hash_run(dut, sel, msg, rng, src=src, sink=sink), sel, msg, f"sel={sel} len={n} src={src} sink={sink}")


@cocotb.test()
async def test_boundary_and_random_lengths(dut):
    """V3: message lengths at the rate boundaries of every mode and random lengths up to 300, garbage in the unused bytes of the last word."""
    await clock_reset(dut)
    rng = random.Random(951)
    lens = BOUNDARY + [rng.randrange(0, 301) for _ in range(20)]
    for sel in (H, G, J):
        for n in lens:
            msg = rmsg(rng, n)
            check(await hash_run(dut, sel, msg, rng, src=rng.choice(MODES), sink=rng.choice(MODES)), sel, msg, f"sel={sel} len={n}")


@cocotb.test()
async def test_start_sel_len_while_busy_ignored(dut):
    """V4: a start with another sel and len while busy is ignored."""
    await clock_reset(dut)
    rng = random.Random(952)
    for sel, n in REQUIRED:
        msg = rmsg(rng, n)
        check(await hash_run(dut, sel, msg, rng, src="rand", sink="rand", start_noise=True), sel, msg, f"noise sel={sel} len={n}")


@cocotb.test()
async def test_reset_in_the_middle_then_clean_run(dut):
    """V4: reset in the middle of a run, then a clean run; the wrapper is idle after the reset."""
    await clock_reset(dut)
    rng = random.Random(953)
    for sel, n in ((J, 1120), (G, 64), (H, 300)):
        msg = rmsg(rng, n)
        await idle(dut)
        dut.h_start_i.value = 1
        dut.h_sel_i.value = sel
        dut.h_len_i.value = n
        await idle(dut, 1)
        dut.h_start_i.value = 0
        for i in range(25):
            dut.h_in_valid_i.value = 1
            dut.h_in_data_i.value = rng.getrandbits(64)
            dut.h_out_ready_i.value = 0
            await idle(dut, 1)
        dut.rst_ni.value = 0
        await idle(dut, 2)
        dut.rst_ni.value = 1
        dut.h_in_valid_i.value = 0
        await idle(dut, 2)
        assert int(dut.h_busy_o.value) == 0 and int(dut.h_out_valid_o.value) == 0 and int(dut.h_in_ready_o.value) == 0, "not idle after reset"
        check(await hash_run(dut, sel, msg, rng), sel, msg, f"after reset sel={sel} len={n}")


@cocotb.test()
async def test_j_then_h_then_g_in_a_row(dut):
    """V4: J (SHAKE256, stopped after 4 words), then H and G at once: no state is left in the sponge."""
    await clock_reset(dut)
    rng = random.Random(954)
    for _ in range(10):
        for sel, n in ((J, 1120), (H, 1184), (G, 64), (J, 33), (G, 33)):
            msg = rmsg(rng, n)
            check(await hash_run(dut, sel, msg, rng, sink=rng.choice(MODES)), sel, msg, f"row sel={sel} len={n}")


@cocotb.test()
async def test_constant_cycles_and_cycle_table(dut):
    """V6 and V10: the cycle count of a run with always-ready sink and no input gaps is the same for every data value of one (sel, len); the table is written."""
    await clock_reset(dut)
    rng = random.Random(955)
    table = {}
    for sel, n in REQUIRED:
        cyc = set()
        for k in range(40):
            msg = (bytes([[0, 255, 0xAA, 0x55][k]]) * n) if k < 4 else rmsg(rng, n)
            r = await hash_run(dut, sel, msg, rng)
            check(r, sel, msg, f"cycles sel={sel} len={n} k={k}")
            cyc.add(r["cycles"])
        assert len(cyc) == 1, f"sel={sel} len={n}: cycle counts {sorted(cyc)} depend on the data"
        table[f"{'HGJ'[sel]}_{n}"] = cyc.pop()
    dut._log.info(f"hash cycles (always-ready sink, no gaps), CORE_R2={CORE_R2}: {table}")
    out = os.environ.get("HF_CYCLES_OUT")
    if out:
        with open(out, "w") as f:
            json.dump({"hash_cycles": table, "core_r2": CORE_R2}, f)
