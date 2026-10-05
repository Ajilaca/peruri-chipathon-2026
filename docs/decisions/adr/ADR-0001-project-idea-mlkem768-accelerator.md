# ADR 0001: Project idea - ML-KEM-768 accelerator (HW/SW co-design) on DE10-Nano

- Status: Accepted
- Date: 2026-09-28
- Decided by: team J5 (basis: the team's proposal draft, title and Sections 1-2 as written by the team)

## Context
Earlier screening compared many ideas across the four official subthemes. The team's proposal
draft names "Akselerasi ML-KEM pada Hardware FPGA: Prototipe Kriptografi Pasca-Kuantum untuk
Perlindungan Data" and describes ML-KEM-768 with Keccak-f[1600] and NTT/INTT in the fabric.

## Decision
Build an ML-KEM-768 accelerator (HW/SW co-design) on the DE10-Nano. HPS: protocol flow,
baseline, timing. Fabric: NTT/INTT+pointwise, Keccak, sampler, compress/encode, control.

## Consequences
- Roadmap: `docs/ROADMAP.md`. Locked parameters and rules: `/mlkem-guard`.
- The *declared* competition subtheme is a separate open decision (see PENDING.md).
- Other screened ideas are not pursued unless a new ADR reopens them.

## Evidence
`docs/PROJECT_BRIEF.md`; `docs/proposal/references.md`.
