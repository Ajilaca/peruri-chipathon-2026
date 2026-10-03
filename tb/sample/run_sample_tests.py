"""tb/sample/run_sample_tests.py -- Phase 8b verification (docs/evidence/phase08-keccak-stream/8b/test_plan_8b.md V3-V8) against one simulator.

Builds:
  ntt     rtl/sample/sample_ntt_core.sv: tb/sample/test_sample_ntt_core.py (V3, V7)
  cbd     rtl/sample/cbd2_core.sv: tb/sample/test_cbd2_core.py (V4, V7)
  top1    rtl/sample/keccak_sampler.sv with CORE_R2 = 1 (C5 sponge): tb/sample/test_keccak_sampler.py (V5, V6, V7); the cycle table is written to KS_CYCLES_OUT_DIR
  top0    the same with CORE_R2 = 0 (K0 sponge)
  nclt    NC-LT:   ntt core accepts d <= q            -> test_crafted_streams must FAIL
  nc2nd   NC-2ND:  ntt core takes a 257th coefficient -> a test of the ntt core must FAIL
  ncord   NC-ORD:  ntt core triple bytes in reverse order -> test_crafted_streams must FAIL
  nccbd   NC-CBD:  cbd core f = y - x                 -> test_nibble_table_and_special_streams must FAIL
  nc17    NC-17:   cbd core accepts a 17th word       -> test_cbd_words_17th_not_taken must FAIL (top, C5)
  ncstop  NC-STOP: the wrapper never issues stop_i on completion -> test_stop_wipes_sponge must FAIL (top, C5)
Environment: KS_OUTW (output width, default 1), KS_N (cases), KS_BUILD_DIR, KS_CYCLES_OUT_DIR.
Usage: python3 tb/sample/run_sample_tests.py icarus|verilator [ntt cbd top1 top0 nclt nc2nd ncord nccbd nc17 ncstop]
"""
import os
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from cocotb_tools.runner import get_runner

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
K = ROOT / "rtl" / "keccak"
S = ROOT / "rtl" / "sample"
OUTW = int(os.environ.get("KS_OUTW", "1"))
KECCAK = [K / "keccak_pkg.sv", K / "keccak_round.sv", K / "keccak_f1600.sv", K / "keccak_sponge.sv", K / "keccak_f1600_r2.sv", K / "keccak_sponge_r2.sv"]
NTT, CBD, TOP = S / "sample_ntt_core.sv", S / "cbd2_core.sv", S / "keccak_sampler.sv"


def mutate(src, dst, edits):
    t = src.read_text()
    for old, new in edits:
        assert t.count(old) == 1, f"{src.name}: pattern {old!r} found {t.count(old)} times"
        t = t.replace(old, new)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(t)
    return dst


def build_test(sim, root, name, top, sources, module, params=None, env=None):
    bd = root / f"sim_build_{sim}_w{OUTW}_{name}"
    r = get_runner(sim)
    r.build(sources=sources, hdl_toplevel=top, build_dir=bd, parameters=params or {}, build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [], always=True)
    out = Path(os.environ.get("KS_CYCLES_OUT_DIR", str(bd))) / f"cycles_w{OUTW}_{sim}_{name}.json"
    if out.exists():
        out.unlink()
    e = {"KS_CYCLES_OUT": str(out), "KS_OUTW": str(OUTW)}
    e.update(env or {})
    res = r.test(hdl_toplevel=top, test_module=module, test_dir=HERE, build_dir=bd, results_xml=str(bd / "results.xml"), extra_env=e)
    cases = ET.parse(res).getroot().findall(".//testcase")
    ran = [c for c in cases if c.find("skipped") is None]
    failed = [c.get("name") for c in ran if c.find("failure") is not None or c.find("error") is not None]
    return ran, failed


def run(sim, root, names):
    ok, total, bad = True, 0, 0
    for name in names:
        mdir = root / f"mut_{sim}_{name}"
        if name in ("ntt", "cbd", "top1", "top0"):
            top, srcs, mod, params = {
                "ntt": ("sample_ntt_core", [NTT], "test_sample_ntt_core", None),
                "cbd": ("cbd2_core", [CBD], "test_cbd2_core", None),
                "top1": ("keccak_sampler", KECCAK + [NTT, CBD, TOP], "test_keccak_sampler", {"CORE_R2": 1}),
                "top0": ("keccak_sampler", KECCAK + [NTT, CBD, TOP], "test_keccak_sampler", {"CORE_R2": 0}),
            }[name]
            ran, failed = build_test(sim, root, name, top, srcs, mod, params)
            good = bool(ran) and not failed
            print(f"[{sim}] {name} (OUTW={OUTW}): {len(ran) - len(failed)}/{len(ran)} " + ("PASS" if good else f"FAIL {failed}"))
            total += len(ran)
            bad += len(failed) if failed else (0 if good else 1)
        else:
            if name == "nclt":
                m = mutate(NTT, mdir / NTT.name, [("a1_q    <= (nd1 < Q);", "a1_q    <= (nd1 <= Q);"), ("a2_q    <= (nd2 < Q);", "a2_q    <= (nd2 <= Q);")])
                top, srcs, mod, must, params = "sample_ntt_core", [m], "test_sample_ntt_core", "test_crafted_streams", None
            elif name == "nc2nd":
                m = mutate(NTT, mdir / NTT.name, [("wire e_last = emit && (n_q == 9'd255);", "wire e_last = emit && (n_q == 9'd256);")])
                top, srcs, mod, must, params = "sample_ntt_core", [m], "test_sample_ntt_core", "test_crafted_streams", None
            elif name == "ncord":
                m = mutate(NTT, mdir / NTT.name, [("wire [ 7:0] b0 = win_q[7:0];", "wire [ 7:0] b0 = win_q[23:16];"), ("wire [ 7:0] b2 = win_q[23:16];", "wire [ 7:0] b2 = win_q[7:0];")])
                top, srcs, mod, must, params = "sample_ntt_core", [m], "test_sample_ntt_core", "test_crafted_streams", None
            elif name == "nccbd":
                m = mutate(CBD, mdir / CBD.name, [("x = {1'b0, nb[0]} + {1'b0, nb[1]};", "x = {1'b0, nb[2]} + {1'b0, nb[3]};"), ("y = {1'b0, nb[2]} + {1'b0, nb[3]};", "y = {1'b0, nb[0]} + {1'b0, nb[1]};")])
                top, srcs, mod, must, params = "cbd2_core", [m], "test_cbd2_core", "test_nibble_table_and_special_streams", None
            elif name == "nc17":
                m = mutate(CBD, mdir / CBD.name, [("(wcnt_q < 5'd16)", "(wcnt_q < 5'd17)")])
                top, srcs, mod, must, params = "keccak_sampler", KECCAK + [NTT, m, TOP], "test_keccak_sampler", "test_cbd_words_17th_not_taken", {"CORE_R2": 1}
            elif name == "ncstop":
                m = mutate(TOP, mdir / TOP.name, [("assign sp_stop = abort_i || n_fin || c_fin;", "assign sp_stop = abort_i;")])
                top, srcs, mod, must, params = "keccak_sampler", KECCAK + [NTT, CBD, m], "test_keccak_sampler", "test_stop_wipes_sponge", {"CORE_R2": 1}
            else:
                raise SystemExit(f"unknown target {name}")
            ran, failed = build_test(sim, root, name, top, srcs, mod, params)
            good = must in failed
            print(f"[{sim}] {name}: {must} failed as required: {good}; failed={failed}" + ("" if good else "  NEGATIVE CONTROL VOID"))
            total += 1
            bad += 0 if good else 1
        ok &= good
    print(f"[{sim}] TOTAL: {total - bad}/{total} passed")
    return ok


if __name__ == "__main__":
    sim = sys.argv[1] if len(sys.argv) > 1 else "icarus"
    names = sys.argv[2:] or ["ntt", "cbd", "top1", "top0", "nclt", "nc2nd", "ncord", "nccbd", "nc17", "ncstop"]
    root = Path(os.environ.get("KS_BUILD_DIR") or tempfile.mkdtemp(prefix="chip2026_8b_"))
    sys.exit(0 if run(sim, root, names) else 1)
