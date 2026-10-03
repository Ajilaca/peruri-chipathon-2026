# CLAUDE.md — CHIP 2026 Hackathon · Team J5 (ITB) · ML-KEM-768 accelerator on DE10-Nano

Project-level instructions for Claude Code. They override plugin defaults.
Context and evidence live in `docs/`: read **`docs/PROJECT_BRIEF.md`** (why), **`docs/ROADMAP.md`**
(phases and done-criteria), **`docs/decisions/PENDING.md`** (open choices) when relevant.
Tooling rationale: `docs/AI_TOOLING_RESEARCH.md`. Install/verify history: `docs/TOOLING_INSTALL_LOG.md`.

## 0. Mission and hard constraints (read first, every session)

**Goal.** Design, verify and *measure* an ML-KEM-768 (NIST FIPS 203) accelerator with
hardware/software co-design on the DE10-Nano: Keccak-f[1600] and NTT/INTT in the fabric,
protocol flow and software baseline on the HPS, constant-time proven by cycle-count invariance.

| # | Constraint | Enforced by |
|---|---|---|
| C1 | **The mathematics is locked.** Never change q, n, k, eta, du, dv, the root of unity, or any FIPS 203 arithmetic. Innovation is architecture only. | `/mlkem-guard`, ADR 0002 |
| C2 | **No invented numbers.** Resource/timing/performance figures come only from Quartus reports or board runs in this repo; everything else is labelled `ESTIMATE`, a cited source `[n]`, or "perhitungan tim". | `/quartus-report`, `/proposal-claims` |
| C3 | **No overclaims.** Never write "quantum-proof"; never claim side-channel (power/EM) resistance, speed-up vs software, power savings, or "first" without evidence. Core claim = constant-time. | `/proposal-claims` |
| C4 | **Proposal limit: 6 pages** (cover and references not counted). Sections 1-2 = pages 1-3 (written); Section 3 = pages 4-6 (**not written; do not write it until asked**). | `docs/proposal/README.md` |
| C5 | **Do not decide for the team.** Open choices are in `docs/decisions/PENDING.md`; ask, then record with `/decision-record`. | `/decision-record` |
| C6 | **Human approval between phases**; verify before optimising. | `/phase-gate` |
| C7 | **The GitHub repository is public.** No secrets, no personal contact data (emails/phones), no large binaries. | `scripts/setup_github.sh`, `.claude/settings.json` |
| C8 | Prefer measurable objectives; label simulation-only results as such. Never claim hardware validation without evidence in `docs/evidence/`. | rules in §3 |

**Language.** Talk to the team in Indonesian. Code, identifiers and comments in English.
Proposal text in formal Indonesian (foreign terms in italics). State uncertainty plainly.

## 1. Project identity

| Item | Value |
|---|---|
| Competition | CHIP 2026 Hackathon (PERURI Digital Summit), category *IC Chip Design & FPGA Implementation* |
| Team | J5, Institut Teknologi Bandung (4 members) |
| Repository | https://github.com/Ajilaca/peruri-chipathon-2026 (public, MIT licence, ADR 0016) |
| Target board | Terasic DE10-Nano (no board attached at last check; see PENDING #8) |
| Device | Intel/Altera Cyclone V SE SoC **5CSEBA6U23I7** (FPGA fabric + dual Cortex-A9 HPS) |
| EDA (ground truth) | Intel Quartus Prime Lite **25.1std** (verified on the team machine 2026-09-24) + Questa Starter (licence variable not set) |
| HDL | SystemVerilog / Verilog |
| Open-source verification | OSS CAD Suite: Verilator, Icarus, Yosys + slang, SymbiYosys; cocotb + pyslang in `.venv` |
| Environment | `. scripts/env.sh` (tools on PATH, activates `.venv`) |

### Device capacity (datasheet vs. fitter)
Intel's Cyclone V overview gives the A6 device **41,910 ALMs, 166,036 registers, 5,570 Kb M10K,
621 Kb MLAB, 112 variable-precision DSP blocks (224 18x18 multipliers), 6 FPGA PLLs**. The
fitter's denominators can differ (e.g. block counts); **quote the fitter report's denominator**
when stating utilisation.

> The official template lists **415,000** flip-flops. That does not match Intel's documentation
> (166,036). Never copy the template figure.

Subthemes (official page): 01 Secure Identity & Security Element · 02 Hardware Cryptography
Accelerator · 03 AI/Edge Accelerator · 04 Secure Communication. The team chose the idea
(ADR 0001); **which subtheme to declare is still open** (PENDING #2).

## 2. Current phase
- Done: Phases 0–5 (`docs/results/result_phase0.md` .. `result_phase5.md`). Phase 4 final decision: ADR 0009
  (L = 8, P = 6, configuration C3-P6; NTT-core design budget 30% = 12,573 ALM). Phase 5 (`result_phase5.md`, Approval ticked by
  Jevan 2026-10-03): C4 = C4b-B (Barrett reducer, 119 / 375 cycles, 9,166–9,208 ALM, 18 DSP); 5c (C4c)
  measured and not adopted (ADR 0014); 5d not attempted; information compiles at 20 ns do not meet timing for C3-P6 or C4b-B;
  the critical path is the memory read (ADR 0010).
- Done: Phase 5M (`docs/results/result_phase5m.md`, Approval ticked by Jevan 2026-10-03): S6 = M6 base by team decision (ADR 0020; the rule did not adopt it), S7 split memory read **adopted by the rule** (ADR 0021, superseded by 0025: median Fmax 38.720 MHz,
  NTT = INTT = 120 cycles, 9,361-9,405 ALM, 16 DSP), S8 write-path register **not adopted** (ADR 0023, superseded by 0025: 37.990 MHz, 122 cycles), S9 M10K study (ADR 0022, superseded by 0025: a conflict-free 1R1W 16-bank map exists, no hardware number).
  Decided 2026-10-02 (Jevan, Team J5): ADR 0013 (Barrett), ADR 0015 (5d moves to Phase 6), ADR 0017 (Phase 5M), ADR 0019 (minimal path to full ML-KEM: skips Phase 6 and 8a/8c/8d; S7-S9 done by note 3). The configuration
  for later phases is S10 (ADR 0025 Accepted 2026-10-03, Jevan). Read `HANDOFF.md` first in a new session.
- Done: Phase 6 (`docs/results/result_phase6.md`, Approval ticked by Jevan 2026-10-03; ADR 0024 Accepted: Phase 6 now, S10 inside it): K-PKE arithmetic sequencer bit-exact (KeyGen 5,493 / Encrypt 6,810 / Decrypt 3,121 cycles,
  counts 6/0/9, 3/4/12, 3/1/3); **S10** (16 x 1R1W memory, no slot arbitration) adopted by its rule and **accepted as the NTT/INTT core** (ADR 0025 Accepted 2026-10-03, Jevan): median Fmax 44.320 MHz at 40 ns, 5,077 ALM, 118 cycles, timing met at 20 ns at 6/6 seeds
  (kernel-only).
- Done: Phase 7 (`docs/results/result_phase7.md`, Approval box empty): Keccak-f[1600] K0 (1 round/cycle, 24 busy cycles) and SHA3-256/512, SHAKE128/256 sponge bit-exact against hashlib on both simulators, formal K1-K5; Quartus (kernel-only, seed 1):
  3,572 ALM, 1,653 registers, 0 M10K, 0 DSP, timing met at 40 ns (Fmax 56.99 MHz) and at 20 ns (76.30 MHz); about 2,000 Keccak cycles per ML-KEM operation (perhitungan tim). Not tier T1 (samplers missing). Next per ADR 0019: samplers (Phase 8b),
  after the Phase 7 Approval; open: PENDING #25, #26.
- Do not start RTL for a block until its golden model exists and its phase is approved.
- Each phase ends with a validated result artifact (`docs/results/`); a human approves it before the next phase.
  Never tick the Approval box yourself.

## 3. Engineering rules (non-negotiable)
1. **Never fabricate** synthesis, timing, resource, simulation or hardware results. If a tool
   in this repository did not produce it, it does not exist yet.
2. **Separate estimates from measurements.** Label every quantitative claim `ESTIMATE`
   (method + assumptions) or `MEASURED` (path to the raw report/log).
3. **Ground-truth order:** DE10-Nano hardware > Quartus reports (fit/sta/asm) > RTL simulation
   and formal > analytical estimates.
4. **Never claim hardware validation** without SignalTap captures, on-board logs, HPS test
   output or a recorded demo under `docs/evidence/`.
5. **Verify RTL before optimising it.** No timing/area work on a block without a passing
   testbench against the golden model.
6. Objectives are measurable: ALM, registers, M10K, DSP, Fmax per clock domain, latency
   (cycles and ns), throughput, and versus an HPS software baseline measured on the same board.
7. **Define every clock domain** (source, frequency, relationship) in the spec and `.sdc`.
   Every crossing uses a documented synchroniser; no unexplained `set_false_path`.
8. **Define the reset strategy** (sync/async, polarity, domain per clock) before writing RTL.
9. Every RTL file starts with `` `default_nettype none `` and restores `` `default_nettype wire ``
   at the end.
10. Fitter and timing warnings are findings: critical warnings are triaged in writing, never
    silently waived.

### Borrowed verification principles
(adapted from the MIT-licensed oh-my-fpga skill pack; the pack itself is not used)
- **Verification-first:** never say "timing closed", "CDC clean" or "tests pass" without fresh
  tool output proving it.
- **Never fake-pass:** do not weaken an assertion, widen a tolerance, add a waiver or false
  path to turn a result green. Ask first and state the assumption.
- **Smallest safe change first:** constraints and parameters before RTL rewrites.
- **Surface trade-offs, then stop:** when safe options are exhausted, report options and costs
  and hand the decision back to the team.

## 4. ML-KEM domain rules (details and verified values in `/mlkem-guard`)
- N stays a power of two. The NTT is **incomplete**: 512 does not divide q-1, so 7 layers and a
  degree-1 binomial "pointwise" product, not 8 layers and scalar products.
- Constant-time means: no secret-dependent branch, address, loop count, division or modulo.
  It is **not** side-channel resistance and must not be described as such.
- Golden model first, independent of RTL; official KAT vectors only (do not invent vectors; do
  not mix old Kyber vectors with FIPS 203). Read NIST's FIPS 203 errata before locking vectors.
- Keep `tb/golden/params.py` constants exactly named for `check_params.py`.

## 5. Design priority
Technical feasibility -> measurable hardware improvement -> verification -> resource/timing
efficiency -> differentiation -> application/business relevance. The business case is scored but
supports the technical problem; it never overrides feasibility on the DE10-Nano.

## 6. Tools and skills

### 6.1 Project skills (in `.claude/skills/`, shared through Git)
| Skill | Use it when |
|---|---|
| `/quartus-report` | any resource/timing/Fmax number is needed; compile and extract MEASURED evidence |
| `/proposal-claims` | drafting or editing text for judges; before committing docs/README |
| `/mlkem-guard` | any NTT/Keccak/sampler/FO/KAT work; anyone proposes changing the maths |
| `/decision-record` | the team decides something, or a pending choice is noticed |
| `/phase-gate` | "is phase N done?", "what next?", before starting a new block; writes `docs/results/result_phase<N>.md` |

### 6.2 Quartus is the only source of FPGA implementation numbers
- Numbers come **only** from `quartus_sh --flow compile <rev>` and the `.fit.summary`,
  `.sta.summary`, `.flow.rpt`, `.sta.rpt` reports (use `/quartus-report`).
- **Yosys, Design Compiler or any agent-generated "LUT/area" figure is never reported as Cyclone V
  resource usage**, not even labelled as an estimate for Cyclone V. Yosys is for formal and
  elaboration checks only.
- Compiles are long: run in the background, log to a file, read the summaries; do not paste whole
  `.rpt` files into context.
- SignalTap: configure `.stp` deliberately, record the trigger, save captures to `docs/evidence/`
  (`quartus_stp` is the CLI).
- DE10-Nano pin assignments come from Terasic's documentation / GHRD. Never invent pin locations.

### 6.3 Verification stack
- Lint: `verilator --lint-only -Wall` **and** `slang`. Verible is style-only.
- Simulation: cocotb (`.venv`) on Verilator and Icarus; cross-check a failure on the second
  simulator before blaming the RTL.
- Golden models in Python (`hashlib` for SHA-3/SHAKE; integer models for arithmetic); tests compare
  bit-exact.
- Formal: SymbiYosys (`sby`) for per-module properties (FSM safety, handshakes, overflow).
- Enumerate corner cases in the test plan before writing tests.

### 6.4 Plugin `rtl-agent-team` (primary agent pipeline)
- Declared in `.claude/settings.json` (marketplace + enabled plugin, project scope), so a teammate
  can install it after trusting the folder; check with `claude plugin list` (0.14.6 verified here).
- Use phase skills **individually with human approval between phases**; never run
  `/rtl-agent-team:rat-auto-design` end to end.
- **Its verification Stop-gates are dormant until a `.rat/` directory exists**, which
  `/rtl-agent-team:rat-init-project` creates (`docs/AI_TOOLING_RESEARCH.md` §9.1). Running it is a
  team decision (PENDING #13); do not run it unasked. Until then, the verify-before-claim rule
  is enforced by these instructions and by `/phase-gate`, not by hooks.
- ASIC steps (Design Compiler/Liberty PPA, DFT, silicon validation) are out of scope; their
  area/timing numbers are not FPGA results (§6.2). Its `synthesis-reviewer` may read **Quartus**
  reports. Once gates are active, waivers need a written reason in the commit message.
- During `/rtl-agent-team:rat-setup`: skip SystemC and skip global rule deployment.

### 6.5 Not part of this environment
- GateFlow: optional fallback only; never enable together with rtl-agent-team.
- SynthPilot / oh-my-fpga: not installed. weft-mcp: candidate for later. FPGA-LSP: optional (it
  reformats files in place; not without team agreement).
- Add no plugin, MCP server or skill pack without an evaluation entry in
  `docs/AI_TOOLING_RESEARCH.md`.

## 7. Repository layout and Git rules

```
rtl/          synthesizable SystemVerilog (one module per file)
tb/           cocotb tests + Python golden models (tb/golden/params.py = locked constants)
formal/       .sby files and property modules
quartus/      .qpf/.qsf/.sdc, Platform Designer files, build scripts
sw/hps/       HPS-side (ARM Linux) drivers, tests, benchmarks
docs/         PROJECT_BRIEF, ROADMAP, decisions/, evidence/, proposal/, tooling docs
scripts/      env.sh, setup_tooling.sh, setup_github.sh, smoke tests
.claude/      settings.json (shared), skills/ (shared); settings.local.json is personal, git-ignored
```

- Work on branches named `phase<N>-<topic>`; merge to `main` by pull request. **Never force-push;
  never rewrite pushed history.** Do not push, open issues or PRs unless asked (settings ask first).
- Commit messages: short imperative subject; when a commit adds a number, name the evidence file.
- Never commit: `.venv/`, Quartus `output_files/`, `db/`, secrets, emails/phone numbers, files over
  5 MB. Final bitstreams (`.sof`/`.rbf`) go under `release/` on purpose and only when measured.
- `scripts/setup_github.sh check` (read-only) scans for these problems before a commit.

## 8. Proposal traceability
The proposal needs: executive summary, problem statement, architecture + RTL module list, resource
estimates (labelled ESTIMATE until Quartus measures them), test plan (RTL sim, corner cases,
timing/latency, synthesis, bitstream, SignalTap, on-board real-time), measurable success
metrics, references, repository link and technical documentation. Every number must trace to
`docs/proposal/references.md`, `docs/proposal/CLAIMS_REGISTER.md`, or a file under `docs/evidence/`.
