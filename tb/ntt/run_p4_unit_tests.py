"""tb/ntt/run_p4_unit_tests.py — Phase 4 cocotb unit tests (evidence/phase04/test_plan.md,
V2-V4) against one simulator.

Usage: python3 tb/ntt/run_p4_unit_tests.py icarus|verilator
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
RTL_MEM = HERE.parent.parent / "rtl" / "mem"

# (label, toplevel, sources, test_module, parameters, extra_env)
UNITS = []
for reg_after, p in ((0, "-"), (8, "2"), (129, "4"), (2081, "6")):
    UNITS.append((f"modmul_reduce_staged REG_AFTER={reg_after} (P={p})", "modmul_reduce_staged",
                  [RTL_NTT / "ntt_pkg.sv", RTL_NTT / "modmul_reduce_staged.sv"], "test_modmul_staged",
                  {"REG_AFTER": reg_after}, {"P4_REG_AFTER": str(reg_after)}))
# V3: pipelined butterfly, same multiplier register configurations
for mul_reg, p in ((0, "-"), (8, "2"), (129, "4"), (2081, "6")):
    UNITS.append((f"butterfly_shared_pipe MUL_REG={mul_reg} (P={p})", "butterfly_shared_pipe",
                  [RTL_NTT / "ntt_pkg.sv", RTL_NTT / "pipe_delay.sv", RTL_NTT / "modmul_reduce_staged.sv",
                   RTL_NTT / "butterfly_shared_pipe.sv"], "test_butterfly_pipe",
                  {"MUL_REG": mul_reg}, {"P4_MUL_REG": str(mul_reg)}))
# V4: memory variant, (ARB_REG, WR_DELAY) of each P (test plan section 2) plus the unpipelined case
for arb_reg, wr_delay, p in ((0, 0, "-"), (1 << 13, 1, "2"), ((1 << 7) | (1 << 16), 2, "4"),
                             ((1 << 4) | (1 << 11) | (1 << 16), 3, "6")):
    UNITS.append((f"poly_mem_multiport_pipe ARB_REG={arb_reg:#x} WR_DELAY={wr_delay} (P={p})",
                  "poly_mem_multiport_pipe",
                  [RTL_NTT / "ntt_pkg.sv", RTL_MEM / "bank_map_rom.sv", RTL_NTT / "pipe_delay.sv",
                   RTL_MEM / "poly_mem_multiport_pipe.sv"], "test_poly_mem_pipe",
                  {"NUM_LANES": 8, "ARB_REG": arb_reg, "WR_DELAY": wr_delay},
                  {"P4_ARB_REG": str(arb_reg), "P4_WR_DELAY": str(wr_delay)}))


def run(sim: str, build_root: Path) -> bool:
    ok, total, failed_total = True, 0, 0
    for i, (label, top, sources, test_module, params, env) in enumerate(UNITS):
        build_dir = build_root / f"sim_build_{sim}_{top}_{i}"
        runner = get_runner(sim)
        runner.build(sources=sources, hdl_toplevel=top, build_dir=build_dir, parameters=params,
                     build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [], always=True)
        results = runner.test(hdl_toplevel=top, test_module=test_module, test_dir=HERE, build_dir=build_dir,
                              results_xml=str(build_dir / "results.xml"), extra_env=env)
        cases = ET.parse(results).getroot().findall(".//testcase")
        failed = [c.get("name") for c in cases if c.find("failure") is not None or c.find("error") is not None]
        total += len(cases)
        failed_total += len(failed)
        print(f"[{sim}] {label}: {len(cases) - len(failed)}/{len(cases)} " + ("PASS" if not failed else f"FAIL {failed}"))
        ok &= bool(cases) and not failed
    print(f"[{sim}] TOTAL: {total - failed_total}/{total} passed")
    return ok


if __name__ == "__main__":
    sim_name = sys.argv[1] if len(sys.argv) > 1 else "icarus"
    root = Path(os.environ.get("P4_BUILD_DIR") or tempfile.mkdtemp(prefix="chip2026_p4_"))
    sys.exit(0 if run(sim_name, root) else 1)
