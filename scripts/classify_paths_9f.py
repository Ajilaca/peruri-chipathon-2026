#!/usr/bin/env python3
"""scripts/classify_paths_9f.py -- Phase 9F: classifies the worst setup paths of a report written by scripts/phase5m_top_paths.tcl (the *_summary.rpt file: columns Slack, From Node, To Node) into the blocks of the ML-KEM core.
A path is named "<class of From node> -> <class of To node>"; classes are decided from the hierarchy names only (no timing is computed here). Output: for each class pair the number of paths and the worst slack.
Usage: python3 scripts/classify_paths_9f.py REPORT_summary.rpt [REPORT2 ...]
"""
import re
import sys
from collections import OrderedDict

RULES = [
    (r"u_smp\|keccak_sponge(_r2)?:.*keccak_f1600(_r2)?:", "Keccak permutation (sampler sponge)"),
    (r"u_hash\|keccak_sponge(_r2)?:.*keccak_f1600(_r2)?:", "Keccak permutation (hash instance)"),
    (r"u_smp\|", "sampler (outside the permutation)"),
    (r"u_hash\|", "hash wrapper / sponge control"),
    (r"u_ldpoly|u_ld\b|g_ld[12]\.u_ld", "load task"),
    (r"u_stpoly|u_st\b|g_st[12]\.u_st", "store task"),
    (r"u_fo\|", "FO comparison"),
    (r"u_kb\||u_cb\||u_cb2\|", "byte buffer RAM"),
    (r"rf_q|rf_rd_q", "register file"),
    (r"ntt_core|poly_mem|modmul|butterfly|u_ntt|pwm_unit|poly_store", "NTT core / memory / PWM"),
    (r"kpke_sched_smp", "engine sequencer"),
    (r"u_eng\|", "engine (other)"),
]


def cls(node):
    for pat, name in RULES:
        if re.search(pat, node):
            return name
    return "core controller / other"


def main():
    for f in sys.argv[1:]:
        rows = []
        for ln in open(f):
            m = re.match(r";\s*(-?[\d.]+)\s*;\s*(\S+)\s*;\s*(\S+)\s*;", ln)
            if m:
                rows.append((float(m.group(1)), cls(m.group(2)), cls(m.group(3))))
        agg = OrderedDict()
        for s, a, b in sorted(rows):
            k = f"{a} -> {b}"
            n, w = agg.get(k, (0, s))
            agg[k] = (n + 1, min(w, s))
        print(f"## {f}")
        print(f"paths: {len(rows)}, slack {min(r[0] for r in rows):.3f} .. {max(r[0] for r in rows):.3f} ns")
        for k, (n, w) in sorted(agg.items(), key=lambda kv: kv[1][1]):
            print(f"  worst slack {w:7.3f} ns, {n:4d} paths: {k}")


if __name__ == "__main__":
    main()
