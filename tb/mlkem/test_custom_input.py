"""tb/mlkem/test_custom_input.py -- try the ML-KEM-768 core (rtl/mlkem/mlkem_core.sv) with inputs of your own. Not part of the Phase 9 test plan; a demonstration helper.

Environment (set by tb/mlkem/try_custom.py): CUSTOM_D, CUSTOM_Z, CUSTOM_M (64 hex characters = 32 bytes each), CUSTOM_FLIP (byte index of the ciphertext to damage, default 5).
Flow: KeyGen(d, z) -> Encaps(ek, m) -> Decaps(dk, c) -> Decaps(dk, damaged c). Every RTL output is compared with the golden model (tb/golden/mlkem.py, FIPS 203 Algorithms 16-18); simulation only.
"""
import os

import cocotb
from core_tb import rtl_decaps, rtl_encaps, rtl_keygen, setup
from mlkem import ml_kem_decaps_internal, ml_kem_encaps_internal, ml_kem_keygen_internal


def hx(name):
    v = bytes.fromhex(os.environ[name])
    assert len(v) == 32, f"{name} must be 32 bytes (64 hex characters)"
    return v


@cocotb.test()
async def test_custom(dut):
    d, z, m = hx("CUSTOM_D"), hx("CUSTOM_Z"), hx("CUSTOM_M")
    flip = int(os.environ.get("CUSTOM_FLIP", "5"))
    await setup(dut)
    ok = True

    def line(name, good, extra=""):
        nonlocal ok
        ok &= good
        print(f"  {'OK  ' if good else 'FAIL'} {name} {extra}")

    print("\n=== ML-KEM-768 core, inputs ===")
    print(f"  d = {d.hex()}\n  z = {z.hex()}\n  m = {m.hex()}")
    ek, dk, cyc = await rtl_keygen(dut, d, z)
    ek_g, dk_g = ml_kem_keygen_internal(d, z)
    line("KeyGen: ek (1184 B) equals golden", ek == ek_g, f"({cyc} cycles)")
    line("KeyGen: dk (2400 B) equals golden", dk[:2400] == dk_g)
    k, c, cyc = await rtl_encaps(dut, ek, m)
    k_g, c_g = ml_kem_encaps_internal(ek_g, m)
    line("Encaps: ciphertext (1088 B) equals golden", c == c_g, f"({cyc} cycles)")
    line("Encaps: shared secret K equals golden", k == k_g)
    k2, cyc = await rtl_decaps(dut, dk[:2400], c)
    line("Decaps (valid c): K equals the Encaps K", k2 == k, f"({cyc} cycles)")
    bad = bytearray(c)
    bad[flip] ^= 0x01
    bad = bytes(bad)
    k3, cyc = await rtl_decaps(dut, dk[:2400], bad)
    k3_g = ml_kem_decaps_internal(dk_g, bad)
    line(f"Decaps (ciphertext byte {flip} damaged): K equals golden (implicit rejection)", k3 == k3_g, f"({cyc} cycles)")
    line("Decaps (damaged c): K differs from the real K", k3 != k)
    print(f"  shared secret K     = {k.hex()}\n  K after damaged c   = {k3.hex()}")
    print("=== RESULT:", "ALL OK" if ok else "MISMATCH", "===")
    assert ok
