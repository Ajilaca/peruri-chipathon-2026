"""tb/ntt/test_modmul.py — cocotb bit-exact test for rtl/ntt/modmul_reduce.sv.

Corner cases and random coverage per evidence/phase01/test_plan.md
("Unit: modmul_reduce"). Reference: plain Python (a*b) % Q, not tb/golden directly (modmul_reduce
has no golden-model counterpart function of its own — it implements the inner "zeta * f[...]"
step used throughout Algorithms 9-12), but Q is imported from tb/golden/params.py so the modulus
itself is never retyped.
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))

import cocotb
from cocotb.triggers import Timer
from params import Q


async def _check(dut, a: int, b: int):
    dut.a_i.value = a
    dut.b_i.value = b
    await Timer(1, unit="ns")
    expected = (a * b) % Q
    actual = int(dut.p_o.value)
    assert actual == expected, f"a={a} b={b}: expected {expected}, got {actual}"


@cocotb.test()
async def test_modmul_corners(dut):
    for a, b in [(0, 0), (Q - 1, Q - 1), (1, 0), (1, Q - 1), (Q - 1, 1)]:
        await _check(dut, a, b)


@cocotb.test()
async def test_modmul_random(dut):
    rng = random.Random(0)
    for _ in range(2000):
        await _check(dut, rng.randrange(Q), rng.randrange(Q))
