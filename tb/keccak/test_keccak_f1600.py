"""tb/keccak/test_keccak_f1600.py -- Phase 7 test plan V4: rtl/keccak/keccak_f1600.sv against the golden Keccak (tb/golden/keccak.py).
Corner cases of section 3: all-zero state, all-ones state, each single-bit state (1,600), 200 random states, a chain of 10 permutations. The state after EVERY round
is compared with the golden trace (internal register state_q, sampled every cycle) and busy_o must be high for exactly 24 cycles, whatever the state.
Also: lane read port, lane xor ignored while busy and for lane >= 25, run ignored while busy, clear in the middle of a permutation.
Environment: KK_SEEDS (random states, default 200).
"""
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))

import cocotb
import keccak as K
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge

NSTATES = int(os.environ.get("KK_SEEDS", "200"))


async def _setup(dut):
    cocotb.start_soon(Clock(dut.clk_i, 10, unit="ns").start())
    dut.rst_ni.value = 0
    for s in ("run_i", "clear_i", "xor_en_i"):
        getattr(dut, s).value = 0
    dut.xor_lane_i.value = 0
    dut.xor_data_i.value = 0
    dut.rd_lane_i.value = 0
    await ClockCycles(dut.clk_i, 3)
    await FallingEdge(dut.clk_i)
    dut.rst_ni.value = 1


async def _load(dut, lanes):
    await FallingEdge(dut.clk_i)
    dut.clear_i.value = 1
    await FallingEdge(dut.clk_i)
    dut.clear_i.value = 0
    for i, v in enumerate(lanes):
        dut.xor_en_i.value, dut.xor_lane_i.value, dut.xor_data_i.value = 1, i, v
        await FallingEdge(dut.clk_i)
    dut.xor_en_i.value = 0


def _state(dut):
    v = int(dut.state_q.value)
    return [(v >> (64 * i)) & K.M64 for i in range(25)]


async def _permute(dut, lanes):
    """Loads `lanes`, runs one permutation; returns (states sampled each cycle, busy cycles, done pulses)."""
    await _load(dut, lanes)
    assert _state(dut) == lanes, "load through the xor port"
    dut.run_i.value = 1
    await FallingEdge(dut.clk_i)  # the cycle after the edge that sampled run_i
    dut.run_i.value = 0
    samples, busy, done = [_state(dut)], 0, 0
    for _ in range(40):
        busy += int(dut.busy_o.value)
        done += int(dut.done_o.value)
        if not int(dut.busy_o.value) and len(samples) > 1:
            break
        await FallingEdge(dut.clk_i)
        samples.append(_state(dut))
    return samples, busy, done


def _check(samples, busy, done, lanes, tag):
    assert busy == 24, f"{tag}: busy_o high for {busy} cycles, expected exactly 24"
    assert done == 1, f"{tag}: {done} done pulses"
    trace = K.keccak_trace(lanes)
    assert len(samples) == 25, f"{tag}: {len(samples)} samples"
    for r in range(24):
        assert samples[r + 1] == trace[r], f"{tag}: state after round {r} differs from the golden trace"
    assert samples[24] == K.keccak_f1600(lanes)


@cocotb.test()
async def test_permutation_every_round_and_24_cycles(dut):
    await _setup(dut)
    rng = random.Random(710)
    states = [("zero", [0] * 25), ("ones", [K.M64] * 25)]
    states += [(f"bit{b}", [(1 << (b % 64)) if i == b // 64 else 0 for i in range(25)]) for b in range(1600)]
    states += [(f"rand{i}", [rng.getrandbits(64) for _ in range(25)]) for i in range(NSTATES)]
    for tag, lanes in states:
        s, b, d = await _permute(dut, lanes)
        _check(s, b, d, lanes, tag)
    # chain: output fed back as input, 10 times (xor into the existing state is not used: the state stays in the core)
    lanes = [rng.getrandbits(64) for _ in range(25)]
    await _load(dut, lanes)
    exp = lanes
    for it in range(10):
        dut.run_i.value = 1
        await FallingEdge(dut.clk_i)
        dut.run_i.value = 0
        n = 0
        while True:
            await FallingEdge(dut.clk_i)
            n += 1
            if int(dut.done_o.value):
                break
            assert n < 40
        exp = K.keccak_f1600(exp)
        assert _state(dut) == exp, f"chain step {it}"
        assert n == 24, f"chain step {it}: done {n} cycles after the first busy cycle"
    dut._log.info(f"{len(states)} states (zero, ones, 1600 single-bit, {NSTATES} random) + chain of 10: every round equal to the golden trace, busy_o = 24 cycles each")


@cocotb.test()
async def test_ports(dut):
    await _setup(dut)
    rng = random.Random(711)
    lanes = [rng.getrandbits(64) for _ in range(25)]
    await _load(dut, lanes)
    for i in range(25):
        dut.rd_lane_i.value = i
        await FallingEdge(dut.clk_i)
        assert int(dut.rd_data_o.value) == lanes[i], f"read lane {i}"
    dut.rd_lane_i.value = 25
    await FallingEdge(dut.clk_i)
    assert int(dut.rd_data_o.value) == 0, "read of lane >= 25 must give 0"
    # xor into lane 25..31 ignored
    for ln in (25, 31):
        dut.xor_en_i.value, dut.xor_lane_i.value, dut.xor_data_i.value = 1, ln, K.M64
        await FallingEdge(dut.clk_i)
    dut.xor_en_i.value = 0
    await FallingEdge(dut.clk_i)
    assert _state(dut) == lanes, "xor to a lane >= 25 changed the state"
    # xor and a second run ignored while busy; busy stays 24 cycles
    dut.run_i.value = 1
    await FallingEdge(dut.clk_i)
    dut.run_i.value = 0
    busy = 0
    for k in range(40):
        if k in (3, 7):
            dut.xor_en_i.value, dut.xor_lane_i.value, dut.xor_data_i.value = 1, 4, K.M64
            dut.run_i.value = 1
        else:
            dut.xor_en_i.value = 0
            dut.run_i.value = 0
        busy += int(dut.busy_o.value)
        if not int(dut.busy_o.value):
            break
        await FallingEdge(dut.clk_i)
    dut.xor_en_i.value = 0
    dut.run_i.value = 0
    assert busy == 24, f"busy {busy} with xor and run during the permutation"
    assert _state(dut) == K.keccak_f1600(lanes), "xor or run while busy changed the result"
    # clear in the middle of a permutation: busy drops, state wiped; a new permutation is again 24 cycles
    await _load(dut, lanes)
    dut.run_i.value = 1
    await FallingEdge(dut.clk_i)
    dut.run_i.value = 0
    await ClockCycles(dut.clk_i, 5)
    await FallingEdge(dut.clk_i)
    dut.clear_i.value = 1
    await FallingEdge(dut.clk_i)
    dut.clear_i.value = 0
    await FallingEdge(dut.clk_i)
    assert int(dut.busy_o.value) == 0 and _state(dut) == [0] * 25, "clear in the middle of a permutation"
    s, b, d = await _permute(dut, lanes)
    _check(s, b, d, lanes, "after clear")
    dut._log.info("read port, lane >= 25, xor/run while busy, clear mid-permutation: OK")
