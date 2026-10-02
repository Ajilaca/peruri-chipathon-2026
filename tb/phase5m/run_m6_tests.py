"""tb/phase5m/run_m6_tests.py — Phase 5M step S6 verification (docs/evidence/phase05m-memsched/test_plan.md V2, V5, V6, V7) against
one simulator.

Builds:
  half     rtl/arith/half_mod.sv, exhaustive over all 3,329 inputs (V2)
  halfneg  half_mod mutant (adds q for EVEN inputs): test_half_mod must FAIL (V2 negative control)
  m6       rtl/ntt/ntt_core_m6_p6.sv (revision M6):
             - the Phase 4 core test tb/ntt/test_ntt_core_c3.py UNCHANGED (bit-exact NTT, INTT against the FIPS 203 intt() with its
               3303 scaling, round trip, boundary-directed data, constant cycles, hazard scoreboard, bank_overflow_o) (V5);
               required cycles NTT = INTT = 119
             - tb/phase5m/test_m6_basis.py: 256 unit vectors and 256 (q-1) unit vectors, equal to intt() and intt_halving() (V6)
  nch      m6 with a mutant butterfly_m6.sv whose INTT a-path skips the halving: the INTT bit-exact test must FAIL (V7 NCH)
  ncr      m6 with a mutant twiddle_rom_half.sv whose INTT entries of layer 3 (indices 8..15) are not halved: the INTT bit-exact test
           must FAIL, the NTT bit-exact test must PASS (V7 NCR)
Test-only mutants are written to the build directory; the repository RTL is never modified.
Usage: python3 tb/phase5m/run_m6_tests.py icarus|verilator [half halfneg m6 nch ncr]   (default: all)
Exit code 0 only if every selected build behaves as required.
"""

import json
import os
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from cocotb_tools.runner import get_runner

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
RTL_NTT, RTL_MEM, RTL_ARITH = ROOT / "rtl" / "ntt", ROOT / "rtl" / "mem", ROOT / "rtl" / "arith"
TB_NTT = ROOT / "tb" / "ntt"

PKG = RTL_NTT / "ntt_pkg.sv"
CORE_SOURCES = [
    PKG, RTL_NTT / "twiddle_rom.sv", RTL_ARITH / "twiddle_rom_half.sv", RTL_MEM / "bank_map_rom.sv",
    RTL_NTT / "pipe_delay.sv", RTL_NTT / "modmul_reduce_staged.sv", RTL_ARITH / "modmul_fold.sv",
    RTL_ARITH / "modmul_barrett.sv", RTL_ARITH / "modmul_montgomery.sv", RTL_ARITH / "modmul_sel.sv",
    RTL_ARITH / "half_mod.sv", RTL_ARITH / "butterfly_m6.sv", RTL_MEM / "poly_mem_multiport_pipe.sv",
    RTL_NTT / "ntt_core_m6.sv", RTL_NTT / "ntt_core_m6_p6.sv",
]


def mutate(src: Path, dst: Path, old: str, new: str) -> Path:
    text = src.read_text()
    assert text.count(old) == 1, f"{src.name}: pattern for the mutant not found exactly once"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text.replace(old, new))
    return dst


def mutant_rom(src: Path, dst: Path) -> Path:
    """INTT entries of layer 3 (zeta indices 8..15 -> array indices 128 + k) replaced by the NTT entries (halving dropped)."""
    text = src.read_text()
    ntt = {int(m.group(1)): m.group(2) for m in re.finditer(r"rom_zeta\[(\d+)\] = 12'd(\d+);", text) if int(m.group(1)) < 128}
    for k in range(8, 16):
        text, n = re.subn(rf"rom_zeta\[{128 + k}\] = 12'd\d+;", f"rom_zeta[{128 + k}] = 12'd{ntt[k]};", text)
        assert n == 1
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text)
    return dst


def build_and_test(sim, build_root, name, top, sources, tests, params=None, extra_env=None):
    build_dir = build_root / f"sim_build_{sim}_m6_{name}"
    runner = get_runner(sim)
    runner.build(sources=sources, hdl_toplevel=top, build_dir=build_dir, parameters=params or {},
                 build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [], always=True)
    outs = []
    for (module, test_dir) in tests:
        cycles_out = build_dir / f"cycles_{module}.json"
        if cycles_out.exists():
            cycles_out.unlink()
        env = {"C3_RDLAT": "3", "C3_WRDLY": "3", "C3_CORE": "u_core", "C3_NEGCTL": "0", "C3_CYCLES_OUT": str(cycles_out)}
        env.update(extra_env or {})
        results = runner.test(hdl_toplevel=top, test_module=module, test_dir=test_dir, build_dir=build_dir,
                              results_xml=str(build_dir / f"results_{module}.xml"), extra_env=env)
        cases = ET.parse(results).getroot().findall(".//testcase")
        ran = [c for c in cases if c.find("skipped") is None]
        failed = [c.get("name") for c in ran if c.find("failure") is not None or c.find("error") is not None]
        note = json.loads(cycles_out.read_text()) if cycles_out.exists() else {}
        outs.append((module, [c.get("name") for c in ran], failed, note))
    return outs


def run(sim, build_root, names):
    ok = True
    total = bad = 0
    for name in names:
        mdir = build_root / f"mut_{sim}_{name}"
        if name in ("half", "halfneg"):
            src = RTL_ARITH / "half_mod.sv"
            if name == "halfneg":
                src = mutate(src, mdir / "half_mod.sv", "x_i[0] ? (CW + 1)'(Q) : (CW + 1)'(0)",
                             "x_i[0] ? (CW + 1)'(0) : (CW + 1)'(Q)")
            (module, ran, failed, _), = build_and_test(sim, build_root, name, "half_mod", [PKG, src],
                                                       [("test_half_mod", HERE)])
            if name == "half":
                good = ran and not failed
                print(f"[{sim}] half ({'half_mod'}): {len(ran) - len(failed)}/{len(ran)} " + ("PASS" if good else f"FAIL {failed}"))
            else:
                good = len(failed) == len(ran) == 1
                print(f"[{sim}] halfneg: exhaustive test failed as required: {failed}" if good
                      else f"[{sim}] halfneg: NEGATIVE CONTROL VOID, failed={failed}")
            total += 1
            bad += 0 if good else 1
            ok &= bool(good)
            continue
        sources = list(CORE_SOURCES)
        if name == "nch":
            m = mutate(RTL_ARITH / "butterfly_m6.sv", mdir / "butterfly_m6.sv", "      a_o = side_half;", "      a_o = side_d;")
            sources = [m if s.name == "butterfly_m6.sv" else s for s in sources]
        if name == "ncr":
            m = mutant_rom(RTL_ARITH / "twiddle_rom_half.sv", mdir / "twiddle_rom_half.sv")
            sources = [m if s.name == "twiddle_rom_half.sv" else s for s in sources]
        tests = [("test_ntt_core_c3", TB_NTT)] + ([("test_m6_basis", HERE)] if name == "m6" else [])
        outs = build_and_test(sim, build_root, name, "ntt_core_m6_p6", sources, tests)
        if name == "m6":
            for module, ran, failed, note in outs:
                good = bool(ran) and not failed
                extra = ""
                if module == "test_ntt_core_c3":
                    good &= (note.get("cycles_NTT"), note.get("cycles_INTT")) == (119, 119)
                    extra = f"  {note}"
                print(f"[{sim}] m6 {module}: {len(ran) - len(failed)}/{len(ran)} " + ("PASS" if good else f"FAIL {failed}") + extra)
                total += len(ran)
                bad += len(failed) if failed else (0 if good else 1)
                ok &= good
        else:
            module, ran, failed, _ = outs[0]
            intt_fail = "test_intt_bit_exact" in failed
            ntt_ok = "test_ntt_bit_exact" not in failed
            good = intt_fail and (ntt_ok if name == "ncr" else True)
            print(f"[{sim}] {name}: INTT bit-exact failed as required: {intt_fail}; NTT bit-exact failed: {not ntt_ok}; "
                  f"failed={failed}" + ("" if good else "  NEGATIVE CONTROL VOID"))
            total += 1
            bad += 0 if good else 1
            ok &= good
    print(f"[{sim}] TOTAL: {total - bad}/{total} passed")
    return ok


if __name__ == "__main__":
    sim_name = sys.argv[1] if len(sys.argv) > 1 else "icarus"
    selected = sys.argv[2:] or ["half", "halfneg", "m6", "nch", "ncr"]
    root = Path(os.environ.get("M6_BUILD_DIR") or tempfile.mkdtemp(prefix="chip2026_m6_"))
    sys.exit(0 if run(sim_name, root, selected) else 1)
