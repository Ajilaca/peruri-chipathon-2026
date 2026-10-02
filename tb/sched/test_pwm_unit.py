"""tb/sched/test_pwm_unit.py -- Phase 6 test plan V4: rtl/sched/pwm_unit.sv against the golden BaseCaseMultiply (FIPS 203 Algorithm 12) plus accumulation,
latency 7, corner pairs and random pairs, streaming one pair per cycle."""
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from params import Q
from primitives import _GAMMA, base_case_multiply

LAT = 7
NRAND = int(os.environ.get("PWM_NRAND", "20000"))


def _vectors():
    m = Q - 1
    v = []
    for g in (_GAMMA[0], _GAMMA[63], _GAMMA[64], _GAMMA[127], 0, 1, m):
        for t in ((0, 0, 0, 0, 0, 0), (m, m, m, m, m, m), (m, 0, m, 0, m, 0), (0, m, 0, m, 0, m), (1, 1, 1, 1, 1, 1)):
            v.append(t[:4] + (g,) + t[4:])
    rng = random.Random(61)
    for _ in range(NRAND):
        v.append(tuple(rng.randrange(Q) for _ in range(4)) + (rng.choice(_GAMMA),) + (rng.randrange(Q), rng.randrange(Q)))
    return v


@cocotb.test()
async def test_pwm_stream(dut):
    cocotb.start_soon(Clock(dut.clk_i, 10, unit="ns").start())
    vec = _vectors()
    exp = []
    for a0, a1, b0, b1, g, c0, c1 in vec:
        p0, p1 = base_case_multiply(a0, a1, b0, b1, g)
        exp.append(((c0 + p0) % Q, (c1 + p1) % Q))
    got = []
    for i in range(len(vec) + LAT):
        await FallingEdge(dut.clk_i)
        if i >= LAT:
            got.append((int(dut.c0_o.value), int(dut.c1_o.value)))
        a0, a1, b0, b1, g, c0, c1 = vec[min(i, len(vec) - 1)]
        dut.a0_i.value, dut.a1_i.value, dut.b0_i.value, dut.b1_i.value = a0, a1, b0, b1
        dut.gamma_i.value, dut.acc0_i.value, dut.acc1_i.value = g, c0, c1
    # inputs driven at falling edge i are taken at the next rising edge; LAT = 7 registers later the result is visible at falling edge i + LAT
    bad = [k for k in range(len(vec)) if got[k] != exp[k]]
    dut._log.info(f"pwm_unit: {len(vec) - len(bad)}/{len(vec)} pairs equal to BaseCaseMultiply + accumulate")
    assert not bad, f"{len(bad)} mismatches, first at {bad[0]}: got {got[bad[0]]} expected {exp[bad[0]]}"
