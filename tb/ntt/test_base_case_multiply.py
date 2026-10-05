"""tb/ntt/test_base_case_multiply.py — cocotb bit-exact test for
rtl/ntt/base_case_multiply.sv against tb/golden/primitives.py:base_case_multiply
(FIPS 203 Algorithm 12).

Corner cases and random coverage per
evidence/phase01/test_plan.md ("Unit: base_case_multiply").
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))

import cocotb
from cocotb.triggers import Timer
from params import Q
from primitives import _GAMMA, base_case_multiply


async def _check(dut, a0, a1, b0, b1, gamma):
    dut.a0_i.value = a0
    dut.a1_i.value = a1
    dut.b0_i.value = b0
    dut.b1_i.value = b1
    dut.gamma_i.value = gamma
    await Timer(1, unit="ns")
    c0_exp, c1_exp = base_case_multiply(a0, a1, b0, b1, gamma)
    c0_act, c1_act = int(dut.c0_o.value), int(dut.c1_o.value)
    assert (c0_act, c1_act) == (c0_exp, c1_exp), (
        f"a0={a0} a1={a1} b0={b0} b1={b1} gamma={gamma}: "
        f"expected ({c0_exp},{c1_exp}), got ({c0_act},{c1_act})"
    )


@cocotb.test()
async def test_base_case_multiply_corners(dut):
    m = Q - 1
    await _check(dut, 0, 0, 0, 0, 0)
    await _check(dut, m, m, m, m, m)
    await _check(dut, m, m, m, m, 0)
    await _check(dut, m, m, m, m, m)
    await _check(dut, 1, 0, 1, 0, _GAMMA[0])
    await _check(dut, 1, 0, 1, 0, _GAMMA[127])


@cocotb.test()
async def test_base_case_multiply_random(dut):
    rng = random.Random(1)
    for _ in range(500):
        gamma = rng.choice(_GAMMA)
        await _check(
            dut,
            rng.randrange(Q), rng.randrange(Q),
            rng.randrange(Q), rng.randrange(Q),
            gamma,
        )
