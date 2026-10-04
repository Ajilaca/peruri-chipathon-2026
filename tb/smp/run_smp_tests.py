"""tb/smp/run_smp_tests.py -- Phases 8c / 8d verification (docs/evidence/phase08-keccak-stream/8c/test_plan_8c.md V3-V6, 8d/test_plan_8d.md) against one simulator.
Builds rtl/sched/kpke_smp_top_s10.sv for the variant KP_VAR (0 STORE: NPOLY 24; 1 STREAM: NPOLY 12, STREAM_A; 2 OVERLAP: NPOLY 12, STREAM_A, OVERLAP) with tb/smp/test_kpke_smp.py.
  top      the design as it is
  nc<x>    negative controls (test-only copies of rtl/sched/kpke_sched_smp.sv): the bit-exact test must FAIL
             ncij    NC-IJ    message bytes i and j swapped (SampleNTT message)
             ncctr   NC-CTR   CBD counter off by one
             ncalign NC-ALIGN accumulator and gamma addressed one beat late in PWMS            (VAR 1, 2)
             ncvalid NC-VALID a PWMS beat counted without the sampler's valid                   (VAR 1, 2)
             ncacc   NC-ACC   accumulator not used on a middle pass
             nchaz   NC-HAZ   (VAR 2) a transform reads the slot that a non-blocking sample has just started (test-only copy of the ROM)
             ncarb   NC-ARB   (VAR 3) no arbitration of the store write port (wr_free always 1)
Usage: python3 tb/smp/run_smp_tests.py icarus|verilator [top ncij ncctr ncalign ncvalid ncacc ...]   Environment: KP_VAR, KP_CORE_R2, KP_N, KP_BUILD_DIR, KP_CYCLES_OUT_DIR.
"""
import os
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from cocotb_tools.runner import get_runner

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
VAR = int(os.environ.get("KP_VAR", "0"))
R = ROOT / "rtl"
KECCAK = [R / "keccak" / f for f in ("keccak_pkg.sv", "keccak_round.sv", "keccak_f1600.sv", "keccak_sponge.sv", "keccak_f1600_r2.sv", "keccak_sponge_r2.sv")]
SAMPLE = [R / "sample" / f for f in ("sample_ntt_core.sv", "cbd2_core.sv", "keccak_sampler.sv")]
NTT = [R / "ntt" / f for f in ("ntt_pkg.sv", "twiddle_rom.sv", "pipe_delay.sv", "modmul_reduce_staged.sv")] + [R / "arith" / f for f in ("twiddle_rom_half.sv", "modmul_fold.sv", "modmul_barrett.sv", "modmul_montgomery.sv", "modmul_sel.sv", "half_mod.sv", "butterfly_m6.sv")] \
    + [R / "mem" / "poly_mem_m10k.sv", R / "ntt" / "ntt_core_s10.sv", R / "ntt" / "ntt_core_s10_p5.sv"]
SCHED = [R / "sched" / f for f in ("gamma_rom.sv", "kpke_smp_prog_rom.sv", "poly_store_smp.sv", "pwm_unit.sv", "kpke_sched_smp.sv", "kpke_smp_top_s10.sv")]
SEQ = R / "sched" / "kpke_sched_smp.sv"
PARAMS = {0: {"NPOLY": 24, "VAR": 0, "STREAM_A": 0, "OVERLAP": 0}, 1: {"NPOLY": 12, "VAR": 1, "STREAM_A": 1, "OVERLAP": 0}, 2: {"NPOLY": 12, "VAR": 2, "STREAM_A": 1, "OVERLAP": 1}, 3: {"NPOLY": 12, "VAR": 3, "STREAM_A": 1, "OVERLAP": 1}}[VAR]
if "KP_CORE_R2" in os.environ:        # Phase 9F S1: the K0 sampler (0) or the C5 sampler (1) in the sequencer tests
    PARAMS = {**PARAMS, "CORE_R2": int(os.environ["KP_CORE_R2"])}
ROM = R / "sched" / "kpke_smp_prog_rom.sv"
MUT = {
    "ncij": [("msg_b32_q <= 8'(a_q % 5'd3);   // j = m mod 3", "msg_b32_q <= 8'(a_q / 5'd3);"), ("msg_b33_q <= 8'(a_q / 5'd3);   // i = m div 3", "msg_b33_q <= 8'(a_q % 5'd3);")],
    "ncctr": [("msg_b32_q <= {3'd0, b_q};", "msg_b32_q <= {3'd0, b_q} + 8'd1;")],
    "ncalign": [("wire [6:0]   rd_idx  = in_pwms ? nxt[6:0] : cnt_q[6:0];", "wire [6:0]   rd_idx  = in_pwms ? bcnt_q[6:0] : cnt_q[6:0];")],
    "ncvalid": [("assign beat  = STREAM_A && (state_q == S_PWMS) && smp_cvalid && smp_pwm_q;", "assign beat  = STREAM_A && (state_q == S_PWMS) && smp_pwm_q;")],
    "ncacc": [(".acc0_i(first_q ? 12'd0 : acc_rd_e), .acc1_i(first_q ? 12'd0 : acc_rd_o),", ".acc0_i(12'd0), .acc1_i(12'd0),")],
}
NEEDS_STREAM = {"ncalign", "ncvalid"}
# ROM mutation: the first transform of the OVERLAP KeyGen reads the slot that the non-blocking sample just started (a data hazard)
ROM_MUT = {"nchaz": [("{2'd2, 2'd0, 6'd2}: op_o = {4'd1, 1'b0, 1'b0, 5'd0, 5'd0, 5'd0};", "{2'd2, 2'd0, 6'd2}: op_o = {4'd1, 1'b0, 1'b0, 5'd1, 5'd0, 5'd0};")]}
MUT["ncarb"] = [("wire wr_free = OVERLAP ? !seq_wr && !idle_st : 1'b1;", "wire wr_free = 1'b1;")]
ONLY_VAR = {"nchaz": 2, "ncarb": 3}


def mutate(dst, edits, src=SEQ):
    t = src.read_text()
    for old, new in edits:
        assert t.count(old) == 1, f"{src.name}: pattern {old!r} found {t.count(old)} times"
        t = t.replace(old, new)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(t)
    return dst


def build_test(sim, root, name, sources):
    bd = root / f"sim_build_{sim}_v{VAR}_{name}"
    r = get_runner(sim)
    r.build(sources=sources, hdl_toplevel="kpke_smp_top_s10", build_dir=bd, parameters=PARAMS, build_args=["--timing", "-Wno-fatal"] if sim == "verilator" else [], always=True)
    out = Path(os.environ.get("KP_CYCLES_OUT_DIR", str(bd))) / f"cycles_v{VAR}_{sim}_{name}.json"
    if out.exists():
        out.unlink()
    res = r.test(hdl_toplevel="kpke_smp_top_s10", test_module="test_kpke_smp", test_dir=HERE, build_dir=bd, results_xml=str(bd / "results.xml"), extra_env={"KP_CYCLES_OUT": str(out), "KP_VAR": str(VAR)})
    cases = ET.parse(res).getroot().findall(".//testcase")
    ran = [c for c in cases if c.find("skipped") is None]
    failed = [c.get("name") for c in ran if c.find("failure") is not None or c.find("error") is not None]
    return ran, failed


def run(sim, root, names):
    ok, total, bad = True, 0, 0
    for name in names:
        if name == "top":
            ran, failed = build_test(sim, root, name, KECCAK + SAMPLE + NTT + SCHED)
            good = bool(ran) and not failed
            print(f"[{sim}] top (VAR={VAR}): {len(ran) - len(failed)}/{len(ran)} " + ("PASS" if good else f"FAIL {failed}"))
            total += len(ran)
            bad += len(failed) if failed else (0 if good else 1)
        else:
            if (name in NEEDS_STREAM and VAR == 0) or (name in ONLY_VAR and ONLY_VAR[name] != VAR):
                continue
            if name in ROM_MUT:
                m = mutate(root / f"mut_{sim}_{name}" / ROM.name, ROM_MUT[name], ROM)
                swap = {ROM: m}
            else:
                m = mutate(root / f"mut_{sim}_{name}" / SEQ.name, MUT[name])
                swap = {SEQ: m}
            ran, failed = build_test(sim, root, name, KECCAK + SAMPLE + NTT + [swap.get(p, p) for p in SCHED])
            good = "test_programs_bit_exact" in failed
            print(f"[{sim}] {name}: test_programs_bit_exact failed as required: {good}; failed={failed}" + ("" if good else "  NEGATIVE CONTROL VOID"))
            total += 1
            bad += 0 if good else 1
        ok &= good
    print(f"[{sim}] TOTAL: {total - bad}/{total} passed")
    return ok


if __name__ == "__main__":
    sim = sys.argv[1] if len(sys.argv) > 1 else "icarus"
    names = sys.argv[2:] or ["top", "ncij", "ncctr", "ncalign", "ncvalid", "ncacc", "nchaz", "ncarb"]
    root = Path(os.environ.get("KP_BUILD_DIR") or tempfile.mkdtemp(prefix="chip2026_8c_"))
    sys.exit(0 if run(sim, root, names) else 1)
