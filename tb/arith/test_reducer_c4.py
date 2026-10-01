"""tb/arith/test_reducer_c4.py — cocotb unit test (Phase 5 test plan V3, corner list of section 6) for a
reducer behind rtl/arith/modmul_sel.sv, driven through tb/arith/c4_tb_wrappers.sv:modmul_c4_tb (which supplies b in
Montgomery form for RED_KIND 3, so every kind is checked against (a * b) mod q). The exhaustive check over all a, b is tb/arith/reducer_exhaustive/;
this test covers the named corners, 10,000 random pairs back-to-back, isolated inputs with idle cycles between
them, and that every result appears exactly LATENCY cycles after its inputs.

Environment (set per build by tb/arith/run_c4_unit_tests.py):
  C4_RED_KIND   reducer kind of modmul_sel (0 = staged, 1 = fold, 2 = Barrett, 3 = Montgomery)
  C4_REG_AFTER  REG_AFTER of the build (latency = number of bits set)
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

RED_KIND = int(os.environ.get("C4_RED_KIND", "1"))
REG_AFTER = int(os.environ.get("C4_REG_AFTER", "0"))
LATENCY = bin(REG_AFTER).count("1")
INV128 = 3303


def _fold_trace(x: int) -> list[int]:
    """Python model of rtl/arith/modmul_fold.sv: the value after each of the five folds."""
    vals = []
    for _ in range(5):
        x = 767 * (x >> 12) + (x & 0xFFF)
        vals.append(x)
    return vals


def _pre_select(a: int, b: int) -> int:
    """The value entering the final select stage of the reducer of this build (Python models of the RTL)."""
    x = a * b
    if RED_KIND == 2:                                   # Barrett: r = x - q * ((x * 5039) >> 24)
        return x - Q * ((x * 5039) >> 24)
    if RED_KIND == 3:                                   # Montgomery: b arrives in Montgomery form
        x = a * ((b * 4096) % Q)
        m = (-769 * (x & 0xFFF)) & 0xFFF
        return (x + m * Q) >> 12
    return _fold_trace(x)[-1]                           # fold (and a harmless extra set for kind 0)


def _pair_for(prod: int):
    """Some (a, b) in [0, q)^2 with a * b == prod, or None."""
    for a in range(max(1, -(-prod // (Q - 1))), Q):
        if prod % a == 0 and prod // a < Q:
            return a, prod // a
    return None


def _corners() -> list[tuple[int, int]]:
    m = Q - 1
    pairs = [(0, 0), (0, m), (m, 0), (1, 1), (1, m), (m, 1), (m, m), (2, m), (m, 2)]
    # products at and next to multiples of q
    for k in (1, 2, Q - 2, Q - 1):
        for prod in (k * Q - 1, k * Q, k * Q + 1):
            p = _pair_for(prod)
            if p:
                pairs.append(p)
    # products next to fold boundaries 2^12 * j
    for j in (1, 2, 767, 2703):
        for prod in (4096 * j - 1, 4096 * j, 4096 * j + 1):
            p = _pair_for(prod)
            if p:
                pairs.append(p)
    # products whose value before the final select lies at / near q and 2q (found on a fixed grid)
    rng = random.Random(5)
    want = {Q - 1: None, Q: None, 2 * Q - 1: None, 2 * Q: None}
    best_high = None
    for _ in range(200000):
        a, b = rng.randrange(Q), rng.randrange(Q)
        v = _pre_select(a, b)
        if v in want and want[v] is None:
            want[v] = (a, b)
        if best_high is None or v > best_high[0]:
            best_high = (v, (a, b))
    pairs += [p for p in want.values() if p]
    pairs.append(best_high[1])
    # every twiddle and the INTT scaling constant against 0, 1, q-1
    for z in list(_ZETA_BITREV) + [INV128]:
        for b in (0, 1, m):
            pairs.append((z, b))
    return pairs


async def _start(dut):
    cocotb.start_soon(Clock(dut.clk_i, 10, unit="ns").start())
    dut.a_i.value = 0
    dut.b_i.value = 0


async def _stream(dut, pairs):
    """One pair per clock, back-to-back; each result checked LATENCY cycles later."""
    pending = []
    for a, b in pairs + [(0, 0)] * LATENCY:
        await FallingEdge(dut.clk_i)
        dut.a_i.value = a
        dut.b_i.value = b
        pending.append((a, b))
        await Timer(1, unit="ns")
        if len(pending) > LATENCY:
            ea, eb = pending[-1 - LATENCY]
            got = int(dut.p_o.value)
            assert got == (ea * eb) % Q, (
                f"kind={RED_KIND} REG_AFTER={REG_AFTER}: ({ea}*{eb}) mod q = {(ea * eb) % Q}, got {got}")


@cocotb.test()
async def test_corners_back_to_back(dut):
    await _start(dut)
    await _stream(dut, _corners())


@cocotb.test()
async def test_random_back_to_back(dut):
    await _start(dut)
    rng = random.Random(50 + REG_AFTER + 1000 * RED_KIND)
    await _stream(dut, [(rng.randrange(Q), rng.randrange(Q)) for _ in range(10000)])


@cocotb.test()
async def test_isolated_inputs_latency(dut):
    """A single input followed by idle (zero) cycles: the result must appear exactly LATENCY cycles later and
    the zeros around it must give 0, i.e. no value leaks into a neighbouring cycle."""
    await _start(dut)
    rng = random.Random(7)
    seq = []
    for _ in range(50):
        seq.append((rng.randrange(1, Q), rng.randrange(1, Q)))
        seq += [(0, 0)] * rng.randrange(1, 5)
    await _stream(dut, seq)
