# Open decisions (team to decide; Claude must not assume an answer)

Update this list whenever something is decided (move it to an ADR) or discovered.

| # | Question | Why it matters | Blocks |
|---|---|---|---|
| 1 | **Target side**: accelerator for the *card / secure element* or the *reader*? | Sources place the bottleneck on the card chip (8-12 KB RAM); the DE10-Nano's HPS is far stronger than a card chip. Changes Sections 1-3 wording and the demo. | Phase 4; proposal Section 3 |
| 2 | **Declared subtheme** (02 Hardware Crypto Accelerator? 01 Secure Identity? other) and how to relate to the reference baselines | ML-KEM uses SHA-3/Keccak, not SHA-256, so the TT07 SHA-256 baseline is not reused directly; subtheme 02 stresses small, area-efficient blocks | Registration text |
| 3 | **Transfer mechanism**: DMA or plain memory-mapped access | A polynomial is only 3,072 bits; DMA setup may cost more than it saves | Phase 3 (decide by measurement) |
| 4 | **Randomness source** for prototype: HPS or an FPGA TRNG | TRNG needs its own statistical validation; currently out of scope | Phase 3 |
| 5 | **Hybrid mode** (classical ECDH + ML-KEM at the HPS): include? | BSI requires hybrid for production; adds scope | Phase 6 |
| 6 | **Second software baseline** (e.g. soft core in fabric at a low clock) | Cortex-A9 baseline may show little or negative speed-up | Phase 5 |
| 7 | **Emulated protocol / message flow** ("PQ-PACE" is not a standard; ICAO is still specifying) | Needed to define latency at protocol level | Phase 4 |
| 8 | **Board availability**: is a DE10-Nano provided or owned? (`jtagconfig` showed none on 2026-09-24; an older Cyclone III board is not a target: no HPS, Quartus II 13.1 only) | Without a board only simulation + Quartus evidence exist | Phases 3-5 |
| 9 | **FIPS 203 errata**: content of NIST's list (planning note 17 Nov 2025) not yet read | May change test vectors | Phase 0 |
| 10 | **Prior-art search** extension (IEEE Xplore, IACR ePrint, Google Patents) | Needed before any novelty wording beyond the current scoped claim | Before submission |
| 11 | **Repository licence** (repo is public; without one, default copyright applies) | Affects reuse and the demo repository link | Before publishing code |
| 12 | Does the **Appendix** count toward the 6-page limit? | Decides where figures go | Section 3 layout |
| 13 | **Activate `rtl-agent-team` hooks** by running `/rtl-agent-team:rat-init-project` (creates `.rat/`)? The original blocker ("idea not chosen") is resolved by ADR 0001 | Its Stop-gates block ending a session after unverified RTL edits, which mechanically enforces verify-before-claim; but it also adds structure to the repo | Before Phase 1 |
