"""tb/ntt/run_ntt_c3_tests.py — Phase 4 core regression (docs/evidence/phase04-pipeline/test_plan.md,
V5-V8) against one simulator: the three Quartus wrappers rtl/ntt/ntt_core_c3_p{2,4,6}.sv (the modules
that are actually compiled), then the negative control (rtl/ntt/ntt_core_c3.sv with a depth of 8, which
is beyond the schedule's slack; test-only, never compiled in Quartus).

Usage: python3 tb/ntt/run_ntt_c3_tests.py icarus|verilator [p2 p4 p6 negctl ...]   (default: all)
Exit code 0 only if every testcase of every selected build passed.
"""

import json
import os
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from cocotb_tools.runner import get_runner

HERE = Path(__file__).resolve().parent
RTL_NTT = HERE.parent.parent / "rtl" / "ntt"
RTL_MEM = HERE.parent.parent / "rtl" / "mem"

COMMON_SOURCES = [
    RTL_NTT / "ntt_pkg.sv", RTL_NTT / "twiddle_rom.sv", RTL_MEM / "bank_map_rom.sv",
    RTL_NTT / "pipe_delay.sv", RTL_NTT / "modmul_reduce_staged.sv", RTL_NTT / "butterfly_shared_pipe.sv",
    RTL_MEM / "poly_mem_multiport_pipe.sv", RTL_NTT / "ntt_core_c3.sv",
]
# name -> (toplevel, extra source, parameters, RDLAT, WRDLY, core instance, negctl)
BUILDS = {
    "p2": ("ntt_core_c3_p2", RTL_NTT / "ntt_core_c3_p2.sv", {}, 1, 1, "u_core", False),
    "p4": ("ntt_core_c3_p4", RTL_NTT / "ntt_core_c3_p4.sv", {}, 2, 2, "u_core", False),
    "p6": ("ntt_core_c3_p6", RTL_NTT / "ntt_core_c3_p6.sv", {}, 3, 3, "u_core", False),
    "negctl": ("ntt_core_c3", None, {"NUM_LANES": 8, "ARB_REG": 0, "MUL_REG": 0xFF}, 0, 8, "", True),
}


def run(sim: str, build_root: Path, names: list[str]) -> bool:
    ok, total, failed_total = True, 0, 0
    for name in names:
        top, extra, params, rdlat, wrdly, core, negctl = BUILDS[name]
        build_dir = build_root / f"sim_build_{sim}_c3_{name}"
        cycles_out = build_dir / "cycles.json"
        runner = get_runner(sim)
        runner.build(sources=COMMON_SOURCES + ([extra] if extra else []), hdl_toplevel=top,
                     build_dir=build_dir, parameters=params,
                     build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [], always=True)
        if cycles_out.exists():
            cycles_out.unlink()
        results = runner.test(hdl_toplevel=top, test_module="test_ntt_core_c3", test_dir=HERE,
                              build_dir=build_dir, results_xml=str(build_dir / "results.xml"),
                              extra_env={"C3_RDLAT": str(rdlat), "C3_WRDLY": str(wrdly), "C3_CORE": core,
                                         "C3_NEGCTL": "1" if negctl else "0",
                                         "C3_CYCLES_OUT": str(cycles_out)})
        cases = ET.parse(results).getroot().findall(".//testcase")
        ran = [c for c in cases if c.find("skipped") is None]
        failed = [c.get("name") for c in ran if c.find("failure") is not None or c.find("error") is not None]
        total += len(ran)
        failed_total += len(failed)
        note = json.loads(cycles_out.read_text()) if cycles_out.exists() else {}
        print(f"[{sim}] {name} ({top}): {len(ran) - len(failed)}/{len(ran)} "
              + ("PASS" if ran and not failed else f"FAIL {failed}") + f"  {note}")
        ok &= bool(ran) and not failed and bool(note)
    print(f"[{sim}] TOTAL: {total - failed_total}/{total} passed")
    return ok


if __name__ == "__main__":
    sim_name = sys.argv[1] if len(sys.argv) > 1 else "icarus"
    selected = sys.argv[2:] or list(BUILDS)
    root = Path(os.environ.get("P4_BUILD_DIR") or tempfile.mkdtemp(prefix="chip2026_c3_"))
    sys.exit(0 if run(sim_name, root, selected) else 1)
