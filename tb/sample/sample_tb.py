"""tb/sample/sample_tb.py -- shared helpers of the Phase 8b sampler tests (docs/evidence/phase08-keccak-stream/8b/test_plan_8b.md).

Cycle model of the drivers: inputs are written at the falling edge, the combinational outputs are read 1 ns later (they settle), and the values read are the ones the next rising edge samples.
Output beats hold OUTW coefficients (env KS_OUTW, default 1): lane k of a beat is bits [12k+11:12k], lane 0 is the lower coefficient index.
"""
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))

import cocotb
import sampler_model as M
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, Timer
from params import N, Q

OUTW = int(os.environ.get("KS_OUTW", "1"))
NCASES = int(os.environ.get("KS_N", "500"))
LIMIT = 6000


def triple(d1, d2):
    """Three stream bytes that give the candidates d1 and d2 (12 bit each)."""
    return bytes([d1 & 255, ((d1 >> 8) & 15) | ((d2 & 15) << 4), d2 >> 4])


def words_of(stream: bytes, nwords: int, rng):
    """64-bit little-endian words of the stream, padded with random words up to nwords (more words than the sampler may take)."""
    stream = stream + bytes(rng.randrange(256) for _ in range(8 * nwords - len(stream)))
    return [int.from_bytes(stream[8 * i: 8 * i + 8], "little") for i in range(nwords)]


def lanes(value):
    return [(value >> (12 * k)) & 0xFFF for k in range(OUTW)]


class Ready:
    """coef_ready_i pattern per cycle: 'always', 'rand' (p = 0.5) or 'runs' (low runs of 1, 2, 7 or 40 cycles at random points)."""

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


async def clock_reset(dut, init):
    cocotb.start_soon(Clock(dut.clk_i, 10, unit="ns").start())
    dut.rst_ni.value = 0
    for k, v in init.items():
        getattr(dut, k).value = v
    await ClockCycles(dut.clk_i, 3)
    await FallingEdge(dut.clk_i)
    dut.rst_ni.value = 1


class Monitor:
    """Collects coefficient beats, checks that an unaccepted output is held, counts done_o pulses."""

    def __init__(self):
        self.beats, self.lasts, self.done, self.prev = [], [], 0, None

    def sample(self, dut, go_out):
        cv, cd, cl = int(dut.coef_valid_o.value), int(dut.coef_data_o.value), int(dut.coef_last_o.value)
        if self.prev is not None and self.prev[0] and not self.prev[3]:
            assert cv and cd == self.prev[1] and cl == self.prev[2], "output not held while coef_ready_i was low"
        self.prev = (cv, cd, cl, go_out)
        if cv and go_out:
            self.beats.append(cd)
            if cl:
                self.lasts.append(len(self.beats))
        if int(dut.done_o.value):
            self.done += 1
        return cv

    def coefs(self):
        out = []
        for b in self.beats:
            out += lanes(b)
        return out


def check_poly(mon, expect, what):
    got = mon.coefs()
    assert len(got) == N, f"{what}: {len(got)} coefficients"
    assert got == expect, f"{what}: coefficients differ at index {next(i for i in range(N) if got[i] != expect[i])}"
    assert mon.lasts == [len(mon.beats)], f"{what}: coef_last_o on beats {mon.lasts}, {len(mon.beats)} beats"
    assert mon.done == 1, f"{what}: done_o pulsed {mon.done} times"
    assert all(0 <= c < Q for c in got)
