"""tb/ntt/run_ntt_c2_tests.py — runs the Phase 3 cocotb regression (rtl/ntt/ntt_core_c2.sv)
against one simulator, once per NUM_LANES in {1,2,4,8} (CRG-3: bit-exact on both simulators).

Usage: python3 tb/ntt/run_ntt_c2_tests.py icarus|verilator
Exit code 0 only if every testcase, for every L, passed.
"""

import os
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from cocotb_tools.runner import get_runner

HERE = Path(__file__).resolve().parent
RTL_NTT = HERE.parent.parent / "rtl" / "ntt"
RTL_MEM = HERE.parent.parent / "rtl" / "mem"

C2_SOURCES = [
    RTL_NTT / "ntt_pkg.sv", RTL_NTT / "twiddle_rom.sv", RTL_NTT / "modmul_reduce.sv",
    RTL_NTT / "base_case_multiply.sv", RTL_NTT / "butterfly.sv",
    RTL_MEM / "bank_map_rom.sv", RTL_MEM / "poly_mem_multiport.sv", RTL_NTT / "ntt_core_c2.sv",
]


def run_one(sim: str, build_root: Path, num_lanes: int) -> tuple[int, int, list[str]]:
    build_dir = build_root / f"sim_build_{sim}_L{num_lanes}"
    runner = get_runner(sim)
    runner.build(
        sources=C2_SOURCES,
        hdl_toplevel="ntt_core_c2",
        build_dir=build_dir,
        parameters={"NUM_LANES": num_lanes},
        build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [],
        always=True,
    )
    results = runner.test(
        hdl_toplevel="ntt_core_c2",
        test_module="test_ntt_core_c2",
        test_dir=HERE,
        build_dir=build_dir,
        results_xml=str(build_dir / "results.xml"),
        extra_env={"NTT_C2_L": str(num_lanes)},
    )
    root = ET.parse(results).getroot()
    cases = root.findall(".//testcase")
    failed = [c for c in cases if c.find("failure") is not None or c.find("error") is not None]
    names = [f"{c.get('classname')}::{c.get('name')}" for c in failed]
    return len(cases), len(failed), names


def run(sim: str, build_root: Path) -> bool:
    all_ok = True
    total_cases = total_failed = 0

    for L in (1, 2, 4, 8):
        n, f, names = run_one(sim, build_root, L)
        total_cases += n
        total_failed += f
        print(f"[{sim}] ntt_core_c2 L={L}: {n - f}/{n} PASS" if not f
              else f"[{sim}] ntt_core_c2 L={L}: {n - f}/{n} FAIL {names}")
        all_ok &= (f == 0 and n > 0)

    print(f"[{sim}] TOTAL: {total_cases - total_failed}/{total_cases} passed")
    return all_ok


if __name__ == "__main__":
    sim_name = sys.argv[1] if len(sys.argv) > 1 else "icarus"
    build_root = Path(os.environ.get("NTT_C2_BUILD_DIR") or tempfile.mkdtemp(prefix="chip2026_ntt_c2_"))
    ok = run(sim_name, build_root)
    sys.exit(0 if ok else 1)
