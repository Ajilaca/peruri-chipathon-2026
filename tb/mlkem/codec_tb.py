"""tb/mlkem/codec_tb.py -- shared helpers of the Phase 9a codec tests (docs/evidence/phase09-integration/9a/test_plan_9a.md).

Cycle model of the drivers (as Phase 8b): inputs are written at the falling edge, the combinational outputs are read 1 ns later, and the values read are the ones the next rising edge samples.
Toplevel: rtl/mlkem/mlkem_codec_top.sv (packer p_*, unpacker u_*, side by side), or with CT_W=2 rtl/mlkem/mlkem_codec2_top.sv (Phase 9M, two bytes per beat, byte 2i in bits 7:0; test_plan_9m1.md V2).
"""
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, Timer
from params import N, Q

NCASES = int(os.environ.get("CT_N", "40"))
W = int(os.environ.get("CT_W", "1"))     # bytes per beat of the byte port (1: Phase 9a codec, 2: Phase 9M codec2)
LIMIT = 4000
DSEL = {1: 0, 4: 1, 10: 2, 12: 3}


def val(sig):
    """Integer value of a signal, -1 when it is not fully 0/1 (an unreset data register that is not valid yet)."""
    v = sig.value
    return int(v) if v.is_resolvable else -1


class Pattern:
    """Per-cycle valid / ready pattern: 'always', 'rand' (p = 0.5), 'runs' (low runs of 1, 2, 7 or 40 cycles at random points)."""

    def __init__(self, mode, rng):
        self.mode, self.rng, self.low = mode, rng, 0

    def __call__(self):
        if self.mode == "always":
            return 1
        if self.mode == "rand":
            return int(self.rng.random() < 0.5)
        if self.low > 0:
            self.low -= 1
            return 0
        if self.rng.random() < 0.04:
            self.low = self.rng.choice([1, 2, 7, 40]) - 1
            return 0
        return 1


MODES = ("always", "rand", "runs")


async def clock_reset(dut):
    cocotb.start_soon(Clock(dut.clk_i, 10, unit="ns").start())
    dut.rst_ni.value = 0
    for n in ("p_start_i", "p_dsel_i", "p_coef_valid_i", "p_coef_data_i", "p_byte_ready_i", "u_start_i", "u_dsel_i", "u_byte_valid_i", "u_byte_data_i", "u_coef_ready_i"):
        getattr(dut, n).value = 0
    await ClockCycles(dut.clk_i, 3)
    await FallingEdge(dut.clk_i)
    dut.rst_ni.value = 1


async def idle(dut, n=3):
    await ClockCycles(dut.clk_i, n)
    await FallingEdge(dut.clk_i)


async def pack_run(dut, d, poly, rng, sink="always", src="always", start_noise=False):
    """One packer run. Returns dict: bytes, cycles (falling edges from the start cycle to done_o), accepted (coefficients), last_at (index of the byte with byte_last_o), done (pulses seen)."""
    await FallingEdge(dut.clk_i)
    dut.p_start_i.value = 1
    dut.p_dsel_i.value = DSEL[d]
    await FallingEdge(dut.clk_i)
    dut.p_start_i.value = 1 if start_noise else 0          # a start while busy must be ignored
    if start_noise:
        dut.p_dsel_i.value = DSEL[4 if d != 4 else 10]      # a dsel change while busy must be ignored too
    sink_p, src_p = Pattern(sink, rng), Pattern(src, rng)
    out, idx, last_at, done, cycles, prev = bytearray(), 0, [], 0, 0, None
    for _ in range(LIMIT):
        cycles += 1
        v = int(src_p())
        dut.p_coef_valid_i.value = v
        dut.p_coef_data_i.value = poly[idx] if idx < N else rng.randrange(4096)
        r = sink_p()
        dut.p_byte_ready_i.value = r
        await Timer(1, "ns")
        cr, bv, bd, bl = int(dut.p_coef_ready_o.value), int(dut.p_byte_valid_o.value), val(dut.p_byte_data_o), int(dut.p_byte_last_o.value)
        if prev is not None and prev[0] and not prev[3]:
            assert bv and bd == prev[1] and bl == prev[2], "byte output not held while byte_ready_i was low"
        prev = (bv, bd, bl, r)
        if v and cr:
            idx += 1
        assert bd != -1 or not bv, "valid byte with an unresolved value"
        if bv and r:
            out.extend(bd.to_bytes(W, "little"))
            if bl:
                last_at.append(len(out) - 1)
        if int(dut.p_done_o.value):
            done += 1
            break
        await FallingEdge(dut.clk_i)
    dut.p_coef_valid_i.value = 0
    dut.p_byte_ready_i.value = 0
    dut.p_start_i.value = 0
    return {"bytes": bytes(out), "cycles": cycles, "accepted": idx, "last_at": last_at, "done": done}


async def unpack_run(dut, d, data, rng, sink="always", src="always", start_noise=False):
    """One unpacker run. Returns dict: coefs, cycles, accepted (bytes), last_at (index of the coefficient with coef_last_o), done."""
    await FallingEdge(dut.clk_i)
    dut.u_start_i.value = 1
    dut.u_dsel_i.value = DSEL[d]
    await FallingEdge(dut.clk_i)
    dut.u_start_i.value = 1 if start_noise else 0
    if start_noise:
        dut.u_dsel_i.value = DSEL[4 if d != 4 else 10]
    sink_p, src_p = Pattern(sink, rng), Pattern(src, rng)
    out, idx, last_at, done, cycles, prev = [], 0, [], 0, 0, None
    for _ in range(LIMIT):
        cycles += 1
        v = int(src_p())
        dut.u_byte_valid_i.value = v
        dut.u_byte_data_i.value = int.from_bytes(data[idx:idx + W], "little") if idx < len(data) else rng.randrange(256 ** W)
        r = sink_p()
        dut.u_coef_ready_i.value = r
        await Timer(1, "ns")
        br, cv, cd, cl = int(dut.u_byte_ready_o.value), int(dut.u_coef_valid_o.value), val(dut.u_coef_data_o), int(dut.u_coef_last_o.value)
        if prev is not None and prev[0] and not prev[3]:
            assert cv and cd == prev[1] and cl == prev[2], "coefficient output not held while coef_ready_i was low"
        prev = (cv, cd, cl, r)
        if v and br:
            idx += W
        assert cd != -1 or not cv, "valid coefficient with an unresolved value"
        if cv and r:
            out.append(cd)
            if cl:
                last_at.append(len(out) - 1)
        if int(dut.u_done_o.value):
            done += 1
            break
        await FallingEdge(dut.clk_i)
    dut.u_byte_valid_i.value = 0
    dut.u_coef_ready_i.value = 0
    dut.u_start_i.value = 0
    return {"coefs": out, "cycles": cycles, "accepted": idx, "last_at": last_at, "done": done}


def special_polys():
    rng = random.Random(910)
    yield "zero", [0] * N
    yield "max", [Q - 1] * N
    yield "alt", [0 if i % 2 else Q - 1 for i in range(N)]
    yield "ramp", [i * 13 % Q for i in range(N)]
    yield "ties", [(Q + 1) // 2 + (i % 3) - 1 for i in range(N)]
    for k in range(NCASES):
        yield f"rand{k}", [rng.randrange(Q) for _ in range(N)]
