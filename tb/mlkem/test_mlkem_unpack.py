"""tb/mlkem/test_mlkem_unpack.py -- Phase 9a tests V4, V5 (decompress side and round trip), V6, V7, V11 of rtl/mlkem/mlkem_unpack.sv against the unmodified golden primitives."""
import json
import os
import random

import cocotb
from codec_tb import MODES, N, Q, clock_reset, idle, pack_run, special_polys, unpack_run
from primitives import byte_decode, byte_encode, compress, decompress


def golden(d, data):
    v = byte_decode(d, data)
    return v if d == 12 else decompress(d, v)


def check_run(r, d, data, what):
    exp = golden(d, data)
    assert r["done"] == 1, f"{what}: done_o pulsed {r['done']} times"
    assert r["accepted"] == 32 * d, f"{what}: {r['accepted']} bytes accepted"
    assert len(r["coefs"]) == N, f"{what}: {len(r['coefs'])} coefficients"
    assert r["last_at"] == [N - 1], f"{what}: coef_last_o at {r['last_at']}"
    assert r["coefs"] == exp, f"{what}: coefficients differ from the golden at index {next(i for i in range(N) if r['coefs'][i] != exp[i])}"


def rand_bytes(rng, d):
    return bytes(rng.randrange(256) for _ in range(32 * d))


@cocotb.test()
async def test_random_all_d_all_modes(dut):
    """V4: random byte strings, all four d, every back-pressure and gap mode (d = 12 includes values >= q: reduction)."""
    await clock_reset(dut)
    rng = random.Random(930)
    n = 0
    for k in range(4 * int(os.environ.get("CT_N", "40"))):
        for d in (1, 4, 10, 12):
            data = rand_bytes(rng, d)
            sink, src = rng.choice(MODES), rng.choice(MODES)
            check_run(await unpack_run(dut, d, data, rng, sink=sink, src=src), d, data, f"rand{k} d={d} sink={sink} src={src}")
            n += 1
    dut._log.info(f"{n} unpack runs equal to the golden")


@cocotb.test()
async def test_every_mode_pair(dut):
    await clock_reset(dut)
    rng = random.Random(931)
    for sink in MODES:
        for src in MODES:
            for d in (1, 4, 10, 12):
                data = rand_bytes(rng, d)
                check_run(await unpack_run(dut, d, data, rng, sink=sink, src=src), d, data, f"d={d} sink={sink} src={src}")


@cocotb.test()
async def test_exhaustive_decompress_and_all_12_bit_values(dut):
    """V5: every input of decompress (all 2^d values for d = 1, 4, 10) and every 12-bit value (0..4095, reduced mod q) through the RTL."""
    await clock_reset(dut)
    rng = random.Random(932)
    for d, top in ((1, 2), (4, 16), (10, 1024), (12, 4096)):
        vals = list(range(top))
        vals += [rng.randrange(top) for _ in range((-len(vals)) % N)]
        for i in range(0, len(vals), N):
            data = byte_encode(d, vals[i: i + N])
            check_run(await unpack_run(dut, d, data, rng), d, data, f"exhaustive d={d} block {i // N}")


@cocotb.test()
async def test_roundtrip_through_both_modules(dut):
    """V5: pack then unpack through the RTL equals the golden round trip (decompress of compress; identity for d = 12)."""
    await clock_reset(dut)
    rng = random.Random(933)
    for k, (name, poly) in enumerate(special_polys()):
        if k >= 30:
            break
        for d in (1, 4, 10, 12):
            p = await pack_run(dut, d, poly, rng, sink="rand", src="rand")
            u = await unpack_run(dut, d, p["bytes"], rng, sink="rand", src="rand")
            exp = poly if d == 12 else decompress(d, compress(d, poly))
            assert u["coefs"] == exp, f"round trip {name} d={d}"


@cocotb.test()
async def test_start_and_dsel_while_busy_ignored(dut):
    await clock_reset(dut)
    rng = random.Random(934)
    for d in (1, 4, 10, 12):
        data = rand_bytes(rng, d)
        check_run(await unpack_run(dut, d, data, rng, sink="rand", src="rand", start_noise=True), d, data, f"noise d={d}")


@cocotb.test()
async def test_reset_in_the_middle_then_clean_run(dut):
    await clock_reset(dut)
    rng = random.Random(935)
    for d in (4, 12):
        data = rand_bytes(rng, d)
        await idle(dut)
        dut.u_start_i.value = 1
        dut.u_dsel_i.value = {4: 1, 12: 3}[d]
        await idle(dut, 1)
        dut.u_start_i.value = 0
        for i in range(30):
            dut.u_byte_valid_i.value = 1
            dut.u_byte_data_i.value = data[i]
            dut.u_coef_ready_i.value = 0
            await idle(dut, 1)
        dut.rst_ni.value = 0
        await idle(dut, 2)
        dut.rst_ni.value = 1
        dut.u_byte_valid_i.value = 0
        await idle(dut, 2)
        assert int(dut.u_busy_o.value) == 0 and int(dut.u_coef_valid_o.value) == 0 and int(dut.u_byte_ready_o.value) == 0, "not idle after reset"
        check_run(await unpack_run(dut, d, data, rng), d, data, f"after reset d={d}")


@cocotb.test()
async def test_constant_cycles_and_cycle_table(dut):
    """V7 and V11: identical cycles for every data value of one d (always-ready sink, no gaps); the table is written."""
    await clock_reset(dut)
    rng = random.Random(936)
    table = {}
    for d in (1, 4, 10, 12):
        cyc = set()
        for k in range(100):
            data = rand_bytes(rng, d) if k >= 4 else bytes([[0, 255, 0xAA, 0x55][k]]) * (32 * d)
            r = await unpack_run(dut, d, data, rng)
            check_run(r, d, data, f"cycles k={k} d={d}")
            cyc.add(r["cycles"])
        assert len(cyc) == 1, f"d={d}: cycle counts {sorted(cyc)} depend on the data"
        table[d] = cyc.pop()
    dut._log.info(f"unpack cycles per polynomial (always-ready sink, no gaps): {table}")
    out = os.environ.get("CT_CYCLES_OUT")
    if out:
        with open(out, "w") as f:
            json.dump({"unpack_cycles": table}, f)
