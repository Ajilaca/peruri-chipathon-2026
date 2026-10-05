"""tb/keccak/run_keccak_tests.py -- Phase 7 verification (evidence/phase07/test_plan.md V4-V7) against one simulator.

Builds:
  perm    rtl/keccak/keccak_f1600.sv: tb/keccak/test_keccak_f1600.py (V4)
  sponge  rtl/keccak/keccak_sponge.sv: tb/keccak/test_keccak_sponge.py (V5, V6); the cycle table is written to KK_CYCLES_OUT_DIR (default: the build directory)
  ncrc    perm with one bit of one round constant wrong (test-only copy of keccak_pkg.sv): the permutation test must FAIL (V7 NC-RC)
  ncr     perm with 23 rounds (test-only copy of keccak_f1600.sv): the permutation test must FAIL (V7 NC-R, also the latency check)
  ncpad   sponge with the SHA3 domain byte 0x1F instead of 0x06 (test-only copy of keccak_sponge.sv): the bit-exact test must FAIL (V7 NC-PAD)
Environment: KK_RPC = rounds per cycle: 1 (default) builds K0 (keccak_f1600, keccak_sponge); 2 builds Phase 8a C5 (keccak_f1600_r2, keccak_sponge_r2; evidence/phase08/8a/test_plan_8a.md).
Usage: python3 tb/keccak/run_keccak_tests.py icarus|verilator [perm sponge ncrc ncr ncpad]
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
R = ROOT / "rtl" / "keccak"
RPC = int(os.environ.get("KK_RPC", "1"))
SFX = "_r2" if RPC == 2 else ""
PKG, RND, F, SP = R / "keccak_pkg.sv", R / "keccak_round.sv", R / f"keccak_f1600{SFX}.sv", R / f"keccak_sponge{SFX}.sv"
F_TOP, SP_TOP = f"keccak_f1600{SFX}", f"keccak_sponge{SFX}"
PERM = 24 // RPC + 2
R_OLD = "if (rnd_q == 5'(ROUNDS - 1)) begin" if RPC == 1 else "if (rnd_q == 4'(ROUNDS / 2 - 1)) begin"
R_NEW = "if (rnd_q == 5'(ROUNDS - 2)) begin" if RPC == 1 else "if (rnd_q == 4'(ROUNDS / 2 - 2)) begin"


def mutate(src, dst, old, new):
    t = src.read_text()
    assert t.count(old) == 1, f"{src.name}: pattern found {t.count(old)} times"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(t.replace(old, new))
    return dst


def build_test(sim, root, name, top, sources, module, env):
    bd = root / f"sim_build_{sim}_k0_r{RPC}_{name}"
    r = get_runner(sim)
    r.build(sources=sources, hdl_toplevel=top, build_dir=bd, build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [], always=True)
    out = Path(os.environ.get("KK_CYCLES_OUT_DIR", str(bd))) / f"cycles_k0_r{RPC}_{sim}_{name}.json"
    if out.exists():
        out.unlink()
    e = {"KK_CYCLES_OUT": str(out), "KK_RPC": str(RPC), "KK_PERM": str(PERM)}
    e.update(env)
    res = r.test(hdl_toplevel=top, test_module=module, test_dir=HERE, build_dir=bd, results_xml=str(bd / "results.xml"), extra_env=e)
    cases = ET.parse(res).getroot().findall(".//testcase")
    ran = [c for c in cases if c.find("skipped") is None]
    failed = [c.get("name") for c in ran if c.find("failure") is not None or c.find("error") is not None]
    npoints = len(json.loads(out.read_text())) if out.exists() else 0
    return ran, failed, npoints


def run(sim, root, names):
    ok = True
    total = bad = 0
    for name in names:
        mdir = root / f"mut_{sim}_{name}"
        if name == "perm":
            ran, failed, _ = build_test(sim, root, name, F_TOP, [PKG, RND, F], "test_keccak_f1600", {})
            good = bool(ran) and not failed
            print(f"[{sim}] perm: {len(ran) - len(failed)}/{len(ran)} " + ("PASS" if good else f"FAIL {failed}"))
            total += len(ran)
            bad += len(failed) if failed else (0 if good else 1)
        elif name == "sponge":
            ran, failed, npts = build_test(sim, root, name, SP_TOP, [PKG, RND, F, SP], "test_keccak_sponge", {})
            good = bool(ran) and not failed
            print(f"[{sim}] sponge: {len(ran) - len(failed)}/{len(ran)} " + ("PASS" if good else f"FAIL {failed}") + f"  cycle points: {npts}")
            total += len(ran)
            bad += len(failed) if failed else (0 if good else 1)
        elif name in ("ncrc", "ncr"):
            if name == "ncrc":
                m = mutate(PKG, mdir / PKG.name, "5'd1 : keccak_rc = 64'h0000000000008082;", "5'd1 : keccak_rc = 64'h0000000000008083;")
                src = [m, RND, F]
            else:
                m = mutate(F, mdir / F.name, R_OLD, R_NEW)
                src = [PKG, RND, m]
            ran, failed, _ = build_test(sim, root, name, F_TOP, src, "test_keccak_f1600", {})
            good = "test_permutation_every_round_and_24_cycles" in failed
            print(f"[{sim}] {name}: permutation test failed as required: {good}; failed={failed}" + ("" if good else "  NEGATIVE CONTROL VOID"))
            total += 1
            bad += 0 if good else 1
        elif name == "ncpad":
            m = mutate(SP, mdir / SP.name, "ds        = mode_q[1] ? 8'h1F : 8'h06;", "ds        = 8'h1F;")
            ran, failed, _ = build_test(sim, root, name, SP_TOP, [PKG, RND, F, m], "test_keccak_sponge", {})
            good = "test_modes_bit_exact" in failed
            print(f"[{sim}] ncpad: bit-exact test failed as required: {good}; failed={failed}" + ("" if good else "  NEGATIVE CONTROL VOID"))
            total += 1
            bad += 0 if good else 1
        ok &= good
    print(f"[{sim}] TOTAL: {total - bad}/{total} passed")
    return ok


if __name__ == "__main__":
    sim = sys.argv[1] if len(sys.argv) > 1 else "icarus"
    names = sys.argv[2:] or ["perm", "sponge", "ncrc", "ncr", "ncpad"]
    root = Path(os.environ.get("KK_BUILD_DIR") or tempfile.mkdtemp(prefix="chip2026_k0_"))
    sys.exit(0 if run(sim, root, names) else 1)
