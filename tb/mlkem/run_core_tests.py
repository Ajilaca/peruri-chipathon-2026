"""tb/mlkem/run_core_tests.py -- Phase 9c verification (evidence/phase09/9c/test_plan_9c.md V3-V8) against one simulator.

Builds rtl/mlkem/mlkem_core.sv (with the K-PKE engine of 8d and the 9a / 9b blocks) and runs:
  core    tb/mlkem/test_mlkem_core.py (ACVP, random cross-check, chain, protocol, constant cycles, cycles)
  nccmp   NC-CMP:  the key of Decaps is always K'                       -> test_acvp_decaps must FAIL     (CORE_FAST=1)
  ncsel   NC-SEL:  the selection of K' and K_bar is inverted            -> test_acvp_decaps must FAIL     (CORE_FAST=1)
  nclen   NC-LEN:  every hash is one byte short                         -> test_acvp_encaps must FAIL     (CORE_FAST=1)
  ncoff   NC-OFF:  Decaps feeds h from the z offset                     -> test_acvp_decaps must FAIL     (CORE_FAST=1)
  ncwcore NC-W-CORE (CORE_W2=1 only): the two-byte loader writes the coefficient index + 1 -> test_acvp_encaps must FAIL     (CORE_FAST=1)
  ncrom   NC-ROM:  the message polynomial is loaded with d = 4          -> test_acvp_encaps must FAIL     (CORE_FAST=1)
Environment: CORE_BUILD_DIR, CORE_CYCLES_OUT_DIR, CORE_N, CORE_W2 (1: the Phase 9M two-byte load / store tasks, parameter CODEC_W2 = 1; test_plan_9m1.md V3), CORE_P6 (1: P = 6 in the NTT core, parameter NTT_P6 = 1, mlkem_core3; test_plan_9s2.md V7), CORE_K0 (1: the K0 sponge for the hash instance, parameter HASH_C5 = 0; test_plan_9m3.md V2).
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
TOP = os.environ.get("CORE_TOP", "mlkem_core")      # mlkem_core2 selects the Phase 9F module (parameter SMP_C5, S1)
MLK[-1] = M / f"{TOP}.sv"
BG = TOP in ("mlkem_core3", "mlkem_core4")          # Phase 9F S1b: background hash job, programs of mlkem_ctl_rom2.sv (core4, Phase 9I item 4: mlkem_ctl_rom3.sv)
OV = TOP == "mlkem_core4"                           # Phase 9I item 4: loads behind the engine (engine variant kpke_sched_smp4 / kpke_smp_top_s10o, loader mlkem_ldpoly2o)
ROMN = "mlkem_ctl_rom3.sv" if OV else "mlkem_ctl_rom2.sv"
if BG:
    MLK = [M / ROMN if f.name == "mlkem_ctl_rom.sv" else f for f in MLK]
if OV:
    ENG += [ROOT / "rtl/sched/kpke_sched_smp4.sv", ROOT / "rtl/sched/kpke_smp_top_s10o.sv"]
CORE, ROM = M / f"{TOP}.sv", M / (ROMN if BG else "mlkem_ctl_rom.sv")
LENPAT = ".len_i(hx_len)" if BG else ".len_i({5'd0, f_hlen})"
W2 = os.environ.get("CORE_W2", "0") == "1"
K0 = os.environ.get("CORE_K0", "0") == "1"
S0 = os.environ.get("CORE_SMP0", "0") == "1"       # K0 sampler sponge in the engine (mlkem_core2 only)
assert not S0 or TOP in ("mlkem_core2", "mlkem_core3", "mlkem_core4"), "CORE_SMP0=1 needs CORE_TOP=mlkem_core2, mlkem_core3 or mlkem_core4"
P6 = os.environ.get("CORE_P6", "0") == "1"         # P = 6 in the NTT core of the engine (S2; mlkem_core3 only)
assert not P6 or TOP in ("mlkem_core3", "mlkem_core4"), "CORE_P6=1 needs CORE_TOP=mlkem_core3 or mlkem_core4"
AR = os.environ.get("CORE_AR", "0") == "1"         # registered issue address in the NTT core (S2b; mlkem_core3 / mlkem_core4)
assert not AR or TOP in ("mlkem_core3", "mlkem_core4"), "CORE_AR=1 needs CORE_TOP=mlkem_core3 or mlkem_core4"
PARAMS = {**({"CODEC_W2": 1} if W2 else {}), **({"HASH_C5": 0} if K0 else {}), **({"SMP_C5": 0} if S0 else {}), **({"NTT_P6": 1} if P6 else {}), **({"NTT_AR": 1} if AR else {})}
if W2:
    MLK += [M / f for f in ("mlkem_pack2.sv", "mlkem_unpack2.sv", "mlkem_wordbytes2.sv", "mlkem_bytedst2.sv", "mlkem_ldpoly2.sv", "mlkem_stpoly2.sv")]
    if OV:
        MLK += [M / "mlkem_ldpoly2o.sv"]
assert not OV or W2, "CORE_TOP=mlkem_core4 needs CORE_W2=1"


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
    r.build(sources=srcs, hdl_toplevel=TOP, build_dir=bd, build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [], parameters=PARAMS, always=True)
    out = Path(os.environ.get("CORE_CYCLES_OUT_DIR", str(bd))) / f"cycles_{sim}_{name}.json"
    if out.exists():
        out.unlink()
    env = {"CORE_CYCLES_OUT": str(out), "CORE_FAST": "1" if fast else "0"}
    res = r.test(hdl_toplevel=TOP, test_module="test_mlkem_core", test_dir=HERE, build_dir=bd, results_xml=str(bd / "results.xml"), extra_env=env)
    cases = ET.parse(res).getroot().findall(".//testcase")
    ran = [c for c in cases if c.find("skipped") is None]
    failed = [c.get("name") for c in ran if c.find("failure") is not None or c.find("error") is not None]
    return ran, failed


def run(sim, root, names):
    ok, total, bad = True, 0, 0
    for name in names:
        mdir = root / f"mut_{sim}_{name}"
        eng4 = None
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
                core = mutate(CORE, mdir / CORE.name, [(LENPAT, LENPAT[:-1] + " - 16'd1)", 1)])
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
            elif name in ("ncilk", "ncthrld", "ncgrant", "ncjoin"):          # Phase 9I item 4 controls (mlkem_core4): the engine variant and the controller are mutated
                assert OV, f"{name} needs CORE_TOP=mlkem_core4"
                ENG4 = ROOT / "rtl/sched/kpke_sched_smp4.sv"
                thr_edit = [("    host_grant = idle_st || (HOSTOV && !seq_wr && !smp_wr);", "    host_grant = idle_st || (HOSTOV && !seq_wr && !smp_wr && (thr_q == 3'd0));", 1),
                            ("  logic host_grant;\n", "  logic host_grant;\n  logic [2:0] thr_q = 3'd0;\n  always_ff @(posedge clk_i) thr_q <= idle_st ? 3'd0 : thr_q + 3'd1;   // restarts with every operation, so that the cycle count stays constant\n", 1)]
                if name == "ncthrld":         # throttled host port (one grant in eight cycles), interlock intact: the loads end late, the engine waits: the whole core target must PASS
                    eng4 = mutate(ENG4, mdir / ENG4.name, thr_edit)
                    must = None
                elif name == "ncilk":         # the same throttled host port WITHOUT the interlock: the engine reads slots that are not loaded -> ACVP must FAIL
                    eng4 = mutate(ENG4, mdir / ENG4.name, thr_edit + [("    if (HOSTOV && (state_q == S_FETCH)) begin", "    if (1'b0 && HOSTOV && (state_q == S_FETCH)) begin", 1)])
                    must = "test_acvp_encaps"
                elif name == "ncgrant":       # the loader ignores the write handshake (it writes and advances although the engine did not grant the port) -> coefficients are lost -> must FAIL
                    LD2O = M / "mlkem_ldpoly2o.sv"
                    ld2 = mutate(LD2O, mdir / LD2O.name, [(".coef_ready_i(tb_wready_i)", ".coef_ready_i(1'b1)", 1), ("assign tb_we_o    = coef_valid && tb_wready_i;", "assign tb_we_o    = coef_valid;", 1),
                                                          ("      if (coef_valid && tb_wready_i) cidx_q <= cidx_q + 8'd1;", "      if (coef_valid) cidx_q <= cidx_q + 8'd1;", 1)])
                    must = "test_acvp_encaps"
                else:                         # NC-JOIN4: RUNJ does not wait for the engine -> must FAIL
                    eng4 = ENG4
                    core = mutate(CORE, mdir / CORE.name, [("        S_RUNJ: if (eng_dn_q || eng_done) begin", "        S_RUNJ: begin", 1)])
                    must = "test_acvp_encaps"
            elif name in ("ncprio", "ncwr", "ncjob", "ncthr", "ncthrnj"):
                assert BG, f"{name} needs CORE_TOP=mlkem_core3"
                if name == "ncprio":          # NC-PRIO: a sidecar read is issued even when the main controller reads
                    core = mutate(CORE, mdir / CORE.name, [("((!bfd_valid_q && !bhold_v_q) || bfd_consumed) && !fg_rd_req;", "((!bfd_valid_q && !bhold_v_q) || bfd_consumed);", 1)])
                    must = "test_acvp_encaps"
                elif name == "ncwr":          # NC-WR: the sidecar's digest write wins over a main write in the same cycle
                    core = mutate(CORE, mdir / CORE.name, [("wire   bg_out_ready = (bs_q == B_HGT) && !fg_wr_en;", "wire   bg_out_ready = (bs_q == B_HGT);", 1), ("    if (!fw_en && bg_take) begin", "    if (bg_take) begin", 1)])
                    must = "test_acvp_keygen"
                elif name == "ncjob":         # NC-ROM (job): the job of KeyGen and Encaps reads from word offset 145 instead of 144
                    t_ = ROM.read_text().split("\n")
                    hits = [i for i, ln in enumerate(t_) if "HFD 0 144 148" in ln and ("keygen" in ln or "encaps" in ln) and f"40'h{CM.encode(('HFD', CM.KB, CM.OFF_EK, 148)):010x}" in ln]
                    assert len(hits) == 2, hits      # the job words of KeyGen and Encaps (the main programs no longer contain this HFD)
                    for i in hits:
                        t_[i] = t_[i].replace(f"40'h{CM.encode(('HFD', CM.KB, CM.OFF_EK, 148)):010x}", f"40'h{CM.encode(('HFD', CM.KB, CM.OFF_EK + 1, 148)):010x}")
                    rom = mdir / ROM.name
                    rom.parent.mkdir(parents=True, exist_ok=True)
                    rom.write_text("\n".join(t_))
                    must = "test_acvp_encaps"
                else:                         # throttled sidecar: one sidecar read every 32 cycles, so that the job outlasts the main work
                    thr = [("  wire        bfd_issue   = (bs_q == B_HFD)", "  logic [4:0] thr_q = 5'd0;\n  always_ff @(posedge clk_i) thr_q <= (state_q == S_IDLE) ? 5'd0 : thr_q + 5'd1;\n  wire        bfd_issue   = (thr_q == 5'd0) && (bs_q == B_HFD)", 1)]
                    if name == "ncthrnj":     # ... and no protection at all: JN, END, HST, HFD, HGT and BGS do not look at the sidecar
                        thr += [("            OpHst: if (!bg_own) begin", "            OpHst: begin", 1), ("            OpJn: if (!bg_own) begin", "            OpJn: begin", 1), ("            OpHfd: if (!bg_own) begin", "            OpHfd: begin", 1),
                                ("            OpHgt:  if (!bg_own) state_q <= S_HGT;", "            OpHgt:  state_q <= S_HGT;", 1), ("            OpEnd: if (!bg_own) begin", "            OpEnd: begin", 1),
                                ("  wire   m_hs_start  = disp && (opc == OpHst) && !bg_own;", "  wire   m_hs_start  = disp && (opc == OpHst);", 1)]
                    core = mutate(CORE, mdir / CORE.name, thr)
                    must = "test_acvp_encaps"
            elif name == "ncwcore":
                assert W2, "ncwcore needs CORE_W2=1"
                LD2 = M / "mlkem_ldpoly2.sv"
                ld2 = mutate(LD2, mdir / LD2.name, [("assign tb_addr_o  = cidx_q;", "assign tb_addr_o  = cidx_q + 8'd1;", 1)])
                must = "test_acvp_encaps"
            else:
                raise SystemExit(f"unknown target {name}")
            eng4_ = eng4
            srcs = [core if f == CORE else rom if f == ROM else (ld2 if (name == "ncwcore" and f.name == "mlkem_ldpoly2.sv") or (name == "ncgrant" and f.name == "mlkem_ldpoly2o.sv") else (eng4_ if eng4_ is not None and f.name == "kpke_sched_smp4.sv" else f)) for f in ENG + MLK]
            ran, failed = build_test(sim, root, name, srcs, True)
            if name in ("ncthr", "ncthrld"):   # the throttled copy must PASS everything: the join waits for a slow job (ncthrld: the engine waits for a slow loader)
                good = bool(ran) and not failed
                print(f"[{sim}] {name}: throttled sidecar passes the whole core target: {good}; failed={failed}" + ("" if good else "  JOIN OR ARBITRATION BROKEN"))
                total += 1
                bad += 0 if good else 1
                ok &= good
                continue
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
