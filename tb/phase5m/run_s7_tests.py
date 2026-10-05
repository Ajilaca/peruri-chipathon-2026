"""tb/phase5m/run_s7_tests.py -- Phase 5M step S7 verification (evidence/phase05m/test_plan_s7.md V2-V5) against one simulator.

Builds:
  mem1   rtl/mem/poly_mem_multiport_split.sv, RD_SPLIT = 1, ARB_REG = bits 4, 11, 16, WR_DELAY = 3: test_poly_mem_split (V2)
  mem0   same, RD_SPLIT = 0 (the model reduces to the Phase 4 one): test_poly_mem_split
  memdiff tb/phase5m/mem_diff_top.sv (frozen memory and RD_SPLIT = 0 side by side): test_poly_mem_diff (V3)
  s7     rtl/ntt/ntt_core_s7_p7.sv (revision S7): tb/phase5m/test_ntt_core_s7.py (Phase 4 core test adapted, plus the 512 INTT unit vectors) (V4);
         required cycles NTT = INTT = 120
  ncd    s7 with a mutant memory whose write control is delayed by WR_DELAY + RD_SPLIT - 1 (one cycle short): bit-exact NTT and INTT must FAIL (V5 NCD)
  ncs    s7 with a mutant memory whose output select is NOT delayed with the registered read data: bit-exact NTT and INTT must FAIL (V5 NCS)
Test-only mutants are written to the build directory; the repository RTL is never modified.
Usage: python3 tb/phase5m/run_s7_tests.py icarus|verilator [mem1 mem0 memdiff s7 ncd ncs]   (default: all)
Exit code 0 only if every selected build behaves as required.
"""

import json
import os
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from cocotb_tools.runner import get_runner

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
RTL_NTT, RTL_MEM, RTL_ARITH = ROOT / "rtl" / "ntt", ROOT / "rtl" / "mem", ROOT / "rtl" / "arith"
PKG = RTL_NTT / "ntt_pkg.sv"
SPLIT = RTL_MEM / "poly_mem_multiport_split.sv"
ARB = (1 << 4) | (1 << 11) | (1 << 16)
CORE_SOURCES = [
    PKG, RTL_NTT / "twiddle_rom.sv", RTL_ARITH / "twiddle_rom_half.sv", RTL_MEM / "bank_map_rom.sv", RTL_NTT / "pipe_delay.sv",
    RTL_NTT / "modmul_reduce_staged.sv", RTL_ARITH / "modmul_fold.sv", RTL_ARITH / "modmul_barrett.sv",
    RTL_ARITH / "modmul_montgomery.sv", RTL_ARITH / "modmul_sel.sv", RTL_ARITH / "half_mod.sv", RTL_ARITH / "butterfly_m6.sv",
    SPLIT, RTL_NTT / "ntt_core_s7.sv", RTL_NTT / "ntt_core_s7_p7.sv",
]


def mutate(src: Path, dst: Path, old: str, new: str, count: int = 1) -> Path:
    text = src.read_text()
    assert text.count(old) == count, f"{src.name}: pattern found {text.count(old)} times, expected {count}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text.replace(old, new))
    return dst


def build_test(sim, build_root, name, top, sources, module, test_dir, params=None, env=None):
    build_dir = build_root / f"sim_build_{sim}_s7_{name}"
    runner = get_runner(sim)
    runner.build(sources=sources, hdl_toplevel=top, build_dir=build_dir, parameters=params or {},
                 build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [], always=True)
    cycles_out = build_dir / "cycles.json"
    if cycles_out.exists():
        cycles_out.unlink()
    e = {"C3_CYCLES_OUT": str(cycles_out)}
    e.update(env or {})
    results = runner.test(hdl_toplevel=top, test_module=module, test_dir=test_dir, build_dir=build_dir,
                          results_xml=str(build_dir / "results.xml"), extra_env=e)
    cases = ET.parse(results).getroot().findall(".//testcase")
    ran = [c for c in cases if c.find("skipped") is None]
    failed = [c.get("name") for c in ran if c.find("failure") is not None or c.find("error") is not None]
    note = json.loads(cycles_out.read_text()) if cycles_out.exists() else {}
    return [c.get("name") for c in ran], failed, note


CORE_ENV = {"C3_RDLAT": "4", "C3_RDPHYS": "3", "C3_WRDLY": "3", "C3_CORE": "u_core", "C3_NEGCTL": "0"}


def run(sim, build_root, names):
    ok = True
    total = bad = 0
    for name in names:
        mdir = build_root / f"mut_{sim}_{name}"
        if name in ("mem1", "mem0"):
            sp = 1 if name == "mem1" else 0
            ran, failed, _ = build_test(sim, build_root, name, "poly_mem_multiport_split",
                                        [PKG, RTL_MEM / "bank_map_rom.sv", RTL_NTT / "pipe_delay.sv", SPLIT], "test_poly_mem_split", HERE,
                                        params={"NUM_LANES": 8, "ARB_REG": ARB, "WR_DELAY": 3, "RD_SPLIT": sp},
                                        env={"P7_ARB_REG": str(ARB), "P7_WR_DELAY": "3", "P7_RD_SPLIT": str(sp)})
            good = bool(ran) and not failed
            print(f"[{sim}] {name} (RD_SPLIT={sp}): {len(ran) - len(failed)}/{len(ran)} " + ("PASS" if good else f"FAIL {failed}"))
            total += len(ran)
            bad += len(failed) if failed else (0 if good else 1)
            ok &= good
        elif name == "memdiff":
            ran, failed, _ = build_test(sim, build_root, name, "mem_diff_top",
                                        [PKG, RTL_MEM / "bank_map_rom.sv", RTL_NTT / "pipe_delay.sv", RTL_MEM / "poly_mem_multiport_pipe.sv",
                                         SPLIT, HERE / "mem_diff_top.sv"], "test_poly_mem_diff", HERE,
                                        params={"ARB_REG": ARB, "WR_DELAY": 3})
            good = bool(ran) and not failed
            print(f"[{sim}] memdiff: {len(ran) - len(failed)}/{len(ran)} " + ("PASS" if good else f"FAIL {failed}"))
            total += len(ran)
            bad += len(failed) if failed else (0 if good else 1)
            ok &= good
        else:
            sources = list(CORE_SOURCES)
            if name == "ncd":
                m = mutate(SPLIT, mdir / "poly_mem_multiport_split.sv", ".STAGES(WR_DELAY + RD_SPLIT)", ".STAGES(WR_DELAY + RD_SPLIT - 1)", 4)
                sources = [m if s.name == SPLIT.name else s for s in sources]
            if name == "ncs":
                m = mutate(SPLIT, mdir / "poly_mem_multiport_split.sv", "assign bank_rs      = bank_rq2;", "assign bank_rs      = bank_r;")
                sources = [m if s.name == SPLIT.name else s for s in sources]
            ran, failed, note = build_test(sim, build_root, name, "ntt_core_s7_p7", sources, "test_ntt_core_s7", HERE, env=CORE_ENV)
            if name == "s7":
                good = bool(ran) and not failed and (note.get("cycles_NTT"), note.get("cycles_INTT")) == (120, 120)
                print(f"[{sim}] s7: {len(ran) - len(failed)}/{len(ran)} " + ("PASS" if good else f"FAIL {failed}") + f"  {note}")
                total += len(ran)
                bad += len(failed) if failed else (0 if good else 1)
                ok &= good
            else:
                good = "test_ntt_bit_exact" in failed and "test_intt_bit_exact" in failed
                print(f"[{sim}] {name}: bit-exact NTT and INTT failed as required: {good}; failed={failed}" + ("" if good else "  NEGATIVE CONTROL VOID"))
                total += 1
                bad += 0 if good else 1
                ok &= good
    print(f"[{sim}] TOTAL: {total - bad}/{total} passed")
    return ok


if __name__ == "__main__":
    sim_name = sys.argv[1] if len(sys.argv) > 1 else "icarus"
    selected = sys.argv[2:] or ["mem1", "mem0", "memdiff", "s7", "ncd", "ncs"]
    root = Path(os.environ.get("S7_BUILD_DIR") or tempfile.mkdtemp(prefix="chip2026_s7_"))
    sys.exit(0 if run(sim_name, root, selected) else 1)
