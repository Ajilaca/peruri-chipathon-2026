"""tb/s10/run_s10_tests.py -- S10 verification (evidence/phase06/test_plan_s10.md V2-V4, V6) against one simulator.

Builds:
  mem    rtl/mem/poly_mem_m10k.sv, RD_LAT 2, WR_DELAY 3: tb/s10/test_poly_mem_m10k.py (V2)
  s10    rtl/ntt/ntt_core_s10_p5.sv: the core test tb/s10/test_ntt_core_s10.py (S7 test, start bound from the guard formula) with C3_RDLAT 2, C3_RDPHYS 0, C3_WRDLY 3 (V3); required cycles 118 / 118
  ncm    s10 with the bank map without the XOR bit (test-only copy): bit-exact must FAIL (V4 NC-M)
  ncw    s10 with the write control one cycle short (test-only copy): bit-exact must FAIL (V4 NC-W)
  p6     rtl/sched/kpke_sched_top_s10.sv: the Phase 6 test tb/sched/test_kpke_sched.py (V6)
Phase 9F step S2 (evidence/phase9m/batch2/9s2/test_plan_9s2.md): the same targets at P = 6 (parameter P6 = 1 of ntt_core_s10_p5, C3_WRDLY 4):
  mem6 (WR_DELAY 4), s10p6 (required cycles 119 / 119), ncm6, ncw6 (negative controls; V2-V4)
Phase 9F step S2b (evidence/phase9m/batch2/9s2b/test_plan_9s2b.md): P = 6 with the registered issue address (parameter AREG = 1):
  s10p6a (required cycles 119 / 119), ncar (negative control: the registered address is loaded one cycle late; V2, V3)
Usage: python3 tb/s10/run_s10_tests.py icarus|verilator [mem s10 ncm ncw p6 mem6 s10p6 ncm6 ncw6 s10p6a ncar]
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
MEM = R / "mem/poly_mem_m10k.sv"
CORE = [R / "ntt/ntt_pkg.sv", R / "ntt/twiddle_rom.sv", R / "arith/twiddle_rom_half.sv", R / "ntt/pipe_delay.sv", R / "ntt/modmul_reduce_staged.sv",
        R / "arith/modmul_fold.sv", R / "arith/modmul_barrett.sv", R / "arith/modmul_montgomery.sv", R / "arith/modmul_sel.sv", R / "arith/half_mod.sv",
        R / "arith/butterfly_m6.sv", MEM, R / "ntt/ntt_core_s10.sv", R / "ntt/ntt_core_s10_p5.sv"]
SCHED = [R / "sched/gamma_rom.sv", R / "sched/kpke_prog_rom.sv", R / "sched/poly_store.sv", R / "sched/pwm_unit.sv", R / "sched/kpke_sched.sv",
         R / "sched/kpke_sched_top_s10.sv"]
CORE_ENV = {"C3_RDLAT": "2", "C3_RDPHYS": "0", "C3_WRDLY": "3", "C3_CORE": "u_core", "C3_NEGCTL": "0"}


def mutate(src, dst, old, new):
    t = src.read_text()
    assert t.count(old) == 1, f"{src.name}: pattern found {t.count(old)} times"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(t.replace(old, new))
    return dst


def build_test(sim, root, name, top, sources, module, test_dir, env, params=None):
    bd = root / f"sim_build_{sim}_s10_{name}"
    r = get_runner(sim)
    r.build(sources=sources, hdl_toplevel=top, build_dir=bd, parameters=params or {},
            build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [], always=True)
    out = bd / "cycles.json"
    if out.exists():
        out.unlink()
    e = {"C3_CYCLES_OUT": str(out), "KS_CYCLES_OUT": str(out)}
    e.update(env)
    res = r.test(hdl_toplevel=top, test_module=module, test_dir=test_dir, build_dir=bd, results_xml=str(bd / "results.xml"), extra_env=e)
    cases = ET.parse(res).getroot().findall(".//testcase")
    ran = [c for c in cases if c.find("skipped") is None]
    failed = [c.get("name") for c in ran if c.find("failure") is not None or c.find("error") is not None]
    note = json.loads(out.read_text()) if out.exists() else {}
    return ran, failed, note


def run(sim, root, names):
    ok = True
    total = bad = 0
    for name in names:
        mdir = root / f"mut_{sim}_{name}"
        if name in ("mem", "mem6"):
            wd = 4 if name == "mem6" else 3
            ran, failed, _ = build_test(sim, root, name, "poly_mem_m10k", [R / "ntt/ntt_pkg.sv", R / "ntt/pipe_delay.sv", MEM], "test_poly_mem_m10k", HERE,
                                        {"P10_RD_LAT": "2", "P10_WR_DELAY": str(wd)}, params={"NUM_LANES": 8, "RD_LAT": 2, "WR_DELAY": wd})
            good = bool(ran) and not failed
            print(f"[{sim}] {name} (RD_LAT=2, WR_DELAY={wd}): {len(ran) - len(failed)}/{len(ran)} " + ("PASS" if good else f"FAIL {failed}"))
            total += len(ran)
            bad += len(failed) if failed else (0 if good else 1)
        elif name == "p6":
            ran, failed, note = build_test(sim, root, name, "kpke_sched_top_s10", CORE + SCHED, "test_kpke_sched", ROOT / "tb" / "sched",
                                           {"KS_NEGCTL": "0", "KS_SEEDS": os.environ.get("KS_SEEDS", "2")})
            good = bool(ran) and not failed
            print(f"[{sim}] p6 (Phase 6 top with S10): {len(ran) - len(failed)}/{len(ran)} " + ("PASS" if good else f"FAIL {failed}") + f"  {note}")
            total += len(ran)
            bad += len(failed) if failed else (0 if good else 1)
        else:
            src = list(CORE)
            p6 = name.endswith("p6") or name in ("ncm6", "ncw6", "s10p6a", "ncar")     # S2: P = 6 (S2b targets too)
            ar = name in ("s10p6a", "ncar")                                            # S2b: AREG = 1
            base = {"s10p6": "s10", "ncm6": "ncm", "ncw6": "ncw", "s10p6a": "s10"}.get(name, name)
            env = {**CORE_ENV, "C3_WRDLY": "4"} if p6 else CORE_ENV
            if base == "ncm":
                m = mutate(MEM, mdir / MEM.name, "f_bank = {a[1] ^ a[2] ^ a[3] ^ a[4], a[7], a[6], a[5]};", "f_bank = {a[4], a[7], a[6], a[5]};")
                src = [m if s.name == MEM.name else s for s in src]
            if base == "ncar":
                core = R / "ntt/ntt_core_s10.sv"
                m = mutate(core, mdir / core.name, "p_n     = 8'(gl * (128 / NUM_LANES)) + 8'(t_d);", "p_n     = 8'(gl * (128 / NUM_LANES)) + 8'(t_q);")
                src = [m if s.name == core.name else s for s in src]
            if base == "ncw":
                m = mutate(MEM, mdir / MEM.name, "localparam int WrLat    = RD_LAT + WR_DELAY;", "localparam int WrLat    = RD_LAT + WR_DELAY - 1;")
                src = [m if s.name == MEM.name else s for s in src]
            ran, failed, note = build_test(sim, root, name, "ntt_core_s10_p5", src, "test_ntt_core_s10", HERE, env, params=({"P6": 1, **({"AREG": 1} if ar else {})}) if p6 else None)
            if base == "s10":
                want = (119, 119) if p6 else (118, 118)
                good = bool(ran) and not failed and (note.get("cycles_NTT"), note.get("cycles_INTT")) == want
                print(f"[{sim}] {name}: {len(ran) - len(failed)}/{len(ran)} " + ("PASS" if good else f"FAIL {failed}") + f"  {note}")
                total += len(ran)
                bad += len(failed) if failed else (0 if good else 1)
            else:
                good = "test_ntt_bit_exact" in failed and "test_intt_bit_exact" in failed
                print(f"[{sim}] {name}: bit-exact NTT and INTT failed as required: {good}; failed={failed}" + ("" if good else "  NEGATIVE CONTROL VOID"))
                total += 1
                bad += 0 if good else 1
        ok &= good
    print(f"[{sim}] TOTAL: {total - bad}/{total} passed")
    return ok


if __name__ == "__main__":
    sim = sys.argv[1] if len(sys.argv) > 1 else "icarus"
    names = sys.argv[2:] or ["mem", "s10", "ncm", "ncw", "p6"]     # the S2 targets (mem6 s10p6 ncm6 ncw6) are named on the command line
    root = Path(os.environ.get("S10_BUILD_DIR") or tempfile.mkdtemp(prefix="chip2026_s10_"))
    sys.exit(0 if run(sim, root, names) else 1)
