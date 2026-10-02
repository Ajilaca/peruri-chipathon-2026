"""tb/phase5m/test_poly_mem_split.py -- Phase 5M S7 test V2: a copy of the Phase 4 memory test tb/ntt/test_poly_mem_pipe.py (frozen) for
rtl/mem/poly_mem_multiport_split.sv, NUM_LANES = 8, against a cycle-accurate Python model:

    request at cycle c -> storage physically read at c + NARB (NARB = bits set in ARB_REG) -> rdata_o at c + NARB + RD_SPLIT
    write of that request (if requested) lands at the end of c + NARB + RD_SPLIT + WR_DELAY, write data presented by the caller in that cycle
    bank_overflow_o is flagged at c + NARB (the read-stage control, not delayed by RD_SPLIT)

The data a read returns is the storage content at the physical read cycle (before that cycle's landing), which with RD_SPLIT = 1 is one cycle
before the data appears. ARB_REG / WR_DELAY / RD_SPLIT come from P7_ARB_REG / P7_WR_DELAY / P7_RD_SPLIT (set by tb/phase5m/run_s7_tests.py).
"""

import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "mem"))

import cocotb
from bank_model import addr_pair, bank_of, lane_p
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, Timer
from params import Q

L = 8
NP = 2 * L
AW, CW = 8, 12
ARB_REG = int(os.environ.get("P7_ARB_REG", "0"))
WR_DELAY = int(os.environ.get("P7_WR_DELAY", "0"))
RD_SPLIT = int(os.environ.get("P7_RD_SPLIT", "1"))
NARB = bin(ARB_REG).count("1")
RD_LAT = NARB + RD_SPLIT          # request -> read data
PIPE = RD_LAT + WR_DELAY


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
        # read stage: the requests of RD_LAT cycles ago (data), storage content of the physical read cycle c - RD_SPLIT
        rd = self.hist[c - RD_LAT] if c >= RD_LAT else []
        ovf = int(d.bank_overflow_o.value)
        assert ovf == (1 if (c - NARB) in self.ovf_cycles else 0), f"bank_overflow_o = {ovf} at cycle {c}"
        if (c - RD_LAT) not in self.ovf_cycles:
            view = self.snap[c - RD_SPLIT] if c >= RD_SPLIT else {}
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
                        f"(ARB_REG={ARB_REG:#x}, WR_DELAY={WR_DELAY}, RD_SPLIT={RD_SPLIT})")
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
    for a in range(0, 256, 2):                           # initialise through two ports per cycle
        await b.cycle([(0, a, True, rng.randrange(Q)), (1, a + 1, True, rng.randrange(Q))]
                      )
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
    """Sanity of the diagnostic itself: three enabled ports on one bank in one cycle must raise
    bank_overflow_o (RD_LAT cycles later), two must not."""
    b = Bench(dut)
    await b.reset()
    same = [a for a in range(256) if bank_of(a, L) == 3][:3]
    await b.cycle([(0, same[0], False, 0), (7, same[1], False, 0)])
    await b.cycle([(0, same[0], False, 0), (7, same[1], False, 0), (12, same[2], False, 0)],
                  expect_overflow=True)
    await b.cycle([(2, same[2], False, 0)])
    await b.flush()
