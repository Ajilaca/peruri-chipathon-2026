"""tb/mlkem/run_hashfo_tests.py -- Phase 9b verification (evidence/phase09/9b/test_plan_9b.md V3-V7, V10) against one simulator.

Builds rtl/mlkem/mlkem_hash_fo_top.sv and runs:
  hash1   tb/mlkem/test_mlkem_hash.py with the C5 sponge (CORE_R2 = 1)      (V3, V4, V6, V10)
  hash0   the same with the K0 sponge (CORE_R2 = 0)
  fo      tb/mlkem/test_mlkem_fo_cmp.py                                      (V5, V6, V10)
  ncstop  NC-STOP: J never stops the squeeze                  -> test_required_lengths_all_modes must FAIL
  nclast  NC-LAST: G puts out only 4 digest words             -> test_required_lengths_all_modes must FAIL
  ncsel   NC-SEL:  J uses SHAKE128                            -> test_required_lengths_all_modes must FAIL
  ncmask  NC-MASK: the compare looks at the low 32 bits only  -> test_every_single_bit_difference must FAIL
  ncswap  NC-SWAP: the key select is inverted                 -> test_equal_and_random_pairs_with_gaps must FAIL
  ncearly NC-EARLY: the compare ends at the first difference  -> test_constant_cycles_and_cycle_table must FAIL
Environment: HF_BUILD_DIR, HF_CYCLES_OUT_DIR.
Usage: python3 tb/mlkem/run_hashfo_tests.py icarus|verilator [hash1 hash0 fo ncstop nclast ncsel ncmask ncswap ncearly]
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
M = ROOT / "rtl" / "mlkem"
KECCAK = [K / "keccak_pkg.sv", K / "keccak_round.sv", K / "keccak_f1600.sv", K / "keccak_sponge.sv", K / "keccak_f1600_r2.sv", K / "keccak_sponge_r2.sv"]
HASH, FO, TOP = M / "mlkem_hash.sv", M / "mlkem_fo_cmp.sv", M / "mlkem_hash_fo_top.sv"


def mutate(src, dst, edits):
    t = src.read_text()
    for old, new in edits:
        assert t.count(old) == 1, f"{src.name}: pattern {old!r} found {t.count(old)} times"
        t = t.replace(old, new)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(t)
    return dst


def build_test(sim, root, name, sources, module, core_r2=1):
    bd = root / f"sim_build_{sim}_{name}"
    r = get_runner(sim)
    r.build(sources=sources, hdl_toplevel="mlkem_hash_fo_top", build_dir=bd, parameters={"CORE_R2": core_r2}, build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [], always=True)
    out = Path(os.environ.get("HF_CYCLES_OUT_DIR", str(bd))) / f"cycles_{sim}_{name}.json"
    if out.exists():
        out.unlink()
    res = r.test(hdl_toplevel="mlkem_hash_fo_top", test_module=module, test_dir=HERE, build_dir=bd, results_xml=str(bd / "results.xml"), extra_env={"HF_CYCLES_OUT": str(out), "HF_CORE_R2": str(core_r2)})
    cases = ET.parse(res).getroot().findall(".//testcase")
    ran = [c for c in cases if c.find("skipped") is None]
    failed = [c.get("name") for c in ran if c.find("failure") is not None or c.find("error") is not None]
    return ran, failed


def run(sim, root, names):
    ok, total, bad = True, 0, 0
    for name in names:
        mdir = root / f"mut_{sim}_{name}"
        if name in ("hash1", "hash0", "fo"):
            mod = "test_mlkem_fo_cmp" if name == "fo" else "test_mlkem_hash"
            ran, failed = build_test(sim, root, name, KECCAK + [HASH, FO, TOP], mod, core_r2=0 if name == "hash0" else 1)
            good = bool(ran) and not failed
            print(f"[{sim}] {name}: {len(ran) - len(failed)}/{len(ran)} " + ("PASS" if good else f"FAIL {failed}"))
            total += len(ran)
            bad += len(failed) if failed else (0 if good else 1)
        else:
            if name == "ncstop":
                m = mutate(HASH, mdir / HASH.name, [("wire   sp_stop     = take && last_word && is_j;", "wire   sp_stop     = 1'b0;")])
                srcs, mod, must = KECCAK + [m, FO, TOP], "test_mlkem_hash", "test_required_lengths_all_modes"
            elif name == "nclast":
                m = mutate(HASH, mdir / HASH.name, [("wire [3:0]  last_idx = is_g ? 4'd7 : 4'd3;", "wire [3:0]  last_idx = 4'd3;")])
                srcs, mod, must = KECCAK + [m, FO, TOP], "test_mlkem_hash", "test_required_lengths_all_modes"
            elif name == "ncsel":
                m = mutate(HASH, mdir / HASH.name, [("default: mode_in = 2'd3;", "default: mode_in = 2'd2;")])
                srcs, mod, must = KECCAK + [m, FO, TOP], "test_mlkem_hash", "test_required_lengths_all_modes"
            elif name == "ncmask":
                m = mutate(FO, mdir / FO.name, [("wire [63:0]  diff_next = diff_q | (a_data_i ^ b_data_i);", "wire [63:0]  diff_next = diff_q | ((a_data_i ^ b_data_i) & 64'h0000_0000_FFFF_FFFF);")])
                srcs, mod, must = KECCAK + [HASH, m, TOP], "test_mlkem_fo_cmp", "test_every_single_bit_difference"
            elif name == "ncswap":
                m = mutate(FO, mdir / FO.name, [("k_q   <= (kgood_i & ~mask) | (kbad_i & mask);", "k_q   <= (kgood_i & mask) | (kbad_i & ~mask);")])
                srcs, mod, must = KECCAK + [HASH, m, TOP], "test_mlkem_fo_cmp", "test_equal_and_random_pairs_with_gaps"
            elif name == "ncearly":
                m = mutate(FO, mdir / FO.name, [("wire last    = take && (cnt_q == CNTW'(WORDS - 1));", "wire last    = take && ((cnt_q == CNTW'(WORDS - 1)) || (|(diff_q | (a_data_i ^ b_data_i))));")])
                srcs, mod, must = KECCAK + [HASH, m, TOP], "test_mlkem_fo_cmp", "test_constant_cycles_and_cycle_table"
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
    names = sys.argv[2:] or ["hash1", "hash0", "fo", "ncstop", "nclast", "ncsel", "ncmask", "ncswap", "ncearly"]
    root = Path(os.environ.get("HF_BUILD_DIR") or tempfile.mkdtemp(prefix="chip2026_9b_"))
    sys.exit(0 if run(sim, root, names) else 1)
