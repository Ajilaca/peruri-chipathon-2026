"""Toolchain smoke test runner (NOT project verification).

Usage:  python3 run_smoke.py icarus|verilator
Builds in a temp directory (or $SMOKE_BUILD_DIR) so read-only or noexec
checkouts still work. Exit code 0 only if the cocotb test passed.
"""
import os
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from cocotb_tools.runner import get_runner

sim = sys.argv[1] if len(sys.argv) > 1 else "icarus"
here = Path(__file__).resolve().parent
build_root = Path(os.environ.get("SMOKE_BUILD_DIR") or tempfile.mkdtemp(prefix="chip2026_smoke_"))
build_dir = build_root / f"sim_build_{sim}"

runner = get_runner(sim)
runner.build(
    sources=[here / "smoke_counter.sv"],
    hdl_toplevel="smoke_counter",
    build_dir=build_dir,
    build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [],
    always=True,
)
results = runner.test(
    hdl_toplevel="smoke_counter",
    test_module="test_smoke_counter",
    test_dir=here,
    build_dir=build_dir,
    results_xml=str(build_dir / "results.xml"),
)
root = ET.parse(results).getroot()
cases = root.findall(".//testcase")
failed = [c for c in cases if c.find("failure") is not None or c.find("error") is not None]
print(f"SMOKE {sim}: {len(cases) - len(failed)}/{len(cases)} passed (build dir: {build_dir})")
sys.exit(1 if failed or not cases else 0)
