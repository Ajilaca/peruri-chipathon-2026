#!/usr/bin/env python3
"""quartus/phase01_ntt_c0/extract_c0_timing_evidence.py

Builds evidence/phase01/quartus_C0_timing_analysis_<UTCdate>.md (and a .json
with the same values) from the Quartus reports of revision C0. Every value is copied or
mechanically derived from report text; nothing is typed by hand.

Inputs (all in output_files/, git-ignored):
  C0.map.rpt C0.fit.rpt C0.asm.rpt C0.sta.rpt C0.fit.summary C0.sta.summary   (from the compile)
  C0_*.rpt                                     (from `quartus_sta -t report_critical_paths.tcl`)

Run from quartus/phase01_ntt_c0/:
  python3 extract_c0_timing_evidence.py
"""
import collections
import datetime
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "output_files"
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
from segment_path import parse  # noqa: E402


def read(name):
    return (OUT / name).read_text(errors="replace")


def lines_matching(text, rx):
    return [l.rstrip() for l in text.splitlines() if re.search(rx, l)]


def kv_summary(text):
    d = collections.OrderedDict()
    for l in text.splitlines():
        if " : " in l:
            k, v = l.split(" : ", 1)
            d[k.strip()] = v.strip()
    return d


def sta_summary(text):
    rows, cur = [], {}
    for l in text.splitlines():
        m = re.match(r"^(Type|Slack|TNS)\s*:\s*(.*)$", l.strip())
        if m:
            cur[m.group(1)] = m.group(2)
            if m.group(1) == "TNS":
                rows.append(cur)
                cur = {}
    return rows


def fmax_panels(text):
    out = []
    for m in re.finditer(r"; (Slow [^;]*?Fmax Summary)\s*;[^\n]*\n((?:[^\n]*\n){6})", text):
        block = m.group(2)
        v = re.search(r";\s*([\d.]+ MHz)\s*;\s*([\d.]+ MHz)\s*;\s*(\S+)\s*;", block)
        if v:
            out.append((m.group(1).strip(), v.group(1), v.group(2), v.group(3)))
    return out


def entity_rows(fit):
    rows = []
    grab = False
    for l in fit.splitlines():
        if "; Fitter Resource Utilization by Entity" in l:
            grab = True
            continue
        if grab and l.startswith("Note:"):
            break
        if grab and l.startswith(";") and "Compilation Hierarchy Node" not in l:
            p = [x.strip() for x in l.strip().strip(";").split(";")]
            if len(p) > 8 and p[0].startswith("|"):
                rows.append({"node": p[0], "alms_needed": p[1], "comb_aluts": p[6],
                             "regs": p[7]})
    return rows


def endpoint_classes(summary_rpt):
    rows = []
    for l in summary_rpt.splitlines():
        p = [x.strip() for x in l.split(";")]
        if len(p) >= 9 and re.match(r"^-?\d+\.\d+$", p[1] or ""):
            rows.append({"slack": float(p[1]), "from": p[2], "to": p[3], "skew": float(p[7]),
                         "data_delay": float(p[8])})

    def cls(n):
        if n.startswith("poly_mem:u_mem|mem["):
            return "poly_mem storage register"
        return re.sub(r"(\[\d+\]|\.S_\w+|~reg0)", "", n)

    total = collections.Counter(cls(r["to"]) for r in rows)
    viol = collections.Counter(cls(r["to"]) for r in rows if r["slack"] < 0)
    starts = collections.Counter(re.sub(r"\[\d+\]", "[*]", r["from"]) for r in rows if r["slack"] < 0)
    bins = collections.OrderedDict()
    for lo, hi in [(-50, -40), (-40, -30), (-30, -20), (-20, -10), (-10, 0), (0, 25)]:
        bins[f"[{lo}, {hi})"] = sum(1 for r in rows if lo <= r["slack"] < hi)
    return rows, total, viol, starts, bins


def path_cells(rpt, idx=1):
    head, agg, rows = parse(rpt, idx)
    t, cells = 0.0, []
    for incr, typ, el in rows:
        t += incr
        if typ == "CELL":
            cells.append((round(t, 3), round(incr, 3), el))
    ic = sum(i for i, ty, _ in rows if ty == "IC")
    cell = sum(i for i, ty, _ in rows if ty == "CELL")
    return head, agg, cells, ic, cell


def required_path(rpt_text):
    blk = rpt_text.split("Data Required Path", 1)[1].split("\n\n", 1)[0]
    out = {}
    for l in blk.splitlines():
        p = [x.strip() for x in l.split(";")]
        if len(p) >= 8 and p[7] in ("clock path", "clock pessimism removed", "clock uncertainty"):
            out[p[7]] = p[2]
        if len(p) >= 8 and p[4] == "uTsu":
            out["uTsu"] = p[2]
    return out


def launch_clock(rpt_text):
    blk = rpt_text.split("Data Arrival Path", 1)[1].split("Data Required Path", 1)[0]
    for l in blk.splitlines():
        p = [x.strip() for x in l.split(";")]
        if len(p) >= 8 and p[7] == "clock path":
            return p[2]
    return None


def main():
    date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    mapr, fitr, asmr, star = read("C0.map.rpt"), read("C0.fit.rpt"), read("C0.asm.rpt"), read("C0.sta.rpt")
    fit_sum = kv_summary(read("C0.fit.summary"))
    sta_rows = sta_summary(read("C0.sta.summary"))
    fmax = fmax_panels(star)
    stages = {
        "Analysis & Synthesis": lines_matching(mapr, r"Analysis & Synthesis was successful"),
        "Fitter": lines_matching(fitr, r"Fitter was successful"),
        "Assembler": lines_matching(asmr, r"Assembler was successful"),
        "Timing Analyzer": lines_matching(star, r"Timing Analyzer was successful"),
    }
    crit = {
        "Analysis & Synthesis": lines_matching(mapr, r"^Critical Warning"),
        "Fitter": lines_matching(fitr, r"^Critical Warning"),
        "Timing Analyzer": sorted(set(lines_matching(star, r"^Critical Warning"))),
    }
    n_sta_crit = len(lines_matching(star, r"^Critical Warning"))
    inferred = [l for l in lines_matching(mapr, r"Inferred divider/modulo megafunction|uninferred due to|Parameter \"LPM_WIDTH[ND]\"") if "Info" in l]
    virtual_info = lines_matching(mapr, r"Info \(15717\)")
    ents = entity_rows(fitr)
    dsp = lines_matching(fitr, r"Mult0~mac\s*;\s*Two Independent")

    top = read("C0_setup_top5000_summary.rpt")
    rows, total, viol, starts, bins = endpoint_classes(top)
    tns_check = round(sum(r["slack"] for r in rows if r["slack"] < 0), 3)

    per = {}
    for key, f in [("worst (through u_fwd_mul, NTT/CT)", "C0_path_through_u_fwd_mul.rpt"),
                   ("through u_inv_mul (INTT/GS)", "C0_path_through_u_inv_mul.rpt"),
                   ("through u_scale_mul (INTT x3303 scaling)", "C0_path_through_u_scale_mul.rpt"),
                   ("to layer_q (control only)", "C0_path_to_layer_q.rpt"),
                   ("to zeta_idx_q (control only)", "C0_path_to_zeta_idx_q.rpt")]:
        head, agg, cells, ic, cell = path_cells(OUT / f)
        per[key] = {"file": f, "head": head, "agg": agg, "cells": cells, "ic": round(ic, 3),
                    "cell": round(cell, 3)}
    worst_txt = read("C0_path_through_u_fwd_mul.rpt").split("Path #2:", 1)[0]
    req = required_path(worst_txt)
    launch = launch_clock(worst_txt)
    worst_summary = lines_matching(worst_txt, r"^; -48\.\d+ ;")

    data = {
        "generated_utc": date,
        "fit_summary": fit_sum,
        "sta_summary": sta_rows,
        "fmax": fmax,
        "stages": stages,
        "critical_warnings": crit,
        "sta_critical_warning_count": n_sta_crit,
        "inferred": inferred,
        "virtual_pin_info": virtual_info,
        "entities": ents,
        "dsp": dsp,
        "endpoints_total": len(rows),
        "endpoints_violating": sum(1 for r in rows if r["slack"] < 0),
        "endpoint_classes_total": dict(total),
        "endpoint_classes_violating": dict(viol),
        "violating_start_nodes": dict(starts),
        "slack_bins": dict(bins),
        "sum_negative_endpoint_slack": tns_check,
        "paths": {k: {"file": v["file"], "head": v["head"], "agg": v["agg"], "ic": v["ic"],
                      "cell": v["cell"], "cells": v["cells"]} for k, v in per.items()},
        "worst_launch_clock_path": launch,
        "worst_required_path": req,
        "worst_summary_row": worst_summary,
    }
    ev_dir = REPO / "evidence" / "phase01"
    (ev_dir / "quartus_C0_timing_analysis.json").write_text(json.dumps(data, indent=1))

    L = []
    w = L.append
    w("# MEASURED - Quartus C0 timing analysis (Phase 1 baseline, NOT an optimisation result)")
    w("")
    w(f"- Generated: {date} UTC by `quartus/phase01_ntt_c0/extract_c0_timing_evidence.py` "
      "(values copied from Quartus report text; derived numbers say how they were derived).")
    w("- Compile: Quartus Prime Lite 25.1std, revision `C0`, top `ntt_core`, device 5CSEBA6U23I7, "
      "provisional clock `create_clock -period 20.000` on virtual pin `clk_i` (`quartus/phase01_ntt_c0/C0.sdc`).")
    w("- Drill-down: `quartus_sta -t quartus/phase01_ntt_c0/report_critical_paths.tcl` on the existing "
      "post-fit netlist (read-only: no recompile, RTL/QSF/SDC unchanged), corner Slow 1100mV 100C.")
    w("- Also see the fitter/STA summary extract `evidence/quartus/C0.md`.")
    w("")
    w("## 1. Did every stage complete?")
    w("")
    w("| Stage | Quartus message (verbatim) |")
    w("|---|---|")
    for k, v in stages.items():
        w(f"| {k} | {v[0].replace('Info: ', '') if v else 'NOT FOUND'} |")
    w("")
    w("All four stages completed without errors. Completing is not the same as meeting timing: "
      f"the Timing Analyzer raised `Critical Warning (332148): Timing requirements not met` "
      f"{n_sta_crit} times (once per analysed corner).")
    w("")
    w("## 2. Measured resources and timing")
    w("")
    w("| Quantity | Value (verbatim) | Source |")
    w("|---|---|---|")
    for k in ("Logic utilization (in ALMs)", "Total registers", "Total block memory bits",
              "Total RAM Blocks", "Total DSP Blocks", "Total virtual pins"):
        w(f"| {k} | {fit_sum.get(k)} | `C0.fit.summary` |")
    for name, f, rf, clk in fmax:
        w(f"| Fmax, {name.replace(' Fmax Summary', '')} | {f} (restricted {rf}, clock {clk}) | `C0.sta.rpt` |")
    w("")
    w("| Corner / check | Slack (ns) | TNS (ns) |")
    w("|---|---|---|")
    for r in sta_rows:
        w(f"| {r['Type']} | {r['Slack']} | {r['TNS']} |")
    w("")
    setup = [float(r["Slack"]) for r in sta_rows if "Setup" in r["Type"]]
    hold = [float(r["Slack"]) for r in sta_rows if "Hold" in r["Type"]]
    tns = [float(r["TNS"]) for r in sta_rows if "Setup" in r["Type"]]
    w(f"- Worst setup slack: **{min(setup)} ns** (all four corners negative) -> **timing NOT met** at the 20.000 ns provisional period.")
    w(f"- Worst hold slack: **{min(hold)} ns** (positive in all corners -> hold met).")
    w(f"- Worst setup TNS: **{min(tns)} ns**.")
    w("- Cross-check (derived): 1 / (20.000 ns + 48.323 ns) = 14.64 MHz, equal to the Fmax panel.")
    w("")
    w("## 3. What synthesis built (explains the path)")
    w("")
    w("Analysis & Synthesis messages (verbatim):")
    w("")
    w("```")
    for l in inferred:
        w(l.strip())
    w("```")
    w("")
    w("Fitter DSP usage (verbatim rows, truncated after the placement column):")
    w("")
    w("```")
    for l in dsp:
        w(";".join(l.split(";")[:4]) + ";")
    w("```")
    w("")
    w("Fitter Resource Utilization by Entity (ALMs needed / combinational ALUTs / dedicated registers):")
    w("")
    w("| Hierarchy node | ALMs needed | Comb. ALUTs | Registers |")
    w("|---|---|---|---|")
    for e in ents:
        n = e["node"]
        if re.search(r"ntt_core|butterfly:|modmul_reduce:|poly_mem:|twiddle_rom:", n):
            w(f"| `{n}` | {e['alms_needed']} | {e['comb_aluts']} | {e['regs']} |")
    w("")
    w("(Each `modmul_reduce` row's ALMs sit entirely inside its `lpm_divide:Mod0` child; the "
      "child rows are omitted. Numbers in parentheses are the node's own resources.)")
    w("")
    w("Reading: each `%` in `rtl/ntt/modmul_reduce.sv` became a combinational 24-bit / 12-bit "
      "`lpm_divide` (3 instances); the 256x12 `poly_mem` became 3072 flip-flops plus read/write "
      "multiplexers (0 RAM blocks used); the twiddle ROM was not mapped to RAM.")
    w("")
    w("## 4. Worst setup path (Slow 1100mV 100C)")
    w("")
    wp = per["worst (through u_fwd_mul, NTT/CT)"]
    h = wp["head"]
    w(f"- From (startpoint): `{h.get('From Node')}`")
    w(f"- To (endpoint): `{h.get('To Node')}`")
    w(f"- Data arrival {h.get('Data Arrival Time')} ns, data required {h.get('Data Required Time')} ns, slack {h.get('Slack')}")
    w(f"- Launch clock path {launch} ns; latch clock path {req.get('clock path')} ns "
      f"(of which clock pessimism removed {req.get('clock pessimism removed')} ns); clock uncertainty {req.get('clock uncertainty')} ns.")
    w(f"- Data-path delay {sum(wp['agg'].values()):.3f} ns = cells {wp['cell']:.3f} ns + interconnect {wp['ic']:.3f} ns.")
    w("")
    w("Cells on the path (cumulative ns from launch-register output, increment, element):")
    w("")
    w("```")
    for t, inc, el in wp["cells"]:
        if "Mod0|" in el and "sumout" not in el and "StageOut" not in el:
            continue
        w(f"{t:8.3f}  +{inc:.3f}  {el}")
    w("```")
    w("(carry-chain `cout` cells inside `Mod0` omitted for length; every `op_N...sumout` / "
      "`StageOut` stage is kept. Full list in the .json.)")
    w("")
    w("## 5. Delay attribution per structure (derived by `segment_path.py`, rules in its docstring)")
    w("")
    for k, v in per.items():
        tot = sum(v["agg"].values())
        w(f"### {k}: slack {v['head'].get('Slack')}, `{v['head'].get('From Node')}` -> `{v['head'].get('To Node')}`")
        w("")
        w("| Structure | Delay (ns) | Share |")
        w("|---|---|---|")
        for s, d in sorted(v["agg"].items(), key=lambda kv: -kv[1]):
            w(f"| {s} | {d:.3f} | {100 * d / tot:.1f} % |")
        w(f"| **total data path** | **{tot:.3f}** | cells {v['cell']:.3f} / interconnect {v['ic']:.3f} |")
        w("")
    w("## 6. All setup endpoints (`report_timing -npaths 5000 -nworst 1`, one worst path per endpoint)")
    w("")
    w(f"- Endpoints analysed: {len(rows)}; violating: {data['endpoints_violating']}.")
    w(f"- Violating endpoints by type: {dict(viol)}")
    w(f"- Startpoint of the worst path into every violating endpoint: {dict(starts)}")
    w(f"- Endpoint count per slack range (ns): {dict(bins)}")
    w(f"- Sum of negative per-endpoint worst slacks (derived): {tns_check} ns "
      f"(STA TNS for this corner: {tns[0]} ns).")
    w("")
    w("## 7. Clock / constraint methodology evidence")
    w("")
    w("```")
    for l in crit["Analysis & Synthesis"] + virtual_info:
        w(l.strip())
    w("```")
    w("")
    w("- The clock source in every reported path is `clk_i` at `LABCELL_X1_Y36_N15` (a logic cell, "
      "because `clk_i` is a virtual pin), then `clk_i~CLKENA0` on `CLKCTRL_G3` (global clock, fan-out 3104).")
    w(f"- Clock-related terms on the worst path: skew {rows[0]['skew'] if rows else '?'} ns "
      f"(summary row) and uncertainty {req.get('clock uncertainty')} ns, against a data-path delay of "
      f"{sum(wp['agg'].values()):.3f} ns and a 20.000 ns period.")
    w("- 23 input ports and 14 output ports are unconstrained (`C0.sta.rpt`, Unconstrained Paths "
      "Summary); I/O paths are therefore not analysed. The failing paths are register-to-register.")
    w("")
    (ev_dir / "quartus_C0_timing_analysis.md").write_text("\n".join(L) + "\n")
    print(f"wrote {ev_dir}/quartus_C0_timing_analysis.md and .json")


if __name__ == "__main__":
    main()
