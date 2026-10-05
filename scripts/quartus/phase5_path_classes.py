#!/usr/bin/env python3
"""Group a Quartus `report_timing -detail summary` file by (start block, end block).

Usage: phase5_path_classes.py <paths_summary.rpt>
Read-only: prints, per (from, to) class, the worst slack and the number of paths, in report order.
Bit indices are collapsed to [*]; reducer cut registers are named <instance>.cut<n>
(REG_AFTER position n of modmul_reduce_staged, or of the reducer behind modmul_sel in C4). Nothing is computed beyond grouping.
"""
import re
import sys
from collections import OrderedDict


def node_class(n):
    m = re.search(r"modmul_\w+:(u_mul|u_scale_mul)\|(?:modmul_\w+:[\w.]*u_red\|)?g_cut\[(\d+)\]", n)
    if m:
        return f"{m.group(1)}.cut{m.group(2)}"
    m = re.search(r"(g_arb\[\d+\]\.g_reg\.\w+|u_dly_\w+|state_q|\w+_q)", n)
    return n.split("|")[-2].split(":")[0] + "/" + (m.group(1) if m else n.split("|")[-1])


rows = []
for line in open(sys.argv[1], errors="replace"):
    c = [x.strip() for x in line.split(";")]
    if len(c) > 4 and re.match(r"^-?\d+\.\d+$", c[1]):
        rows.append((float(c[1]), c[2], c[3]))
classes = OrderedDict()
for s, f, t in rows:
    k = (re.sub(r"\[\d+\]", "[*]", node_class(f)), re.sub(r"\[\d+\]", "[*]", node_class(t)))
    w, n = classes.get(k, (s, 0))
    classes[k] = (min(w, s), n + 1)
print(f"{len(rows)} paths; slack min {rows[0][0]:.3f} max {rows[-1][0]:.3f}")
for (f, t), (s, n) in classes.items():
    print(f"{s:7.3f} n={n:3d}  {f}  ->  {t}")
