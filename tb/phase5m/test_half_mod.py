"""tb/phase5m/test_half_mod.py — Phase 5M S6, test plan V2: rtl/arith/half_mod.sv for EVERY x in [0, q): y < q and 2*y = x (mod q),
and y equals the golden half_mod (tb/golden/intt_halving.py). The toplevel is half_mod; the same test is run against a mutant
(negative control) and must FAIL there."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))

import cocotb
from cocotb.triggers import Timer
from intt_halving import half_mod
from params import Q


@cocotb.test()
async def test_half_mod_exhaustive(dut):
    bad = []
    for x in range(Q):
        dut.x_i.value = x
        await Timer(1, unit="ns")
        y = int(dut.y_o.value)
        if not (y < Q and (2 * y) % Q == x and y == half_mod(x)):
            bad.append((x, y))
    dut._log.info(f"half_mod: {Q - len(bad)}/{Q} inputs correct")
    assert not bad, f"{len(bad)} wrong results, first {bad[:3]}"
