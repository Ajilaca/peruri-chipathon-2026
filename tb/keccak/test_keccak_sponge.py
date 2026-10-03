"""tb/keccak/test_keccak_sponge.py -- Phase 7 test plan V5 and V6: rtl/keccak/keccak_sponge.sv (K0) against hashlib and the golden sponge.
V5: all four modes; message lengths 0, 1, 7, 8, 9, rate -1, rate, rate +1, 2 rate -1, 2 rate, 2 rate +1, 3 rate and the ML-KEM-768 lengths 32, 33, 34, 64, 1120, 1184 plus random
    lengths; SHA3 digests; SHAKE outputs of 1 word up to 5 blocks; garbage in the ignored bytes of the last word; random back-pressure on both interfaces; stop in the middle of
    absorb, of a permutation and of a squeeze; start while busy ignored; reset in the middle of a message; perm_cnt_o equal to the golden permutation count.
V6: for each (mode, length, output words) three messages (random, all-0x00, all-0xFF) give identical cycle counts without back-pressure; the cycle table is written to KK_CYCLES_OUT
    (json) and every point is compared with the formula derived from the FSM (see _formula).
Environment: KK_NEGCTL=1 builds a mutant: the test passes only if a bit-exact comparison FAILS (checked by the runner through the failing test names). KK_CYCLES_OUT, KK_SEEDS.
"""
import hashlib
import json
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "golden"))

import cocotb
import keccak as K
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge

NSEEDS = int(os.environ.get("KK_SEEDS", "20"))
CYCLES_OUT = os.environ.get("KK_CYCLES_OUT", "")
MODES = ["sha3_256", "sha3_512", "shake_128", "shake_256"]
RATE = {"sha3_256": 136, "sha3_512": 72, "shake_128": 168, "shake_256": 136}
RW = {m: RATE[m] // 8 for m in MODES}
FIXED_WORDS = {"sha3_256": 4, "sha3_512": 8}
ML = [32, 33, 34, 64, 1120, 1184]
PERM_CYCLES = 26  # run cycle + 24 busy cycles + done cycle, as seen by the controller


def _ref(mode, msg, nbytes):
    h = getattr(hashlib, mode)(msg)
    return h.digest() if mode.startswith("sha3") else h.digest(nbytes)


def _formula(mode, ln, ow):
    """Cycles from the start cycle to the cycle that accepts the last output word (no back-pressure), derived from the FSM of keccak_sponge.sv."""
    rate = RATE[mode]
    rw = RW[mode]
    pad2 = 0 if (ln % rate) // 8 == rw - 1 else 1
    absorb_perms = ln // rate + 1
    return 1 + (ln // 8 + 1) + pad2 + PERM_CYCLES * absorb_perms + ow + PERM_CYCLES * ((ow - 1) // rw)


async def _setup(dut):
    cocotb.start_soon(Clock(dut.clk_i, 10, unit="ns").start())
    dut.rst_ni.value = 0
    dut.start_i.value = 0
    dut.mode_i.value = 0
    dut.len_i.value = 0
    dut.stop_i.value = 0
    dut.in_valid_i.value = 0
    dut.in_data_i.value = 0
    dut.out_ready_i.value = 0
    await ClockCycles(dut.clk_i, 3)
    await FallingEdge(dut.clk_i)
    dut.rst_ni.value = 1


def _words(msg, rng):
    """64-bit input words; bytes past the message in the last word are garbage."""
    out = []
    for w in range(-(-len(msg) // 8)):
        chunk = msg[8 * w: 8 * w + 8]
        chunk = chunk + bytes(rng.randrange(256) for _ in range(8 - len(chunk)))
        out.append(int.from_bytes(chunk, "little"))
    return out


async def hash_call(dut, mode, msg, ow, rng=None, gaps=False, garbage=True, stop_after_absorb_cycles=None):
    """Runs one hash: returns (digest words as bytes, cycles from start to the last accepted output word, perm_cnt at that moment).
    stop_after_absorb_cycles: abort after that many cycles (returns None)."""
    grng = rng or random.Random(0)
    words = _words(msg, grng if garbage else random.Random(1)) if garbage else [int.from_bytes((msg[8 * w: 8 * w + 8]).ljust(8, b"\0"), "little") for w in range(-(-len(msg) // 8))]
    mi = MODES.index(mode)
    await FallingEdge(dut.clk_i)
    dut.start_i.value, dut.mode_i.value, dut.len_i.value = 1, mi, len(msg)
    await FallingEdge(dut.clk_i)
    dut.start_i.value = 0
    cycles = 1
    wi = 0
    got = []
    fixed = mode in FIXED_WORDS
    while True:
        cycles += 1
        if stop_after_absorb_cycles is not None and cycles > stop_after_absorb_cycles:
            dut.stop_i.value = 1
            dut.in_valid_i.value = 0
            dut.out_ready_i.value = 0
            await FallingEdge(dut.clk_i)
            dut.stop_i.value = 0
            return None
        if cycles > 20000:
            raise AssertionError("hash did not finish")
        # input side
        go_in = wi < len(words) and (not gaps or grng.random() < 0.7)
        dut.in_valid_i.value = 1 if go_in else 0
        dut.in_data_i.value = words[wi] if wi < len(words) else grng.getrandbits(64)
        go_out = (not gaps) or grng.random() < 0.7
        dut.out_ready_i.value = 1 if go_out else 0
        in_ready, out_valid = int(dut.in_ready_o.value), int(dut.out_valid_o.value)
        in_fire = go_in and in_ready
        out_fire = go_out and out_valid
        if out_fire:
            got.append(int(dut.out_data_o.value))
            if fixed and len(got) == FIXED_WORDS[mode]:
                assert int(dut.out_last_o.value) == 1, "out_last_o missing on the last digest word"
            elif int(dut.out_last_o.value):
                assert fixed, "out_last_o on a SHAKE word"
            pc = int(dut.perm_cnt_o.value)
            if len(got) == ow:
                dut.in_valid_i.value = 0  # out_ready_i stays high until the edge that accepts this word has passed
                if not fixed:
                    dut.stop_i.value = 1
                await FallingEdge(dut.clk_i)
                dut.stop_i.value = 0
                dut.out_ready_i.value = 0
                if fixed:
                    await FallingEdge(dut.clk_i)
                    assert int(dut.busy_o.value) == 0, "not IDLE after the digest"
                return b"".join(w.to_bytes(8, "little") for w in got), cycles, pc
        if in_fire:
            wi += 1
        await FallingEdge(dut.clk_i)


def _lengths(mode):
    r = RATE[mode]
    return sorted({0, 1, 7, 8, 9, r - 1, r, r + 1, 2 * r - 1, 2 * r, 2 * r + 1, 3 * r} | set(ML))


def _outs(mode):
    if mode in FIXED_WORDS:
        return [FIXED_WORDS[mode]]
    rw = RW[mode]
    outs = [1, 2, rw - 1, rw, rw + 1, 3 * rw, 5 * rw]
    if mode == "shake_256":
        outs += [16, 4]  # PRF eta = 2 (128 B) and J (32 B)
    else:
        outs += [105]  # SampleNTT stream up to 840 B
    return sorted(set(outs))


@cocotb.test()
async def test_modes_bit_exact(dut):
    await _setup(dut)
    rng = random.Random(720)
    n = 0
    for mode in MODES:
        for ln in _lengths(mode) + [rng.randrange(1201) for _ in range(NSEEDS)]:
            msg = bytes(rng.randrange(256) for _ in range(ln))
            for ow in _outs(mode):
                if ln in (1184, 1120) and ow not in (FIXED_WORDS.get(mode, ow), 1, RW[mode] + 1):
                    continue
                out, _, pc = await hash_call(dut, mode, msg, ow, rng)
                assert out == _ref(mode, msg, 8 * ow), f"{mode} len {ln} out {ow} words: digest differs from hashlib"
                assert out == (K.sha3_256(msg) if mode == "sha3_256" else K.sha3_512(msg) if mode == "sha3_512" else getattr(K, mode)(msg, 8 * ow)), "golden sponge differs"
                assert pc == K.num_perms(mode, ln, 8 * ow), f"{mode} len {ln} out {ow}: perm_cnt_o {pc}, golden {K.num_perms(mode, ln, 8 * ow)}"
                n += 1
    dut._log.info(f"{n} (mode, length, output) cases bit-exact against hashlib and the golden sponge, permutation counts equal")


@cocotb.test()
async def test_backpressure(dut):
    await _setup(dut)
    rng = random.Random(721)
    n = 0
    for mode in MODES:
        for ln in (0, 5, RATE[mode] - 1, RATE[mode], RATE[mode] + 9, 2 * RATE[mode] + 1, 300):
            msg = bytes(rng.randrange(256) for _ in range(ln))
            for ow in ([FIXED_WORDS[mode]] if mode in FIXED_WORDS else [3, RW[mode] + 2]):
                out, _, _ = await hash_call(dut, mode, msg, ow, rng, gaps=True)
                assert out == _ref(mode, msg, 8 * ow), f"{mode} len {ln} out {ow} with back-pressure"
                n += 1
    dut._log.info(f"{n} cases with random gaps on in_valid_i and out_ready_i bit-exact")


@cocotb.test()
async def test_stop_start_reset(dut):
    await _setup(dut)
    rng = random.Random(722)
    msg = bytes(rng.randrange(256) for _ in range(300))
    # stop in the middle of absorb, of a permutation and of a squeeze; the stop cycle is chosen from the FSM formula so that it falls inside the intended phase
    f1 = _formula("shake_128", 300, 1)  # cycle of the first output word of SHAKE128 over 300 bytes
    cases = [("sha3_256", 4, 20),                             # absorb (block 1 takes cycles 2..18)
             ("sha3_256", 4, 1 + 17 + 8),                     # inside the first permutation
             ("sha3_256", 4, _formula("sha3_256", 300, 4) - 2),  # squeeze (two digest words accepted)
             ("shake_128", 30, f1 + 5),                       # squeeze, first block
             ("shake_128", 30, f1 + 30)]                      # permutation between two squeeze blocks
    for mode, ow, cyc in cases:
        r = await hash_call(dut, mode, msg, ow, rng, stop_after_absorb_cycles=cyc)
        assert r is None, f"{mode}: finished before the stop cycle {cyc}"
        await FallingEdge(dut.clk_i)
        assert int(dut.busy_o.value) == 0, f"stop did not reach IDLE ({mode}, {cyc})"
        out, _, _ = await hash_call(dut, "sha3_512", msg, 8, rng)
        assert out == _ref("sha3_512", msg, 64), f"hash after a stop in the middle ({mode}, {cyc})"
        out, _, _ = await hash_call(dut, "shake_256", msg, 5, rng)
        assert out == _ref("shake_256", msg, 40)
    # start while busy ignored
    await FallingEdge(dut.clk_i)
    dut.start_i.value, dut.mode_i.value, dut.len_i.value = 1, 2, 10
    await FallingEdge(dut.clk_i)
    dut.start_i.value = 0
    for _ in range(3):
        await FallingEdge(dut.clk_i)
    dut.start_i.value, dut.mode_i.value, dut.len_i.value = 1, 0, 500  # busy: must be ignored (message is 10 bytes, SHAKE128)
    words = _words(bytes(range(10)), rng)
    wi = 0
    got = []
    for _ in range(200):
        dut.in_valid_i.value = 1 if wi < len(words) else 0
        dut.in_data_i.value = words[wi] if wi < len(words) else 0
        dut.out_ready_i.value = 1
        if wi < len(words) and int(dut.in_ready_o.value):
            wi += 1
        if int(dut.out_valid_o.value):
            got.append(int(dut.out_data_o.value))
        if len(got) == 2:
            break
        await FallingEdge(dut.clk_i)
        dut.start_i.value = 0
    dut.in_valid_i.value = 0
    dut.out_ready_i.value = 0
    dut.stop_i.value = 1
    await FallingEdge(dut.clk_i)
    dut.stop_i.value = 0
    assert b"".join(w.to_bytes(8, "little") for w in got) == hashlib.shake_128(bytes(range(10))).digest(16), "start while busy changed the running message"
    # reset in the middle of a message, then a normal hash
    await FallingEdge(dut.clk_i)
    dut.start_i.value, dut.mode_i.value, dut.len_i.value = 1, 3, 400
    await FallingEdge(dut.clk_i)
    dut.start_i.value = 0
    await ClockCycles(dut.clk_i, 30)
    await FallingEdge(dut.clk_i)
    dut.rst_ni.value = 0
    await ClockCycles(dut.clk_i, 2)
    await FallingEdge(dut.clk_i)
    dut.rst_ni.value = 1
    await FallingEdge(dut.clk_i)
    assert int(dut.busy_o.value) == 0
    out, _, _ = await hash_call(dut, "sha3_256", msg, 4, rng)
    assert out == _ref("sha3_256", msg, 32), "hash after reset in the middle of a message"
    dut._log.info("stop (absorb, permutation, squeeze), start while busy, reset mid-message: OK")


@cocotb.test()
async def test_constant_cycles(dut):
    await _setup(dut)
    rng = random.Random(723)
    table = {}
    for mode in MODES:
        for ln in _lengths(mode):
            for ow in _outs(mode):
                if ln in (1184, 1120) and ow not in (FIXED_WORDS.get(mode, ow), RW[mode] + 1):
                    continue
                seen = set()
                for kind in ("rand", "zero", "ones"):
                    msg = bytes(rng.randrange(256) for _ in range(ln)) if kind == "rand" else (bytes(ln) if kind == "zero" else b"\xff" * ln)
                    out, cyc, _ = await hash_call(dut, mode, msg, ow, rng)
                    assert out == _ref(mode, msg, 8 * ow)
                    seen.add(cyc)
                assert len(seen) == 1, f"{mode} len {ln} out {ow}: cycle count depends on the data: {seen}"
                cyc = seen.pop()
                assert cyc == _formula(mode, ln, ow), f"{mode} len {ln} out {ow}: {cyc} cycles, formula {_formula(mode, ln, ow)}"
                table[f"{mode}/{ln}/{ow}"] = cyc
    if CYCLES_OUT:
        Path(CYCLES_OUT).write_text(json.dumps(table, indent=0) + "\n")
    dut._log.info(f"{len(table)} (mode, length, output) points: identical cycles for random, all-0x00 and all-0xFF messages; every point equals the FSM formula")
