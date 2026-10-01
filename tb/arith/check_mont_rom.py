#!/usr/bin/env python3
"""tb/arith/check_mont_rom.py — Phase 5b test plan V7 (generated tables).

Checks, without trusting the generator:
  1. every entry of rtl/arith/twiddle_rom_mont.sv satisfies  ROM_M[i] * R^-1 = ROM[i] (mod q), R = 2^12, against the
     frozen rtl/ntt/twiddle_rom.sv (zeta and gamma tables), and ROM[i] against tb/golden/primitives.py;
  2. every entry is in [0, q);
  3. re-running scripts/gen_twiddle_rom_mont.py's renderer reproduces the committed file byte for byte;
  4. negative control: a copy of the Montgomery ROM with one entry changed must fail check 1.
Usage: python3 tb/arith/check_mont_rom.py      exit code 0 only if 1-3 hold and 4 fails as required.
"""
import importlib.util
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tb" / "golden"))
from params import Q  # noqa: E402
from primitives import _GAMMA, _ZETA_BITREV  # noqa: E402

R = 1 << 12
R_INV = pow(R, -1, Q)


def parse(text: str, sig: str) -> list[int]:
    vals = {int(i): int(v) for i, v in re.findall(rf"{sig}\[(\d+)\] = 12'd(\d+);", text)}
    assert sorted(vals) == list(range(128)), f"{sig}: expected 128 entries"
    return [vals[i] for i in range(128)]


def check(mont_text: str) -> list[str]:
    ref_text = (ROOT / "rtl" / "ntt" / "twiddle_rom.sv").read_text()
    errs = []
    for sig, gold in (("rom_zeta", _ZETA_BITREV), ("rom_gamma", _GAMMA)):
        ref, mont = parse(ref_text, sig), parse(mont_text, sig)
        if ref != list(gold):
            errs.append(f"{sig}: frozen ROM differs from tb/golden")
        for i in range(128):
            if not 0 <= mont[i] < Q:
                errs.append(f"{sig}[{i}] = {mont[i]} out of range")
            if (mont[i] * R_INV) % Q != ref[i]:
                errs.append(f"{sig}[{i}]: {mont[i]} * R^-1 mod q != {ref[i]}")
    return errs


def main() -> int:
    path = ROOT / "rtl" / "arith" / "twiddle_rom_mont.sv"
    text = path.read_text()
    errs = check(text)
    print(f"check 1+2 (Montgomery relation and range, 256 entries): {'PASS' if not errs else 'FAIL ' + str(errs[:3])}")
    spec = importlib.util.spec_from_file_location("gen", ROOT / "scripts" / "gen_twiddle_rom_mont.py")
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    regen_ok = gen.render() == text
    print(f"check 3 (generator reproduces the file): {'PASS' if regen_ok else 'FAIL'}")
    bad = re.sub(r"rom_zeta\[17\] = 12'd(\d+);", lambda m: f"rom_zeta[17] = 12'd{(int(m.group(1)) + 1) % Q};", text)
    neg_errs = check(bad)
    print(f"check 4 (negative control, rom_zeta[17] + 1): {'fails as required' if neg_errs else 'DID NOT FAIL (check void)'}")
    ok = not errs and regen_ok and bool(neg_errs)
    print(f"RESULT: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
