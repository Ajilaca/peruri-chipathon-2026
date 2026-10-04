"""tb/mlkem/run_core_tests.py -- Phase 9c verification (docs/evidence/phase09-integration/9c/test_plan_9c.md V3-V8) against one simulator.

Builds rtl/mlkem/mlkem_core.sv (with the K-PKE engine of 8d and the 9a / 9b blocks) and runs:
  core    tb/mlkem/test_mlkem_core.py (ACVP, random cross-check, chain, protocol, constant cycles, cycles)
  nccmp   NC-CMP:  the key of Decaps is always K'                       -> test_acvp_decaps must FAIL     (CORE_FAST=1)
  ncsel   NC-SEL:  the selection of K' and K_bar is inverted            -> test_acvp_decaps must FAIL     (CORE_FAST=1)
  nclen   NC-LEN:  every hash is one byte short                         -> test_acvp_encaps must FAIL     (CORE_FAST=1)
  ncoff   NC-OFF:  Decaps feeds h from the z offset                     -> test_acvp_decaps must FAIL     (CORE_FAST=1)
  ncrom   NC-ROM:  the message polynomial is loaded with d = 4          -> test_acvp_encaps must FAIL     (CORE_FAST=1)
Environment: CORE_BUILD_DIR, CORE_CYCLES_OUT_DIR, CORE_N.
Usage: python3 tb/mlkem/run_core_tests.py icarus|verilator [core nccmp ncsel nclen ncoff ncrom]
"""
import os
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from cocotb_tools.runner import get_runner

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "tb" / "golden"))
import mlkem_ctl_model as CM  # noqa: E402

M = ROOT / "rtl" / "mlkem"
ENG = [ROOT / p for p in (
    "rtl/keccak/keccak_pkg.sv", "rtl/keccak/keccak_round.sv", "rtl/keccak/keccak_f1600.sv", "rtl/keccak/keccak_sponge.sv", "rtl/keccak/keccak_f1600_r2.sv", "rtl/keccak/keccak_sponge_r2.sv",
    "rtl/sample/sample_ntt_core.sv", "rtl/sample/cbd2_core.sv", "rtl/sample/keccak_sampler.sv", "rtl/ntt/ntt_pkg.sv", "rtl/ntt/twiddle_rom.sv", "rtl/arith/twiddle_rom_half.sv", "rtl/ntt/pipe_delay.sv",
    "rtl/ntt/modmul_reduce_staged.sv", "rtl/arith/modmul_fold.sv", "rtl/arith/modmul_barrett.sv", "rtl/arith/modmul_montgomery.sv", "rtl/arith/modmul_sel.sv", "rtl/arith/half_mod.sv", "rtl/arith/butterfly_m6.sv",
    "rtl/mem/poly_mem_m10k.sv", "rtl/ntt/ntt_core_s10.sv", "rtl/ntt/ntt_core_s10_p5.sv", "rtl/sched/gamma_rom.sv", "rtl/sched/kpke_smp_prog_rom.sv", "rtl/sched/poly_store_smp.sv", "rtl/sched/pwm_unit.sv",
    "rtl/sched/kpke_sched_smp.sv", "rtl/sched/kpke_smp_top_s10.sv")]
MLK = [M / f for f in ("mlkem_pack.sv", "mlkem_unpack.sv", "mlkem_hash.sv", "mlkem_fo_cmp.sv", "mlkem_ram.sv", "mlkem_fifo4.sv", "mlkem_wordbytes.sv", "mlkem_bytedst.sv", "mlkem_ldpoly.sv", "mlkem_stpoly.sv", "mlkem_ctl_rom.sv", "mlkem_core.sv")]
CORE, ROM = M / "mlkem_core.sv", M / "mlkem_ctl_rom.sv"


def mutate(src, dst, edits):
    t = src.read_text()
    for old, new, cnt in edits:
        assert t.count(old) == cnt, f"{src.name}: pattern {old!r} found {t.count(old)} times, expected {cnt}"
        t = t.replace(old, new)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(t)
    return dst


def build_test(sim, root, name, srcs, fast):
    bd = root / f"sim_build_{sim}_{name}"
    r = get_runner(sim)
    r.build(sources=srcs, hdl_toplevel="mlkem_core", build_dir=bd, build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [], always=True)
    out = Path(os.environ.get("CORE_CYCLES_OUT_DIR", str(bd))) / f"cycles_{sim}_{name}.json"
    if out.exists():
        out.unlink()
    env = {"CORE_CYCLES_OUT": str(out), "CORE_FAST": "1" if fast else "0"}
    res = r.test(hdl_toplevel="mlkem_core", test_module="test_mlkem_core", test_dir=HERE, build_dir=bd, results_xml=str(bd / "results.xml"), extra_env=env)
    cases = ET.parse(res).getroot().findall(".//testcase")
    ran = [c for c in cases if c.find("skipped") is None]
    failed = [c.get("name") for c in ran if c.find("failure") is not None or c.find("error") is not None]
    return ran, failed


def run(sim, root, names):
    ok, total, bad = True, 0, 0
    for name in names:
        mdir = root / f"mut_{sim}_{name}"
        if name == "core":
            ran, failed = build_test(sim, root, name, ENG + MLK, False)
            good = bool(ran) and not failed
            print(f"[{sim}] {name}: {len(ran) - len(failed)}/{len(ran)} " + ("PASS" if good else f"FAIL {failed}"))
            total += len(ran)
            bad += len(failed) if failed else (0 if good else 1)
        else:
            core, rom = CORE, ROM
            if name == "nccmp":
                core = mutate(CORE, mdir / CORE.name, [("wr_data = fo_k[64*k_q[1:0] +: 64];", "wr_data = rf_q[{3'd5, k_q[1:0]}];", 1)])
                must = "test_acvp_decaps"
            elif name == "ncsel":
                core = mutate(CORE, mdir / CORE.name, [("wire  [255:0] k_good = {rf_q[23], rf_q[22], rf_q[21], rf_q[20]};", "wire  [255:0] k_good = {rf_q[27], rf_q[26], rf_q[25], rf_q[24]};", 1),
                                                         ("wire  [255:0] k_bad  = {rf_q[27], rf_q[26], rf_q[25], rf_q[24]};", "wire  [255:0] k_bad  = {rf_q[23], rf_q[22], rf_q[21], rf_q[20]};", 1)])
                must = "test_acvp_decaps"
            elif name == "nclen":
                core = mutate(CORE, mdir / CORE.name, [(".len_i({5'd0, f_hlen})", ".len_i({5'd0, f_hlen} - 16'd1)", 1)])
                must = "test_acvp_encaps"
            elif name == "ncoff":
                t = ROM.read_text().split("\n")
                hits = [i for i, ln in enumerate(t) if "// decaps" in ln and f"HFD {CM.KB} {CM.OFF_H} 4" in ln]
                assert len(hits) == 1
                t[hits[0]] = t[hits[0]].replace(f"40'h{CM.encode(('HFD', CM.KB, CM.OFF_H, 4)):010x}", f"40'h{CM.encode(('HFD', CM.KB, CM.OFF_Z, 4)):010x}")
                rom = mdir / ROM.name
                rom.parent.mkdir(parents=True, exist_ok=True)
                rom.write_text("\n".join(t))
                must = "test_acvp_decaps"
            elif name == "ncrom":
                t = ROM.read_text().split("\n")
                old, new = ("LDP", 11, CM.RFR, 4 * CM.R_M, 1), ("LDP", 11, CM.RFR, 4 * CM.R_M, 4)
                hits = [i for i, ln in enumerate(t) if f"LDP 11 {CM.RFR} {4 * CM.R_M} 1" in ln]
                assert len(hits) == 2
                for i in hits:
                    t[i] = t[i].replace(f"40'h{CM.encode(old):010x}", f"40'h{CM.encode(new):010x}")
                rom = mdir / ROM.name
                rom.parent.mkdir(parents=True, exist_ok=True)
                rom.write_text("\n".join(t))
                must = "test_acvp_encaps"
            else:
                raise SystemExit(f"unknown target {name}")
            srcs = [core if f == CORE else rom if f == ROM else f for f in ENG + MLK]
            ran, failed = build_test(sim, root, name, srcs, True)
            good = must in failed
            print(f"[{sim}] {name}: {must} failed as required: {good}; failed={failed}" + ("" if good else "  NEGATIVE CONTROL VOID"))
            total += 1
            bad += 0 if good else 1
        ok &= good
    print(f"[{sim}] TOTAL: {total - bad}/{total} passed")
    return ok


if __name__ == "__main__":
    sim = sys.argv[1] if len(sys.argv) > 1 else "icarus"
    names = sys.argv[2:] or ["core", "nccmp", "ncsel", "nclen", "ncoff", "ncrom"]
    root = Path(os.environ.get("CORE_BUILD_DIR") or tempfile.mkdtemp(prefix="chip2026_9c_"))
    sys.exit(0 if run(sim, root, names) else 1)
