"""tb/sample/test_keccak_sampler.py -- test plan 8b V5, V6 and V7 (top level): rtl/sample/keccak_sampler.sv (sponge + sampler) against hashlib and tb/golden/sampler_model.py.
SampleNTT for rho || j || i (3 x 3 index pairs, random rho), CBD2 for sigma || N; back-pressure on both sides; abort and reset; the sponge is stopped and wiped when the polynomial is complete; cycle counts.
Environment: KS_N (cases, default 500), KS_OUTW (output width), KS_CORE (informational, set by the runner), KS_CYCLES_OUT (json file for the cycle table)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
import os
import random

import cocotb
import sampler_model as M
from cocotb.triggers import FallingEdge, Timer
from params import N, Q
from sample_tb import LIMIT, NCASES, OUTW, Monitor, Ready, check_poly, clock_reset

INIT = dict(start_i=0, kind_i=0, len_i=0, abort_i=0, in_valid_i=0, in_data_i=0, coef_ready_i=0)
CYCLES_OUT = os.environ.get("KS_CYCLES_OUT", "")
LOG = []
PCSTAT = {}  # perm_cnt_o - blocks needed -> number of polynomials


def msg_words(msg, rng):
    """Message words; bytes past the message in the last word are garbage (the sponge ignores them)."""
    out = []
    for w in range(-(-len(msg) // 8)):
        chunk = msg[8 * w: 8 * w + 8]
        chunk = chunk + bytes(rng.randrange(256) for _ in range(8 - len(chunk)))
        out.append(int.from_bytes(chunk, "little"))
    return out


def sum_max(stream):
    """Output cycles of the W1 triple stage (sum over triples of max(1, accepted)) and the number of triples: both from the golden stream, public data."""
    pos, n, tot, t = 0, 0, 0, 0
    while n < N:
        b0, b1, b2 = stream[pos], stream[pos + 1], stream[pos + 2]
        pos += 3
        t += 1
        d = [b0 + 256 * (b1 % 16), (b1 >> 4) + 16 * b2]
        k = min(sum(1 for x in d if x < Q), N - n)
        tot += max(1, k)
        n += k
    return tot, t


def expected(kind, msg):
    if kind == 0:
        s = hashlib.shake_128(msg).digest(1600)
        coefs, nb, _ = M.sample_ntt_stream(s)
        return coefs, nb, s
    s = hashlib.shake_256(msg).digest(128)
    return M.cbd2(s), 128, s


async def poly(dut, kind, msg, rng, ready="always", gap=0.0, abort_at=None, log=True, tail_cycles=4):
    """One polynomial through the top. Returns (monitor, cycles from the start cycle to done_o, perm_cnt_o, sponge words taken)."""
    words = msg_words(msg, rng)
    exp = expected(kind, msg) if abort_at is None else None
    await FallingEdge(dut.clk_i)
    dut.start_i.value, dut.kind_i.value, dut.len_i.value, dut.abort_i.value, dut.in_valid_i.value = 1, kind, len(msg), 0, 0
    await FallingEdge(dut.clk_i)
    dut.start_i.value = 0
    mon, rdy, wi, cycles, sp_words, tail = Monitor(), Ready(ready, rng), 0, 1, 0, 0
    pc = None
    while True:
        cycles += 1
        assert cycles < LIMIT, "keccak_sampler did not finish"
        if abort_at is not None and cycles == abort_at:
            dut.abort_i.value, dut.in_valid_i.value = 1, 0
            await FallingEdge(dut.clk_i)
            dut.abort_i.value = 0
            return None
        go_in = wi < len(words) and rng.random() >= gap
        dut.in_valid_i.value = int(go_in)
        dut.in_data_i.value = words[wi] if wi < len(words) else rng.getrandbits(64)
        go_out = rdy()
        dut.coef_ready_i.value = go_out
        await Timer(1, "ns")
        if go_in and int(dut.in_ready_o.value):
            wi += 1
        if int(dut.sp_out_valid.value) and int(dut.sp_out_ready.value):
            sp_words += 1
        mon.sample(dut, go_out)
        if mon.done:
            if tail == 0:
                done_cycle = cycles
                pc = int(dut.perm_cnt_o.value)
            tail += 1
            assert int(dut.busy_o.value) == 0
            if tail == tail_cycles:
                break
        await FallingEdge(dut.clk_i)
    coefs, nbytes, stream = exp
    check_poly(mon, coefs, "SampleNTT top" if kind == 0 else "CBD top")
    assert int(dut.bytes_o.value) == nbytes, f"bytes_o {int(dut.bytes_o.value)}, golden {nbytes}"
    if kind == 0:
        # Permutations the golden needs: floor(len / 168) + 1 to absorb the message, then one per extra squeezed block (plan Amendment A1).
        blocks = len(msg) // 168 + 1 + (-(-nbytes // 168) - 1)
        last_blk = (-(-nbytes // 168)) * 168  # end of the last block used
        # The window prefetches up to 11 bytes beyond the consumed ones. If it took the last word of the final block while the output was held back, the sponge has already finished the next
        # permutation, so perm_cnt_o is the golden count or one more, and one more only when the consumed bytes reach into the last 11 bytes of that block. Without back-pressure it is equal.
        assert pc in (blocks, blocks + 1), f"perm_cnt_o {pc}, golden says {blocks}; ready={ready} gap={gap} len={len(msg)} bytes={nbytes}"
        if pc == blocks + 1:
            assert nbytes >= last_blk - 11, f"perm_cnt_o {pc} = golden + 1 but only {nbytes} bytes consumed (block ends at {last_blk}); ready={ready} gap={gap} sponge words taken={sp_words} len={len(msg)}"
        if ready == "always" and gap == 0.0:
            assert pc == blocks, f"perm_cnt_o {pc}, golden says {blocks} (no back-pressure); len={len(msg)} bytes={nbytes}"
        PCSTAT[pc - blocks] = PCSTAT.get(pc - blocks, 0) + 1
    else:
        assert sp_words == 16, f"{sp_words} sponge words taken, expected 16"
        assert pc == 1, f"perm_cnt_o {pc}, expected 1"
    return mon, done_cycle, pc, sp_words


@cocotb.test()
async def test_sample_ntt_bit_exact(dut):
    await clock_reset(dut, INIT)
    rng = random.Random(821)
    for i in range(NCASES):
        msg = bytes(rng.randrange(256) for _ in range(32)) + bytes([i % 3, (i // 3) % 3])
        await poly(dut, 0, msg, rng, ready=("always", "rand", "runs")[i % 3], gap=(0.0, 0.3)[(i // 3) % 2])
    for ln in (0, 1, 33, 168, 169, 300):  # any len_i is allowed: the stream is that of hashlib for the same bytes
        await poly(dut, 0, bytes(rng.randrange(256) for _ in range(ln)), rng)
    dut._log.info(f"{NCASES} SampleNTT polynomials (rho || j || i) and 6 other message lengths equal to the golden fed with hashlib SHAKE128; perm_cnt_o minus blocks needed: {sorted(PCSTAT.items())}")


@cocotb.test()
async def test_four_block_polynomials(dut):
    await clock_reset(dut, INIT)
    rng = random.Random(822)
    found = 0
    while found < 6:
        msg = bytes(rng.randrange(256) for _ in range(34))
        if expected(0, msg)[1] > 3 * 168:
            await poly(dut, 0, msg, rng, ready="runs", gap=0.1)
            found += 1
    dut._log.info("6 polynomials that need a 4th XOF block (rho values from a fixed PRNG seed) equal to the golden; perm_cnt_o = 4")


@cocotb.test()
async def test_cbd_bit_exact(dut):
    await clock_reset(dut, INIT)
    rng = random.Random(823)
    for i in range(NCASES):
        msg = bytes(rng.randrange(256) for _ in range(32)) + bytes([i % 256])
        await poly(dut, 1, msg, rng, ready=("always", "rand", "runs")[i % 3], gap=(0.0, 0.3)[(i // 3) % 2])
    for msg in (bytes(33), b"\xff" * 33):
        await poly(dut, 1, msg, rng)
    dut._log.info(f"{NCASES} CBD2 polynomials (sigma || N) equal to the golden fed with hashlib SHAKE256; exactly 16 sponge words taken each time")


@cocotb.test()
async def test_cbd_words_17th_not_taken(dut):
    await clock_reset(dut, INIT)
    rng = random.Random(824)
    for i in range(20):
        _, _, _, w = await poly(dut, 1, bytes(rng.randrange(256) for _ in range(33)), rng, ready="always", tail_cycles=30)
        assert w == 16
    dut._log.info("20 CBD polynomials: the sponge word handshake count is 16 up to 30 cycles after done_o")


@cocotb.test()
async def test_stop_wipes_sponge(dut):
    await clock_reset(dut, INIT)
    rng = random.Random(825)
    for kind in (0, 1):
        mon, _, pc, _ = await poly(dut, kind, bytes(rng.randrange(256) for _ in range(34 - kind)), rng, tail_cycles=3)
        for _ in range(40):
            await FallingEdge(dut.clk_i)
            assert int(dut.sp_busy.value) == 0, "the sponge is still busy after done_o: stop_i was not issued"
            assert int(dut.perm_cnt_o.value) == pc
        await Timer(1, "ns")
    dut._log.info("after done_o the sponge is idle (stop_i issued) and its permutation counter is stable, SampleNTT and CBD")


@cocotb.test()
async def test_constant_cycles_and_cycle_table(dut):
    """V6. CBD: one cycle count for every sigma and N. SampleNTT: the same input twice gives the same count; r = cycles - base is tabulated per number of XOF blocks."""
    await clock_reset(dut, INIT)
    rng = random.Random(826)
    cbd_counts = set()
    for n in range(34):
        for _ in range(3):
            sigma = rng.choice([bytes(32), b"\xff" * 32, bytes(rng.randrange(256) for _ in range(32))])
            _, c, _, _ = await poly(dut, 1, sigma + bytes([n]), rng)
            LOG.append(dict(kind="cbd", len=33, cycles=c))
            cbd_counts.add(c)
    assert len(cbd_counts) == 1, f"CBD cycle counts differ with the data: {sorted(cbd_counts)}"
    rtab = {}
    for i in range(NCASES):
        msg = bytes(rng.randrange(256) for _ in range(32)) + bytes([i % 3, (i // 3) % 3])
        _, c, _, _ = await poly(dut, 0, msg, rng)
        _, nb, s = expected(0, msg)
        tot, t = sum_max(s)
        base = tot if OUTW == 1 else t
        b = -(-nb // 168)
        rtab.setdefault(b, set()).add(c - base)
        LOG.append(dict(kind="sample_ntt", len=34, cycles=c, blocks=b, triples=t, sum_max=tot, bytes=nb))
        if i < 40:
            _, c2, _, _ = await poly(dut, 0, msg, rng)
            assert c2 == c, "the same input gave two different cycle counts"
    if CYCLES_OUT:
        with open(CYCLES_OUT, "w") as f:
            json.dump(LOG, f)
    dut._log.info(f"CBD cycles identical at 102 points: {cbd_counts.pop()}; SampleNTT repeatable (40 repeats); r = cycles - base per blocks: " + ", ".join(f"B={b}: {sorted(v)}" for b, v in sorted(rtab.items())))


@cocotb.test()
async def test_abort_reset_zeroisation(dut):
    await clock_reset(dut, INIT)
    rng = random.Random(827)

    def zero(kind):
        names = ("win_q", "tv_q", "d1_q", "d2_q", "od_q", "ov_q") if kind == 0 else ("w_q", "wv_q", "od_q", "ov_q")
        core = dut.u_ntt if kind == 0 else dut.u_cbd
        return all(int(getattr(core, p).value) == 0 for p in names)

    for kind in (0, 1):
        msg = bytes(rng.randrange(256) for _ in range(34 - kind))
        await poly(dut, kind, msg, rng)
        assert zero(kind), "core state not cleared after done_o"
        for at in (3, 8, 20, 45, 120):
            await poly(dut, kind, msg, rng, abort_at=at)
            await Timer(1, "ns")
            assert int(dut.busy_o.value) == 0 and zero(kind), f"abort at cycle {at}: busy or state not cleared"
            for _ in range(3):
                await FallingEdge(dut.clk_i)
            assert int(dut.sp_busy.value) == 0, "sponge still busy after abort"
            await poly(dut, kind, msg, rng)  # the next polynomial is correct (nothing leaked from the aborted one)
        # reset in the middle
        await FallingEdge(dut.clk_i)
        dut.start_i.value, dut.kind_i.value, dut.len_i.value = 1, kind, len(msg)
        await FallingEdge(dut.clk_i)
        dut.start_i.value = 0
        for _ in range(60):
            await FallingEdge(dut.clk_i)
        dut.rst_ni.value = 0
        await Timer(1, "ns")
        assert int(dut.busy_o.value) == 0 and zero(kind) and int(dut.sp_busy.value) == 0, "reset did not clear"
        await FallingEdge(dut.clk_i)
        dut.rst_ni.value = 1
        await poly(dut, kind, msg, rng)
    dut._log.info("abort at 5 points per kind and reset in the middle: busy low, window/word/output registers zero, sponge idle, the next polynomial correct")


@cocotb.test()
async def test_start_while_busy(dut):
    await clock_reset(dut, INIT)
    rng = random.Random(828)
    msg = bytes(rng.randrange(256) for _ in range(34))
    words = msg_words(msg, rng)
    coefs, nb, _ = expected(0, msg)
    await FallingEdge(dut.clk_i)
    dut.start_i.value, dut.kind_i.value, dut.len_i.value = 1, 0, 34
    await FallingEdge(dut.clk_i)
    mon, wi, c = Monitor(), 0, 0
    while True:
        c += 1
        assert c < LIMIT
        dut.start_i.value, dut.kind_i.value = int(c % 4 == 0), int(c % 8 == 0)  # a start request (even of the other kind) while busy: ignored
        go_in = wi < len(words)
        dut.in_valid_i.value, dut.in_data_i.value, dut.coef_ready_i.value = int(go_in), words[wi] if go_in else 0, 1
        await Timer(1, "ns")
        if go_in and int(dut.in_ready_o.value):
            wi += 1
        mon.sample(dut, 1)
        if mon.done:
            break
        await FallingEdge(dut.clk_i)
    dut.start_i.value = 0
    check_poly(mon, coefs, "start while busy")
    dut._log.info("start requests while busy (both kinds) are ignored; the polynomial is unchanged")
