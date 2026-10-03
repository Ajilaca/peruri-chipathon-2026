"""tb/sample/test_cbd2_core.py -- test plan 8b V4 (and V7 for the CBD core): rtl/sample/cbd2_core.sv against tb/golden/sampler_model.py (cbd2).
Nibble table, special streams, 500 random streams, exactly 16 words taken, back-pressure, abort and reset with the zeroisation probe.
Environment: KS_N (cases, default 500), KS_OUTW (output width, default 1)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import random

import cocotb
import sampler_model as M
from cocotb.triggers import FallingEdge, Timer
from sample_tb import LIMIT, NCASES, Monitor, Ready, check_poly, clock_reset

INIT = dict(start_i=0, abort_i=0, in_valid_i=0, in_data_i=0, coef_ready_i=0)


def stream_words(b):
    return [int.from_bytes(b[8 * i: 8 * i + 8], "little") for i in range(16)]


async def run(dut, b, rng, ready="always", gap=0.0):
    """One polynomial from the 128 bytes b; a 17th word is offered and must not be taken. Returns (monitor, cycles)."""
    words = stream_words(b) + [rng.getrandbits(64), rng.getrandbits(64)]
    exp = M.cbd2(b)
    await FallingEdge(dut.clk_i)
    dut.start_i.value, dut.abort_i.value, dut.in_valid_i.value = 1, 0, 0
    await FallingEdge(dut.clk_i)
    dut.start_i.value = 0
    mon, rdy, wi, cycles, tail = Monitor(), Ready(ready, rng), 0, 0, 0
    while True:
        cycles += 1
        assert cycles < LIMIT, "cbd2_core did not finish"
        go_in = wi < len(words) and rng.random() >= gap
        dut.in_valid_i.value = int(go_in)
        dut.in_data_i.value = words[wi] if wi < len(words) else 0
        go_out = rdy()
        dut.coef_ready_i.value = go_out
        await Timer(1, "ns")
        if go_in and int(dut.in_ready_o.value):
            wi += 1
        mon.sample(dut, go_out)
        if mon.done:
            tail += 1
            assert int(dut.busy_o.value) == 0
            if tail == 4:
                break
        await FallingEdge(dut.clk_i)
    check_poly(mon, exp, "CBD core")
    assert wi == 16, f"{wi} words taken, expected 16"
    assert int(dut.bytes_o.value) == 128
    return mon, cycles


def nibble_table_stream():
    """16 words in which word w holds nibble value (w + j) mod 16 at nibble position j: every value at every position."""
    out = b""
    for w in range(16):
        v = 0
        for j in range(16):
            v |= ((w + j) % 16) << (4 * j)
        out += v.to_bytes(8, "little")
    return out


@cocotb.test()
async def test_nibble_table_and_special_streams(dut):
    await clock_reset(dut, INIT)
    rng = random.Random(811)
    specials = {"nibble table": nibble_table_stream(), "all zero": bytes(128), "all ones": b"\xff" * 128, "0x55": b"\x55" * 128, "0xAA": b"\xaa" * 128}
    for k in range(128):
        specials[f"one hot byte {k}"] = bytes(k) + b"\x0f" + bytes(127 - k)
    for name, b in specials.items():
        for ready, gap in (("always", 0.0), ("rand", 0.3)):
            await run(dut, b, rng, ready, gap)
    table = sorted({M.cbd2(bytes([n | (n << 4)] * 128))[0] for n in range(16)})
    assert table == [0, 1, 2, 3327, 3328], table
    dut._log.info(f"{len(specials)} special streams equal to the golden; the 16 nibble values give only {table}")


@cocotb.test()
async def test_random_streams(dut):
    await clock_reset(dut, INIT)
    rng = random.Random(812)
    for i in range(NCASES):
        b = bytes(rng.randrange(256) for _ in range(128))
        await run(dut, b, rng, ready=("always", "rand", "runs")[i % 3], gap=(0.0, 0.2, 0.5)[(i // 3) % 3])
    dut._log.info(f"{NCASES} random streams equal to the golden; exactly 16 words taken each time")


@cocotb.test()
async def test_cycles_independent_of_data(dut):
    await clock_reset(dut, INIT)
    rng = random.Random(813)
    counts = set()
    for b in [bytes(128), b"\xff" * 128, nibble_table_stream()] + [bytes(rng.randrange(256) for _ in range(128)) for _ in range(40)]:
        _, c = await run(dut, b, rng)
        counts.add(c)
    assert len(counts) == 1, f"cycle counts differ: {sorted(counts)}"
    dut._log.info(f"cycles per polynomial with a stream word available every cycle: {counts.pop()}, the same for 43 inputs")


@cocotb.test()
async def test_abort_reset_zeroisation(dut):
    await clock_reset(dut, INIT)
    rng = random.Random(814)
    b = bytes(rng.randrange(256) for _ in range(128))
    probes = ("w_q", "wv_q", "nib_q", "od_q", "ov_q")

    def zero():
        return all(int(getattr(dut, p).value) == 0 for p in probes)

    await run(dut, b, rng)
    assert zero(), "state not cleared after done_o"
    for stop_at in (2, 9, 40, 200):
        words = stream_words(b)
        await FallingEdge(dut.clk_i)
        dut.start_i.value = 1
        await FallingEdge(dut.clk_i)
        dut.start_i.value = 0
        wi = 0
        for c in range(stop_at):
            go_in = wi < 16
            dut.in_valid_i.value, dut.in_data_i.value, dut.coef_ready_i.value = int(go_in), words[min(wi, 15)], int(c % 3 != 0)
            await Timer(1, "ns")
            if go_in and int(dut.in_ready_o.value):
                wi += 1
            await FallingEdge(dut.clk_i)
        dut.abort_i.value, dut.in_valid_i.value = 1, 0
        await FallingEdge(dut.clk_i)
        dut.abort_i.value = 0
        await Timer(1, "ns")
        assert int(dut.busy_o.value) == 0 and zero(), f"abort after {stop_at} cycles: busy or state not cleared"
        await run(dut, b, rng)
    words = stream_words(b)
    await FallingEdge(dut.clk_i)
    dut.start_i.value = 1
    await FallingEdge(dut.clk_i)
    dut.start_i.value = 0
    for c in range(12):
        dut.in_valid_i.value, dut.in_data_i.value, dut.coef_ready_i.value = 1, words[c], 0
        await FallingEdge(dut.clk_i)
    dut.rst_ni.value = 0
    await Timer(1, "ns")
    assert int(dut.busy_o.value) == 0 and zero(), "asynchronous reset did not clear the state"
    await FallingEdge(dut.clk_i)
    dut.rst_ni.value = 1
    dut.in_valid_i.value = 0
    await run(dut, b, rng)
    dut._log.info("abort at 4 points and reset in the middle clear the word and output registers; the core runs again")
