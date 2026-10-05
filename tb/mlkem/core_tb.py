"""tb/mlkem/core_tb.py -- shared helpers of the Phase 9c core tests (evidence/phase09/9c/test_plan_9c.md).

Same cycle model as the 9a / 9b drivers: inputs are written at the falling edge; a host read address set at a falling edge gives its data at the next falling edge (the memories read synchronously).
Toplevel: rtl/mlkem/mlkem_core.sv. Regions: 0 KB, 1 CB, 2 CB2, 3 RF; register file words: d 0-3, z 4-7, m 8-11, rho 12-15, sigma 16-19, K 20-23, K_bar 24-27, H 28-31.
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge
from fetch_acvp_vectors import dest_path

KB, CB, CB2, RF = 0, 1, 2, 3
R_D, R_Z, R_M, R_K = 0, 4, 8, 20
LIMIT = 200000
FAST = os.environ.get("CORE_FAST", "0") == "1"      # controls: a few vectors only
NRAND = int(os.environ.get("CORE_N", "20"))


async def setup(dut):
    cocotb.start_soon(Clock(dut.clk_i, 10, unit="ns").start())
    dut.rst_ni.value = 0
    for n in ("op_i", "start_i", "h_we_i", "h_addr_i", "h_wdata_i"):
        getattr(dut, n).value = 0
    await ClockCycles(dut.clk_i, 4)
    await FallingEdge(dut.clk_i)
    dut.rst_ni.value = 1
    await ClockCycles(dut.clk_i, 2)
    await FallingEdge(dut.clk_i)


async def write_words(dut, region, word0, data: bytes):
    assert len(data) % 8 == 0
    for i in range(len(data) // 8):
        await FallingEdge(dut.clk_i)
        dut.h_we_i.value = 1
        dut.h_addr_i.value = (region << 10) | (word0 + i)
        dut.h_wdata_i.value = int.from_bytes(data[8 * i: 8 * i + 8], "little")
    await FallingEdge(dut.clk_i)
    dut.h_we_i.value = 0


async def read_words(dut, region, word0, n) -> bytes:
    out = bytearray()
    prev = False
    for i in range(n + 1):
        await FallingEdge(dut.clk_i)
        if prev:
            out += int(dut.h_rdata_o.value).to_bytes(8, "little")
        if i < n:
            dut.h_addr_i.value = (region << 10) | (word0 + i)
            prev = True
    return bytes(out)


async def run_op(dut, op, hook=None):
    """Starts operation op and waits for done_o. Returns the cycle count (falling edges from the one after the start cycle to the one that shows done_o).
    hook(cycle) is called every cycle (to disturb the core in the protocol tests)."""
    await FallingEdge(dut.clk_i)
    dut.op_i.value = op
    dut.start_i.value = 1
    await FallingEdge(dut.clk_i)
    dut.start_i.value = 0
    cycles = 0
    for _ in range(LIMIT):
        await FallingEdge(dut.clk_i)
        cycles += 1
        if hook is not None:
            hook(cycles)
        if int(dut.done_o.value):
            break
    else:
        raise AssertionError("done_o did not rise")
    await FallingEdge(dut.clk_i)
    assert int(dut.busy_o.value) == 0 and int(dut.done_o.value) == 0, "busy_o or done_o still high after the done pulse"
    return cycles


def load(subdir):
    return json.loads(dest_path(subdir).read_text())


def acvp_tests(subdir, function=None):
    doc = load(subdir)
    out = []
    for tg in doc["testGroups"]:
        if tg["parameterSet"] != "ML-KEM-768" or (function and tg.get("function") != function):
            continue
        out += tg["tests"]
    return out


async def rtl_keygen(dut, d: bytes, z: bytes):
    await write_words(dut, RF, R_D, d)
    await write_words(dut, RF, R_Z, z)
    cyc = await run_op(dut, 0)
    dk = await read_words(dut, KB, 0, 300)
    return dk[1152:2336], dk, cyc


async def rtl_encaps(dut, ek: bytes, m: bytes):
    await write_words(dut, KB, 144, ek)
    await write_words(dut, RF, R_M, m)
    cyc = await run_op(dut, 1)
    c = await read_words(dut, CB, 0, 136)
    k = await read_words(dut, RF, R_K, 4)
    return k, c, cyc


async def rtl_decaps(dut, dk: bytes, c: bytes):
    await write_words(dut, KB, 0, dk)
    await write_words(dut, CB, 0, c)
    cyc = await run_op(dut, 2)
    k = await read_words(dut, RF, R_K, 4)
    return k, cyc
