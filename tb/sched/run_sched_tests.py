"""tb/sched/run_sched_tests.py -- Phase 6 verification (evidence/phase06/test_plan.md V4-V6) against one simulator.

Builds:
  pwm    rtl/sched/pwm_unit.sv: tb/sched/test_pwm_unit.py (V4)
  top    rtl/sched/kpke_sched_top.sv: tb/sched/test_kpke_sched.py (V5)
  ncg    top with one gamma ROM entry wrong (test-only copy): bit-exact must FAIL (V6 NC-G)
  ncr    top whose read-back from the NTT core is aligned one cycle off (test-only copy): bit-exact must FAIL (V6 NC-R)
Usage: python3 tb/sched/run_sched_tests.py icarus|verilator [pwm top ncg ncr]
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
R = ROOT / "rtl"
CORE = [R / "ntt/ntt_pkg.sv", R / "ntt/twiddle_rom.sv", R / "arith/twiddle_rom_half.sv", R / "mem/bank_map_rom.sv", R / "ntt/pipe_delay.sv",
        R / "ntt/modmul_reduce_staged.sv", R / "arith/modmul_fold.sv", R / "arith/modmul_barrett.sv", R / "arith/modmul_montgomery.sv",
        R / "arith/modmul_sel.sv", R / "arith/half_mod.sv", R / "arith/butterfly_m6.sv", R / "mem/poly_mem_multiport_split.sv",
        R / "ntt/ntt_core_s7.sv", R / "ntt/ntt_core_s7_p7.sv"]
SCHED = [R / "sched/gamma_rom.sv", R / "sched/kpke_prog_rom.sv", R / "sched/poly_store.sv", R / "sched/pwm_unit.sv", R / "sched/kpke_sched.sv",
         R / "sched/kpke_sched_top.sv"]


def mutate(src, dst, old, new):
    t = src.read_text()
    assert t.count(old) == 1, f"{src.name}: pattern found {t.count(old)} times"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(t.replace(old, new))
    return dst


def build_test(sim, root, name, top, sources, module, env):
    bd = root / f"sim_build_{sim}_p6_{name}"
    r = get_runner(sim)
    r.build(sources=sources, hdl_toplevel=top, build_dir=bd, build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [], always=True)
    out = bd / "cycles.json"
    if out.exists():
        out.unlink()
    e = {"KS_CYCLES_OUT": str(out)}
    e.update(env)
    res = r.test(hdl_toplevel=top, test_module=module, test_dir=HERE, build_dir=bd, results_xml=str(bd / "results.xml"), extra_env=e)
    cases = ET.parse(res).getroot().findall(".//testcase")
    ran = [c for c in cases if c.find("skipped") is None]
    failed = [c.get("name") for c in ran if c.find("failure") is not None or c.find("error") is not None]
    note = json.loads(out.read_text()) if out.exists() else {}
    return ran, failed, note


def run(sim, root, names):
    ok = True
    for name in names:
        mdir = root / f"mut_{sim}_{name}"
        if name == "pwm":
            ran, failed, _ = build_test(sim, root, name, "pwm_unit", [R / "ntt/ntt_pkg.sv", R / "ntt/pipe_delay.sv", R / "arith/modmul_barrett.sv",
                                                                     R / "sched/pwm_unit.sv"], "test_pwm_unit", {})
            good = bool(ran) and not failed
            print(f"[{sim}] pwm: {len(ran) - len(failed)}/{len(ran)} " + ("PASS" if good else f"FAIL {failed}"))
        else:
            src = CORE + SCHED
            if name == "ncg":
                m = mutate(R / "sched/gamma_rom.sv", mdir / "gamma_rom.sv", "7'd5  : gamma_o = ", "7'd5  : gamma_o = 12'd1 + ")
                src = [m if s.name == m.name else s for s in src]
            if name == "ncr":
                m = mutate(R / "sched/kpke_sched.sv", mdir / "kpke_sched.sv", "assign widx_unl = cnt_q - 9'(CORE_RDLAT);",
                           "assign widx_unl = cnt_q - 9'(CORE_RDLAT + 1);")
                src = [m if s.name == m.name else s for s in src]
            env = {"KS_NEGCTL": "0" if name == "top" else "1", "KS_SEEDS": os.environ.get("KS_SEEDS", "2")}
            ran, failed, note = build_test(sim, root, name, "kpke_sched_top", src, "test_kpke_sched", env)
            good = bool(ran) and not failed
            label = "PASS" if good else f"FAIL {failed}"
            if name != "top":
                label = ("bit-exact failed as required" if good else "NEGATIVE CONTROL VOID")
            print(f"[{sim}] {name}: {len(ran) - len(failed)}/{len(ran)} {label}  {note}")
        ok &= good
    print(f"[{sim}] OVERALL: {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    sim = sys.argv[1] if len(sys.argv) > 1 else "icarus"
    names = sys.argv[2:] or ["pwm", "top", "ncg", "ncr"]
    root = Path(os.environ.get("P6_BUILD_DIR") or tempfile.mkdtemp(prefix="chip2026_p6_"))
    sys.exit(0 if run(sim, root, names) else 1)
