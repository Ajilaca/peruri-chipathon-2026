"""tb/ntt/test_butterfly.py - cocotb bit-exact test for rtl/ntt/butterfly.sv against the exact
per-butterfly step of tb/golden/primitives.py:ntt (forward, CT) and :intt (inverse, GS).

Corner cases and random coverage per evidence/phase01/test_plan.md
("Unit: butterfly").
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))

import cocotb
from cocotb.triggers import Timer
from params import Q
from primitives import _ZETA_BITREV


def _fwd(a, b, zeta):
    t = (zeta * b) % Q
    return (a + t) % Q, (a - t) % Q


def _inv(a, b, zeta):
    t = a
    return (t + b) % Q, (zeta * (b - t)) % Q


async def _check(dut, mode: int, a: int, b: int, zeta: int):
    dut.mode_i.value = mode
    dut.a_i.value = a
    dut.b_i.value = b
    dut.zeta_i.value = zeta
    await Timer(1, unit="ns")
    a_exp, b_exp = (_fwd if mode == 0 else _inv)(a, b, zeta)
    a_act, b_act = int(dut.a_o.value), int(dut.b_o.value)
    assert (a_act, b_act) == (a_exp, b_exp), (
        f"mode={mode} a={a} b={b} zeta={zeta}: expected ({a_exp},{b_exp}), "
        f"got ({a_act},{b_act})"
    )


@cocotb.test()
async def test_butterfly_corners(dut):
    m = Q - 1
    zmax = max(_ZETA_BITREV)
    for mode in (0, 1):
        for a, b, zeta in [
            (0, 0, 1), (m, m, 1), (0, m, 1), (m, 0, 1),
            (0, 0, zmax), (m, m, zmax),
        ]:
            await _check(dut, mode, a, b, zeta)


@cocotb.test()
async def test_butterfly_random(dut):
    rng = random.Random(2)
    for mode in (0, 1):
        for _ in range(1000):
            zeta = rng.choice(_ZETA_BITREV)
            await _check(dut, mode, rng.randrange(Q), rng.randrange(Q), zeta)
