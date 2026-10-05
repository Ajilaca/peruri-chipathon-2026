"""tb/arith/run_c4_core_tests.py — Phase 5 core regression (evidence/phase05/test_plan.md V5, V6) against
one simulator, reusing the Phase 4 core test tb/ntt/test_ntt_core_c3.py unchanged (it drives the ports and samples
the core's internal memory request signals, which rtl/ntt/ntt_core_c4.sv keeps under the same names):
bit-exact NTT / INTT / round trip / boundary-directed data against tb/golden/primitives.py, the hazard scoreboard,
bank_overflow_o, and the constant cycle count. In addition this runner requires the measured cycle counts to be
exactly C3-P6's 119 / 375 (ADR 0011 D5: P = 6 and the schedule unchanged).

Builds:
  c4a     rtl/ntt/ntt_core_c4a.sv (fold reducer, the Quartus revision C4a)
  c4k0    rtl/ntt/ntt_core_c4.sv with RED_KIND = 0 and C3-P6's register positions (must behave as C3-P6)
  c4bb    rtl/ntt/ntt_core_c4b_b.sv (Barrett, revision C4b-B)
  c4bm    rtl/ntt/ntt_core_c4b_m.sv (Montgomery, revision C4b-M; Montgomery-form ROM and scaling constant)
  c4c     rtl/ntt/ntt_core_c4c.sv (Barrett + lazy INTT butterfly inputs, revision C4c, ADR 0014)
  negrom  ntt_core_c4b_m with a copy of rtl/arith/twiddle_rom_mont.sv in which rom_zeta[17] is changed (test-only,
          test plan V10): the bit-exact tests must FAIL (the build passes only if they do)
  negctl  rtl/ntt/ntt_core_c4.sv at depth 8 with WrDly = 8 (RdLat 0; RED_KIND = 0, the only reducer with 8 stage
          boundaries), beyond the schedule's slack of 7, test-only: the scoreboard must trip and the results must be
          wrong. The hazard depends on WrDly, not on P: the memory reads RdLat cycles after the request, so a build
          with RdLat 1 + WrDly 7 is physically safe (first attempt, evidence/phase05/5a/
          negctl_first_attempt_rd1_wr7.txt; test plan amendment A2).
Usage: python3 tb/arith/run_c4_core_tests.py icarus|verilator [c4a c4k0 negctl ...]   (default: all)
Exit code 0 only if every testcase of every selected build passed and the cycle counts are as required.
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
RTL_NTT = ROOT / "rtl" / "ntt"
RTL_MEM = ROOT / "rtl" / "mem"
RTL_ARITH = ROOT / "rtl" / "arith"
TB_NTT = ROOT / "tb" / "ntt"

COMMON_SOURCES = [
    RTL_NTT / "ntt_pkg.sv", RTL_NTT / "twiddle_rom.sv", RTL_MEM / "bank_map_rom.sv", RTL_NTT / "pipe_delay.sv",
    RTL_NTT / "modmul_reduce_staged.sv", RTL_ARITH / "modmul_fold.sv", RTL_ARITH / "modmul_barrett.sv",
    RTL_ARITH / "modmul_montgomery.sv", RTL_ARITH / "modmul_sel.sv", RTL_ARITH / "butterfly_c4.sv",
    RTL_ARITH / "lazy_bfly_io.sv", RTL_ARITH / "modmul_barrett_lazy.sv", RTL_ARITH / "butterfly_c4_lazy.sv",
    RTL_MEM / "poly_mem_multiport_pipe.sv", RTL_NTT / "ntt_core_c4.sv",
]
MONT_ROM = RTL_ARITH / "twiddle_rom_mont.sv"


def corrupted_mont_rom(dst: Path) -> Path:
    """Test-only copy of the Montgomery ROM with rom_zeta[17] + 1 (mod q); the repository file is untouched."""
    import re
    text = MONT_ROM.read_text()
    bad = re.sub(r"rom_zeta\[17\] = 12'd(\d+);", lambda m: f"rom_zeta[17] = 12'd{(int(m.group(1)) + 1) % 3329};", text)
    assert bad != text
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(bad)
    return dst
P6_ARB = (1 << 4) | (1 << 11) | (1 << 16)
# name -> (toplevel, extra sources, parameters, RDLAT, WRDLY, core instance, negctl, required cycles)
# required cycles = None for the scheduler negative control; "fail" for a build whose bit-exact tests must fail
BUILDS = {
    "c4a": ("ntt_core_c4a", [MONT_ROM, RTL_NTT / "ntt_core_c4a.sv"], {}, 3, 3, "u_core", False, (119, 375)),
    "c4k0": ("ntt_core_c4", [MONT_ROM], {"NUM_LANES": 8, "ARB_REG": P6_ARB, "RED_KIND": 0, "MUL_REG": 2081},
             3, 3, "", False, (119, 375)),
    "c4bb": ("ntt_core_c4b_b", [MONT_ROM, RTL_NTT / "ntt_core_c4b_b.sv"], {}, 3, 3, "u_core", False, (119, 375)),
    "c4bm": ("ntt_core_c4b_m", [MONT_ROM, RTL_NTT / "ntt_core_c4b_m.sv"], {}, 3, 3, "u_core", False, (119, 375)),
    "c4c": ("ntt_core_c4c", [MONT_ROM, RTL_NTT / "ntt_core_c4c.sv"], {}, 3, 3, "u_core", False, (119, 375)),
    "negrom": ("ntt_core_c4b_m", ["NEGROM", RTL_NTT / "ntt_core_c4b_m.sv"], {}, 3, 3, "u_core", False, "fail"),
    "negctl": ("ntt_core_c4", [MONT_ROM], {"NUM_LANES": 8, "ARB_REG": 0, "RED_KIND": 0, "MUL_REG": 0xFF},
               0, 8, "", True, None),
}


def run(sim: str, build_root: Path, names: list[str]) -> bool:
    ok, total, failed_total = True, 0, 0
    for name in names:
        top, extra, params, rdlat, wrdly, core, negctl, req = BUILDS[name]
        build_dir = build_root / f"sim_build_{sim}_c4_{name}"
        extra = [corrupted_mont_rom(build_root / f"negrom_{sim}" / "twiddle_rom_mont.sv") if e == "NEGROM" else e
                 for e in extra]
        cycles_out = build_dir / "cycles.json"
        runner = get_runner(sim)
        runner.build(sources=COMMON_SOURCES + extra, hdl_toplevel=top,
                     build_dir=build_dir, parameters=params,
                     build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [], always=True)
        if cycles_out.exists():
            cycles_out.unlink()
        results = runner.test(hdl_toplevel=top, test_module="test_ntt_core_c3", test_dir=TB_NTT,
                              build_dir=build_dir, results_xml=str(build_dir / "results.xml"),
                              extra_env={"C3_RDLAT": str(rdlat), "C3_WRDLY": str(wrdly), "C3_CORE": core,
                                         "C3_NEGCTL": "1" if negctl else "0",
                                         "C3_CYCLES_OUT": str(cycles_out)})
        cases = ET.parse(results).getroot().findall(".//testcase")
        ran = [c for c in cases if c.find("skipped") is None]
        failed = [c.get("name") for c in ran if c.find("failure") is not None or c.find("error") is not None]
        note = json.loads(cycles_out.read_text()) if cycles_out.exists() else {}
        cyc_ok = True
        if req == "fail":
            # V10: the build passes only if bit-exact tests fail (a wrong ROM entry must be detected)
            bitexact = [c.get("name") for c in ran if c.get("name") in ("test_ntt_bit_exact", "test_intt_bit_exact")]
            wrong = [n for n in failed if n in bitexact]
            ok_neg = len(bitexact) == 2 and len(wrong) == 2
            print(f"[{sim}] {name} ({top}): bit-exact tests failed as required: {wrong}" if ok_neg
                  else f"[{sim}] {name} ({top}): NEGATIVE CONTROL VOID, failed={failed}")
            total += 1
            failed_total += 0 if ok_neg else 1
            ok &= ok_neg
            continue
        if req is not None:
            cyc_ok = (note.get("cycles_NTT"), note.get("cycles_INTT")) == req
            if not cyc_ok:
                failed.append(f"cycles {note.get('cycles_NTT')}/{note.get('cycles_INTT')} != {req[0]}/{req[1]}")
        total += len(ran)
        failed_total += len(failed)
        print(f"[{sim}] {name} ({top}): {len(ran) - len(failed)}/{len(ran)} "
              + ("PASS" if ran and not failed else f"FAIL {failed}") + f"  {note}")
        ok &= bool(ran) and not failed and bool(note) and cyc_ok
    print(f"[{sim}] TOTAL: {total - failed_total}/{total} passed")
    return ok


if __name__ == "__main__":
    sim_name = sys.argv[1] if len(sys.argv) > 1 else "icarus"
    selected = sys.argv[2:] or list(BUILDS)
    root = Path(os.environ.get("C4_BUILD_DIR") or tempfile.mkdtemp(prefix="chip2026_c4_"))
    sys.exit(0 if run(sim_name, root, selected) else 1)
