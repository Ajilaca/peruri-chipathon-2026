"""tb/mlkem/hashfo_tb.py -- shared helpers of the Phase 9b tests (docs/evidence/phase09-integration/9b/test_plan_9b.md).

Same cycle model as the 9a drivers: inputs are written at the falling edge, the combinational outputs are read 1 ns later and are the values the next rising edge samples.
Toplevel: rtl/mlkem/mlkem_hash_fo_top.sv (hash wrapper h_*, comparison f_*).
"""
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, Timer
from codec_tb import MODES, Pattern, val  # noqa: F401  (Pattern: valid / ready patterns, val: X-tolerant read)

LIMIT = 20000
H, G, J = 0, 1, 2
WORDS = int(os.environ.get("HF_WORDS", "136"))


def to_words(msg: bytes, rng) -> list[int]:
    """64-bit little-endian words of the message; the unused bytes of the last word hold random garbage (the sponge must ignore them)."""
    n = (len(msg) + 7) // 8
    pad = bytes(rng.randrange(256) for _ in range(8 * n - len(msg)))
    b = msg + pad
    return [int.from_bytes(b[8 * i: 8 * i + 8], "little") for i in range(n)]


async def clock_reset(dut):
    cocotb.start_soon(Clock(dut.clk_i, 10, unit="ns").start())
    dut.rst_ni.value = 0
    for n in ("h_start_i", "h_sel_i", "h_len_i", "h_in_valid_i", "h_in_data_i", "h_out_ready_i", "f_start_i", "f_in_valid_i", "f_a_data_i", "f_b_data_i", "f_kgood_i", "f_kbad_i"):
        getattr(dut, n).value = 0
    await ClockCycles(dut.clk_i, 3)
    await FallingEdge(dut.clk_i)
    dut.rst_ni.value = 1


async def idle(dut, n=3):
    await ClockCycles(dut.clk_i, n)
    await FallingEdge(dut.clk_i)


async def hash_run(dut, sel, msg, rng, src="always", sink="always", start_noise=False, extra_after=0):
    """One hash run. Returns dict: words (digest words), cycles (falling edges from the start cycle to done_o), last_at (indices of words with out_last_o), done (pulses), taken (message words accepted)."""
    await FallingEdge(dut.clk_i)
    dut.h_start_i.value = 1
    dut.h_sel_i.value = sel
    dut.h_len_i.value = len(msg)
    await FallingEdge(dut.clk_i)
    dut.h_start_i.value = 1 if start_noise else 0          # a start while busy must be ignored
    if start_noise:
        dut.h_sel_i.value = (sel + 1) % 3
        dut.h_len_i.value = len(msg) + 8
    mw = to_words(msg, rng)
    src_p, sink_p = Pattern(src, rng), Pattern(sink, rng)
    out, idx, last_at, done, cycles, prev = [], 0, [], 0, 0, None
    for _ in range(LIMIT):
        cycles += 1
        v = int(idx < len(mw) and src_p())
        dut.h_in_valid_i.value = v
        dut.h_in_data_i.value = mw[idx] if idx < len(mw) else rng.getrandbits(64)
        r = sink_p()
        dut.h_out_ready_i.value = r
        await Timer(1, "ns")
        ir, ov, od, ol = int(dut.h_in_ready_o.value), int(dut.h_out_valid_o.value), val(dut.h_out_data_o), int(dut.h_out_last_o.value)
        if prev is not None and prev[0] and not prev[3]:
            assert ov and od == prev[1] and ol == prev[2], "digest word not held while h_out_ready_i was low"
        prev = (ov, od, ol, r)
        if v and ir:
            idx += 1
        assert od != -1 or not ov, "valid digest word with an unresolved value"
        if ov and r:
            out.append(od)
            if ol:
                last_at.append(len(out) - 1)
        if int(dut.h_done_o.value):
            done += 1
            break
        await FallingEdge(dut.clk_i)
    dut.h_in_valid_i.value = 0
    dut.h_out_ready_i.value = 0
    dut.h_start_i.value = 0
    return {"words": out, "cycles": cycles, "last_at": last_at, "done": done, "taken": idx}


def digest_bytes(words) -> bytes:
    return b"".join(w.to_bytes(8, "little") for w in words)


async def fo_run(dut, a: bytes, b: bytes, kgood: int, kbad: int, rng, src="always", start_noise=False):
    """One comparison run. a and b are WORDS * 8 bytes. Returns dict: neq, k, cycles, done, taken."""
    aw = [int.from_bytes(a[8 * i: 8 * i + 8], "little") for i in range(WORDS)]
    bw = [int.from_bytes(b[8 * i: 8 * i + 8], "little") for i in range(WORDS)]
    await FallingEdge(dut.clk_i)
    dut.f_start_i.value = 1
    await FallingEdge(dut.clk_i)
    dut.f_start_i.value = 1 if start_noise else 0
    src_p = Pattern(src, rng)
    idx, done, cycles = 0, 0, 0
    for _ in range(LIMIT):
        cycles += 1
        v = int(src_p())                              # keep offering beats after the last one: they must not be accepted
        dut.f_in_valid_i.value = v
        dut.f_a_data_i.value = aw[idx] if idx < WORDS else rng.getrandbits(64)
        dut.f_b_data_i.value = bw[idx] if idx < WORDS else rng.getrandbits(64)
        dut.f_kgood_i.value = kgood
        dut.f_kbad_i.value = kbad
        await Timer(1, "ns")
        ir = int(dut.f_in_ready_o.value)
        if v and ir:
            idx += 1
        if int(dut.f_done_o.value):
            done += 1
            break
        await FallingEdge(dut.clk_i)
    dut.f_in_valid_i.value = 0
    dut.f_start_i.value = 0
    await Timer(1, "ns")
    return {"neq": int(dut.f_neq_o.value), "k": int(dut.f_k_o.value), "cycles": cycles, "done": done, "taken": idx}
