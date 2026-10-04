"""tb/mlkem/test_profile_core.py -- Phase 9M profile (docs/evidence/phase09m-optimisation/profile_2026-10-04.md): cycles of rtl/mlkem/mlkem_core.sv per controller state and per micro-operation for one KeyGen, Encaps and Decaps
with fixed inputs (d = 00..1f, z = 20..3f, m = 40..5f). The cycle of each micro-operation is counted from the controller's program counter and state at every falling edge inside run_op. Environment: PROF_OUT (json path).
Simulation only; the outputs are not checked here (tb/mlkem/test_mlkem_core.py does that)."""
import json
import os
from collections import defaultdict

import cocotb
import core_tb
import mlkem_ctl_model as CM
from core_tb import rtl_decaps, rtl_encaps, rtl_keygen, setup

NAMES = ["IDLE", "FETCH", "DISP", "LDP", "STP", "HFD", "HGT", "SDL", "RUN", "WR32", "RD32", "CMP", "CMPK", "RUNJ"]   # RUNJ: mlkem_core4 (Phase 9I item 4)


@cocotb.test()
async def test_profile(dut):
    await setup(dut)
    res, cur = {}, {}
    orig = core_tb.run_op

    async def run_op_prof(dut_, op, hook=None):
        by_pc, by_st = defaultdict(int), defaultdict(int)

        def h(_):
            by_pc[int(dut_.pc_q.value)] += 1
            by_st[NAMES[int(dut_.state_q.value)]] += 1
        cyc = await orig(dut_, op, h)
        cur.update(pc=dict(by_pc), st=dict(by_st), cyc=cyc)
        return cyc

    core_tb.run_op = run_op_prof
    d, z, m = bytes(range(32)), bytes(range(32, 64)), bytes(range(64, 96))
    ek, dk, _ = await rtl_keygen(dut, d, z)
    res["keygen"] = dict(cur)
    _, c, _ = await rtl_encaps(dut, ek, m)
    res["encaps"] = dict(cur)
    await rtl_decaps(dut, dk[:2400], c)
    res["decaps"] = dict(cur)
    core_tb.run_op = orig
    out = {n: {"cycles": r["cyc"], "by_state": r["st"], "by_pc": [[pc, " ".join(map(str, CM.PROGRAMS[n][pc])), k] for pc, k in sorted(r["pc"].items())]} for n, r in res.items()}
    with open(os.environ["PROF_OUT"], "w") as f:
        json.dump(out, f, indent=1)
