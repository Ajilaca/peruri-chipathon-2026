#!/usr/bin/env python3
"""Extract MEASURED numbers from Quartus report files into a Markdown evidence file.

Only text that is actually present in the reports is reported. Nothing is estimated,
rounded, or filled in. Missing items are reported as "not found".

Usage:
  extract_quartus_report.py <output_files_dir> <revision> [--log quartus.log]
                            [--out docs/evidence/quartus/<rev>-<UTCdate>.md] [--note "text"]
  extract_quartus_report.py --selftest
"""
import argparse, datetime, os, re, sys, tempfile

FIT_KEYS = [
    "Fitter Status", "Quartus Prime Version", "Revision Name", "Top-level Entity Name",
    "Family", "Device", "Timing Models", "Logic utilization (in ALMs)", "Total registers",
    "Total pins", "Total block memory bits", "Total RAM Blocks", "Total DSP Blocks",
    "Total PLLs", "Total DLLs",
]


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return None


def parse_kv(text):
    """'Key : value' lines (fit.summary)."""
    out = {}
    for line in text.splitlines():
        m = re.match(r"^\s*([^:]+?)\s*:\s*(.*?)\s*$", line)
        if m and m.group(1) not in out:
            out[m.group(1)] = m.group(2)
    return out


def parse_sta_summary(text):
    """Blocks of 'Type : ..', 'Slack : ..', 'TNS : ..' (sta.summary)."""
    rows, cur = [], {}
    for line in text.splitlines():
        m = re.match(r"^\s*(Type|Slack|TNS)\s*:\s*(.*?)\s*$", line)
        if not m:
            continue
        cur[m.group(1)] = m.group(2)
        if m.group(1) == "TNS":
            rows.append(cur); cur = {}
    return rows


def parse_fmax(sta_rpt):
    """Rows of every '... Fmax Summary' panel in <rev>.sta.rpt (tolerant to layout)."""
    if not sta_rpt:
        return []
    out, lines, i = [], sta_rpt.splitlines(), 0
    while i < len(lines):
        if "Fmax Summary" in lines[i] and lines[i].lstrip().startswith(";"):
            model = lines[i].strip("; ").strip()
            j = i + 1
            while j < len(lines) and (lines[j].startswith("+") or not lines[j].strip()):
                j += 1
            hdr = None
            while j < len(lines) and (lines[j].startswith(";") or lines[j].startswith("+")):
                if lines[j].startswith(";"):
                    cells = [c.strip() for c in lines[j].strip().strip(";").split(";")]
                    if hdr is None:
                        hdr = cells
                    else:
                        out.append((model, dict(zip(hdr, cells))))
                j += 1
            i = j
        else:
            i += 1
    return out


def slack_value(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def count_log(path):
    t = read(path) if path else None
    if t is None:
        return None
    return {
        "critical": len(re.findall(r"^Critical Warning", t, re.M)),
        "warnings": len(re.findall(r"^Warning", t, re.M)),
        "errors": len(re.findall(r"^Error", t, re.M)),
    }


def build(outdir, rev, log=None, note=""):
    fit_p = os.path.join(outdir, f"{rev}.fit.summary")
    sta_p = os.path.join(outdir, f"{rev}.sta.summary")
    rpt_p = os.path.join(outdir, f"{rev}.sta.rpt")
    fit, sta, rpt = read(fit_p), read(sta_p), read(rpt_p)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    md = [f"# MEASURED — Quartus results for revision `{rev}`", "",
          f"- Generated: {now} by `extract_quartus_report.py` (values copied from the reports, not computed)",
          f"- Source directory: `{outdir}`"]
    if note:
        md.append(f"- Note: {note}")
    md.append("")

    md += ["## Fitter (`%s.fit.summary`)" % rev, ""]
    if fit is None:
        md += [f"**not found:** `{fit_p}`. Run the Quartus compile first; do not estimate.", ""]
    else:
        kv = parse_kv(fit)
        md += ["| Item | Value (verbatim) |", "|---|---|"]
        for k in FIT_KEYS:
            md.append(f"| {k} | {kv.get(k, 'not found')} |")
        md += ["", "Denominators above are the fitter's own; quote them as printed.", ""]

    md += ["## Timing (`%s.sta.summary`)" % rev, ""]
    worst = {"Setup": None, "Hold": None}
    if sta is None:
        md += [f"**not found:** `{sta_p}`.", ""]
    else:
        rows = parse_sta_summary(sta)
        md += ["| Type | Slack (ns) | TNS |", "|---|---|---|"]
        for r in rows:
            md.append(f"| {r.get('Type','?')} | {r.get('Slack','?')} | {r.get('TNS','?')} |")
            v = slack_value(r.get("Slack"))
            for kind in worst:
                if v is not None and f" {kind} " in " " + r.get("Type", "") + " ":
                    if worst[kind] is None or v < worst[kind][0]:
                        worst[kind] = (v, r.get("Type"))
        md.append("")
        for kind, w in worst.items():
            if w:
                flag = "  **NEGATIVE: timing not met**" if w[0] < 0 else ""
                md.append(f"- Worst {kind.lower()} slack: **{w[0]} ns** ({w[1]}){flag}")
        md.append("")

    md += ["## Fmax (`%s.sta.rpt`, Fmax Summary panels)" % rev, ""]
    fm = parse_fmax(rpt)
    if not fm:
        md += ["Fmax not found in the report (missing file or unrecognised panel layout). "
               "Open the Timing Analyzer report and copy it by hand; do not estimate.", ""]
    else:
        cols = list(fm[0][1].keys())
        md += ["| Model | " + " | ".join(cols) + " |", "|---|" + "---|" * len(cols)]
        for model, row in fm:
            md.append(f"| {model} | " + " | ".join(row.get(c, "") for c in cols) + " |")
        md.append("")

    lg = count_log(log)
    if log:
        md += ["## Compile log message counts", ""]
        if lg is None:
            md += [f"**not found:** `{log}`", ""]
        else:
            md += [f"- Critical warnings: {lg['critical']}", f"- Warnings: {lg['warnings']}",
                   f"- Errors: {lg['errors']}",
                   "", "Critical warnings must be triaged in writing (CLAUDE.md rule 10).", ""]
    return "\n".join(md) + "\n", worst


SAMPLE_FIT = """Fitter Status : Successful - Thu Sep 24 06:01:23 2026
Quartus Prime Version : 25.1std.0 Build 1129 10/21/2025 SC Lite Edition
Revision Name : smoke
Top-level Entity Name : smoke_top
Family : Cyclone V
Device : 5CSEBA6U23I7
Timing Models : Final
Logic utilization (in ALMs) : 17 / 41,910 ( < 1 % )
Total registers : 32
Total pins : 4 / 314 ( 1 % )
Total block memory bits : 0 / 5,662,720 ( 0 % )
Total RAM Blocks : 0 / 553 ( 0 % )
Total DSP Blocks : 0 / 112 ( 0 % )
Total PLLs : 0 / 6 ( 0 % )
Total DLLs : 0 / 4 ( 0 % )
"""
SAMPLE_STA = """------------------------------------------------------------
Timing Analyzer Summary
------------------------------------------------------------

Type  : Slow 1100mV 100C Model Setup 'clk'
Slack : 17.095
TNS   : 0.000

Type  : Slow 1100mV 100C Model Hold 'clk'
Slack : 0.414
TNS   : 0.000

Type  : Fast 1100mV -40C Model Hold 'clk'
Slack : 0.182
TNS   : 0.000
"""
SAMPLE_RPT = """; Slow 1100mV 100C Model Fmax Summary
+-----------+-----------------+------------+------+
; Fmax      ; Restricted Fmax ; Clock Name ; Note ;
+-----------+-----------------+------------+------+
; 250.0 MHz ; 250.0 MHz       ; clk        ;      ;
+-----------+-----------------+------------+------+
"""


def selftest():
    with tempfile.TemporaryDirectory() as d:
        for name, txt in (("smoke.fit.summary", SAMPLE_FIT), ("smoke.sta.summary", SAMPLE_STA),
                          ("smoke.sta.rpt", SAMPLE_RPT)):
            open(os.path.join(d, name), "w").write(txt)
        md, worst = build(d, "smoke")
        assert "17 / 41,910 ( < 1 % )" in md, "ALM line"
        assert "| Total DSP Blocks | 0 / 112 ( 0 % ) |" in md, "DSP line"
        assert worst["Setup"][0] == 17.095, worst
        assert worst["Hold"][0] == 0.182, worst
        assert "250.0 MHz" in md, "Fmax panel"
        md2, _ = build(d, "missing")
        assert md2.count("not found") >= 3, "missing files must say 'not found'"
    print("selftest OK (extract_quartus_report.py)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("outdir", nargs="?")
    ap.add_argument("rev", nargs="?")
    ap.add_argument("--log")
    ap.add_argument("--out")
    ap.add_argument("--note", default="")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.outdir and a.rev):
        ap.error("outdir and rev are required")
    md, _ = build(a.outdir, a.rev, a.log, a.note)
    out = a.out or os.path.join("docs", "evidence", "quartus",
                                 f"{a.rev}-{datetime.datetime.now(datetime.timezone.utc):%Y%m%d}.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(md)
    print(md)
    print(f"written: {out}")


if __name__ == "__main__":
    sys.exit(main())
