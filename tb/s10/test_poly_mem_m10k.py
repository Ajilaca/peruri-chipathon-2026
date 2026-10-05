"""tb/s10/test_poly_mem_m10k.py -- S10 test V2 (evidence/phase06/test_plan_s10.md): a copy of the S7 memory test tb/phase5m/test_poly_mem_split.py for
rtl/mem/poly_mem_m10k.sv (16 banks, one port per bank per cycle), NUM_LANES = 8, against a cycle-accurate Python model:

    request at cycle c -> storage physically read at c (the RAM takes the address at the end of the request cycle) -> rdata_o at c + RD_LAT
    write of that request (if requested) lands at the end of c + RD_LAT + WR_DELAY, write data presented by the caller in that cycle
    bank_overflow_o (two or more ports on one bank) is flagged one cycle after the request
Differences from the S7 test, nothing else: the latencies above, the initialisation of the scheduled-traffic test through one port per cycle (two consecutive addresses share a
bank in the 16-bank map), and the overflow test with two ports on one bank. RD_LAT / WR_DELAY come from P10_RD_LAT / P10_WR_DELAY.
"""

import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "mem"))

import cocotb
from bank_model import addr_pair, lane_p
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, Timer
from params import Q

L = 8
NP = 2 * L
AW, CW = 8, 12
RD_LAT = int(os.environ.get("P10_RD_LAT", "2"))
WR_DELAY = int(os.environ.get("P10_WR_DELAY", "0"))
PIPE = RD_LAT + WR_DELAY
OVF_LAT = 1


def bank16(a):
    return ((((a >> 1) ^ (a >> 2) ^ (a >> 3) ^ (a >> 4)) & 1) << 3) | ((a >> 5) & 7)


class Bench:
    """Drives one request set per cycle and checks every read against the model."""

    def __init__(self, dut):
        self.dut = dut
        self.mem = {}          # address -> value, as of the current cycle (None = never written)
        self.snap = []         # snap[c] = copy of mem BEFORE the landing of cycle c (what a physical read in cycle c sees)
        self.hist = []         # request sets, index = cycle
        self.reads_checked = 0
        self.ovf_cycles = set()   # request cycles that put three ports on one bank (deliberately)

    async def reset(self):
        d = self.dut
        cocotb.start_soon(Clock(d.clk_i, 10, unit="ns").start())
        d.rst_ni.value = 0
        d.en_i.value = 0
        d.wr_i.value = 0
        d.addr_i.value = 0
        d.wdata_i.value = 0
        await ClockCycles(d.clk_i, 3)
        await FallingEdge(d.clk_i)
        d.rst_ni.value = 1

    async def cycle(self, reqs, expect_overflow=False):
        """reqs: list of (port, addr, wr, wdata). One clock cycle."""
        d = self.dut
        await FallingEdge(d.clk_i)
        c = len(self.hist)
        self.hist.append(reqs)
        if expect_overflow:
            self.ovf_cycles.add(c)
        en = wr = addr = 0
        for p, a, w, _ in reqs:
            en |= 1 << p
            wr |= (1 if w else 0) << p
            addr |= a << (p * AW)
        d.en_i.value = en
        d.wr_i.value = wr
        d.addr_i.value = addr
        self.snap.append(dict(self.mem))
        landing = self.hist[c - PIPE] if c >= PIPE else []
        wdata = 0
        for p, _, w, v in landing:
            if w:
                wdata |= v << (p * CW)
        d.wdata_i.value = wdata
        await Timer(1, unit="ns")
        # read stage: the requests of RD_LAT cycles ago (data), storage content of their physical read cycle (the request cycle) c - RD_LAT
        rd = self.hist[c - RD_LAT] if c >= RD_LAT else []
        ovf = int(d.bank_overflow_o.value)
        assert ovf == (1 if (c - OVF_LAT) in self.ovf_cycles else 0), f"bank_overflow_o = {ovf} at cycle {c}"
        if (c - RD_LAT) not in self.ovf_cycles:
            view = self.snap[c - RD_LAT] if c >= RD_LAT else {}
            # Only the slices of ports that read an already-written address are converted: storage has
            # no reset, so other slices are X on a 4-state simulator.
            bits = str(d.rdata_o.value)                  # MSB first
            for p, a, _, _ in rd:
                if view.get(a) is not None:
                    field = bits[len(bits) - (p + 1) * CW: len(bits) - p * CW]
                    assert set(field) <= {"0", "1"}, f"cycle {c}: port {p} addr {a}: rdata = {field}"
                    got = int(field, 2)
                    assert got == view[a], (
                        f"cycle {c}: port {p} addr {a}: expected {view[a]}, got {got} "
                        f"(RD_LAT={RD_LAT}, WR_DELAY={WR_DELAY})")
                    self.reads_checked += 1
        # writes land at the clock edge that ends this cycle
        for _, a, w, v in landing:
            if w:
                self.mem[a] = v

    async def flush(self):
        for _ in range(PIPE + 1):
            await self.cycle([])


@cocotb.test()
async def test_every_address_every_port(dut):
    """Write then read back every address through every port."""
    b = Bench(dut)
    await b.reset()
    rng = random.Random(50)
    for port in range(NP):
        for a in range(256):
            await b.cycle([(port, a, True, rng.randrange(Q))])
        await b.flush()
        for a in range(256):
            await b.cycle([(port, a, False, 0)])
    await b.flush()
    assert b.reads_checked >= NP * 256, b.reads_checked


@cocotb.test()
async def test_scheduled_traffic(dut):
    """The lane schedule of both directions, back-to-back: 16 ports per cycle, each bank gets two
    reads and (PIPE cycles later) two writes of different addresses; bank_overflow_o stays 0."""
    b = Bench(dut)
    await b.reset()
    rng = random.Random(51)
    for a in range(256):                                 # initialise through one port per cycle
        await b.cycle([(0, a, True, rng.randrange(Q))])
    await b.flush()
    for mode in (0, 1):
        for layer in range(7):
            for t in range(128 // L):
                reqs = []
                for lane in range(L):
                    j, jlen = addr_pair(layer, mode, lane_p(L, lane, t))
                    reqs.append((2 * lane, j, True, rng.randrange(Q)))
                    reqs.append((2 * lane + 1, jlen, True, rng.randrange(Q)))
                await b.cycle(reqs)
            if PIPE >= 8:
                await b.flush()
    await b.flush()
    for a in range(256):
        await b.cycle([(0, a, False, 0)])
    await b.flush()


@cocotb.test()
async def test_read_after_write_next_cycle(dut):
    """A read performed in the cycle after the write landed returns the new value; a read performed in
    the landing cycle itself still returns the old one."""
    b = Bench(dut)
    await b.reset()
    rng = random.Random(52)
    for a in (0, 1, 127, 128, 255):
        old, new = rng.randrange(Q), rng.randrange(Q)
        await b.cycle([(0, a, True, old)])
        await b.flush()
        await b.cycle([(0, a, True, new)])               # request at cycle c, lands at end of c + PIPE
        for _ in range(WR_DELAY):                        # reads performed at c + RD_LAT + 1 ... c + PIPE
            await b.cycle([(3, a, False, 0)])            # (old value) and c + PIPE + 1 (new value)
        await b.cycle([(3, a, False, 0)])
        await b.cycle([(5, a, False, 0)])
        await b.flush()


@cocotb.test()
async def test_overflow_flag_works(dut):
    """Sanity of the diagnostic itself: two enabled ports on one bank in one cycle must raise
    bank_overflow_o (one cycle later), ports on different banks must not."""
    b = Bench(dut)
    await b.reset()
    same = [a for a in range(256) if bank16(a) == 3][:3]
    other = [a for a in range(256) if bank16(a) == 9][:1]
    await b.cycle([(0, same[0], False, 0), (7, other[0], False, 0)])
    await b.cycle([(0, same[0], False, 0), (12, same[2], False, 0)],
                  expect_overflow=True)
    await b.cycle([(2, same[2], False, 0)])
    await b.flush()
