"""tb/mlkem/run_codec_tests.py -- Phase 9a verification (docs/evidence/phase09-integration/9a/test_plan_9a.md V3-V8, V11) against one simulator.

Builds rtl/mlkem/mlkem_codec_top.sv (packer and unpacker) and runs:
  pack    tb/mlkem/test_mlkem_pack.py   (V3, V5, V6, V7, V11)
  unpack  tb/mlkem/test_mlkem_unpack.py (V4, V5, V6, V7, V11)
  ncrnd   NC-RND: compress without the rounding term (1664 -> 0)           -> test_exhaustive_compress must FAIL
  ncord   NC-ORD: the packer puts out the bits of a byte in reverse order  -> test_random_and_special_all_d_all_modes must FAIL
  ncmod   NC-MOD: unpack d = 12 without the reduction mod q                -> test_exhaustive_decompress_and_all_12_bit_values must FAIL
  nccnt   NC-CNT: the packer accepts a 257th coefficient                   -> test_random_and_special_all_d_all_modes must FAIL
Environment: CT_N (cases, default 40), CT_BUILD_DIR, CT_CYCLES_OUT_DIR.
Usage: python3 tb/mlkem/run_codec_tests.py icarus|verilator [pack unpack ncrnd ncord ncmod nccnt]
"""
import os
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from cocotb_tools.runner import get_runner

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
M = ROOT / "rtl" / "mlkem"
PACK, UNPACK, TOP = M / "mlkem_pack.sv", M / "mlkem_unpack.sv", M / "mlkem_codec_top.sv"


def mutate(src, dst, edits):
    t = src.read_text()
    for old, new, cnt in edits:
        assert t.count(old) == cnt, f"{src.name}: pattern {old!r} found {t.count(old)} times, expected {cnt}"
        t = t.replace(old, new)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(t)
    return dst


def build_test(sim, root, name, sources, module):
    bd = root / f"sim_build_{sim}_{name}"
    r = get_runner(sim)
    r.build(sources=sources, hdl_toplevel="mlkem_codec_top", build_dir=bd, build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [], always=True)
    out = Path(os.environ.get("CT_CYCLES_OUT_DIR", str(bd))) / f"cycles_{sim}_{name}.json"
    if out.exists():
        out.unlink()
    res = r.test(hdl_toplevel="mlkem_codec_top", test_module=module, test_dir=HERE, build_dir=bd, results_xml=str(bd / "results.xml"), extra_env={"CT_CYCLES_OUT": str(out)})
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
            if name == "ncrnd":
                m = mutate(PACK, mdir / PACK.name, [("+ 22'd1664", "+ 22'd0", 3)])
                srcs, mod, must = [m, UNPACK, TOP], "test_mlkem_pack", "test_exhaustive_compress"
            elif name == "ncord":
                m = mutate(PACK, mdir / PACK.name, [("assign byte_data_o = acc_q[7:0];", "assign byte_data_o = {acc_q[0], acc_q[1], acc_q[2], acc_q[3], acc_q[4], acc_q[5], acc_q[6], acc_q[7]};", 1)])
                srcs, mod, must = [m, UNPACK, TOP], "test_mlkem_pack", "test_random_and_special_all_d_all_modes"
            elif name == "ncmod":
                m = mutate(UNPACK, mdir / UNPACK.name, [("default: dec = (x >= 12'd3329) ? (x - 12'd3329) : x;", "default: dec = x;", 1)])
                srcs, mod, must = [PACK, m, TOP], "test_mlkem_unpack", "test_exhaustive_decompress_and_all_12_bit_values"
            elif name == "nccnt":
                m = mutate(PACK, mdir / PACK.name, [("(cin_q != 9'd256)", "(cin_q != 9'd257)", 1)])
                srcs, mod, must = [m, UNPACK, TOP], "test_mlkem_pack", "test_random_and_special_all_d_all_modes"
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
    names = sys.argv[2:] or ["pack", "unpack", "ncrnd", "ncord", "ncmod", "nccnt"]
    root = Path(os.environ.get("CT_BUILD_DIR") or tempfile.mkdtemp(prefix="chip2026_9a_"))
    sys.exit(0 if run(sim, root, names) else 1)
