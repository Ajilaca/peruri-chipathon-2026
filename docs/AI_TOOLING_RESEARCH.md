# AI / EDA Tooling Research — CHIP 2026 Hackathon

**Scope:** research, audit, comparison and installation decision for AI agents, Claude Code
plugins, MCP servers, skills and EDA tools, for a DE10-Nano / Cyclone V / Quartus project.
**Not in scope:** choosing the problem, the subtheme, the architecture, or writing project RTL.
**Audit date:** 2026-09-23. Repository states are as of that date (last-commit dates below).

---

> **Addendum 2026-09-28 (the audit below is unchanged).**
> - The official page lists **four** subthemes (adds 04 Secure Communication); §3 shows three.
> - The project idea is now chosen (ML-KEM-768 accelerator, ADR 0001), so the scope line above
>   ("not in scope: choosing the problem") is historical.
> - Environment facts verified on the team machine (2026-09-24, `docs/TOOLING_INSTALL_LOG.md`):
>   Quartus Prime Lite 25.1std compiled the smoke design for 5CSEBA6U23I7; Questa found (licence
>   variable unset); Claude Code 2.1.232; `rtl-agent-team` 0.14.6 enabled at project scope;
>   no board attached.
> - Added since: project skills in `.claude/skills/` (`quartus-report`, `proposal-claims`,
>   `mlkem-guard`, `decision-record`, `phase-gate`), permissions and marketplace declaration in
>   `.claude/settings.json`, `scripts/setup_github.sh`, and skill/GitHub checks in
>   `scripts/setup_tooling.sh verify`. They are project-owned, not third-party tools.
> - The rtl-agent-team Stop-gates stay dormant until `.rat/` exists (§9.1); activating them is
>   open decision PENDING #13.
> - This file moved from the repository root to `docs/` (CLAUDE.md already referred to it there).

## 1. Executive summary

No evaluated AI tool understands the DE10-Nano, Cyclone V or Quartus end to end. The useful
tools are vendor-neutral **RTL-and-verification** agents plus a **mature open-source
verification toolchain**; Quartus itself must remain the only source of implementation numbers,
driven by project-owned scripts that Claude Code runs through its normal shell access.

Decisions (details in §18):

| Tool | Decision |
|---|---|
| Intel Quartus Prime Lite + Cyclone V device support + Questa Starter | **INSTALL NOW** (manual; script verifies) |
| OSS CAD Suite (Verilator, Icarus, Yosys + slang, SymbiYosys, solvers, slang) | **INSTALL NOW** |
| Python venv: cocotb 2.1.0, pyslang 11.0.0, pytest 9.1.1 | **INSTALL NOW** |
| rtl-agent-team (Claude Code plugin, project scope) | **INSTALL NOW** — primary agent pipeline |
| weft-mcp (Quartus MCP) | **INSTALL LATER** — after a Cyclone V report smoke test |
| GateFlow | **OPTIONAL** — fallback only; never together with rtl-agent-team |
| FPGA-LSP, babyworm/systemverilog-lsp | **OPTIONAL** |
| SynthPilot, oh-my-fpga, abbbe/fpga-mcp-servers, wmm246/fpga-mcp, shroudpro/Quartus-MCP | **DO NOT INSTALL** |

Findings that change how the team should work:

- **The template's flip-flop capacity (415,000) is wrong.** Intel documents 166,036 registers
  for the Cyclone V SE A6.
- **cocotb 2.1 does not build against Ubuntu 24.04's apt Verilator 5.020**, and apt Yosys 0.33
  cannot parse common SystemVerilog. Use the OSS CAD Suite instead (verified).
- **"Verified" claims in agent repositories did not all hold.** GateFlow's asynchronous FIFO
  fails its own testbench in two independent simulators.
- **Syntax-level LSPs miss real bugs.** Verible (FPGA-LSP) missed non-existent port names that
  Verilator and slang both caught.
- The earlier provisional pick of GateFlow was **reversed** after a head-to-head (§16):
  rtl-agent-team is far more mature (724 commits, 1,718 unit tests), MIT-licensed, and enforces
  verification with stop-gates, at the cost of more context and ASIC-oriented phases that must
  be switched off by policy.

---

## 2. Project context

- **Competition:** CHIP 2026 Hackathon (PERURI Digital Summit), category *IC Chip Design & FPGA
  Implementation*.
- **Target:** Terasic DE10-Nano, Cyclone V SE SoC **5CSEBA6U23I7** (FPGA fabric + dual
  Cortex-A9 HPS).
- **Toolchain:** Intel Quartus Prime, SystemVerilog/Verilog.
- **Required workflow capabilities:** RTL simulation, synthesis, timing and resource analysis,
  SignalTap, and real-time hardware validation.

The official proposal template requires:

- executive summary, problem statement, architecture and RTL modules;
- resource estimation against DE10-Nano capacity;
- a test plan covering RTL simulation, corner cases, timing/latency, synthesis, bitstream,
  SignalTap and on-board real-time tests;
- success metrics, references, source repository and technical documentation.

The AI workflow therefore has to support the full chain, not just code generation:

```
Problem → Architecture → HW/SW partition → RTL → Verification → Simulation → Synthesis
→ Resource/Timing analysis → Optimisation → FPGA implementation → SignalTap
→ Hardware validation → Documentation
```

### Device capacity (primary sources)

| Resource | Cyclone V SE A6 (Intel device overview) |
|---|---|
| ALMs | 41,910 |
| Registers | **166,036** (template says 415,000 — incorrect) |
| M10K memory | 5,570 Kb |
| MLAB memory | 621 Kb |
| Variable-precision DSP blocks | 112 (224 × 18×18 multipliers) |
| FPGA PLLs | 6 |

Quartus fitter denominators can differ from the product table. A published DE10-Nano fit report
shows 553 M10K blocks, whereas the product table lists 557. Utilisation must be quoted with the
fitter's own denominator.

---

## 3. Hackathon subthemes

| # | Subtheme | Focus | Named baselines |
|---|---|---|---|
| 01 | Secure Identity & Security Element | Authentication, integrity, key handling, anti-tamper | Peruri chip, TT07 SHA-256, ECC, PUF |
| 02 | Hardware Cryptography Accelerator | Small, area-efficient crypto blocks integrated into a baseline | TT07 SHA-256, other crypto designs |
| 03 | AI / Edge Accelerator | MAC accelerator, small NN, vector compute, edge inference | TT07 Iterative MAC, TinyTPU, Mini AIE |

The TT07 baselines are real Tiny Tapeout 7 shuttle projects. The TT07 chip map includes:

- **#718 "tiny sha256"**, described as a single-cycle-round core;
- an **RO-PUF**;
- **TinyTPU**;
- a **mini-AIE 2×2 CGRA**.

They are reference designs, not tooling, and were not code-audited here; that belongs to the
next phase. No subtheme has been selected.

---

## 4. Evaluation methodology

Each candidate was cloned and inspected at code level, not judged from its README. Where
possible, its claims were **reproduced** in an isolated Linux sandbox (Ubuntu 24.04), using:

- Claude Code 2.1.280, for plugin validation and install tests;
- Verilator, Icarus, Yosys, SymbiYosys and slang (both apt and OSS CAD Suite builds);
- each project's own test suite.

**Evidence levels** used below:

| Level | Meaning |
|---|---|
| **E3 – Reproduced** | Behaviour observed by running it in the audit sandbox |
| **E2 – Code-inspected** | Read in source, not executed |
| **E1 – Documented** | Stated by the project (README/changelog/catalog) only |
| **LOW EVIDENCE** | Few commits/contributors, no releases, or no demonstrated hardware workflow. Not an automatic rejection: the capability is judged separately |

The criteria A–Y from the brief (purpose, architecture, RTL generation/verification, simulation,
synthesis interaction, Quartus/Cyclone V/DE10-Nano/Linux support, Claude Code integration, MCP,
licence, activity, commits, releases, issues, docs, install complexity, evidence of use, overlap,
project value) are covered per tool in §5–§9 and consolidated in §10–§16.

**Popularity was not a ranking input.** Star counts could not be collected uniformly because
the GitHub API rate-limited the sandbox. Commit history comes from the clones.

**Limitation:** no agent was asked to design real project RTL, so **the quality of agent-written
RTL was not measured**. That requires a chosen problem (next phase) and should be evaluated then
on a small block with a golden model.

---

## 5. GateFlow analysis

**Repository:** `codejunkie99/Gateflow-Plugin`. **Decision: OPTIONAL (fallback only).**

**Purpose and architecture (E2).** A Claude Code plugin made of Markdown skills, agents and
commands plus Python hook scripts. It contains 27 skills, 20 agents and 21 commands, a 4-board
database and an 8-block "verified IP" library. Its orchestrator (`/gf`) runs
plan → build → lint → test → formal → synth loops, invoking open-source tools through Bash.
Configuration lives in `.claude/gateflow.local.md`.

**Maturity (E2).**
- 149 commits between 2026-01-29 and **2026-05-21 (last commit)**.
- Essentially one author (two identities on one account) plus one external commit.
- 13 tags, v1.4.3 → v2.5.3.
- The GitHub page showed about 104 stars, 13 forks and 2 open issues on the audit date.
- Its test suite (`tests/`) covers only the CLI/TUI/validator, **not RTL flows**.

**Licence.** BSL-1.1, with an Additional Use Grant covering non-commercial, personal,
educational or evaluation use. Commercial or production use requires contacting the licensor.
It converts to Apache-2.0 on 2028-01-30. The generated RTL is the team's, but using the plugin
inside a commercial venture needs a licence check.

**Component relevance for DE10-Nano / Cyclone V / Quartus:**

| Component | Relevant? | Notes |
|---|---|---|
| `sv-planner` / `gf-plan` | Yes (vendor-neutral) | Block diagrams, FSMs, interfaces, verification plan |
| `sv-codegen`, `sv-developer`, `sv-refactor` | Yes (vendor-neutral) | Generic synthesizable SV |
| `sv-testbench`, `gf-cocotb`, `tb-best-practices` | Yes | SV and cocotb testbenches |
| `sv-debug`, `gf-errors`, `gf-summary` | Yes | Simulation-failure and X-propagation triage |
| `sv-formal`, `gf-formal`, `sv-verification` | Yes, per module | SymbiYosys runs independent of vendor, if the front-end parses the SV |
| `gf-architect`, `sv-understanding`, `gf-viz`, `gf-scan/map` | Yes | Hierarchy, FSM extraction, CDC detection |
| `sv-orchestrator` / `gf-build` | Conditional | Parallel builds; fine once the architecture is fixed |
| `sv-synth` / `gf-synth` | **No — harmful** | Yosys only (iCE40/ECP5/Gowin/Xilinx/generic); its output format looks like FPGA utilisation but is not Quartus |
| `gf-pnr`, `/gf-flash` | **No** | nextpnr (iCE40/ECP5/Gowin); the skill itself states Intel is unsupported |
| `sv-pinmap`, `/gf-boards` | **No** | Boards: Arty A7, Basys 3, iCEBreaker, Tang Nano 9K. **No DE10-Nano** |
| `gf-pcb`, VHDL agents, `gf-learn`, TUI, release/audit tools | No | Not relevant |
| `gf-fusesoc` | Maybe later | Mentions a Quartus backend via Edalize (E1) |

**Reproduced tests on its "verified" IP library (E3).** Apt Verilator 5.020 and Icarus 12 were
used, plus Yosys `synth_intel_alm -family cyclonev` for elaboration.

| Block | Verilator lint | Simulation (own TB) | Notes |
|---|---|---|---|
| axi4lite_slave | clean | PASS | |
| cdc_2ff | clean | PASS | |
| cdc_handshake | clean | PASS | |
| debouncer | clean | PASS | |
| fifo_sync | clean | PASS | |
| uart | 2 warnings | PASS (both simulators) | |
| **fifo_async** | clean | **FAIL in Verilator and Icarus** | TB samples a first-word-fall-through (combinational read) FIFO as if registered; old Yosys could not parse it, OSS CAD Suite Yosys + slang can |
| **spi_master** | clean | **No verdict** | TB fails to elaborate in Icarus (assigns an unresolved wire); no pass/fail output in Verilator |

Two Cyclone V implementation notes, both inferred and **not measured**. The async FIFO's
combinational read and the reset-coupled memory write are unlikely to infer M10K blocks. A
Quartus fit would show whether they land in MLAB or registers.

**Install mechanics (E3).**
- The plugin validates under Claude Code 2.1.280, with one warning: its plugin-root `CLAUDE.md`
  (a SystemVerilog reference) is *not* loaded as context.
- `claude plugin marketplace add codejunkie99/Gateflow-Plugin` followed by
  `claude plugin install gateflow@gateflow --scope project` succeeded.
- Hooks do not auto-install anything; they print guidance.
- **Selective install is impractical.** Agents invoke each other through the `gateflow:`
  namespace (e.g. `gateflow:sv-codegen` 16×, `sv-refactor` 8×, `sv-testbench` 7×), so copying
  individual files breaks the orchestrator.

**Context cost (E3):** about 21.7k characters (~5.4k tokens) of skill/agent/command frontmatter
listed each session.

**Verdict.** GateFlow is the best **lightweight** vendor-neutral RTL loop found, but it:
- supports none of Intel/Quartus/Cyclone V/DE10-Nano;
- has partially broken "verified" examples;
- has been inactive for four months;
- is BSL-licensed.

It is the fallback if rtl-agent-team proves too heavy in practice. Never enable both.

---

## 6. FPGA-LSP analysis

**Repository:** `nyavana/fpga-lsp`. **Conclusion: USEFUL BUT OPTIONAL. LOW EVIDENCE.**
**Decision: OPTIONAL.**

**Purpose and architecture (E2).** A Claude Code plugin that wires two language servers into
Claude Code's native LSP support via `.lsp.json`:
- Verible (SystemVerilog/Verilog);
- rust_hdl `vhdl_ls` (VHDL).

It adds three wrapper skills (`sv-lint`, `sv-format`, `sv-diff`), an `sv-reviewer` agent, and
two hooks: a SessionStart installer plus filelist generator, and a PostToolUse
**format-on-save**. It generates RTL: no. It simulates or synthesises: no. It needs MCP: no.
It is Linux x64 auto-install only.

**Maturity (E2).** **2 commits, both on 2026-05-07**, one author, MIT, plugin v1.0.0, no tags.
It is spec-driven (OpenSpec files) with a CI workflow. It was dogfooded on the author's DE1-SoC
SystemVerilog project, the same Cyclone V SoC family.

**Reproduced (E3):**
- The pinned Verible `v0.0-4053-g89d4d98a` installer downloaded and passed its hard-coded
  SHA-256 check.
- The generated filelist enabled cross-file analysis.
- The plugin manifest validates, and install/uninstall at local scope succeeded.
- Over raw LSP JSON-RPC, the server advertised definition, references, formatting, rename,
  symbols and diagnostics.

LSP behaviour on a 3-file test project:

| Capability | Result |
|---|---|
| Syntax diagnostics (missing `;`) | Caught |
| Style lint (line length etc.) | Caught |
| Cross-file go-to-definition (module → other file) | **Works** |
| Hover | Nearly empty (`### module uart_tx`) |
| Find-references (local signal) | Returned empty |
| Non-existent port names on an instance | **Missed** (Verilator and slang both reported errors) |
| Undeclared signal on an `assign` LHS | Not flagged. It is a legal implicit net; the real fix is `` `default_nettype none `` |

**Assessment.** It provides fast syntax feedback and navigation for Claude, but it is **not a
semantic checker**; Verilator and slang via Bash already provide the important diagnostics.

Risks:
- The format-on-save hook rewrites any `.sv` file Claude touches in place, producing noisy diffs
  across the team.
- Community documentation describes Claude Code's LSP integration as experimental, with
  version-specific regressions.

If an LSP is wanted later, the slang-based `babyworm/systemverilog-lsp` (§9) should be
semantically stronger. That rests on the underlying engine: pyslang 11 flagged all three bad
ports. The plugin's slang-server build itself was not tested.

---

## 7. SynthPilot analysis

**Repository:** `LNC0831/SynthPilot` (docs only). **Decision: DO NOT INSTALL.**

**Classification: PROPRIETARY, with FREE and PAID tiers.** The GitHub repository contains only
a README, a changelog and generated tool catalogs (6 files, 9 commits, tags v1.2.5 and v1.4.0).
The software ships as a proprietary PyPI package. It is an MCP server with one platform per
session: Vivado (510 tools), TangDynasty (102) or Quartus (24).

**Quartus capability (E1, from its own catalog, product v1.3.1 index):**

| Plan | Quartus tools |
|---|---|
| Free (6) | Connection info, capabilities, version probe, restart, test connection, licence status |
| Pro (all 24) | Project create/open/close, add source file, set top, start/cancel build, build status/log, fitter resource usage, report panels, part info, device families, assignments, design names |

- Everything that matters (builds, reports, resource usage) is **paid**.
- There is **no SignalTap**, no programming (`quartus_pgm`), no dedicated timing-analysis tool
  (only generic report-panel reads), and no Platform Designer/HPS.
- Quartus acceptance is stated as **verified only for Windows Lite 25.1**; Standard, Pro and
  Linux are "in validation".
- Cyclone V and DE10-Nano: nothing specific.

**Verdict.** Its Free tier cannot build or read reports, the paid tier is unverified on Linux,
and everything it offers is reachable with Quartus Tcl/CLI directly. No purchase, no install.

---

## 8. oh-my-fpga analysis

**Repository:** `LNC0831/oh-my-fpga`. **Decision: DO NOT INSTALL.**

**What it is (E2).** MIT-licensed, v0.1.0, 3 commits (2026-06-05 → 06-09), one author. It holds
13 Markdown skills: timing-closure, CDC audit, constraints authoring, full flow, sim bring-up,
coverage, lint triage, QoR, utilisation, power, Zynq bring-up, ILA debug, and bitstream
programming.

**Dependency (E2).**
- It is **not standalone**. Every skill states it requires the SynthPilot MCP connected to an
  open **Vivado** session with the Tcl server on port 9999, and calls Vivado-specific SynthPilot
  tools (e.g. `report_timing_summary`, `hw_ila_read_data`).
- A full-text search found **zero** references to Quartus, Intel, Cyclone or SignalTap.
- It is methodology only. It gives Claude no ability to run Quartus, and its tool names would
  not exist in any Quartus session.

**Salvage.** Its four design principles (verification-first, never fake-pass, smallest safe
change first, surface trade-offs then stop) are sound and are adopted, with attribution, in
`CLAUDE.md`.

---

## 9. Additional tools discovered

Searches covered: Claude Code FPGA / SystemVerilog agents, Quartus / Cyclone V / DE10-Nano MCP,
FPGA synthesis MCP, RTL verification agents, HDL LSP, timing and resource agents, and
crypto/NN hardware tooling.

### 9.1 rtl-agent-team — **INSTALL NOW (primary)**

- **Repository:** `babyworm/rtl-agent-team`. MIT licence.
- **Activity:** 724 commits (2026-02-25 → **2026-08-24**), 15 tags (latest v0.14.6), mainly one
  author across several identities.
- **Tests (E3):** 1,718 unit tests collected. 1,701 passed, 16 were skipped, and **1 failed only
  because the sandbox's apt Yosys 0.33 lacks `$check` cells** (an environment issue, not a
  plugin defect).
- **Structure (E2):** 99 agents and 97 skills in a 6-phase pipeline: Research → Architecture →
  µArch → RTL → Verify → Design Note.
- **Notable agents:**
  - `ref-model-dev` and `ref-model-reviewer` (golden models);
  - `security-reviewer`;
  - SVA extraction and policy;
  - `cocotb-reviewer`;
  - CDC checker and reviewer;
  - `synthesizability-gate`;
  - `synthesis-reviewer`, which has an explicit FPGA-resource branch;
  - `design-note-writer`, `requirement-tracer` and `test-plan-writer`.
- **EDA runner (E2):** drives Verilator, Yosys, SymbiYosys and cocotb through Bash. Its
  synthesis path is Yosys generic or Liberty-mapped (ASIC).
  **It has no Quartus support**, so the same "never report Yosys numbers" rule applies.
- **Hooks (E2):** 15 hooks (SessionStart, Pre/PostToolUse, Subagent, and 5 Stop gates).
  - They are **dormant unless the project contains `.rat/`**, created by `rat-init-project`.
  - When active, the Stop gates **block ending a session if RTL files were modified without
    verification**; there are explicit waiver and reset markers.
  - This enforces the project's "verify before claiming" rule mechanically.
- **Setup (E1):** `rat-setup` is interactive and opt-in. It can install cocotb/SystemC and can
  deploy global rules to `~/.claude/rules`. Answer **skip** to SystemC and to global deployment.
- **Install (E3):**
  - `claude plugin marketplace add babyworm/rtl-agent-team` registered the marketplace
    `rtl-agent-marketplace`.
  - `claude plugin install rtl-agent-team@rtl-agent-marketplace --scope project` succeeded and
    wrote only `.claude/settings.json`: no `.rat/` directory, no global files.
- **Context cost (E3):** about 50.9k characters (~12.7k tokens) of skill/agent descriptions per
  session, about 2.3× GateFlow.
- **Fit:** vendor-neutral for RTL and verification. ASIC-oriented for implementation (DC,
  Liberty, DFT, PPA), and those phases are out of scope by policy.

### 9.2 weft-mcp — **INSTALL LATER**

- **Repository:** `FPGArtktic/weft-mcp`. GPL-3.0-only.
- **Activity:** 85 commits concentrated on 2026-08-22/23, 5 tags (v0.1.0–v0.5.0), single author.
  The history is short, but the engineering and documentation quality are high.
- **What it is (E2):** an MCP server for Quartus Prime **25.1** (Lite/Standard/Pro). It offers:
  - lint and simulation in a rootless Podman container with `--network=none`;
  - workspace path sandboxing;
  - async Quartus compile jobs;
  - report parsing to compact JSON (resources, timing per clock);
  - source indexing, document RAG and documentation generation.
- **Not yet available:** programming. There is no SignalTap.
- **Tests (E3):** its suite ran **295 passed, 18 skipped** (the skips need live tools).
- **Honest limits (E1):** the author verified it only against Quartus 25.1 Lite on a **MAX 10**
  demo, and states the bitstream was never loaded onto hardware.
- **Cyclone V concern (E2):** its resource parser maps a `Total ALMs` label. Cyclone V flow
  summaries are believed to label this `Logic utilization (in ALMs)`; this is **unconfirmed**.
  If so, the ALM count would be silently absent. `setup_tooling.sh verify` records the real
  Cyclone V summary labels verbatim so this can be settled with evidence.
- **Why later:**
  - It needs Quartus 25.1 exactly, plus Podman and Python ≥ 3.11.
  - Claude Code can already run the same Quartus commands via Bash.
  - Its value, structured compact results, matters once builds and report volume grow.

### 9.3 abbbe/fpga-mcp-servers — **DO NOT INSTALL** (pattern reference)

- **What it is (E2):** two Python MCP servers, `quartus-mcp` and `de10nano-mcp`, the only tool
  found that is **explicitly for Quartus + DE10-Nano**.
  - Async `make`-based builds with a single-build lock and 1-hour timeout.
  - RBF deploy over SSH (backup, copy, reboot, poll).
  - Serial U-Boot recovery.
  - Register-read verification.
- **Why not (E2):**
  - **No licence file** (all rights reserved by default).
  - 11 commits in one week (Jan 2026).
  - Hard-coded paths (`/opt/altera_lite/24.1std/...`) and hosts (`analog.local`).
  - It assumes a project-specific Makefile (an ADI reference design).
- **Salvage:** its async-build and deploy/recovery *patterns* are good design references for the
  team's own scripts. Do not copy its code.

### 9.4 wmm246/fpga-mcp — **DO NOT INSTALL**

- **What it claims (E1):** MIT-licensed, v0.1.4, 7 commits. An MCP server with 816 tools,
  **167 of them for Quartus** (STA, `quartus_map/fit/asm/pgm`), over a JSON-over-TCP Tcl server
  on port 9998.
- **Problems (E3/E2):**
  - **From a fresh clone its tests fail at import (8 collection errors).** `pyproject.toml`
    packages `src/fpga_mcp`, but the code lives directly in `src/`, so the "69 tests pass" claim
    was not reproducible.
  - It exposes an arbitrary-Tcl "escape hatch" over TCP.
  - There is no SignalTap.
- **Status:** could be re-evaluated from the PyPI build later, but it offers nothing that
  project scripts don't.

### 9.5 shroudpro/Quartus-MCP — **DO NOT INSTALL**

Targets Quartus II 9.1 and a MAX II lab board. Irrelevant to Cyclone V (E1, not code-audited).

### 9.6 babyworm/systemverilog-lsp — **OPTIONAL**

- MIT, 9 commits (last 2026-04-25), pinned by SHA from the rtl-agent-team marketplace.
- It wires **slang-server** as a Claude Code LSP, and builds slang-server from C++ source (git,
  cmake, a C++20 compiler).
- The build was not performed in the audit. The **slang engine itself** (pyslang 11.0.0 and the
  slang 11 CLI) was tested and correctly reports non-existent ports and unconnected ports.
- The project already gets that check from the `slang` CLI via Bash, so the LSP adds navigation
  only.

### 9.7 Verification toolchain components — **INSTALL NOW**

**OSS CAD Suite** (YosysHQ; open-source components under their own licences). The 2026-09-23
Linux x64 build was downloaded in the audit: about 742 MB, 218 s to download and extract. Its
`bin/` contains:
- Verilator 5.053, Icarus 14 (devel) and Yosys 0.69;
- the yosys **slang** plugin, SymbiYosys, and the z3, bitwuzla, boolector and yices solvers;
- the `slang` CLI and `cocotb-config`.

Reproduced with it (E3):
- a cocotb 2.1.0 smoke test **passed on Verilator and Icarus**;
- a SymbiYosys **k-induction proof passed**;
- `slang` caught the port errors;
- `yosys -m slang` parsed GateFlow's `fifo_async.sv`, which apt Yosys 0.33 rejected.

**cocotb** (BSD-3-Clause). Python testbenches let `hashlib` and NumPy act as golden models.
Pinned at **2.1.0**.

**Critical compatibility finding (E3):** cocotb 2.1.0 **fails to compile its VPI shim against
Ubuntu 24.04's apt Verilator 5.020**. The build fails with `doInertialPuts` and `evalNeeded`
not found in `VerilatedVpi`. Hence the OSS CAD Suite's Verilator.

**pyslang 11.0.0.** Semantic elaboration checks from Python and scripts.

### 9.8 Domain tooling (crypto / PUF / NN)

No AI agent or MCP specialised for SHA-256, ECC, PUF or NN-accelerator design on FPGA was found.
Domain support comes from:

- **Reference designs:** the TT07 projects named by the organisers (§3).
- **Golden models:** Python `hashlib`, integer or fixed-point NumPy models, and published test
  vectors.
- **Agent roles:** rtl-agent-team's `ref-model-dev` and `security-reviewer`.

Tools such as hls4ml were not evaluated, because an HLS flow for Cyclone V is outside the
proposal's RTL-centred scope.

---

## 10. Quartus compatibility

| Tool | Drives Quartus? | How | Verified on | SignalTap | Programming |
|---|---|---|---|---|---|
| Quartus CLI via Bash (project scripts) | **Yes** | `quartus_sh`, `quartus_sta`, `quartus_pgm`, `quartus_stp` | Script written; Quartus smoke test **not run in audit** (no Quartus in sandbox) | Yes (`quartus_stp`) | Yes |
| weft-mcp | Yes | Managed `quartus_sh`, report parser | 25.1 Lite, MAX 10 (author) | No | Not yet |
| SynthPilot | Paid tier only | Proprietary | Windows Lite 25.1 (vendor) | No | No |
| abbbe quartus-mcp | Yes | `make` wrapper | Author's 24.1std setup | No | Via SSH + RBF |
| wmm246 fpga-mcp | Claims yes | Tcl server | Not reproducible from source | No | Claims `quartus_pgm` |
| GateFlow / rtl-agent-team / oh-my-fpga / FPGA-LSP | **No** | — | — | — | — |

**Quartus availability:** Quartus Prime Lite 25.1 is published for Linux. Cyclone V device
support is a separate download placed alongside the installer. Lite is the free edition and
covers Cyclone V.

---

## 11. DE10-Nano compatibility

- **No agent's board database includes the DE10-Nano.** GateFlow's 4 boards are Xilinx, Lattice
  and Gowin.
- Only abbbe's MCP targets the board, and it is unlicensed and hard-wired to one lab setup.
- **Pin assignments** must come from Terasic's DE10-Nano documentation and reference designs
  (System Builder output or the golden hardware reference design). They must never come from an
  agent's board database, or be guessed.
- **HPS/FPGA integration** (Platform Designer, HPS-to-FPGA and lightweight bridges, the Linux
  image, device tree) is **not covered by any evaluated tool**. It is a gap (§19).
- **USB-Blaster II on Linux** needs udev rules before `jtagconfig`/`quartus_pgm` see the board.
  The setup script logs `jtagconfig` output but cannot fix permissions.

---

## 12. Linux compatibility

| Tool | Linux status |
|---|---|
| Quartus Prime Lite 25.1 | Official Linux package |
| OSS CAD Suite | Official Linux x64 build; **E3** |
| cocotb, pyslang | PyPI wheels; **E3** on Ubuntu 24.04 / Python 3.12 |
| rtl-agent-team, GateFlow | Markdown + shell/Python hooks; **E3** install on Linux |
| FPGA-LSP | Linux x64 auto-install only; **E3** |
| weft-mcp | Linux (Arch, Ubuntu 24.04 documented); Ubuntu 22.04's Python 3.10 is too old |
| SynthPilot | Linux wheel exists; **Quartus-on-Linux not accepted by vendor** |

**Distribution packages are too old.** apt Verilator 5.020 and apt Yosys 0.33 (Ubuntu 24.04)
should not be used for this project.

---

## 13. Open-source / licence analysis

| Tool | Class | Licence | Implications |
|---|---|---|---|
| rtl-agent-team | Open source | MIT | No restrictions |
| systemverilog-lsp (babyworm) | Open source | MIT | — |
| FPGA-LSP | Open source | MIT | — |
| oh-my-fpga | Open source | MIT | Useless without SynthPilot |
| wmm246/fpga-mcp | Open source | MIT | — |
| weft-mcp | Open source | GPL-3.0-only | Fine as a separate tool; copyleft applies only if its code is modified and redistributed |
| GateFlow | **Source-available** | BSL-1.1 | Non-commercial/educational/evaluation OK; commercial use needs a licence until 2028-01-30 |
| abbbe/fpga-mcp-servers | **No licence** | All rights reserved | Do not copy or modify |
| SynthPilot | **Proprietary** | Commercial; Free/Pro/Max | Quartus builds/reports require **paid** Pro |
| Quartus Prime Lite | Proprietary | Free edition | No licence file needed for Lite |
| Questa Starter | Proprietary | Free, **licence file required** | Obtain from Altera licensing; set the licence variable |
| OSS CAD Suite components | Open source | Various (ISC, LGPL/Artistic, GPL, …) | Tools only; no effect on project RTL |
| cocotb / pyslang | Open source | BSD-3 / MIT | — |

---

## 14. Repository maturity

| Tool | Commits | Active period | Tags | Contributors | Own tests | Evidence class |
|---|---:|---|---|---|---|---|
| rtl-agent-team | 724 | 2026-02-25 → 08-24 | 15 (v0.14.6) | 1 main (several identities) | 1,718 unit — **E3** | Mature |
| GateFlow | 149 | 2026-01-29 → 05-21 | 13 (v2.5.3) | 1 (+1 external commit) | CLI/TUI only | Moderate; **stale 4 months** |
| weft-mcp | 85 | 2026-08-22 → 08-23 | 5 (v0.5.0) | 1 | 295 pass — **E3** | High quality, **short history** |
| abbbe/fpga-mcp-servers | 11 | 2026-01-21 → 01-27 | 0 | 1 | Mock-mode tests | LOW EVIDENCE |
| SynthPilot (public repo) | 9 | 2025-12-21 → 2026-08-17 | 2 | 1 | Closed source | N/A (proprietary) |
| systemverilog-lsp | 9 | → 2026-04-25 | pinned v1.1.4 | 1 | — | LOW EVIDENCE |
| wmm246/fpga-mcp | 7 | 2026-07-23 → 08-06 | 1 | 2 | **Broken from clone** | LOW EVIDENCE |
| oh-my-fpga | 3 | 2026-06-05 → 06-09 | 0 | 1 | Generator-audited (E1) | LOW EVIDENCE |
| FPGA-LSP | 2 | 2026-05-07 | 0 | 1 | CI smoke | LOW EVIDENCE — capability still useful |

---

## 15. Subtheme relevance

No evaluated AI tool is specialised for any subtheme. "Generic" means that a tool improves
verification quality for any RTL but has no domain knowledge of its own.

| Tool | 01 Secure Identity / SE | 02 Crypto Accelerator | 03 AI / Edge Accelerator |
|---|---|---|---|
| rtl-agent-team | Generic + `security-reviewer`, SVA for key-handling invariants | Generic + `ref-model-dev` (golden model) | Generic + `ref-model-dev`, perf-verifier |
| cocotb + Python models | Protocol/auth sequence tests | **Strong:** `hashlib` and test vectors, bit-exact | **Strong:** NumPy integer/fixed-point models |
| SymbiYosys | **Strong:** FSM safety, "key never leaves" properties | Round-counter, handshake, padding-FSM properties | Accumulator overflow/saturation properties |
| Verilator / Icarus / slang | Generic | Generic | Generic (Verilator speed helps long NN vectors) |
| Quartus + SignalTap | Generic; PUF work needs **placement control** (location/LogicLock), not covered by any AI tool | Generic; ALM/M10K results | Generic; DSP-block inference results |
| weft-mcp (later) | Generic | Generic | Generic |
| GateFlow (fallback) | Generic | Generic | Generic |
| TT07 references (§3) | RO-PUF | tiny sha256 | TinyTPU, mini-AIE CGRA |

Subtheme-specific gaps are listed in §19.

---

## 16. Tool overlap

- **rtl-agent-team vs GateFlow — direct overlap.** Both cover planning, codegen, testbench,
  debug, formal, lint/sim loops, and a Yosys-based "synthesis" that must be disabled by policy.
  Head-to-head:

| Criterion | rtl-agent-team | GateFlow |
|---|---|---|
| Maturity / activity | 724 commits, active to Aug 2026 | 149 commits, idle since May 2026 |
| Own test evidence | 1,718 unit tests, 1 env-caused failure | CLI tests only; 2 of 8 "verified" IP examples fail or give no verdict |
| Licence | MIT | BSL-1.1 |
| Verification enforcement | Stop-gates block unverified RTL edits | Reminder hooks only |
| Golden models / security review | Dedicated agents | Not dedicated |
| FPGA orientation | ASIC-oriented implementation phases (disabled by policy) | Open-source FPGA flows for non-Intel boards (disabled by policy) |
| Context cost | ~12.7k tokens/session | ~5.4k tokens/session |
| Integration effort | Higher (phases, state dir, interactive setup) | Low |
| Install verified | Yes | Yes |

  **Decision: rtl-agent-team is primary. GateFlow is a fallback only. Never enable both.**
  (This reverses the provisional GateFlow pick from the first audit pass.)

- **LSPs.** FPGA-LSP (Verible) and systemverilog-lsp (slang) overlap each other, and both are
  largely superseded by Verilator plus slang CLI checks. At most one would ever be enabled.
- **Quartus MCPs.** weft-mcp, SynthPilot, abbbe and wmm246 all overlap with Claude Code running
  Quartus through Bash. Only weft-mcp adds enough (sandboxing, compact JSON reports) to justify
  a later trial.
- **Linting.** Verilator and slang overlap intentionally: two front-ends reduce false confidence.
- **Simulation.** Verilator and Icarus overlap intentionally. Cross-simulator checks exposed the
  GateFlow testbench defect.

---

## 17. Recommended AI stack

```
                         Claude (Claude Code, repo CLAUDE.md = policy)
                                        │
        ┌───────────────────────────────┼─────────────────────────────────┐
        │                               │                                 │
 rtl-agent-team (phase skills,   Project scripts (Bash)            Human decisions
 human-gated): research, arch,   ─ lint:  verilator -Wall + slang  (subtheme, arch
 µarch, RTL, ref-model,          ─ sim:   cocotb on Verilator +    sign-off, waivers)
 test-plan, SVA, CDC, security,           Icarus (.venv)
 design notes                    ─ formal: SymbiYosys (+slang)
        │                        ─ impl:  quartus_sh --flow compile
        │                                 quartus_sta, report extraction
        │                        ─ debug: quartus_stp (SignalTap)
        │                        ─ board: quartus_pgm / HPS-side tests
        └─────────────┬──────────┘
                      ▼
      Evidence store: docs/evidence/ (raw .summary/.rpt, SignalTap captures,
      HPS logs) ─► the ONLY source for MEASURED numbers in the proposal
                      │
                      ▼
      (later, optional) weft-mcp for compact Quartus JSON once verified on Cyclone V
```

Design rationale:

1. **Quartus stays the ground truth and is driven by transparent, versioned scripts.** No
   intermediate server can misreport it, and every number traces to a file.
2. **Verification is layered and redundant:** two linters, two simulators, formal proofs, and
   golden models.
3. **The agent pipeline is used for thinking and verification discipline, not for
   implementation numbers.**
4. **Every new tool must earn its place** through an entry in this report.

---

## 18. Installation decisions

| Tool | Install? | Why | Risk | Priority |
|---|---|---|---|---|
| Quartus Prime Lite + Cyclone V device support | **INSTALL NOW** (manual) | Only valid source of synthesis, timing, resources, bitstream, SignalTap | ~14 GB+; version drift across team members | P0 |
| Questa-Altera Starter | **INSTALL NOW** (manual) | Vendor simulator, useful for Intel IP/primitives | Needs free licence file | P1 |
| OSS CAD Suite | **INSTALL NOW** | Verified Verilator/Icarus/Yosys+slang/sby/slang set; required for cocotb 2.1 | Nightly builds: pin via `OSS_CAD_SUITE_TAG` (recorded in the install log) | P0 |
| `.venv`: cocotb 2.1.0, pyslang 11.0.0, pytest 9.1.1 | **INSTALL NOW** | Golden-model testbenches; verified combination | Upgrades may break the Verilator pairing; pinned | P0 |
| rtl-agent-team (project scope) | **INSTALL NOW** | Mature, MIT, verification gates, ref-model/security/design-note agents | Context cost; ASIC phases must stay off (CLAUDE.md §5.3) | P1 |
| weft-mcp | **INSTALL LATER** | Structured Quartus JSON, sandboxed runs | Quartus 25.1 only; Cyclone V parsing unconfirmed; Podman | P2 |
| GateFlow | **OPTIONAL** | Lighter fallback agent | BSL; overlap; stale; broken examples | P3 |
| FPGA-LSP | **OPTIONAL** | Navigation, syntax on edit | Format-on-save rewrites; experimental LSP support | P3 |
| systemverilog-lsp (slang) | **OPTIONAL** | Semantic LSP | C++ source build; LOW EVIDENCE | P3 |
| SynthPilot | **DO NOT INSTALL** | Free tier can't build; Linux Quartus unaccepted; paid | Cost, lock-in | — |
| oh-my-fpga | **DO NOT INSTALL** | Vivado-only; requires SynthPilot | — | — |
| abbbe/fpga-mcp-servers | **DO NOT INSTALL** | No licence; hard-coded | Legal, fragility | — |
| wmm246/fpga-mcp | **DO NOT INSTALL** | Broken from source; arbitrary Tcl over TCP | Security, reliability | — |
| shroudpro/Quartus-MCP | **DO NOT INSTALL** | Quartus II 9.1 / MAX II | — | — |

### Installation procedure (INSTALL NOW items only)

Automated by `scripts/setup_tooling.sh` (no sudo, idempotent):

```bash
scripts/setup_tooling.sh check     # report only, changes nothing
scripts/setup_tooling.sh install   # OSS CAD Suite + .venv + rtl-agent-team, then verify
scripts/setup_tooling.sh verify    # versions, lint, cocotb x2, sby proof, Quartus smoke, plugin check
. scripts/env.sh                   # per shell: tools on PATH + .venv active
```

Manual steps, following official instructions:

1. **Quartus Prime Lite.** Download the Linux Quartus Prime Lite installer and the **Cyclone V
   device support** file into one directory, `chmod +x *.run`, and run the installer as a normal
   user. The whole team should use **the same version**. Then run
   `QUARTUS_BIN=/path/to/quartus/bin scripts/setup_tooling.sh verify`, which compiles a smoke
   design for `5CSEBA6U23I7` and logs the **verbatim** fit and STA summaries.
2. **Questa Starter** (optional). Install it from the same download page, request the free
   licence, and set the licence environment variable.
3. **Inside Claude Code:**
   - run `/reload-plugins`;
   - run `/rtl-agent-team:rat-setup`, answering **skip** for SystemC and for global rule
     deployment;
   - do **not** run `rat-init-project` until the subtheme is chosen.
4. **Board:** install the USB-Blaster II udev rules, then confirm `jtagconfig` lists the
   DE10-Nano.

### What was verified in the audit sandbox (Ubuntu 24.04.4, not the team's machines)

`scripts/setup_tooling.sh install` → **17 OK, 0 warnings, 1 failure** (Quartus absent, as
expected). It verified:
- tool versions;
- yosys-slang loading;
- the venv versions;
- clean Verilator and slang lint on the smoke DUT;
- cocotb smoke tests **passing on Verilator and Icarus**;
- a SymbiYosys **proof by k-induction**;
- Claude Code 2.1.280 **recognising `rtl-agent-team@rtl-agent-marketplace` v0.14.6 as enabled**
  at project scope.

The Quartus smoke compile is written but **has not been executed anywhere yet**. Its first real
result will appear in `docs/TOOLING_INSTALL_LOG.md` on a team machine.

Note: a project-level `extraKnownMarketplaces` entry did **not** register the marketplace on a
fresh Claude Code profile in testing. Each teammate therefore runs the install step, which adds
the marketplace explicitly.

---

## 19. Remaining capability gaps

1. **SignalTap automation.** No tool. Plan `.stp` files by hand; script captures via
   `quartus_stp`; store captures as evidence.
2. **HPS/FPGA integration.** No tool covers Platform Designer (`qsys-generate`), bridge
   selection, the HPS Linux image or device tree, or HPS-side drivers and benchmarks. This is
   needed for the proposal's HPS/FPGA interaction section and for any "hardware vs. software"
   comparison, which must be measured on the same HPS.
3. **DE10-Nano board knowledge.** Pins, clocks and reference design come from Terasic
   documentation only.
4. **Quartus report parsing for Cyclone V.** Resolved first by the verbatim smoke-test log, then
   optionally by weft-mcp.
5. **Timing closure on Quartus.** No agent is Quartus-aware. Use the oh-my-fpga-style
   methodology (CLAUDE.md) with `quartus_sta` reports.
6. **Power estimation** (Quartus Power Analyzer). Not covered by any tool.
7. **PUF-specific needs** (subtheme 01). No tool covers placement/routing control for identical
   ring oscillators, or uniqueness/reliability statistics across boards and temperatures. Custom
   scripts would be needed.
8. **Agent RTL quality on this project.** Not yet measured. Evaluate on the first real block.

---

## 20. Risks and limitations

- **Fabricated or mislabelled numbers.** Both candidate agents can emit Yosys/Liberty "area"
  figures. Mitigation: CLAUDE.md §5.1 and the ESTIMATE/MEASURED labelling rule.
- **Plugin supply chain.** Marketplace plugins run hooks (code) on the developer's machine and
  may auto-update.
  - Record the plugin version from the install log.
  - Review the changelog before updating.
  - Keep the plugin at project scope.
- **Context and cost.** rtl-agent-team lists about 12.7k tokens of descriptions per session, and
  multi-agent phases consume many tokens. Use phase skills selectively.
- **Workflow friction.** rtl-agent-team's Stop gates can block ending a session after RTL edits.
  This is intentional; waivers must be justified.
- **Tool version drift.** OSS CAD Suite is a nightly; Quartus versions differ across team
  members. Pin both and record them in the log.
- **Audit limitations:**
  - One sandbox OS only (Ubuntu 24.04).
  - No Quartus and no DE10-Nano available.
  - Stars and issues not collected uniformly (API rate limit).
  - slang-server LSP not built.
  - Agents not exercised on real project RTL.
  - One claim (the weft-mcp Cyclone V label) is explicitly unconfirmed.
- **BSL licence** if GateFlow is ever enabled in a commercial context.

---

## 21. Recommended next step

1. On each team machine:
   - install Quartus Prime Lite with Cyclone V support (same version for everyone);
   - run `scripts/setup_tooling.sh install`, then `verify`;
   - commit `docs/TOOLING_INSTALL_LOG.md` (not `scripts/tooling.env`, which holds machine-specific paths).
2. Confirm the Quartus smoke compile and read the real Cyclone V summary labels in the log. Use
   them to settle the weft-mcp question.
3. Start the next phase, **problem discovery → subtheme selection**, with an evidence-based
   comparison of the three subthemes. For each one, cover:
   - the named baselines (TT07 SHA-256, RO-PUF, TinyTPU, mini-AIE, iterative MAC);
   - DE10-Nano feasibility (ALM/M10K/DSP headroom, achievable clock);
   - how the result can be **measured on the board** against an HPS software baseline;
   - verification difficulty and differentiation.
   Record the decision in `docs/decisions/` before any RTL is written.

---

## 22. Evaluation: Graphify (code knowledge graph) and Obsidian (2026-10-01)

Requested by the team to reduce token usage (CLAUDE.md §6.5: evaluation entry before any addition). Status:
**evaluated; Graphify NOT adopted (proposal, team decides); Obsidian only as a viewer of `docs/`.**

*Graphify* — PyPI `graphifyy` 0.9.73, upstream <https://github.com/safishamsi/graphify> (MIT). Builds a graph of code by
tree-sitter AST (0 LLM tokens in the default mode), writes `graphify-out/{graph.json, graph.html, GRAPH_REPORT.md}`; the
popular setup guide <https://github.com/lucasrosati/claude-code-memory-setup> additionally installs a global `SessionEnd`
hook, a daily cron job, a git hook and edits `CLAUDE.md` — **none of that was installed**. Its "71.5x fewer tokens"
figure comes from one React/Supabase project of 126 TypeScript files (guide's own caveat); it is not evidence for this
repository.

*Trial (MEASURED unless marked; isolated venv and a copy of `rtl/ tb/ formal/ scripts/` outside the repo; no
`graphify install`, no hooks; `~/.claude` and the repository unchanged):*
- `graphify update` on 145 supported files (181 files copied; 35 not classified, e.g. all 28 `.sby`): 3 s, 761 nodes,
  1,508 edges, 62 communities, 0 tokens. `tree-sitter-verilog` is bundled; 72 `.sv` files were read, modules and
  `instantiates` edges were extracted (79 in total).
- **Gap 1 — instantiations inside `generate` blocks are missed.** `ntt_core_c4` shows instantiations of `pipe_delay`,
  `modmul_sel`, `poly_mem_multiport_pipe`, but not the lane `butterfly_c4` / `butterfly_c4_lazy` / `twiddle_rom`, which sit
  inside `if (...) begin : g_...` generate branches (`rtl/ntt/ntt_core_c4.sv` lines 214, 222, 232). So "what is under
  `ntt_core_c4c`?" gets an incomplete answer: `graphify path ntt_core_c4c modmul_barrett_lazy` finds no directed path.
- **Gap 2 — misleading undirected path.** With `--undirected` the 4-hop answer goes through the shared child
  `pipe_delay`, not through the real hierarchy.
- Not in the graph: ADRs, evidence, test plans (8 document nodes from 4 `.md` files); `docs/` is about 621 k characters
  and the code about 592 k characters (ESTIMATE ≈ 155 k and 148 k tokens at 4 characters per token). The knowledge this
  project re-reads most (decisions, evidence tables) is in `docs/`.
- Cost comparison (ESTIMATE, 4 characters per token): a local hierarchy question under `ntt_core_c4c` needs about 5
  files ≈ 24.7 k characters ≈ 6.2 k tokens by reading; `graphify explain` returns about 0.5 k characters but, per
  Gap 1, incomplete. `GRAPH_REPORT.md` is about 12 k characters ≈ 3 k tokens if read at the start of each session.
  `grep` already answers "who instantiates X" for a few hundred tokens.

*Assessment (INFERENCE):* the possible saving is small for this repository (≈ 150 k tokens of code in total, most
reasoning cost comes from long sessions and tool output, not from code exploration), and the one structural feature it
would help most — the module hierarchy — is wrong where this RTL uses `generate`. Adopting it would add a
dependency and, with the full guide, global hooks and a `CLAUDE.md` change on a public repository (C7), for an
uncertain saving. **Recommendation: do not adopt now;** revisit if the extractor handles `generate` or if the code
grows by an order of magnitude. Cheaper measures already in use: `HANDOFF.md`, memory notes, filtered tool output,
`grep` before reading, evidence files instead of logs.

*Obsidian* — a desktop Markdown editor; it does not reduce Claude Code tokens by itself. Allowed use: open `docs/` as
a vault for reading and linking; no plugins; `.obsidian/` is git-ignored (done in this change); no sync of private
notes into the public repository.

## References

Competition
- Hackathon site: https://summit.peruri.co.id/hackathon
- Proposal template: `template-proposal-hackathon-chip-2026.pdf` (provided by organisers)

Audited repositories
- GateFlow: https://github.com/codejunkie99/Gateflow-Plugin
- FPGA-LSP: https://github.com/nyavana/fpga-lsp
- SynthPilot: https://github.com/LNC0831/SynthPilot
- oh-my-fpga: https://github.com/LNC0831/oh-my-fpga
- rtl-agent-team: https://github.com/babyworm/rtl-agent-team
- systemverilog-lsp: https://github.com/babyworm/systemverilog-lsp
- weft-mcp: https://github.com/FPGArtktic/weft-mcp
- fpga-mcp-servers: https://github.com/abbbe/fpga-mcp-servers
- fpga-mcp: https://github.com/wmm246/fpga-mcp
- Quartus-MCP: https://github.com/shroudpro/Quartus-MCP

Toolchain
- OSS CAD Suite: https://github.com/YosysHQ/oss-cad-suite-build
- yosys-slang: https://github.com/povik/yosys-slang
- SymbiYosys: https://github.com/YosysHQ/sby
- Verible: https://github.com/chipsalliance/verible
- cocotb: https://github.com/cocotb/cocotb

Device and software
- Cyclone V device overview / product table: https://cdrdv2-public.intel.com/714207/cyclone-v-product-table.pdf
- Quartus Prime Lite 25.1 (Linux): https://www.altera.com/downloads/fpga-development-tools/quartus-prime-lite-edition-design-software-version-25-1-linux

Baselines
- Tiny Tapeout 7 chip map: https://tinytapeout.com/runs/tt07/
