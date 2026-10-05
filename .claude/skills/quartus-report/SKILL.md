---
name: quartus-report
description: Compile a Quartus project for the DE10-Nano (Cyclone V 5CSEBA6U23I7) and turn the real reports into a MEASURED evidence file (ALM, registers, M10K, DSP, slack, Fmax). Use whenever the user asks for resource usage, timing, Fmax, "does it fit", "timing closed", or any FPGA implementation number. Never report such numbers from Yosys, memory, or estimates.
---

# quartus-report

Quartus is the only source of FPGA implementation numbers in this project
(CLAUDE.md §5.1). This skill runs a compile and records what Quartus printed.

## 1. Compile (long: run in the background)

```bash
. scripts/env.sh                       # Quartus + OSS CAD Suite on PATH
cd quartus/<project_dir>
nohup quartus_sh --flow compile <revision> > compile.log 2>&1 &
```

- A compile takes minutes. Do not block on it and do not paste whole `.rpt` files
  into the conversation; extract the panels you need.
- The revision's reports appear in `output_files/` (ignored by Git; the *extract* is
  what gets committed).
- Pin assignments come from Terasic's DE10-Nano documentation or the GHRD. Never invent
  pin locations.

## 2. Extract the evidence

```bash
python3 .claude/skills/quartus-report/scripts/extract_quartus_report.py \
    quartus/<project_dir>/output_files <revision> \
    --log quartus/<project_dir>/compile.log \
    --note "<what changed: git commit, parameters, clock>"
```

It writes `evidence/quartus/<revision>.md` containing:
fitter summary (verbatim), timing slack table, worst setup/hold slack, Fmax panels if
present, and Critical Warning / Warning / Error counts from the log.

## 3. Rules when you report the result

1. Label every number MEASURED and cite the evidence file path. Quote fitter
   denominators exactly as printed (they can differ from the datasheet).
2. Negative slack = timing not met. Say so plainly. Never say "timing closed"
   without a fresh `sta.summary` showing non-negative worst setup and hold slack for
   all corners.
3. Fmax is only real if it comes from the Timing Analyzer's Fmax Summary panel for a
   constrained clock. If the script prints "Fmax not found", open the report and copy the
   panel by hand. Do not compute Fmax from slack yourself.
4. Critical warnings are triaged in writing (list them, say what each means, and
   whether it is acceptable). Never waive one just to turn a result green.
5. One compile ≠ a trend. When comparing two revisions, compare the two evidence files.
6. Proposal tables (ALM, registers, M10K, DSP) may be filled with numbers only from an
   evidence file; before that they stay `ESTIMATE` (method + assumptions) or `[...]`.

## Known limits

- The parser was validated on the `fit.summary` / `sta.summary` text logged from this
  team's Quartus Prime Lite 25.1std run (`docs/TOOLING_INSTALL_LOG.md`).
- The Fmax panel parser is untested against a real 25.1 `sta.rpt`. If it misreads,
  fix the parser or copy by hand; say which.
- `--selftest` checks the parser against embedded samples.
