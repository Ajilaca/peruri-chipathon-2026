"""tb/phase5m/test_m6_basis.py - Phase 5M S6, test plan V6: the core's INTT (no scaling pass, halving in every layer) for the 256 unit
vectors e_i and the 256 vectors (q-1) * e_i equals BOTH the FIPS 203 intt() (golden, with the final 3303 multiplication) and
intt_halving() (golden model of the halved algorithm). Uses the Phase 4 helpers of tb/ntt/test_ntt_core_c3.py unchanged
(same environment variables: C3_RDLAT, C3_WRDLY, C3_CORE, C3_CYCLES_OUT)."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0] / "ntt"))
sys.path.insert(0, str(HERE.parents[0] / "golden"))
sys.path.insert(0, str(HERE.parents[0] / "mem"))

import cocotb
from intt_halving import intt_halving
from params import N, Q
from primitives import intt
from test_ntt_core_c3 import _check_scoreboard, _setup, _transform


@cocotb.test()
async def test_intt_unit_vectors(dut):
    sb = await _setup(dut)
    n_ok = 0
    for i in range(N):
        for scale in (1, Q - 1):
            f = [0] * N
            f[i] = scale
            got, _ = await _transform(dut, f, 1)
            ref = intt(f)
            assert got == ref, f"INTT of {scale}*e_{i} differs from intt()"
            assert got == intt_halving(f), f"INTT of {scale}*e_{i} differs from intt_halving()"
            n_ok += 1
    dut._log.info(f"INTT unit vectors: {n_ok}/{2 * N} equal to intt() and intt_halving()")
    _check_scoreboard(sb)
