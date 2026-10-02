"""tb/phase5m/test_poly_mem_diff.py -- Phase 5M S7 test V3: with RD_SPLIT = 0 the new memory (rtl/mem/poly_mem_multiport_split.sv) equals the frozen
rtl/mem/poly_mem_multiport_pipe.sv on every output in every cycle, for random request streams (including three ports on one bank, which raises the
overflow flag in both) and random write data. Toplevel: tb/phase5m/mem_diff_top.sv."""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, Timer


@cocotb.test()
async def test_equal_to_frozen_memory(dut):
    cocotb.start_soon(Clock(dut.clk_i, 10, unit="ns").start())
    dut.rst_ni.value = 0
    dut.en_i.value = 0
    dut.wr_i.value = 0
    dut.addr_i.value = 0
    dut.wdata_i.value = 0
    await ClockCycles(dut.clk_i, 3)
    await FallingEdge(dut.clk_i)
    dut.rst_ni.value = 1
    rng = random.Random(70)
    diffs = []
    n = 6000
    for c in range(n):
        await FallingEdge(dut.clk_i)
        en = rng.getrandbits(16) if rng.random() < 0.8 else 0
        wr = rng.getrandbits(16)
        dut.en_i.value = en
        dut.wr_i.value = wr
        dut.addr_i.value = rng.getrandbits(128)
        dut.wdata_i.value = rng.getrandbits(192)
        await Timer(1, unit="ns")
        for a, b, name in ((dut.rdata_a_o, dut.rdata_b_o, "rdata"), (dut.ovf_a_o, dut.ovf_b_o, "overflow")):
            if str(a.value) != str(b.value):
                diffs.append((c, name))
    dut._log.info(f"differential: {n} cycles, {len(diffs)} differences")
    assert not diffs, f"{len(diffs)} differences, first {diffs[:3]}"
