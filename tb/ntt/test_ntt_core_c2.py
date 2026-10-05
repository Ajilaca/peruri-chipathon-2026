"""tb/ntt/test_ntt_core_c2.py - cocotb bit-exact regression for rtl/ntt/ntt_core_c2.sv
(configuration C2: multi-lane NTT/INTT, NUM_LANES in {1,2,4,8}) against
tb/golden/primitives.py.

Per evidence/phase03/test_plan.md ("Unit: ntt_core_c2 lane datapath"): bit-exact
correctness must hold for every L; cycle count is measured and required constant *within* a
given L (not assumed equal to C0/C1) except at L=1, where the schedule collapses to the exact
same t/p sequence as C0/C1 and must reproduce their measured 897 (NTT) / 1153 (INTT) cycles
exactly. `bank_overflow_o` (rtl/mem/poly_mem_multiport.sv) must never assert for any L -- that is
the runtime check that the proof in
evidence/phase03/lane_schedule_verification.txt actually holds for the
RTL, not just for the Python model.

NUM_LANES comes from the NTT_C2_L environment variable (cocotb build-time parameters are set per
simulation run; see tb/ntt/run_ntt_c2_tests.py, which builds this module once per L).
"""

import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge, Timer
from params import N, Q
from primitives import intt, ntt

NUM_LANES = int(os.environ.get("NTT_C2_L", "1"))

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
        assert int(dut.bank_overflow_o.value) == 0, f"bank_overflow_o asserted during load, addr={addr}"
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
        assert guard < MAX_CYCLES, "ntt_core_c2 never went busy after start_i"
    dut.start_i.value = 0
    cycles = 0
    while int(dut.done_o.value) == 0:
        assert int(dut.bank_overflow_o.value) == 0, f"bank_overflow_o asserted mid-run at cycle {cycles}"
        await RisingEdge(dut.clk_i)
        cycles += 1
        assert cycles < MAX_CYCLES, "ntt_core_c2 did not assert done_o in time"
    return cycles


@cocotb.test()
async def test_ntt_bit_exact(dut):
    await _start_clock(dut)
    await _reset(dut)
    rng = random.Random(30)
    polys = _corner_polys() + [[rng.randrange(Q) for _ in range(N)] for _ in range(100)]
    for f in polys:
        await _load(dut, f)
        await _run(dut, 0)
        got = await _read_all(dut)
        assert got == ntt(f), f"NTT mismatch (L={NUM_LANES}), first coeffs of input: {f[:4]}"


@cocotb.test()
async def test_intt_bit_exact(dut):
    await _start_clock(dut)
    await _reset(dut)
    rng = random.Random(31)
    polys = _corner_polys() + [[rng.randrange(Q) for _ in range(N)] for _ in range(100)]
    for f in polys:
        await _load(dut, f)
        await _run(dut, 1)
        got = await _read_all(dut)
        assert got == intt(f), f"INTT mismatch (L={NUM_LANES}), first coeffs of input: {f[:4]}"


@cocotb.test()
async def test_ntt_intt_roundtrip(dut):
    await _start_clock(dut)
    await _reset(dut)
    rng = random.Random(32)
    for _ in range(50):
        f = [rng.randrange(Q) for _ in range(N)]
        await _load(dut, f)
        await _run(dut, 0)
        f_hat = await _read_all(dut)
        await _load(dut, f_hat)
        await _run(dut, 1)
        f_rt = await _read_all(dut)
        assert f_rt == f, f"intt(ntt(f)) != f through the RTL (L={NUM_LANES})"


@cocotb.test()
async def test_cycle_count_constant(dut):
    """CRG-7: cycle count from start_i to done_o must be identical for every input, in a given
    direction, at this L (no data-dependent stall). At L=1 it must additionally equal C0/C1's
    measured 897 (NTT) / 1153 (INTT) exactly -- the schedule collapses to the same t/p sequence.
    """
    await _start_clock(dut)
    await _reset(dut)
    rng = random.Random(33)
    polys = _corner_polys() + [[rng.randrange(Q) for _ in range(N)] for _ in range(20)]

    fwd_cycles = set()
    for f in polys:
        await _load(dut, f)
        fwd_cycles.add(await _run(dut, 0))
    assert len(fwd_cycles) == 1, f"NTT cycle count not constant at L={NUM_LANES}: {fwd_cycles}"

    inv_cycles = set()
    for f in polys:
        await _load(dut, f)
        inv_cycles.add(await _run(dut, 1))
    assert len(inv_cycles) == 1, f"INTT cycle count not constant at L={NUM_LANES}: {inv_cycles}"

    fwd = fwd_cycles.pop()
    inv = inv_cycles.pop()

    if NUM_LANES == 1:
        assert fwd == C0_NTT_CYCLES, f"L=1 NTT cycles {fwd} != C0's {C0_NTT_CYCLES}"
        assert inv == C0_INTT_CYCLES, f"L=1 INTT cycles {inv} != C0's {C0_INTT_CYCLES}"

    print(f"L={NUM_LANES} cycles: NTT={fwd} INTT={inv}")
