"""tb/ntt/test_ntt_core.py — cocotb bit-exact test for rtl/ntt/ntt_core.sv against
tb/golden/primitives.py (`ntt`, `intt`), plus the constant-cycle check (CRG-7).

Corner cases and counts per docs/evidence/phase01-ntt-baseline/test_plan.md
("Unit: ntt_core"). No RTL was optimised or the test weakened to make this pass.
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
MAX_CYCLES = 5000  # generous timeout; the real run is ~900-1150 cycles


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
    """Starts the core and waits for done_o. Returns the cycle count from the core actually
    going busy to done (so it does not depend on how many cycles start_i needed to be held).

    start_i is held until busy_o is observed high rather than pulsed for exactly one cycle:
    a value written to a signal from a running coroutine is only visible to the RTL from the
    *next* clock edge onward (a cocotb/VPI write-timing property, not a testbench choice), so a
    single-cycle pulse dropped immediately after one `await RisingEdge` can be removed again
    before the FSM ever samples it as 1. Holding it until busy_o rises sidesteps that race
    instead of depending on precise timing.
    """
    dut.mode_i.value = mode
    dut.start_i.value = 1
    guard = 0
    while int(dut.busy_o.value) == 0:
        await RisingEdge(dut.clk_i)
        guard += 1
        assert guard < MAX_CYCLES, "ntt_core never went busy after start_i"
    dut.start_i.value = 0
    cycles = 0
    while int(dut.done_o.value) == 0:
        await RisingEdge(dut.clk_i)
        cycles += 1
        assert cycles < MAX_CYCLES, "ntt_core did not assert done_o in time"
    return cycles


@cocotb.test()
async def test_ntt_bit_exact(dut):
    await _start_clock(dut)
    await _reset(dut)
    rng = random.Random(10)
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
    rng = random.Random(11)
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
    rng = random.Random(12)
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
async def test_constant_cycle_count(dut):
    """CRG-7: identical cycle count for every input, in each direction separately."""
    await _start_clock(dut)
    await _reset(dut)
    rng = random.Random(13)
    polys = _corner_polys() + [[rng.randrange(Q) for _ in range(N)] for _ in range(20)]

    fwd_cycles = set()
    for f in polys:
        await _load(dut, f)
        fwd_cycles.add(await _run(dut, 0))
    assert len(fwd_cycles) == 1, f"NTT cycle count not constant: {fwd_cycles}"

    inv_cycles = set()
    for f in polys:
        await _load(dut, f)
        inv_cycles.add(await _run(dut, 1))
    assert len(inv_cycles) == 1, f"INTT cycle count not constant: {inv_cycles}"

    print(f"cycles: NTT={fwd_cycles.pop()} INTT={inv_cycles.pop()}")
