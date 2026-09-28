# Roadmap — ML-KEM-768 accelerator on DE10-Nano

**Status line (update only from verified evidence):**
Phase 0 golden model + KAT: technically DONE, human approval pending (see
`docs/results/result_phase0.md`: 80/80 ML-KEM-768 ACVP sample-vector cases passed, 2000/2000
matched an independent oracle (kyber-py); ML-KEM-512/1024 untested; model is not constant-time)
· tooling verified (Quartus 25.1std smoke compile MEASURED, see `docs/TOOLING_INSTALL_LOG.md`)
· no DE10-Nano attached at last check (`jtagconfig` empty, 2026-09-24) · competition schedule
unknown.

Gate rules: Phases 0-5 are mandatory and sequential. Phase 6 only after Phase 5 is verified.
Human approval between phases. Evidence lives in `docs/evidence/`. Skill: `/phase-gate`.
**Every phase ends with a result artifact** `docs/results/result_phase<N>.md` (template
`docs/results/TEMPLATE_result_phase.md`), validated by `check_result.py`; a human ticks its Approval box
before the next phase starts. Prompts for the current phase: `docs/prompts/phase0.md`.

## Phase 0 — Foundations
- **Work:** read FIPS 203 and the NIST errata list; write the Python golden model (`tb/golden/`, constants in
  `params.py`); run the official NIST ACVP vectors; cross-check against one independent implementation.
  Step-by-step prompts: `docs/prompts/phase0.md`.
- **Done when:**
  1. `check_params.py` passes (locked parameters), and k/eta/du/dv are confirmed against the FIPS 203 parameter table.
  2. Golden model reproduces the official ML-KEM-768 vectors (NIST ACVP, pinned commit in
     `.claude/skills/mlkem-guard/reference/kat_sources.md`; these are NIST **sample** sets, 25 cases per group;
     raw output in `docs/evidence/golden/`).
  3. Errata findings recorded (evidence file + ADR).
  4. Independent cross-check log on random inputs in `docs/evidence/golden/` (oracle: kyber-py in a throwaway venv).
  5. `docs/results/result_phase0.md` passes `check_result.py`, and a human has approved it.
- **Proposal use:** references, specification, corner-case list.

## Phase 1 — NTT / INTT + pointwise multiplication
- **Work:** `rtl/`: 7-layer incomplete NTT, INTT, binomial pointwise product, modular
  reduction; DSP 18x18 mapping; polynomial RAM in M10K.
- **Done when:**
  1. cocotb bit-exact vs golden on random + edge inputs, on Verilator **and** Icarus.
  2. `verilator --lint-only -Wall` and `slang` clean.
  3. Constant cycle count across inputs (evidence).
  4. Quartus compile of the block; MEASURED evidence file (ALM, registers, M10K, DSP, slack, Fmax).

## Phase 2 — Keccak-f[1600] + SHA3 / SHAKE
- **Done when:** matches `hashlib` (SHA3-256/512, SHAKE128/256) for random and boundary
  lengths (empty, rate boundaries); lint/slang clean; MEASURED evidence file.

## Phase 3 — Integration (HPS + fabric)
- **Work:** Platform Designer system, HPS-FPGA bridge, HPS driver, sampler, compress/encode,
  FO comparison; full KeyGen / Encaps / Decaps.
- **Done when:** full operations match golden KATs (in simulation; on the board if one is
  available; each labelled accordingly); transfer mechanism chosen by measurement (ADR).

## Phase 4 — Protocol demonstration
- **Blocked by decisions:** card-side vs reader-side target; concrete emulated message flow.
- **Done when:** handshake demonstrated end to end; logs and SignalTap captures stored
  (board required; without one, mark simulation only).

## Phase 5 — Measurement
- **Done when:** MEASURED cycles and time for KeyGen/Encaps/Decaps; ALM/registers/M10K/DSP/Fmax;
  cycle-count invariance; software baseline on the same board (and a second baseline if the
  team decides); transfer overhead separated; `docs/proposal/CLAIMS_REGISTER.md` updated.

## Phase 6 — Advanced (optional)
TVLA with the oscilloscope, masking/shuffling, fault detection inside the datapath,
ML-KEM-512/1024 parameterisation, hybrid ECDH + ML-KEM at the HPS. Each item needs its own
ADR and evidence; no claim before then.

## Proposal pages (cover and references not counted; limit 6 pages)
- Pages 1-3: Sections 1-2 (written).
- Pages 4-6: Section 3 "Proposed Chip Design" (block diagram, RTL module list, resource
  table, tools, test plan, success metrics). **Not written yet.** Resource cells stay
  `ESTIMATE` or `[...]` until Phase 1-2 evidence exists.
- Template error to avoid: it lists 415,000 flip-flops, while Intel's table says 166,036.
