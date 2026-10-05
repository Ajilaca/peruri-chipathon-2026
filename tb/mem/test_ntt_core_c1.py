"""tb/mem/test_ntt_core_c1.py - cocotb bit-exact + cycle-exact regression for rtl/mem/ntt_core_c1.sv
(configuration C1: C0's FSM/butterfly + poly_mem_banked at NUM_BANKS=1) against
tb/golden/primitives.py and against Phase 1's own MEASURED cycle counts.

Per evidence/phase02/test_plan.md ("Regression: ntt_core_c1"): the banked memory at
NUM_BANKS=1 must not change behaviour OR cycle count relative to C0
(evidence/phase01/cocotb_regression.txt: NTT=897, INTT=1153). This
test checks equality against those exact numbers, not just "constant" -- a stall cycle introduced
by the bank-map lookup would still be a constant cycle count, just the wrong one, and must FAIL.
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, Timer
from params import N, Q
from primitives import intt, ntt

CLK_PERIOD_NS = 10
MAX_CYCLES = 5000
C0_NTT_CYCLES = 897
C0_INTT_CYCLES = 1153


def _corner_polys() -> list[list[int]]:
    m = Q - 1
    imp0 = [0] * N
    imp0[0] = 1
    imp_last = [0] * N
    imp_last[-1] = 1
    alt = [(0 if i % 2 == 0 else m) for i in range(N)]
    return [[0] * N, [m] * N, imp0, imp_last, alt]


async def _start_clock(dut) -> None:
    cocotb.start_soon(Clock(dut.clk_i, CLK_PERIOD_NS, unit="ns").start())


async def _reset(dut) -> None:
    dut.rst_ni.value = 0
    dut.start_i.value = 0
    dut.mode_i.value = 0
    dut.host_we_i.value = 0
    dut.host_addr_i.value = 0
    dut.host_wdata_i.value = 0
    await ClockCycles(dut.clk_i, 5)
    dut.rst_ni.value = 1
    await RisingEdge(dut.clk_i)


async def _load(dut, coeffs: list[int]) -> None:
    for addr, val in enumerate(coeffs):
        dut.host_addr_i.value = addr
        dut.host_wdata_i.value = val
        dut.host_we_i.value = 1
        await RisingEdge(dut.clk_i)
    dut.host_we_i.value = 0


async def _read_all(dut) -> list[int]:
    out = []
    for addr in range(N):
        dut.host_addr_i.value = addr
        await Timer(1, unit="ns")
        out.append(int(dut.host_rdata_o.value))
    return out


async def _run(dut, mode: int) -> int:
    dut.mode_i.value = mode
    dut.start_i.value = 1
    guard = 0
    while int(dut.busy_o.value) == 0:
        await RisingEdge(dut.clk_i)
        guard += 1
        assert guard < MAX_CYCLES, "ntt_core_c1 never went busy after start_i"
    dut.start_i.value = 0
    cycles = 0
    while int(dut.done_o.value) == 0:
        await RisingEdge(dut.clk_i)
        cycles += 1
        assert cycles < MAX_CYCLES, "ntt_core_c1 did not assert done_o in time"
    return cycles


@cocotb.test()
async def test_ntt_bit_exact(dut):
    await _start_clock(dut)
    await _reset(dut)
    rng = random.Random(20)
    polys = _corner_polys() + [[rng.randrange(Q) for _ in range(N)] for _ in range(100)]
    for f in polys:
        await _load(dut, f)
        await _run(dut, 0)
        got = await _read_all(dut)
        assert got == ntt(f), f"NTT mismatch, first coeffs of input: {f[:4]}"


@cocotb.test()
async def test_intt_bit_exact(dut):
    await _start_clock(dut)
    await _reset(dut)
    rng = random.Random(21)
    polys = _corner_polys() + [[rng.randrange(Q) for _ in range(N)] for _ in range(100)]
    for f in polys:
        await _load(dut, f)
        await _run(dut, 1)
        got = await _read_all(dut)
        assert got == intt(f), f"INTT mismatch, first coeffs of input: {f[:4]}"


@cocotb.test()
async def test_ntt_intt_roundtrip(dut):
    await _start_clock(dut)
    await _reset(dut)
    rng = random.Random(22)
    for _ in range(50):
        f = [rng.randrange(Q) for _ in range(N)]
        await _load(dut, f)
        await _run(dut, 0)
        f_hat = await _read_all(dut)
        await _load(dut, f_hat)
        await _run(dut, 1)
        f_rt = await _read_all(dut)
        assert f_rt == f, "intt(ntt(f)) != f through the RTL"


@cocotb.test()
async def test_cycle_count_matches_c0_exactly(dut):
    """CRG-7 + Phase 2 PASS criterion ('measured stall cycles = 0 at L = 1'): C1's cycle count
    must equal C0's measured 897 (NTT) / 1153 (INTT) exactly, for every input, not merely be
    constant at some other value.
    """
    await _start_clock(dut)
    await _reset(dut)
    rng = random.Random(23)
    polys = _corner_polys() + [[rng.randrange(Q) for _ in range(N)] for _ in range(20)]

    fwd_cycles = set()
    for f in polys:
        await _load(dut, f)
        fwd_cycles.add(await _run(dut, 0))
    assert fwd_cycles == {C0_NTT_CYCLES}, (
        f"NTT cycle count changed vs C0: got {fwd_cycles}, expected {{{C0_NTT_CYCLES}}} "
        "(stall cycles introduced by the banked memory)"
    )

    inv_cycles = set()
    for f in polys:
        await _load(dut, f)
        inv_cycles.add(await _run(dut, 1))
    assert inv_cycles == {C0_INTT_CYCLES}, (
        f"INTT cycle count changed vs C0: got {inv_cycles}, expected {{{C0_INTT_CYCLES}}} "
        "(stall cycles introduced by the banked memory)"
    )

    print(f"cycles: NTT={fwd_cycles.pop()} (C0: {C0_NTT_CYCLES}) "
          f"INTT={inv_cycles.pop()} (C0: {C0_INTT_CYCLES})  stall cycles = 0")
