"""tb/sample/test_sample_ntt_core.py -- test plan 8b V3 (and V7 for the SampleNTT core): rtl/sample/sample_ntt_core.sv against tb/golden/sampler_model.py.
Crafted streams (every case of plan section 2), 500 XOF streams, back-pressure runs and stream gaps, abort and reset with the zeroisation probe, start while busy.
Environment: KS_N (cases, default 500), KS_OUTW (output width, default 1)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import random

import cocotb
import sampler_model as M
from cocotb.triggers import FallingEdge, Timer
from params import N, Q
from sample_tb import LIMIT, NCASES, OUTW, Monitor, Ready, check_poly, clock_reset, triple, words_of

INIT = dict(start_i=0, abort_i=0, in_valid_i=0, in_data_i=0, coef_ready_i=0)
COVER = set()  # OUTW = 2: (carry held, accepted candidates of the triple) combinations seen at the triple stage
NW = 400  # words offered (3,200 bytes: more than the longest crafted stream needs; a stream never ends before the polynomial is complete)


async def run(dut, stream, rng, ready="always", gap=0.0, check=True):
    """One polynomial from `stream` (bytes). Returns (monitor, bytes_o, cycles, words taken)."""
    words = words_of(stream, NW, rng)
    exp, nbytes, _ = M.sample_ntt_stream(stream)
    await FallingEdge(dut.clk_i)
    dut.start_i.value, dut.abort_i.value, dut.in_valid_i.value = 1, 0, 0
    await FallingEdge(dut.clk_i)
    dut.start_i.value = 0
    mon, rdy, wi, cycles, tail = Monitor(), Ready(ready, rng), 0, 0, 0
    while True:
        cycles += 1
        assert cycles < LIMIT, "sample_ntt_core did not finish"
        go_in = wi < len(words) and rng.random() >= gap
        dut.in_valid_i.value = int(go_in)
        dut.in_data_i.value = words[wi] if wi < len(words) else 0
        go_out = rdy()
        dut.coef_ready_i.value = go_out
        await Timer(1, "ns")
        in_fire = go_in and int(dut.in_ready_o.value)
        mon.sample(dut, go_out)
        if OUTW == 2 and int(dut.tv_q.value) and int(dut.busy_o.value):
            COVER.add((int(dut.cv_q.value), int(dut.a1_q.value) + int(dut.a2_q.value)))
        if in_fire:
            wi += 1
        if mon.done:
            tail += 1
            assert int(dut.busy_o.value) == 0 and int(dut.coef_valid_o.value) == 0
            if tail == 4:
                break
        await FallingEdge(dut.clk_i)
    if check:
        check_poly(mon, exp, "SampleNTT core")
        assert int(dut.bytes_o.value) == nbytes, f"bytes_o {int(dut.bytes_o.value)}, golden {nbytes}"
    return mon, int(dut.bytes_o.value), cycles, wi


def mixed_stream(rng, choices, ntriples=400):
    return b"".join(triple(rng.choice(choices), rng.choice(choices)) for _ in range(ntriples))


@cocotb.test()
async def test_crafted_streams(dut):
    await clock_reset(dut, INIT)
    rng = random.Random(801)
    streams = {}
    edge = [0, 1, Q - 2, Q - 1, Q, Q + 1, 4095]
    for i in range(40):
        streams[f"boundary mix {i}"] = mixed_stream(rng, edge)
    for a in edge:
        for b in edge:
            streams[f"pair {a},{b}"] = triple(a, b) * 400 + triple(7, 8) * 200
    streams["all accepted (128 triples)"] = b"".join(triple(rng.randrange(Q), rng.randrange(Q)) for _ in range(140))
    streams["rejected run 130 then accepted"] = triple(4095, 4095) * 130 + triple(5, 6) * 140
    streams["rejected run 300 then accepted"] = triple(Q, 4095) * 300 + triple(1, Q - 1) * 140
    streams["last coefficient is d1"] = triple(3, 4) * 127 + triple(9, Q) + triple(11, 12) + bytes(range(60))
    streams["last coefficient is d2"] = triple(3, 4) * 128 + bytes(range(60))
    streams["last d2 after reject-accept"] = triple(3, 4) * 127 + triple(Q, 77) + bytes(range(60))
    streams["only d1 accepted"] = triple(5, Q) * 300
    streams["only d2 accepted"] = triple(Q, 5) * 300
    streams["zero candidates"] = triple(0, 0) * 140
    n = 0
    for name, s in streams.items():
        for ready, gap in (("always", 0.0), ("rand", 0.3)):
            await run(dut, s, rng, ready, gap)
            n += 1
    # byte counts of the special streams are what the golden says
    assert M.sample_ntt_stream(streams["all accepted (128 triples)"])[1] == 384
    assert M.sample_ntt_stream(streams["last coefficient is d1"])[1] == 3 * 129
    assert M.sample_ntt_stream(streams["last coefficient is d2"])[1] == 3 * 128
    dut._log.info(f"{n} crafted runs equal to the golden (coefficients and consumed bytes)")


@cocotb.test()
async def test_random_xof_streams(dut):
    await clock_reset(dut, INIT)
    rng = random.Random(802)
    blocks = {}
    for i in range(NCASES):
        msg = bytes(rng.randrange(256) for _ in range(32)) + bytes([i % 3, (i // 3) % 3])
        s = hashlib.shake_128(msg).digest(8 * NW)
        _, nb, _ = M.sample_ntt_stream(s)
        blocks[-(-nb // 168)] = blocks.get(-(-nb // 168), 0) + 1
        await run(dut, s, rng, ready=("always", "rand", "runs")[i % 3], gap=(0.0, 0.2, 0.5)[(i // 3) % 3])
    dut._log.info(f"{NCASES} XOF streams equal to the golden; blocks needed: {sorted(blocks.items())}")


@cocotb.test()
async def test_four_block_streams(dut):
    await clock_reset(dut, INIT)
    rng = random.Random(803)
    found = 0
    while found < 6:
        msg = bytes(rng.randrange(256) for _ in range(34))
        s = hashlib.shake_128(msg).digest(8 * NW)
        _, nb, _ = M.sample_ntt_stream(s)
        if nb > 3 * 168:
            await run(dut, s, rng, ready="runs", gap=0.1)
            found += 1
    dut._log.info("6 polynomials that need a 4th XOF block equal to the golden")


@cocotb.test()
async def test_abort_reset_zeroisation(dut):
    await clock_reset(dut, INIT)
    rng = random.Random(804)
    s = hashlib.shake_128(bytes(34)).digest(8 * NW)
    probes = ("win_q", "cnt_q", "tv_q", "a1_q", "a2_q", "d1_q", "d2_q", "od_q", "ov_q") + (("cv_q", "carry_q") if OUTW == 2 else ())

    def zero():
        return all(int(getattr(dut, p).value) == 0 for p in probes)

    await run(dut, s, rng)
    assert zero(), "state not cleared after done_o"
    for stop_at in (3, 12, 40, 150):
        words = words_of(s, NW, rng)
        await FallingEdge(dut.clk_i)
        dut.start_i.value = 1
        await FallingEdge(dut.clk_i)
        dut.start_i.value = 0
        wi = 0
        for c in range(stop_at):
            go_in = wi < len(words)
            dut.in_valid_i.value, dut.in_data_i.value, dut.coef_ready_i.value = int(go_in), words[wi], int(c % 3 != 0)
            await Timer(1, "ns")
            if go_in and int(dut.in_ready_o.value):
                wi += 1
            await FallingEdge(dut.clk_i)
        dut.abort_i.value, dut.in_valid_i.value = 1, 0
        await FallingEdge(dut.clk_i)
        dut.abort_i.value = 0
        await Timer(1, "ns")
        assert int(dut.busy_o.value) == 0 and zero(), f"abort after {stop_at} cycles: busy or state not cleared"
        await run(dut, s, rng)  # usable again, same result as a fresh run
    # reset in the middle
    words = words_of(s, NW, rng)
    await FallingEdge(dut.clk_i)
    dut.start_i.value = 1
    await FallingEdge(dut.clk_i)
    dut.start_i.value = 0
    for c in range(20):
        dut.in_valid_i.value, dut.in_data_i.value, dut.coef_ready_i.value = 1, words[c % NW], 0
        await FallingEdge(dut.clk_i)
    dut.rst_ni.value = 0
    await Timer(1, "ns")
    assert int(dut.busy_o.value) == 0 and zero(), "asynchronous reset did not clear the state"
    await FallingEdge(dut.clk_i)
    dut.rst_ni.value = 1
    dut.in_valid_i.value = 0
    await run(dut, s, rng)
    dut._log.info("abort at 4 points and reset in the middle clear the window, triple and output registers; the core runs again")


@cocotb.test()
async def test_start_while_busy_and_back_to_back(dut):
    await clock_reset(dut, INIT)
    rng = random.Random(805)
    s1 = hashlib.shake_128(b"a" * 34).digest(8 * NW)
    s2 = hashlib.shake_128(b"b" * 34).digest(8 * NW)
    words = words_of(s1, NW, rng)
    exp, nbytes, _ = M.sample_ntt_stream(s1)
    await FallingEdge(dut.clk_i)
    dut.start_i.value = 1
    await FallingEdge(dut.clk_i)
    mon, wi, c = Monitor(), 0, 0
    while True:
        c += 1
        assert c < LIMIT
        dut.start_i.value = int(c % 5 == 0)  # a start request every 5th cycle while busy: must be ignored
        go_in = wi < len(words)
        dut.in_valid_i.value, dut.in_data_i.value, dut.coef_ready_i.value = int(go_in), words[wi], 1
        await Timer(1, "ns")
        if go_in and int(dut.in_ready_o.value):
            wi += 1
        mon.sample(dut, 1)
        if mon.done:
            break
        await FallingEdge(dut.clk_i)
    dut.start_i.value = 0
    check_poly(mon, exp, "start while busy")
    assert int(dut.bytes_o.value) == nbytes
    await FallingEdge(dut.clk_i)
    await run(dut, s2, rng)  # next polynomial straight after
    await run(dut, s2, rng)  # same input again: same polynomial
    dut._log.info("start while busy ignored; back-to-back polynomials correct")


@cocotb.test(skip=OUTW != 2)
async def test_w2_pool_coverage(dut):
    """W2: every (carry held 0/1) x (accepted candidates 0/1/2) combination of the pool reaches the triple stage, a pool of 3 included, and the results are right."""
    await clock_reset(dut, INIT)
    rng = random.Random(806)
    for i in range(60):
        await run(dut, mixed_stream(rng, [0, 5, Q - 1, Q, 4095], 500), rng, ("always", "rand", "runs")[i % 3], (0.0, 0.3)[i % 2])
    assert COVER >= {(c, k) for c in (0, 1) for k in (0, 1, 2)}, f"pool combinations seen: {sorted(COVER)}"
    dut._log.info(f"all six pool combinations (carry, accepted) seen: {sorted(COVER)}")
