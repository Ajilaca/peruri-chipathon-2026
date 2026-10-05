"""Toolchain smoke test: proves cocotb can drive the chosen simulator.
Checks the DUT against a Python reference model. Not project verification."""
import random

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge


@cocotb.test()
async def counter_matches_model(dut):
    width = len(dut.count)
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    dut.rst_n.value = 0
    dut.en.value = 0
    for _ in range(2):
        await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1
    model = 0
    rng = random.Random(2026)
    for cycle in range(300):
        en = rng.randint(0, 1)
        dut.en.value = en          # drive on falling edge
        await FallingEdge(dut.clk)  # one rising edge has passed; sample mid-cycle
        if en:
            model = (model + 1) % (1 << width)
        got = int(dut.count.value)
        assert got == model, f"cycle {cycle}: dut={got} model={model}"
    dut._log.info("smoke: 300 cycles matched the Python model")
