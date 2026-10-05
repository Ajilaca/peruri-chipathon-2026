"""tb/phase5m/test_ntt_core_s7.py -- Phase 5M step S7 core test (evidence/phase05m/test_plan_s7.md V4, V5): a copy of the Phase 4 core
test tb/ntt/test_ntt_core_c3.py (which stays frozen) for the core with the memory read split by one register stage (RD_SPLIT = 1).
Differences from the Phase 4 test, nothing else:
  - C3_RDLAT is the number of cycles from a request to its read DATA (= arbitration cuts + RD_SPLIT, here 4), used for host read-back and the
    zeta alignment; C3_RDPHYS is the cycle in which the STORAGE is physically read (arbitration cuts only, here 3), used by the hazard scoreboard's
    same-cycle read / write check; the write lands at the end of cycle request + C3_RDLAT + C3_WRDLY (= P = 7);
  - the golden INTT comparison is unchanged (FIPS 203 intt(), which includes the 3303 scaling the M6 core no longer performs);
  - one more test: the 512 INTT unit vectors of S6 (tests equality with intt() and intt_halving()).
Environment: C3_RDLAT, C3_RDPHYS, C3_WRDLY, C3_CORE, C3_NEGCTL, C3_CYCLES_OUT (set by tb/phase5m/run_s7_tests.py).
"""

import json
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
from params import N, Q
from intt_halving import intt_halving
from primitives import intt, ntt

L = 8
NP = 2 * L
AW = 8
RDLAT = int(os.environ.get("C3_RDLAT", "0"))
RDPHYS = int(os.environ.get("C3_RDPHYS", str(RDLAT)))
WRDLY = int(os.environ.get("C3_WRDLY", "0"))
PIPE = RDLAT + WRDLY
CORE = os.environ.get("C3_CORE", "")
NEGCTL = os.environ.get("C3_NEGCTL", "0") == "1"
CYCLES_OUT = os.environ.get("C3_CYCLES_OUT", "")

CLK_PERIOD_NS = 10
MAX_CYCLES = 5000
S_RUN, S_SCALE = 1, 2          # S_SCALE (= 2) never occurs in the M6 / S7 cores
EXPECT_NTT = 7 * (128 // L) + 1 + PIPE          # ESTIMATE of the plan; the measured value is recorded
EXPECT_INTT = EXPECT_NTT                       # S7: INTT has the NTT's cycle count (no scaling pass)


def _core(dut):
    return getattr(dut, CORE) if CORE else dut


class Scoreboard:
    def __init__(self, dut):
        self.core = _core(dut)
        self.clk = dut.clk_i
        self.cycle = 0
        self.lands = {}         # address -> cycle at whose end its pending write lands
        self.reqs = {}          # request cycle -> tuple of addresses (S_RUN / S_SCALE requests only)
        self.violations = []
        self.requests_seen = 0

    async def run(self):
        while True:
            await FallingEdge(self.clk)
            await Timer(2, unit="ns")            # after the test has driven its inputs for this cycle
            c = self.cycle
            self.cycle += 1
            state = self.core.state_q.value
            if not state.is_resolvable or int(state) not in (S_RUN, S_SCALE):
                self.reqs.pop(c - PIPE - 1, None)
                continue
            en = int(self.core.mem_en.value)
            wr = int(self.core.mem_wr.value)
            addr = int(self.core.mem_addr.value)
            addrs = tuple((addr >> (i * AW)) & 0xFF for i in range(NP) if (en >> i) & 1)
            assert all((wr >> i) & 1 for i in range(NP) if (en >> i) & 1), "busy request without write-back"
            for a in addrs:                       # (a) issued while an earlier write is still in flight
                if self.lands.get(a, -1) >= c:
                    self.violations.append(("read-issued-before-write-landed", c, a, self.lands[a]))
            for a in addrs:
                self.lands[a] = c + PIPE
            self.reqs[c] = addrs
            self.requests_seen += len(addrs)
            if WRDLY > 0:                         # (b) performed in the same cycle: read of request
                rd = self.reqs.get(c - RDPHYS, ())  #    c - RDPHYS (storage read), write of request c - PIPE
                wrs = self.reqs.get(c - PIPE, ())
                for a in set(rd) & set(wrs):
                    self.violations.append(("same-cycle-read-write", c, a, c))
            self.reqs.pop(c - PIPE - 1, None)


def _corner_polys() -> list[list[int]]:
    m = Q - 1
    imp0 = [0] * N
    imp0[0] = 1
    imp_last = [0] * N
    imp_last[-1] = 1
    alt = [(0 if i % 2 == 0 else m) for i in range(N)]
    return [[0] * N, [m] * N, imp0, imp_last, alt]


def _tight_addresses(mode: int) -> set[int]:
    """Addresses with the smallest write-to-next-read distance at each layer boundary (and before the
    INTT scaling pass): same model as scripts/test/pipeline_hazard_slack.py."""
    t_per = 128 // L
    out = set()
    for layer in range(6):
        t_w, t_r = {}, {}
        for t in range(t_per):
            for lane in range(L):
                p = lane_p(L, lane, t)
                for a in addr_pair(layer, mode, p):
                    t_w[a] = t
                for a in addr_pair(layer + 1, mode, p):
                    t_r[a] = t
        slack = {a: t_per + t_r[a] - t_w[a] - 1 for a in range(N)}
        out |= {a for a in range(N) if slack[a] == min(slack.values())}
    if mode == 1:
        t_w = {}
        for t in range(t_per):
            for lane in range(L):
                for a in addr_pair(6, 1, lane_p(L, lane, t)):
                    t_w[a] = t
        slack = {a: t_per + a - t_w[a] - 1 for a in range(N)}
        out |= {a for a in range(N) if slack[a] == min(slack.values())}
    return out


async def _setup(dut) -> Scoreboard:
    cocotb.start_soon(Clock(dut.clk_i, CLK_PERIOD_NS, unit="ns").start())
    dut.rst_ni.value = 0
    dut.start_i.value = 0
    dut.mode_i.value = 0
    dut.host_we_i.value = 0
    dut.host_addr_i.value = 0
    dut.host_wdata_i.value = 0
    await ClockCycles(dut.clk_i, 5)
    await FallingEdge(dut.clk_i)
    dut.rst_ni.value = 1
    sb = Scoreboard(dut)
    cocotb.start_soon(sb.run())
    return sb


def _no_overflow(dut, where: str) -> None:
    v = dut.bank_overflow_o.value
    assert v.is_resolvable and int(v) == 0, f"bank_overflow_o = {v} {where}"


async def _load(dut, coeffs: list[int]) -> None:
    for addr, val in enumerate(coeffs):
        await FallingEdge(dut.clk_i)
        dut.host_addr_i.value = addr
        dut.host_wdata_i.value = val
        dut.host_we_i.value = 1
        _no_overflow(dut, f"during load, addr={addr}")
    await FallingEdge(dut.clk_i)
    dut.host_we_i.value = 0


async def _run(dut, mode: int) -> int:
    """Holds start_i until busy_o rises; returns the cycles from the first busy cycle to done_o."""
    dut.mode_i.value = mode
    dut.start_i.value = 1
    guard = 0
    while int(dut.busy_o.value) == 0:
        await FallingEdge(dut.clk_i)
        guard += 1
        assert guard < MAX_CYCLES, "ntt_core_c3 never went busy after start_i"
    assert guard <= WRDLY + 2, f"start_i taken only after {guard} cycles"
    dut.start_i.value = 0
    cycles = 0
    while int(dut.done_o.value) == 0:
        _no_overflow(dut, f"mid-run at cycle {cycles}")
        await FallingEdge(dut.clk_i)
        cycles += 1
        assert cycles < MAX_CYCLES, "ntt_core_c3 did not assert done_o in time"
    return cycles


async def _read_all(dut) -> list[int]:
    """host_rdata_o shows the coefficient RDLAT cycles after host_addr_i; addresses are streamed."""
    out = []
    for i in range(N + RDLAT):
        await FallingEdge(dut.clk_i)
        if RDLAT > 0 and i >= RDLAT:
            out.append(int(dut.host_rdata_o.value))
        dut.host_addr_i.value = min(i, N - 1)
        if RDLAT == 0:
            await Timer(1, unit="ns")
            out.append(int(dut.host_rdata_o.value))
        _no_overflow(dut, f"during read-back, i={i}")
    return out


async def _transform(dut, f: list[int], mode: int) -> tuple[list[int], int]:
    await _load(dut, f)
    cycles = await _run(dut, mode)
    return await _read_all(dut), cycles


def _check_scoreboard(sb: Scoreboard) -> None:
    assert sb.requests_seen > 0, "scoreboard saw no request: it is not connected"
    assert not sb.violations, f"{len(sb.violations)} hazard(s), first: {sb.violations[:3]}"


@cocotb.test(skip=NEGCTL)
async def test_ntt_bit_exact(dut):
    sb = await _setup(dut)
    rng = random.Random(30)
    for f in _corner_polys() + [[rng.randrange(Q) for _ in range(N)] for _ in range(100)]:
        got, _ = await _transform(dut, f, 0)
        assert got == ntt(f), f"NTT mismatch (P={PIPE}), first coeffs of input: {f[:4]}"
    _check_scoreboard(sb)


@cocotb.test(skip=NEGCTL)
async def test_intt_bit_exact(dut):
    sb = await _setup(dut)
    rng = random.Random(31)
    for f in _corner_polys() + [[rng.randrange(Q) for _ in range(N)] for _ in range(100)]:
        got, _ = await _transform(dut, f, 1)
        assert got == intt(f), f"INTT mismatch (P={PIPE}), first coeffs of input: {f[:4]}"
    _check_scoreboard(sb)


@cocotb.test(skip=NEGCTL)
async def test_ntt_intt_roundtrip(dut):
    sb = await _setup(dut)
    rng = random.Random(32)
    for _ in range(50):
        f = [rng.randrange(Q) for _ in range(N)]
        f_hat, _ = await _transform(dut, f, 0)
        f_rt, _ = await _transform(dut, f_hat, 1)
        assert f_rt == f, f"intt(ntt(f)) != f through the RTL (P={PIPE})"
    _check_scoreboard(sb)


@cocotb.test(skip=NEGCTL)
async def test_boundary_directed(dut):
    """V7 directed data: pairs of polynomials that differ only at the addresses with the tightest
    layer-boundary slack, so a stale read there changes the result."""
    sb = await _setup(dut)
    rng = random.Random(34)
    for mode, gold in ((0, ntt), (1, intt)):
        tight = sorted(_tight_addresses(mode))
        assert tight
        for _ in range(10):
            f = [rng.randrange(Q) for _ in range(N)]
            g = list(f)
            for a in tight:
                g[a] = (f[a] + 1 + rng.randrange(Q - 1)) % Q
            for poly in (f, g):
                got, _ = await _transform(dut, poly, mode)
                assert got == gold(poly), f"mode={mode} mismatch on boundary-directed data (P={PIPE})"
    _check_scoreboard(sb)


@cocotb.test(skip=NEGCTL)
async def test_cycle_count_constant(dut):
    """V6 / CRG-7: cycles from busy_o to done_o identical for every input, per direction."""
    sb = await _setup(dut)
    rng = random.Random(33)
    polys = _corner_polys() + [[rng.randrange(Q) for _ in range(N)] for _ in range(20)]
    counts = {}
    for mode, name in ((0, "NTT"), (1, "INTT")):
        seen = set()
        for f in polys:
            _, cycles = await _transform(dut, f, mode)
            seen.add(cycles)
        assert len(seen) == 1, f"{name} cycle count not constant at P={PIPE}: {seen}"
        counts[name] = seen.pop()
    _check_scoreboard(sb)
    stall = {"NTT": counts["NTT"] - EXPECT_NTT, "INTT": counts["INTT"] - EXPECT_INTT}
    dut._log.info(f"P={PIPE} cycles: NTT={counts['NTT']} INTT={counts['INTT']} stall vs plan: {stall}")
    if CYCLES_OUT:
        Path(CYCLES_OUT).write_text(json.dumps(
            {"P": PIPE, "RDLAT": RDLAT, "WRDLY": WRDLY, "cycles_NTT": counts["NTT"],
             "cycles_INTT": counts["INTT"], "stall_NTT": stall["NTT"], "stall_INTT": stall["INTT"]}) + "\n")


@cocotb.test(skip=not NEGCTL)
async def test_negative_control_must_fail(dut):
    """V7 negative control: a depth beyond the schedule's slack. This test PASSES only if the scoreboard
    trips AND the transform result is wrong, in both directions."""
    sb = await _setup(dut)
    rng = random.Random(35)
    summary = {}
    for mode, gold, name in ((0, ntt, "NTT"), (1, intt, "INTT")):
        before = len(sb.violations)
        wrong = 0
        for _ in range(5):
            f = [rng.randrange(Q) for _ in range(N)]
            got, _ = await _transform(dut, f, mode)
            wrong += got != gold(f)
        tripped = len(sb.violations) - before
        summary[name] = (tripped, wrong)
        assert tripped > 0, f"{name}: scoreboard did not trip at P={PIPE}; V7 is void"
        assert wrong == 5, f"{name}: only {wrong}/5 results wrong at P={PIPE}; bit-exact check is weak"
    dut._log.info(f"negative control P={PIPE}: (violations, wrong results of 5) = {summary}; "
                  f"first violation: {sb.violations[0]}")
    if CYCLES_OUT:
        Path(CYCLES_OUT).write_text(json.dumps(
            {"negctl_P": PIPE, "violations_NTT": summary["NTT"][0], "wrong_NTT": summary["NTT"][1],
             "violations_INTT": summary["INTT"][0], "wrong_INTT": summary["INTT"][1]}) + "\n")


@cocotb.test(skip=NEGCTL)
async def test_intt_unit_vectors(dut):
    sb = await _setup(dut)
    n_ok = 0
    for i in range(N):
        for scale in (1, Q - 1):
            f = [0] * N
            f[i] = scale
            got, _ = await _transform(dut, f, 1)
            assert got == intt(f), f"INTT of {scale}*e_{i} differs from intt()"
            assert got == intt_halving(f), f"INTT of {scale}*e_{i} differs from intt_halving()"
            n_ok += 1
    dut._log.info(f"INTT unit vectors: {n_ok}/{2 * N} equal to intt() and intt_halving()")
    _check_scoreboard(sb)
