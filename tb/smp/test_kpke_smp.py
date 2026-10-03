"""tb/smp/test_kpke_smp.py -- Phase 8c / 8d test plan V3-V5: rtl/sched/kpke_smp_top_s10.sv runs the K-PKE programs with sampling (STORE, STREAM, OVERLAP; env KP_VAR). After each program every slot the program writes or reads
is read back and must equal the golden program model (tb/golden/kpke_smp_model.py), and the end results must equal the unmodified golden K-PKE (t_hat of KeyGen, the ciphertext of Encrypt, the message of Decrypt).
Counters, constant cycles (fixed rho, varied secrets), the stall coverage of the PWMS passes and the store-port arbitration are checked. Environment: KP_VAR (0 STORE, 1 STREAM, 2 OVERLAP), KP_N (random cases per program, default 3),
KP_CYCLES_OUT (json with the cycle counts)."""
import json
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))

import cocotb
import kpke
import kpke_smp_model as M
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge
from params import DU, DV, K, N
from primitives import byte_decode, byte_encode, compress
from sampler_model import sample_ntt_stream

VAR = int(os.environ.get("KP_VAR", "0"))
NCASES = int(os.environ.get("KP_N", "3"))
CYCLES_OUT = os.environ.get("KP_CYCLES_OUT", "")
MAX_CYCLES = 120000
S_PWMS = 9  # state_t encoding of kpke_sched_smp.sv
EXPECT = {"keygen": (6, 0, 9), "encrypt": (3, 4, 12), "decrypt": (3, 1, 3)}
NSMP = {M.STORE: {"keygen": 15, "encrypt": 16, "decrypt": 0}, M.STREAM: {"keygen": 6, "encrypt": 7, "decrypt": 0}, M.OVERLAP: {"keygen": 6, "encrypt": 7, "decrypt": 0}, M.STRESS: {"keygen": 6, "encrypt": 7, "decrypt": 0}}
PROGS = M.programs(VAR)
STALL = {"first": 0, "gap0": 0, "gap1": 0, "gap2_13": 0, "gap14": 0, "beats": 0}
HELD = {"held_cycles": 0, "overlap_cycles": 0}   # OVERLAP / STRESS: cycles in which a sampler beat waits for the store write port; cycles in which the sampler runs while the sequencer is busy with another operation


def _rand(rng, n=32):
    return bytes(rng.randrange(256) for _ in range(n))


async def _setup(dut):
    cocotb.start_soon(Clock(dut.clk_i, 10, unit="ns").start())
    dut.rst_ni.value = 0
    for p in ("start_i", "prog_i", "tb_we_i", "tb_slot_i", "tb_addr_i", "tb_wdata_i", "seed_we_i", "seed_sel_i", "seed_idx_i", "seed_data_i"):
        getattr(dut, p).value = 0
    await ClockCycles(dut.clk_i, 5)
    await FallingEdge(dut.clk_i)
    dut.rst_ni.value = 1


async def _seed(dut, rho, sd):
    for sel, val in ((0, rho), (1, sd)):
        for w in range(4):
            await FallingEdge(dut.clk_i)
            dut.seed_sel_i.value, dut.seed_idx_i.value = sel, w
            dut.seed_data_i.value = int.from_bytes(val[8 * w: 8 * w + 8], "little")
            dut.seed_we_i.value = 1
    await FallingEdge(dut.clk_i)
    dut.seed_we_i.value = 0


async def _load(dut, slots, which):
    for s in which:
        for a in range(N):
            await FallingEdge(dut.clk_i)
            dut.tb_slot_i.value, dut.tb_addr_i.value, dut.tb_wdata_i.value, dut.tb_we_i.value = s, a, slots[s][a], 1
    await FallingEdge(dut.clk_i)
    dut.tb_we_i.value = 0


async def _read(dut, which):
    out = {s: [0] * N for s in which}
    seq = [(s, a) for s in which for a in range(N)]
    prev = None
    for i in range(len(seq) + 1):
        await FallingEdge(dut.clk_i)
        if prev is not None:
            out[prev[0]][prev[1]] = int(dut.tb_rdata_o.value)
        if i < len(seq):
            dut.tb_slot_i.value, dut.tb_addr_i.value = seq[i]
            prev = seq[i]
    return out


async def _run(dut, name, stall_stats=False):
    dut.prog_i.value = M.PROG_ID[name]
    dut.start_i.value = 1
    await FallingEdge(dut.clk_i)
    dut.start_i.value = 0
    cycles = 1
    gap, seen_first = 0, False
    in_pass = False
    while int(dut.done_o.value) == 0:
        assert int(dut.bank_overflow_o.value) == 0, "bank_overflow_o raised"
        if stall_stats and VAR != M.STORE:
            st = int(dut.u_sched.state_q.value)
            if st == S_PWMS:
                beat = int(dut.u_sched.beat.value)
                if not in_pass:
                    in_pass, gap, seen_first = True, 0, False
                if beat:
                    key = "first" if not seen_first else ("gap0" if gap == 0 else "gap1" if gap == 1 else "gap2_13" if gap < 14 else "gap14")
                    STALL[key] += 1
                    STALL["beats"] += 1
                    seen_first, gap = True, 0
                else:
                    gap += 1
            else:
                in_pass = False
        if VAR >= M.OVERLAP:
            if int(dut.u_sched.smp_cvalid.value) and not int(dut.u_sched.smp_cready.value) and int(dut.u_sched.smp_wr_q.value):
                HELD["held_cycles"] += 1
            if int(dut.u_sched.smp_busy.value) and int(dut.u_sched.state_q.value) in (2, 3, 4, 5, 6):   # LOAD, START, RUN, UNLOAD, PASS
                HELD["overlap_cycles"] += 1
        await FallingEdge(dut.clk_i)
        cycles += 1
        assert cycles < MAX_CYCLES, f"{name}: done_o never rose"
    counts = (int(dut.cnt_ntt_o.value), int(dut.cnt_intt_o.value), int(dut.cnt_pwm_o.value), int(dut.cnt_smp_o.value))
    return cycles, counts


def _touched(name, loaded):
    t = {d for opc, d, a, b, f, l in PROGS[name] if opc not in (M.OP_END, M.OP_WAIT)} | set(loaded)
    return sorted(t)


def _end_to_end(variant, name, ref, slots):
    lg = lambda s: M.logical(variant, slots, s)  # noqa: E731
    if name == "keygen":
        return [lg(12 + i) for i in range(K)] == [byte_decode(12, ref[384 * i: 384 * (i + 1)]) for i in range(K)]
    if name == "encrypt":
        c1 = b"".join(byte_encode(DU, compress(DU, lg(12 + i))) for i in range(K))
        return c1 + byte_encode(DV, compress(DV, lg(19))) == ref
    return byte_encode(1, compress(1, lg(19))) == ref


def _case_inputs(name, rng, rho=None, sd=None, fixed=None):
    """(hardware slots, loaded slot list, rho, sd, reference for the end-to-end check)."""
    if name == "keygen":
        d = _rand(rng)
        slots, r_, s_ = M.inputs(VAR, "keygen", d=d)
        ek, _ = kpke.k_pke_keygen(d)
        return slots, [], rho or r_, sd or s_, ek
    ek, dk = kpke.k_pke_keygen(_rand(rng))
    m, r = _rand(rng), _rand(rng)
    c = kpke.k_pke_encrypt(ek, m, r)
    if name == "encrypt":
        slots, r_, s_ = M.inputs(VAR, "encrypt", ek_pke=ek, m=m, r=r)
        return slots, [M.phys(VAR, s) for s in (16, 17, 18, 20)], r_, s_, c
    slots, r_, s_ = M.inputs(VAR, "decrypt", dk_pke=dk, c=c)
    return slots, [M.phys(VAR, s) for s in (9, 10, 11, 12, 13, 14, 19)], r_, s_, m


async def _case(dut, name, slots, loaded, rho, sd, ref, stall_stats=False):
    expect = [list(p) for p in slots]
    ecount = M.run(PROGS[name], expect, rho, sd)
    await _load(dut, slots, loaded)
    await _seed(dut, rho, sd)
    cycles, counts = await _run(dut, name, stall_stats)
    which = _touched(name, loaded)
    got = await _read(dut, which)
    ok = all(got[s] == expect[s] for s in which)
    if ok and ref is not None:
        full = [list(p) for p in slots]
        for s in which:
            full[s] = got[s]
        assert _end_to_end(VAR, name, ref, full), f"{name}: end result differs from the golden K-PKE"
    assert counts == EXPECT[name] + (NSMP[VAR][name],), f"{name}: counters {counts}, expected {EXPECT[name] + (NSMP[VAR][name],)}"
    return ok, cycles


def _four_block_rho(rng):
    while True:
        rho = _rand(rng)
        for m in range(9):
            j, i = M.msg_ji(m)
            import hashlib
            s = hashlib.shake_128(rho + bytes([j, i])).digest(1600)
            if sample_ntt_stream(s)[1] > 3 * 168:
                return rho


@cocotb.test()
async def test_programs_bit_exact(dut):
    await _setup(dut)
    rng = random.Random(700)   # the same inputs (same rho set) for every variant, so that cycle means are comparable
    cyc = {}
    four = _four_block_rho(random.Random(701))
    for name in ("keygen", "encrypt", "decrypt"):
        cases = [_case_inputs(name, rng) for _ in range(NCASES)]
        s, lo, rho, sd, ref = _case_inputs(name, rng)
        cases.append((s, lo, rho, sd, ref))
        extra = [(bytes(32), bytes(32)), (b"\xff" * 32, b"\xff" * 32), (four, _rand(rng))]
        for rho_x, sd_x in extra:
            s, lo, _, _, ref = _case_inputs(name, rng)
            cases.append((s, lo, rho_x, sd_x, None))
        times = []
        for slots, lo, rho, sd, ref in cases:
            ok, c = await _case(dut, name, slots, lo, rho, sd, ref, stall_stats=True)
            assert ok, f"{name}: slots differ from the golden program model"
            times.append(c)
        cyc[name] = times
        dut._log.info(f"{name} (VAR {VAR}): {len(cases)} cases bit-exact, counters {EXPECT[name]} + smp {NSMP[VAR][name]}, cycles {sorted(set(times))}")
    if VAR != M.STORE:
        dut._log.info(f"PWMS stall coverage (beats by the gap before them): {STALL}")
    if VAR >= M.OVERLAP:
        dut._log.info(f"overlap: {HELD}")
        assert HELD["overlap_cycles"] > 0, "the sampler never ran while the sequencer computed"
        if VAR == M.STRESS:
            assert HELD["held_cycles"] > 0, "no sampler beat was held back by a sequencer write: the arbitration was not exercised"
    if CYCLES_OUT:
        Path(CYCLES_OUT).write_text(json.dumps({"var": VAR, "cycles": cyc, "stall": STALL, "overlap": HELD}) + "\n")


@cocotb.test()
async def test_constant_cycles_fixed_rho(dut):
    await _setup(dut)
    rng = random.Random(710)
    res = {}
    for name in ("keygen", "encrypt"):
        rho = _rand(rng)
        times = []
        for t in range(8):
            slots, lo, _, _, ref = _case_inputs(name, rng)
            sd = bytes([0xFF] * 32) if t == 0 else bytes(32) if t == 1 else _rand(rng)
            ok, c = await _case(dut, name, slots, lo, rho, sd, None)
            assert ok, f"{name}: slots differ from the model (fixed rho, secret {t})"
            times.append(c)
        assert len(set(times)) == 1, f"{name}: cycle count depends on the secret: {times}"
        res[name] = times[0]
    dut._log.info(f"fixed rho, 8 different secrets: identical cycles per program {res} (VAR {VAR})")


@cocotb.test()
async def test_stall_coverage(dut):
    if VAR == M.STORE:
        return
    assert all(STALL[k] > 0 for k in ("first", "gap0", "gap1", "gap2_13", "gap14")), f"PWMS stall classes not all seen: {STALL}"
    dut._log.info(f"every PWMS stall class seen (before the first beat, back-to-back, gap 1, gap 2-13, gap >= 14 for a block boundary): {STALL}")
