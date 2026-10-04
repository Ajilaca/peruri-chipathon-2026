#!/usr/bin/env python3
"""tb/mlkem/profile_core.py -- Phase 9M: build rtl/mlkem/mlkem_core.sv and run tb/mlkem/test_profile_core.py (cycles per state and per micro-operation).
Usage: . scripts/env.sh && [CORE_W2=1] [CORE_K0=1] [CORE_TOP=mlkem_core2 CORE_SMP0=1] python3 tb/mlkem/profile_core.py OUT.json [verilator|icarus]   (CORE_W2=1: the Phase 9M two-byte load / store tasks)"""
import sys
import tempfile
from pathlib import Path

from cocotb_tools.runner import get_runner

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_core_tests as R  # noqa: E402

out = Path(sys.argv[1]).resolve()
sim = sys.argv[2] if len(sys.argv) > 2 else "verilator"
bd = Path(tempfile.mkdtemp(prefix="mlkem_prof_")) / "build"
r = get_runner(sim)
r.build(sources=R.ENG + R.MLK, hdl_toplevel=R.TOP, build_dir=bd, build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [], parameters=R.PARAMS, always=True)
r.test(hdl_toplevel=R.TOP, test_module="test_profile_core", test_dir=HERE, build_dir=bd, results_xml=str(bd / "results.xml"), extra_env={"PROF_OUT": str(out)})
print("written", out)
