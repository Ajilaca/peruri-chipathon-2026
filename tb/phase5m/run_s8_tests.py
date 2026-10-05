"""tb/phase5m/run_s8_tests.py -- Phase 5M step S8 verification (evidence/phase05m/test_plan_s8.md V2-V4, V6) against one simulator.

Builds:
  mem4   rtl/mem/poly_mem_multiport_split.sv at the S8 write delay: RD_SPLIT = 1, ARB_REG = bits 4, 11, 16, WR_DELAY = 4: test_poly_mem_split (V6)
  s8     rtl/ntt/ntt_core_s8_p8.sv (revision S8): tb/phase5m/test_ntt_core_s8.py (V2); required cycles NTT = INTT = 122
  ncb    s8 with the bubble removed (test-only copy, `Stall = 0`): bit-exact NTT and INTT must FAIL (V3 NC-B)
  ncw    s8 whose memory write control is NOT delayed by the write-path register (`WR_DELAY = WrDly`): bit-exact NTT and INTT must FAIL (V4 NC-W)
Test-only mutants are written to the build directory; the repository RTL is never modified.
Usage: python3 tb/phase5m/run_s8_tests.py icarus|verilator [mem4 s8 ncb ncw]   (default: all)
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
    SPLIT, RTL_NTT / "ntt_core_s8.sv", RTL_NTT / "ntt_core_s8_p8.sv",
]


def mutate(src: Path, dst: Path, old: str, new: str, count: int = 1) -> Path:
    text = src.read_text()
    assert text.count(old) == count, f"{src.name}: pattern found {text.count(old)} times, expected {count}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text.replace(old, new))
    return dst


def build_test(sim, build_root, name, top, sources, module, test_dir, params=None, env=None):
    build_dir = build_root / f"sim_build_{sim}_s8_{name}"
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


CORE_ENV = {"C3_RDLAT": "4", "C3_RDPHYS": "3", "C3_WRDLY": "4", "C3_CORE": "u_core", "C3_NEGCTL": "0"}


def run(sim, build_root, names):
    ok = True
    total = bad = 0
    for name in names:
        mdir = build_root / f"mut_{sim}_{name}"
        if name == "mem4":
            ran, failed, _ = build_test(sim, build_root, name, "poly_mem_multiport_split",
                                        [PKG, RTL_MEM / "bank_map_rom.sv", RTL_NTT / "pipe_delay.sv", SPLIT], "test_poly_mem_split", HERE,
                                        params={"NUM_LANES": 8, "ARB_REG": ARB, "WR_DELAY": 4, "RD_SPLIT": 1},
                                        env={"P7_ARB_REG": str(ARB), "P7_WR_DELAY": "4", "P7_RD_SPLIT": "1"})
            good = bool(ran) and not failed
            print(f"[{sim}] mem4 (RD_SPLIT=1, WR_DELAY=4): {len(ran) - len(failed)}/{len(ran)} " + ("PASS" if good else f"FAIL {failed}"))
            total += len(ran)
            bad += len(failed) if failed else (0 if good else 1)
            ok &= good
        else:
            sources = list(CORE_SOURCES)
            core = RTL_NTT / "ntt_core_s8.sv"
            if name == "ncb":
                m = mutate(core, mdir / "ntt_core_s8.sv", "localparam bit Stall = (WR_REG != 0);", "localparam bit Stall = 1'b0;")
                sources = [m if s.name == core.name else s for s in sources]
            if name == "ncw":
                m = mutate(core, mdir / "ntt_core_s8.sv", ".WR_DELAY(WrDly + WR_REG),", ".WR_DELAY(WrDly),")
                sources = [m if s.name == core.name else s for s in sources]
            ran, failed, note = build_test(sim, build_root, name, "ntt_core_s8_p8", sources, "test_ntt_core_s8", HERE, env=CORE_ENV)
            if name == "s8":
                good = bool(ran) and not failed and (note.get("cycles_NTT"), note.get("cycles_INTT")) == (122, 122)
                print(f"[{sim}] s8: {len(ran) - len(failed)}/{len(ran)} " + ("PASS" if good else f"FAIL {failed}") + f"  {note}")
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
    selected = sys.argv[2:] or ["mem4", "s8", "ncb", "ncw"]
    root = Path(os.environ.get("S8_BUILD_DIR") or tempfile.mkdtemp(prefix="chip2026_s8_"))
    sys.exit(0 if run(sim_name, root, selected) else 1)
