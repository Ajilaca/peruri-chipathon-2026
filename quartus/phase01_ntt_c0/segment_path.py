#!/usr/bin/env python3
"""Attribute the data-path delay of one Quartus `report_timing -detail full_path` path to design
structures, using only the element names and incremental delays printed by Quartus.

Usage: python3 segment_path.py <report.rpt> [path_index=1]
Rules (by element-name substring, first match wins):
  modulo divider    : "Mod0|"                  (lpm_divide inferred from `%` in modmul_reduce.sv)
  DSP multiplier    : "Mult0~mac"
  memory read mux   : "u_mem|Mux"
  memory write/reg  : "mem_wdata", "u_mem|mem["
  butterfly add/sub : "u_bfly|Add", "u_bfly|LessThan", "u_bfly|" (other)
  control/address   : everything else on the data path (FSM, len/log2len lookup, shifts, j/jlen
                      adders, mem_addr muxes, scale path muxes)
Each row's Incr (cell delay or the interconnect feeding it) is charged to that row's element.
"""
import re, sys, collections

RULES = [("modulo divider (lpm_divide)", ["Mod0|"]),
         ("DSP multiplier", ["Mult0~mac"]),
         ("memory read mux (poly_mem)", ["u_mem|Mux"]),
         ("memory write mux + storage reg", ["mem_wdata", "u_mem|mem["]),
         ("butterfly add/sub mod", ["u_bfly|"]),]

def cat(el):
    for name, keys in RULES:
        if any(k in el for k in keys):
            return name
    return "control / address logic"

def parse(path, idx=1):
    lines = open(path).read().split("\n")
    starts = [i for i, l in enumerate(lines) if re.match(r"^Path #\d+:", l)]
    s = starts[idx - 1]
    e = starts[idx] if idx < len(starts) else len(lines)
    block = lines[s:e]
    head = {}
    for l in block:
        m = re.match(r"^; (From Node|To Node|Data Arrival Time|Data Required Time|Slack)\s*;\s*(.*?)\s*;", l)
        if m:
            head[m.group(1)] = m.group(2)
    # data arrival path rows
    try:
        a = next(i for i, l in enumerate(block) if "Data Arrival Path" in l)
        r = next(i for i, l in enumerate(block) if "Data Required Path" in l)
    except StopIteration:
        return head, None, None
    rows = []
    in_data = False
    for l in block[a:r]:
        p = [x.strip() for x in l.split(";")]
        if len(p) < 8:
            continue
        if p[7] == "data path":
            in_data = True
            continue
        if not in_data:
            continue
        try:
            incr = float(p[2])
        except ValueError:
            continue
        rows.append((incr, p[4], p[7]))
    agg = collections.OrderedDict()
    for incr, typ, el in rows:
        c = cat(el)
        agg[c] = agg.get(c, 0.0) + incr
    return head, agg, rows

if __name__ == "__main__":
    f = sys.argv[1]
    idx = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    head, agg, rows = parse(f, idx)
    print(f"## {f} (path #{idx})")
    for k in ("From Node", "To Node", "Data Arrival Time", "Data Required Time", "Slack"):
        print(f"{k}: {head.get(k)}")
    if agg:
        tot = sum(agg.values())
        print(f"data-path delay attributed: {tot:.3f} ns")
        for k, v in sorted(agg.items(), key=lambda kv: -kv[1]):
            print(f"  {k:34s} {v:7.3f} ns  ({100*v/tot:5.1f} %)")
        n_div = sum(1 for _, t, el in rows if t == "CELL" and "Mod0|" in el)
        print(f"  cells inside lpm_divide on this path: {n_div}")
