#!/usr/bin/env python3
"""tb/mlkem/try_custom.py -- run the ML-KEM-768 RTL core on your own d, z, m (simulation, Verilator by default).

Usage: . scripts/env.sh && python3 tb/mlkem/try_custom.py [--d HEX] [--z HEX] [--m HEX] [--flip N] [--sim verilator|icarus]
Each of d, z, m is 32 bytes = 64 hex characters; omitted values are random (the values used are printed). Compares the RTL with the golden model; not part of the Phase 9 test plan.
"""
import argparse
import os
import secrets
import sys
import tempfile
from pathlib import Path

from cocotb_tools.runner import get_runner

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_core_tests as R  # noqa: E402

ap = argparse.ArgumentParser()
for n in "dzm":
    ap.add_argument(f"--{n}", default=None, help="32 bytes as 64 hex characters (default: random)")
ap.add_argument("--flip", type=int, default=5, help="ciphertext byte index to damage for the rejection check")
ap.add_argument("--sim", default="verilator", choices=["verilator", "icarus"])
a = ap.parse_args()
vals = {n: (getattr(a, n) or secrets.token_hex(32)) for n in "dzm"}
for n, v in vals.items():
    if len(bytes.fromhex(v)) != 32:
        raise SystemExit(f"--{n} must be 64 hex characters")
root = Path(tempfile.mkdtemp(prefix="mlkem_custom_"))
r = get_runner(a.sim)
bd = root / "build"
r.build(sources=R.ENG + R.MLK, hdl_toplevel="mlkem_core", build_dir=bd, build_args=["--timing", "-Wno-fatal"] if a.sim == "verilator" else [], always=True)
env = {"CUSTOM_D": vals["d"], "CUSTOM_Z": vals["z"], "CUSTOM_M": vals["m"], "CUSTOM_FLIP": str(a.flip)}
res = r.test(hdl_toplevel="mlkem_core", test_module="test_custom_input", test_dir=HERE, build_dir=bd, results_xml=str(bd / "results.xml"), extra_env=env)
import xml.etree.ElementTree as ET  # noqa: E402
bad = [c for c in ET.parse(res).getroot().findall(".//testcase") if c.find("failure") is not None or c.find("error") is not None]
print("RESULT:", "MISMATCH" if bad else "RTL equals the golden model for these inputs")
sys.exit(1 if bad else 0)
