"""tb/ntt/test_modmul_staged.py - cocotb unit test for rtl/ntt/modmul_reduce_staged.sv (Phase 4 test
plan V2, corner cases and latency). The exhaustive equality check against modmul_reduce.sv is
tb/ntt/p4_reducer/; this test checks the corner cases named in the plan and that results come out
exactly LATENCY cycles after their inputs when inputs are applied back-to-back (no bubbles).

REG_AFTER comes from the P4_REG_AFTER environment variable (set per build by run_p4_unit_tests.py).
"""

import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from params import Q

REG_AFTER = int(os.environ.get("P4_REG_AFTER", "0"))
LATENCY = bin(REG_AFTER).count("1")


def _corners() -> list[tuple[int, int]]:
    m = Q - 1
    pairs = [(0, 0), (m, m), (1, 0), (0, 1), (1, 1), (1, m), (m, 1), (2, m), (m, 2)]
    for k in (1, 2, 1000, m):                       # products just below / at / just above multiples of q
        for prod in (k * Q - 1, k * Q, k * Q + 1):
            for a in range(1, Q):
                if prod % a == 0 and prod // a < Q:
                    pairs.append((a, prod // a))
                    break
    return pairs


async def _stream(dut, pairs):
    """Applies one pair per clock, back-to-back; checks each result LATENCY cycles later."""
    cocotb.start_soon(Clock(dut.clk_i, 10, unit="ns").start())
    pending = []
    for a, b in pairs + [(0, 0)] * LATENCY:
        await FallingEdge(dut.clk_i)
        dut.a_i.value = a
        dut.b_i.value = b
        pending.append((a, b))
        await cocotb.triggers.Timer(1, unit="ns")
        if len(pending) > LATENCY:
            ea, eb = pending[-1 - LATENCY]
            got = int(dut.p_o.value)
            assert got == (ea * eb) % Q, (
                f"REG_AFTER={REG_AFTER}: ({ea}*{eb}) mod q = {(ea * eb) % Q}, got {got} "
                f"(latency {LATENCY})")


@cocotb.test()
async def test_corners_and_latency(dut):
    await _stream(dut, _corners())


@cocotb.test()
async def test_random_back_to_back(dut):
    rng = random.Random(40 + REG_AFTER)
    await _stream(dut, [(rng.randrange(Q), rng.randrange(Q)) for _ in range(2000)])
