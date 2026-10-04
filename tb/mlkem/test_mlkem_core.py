"""tb/mlkem/test_mlkem_core.py -- Phase 9c tests V3-V6, V8 of rtl/mlkem/mlkem_core.sv: every pinned ACVP vector of ML-KEM-768 (keyGen, encapsulation, decapsulation), a random cross-check against the unmodified golden ml_kem_*_internal,
the chain KeyGen -> Encaps -> Decaps, protocol corner cases and constant cycles. Environment: CORE_FAST=1 (controls: a few vectors), CORE_N (random cases), CORE_CYCLES_OUT (json)."""
import json
import os
import random

import cocotb
from cocotb.triggers import FallingEdge
from core_tb import CB, FAST, KB, NRAND, R_D, R_K, R_M, RF, acvp_tests, read_words, rtl_decaps, rtl_encaps, rtl_keygen, run_op, setup, write_words  # noqa: F401
from mlkem import ml_kem_decaps_internal, ml_kem_encaps_internal, ml_kem_keygen_internal
from params import CT_BYTES
from primitives import H

CYCLES = {"keygen": [], "encaps": [], "decaps": []}


def rb(rng, n=32):
    return bytes(rng.randrange(256) for _ in range(n))


def pick(tests, key=None):
    if not FAST:
        return tests
    if key is None:
        return tests[:2]
    valid = [t for t in tests if t.get("reason", "valid decapsulation") == "valid decapsulation"][:1]
    bad = [t for t in tests if t.get("reason") == "modified ciphertext"][:2]
    return valid + bad


@cocotb.test()
async def test_acvp_keygen(dut):
    """V3: ACVP keyGen: ek and dk of every vector."""
    await setup(dut)
    tests = pick(acvp_tests("ML-KEM-keyGen-FIPS203"))
    for t in tests:
        ek, dk, cyc = await rtl_keygen(dut, bytes.fromhex(t["d"]), bytes.fromhex(t["z"]))
        CYCLES["keygen"].append(cyc)
        assert ek.hex() == t["ek"].lower(), f"keyGen tcId {t['tcId']}: ek differs"
        assert dk.hex() == t["dk"].lower(), f"keyGen tcId {t['tcId']}: dk differs"
    dut._log.info(f"ACVP keyGen: {len(tests)} vectors equal")


@cocotb.test()
async def test_acvp_encaps(dut):
    """V3: ACVP encapsulation: c and k of every vector."""
    await setup(dut)
    tests = pick(acvp_tests("ML-KEM-encapDecap-FIPS203", "encapsulation"))
    for t in tests:
        k, c, cyc = await rtl_encaps(dut, bytes.fromhex(t["ek"]), bytes.fromhex(t["m"]))
        CYCLES["encaps"].append(cyc)
        assert c.hex() == t["c"].lower(), f"encapsulation tcId {t['tcId']}: c differs"
        assert k.hex() == t["k"].lower(), f"encapsulation tcId {t['tcId']}: k differs"
    dut._log.info(f"ACVP encapsulation: {len(tests)} vectors equal")


@cocotb.test()
async def test_acvp_decaps(dut):
    """V3: ACVP decapsulation (valid and modified ciphertexts): k of every vector."""
    await setup(dut)
    tests = pick(acvp_tests("ML-KEM-encapDecap-FIPS203", "decapsulation"), key="reason")
    for t in tests:
        k, cyc = await rtl_decaps(dut, bytes.fromhex(t["dk"]), bytes.fromhex(t["c"]))
        CYCLES["decaps"].append(cyc)
        assert k.hex() == t["k"].lower(), f"decapsulation tcId {t['tcId']} ({t.get('reason')}): k differs"
    dut._log.info(f"ACVP decapsulation: {len(tests)} vectors equal")


@cocotb.test()
async def test_random_cross_check_and_chain(dut):
    """V4: random KeyGen, Encaps, Decaps (valid and one-bit-changed ciphertexts) against the unmodified golden, and the chain KeyGen -> Encaps -> Decaps through the RTL."""
    await setup(dut)
    rng = random.Random(980)
    n = 2 if FAST else NRAND
    for i in range(n):
        d, z, m = rb(rng), rb(rng), rb(rng)
        ek, dk, _ = await rtl_keygen(dut, d, z)
        assert (ek, dk) == ml_kem_keygen_internal(d, z), f"random keygen {i}"
        k, c, _ = await rtl_encaps(dut, ek, m)
        gk, gc = ml_kem_encaps_internal(ek, m)
        assert (k, c) == (gk, gc), f"random encaps {i}"
        k2, _ = await rtl_decaps(dut, dk, c)
        assert k2 == k == ml_kem_decaps_internal(dk, c), f"chain {i}"
        positions = (0, CT_BYTES - 1, 960, 959, rng.randrange(CT_BYTES))
        bad = bytearray(c)
        bad[positions[i % len(positions)]] ^= 1 << rng.randrange(8)
        k3, _ = await rtl_decaps(dut, dk, bytes(bad))
        assert k3 == ml_kem_decaps_internal(dk, bytes(bad)) and k3 != k, f"modified ciphertext {i}"
    dut._log.info(f"{n} random cases equal (keygen, encaps, decaps valid and modified, chain)")


@cocotb.test()
async def test_protocol_corner_cases(dut):
    """V5: start, op and host write while busy are ignored; reset in the middle then a clean operation; back to back operations with other keys."""
    await setup(dut)
    rng = random.Random(981)
    d, z, m = rb(rng), rb(rng), rb(rng)
    ek, dk = ml_kem_keygen_internal(d, z)
    # disturbances during an Encaps: start with another op, op change, host write into the ek that is being hashed
    await write_words(dut, KB, 144, ek)
    await write_words(dut, RF, R_M, m)

    def hook(cycle):
        if cycle == 5:
            dut.op_i.value = 2
            dut.start_i.value = 1
            dut.h_we_i.value = 1
            dut.h_addr_i.value = (KB << 10) | 144
            dut.h_wdata_i.value = 0xDEADBEEFDEADBEEF
        elif cycle == 6:
            dut.start_i.value = 0
            dut.h_we_i.value = 0

    await run_op(dut, 1, hook=hook)
    k = await read_words(dut, RF, R_K, 4)
    c = await read_words(dut, CB, 0, 136)
    gk, gc = ml_kem_encaps_internal(ek, m)
    assert (k, c) == (gk, gc), "a disturbance while busy changed the result"
    # reset in the middle of a Decaps, then a clean KeyGen
    await write_words(dut, KB, 0, dk)
    await write_words(dut, CB, 0, c)
    await FallingEdge(dut.clk_i)
    dut.op_i.value = 2
    dut.start_i.value = 1
    await FallingEdge(dut.clk_i)
    dut.start_i.value = 0
    for _ in range(2500):
        await FallingEdge(dut.clk_i)
    assert int(dut.busy_o.value) == 1
    dut.rst_ni.value = 0
    await FallingEdge(dut.clk_i)
    await FallingEdge(dut.clk_i)
    dut.rst_ni.value = 1
    await FallingEdge(dut.clk_i)
    assert int(dut.busy_o.value) == 0 and int(dut.done_o.value) == 0, "not idle after the reset"
    ek2, dk2, _ = await rtl_keygen(dut, d, z)
    assert (ek2, dk2) == (ek, dk), "KeyGen after a reset in the middle of a Decaps"
    # back to back: another key pair, Encaps then Decaps with another dk, the earlier buffers must not leak
    d2, z2, m2 = rb(rng), rb(rng), rb(rng)
    ekb, dkb = ml_kem_keygen_internal(d2, z2)
    kb, cb, _ = await rtl_encaps(dut, ekb, m2)
    assert (kb, cb) == ml_kem_encaps_internal(ekb, m2)
    k4, _ = await rtl_decaps(dut, dk, cb)               # a ciphertext for another key: implicit rejection
    assert k4 == ml_kem_decaps_internal(dk, cb) != kb
    # the shared secret register is held after done
    held = await read_words(dut, RF, R_K, 4)
    for _ in range(50):
        await FallingEdge(dut.clk_i)
    assert await read_words(dut, RF, R_K, 4) == held, "the shared secret changed after done"


@cocotb.test()
async def test_constant_cycles(dut):
    """V6: Decaps cycles identical for valid and rejected ciphertexts and for different secret keys with the same ek; Encaps identical for different m with the same ek; KeyGen spread reported."""
    await setup(dut)
    rng = random.Random(982)
    d, z, m = rb(rng), rb(rng), rb(rng)
    ek, dk = ml_kem_keygen_internal(d, z)
    dk_pke, h = dk[:1152], dk[2336:2368]
    assert h == H(ek)
    dec_cycles, enc_cycles = set(), set()
    n = 3 if FAST else 8
    for i in range(n):
        m_i = rb(rng)
        k, c, cyc = await rtl_encaps(dut, ek, m_i)
        assert (k, c) == ml_kem_encaps_internal(ek, m_i)
        enc_cycles.add(cyc)
        # different secret key, same ek: dk_pke and z changed, H(ek) consistent
        dk_i = rb(rng, 1152) + ek + h + rb(rng)
        for ct in (c, bytes(CT_BYTES), rb(rng, CT_BYTES)):
            kk, cyc = await rtl_decaps(dut, dk_i, ct)
            assert kk == ml_kem_decaps_internal(dk_i, ct), f"decaps {i}"
            dec_cycles.add(cyc)
        kk, cyc = await rtl_decaps(dut, dk, c)               # valid ciphertext with the true key
        assert kk == k
        dec_cycles.add(cyc)
    assert len(enc_cycles) == 1, f"Encaps cycles {sorted(enc_cycles)} depend on m"
    assert len(dec_cycles) == 1, f"Decaps cycles {sorted(dec_cycles)} depend on the ciphertext or the secret key"
    kg = set(CYCLES["keygen"])
    dut._log.info(f"constant cycles: Encaps {sorted(enc_cycles)}, Decaps {sorted(dec_cycles)}; KeyGen over the ACVP seeds: min {min(kg) if kg else None}, max {max(kg) if kg else None}")
    out = os.environ.get("CORE_CYCLES_OUT")
    if out:
        with open(out, "w") as f:
            json.dump({"encaps": sorted(enc_cycles), "decaps": sorted(dec_cycles), "keygen_min": min(kg) if kg else None, "keygen_max": max(kg) if kg else None,
                       "keygen_n": len(CYCLES["keygen"]), "encaps_acvp_min": min(CYCLES["encaps"]) if CYCLES["encaps"] else None, "encaps_acvp_max": max(CYCLES["encaps"]) if CYCLES["encaps"] else None,
                       "decaps_acvp_min": min(CYCLES["decaps"]) if CYCLES["decaps"] else None, "decaps_acvp_max": max(CYCLES["decaps"]) if CYCLES["decaps"] else None}, f)
