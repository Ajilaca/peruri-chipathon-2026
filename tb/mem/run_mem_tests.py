"""tb/mem/run_mem_tests.py - runs every Phase 2 cocotb test module against one simulator
(CRG-3: bit-exact against the golden model, on both simulators).

Usage: python3 tb/mem/run_mem_tests.py icarus|verilator
Exit code 0 only if every testcase in every module (and every NUM_BANKS variant of
bank_map_rom) passed.
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

BANK_SOURCES = [RTL_NTT / "ntt_pkg.sv", RTL_MEM / "bank_map_rom.sv"]
C1_SOURCES = [
    RTL_NTT / "ntt_pkg.sv", RTL_NTT / "twiddle_rom.sv", RTL_NTT / "modmul_reduce.sv",
    RTL_NTT / "base_case_multiply.sv", RTL_NTT / "butterfly.sv",
    RTL_MEM / "bank_map_rom.sv", RTL_MEM / "poly_mem_banked.sv", RTL_MEM / "ntt_core_c1.sv",
]


def run_one(sim: str, build_root: Path, toplevel: str, sources, test_module: str,
            parameters=None, extra_env=None) -> tuple[int, int, list[str]]:
    tag = toplevel + ("_" + "_".join(f"{k}{v}" for k, v in (parameters or {}).items()) if parameters else "")
    build_dir = build_root / f"sim_build_{sim}_{tag}"
    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel=toplevel,
        build_dir=build_dir,
        parameters=parameters or {},
        build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [],
        always=True,
    )
    results = runner.test(
        hdl_toplevel=toplevel,
        test_module=test_module,
        test_dir=HERE,
        build_dir=build_dir,
        results_xml=str(build_dir / "results.xml"),
        extra_env=extra_env or {},
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
        n, f, names = run_one(sim, build_root, "bank_map_rom", BANK_SOURCES, "test_bank_map",
                              parameters={"NUM_BANKS": L}, extra_env={"BANK_MAP_L": str(L)})
        total_cases += n; total_failed += f
        print(f"[{sim}] bank_map_rom NUM_BANKS={L}: {n - f}/{n} PASS" if not f
              else f"[{sim}] bank_map_rom NUM_BANKS={L}: {n - f}/{n} FAIL {names}")
        all_ok &= (f == 0 and n > 0)

    n, f, names = run_one(sim, build_root, "ntt_core_c1", C1_SOURCES, "test_ntt_core_c1")
    total_cases += n; total_failed += f
    print(f"[{sim}] ntt_core_c1: {n - f}/{n} PASS" if not f else f"[{sim}] ntt_core_c1: {n - f}/{n} FAIL {names}")
    all_ok &= (f == 0 and n > 0)

    print(f"[{sim}] TOTAL: {total_cases - total_failed}/{total_cases} passed")
    return all_ok


if __name__ == "__main__":
    sim_name = sys.argv[1] if len(sys.argv) > 1 else "icarus"
    build_root = Path(os.environ.get("MEM_BUILD_DIR") or tempfile.mkdtemp(prefix="chip2026_mem_"))
    ok = run(sim_name, build_root)
    sys.exit(0 if ok else 1)
