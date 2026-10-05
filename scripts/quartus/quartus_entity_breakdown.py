#!/usr/bin/env python3
"""scripts/quartus/quartus_entity_breakdown.py

Groups Quartus "Fitter Resource Utilization by Entity" rows (from <rev>.fit.rpt) by function for
the Phase 3 C2 family (ntt_core_c2 and its variants), so ALM can be attributed to multipliers,
butterfly logic, memory, address/control, etc. Values are copied from the report, only summed.

Usage: python3 scripts/quartus/quartus_entity_breakdown.py TAG1 path/to/A.fit.rpt [TAG2 path/to/B.fit.rpt ...]
The delta column is last TAG minus first TAG.
"""
import re
import sys
from collections import defaultdict

# (regex on full hierarchy name, group key, use the node's own resources instead of its total)
GROUPS = [
    (r"modmul_reduce:u_fwd_mul$", "fwd_mul", False),
    (r"modmul_reduce:u_inv_mul$", "inv_mul", False),
    (r"modmul_reduce:u_mul$", "shared_mul", False),
    (r"modmul_reduce:u_scale_mul$", "scale_mul", False),
    (r"butterfly\w*:g_lane\[\d+\]\.u_bfly$", "bfly_own", True),
    (r"twiddle_rom:g_lane\[\d+\]\.u_rom$", "twiddle_rom", False),
    (r"bank_map_rom:g_map\[\d+\]\.u_map$", "bank_map_rom", False),
    (r"poly_mem_multiport:u_mem$", "mem_own", True),
    (r"ntt_core_c2\w*:u_dut$", "core_own", True),
    (r"ntt_core_c2\w*_l\d$", "top_own", True),
]


def parse(path):
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    start = next(i for i, l in enumerate(lines) if l.startswith("; Fitter Resource Utilization by Entity"))
    rows = []
    for l in lines[start + 4:]:
        if l.startswith("+"):
            break
        c = [x.strip() for x in l.split(";")[1:-1]]
        if len(c) < 15:
            continue
        tot = lambda s: float(s.split("(")[0].strip() or 0)
        own = lambda s: float(s.split("(")[1].rstrip(")")) if "(" in s else 0.0
        rows.append(dict(alm=tot(c[1]), alm_own=own(c[1]), alut=tot(c[6]), alut_own=own(c[6]),
                         reg=tot(c[7]), reg_own=own(c[7]), dsp=tot(c[11]), full=c[14]))
    return rows


def group(rows):
    g = defaultdict(lambda: dict(alm=0.0, alut=0.0, reg=0.0, dsp=0.0, n=0))
    for r in rows:
        for pat, key, use_own in GROUPS:
            if re.search(pat, r["full"]):
                d = g[key]
                d["n"] += 1
                if use_own:
                    d["alm"] += r["alm_own"]; d["alut"] += r["alut_own"]; d["reg"] += r["reg_own"]
                else:
                    d["alm"] += r["alm"]; d["alut"] += r["alut"]; d["reg"] += r["reg"]; d["dsp"] += r["dsp"]
                break
    return g


def main(argv):
    res = {}
    for tag, path in zip(argv[1::2], argv[2::2]):
        rows = parse(path)
        res[tag] = (rows[0], group(rows))
    tags = list(res)
    for t in tags:
        top = res[t][0]
        print(f"TOTAL {t}: ALM={top['alm']} ALUT={top['alut']:.0f} REG={top['reg']:.0f} DSP={top['dsp']:.0f}")
    hdr = "".join(f" | {t}: n ALM ALUT REG DSP" for t in tags)
    print(f"{'group':12s}{hdr}" + (" | dALM dALUT" if len(tags) > 1 else ""))
    for _, key, _ in GROUPS:
        vals = [res[t][1].get(key, dict(alm=0, alut=0, reg=0, dsp=0, n=0)) for t in tags]
        if all(v["n"] == 0 for v in vals):
            continue
        cols = "".join(f" | {v['n']:>2d} {v['alm']:8.1f} {v['alut']:6.0f} {v['reg']:5.0f} {v['dsp']:3.0f}" for v in vals)
        d = (f" | {vals[-1]['alm'] - vals[0]['alm']:+8.1f} {vals[-1]['alut'] - vals[0]['alut']:+6.0f}"
             if len(vals) > 1 else "")
        print(f"{key:12s}{cols}{d}")
    for t in tags:
        print(f"{t}: sum of groups ALM = {sum(v['alm'] for v in res[t][1].values()):.1f} "
              "(differs from TOTAL only by per-node rounding)")


if __name__ == "__main__":
    main(sys.argv)
