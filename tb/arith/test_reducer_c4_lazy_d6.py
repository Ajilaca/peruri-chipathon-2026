"""tb/arith/test_reducer_c4_lazy_d6.py - Phase 5c test plan A4: rtl/arith/modmul_barrett_lazy.sv driven with
operands a, b in [0, q) (the ADR 0011 D6 contract, i.e. a regression of 5b) and with the lazy extremes b in
[q, 2q): corners, 10,000 random pairs back-to-back, latency exactly LATENCY cycles. The exhaustive check over the
whole lazy domain is tb/arith/lazy_exhaustive/. C4_REG_AFTER gives REG_AFTER (latency = bits set)."""

import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, Timer
from params import Q

REG_AFTER = int(os.environ.get("C4_REG_AFTER", "0"))
LATENCY = bin(REG_AFTER).count("1")


async def _stream(dut, pairs):
    cocotb.start_soon(Clock(dut.clk_i, 10, unit="ns").start())
    pending = []
    for a, b in pairs + [(0, 0)] * LATENCY:
        await FallingEdge(dut.clk_i)
        dut.a_i.value, dut.b_i.value = a, b
        pending.append((a, b))
        await Timer(1, unit="ns")
        if len(pending) > LATENCY:
            ea, eb = pending[-1 - LATENCY]
            got = int(dut.p_o.value)
            assert got == (ea * eb) % Q, f"({ea}*{eb}) mod q = {(ea * eb) % Q}, got {got}"


@cocotb.test()
async def test_corners(dut):
    m = Q - 1
    pairs = [(a, b) for a in (0, 1, m, m - 1) for b in (0, 1, m, Q, Q + 1, 2 * Q - 2, 2 * Q - 1)]
    await _stream(dut, pairs)


@cocotb.test()
async def test_random_d6_domain(dut):
    rng = random.Random(61 + REG_AFTER)
    await _stream(dut, [(rng.randrange(Q), rng.randrange(Q)) for _ in range(10000)])


@cocotb.test()
async def test_random_lazy_domain(dut):
    rng = random.Random(62 + REG_AFTER)
    await _stream(dut, [(rng.randrange(Q), rng.randrange(2 * Q)) for _ in range(10000)])
