"""tb/arith/test_lazy_corners.py — Phase 5c test plan A4 V4-lazy: corner cases of the lazy INTT butterfly input
(rtl/arith/butterfly_c4_lazy.sv) against the exact per-butterfly step of tb/golden/primitives.py.

Corners (both extreme lazy values, with every twiddle of the table): a = 0, b = q-1 (multiplier input u = 2q-1);
a = q-1, b = 0 (u = 1); a = b = q-1 (side operand s = 2q-2); a = b = 0; a = 1, b = 0; a = 0, b = 1; all streamed
back-to-back in INTT mode and in NTT mode. MUL_REG comes from P4_MUL_REG (latency = bits set).
"""

import os
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
    dut.mode_i.value = mode
    gold = _fwd if mode == 0 else _inv
    sent = []
    for a, b, z in triples + [(0, 0, 1)] * LATENCY:
        await FallingEdge(dut.clk_i)
        dut.a_i.value, dut.b_i.value, dut.zeta_i.value = a, b, z
        sent.append((a, b, z))
        await Timer(1, unit="ns")
        if len(sent) > LATENCY:
            ea, eb, ez = sent[-1 - LATENCY]
            got = (int(dut.a_o.value), int(dut.b_o.value))
            assert got == gold(ea, eb, ez), (
                f"MUL_REG={MUL_REG} mode={mode} a={ea} b={eb} zeta={ez}: expected {gold(ea, eb, ez)}, got {got}")


@cocotb.test()
async def test_lazy_extremes_all_twiddles(dut):
    cocotb.start_soon(Clock(dut.clk_i, 10, unit="ns").start())
    m = Q - 1
    pairs = [(0, m), (m, 0), (m, m), (0, 0), (1, 0), (0, 1), (1, m), (m, 1), (m - 1, m), (m, m - 1)]
    triples = [(a, b, z) for z in sorted(set(_ZETA_BITREV)) for a, b in pairs]
    for mode in (1, 0):
        await _stream(dut, mode, triples)
