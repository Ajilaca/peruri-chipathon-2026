#!/usr/bin/env python3
"""tb/phase5m/check_half_rom.py — Phase 5M S6, test plan V4: rtl/arith/twiddle_rom_half.sv
  (1) is reproduced byte for byte by scripts/gen_twiddle_rom_half.py;
  (2) NTT half (entries 0..127) equals ROM_ZETA of the frozen rtl/ntt/twiddle_rom.sv;
  (3) INTT half (entries 128..255) equals zeta * 1665 mod q for every entry, with 2 * 1665 = 1 (mod q), computed here from the golden
      model independently of the generator's tables.
Exit code 0 only if all hold."""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tb" / "golden"))
import gen_twiddle_rom_half as gen  # noqa: E402
from params import Q  # noqa: E402
from primitives import ntt  # noqa: E402,F401  (golden import check)
import primitives  # noqa: E402

text = (ROOT / "rtl" / "arith" / "twiddle_rom_half.sv").read_text()
errs = []
if text != gen.render():
    errs.append("file differs from the generator output")
rom = {int(m.group(1)): int(m.group(2)) for m in re.finditer(r"rom_zeta\[(\d+)\] = 12'd(\d+);", text)}
frozen = (ROOT / "rtl" / "ntt" / "twiddle_rom.sv").read_text()
frozen_zeta = {int(m.group(1)): int(m.group(2)) for m in re.finditer(r"rom_zeta\[(\d+)\] = 12'd(\d+);", frozen)}
if len(rom) != 256 or len(frozen_zeta) != 128:
    errs.append(f"entry counts {len(rom)} / {len(frozen_zeta)}")
for i in range(128):
    if rom.get(i) != frozen_zeta.get(i):
        errs.append(f"NTT entry {i}: {rom.get(i)} != frozen {frozen_zeta.get(i)}")
    z = pow(primitives.ZETA, primitives._bitrev7(i), Q)
    if rom.get(i) != z:
        errs.append(f"NTT entry {i} != zeta^BitRev7({i})")
    if rom.get(128 + i) != (z * 1665) % Q or (rom.get(128 + i) * 2) % Q != z:
        errs.append(f"INTT entry {i} != zeta/2")
print("check_half_rom:", "OK, 256 entries (NTT half = frozen ROM, INTT half = zeta/2 mod q), generator reproduces the file"
      if not errs else f"FAIL {errs[:5]}")
sys.exit(1 if errs else 0)
