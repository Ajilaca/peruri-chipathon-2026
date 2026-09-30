#!/usr/bin/env python3
"""formal/run_formal_slang.py

Runs every SymbiYosys proof of Phases 1-3 with the yosys-slang frontend and `memory_map -rom-only`,
plus negative controls, and checks each result against its expected status.

  A. Phase 3 proofs (formal/phase03-multilane/ntt_core_c2*_safety.sby, already written for this flow):
     C2, C2-K2, C2-K2-K1 at NUM_LANES = 1, 2, 4, 8. Expected: PASS.
  B. Negative controls, generated here from a deliberately corrupted COPY of rtl/mem/bank_map_rom.sv
     (the repository RTL is never modified). Expected: FAIL / UNKNOWN as listed -- if one of these
     passes, the corresponding PASS in (A) would be vacuous.
  C. Phase 1 and Phase 2 proofs, converted on the fly to the same flow (their committed .sby and
     formal-top files are read, not modified). Expected: PASS.

Properties covered by these proofs: FSM handshake (busy_o drop -> done_o one cycle later), and for
Phase 3 bank_overflow_o == 0 plus the t_q / layer_q range invariants; Phase 2's bank_map proof is the
own-pair property on the generated ROM. They do NOT prove NTT/INTT bit-exactness or memory data
integrity (simulation evidence covers those).

Usage: . scripts/env.sh && python3 formal/run_formal_slang.py
Work directories go to formal/work/ (git-ignored). Exit code 0 only if every result is as expected.
"""
import pathlib
import re
import shutil
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
WORK = HERE / "work"
RESET_OLD = "  initial assume (!rst_ni);\n"
RESET_NEW = ("  logic f_init = 1'b1;\n  always_ff @(posedge clk_i) f_init <= 1'b0;\n"
             "  always_comb if (f_init) assume (!rst_ni);\n")


def run_sby(sby_path: pathlib.Path, name: str, timeout: int = 1800):
    """Returns (status, detail, seconds). status in PASS / FAIL / UNKNOWN / ERROR / TIMEOUT."""
    out = WORK / name
    t0 = time.time()
    try:
        p = subprocess.run(["sby", "-f", "-d", str(out), str(sby_path)], cwd=sby_path.parent,
                           capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "TIMEOUT", "", time.time() - t0
    log = p.stdout + p.stderr
    m = re.search(r"DONE \((\w+), rc=\d+\)", log)
    status = m.group(1) if m else "ERROR"
    parts = re.findall(r"summary: engine_\d+ \([^)]*\) returned (\w+)(?: for (\w+))?", log)
    detail = ", ".join(f"{b or 'bmc'}={a}" for a, b in dict.fromkeys(parts))
    fa = re.search(r"failed assertion .* at (\S+?):(\d+)", log)
    if fa:
        detail += f"; failed assert {pathlib.Path(fa.group(1)).name}:{fa.group(2)}"
    return status, detail, time.time() - t0


def parse_sby(path: pathlib.Path):
    s = path.read_text()
    files = [x.strip() for x in s[s.index("[files]"):].splitlines()[1:] if x.strip()]
    top = re.search(r"^prep -top (\S+)$", s, re.M).group(1)
    options = s[s.index("[options]"):s.index("[script]")]
    return s, files, top, options


def make_slang_sby(src: pathlib.Path, dst_dir: pathlib.Path, *, replace=None, options=None):
    """Writes a slang-flow copy of a native-flow or slang-flow .sby into dst_dir with absolute [files]
    paths. `replace` maps a source basename to a substitute file path."""
    s, files, top, opts = parse_sby(src)
    dst_dir.mkdir(parents=True, exist_ok=True)
    g = re.search(r"-G (\w+=\d+)", s)
    abs_files = []
    for f in files:
        p = (src.parent / f).resolve()
        if replace and p.name in replace:
            p = replace[p.name]
        elif RESET_OLD in p.read_text():           # Phase 1/2 formal tops: slang-compatible reset assume
            q = dst_dir / p.name
            q.write_text(p.read_text().replace(RESET_OLD, RESET_NEW))
            p = q
        abs_files.append(p)
    names = " ".join(p.name for p in abs_files)
    script = ("[script]\nplugin -i slang\n"
              f"read_slang -D FORMAL {names} --top {top}" + (f" -G {g.group(1)}" if g else "") + "\n"
              f"prep -top {top}\nmemory_map -rom-only\n\n")
    text = (options or opts) + script + "[files]\n" + "\n".join(str(p) for p in abs_files) + "\n"
    out = dst_dir / (src.stem + ".sby")
    out.write_text(text)
    return out


def corrupt_bank_map(num_banks: int, addr: int, dst: pathlib.Path):
    """Copy of rtl/mem/bank_map_rom.sv with the bank of one address changed, for one NUM_BANKS."""
    src = (ROOT / "rtl/mem/bank_map_rom.sv").read_text()
    a = src.index(f"if (NUM_BANKS == {num_banks})")
    nxt = src.find("if (NUM_BANKS == ", a + 10)
    b = nxt if nxt != -1 else len(src)
    blk = src[a:b]
    m = re.search(rf"(8'd{addr}: begin bank_o = (\d)'d)(\d+);", blk)
    wrong = int(m.group(3)) ^ 1
    new = blk.replace(m.group(0), f"{m.group(1)}{wrong};", 1)
    assert new != blk
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(src[:a] + new + src[b:])
    return f"bank_map_rom copy, NUM_BANKS={num_banks}: bank({addr}) {m.group(3)} -> {wrong}"


def main() -> int:
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir()
    rows = []  # (group, name, expected, status, detail, secs)

    p3 = HERE / "phase03-multilane"
    for cfg, label in (("ntt_core_c2", "C2"), ("ntt_core_c2_k2", "C2-K2"), ("ntt_core_c2_k2_k1", "C2-K2-K1")):
        for L in (1, 2, 4, 8):
            sby = p3 / f"{cfg}_l{L}_safety.sby"
            st, det, sec = run_sby(sby, sby.stem)
            rows.append(("A Phase 3", f"{label} L={L}", "PASS", st, det, sec))

    bmc60 = "[options]\nmode bmc\ndepth 60\n\n[engines]\nsmtbmc boolector\n\n"
    ncs = [
        ("NC-A", "ntt_core_c2_l2_safety.sby", 2, 128, None, "FAIL",
         "violation in the first NTT cycle -> must be caught by the base case"),
        ("NC-B", "ntt_core_c2_l2_safety.sby", 2, 40, None, "UNKNOWN",
         "violation beyond depth 6 -> base case passes, induction must fail"),
        ("NC-B/bmc60", "ntt_core_c2_l2_safety.sby", 2, 40, bmc60, "FAIL",
         "same corruption, BMC depth 60 -> the violation is real and reachable"),
        ("NC-C", "ntt_core_c2_k2_k1_l8_safety.sby", 8, 128, None, "FAIL",
         "selected config C2-K2-K1 L=8, violation in the first NTT cycle"),
    ]
    for tag, sby_name, nb, addr, opts, expected, why in ncs:
        d = WORK / ("negctl_" + tag.replace("/", "_"))
        what = corrupt_bank_map(nb, addr, d / "mutant" / "bank_map_rom.sv")
        sby = make_slang_sby(p3 / sby_name, d, replace={"bank_map_rom.sv": d / "mutant" / "bank_map_rom.sv"},
                             options=opts)
        st, det, sec = run_sby(sby, d.name + "_run")
        rows.append(("B Negative control", f"{tag}: {what} ({why})", expected, st, det, sec))

    for sub, name, label in (("phase01-ntt", "ntt_core_safety.sby", "Phase 1 ntt_core (C0) FSM safety"),
                             ("phase02-mem", "ntt_core_c1_safety.sby", "Phase 2 ntt_core_c1 (C1) FSM safety"),
                             ("phase02-mem", "bank_map_safety.sby", "Phase 2 bank_map_rom own-pair (NUM_BANKS=8)")):
        d = WORK / ("rerun_" + name.replace(".sby", ""))
        sby = make_slang_sby(HERE / sub / name, d)
        st, det, sec = run_sby(sby, d.name + "_run")
        rows.append(("C Phase 1/2 re-run", label, "PASS", st, det, sec))

    ok = True
    print("| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |")
    print("|---|---|---|---|---|---|---|")
    for grp, name, exp, st, det, sec in rows:
        good = st == exp
        ok &= good
        print(f"| {grp} | {name} | {exp} | {st} | {det} | {sec:.1f} | {'yes' if good else '**NO**'} |")
    print()
    print(f"OVERALL: {'all results as expected' if ok else 'MISMATCH -- see table'} "
          f"({sum(1 for r in rows if r[3] == r[2])}/{len(rows)})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
