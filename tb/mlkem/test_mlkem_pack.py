"""tb/mlkem/test_mlkem_pack.py -- Phase 9a tests V3, V5 (compress side), V6, V7, V11 of rtl/mlkem/mlkem_pack.sv against the unmodified golden primitives."""
import json
import os
import random

import cocotb
from codec_tb import MODES, N, Q, clock_reset, idle, pack_run, special_polys
from primitives import byte_encode, compress


def golden(d, poly):
    return byte_encode(d, poly if d == 12 else compress(d, poly))


def check_run(r, d, poly, what):
    assert r["done"] == 1, f"{what}: done_o pulsed {r['done']} times"
    assert r["accepted"] == N, f"{what}: {r['accepted']} coefficients accepted"
    assert len(r["bytes"]) == 32 * d, f"{what}: {len(r['bytes'])} bytes"
    assert r["last_at"] == [32 * d - 1], f"{what}: byte_last_o at {r['last_at']}"
    assert r["bytes"] == golden(d, poly), f"{what}: bytes differ from the golden at byte {next(i for i in range(32 * d) if r['bytes'][i] != golden(d, poly)[i])}"


@cocotb.test()
async def test_random_and_special_all_d_all_modes(dut):
    """V3: random and special polynomials, all four d, every back-pressure and gap mode."""
    await clock_reset(dut)
    rng = random.Random(920)
    n = 0
    for name, poly in special_polys():
        for d in (1, 4, 10, 12):
            sink, src = rng.choice(MODES), rng.choice(MODES)
            r = await pack_run(dut, d, poly, rng, sink=sink, src=src)
            check_run(r, d, poly, f"{name} d={d} sink={sink} src={src}")
            n += 1
    dut._log.info(f"{n} pack runs equal to the golden")


@cocotb.test()
async def test_every_mode_pair(dut):
    """V3: every (sink, source) mode pair, one polynomial per d."""
    await clock_reset(dut)
    rng = random.Random(921)
    poly = [rng.randrange(Q) for _ in range(N)]
    for sink in MODES:
        for src in MODES:
            for d in (1, 4, 10, 12):
                check_run(await pack_run(dut, d, poly, rng, sink=sink, src=src), d, poly, f"d={d} sink={sink} src={src}")


@cocotb.test()
async def test_exhaustive_compress(dut):
    """V5: every x in [0, q-1] goes through the compress pipeline for d = 1, 4, 10 (13 polynomials of 256 values and one padded) and equals the golden."""
    await clock_reset(dut)
    rng = random.Random(922)
    vals = list(range(Q))
    vals += vals[: (-len(vals)) % N]
    polys = [vals[i: i + N] for i in range(0, len(vals), N)]
    assert len(polys) == 14
    for d in (1, 4, 10):
        for k, p in enumerate(polys):
            check_run(await pack_run(dut, d, p, rng), d, p, f"exhaustive d={d} poly {k}")
    # the same through d = 12 (unchanged)
    for k, p in enumerate(polys):
        check_run(await pack_run(dut, 12, p, rng), 12, p, f"exhaustive d=12 poly {k}")


@cocotb.test()
async def test_start_and_dsel_while_busy_ignored(dut):
    """V6: a start and a dsel change while busy are ignored."""
    await clock_reset(dut)
    rng = random.Random(923)
    for d in (1, 4, 10, 12):
        poly = [rng.randrange(Q) for _ in range(N)]
        check_run(await pack_run(dut, d, poly, rng, sink="rand", src="rand", start_noise=True), d, poly, f"noise d={d}")


@cocotb.test()
async def test_reset_in_the_middle_then_clean_run(dut):
    """V6: reset in the middle of a run, then a clean run, and nothing is output while idle."""
    await clock_reset(dut)
    rng = random.Random(924)
    poly = [rng.randrange(Q) for _ in range(N)]
    for d in (4, 12):
        await idle(dut)
        dut.p_start_i.value = 1
        dut.p_dsel_i.value = {4: 1, 12: 3}[d]
        await idle(dut, 1)
        dut.p_start_i.value = 0
        for i in range(40):
            dut.p_coef_valid_i.value = 1
            dut.p_coef_data_i.value = poly[i]
            dut.p_byte_ready_i.value = 1
            await idle(dut, 1)
        dut.rst_ni.value = 0
        await idle(dut, 2)
        dut.rst_ni.value = 1
        dut.p_coef_valid_i.value = 0
        await idle(dut, 2)
        assert int(dut.p_busy_o.value) == 0 and int(dut.p_byte_valid_o.value) == 0 and int(dut.p_coef_ready_o.value) == 0, "not idle after reset"
        check_run(await pack_run(dut, d, poly, rng), d, poly, f"after reset d={d}")


@cocotb.test()
async def test_constant_cycles_and_cycle_table(dut):
    """V7 and V11: the cycle count of a run with always-ready sink and no gaps is the same for every data value of one d; the table is written."""
    await clock_reset(dut)
    rng = random.Random(925)
    table = {}
    for d in (1, 4, 10, 12):
        cyc = set()
        for k, (name, poly) in enumerate(special_polys()):
            if k >= 100:
                break
            r = await pack_run(dut, d, poly, rng)
            check_run(r, d, poly, f"cycles {name} d={d}")
            cyc.add(r["cycles"])
        assert len(cyc) == 1, f"d={d}: cycle counts {sorted(cyc)} depend on the data"
        table[d] = cyc.pop()
    dut._log.info(f"pack cycles per polynomial (always-ready sink, no gaps): {table}")
    out = os.environ.get("CT_CYCLES_OUT")
    if out:
        with open(out, "w") as f:
            json.dump({"pack_cycles": table}, f)
