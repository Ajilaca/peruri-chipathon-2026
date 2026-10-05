"""tb/ntt/run_ntt_tests.py - runs every Phase 1 cocotb test module against one simulator
(CRG-3: "bit-exact against the golden model, on both simulators").

Usage: python3 tb/ntt/run_ntt_tests.py icarus|verilator [--build-dir DIR]
Exit code 0 only if every testcase in every module passed.
"""

import os
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from cocotb_tools.runner import get_runner

HERE = Path(__file__).resolve().parent
RTL_DIR = HERE.parent.parent / "rtl" / "ntt"

SOURCES = [
    RTL_DIR / "ntt_pkg.sv",
    RTL_DIR / "twiddle_rom.sv",
    RTL_DIR / "modmul_reduce.sv",
    RTL_DIR / "base_case_multiply.sv",
    RTL_DIR / "butterfly.sv",
    RTL_DIR / "poly_mem.sv",
    RTL_DIR / "ntt_core.sv",
]

# (hdl_toplevel, test_module)
UNITS = [
    ("modmul_reduce", "test_modmul"),
    ("base_case_multiply", "test_base_case_multiply"),
    ("butterfly", "test_butterfly"),
    ("ntt_core", "test_ntt_core"),
]


def run(sim: str, build_root: Path) -> bool:
    all_ok = True
    total_cases = 0
    total_failed = 0
    for toplevel, test_module in UNITS:
        build_dir = build_root / f"sim_build_{sim}_{toplevel}"
        runner = get_runner(sim)
        runner.build(
            sources=SOURCES,
            hdl_toplevel=toplevel,
            build_dir=build_dir,
            build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [],
            always=True,
        )
        results = runner.test(
            hdl_toplevel=toplevel,
            test_module=test_module,
            test_dir=HERE,
            build_dir=build_dir,
            results_xml=str(build_dir / "results.xml"),
        )
        root = ET.parse(results).getroot()
        cases = root.findall(".//testcase")
        failed = [c for c in cases if c.find("failure") is not None or c.find("error") is not None]
        total_cases += len(cases)
        total_failed += len(failed)
        status = "PASS" if (cases and not failed) else "FAIL"
        print(f"[{sim}] {toplevel} ({test_module}): {len(cases) - len(failed)}/{len(cases)} {status}")
        if failed or not cases:
            all_ok = False
            for c in failed:
                print(f"    FAILED: {c.get('classname')}::{c.get('name')}")
    print(f"[{sim}] TOTAL: {total_cases - total_failed}/{total_cases} passed")
    return all_ok


if __name__ == "__main__":
    sim_name = sys.argv[1] if len(sys.argv) > 1 else "icarus"
    build_root = Path(
        os.environ.get("NTT_BUILD_DIR") or tempfile.mkdtemp(prefix="chip2026_ntt_")
    )
    ok = run(sim_name, build_root)
    sys.exit(0 if ok else 1)
