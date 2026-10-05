"""tb/ntt/test_butterfly_pipe.py - cocotb test for rtl/ntt/butterfly_shared_pipe.sv (Phase 4 test plan V3):
the pipelined butterfly against the exact per-butterfly step of tb/golden/primitives.py (forward CT,
inverse GS), inputs streamed back-to-back, each result compared exactly LATENCY cycles after its inputs.

MUL_REG comes from the P4_MUL_REG environment variable (set per build by run_p4_unit_tests.py).
"""

import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, Timer
from params import Q
from primitives import _ZETA_BITREV

MUL_REG = int(os.environ.get("P4_MUL_REG", "0"))
LATENCY = bin(MUL_REG).count("1")


def _fwd(a, b, zeta):
    t = (zeta * b) % Q
    return (a + t) % Q, (a - t) % Q


def _inv(a, b, zeta):
    return (a + b) % Q, (zeta * (b - a)) % Q


async def _stream(dut, mode, triples):
    """One (a, b, zeta) per clock with no bubbles; mode_i is constant for the whole stream, as in a run."""
    dut.mode_i.value = mode
    gold = _fwd if mode == 0 else _inv
    sent = []
    for a, b, z in triples + [(0, 0, 1)] * LATENCY:
        await FallingEdge(dut.clk_i)
        dut.a_i.value = a
        dut.b_i.value = b
        dut.zeta_i.value = z
        sent.append((a, b, z))
        await Timer(1, unit="ns")
        if len(sent) > LATENCY:
            ea, eb, ez = sent[-1 - LATENCY]
            got = (int(dut.a_o.value), int(dut.b_o.value))
            assert got == gold(ea, eb, ez), (
                f"MUL_REG={MUL_REG} mode={mode} a={ea} b={eb} zeta={ez}: expected {gold(ea, eb, ez)}, "
                f"got {got} (latency {LATENCY})")


@cocotb.test()
async def test_corners(dut):
    cocotb.start_soon(Clock(dut.clk_i, 10, unit="ns").start())
    m = Q - 1
    zetas = (_ZETA_BITREV[0], _ZETA_BITREV[-1], max(_ZETA_BITREV))   # first and last table entries, largest
    triples = [(a, b, z) for z in zetas for a, b in ((0, 0), (m, m), (0, m), (m, 0))]
    for mode in (0, 1):
        await _stream(dut, mode, triples)


@cocotb.test()
async def test_random_back_to_back(dut):
    cocotb.start_soon(Clock(dut.clk_i, 10, unit="ns").start())
    rng = random.Random(41 + MUL_REG)
    for mode in (0, 1):
        await _stream(dut, mode, [(rng.randrange(Q), rng.randrange(Q), rng.choice(_ZETA_BITREV))
                                  for _ in range(1000)])
