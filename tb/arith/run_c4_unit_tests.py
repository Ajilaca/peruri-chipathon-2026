"""tb/arith/run_c4_unit_tests.py - Phase 5 cocotb unit tests (evidence/phase05/test_plan.md V3, V4)
against one simulator: the reducer behind rtl/arith/modmul_sel.sv and the C4 butterfly, for every register
configuration used.

Usage: python3 tb/arith/run_c4_unit_tests.py icarus|verilator [kind ...]     (default: kinds 0 1 2 3)
  kind 0 = frozen modmul_reduce_staged through modmul_sel (sanity: the C3-P6 configuration)
  kind 1 = rtl/arith/modmul_fold.sv (5a)
  kind 2 = rtl/arith/modmul_barrett.sv (5b), kind 3 = rtl/arith/modmul_montgomery.sv (5b)
Units are driven through tb/arith/c4_tb_wrappers.sv (pass-through except for kind 3, whose constant operand is
converted to Montgomery form there).
The 5c lazy units (modmul_barrett_lazy, butterfly_c4_lazy) are added after the kinds.
Exit code 0 only if every testcase passed.
"""

import os
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from cocotb_tools.runner import get_runner

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
RTL_NTT = ROOT / "rtl" / "ntt"
RTL_ARITH = ROOT / "rtl" / "arith"
TB_NTT = ROOT / "tb" / "ntt"

LAZY_SRC = [RTL_ARITH / "lazy_bfly_io.sv", RTL_ARITH / "modmul_barrett_lazy.sv", RTL_ARITH / "butterfly_c4_lazy.sv"]
REDUCERS = [RTL_NTT / "ntt_pkg.sv", RTL_NTT / "modmul_reduce_staged.sv", RTL_ARITH / "modmul_fold.sv",
            RTL_ARITH / "modmul_barrett.sv", RTL_ARITH / "modmul_montgomery.sv", RTL_ARITH / "modmul_sel.sv"]
TB_WRAP = HERE / "c4_tb_wrappers.sv"
# kind -> register configurations (REG_AFTER) used: combinational, and the P = 6 one (latency 3)
CONFIGS = {0: (0, 2081), 1: (0, 41), 2: (0, 7), 3: (0, 7)}


def units(kinds, lazy=True):
    out = []
    for kind in kinds:
        for reg in CONFIGS[kind]:
            out.append((f"modmul_c4_tb RED_KIND={kind} REG_AFTER={reg}", "modmul_c4_tb", REDUCERS + [TB_WRAP],
                        "test_reducer_c4",
                        HERE, {"RED_KIND": kind, "REG_AFTER": reg},
                        {"C4_RED_KIND": str(kind), "C4_REG_AFTER": str(reg)}))
        for reg in CONFIGS[kind]:
            # V4: the Phase 4 butterfly test (tb/ntt/test_butterfly_pipe.py) drives only the ports, which
            # butterfly_c4(_tb) shares with butterfly_shared_pipe; its MUL_REG comes from P4_MUL_REG.
            out.append((f"butterfly_c4_tb RED_KIND={kind} MUL_REG={reg}", "butterfly_c4_tb",
                        REDUCERS + [RTL_NTT / "pipe_delay.sv", RTL_ARITH / "butterfly_c4.sv", TB_WRAP],
                        "test_butterfly_pipe",
                        TB_NTT, {"RED_KIND": kind, "MUL_REG": reg}, {"P4_MUL_REG": str(reg)}))
    if lazy:
        # 5c (ADR 0014, test plan A4): the Barrett reducer with a 13-bit operand, and the lazy butterfly driven by the
        # unchanged Phase 4 butterfly test plus the lazy corner test; MUL_REG 0 (combinational) and 7 (cuts X, S1, S2).
        for reg in (0, 7):
            out.append((f"modmul_barrett_lazy REG_AFTER={reg} (a<q, b<q regression of 5b)", "modmul_barrett_lazy",
                        REDUCERS + LAZY_SRC, "test_reducer_c4_lazy_d6", HERE, {"REG_AFTER": reg},
                        {"C4_REG_AFTER": str(reg)}))
            for mod in ("test_butterfly_pipe", "test_lazy_corners"):
                out.append((f"butterfly_c4_lazy MUL_REG={reg} [{mod}]", "butterfly_c4_lazy",
                            REDUCERS + [RTL_NTT / "pipe_delay.sv"] + LAZY_SRC, mod,
                            TB_NTT if mod == "test_butterfly_pipe" else HERE, {"MUL_REG": reg},
                            {"P4_MUL_REG": str(reg)}))
    return out


def run(sim: str, build_root: Path, kinds) -> bool:
    ok, total, failed_total = True, 0, 0
    for i, (label, top, sources, test_module, test_dir, params, env) in enumerate(units(kinds)):
        build_dir = build_root / f"sim_build_{sim}_{top}_{i}"
        runner = get_runner(sim)
        runner.build(sources=sources, hdl_toplevel=top, build_dir=build_dir, parameters=params,
                     build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [], always=True)
        results = runner.test(hdl_toplevel=top, test_module=test_module, test_dir=test_dir, build_dir=build_dir,
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
    kinds = [int(k) for k in sys.argv[2:]] or [0, 1, 2, 3]
    root = Path(os.environ.get("C4_BUILD_DIR") or tempfile.mkdtemp(prefix="chip2026_c4u_"))
    sys.exit(0 if run(sim_name, root, kinds) else 1)
