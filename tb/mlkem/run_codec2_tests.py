"""tb/mlkem/run_codec2_tests.py -- Phase 9M item 1 (evidence/phase9m/batch1/9m1/test_plan_9m1.md V2, V5) against one simulator.

Builds rtl/mlkem/mlkem_codec2_top.sv (mlkem_pack2 and mlkem_unpack2, two bytes per beat) and runs the unchanged Phase 9a test modules with CT_W=2:
  pack     tb/mlkem/test_mlkem_pack.py
  unpack   tb/mlkem/test_mlkem_unpack.py
  ncword   NC-W-ORD: the two bytes of a pack beat are swapped                   -> test_random_and_special_all_d_all_modes (pack) must FAIL
  ncwcnt   NC-W-CNT: the unpacker takes a beat when 20 bits remain (overflow)  -> test_random_all_d_all_modes (unpack) must FAIL
Environment: CT_N (cases, default 40), CT_BUILD_DIR, CT_CYCLES_OUT_DIR.
Usage: python3 tb/mlkem/run_codec2_tests.py icarus|verilator [pack unpack ncword ncwcnt]
"""
import os
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from cocotb_tools.runner import get_runner

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from run_codec_tests import mutate  # noqa: E402

M = HERE.parent.parent / "rtl" / "mlkem"
PACK, UNPACK, TOP = M / "mlkem_pack2.sv", M / "mlkem_unpack2.sv", M / "mlkem_codec2_top.sv"


def build_test(sim, root, name, sources, module):
    bd = root / f"sim_build_{sim}_{name}"
    r = get_runner(sim)
    r.build(sources=sources, hdl_toplevel="mlkem_codec2_top", build_dir=bd, build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [], always=True)
    out = Path(os.environ.get("CT_CYCLES_OUT_DIR", str(bd))) / f"cycles2_{sim}_{name}.json"
    if out.exists():
        out.unlink()
    res = r.test(hdl_toplevel="mlkem_codec2_top", test_module=module, test_dir=HERE, build_dir=bd, results_xml=str(bd / "results.xml"), extra_env={"CT_CYCLES_OUT": str(out), "CT_W": "2"})
    cases = ET.parse(res).getroot().findall(".//testcase")
    ran = [c for c in cases if c.find("skipped") is None]
    failed = [c.get("name") for c in ran if c.find("failure") is not None or c.find("error") is not None]
    return ran, failed


def run(sim, root, names):
    ok, total, bad = True, 0, 0
    for name in names:
        mdir = root / f"mut_{sim}_{name}"
        if name in ("pack", "unpack"):
            ran, failed = build_test(sim, root, name, [PACK, UNPACK, TOP], f"test_mlkem_{name}")
            good = bool(ran) and not failed
            print(f"[{sim}] {name}: {len(ran) - len(failed)}/{len(ran)} " + ("PASS" if good else f"FAIL {failed}"))
            total += len(ran)
            bad += len(failed) if failed else (0 if good else 1)
        else:
            if name == "ncword":
                m = mutate(PACK, mdir / PACK.name, [("assign beat_data_o = acc_q[15:0];", "assign beat_data_o = {acc_q[7:0], acc_q[15:8]};", 1)])
                srcs, mod, must = [m, UNPACK, TOP], "test_mlkem_pack", "test_random_and_special_all_d_all_modes"
            elif name == "ncwcnt":
                m = mutate(UNPACK, mdir / UNPACK.name, [("(cnt_after <= 6'd16)", "(cnt_after <= 6'd20)", 1)])
                srcs, mod, must = [PACK, m, TOP], "test_mlkem_unpack", "test_random_all_d_all_modes"
            else:
                raise SystemExit(f"unknown target {name}")
            ran, failed = build_test(sim, root, name, srcs, mod)
            good = must in failed
            print(f"[{sim}] {name}: {must} failed as required: {good}; failed={failed}" + ("" if good else "  NEGATIVE CONTROL VOID"))
            total += 1
            bad += 0 if good else 1
        ok &= good
    print(f"[{sim}] TOTAL: {total - bad}/{total} passed")
    return ok


if __name__ == "__main__":
    sim = sys.argv[1] if len(sys.argv) > 1 else "icarus"
    names = sys.argv[2:] or ["pack", "unpack", "ncword", "ncwcnt"]
    root = Path(os.environ.get("CT_BUILD_DIR") or tempfile.mkdtemp(prefix="chip2026_9m1_codec_"))
    sys.exit(0 if run(sim, root, names) else 1)
