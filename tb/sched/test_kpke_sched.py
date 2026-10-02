"""tb/sched/test_kpke_sched.py -- Phase 6 test plan V5 (and V6 with KS_NEGCTL=1): rtl/sched/kpke_sched_top.sv runs the K-PKE arithmetic programs; the slots read
back after each program must equal the golden schedule model (tb/golden/kpke_sched_model.py, itself proven equal to the golden K-PKE), and the end results must equal the
unmodified golden K-PKE (t_hat of KeyGen, the ciphertext of Encrypt after compression and encoding, the message of Decrypt). Transform counters and constant cycle counts
per program are checked. With KS_NEGCTL=1 the build is a mutant and the test passes only if the bit-exact comparison FAILS.
Environment: KS_NEGCTL, KS_SEEDS (random cases per program), KS_CYCLES_OUT (json with the cycle counts).
"""
import json
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))

import cocotb
import kpke
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge
from kpke_sched_model import NPOLY, PROG_ID, PROGRAMS, decrypt_inputs, encrypt_inputs, keygen_inputs, run
from params import DU, DV, K, N, Q
from primitives import byte_decode, byte_encode, compress

NEGCTL = os.environ.get("KS_NEGCTL", "0") == "1"
NSEEDS = int(os.environ.get("KS_SEEDS", "2"))
CYCLES_OUT = os.environ.get("KS_CYCLES_OUT", "")
MAX_CYCLES = 60000
EXPECT_COUNTS = {"keygen": (6, 0, 9), "encrypt": (3, 4, 12), "decrypt": (3, 1, 3)}


def _rand(rng, n=32):
    return bytes(rng.randrange(256) for _ in range(n))


async def _setup(dut):
    cocotb.start_soon(Clock(dut.clk_i, 10, unit="ns").start())
    dut.rst_ni.value = 0
    dut.start_i.value = 0
    dut.prog_i.value = 0
    dut.tb_we_i.value = 0
    dut.tb_slot_i.value = 0
    dut.tb_addr_i.value = 0
    dut.tb_wdata_i.value = 0
    await ClockCycles(dut.clk_i, 5)
    await FallingEdge(dut.clk_i)
    dut.rst_ni.value = 1


async def _load(dut, slots):
    for s in range(NPOLY):
        for a in range(N):
            await FallingEdge(dut.clk_i)
            dut.tb_slot_i.value, dut.tb_addr_i.value, dut.tb_wdata_i.value, dut.tb_we_i.value = s, a, slots[s][a], 1
    await FallingEdge(dut.clk_i)
    dut.tb_we_i.value = 0


async def _read(dut):
    out = [[0] * N for _ in range(NPOLY)]
    seq = [(s, a) for s in range(NPOLY) for a in range(N)]
    prev = None
    for i in range(len(seq) + 1):
        await FallingEdge(dut.clk_i)
        if prev is not None:
            out[prev[0]][prev[1]] = int(dut.tb_rdata_o.value)
        if i < len(seq):
            dut.tb_slot_i.value, dut.tb_addr_i.value = seq[i]
            prev = seq[i]
    return out


async def _run(dut, name):
    dut.prog_i.value = PROG_ID[name]
    dut.start_i.value = 1
    await FallingEdge(dut.clk_i)
    dut.start_i.value = 0
    cycles = 1
    while int(dut.done_o.value) == 0:
        assert int(dut.bank_overflow_o.value) == 0, "bank_overflow_o raised"
        await FallingEdge(dut.clk_i)
        cycles += 1
        assert cycles < MAX_CYCLES, f"{name}: done_o never rose"
    counts = (int(dut.cnt_ntt_o.value), int(dut.cnt_intt_o.value), int(dut.cnt_pwm_o.value))
    return cycles, counts


async def _case(dut, name, slots):
    """Loads slots, runs the program, reads every slot back; returns (equal to the model, slots read, cycles, counts)."""
    expect = [list(p) for p in slots]
    run(PROGRAMS[name], expect)
    await _load(dut, slots)
    cycles, counts = await _run(dut, name)
    got = await _read(dut)
    return got == expect, got, cycles, counts


def _inputs(name, rng):
    if name == "keygen":
        d = _rand(rng)
        slots, _ = keygen_inputs(d)
        ek, _ = kpke.k_pke_keygen(d)
        return slots, ("keygen", ek)
    ek, dk = kpke.k_pke_keygen(_rand(rng))
    m, r = _rand(rng), _rand(rng)
    c = kpke.k_pke_encrypt(ek, m, r)
    if name == "encrypt":
        return encrypt_inputs(ek, m, r), ("encrypt", c)
    return decrypt_inputs(dk, c), ("decrypt", m)


def _end_to_end(kind, ref, got):
    if kind == "keygen":
        return [got[12 + i] for i in range(K)] == [byte_decode(12, ref[384 * i: 384 * (i + 1)]) for i in range(K)]
    if kind == "encrypt":
        c1 = b"".join(byte_encode(DU, compress(DU, got[12 + i])) for i in range(K))
        return c1 + byte_encode(DV, compress(DV, got[19])) == ref
    return byte_encode(1, compress(1, got[19])) == ref


@cocotb.test(skip=NEGCTL)
async def test_programs_bit_exact_and_constant(dut):
    await _setup(dut)
    rng = random.Random(600)
    cyc = {}
    for name in ("keygen", "encrypt", "decrypt"):
        seen = set()
        cases = [_inputs(name, rng) for _ in range(NSEEDS)]
        corners = [([[0] * N for _ in range(NPOLY)], None), ([[Q - 1] * N for _ in range(NPOLY)], None)]
        for slots, ref in cases + corners:
            ok, got, cycles, counts = await _case(dut, name, slots)
            assert ok, f"{name}: slots differ from the golden schedule model"
            if ref is not None:
                assert _end_to_end(ref[0], ref[1], got), f"{name}: end result differs from the golden K-PKE"
            assert counts == EXPECT_COUNTS[name], f"{name}: transform counters {counts}, expected {EXPECT_COUNTS[name]}"
            seen.add(cycles)
        assert len(seen) == 1, f"{name}: cycle count not constant: {seen}"
        cyc[name] = seen.pop()
        dut._log.info(f"{name}: {NSEEDS} random + 2 corner cases bit-exact, end-to-end equal, counters {EXPECT_COUNTS[name]}, cycles {cyc[name]}")
    if CYCLES_OUT:
        Path(CYCLES_OUT).write_text(json.dumps(cyc) + "\n")


@cocotb.test(skip=not NEGCTL)
async def test_negative_control_must_fail(dut):
    await _setup(dut)
    rng = random.Random(601)
    wrong = 0
    for name in ("keygen", "encrypt"):
        slots, _ = _inputs(name, rng)
        ok, _, _, _ = await _case(dut, name, slots)
        wrong += not ok
    dut._log.info(f"negative control: {wrong}/2 programs differ from the model")
    assert wrong == 2, "mutant not detected by the bit-exact comparison"
