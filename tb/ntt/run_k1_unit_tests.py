"""tb/ntt/run_k1_unit_tests.py - experiment K1: runs the unchanged Phase 1 butterfly unit test
(tb/ntt/test_butterfly.py: corner cases + 1000 random (a, b, zeta) per mode, bit-exact against the
golden per-butterfly step of tb/golden/primitives.py) against rtl/ntt/butterfly_shared.sv.

Usage: python3 tb/ntt/run_k1_unit_tests.py icarus|verilator
Exit code 0 only if every testcase passed.
"""

import os
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from cocotb_tools.runner import get_runner

HERE = Path(__file__).resolve().parent
RTL_NTT = HERE.parent.parent / "rtl" / "ntt"
SOURCES = [RTL_NTT / "ntt_pkg.sv", RTL_NTT / "modmul_reduce.sv", RTL_NTT / "butterfly_shared.sv"]


def run(sim: str, build_root: Path) -> bool:
    build_dir = build_root / f"sim_build_{sim}_butterfly_shared"
    runner = get_runner(sim)
    runner.build(sources=SOURCES, hdl_toplevel="butterfly_shared", build_dir=build_dir,
                 build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [], always=True)
    results = runner.test(hdl_toplevel="butterfly_shared", test_module="test_butterfly", test_dir=HERE,
                          build_dir=build_dir, results_xml=str(build_dir / "results.xml"))
    cases = ET.parse(results).getroot().findall(".//testcase")
    failed = [c for c in cases if c.find("failure") is not None or c.find("error") is not None]
    print(f"[{sim}] butterfly_shared (test_butterfly): {len(cases) - len(failed)}/{len(cases)} "
          + ("PASS" if not failed else f"FAIL {[c.get('name') for c in failed]}"))
    return bool(cases) and not failed


if __name__ == "__main__":
    sim_name = sys.argv[1] if len(sys.argv) > 1 else "icarus"
    root = Path(os.environ.get("K1_BUILD_DIR") or tempfile.mkdtemp(prefix="chip2026_k1_"))
    sys.exit(0 if run(sim_name, root) else 1)
