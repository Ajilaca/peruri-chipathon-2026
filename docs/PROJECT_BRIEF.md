# Project brief — ML-KEM-768 accelerator (Team J5, ITB)

Read this when you need the *why* behind a rule in `CLAUDE.md`. The proposal itself is in
Indonesian and lives outside the repository (submitted PDF/Word); its text is summarised here.

## Goal (one sentence)
Design, verify and measure a **hardware/software co-designed accelerator for ML-KEM-768
(NIST FIPS 203)** on the Terasic DE10-Nano (Cyclone V SoC 5CSEBA6U23I7): Keccak-f[1600]
and NTT/INTT in the FPGA fabric, protocol flow and the software baseline on the HPS
(dual Cortex-A9), with **constant-time** behaviour proven by cycle-count invariance.

## Why (problem statement, sourced in `docs/proposal/references.md`)
- Large quantum computers would break RSA/ECDSA/ECDH (Shor). NIST IR 8547 (still a draft)
  proposes *deprecated after 2030*, *disallowed after 2035* [1][2]. "Harvest now, decrypt
  later" makes it relevant today [3]. No such computer exists yet [4]; resource estimates
  for RSA-2048 fell from ~20M to <1M noisy qubits [5].
- Identity documents are exposed: ICAO Doc 9303 eMRTD security relies on DH/ECDH [6][7];
  ICAO is specifying PQC for it [8]. Indonesian e-passports last 5 or 10 years [9], so a
  10-year passport issued in 2026 outlives the 2035 line (team calculation).
- ML-KEM is standardised (FIPS 203, 13 Aug 2024) [10] but heavy for constrained chips:
  eMRTD chips have 8-12 KB RAM and 12-32-bit CPUs; a post-quantum PAKE (OCAKE) with
  ML-KEM-768 takes ~1.39 s on a 20 MHz STM32 [11]. Software implementations also leak
  through timing (KyberSlash) [13].

## Solution and design principles
1. **Standard conformance**: FIPS 203 parameters unchanged; verified by known-answer tests.
2. **Constant-time**: fixed data path and cycle count independent of secrets.
3. **Resource efficiency as a design goal**, measured from Quartus reports only.
4. **Side-channel (power/EM) resistance is NOT claimed at core stage**; TVLA with the
   team's oscilloscope and masking/shuffling are a later stage.

Architecture: HPS runs the protocol flow (emulated PACE-style key exchange between
"document" and "reader"), key/buffer management, software baseline, timing. Fabric holds
control registers, Keccak-f[1600] (iterative), sampler (CBD + rejection), NTT/INTT +
pointwise (DSP 18x18, coefficients 12 bit), polynomial RAM (M10K), compress/encode and the
constant-time FO comparison. Interface: HPS-FPGA bridge, memory-mapped (Avalon-MM/AXI)
via Platform Designer; the transfer mechanism (DMA or not) is decided by measurement.

## Scope
| Core (required) | Later stage (optional) | Out of scope |
|---|---|---|
| NTT/INTT + pointwise; Keccak-f[1600]; sampler; compress/encode; HPS-FPGA integration; KAT verification; Quartus + board measurement | TVLA with oscilloscope; masking/shuffling; ML-KEM-512/1024 parameterisation; hybrid ECDH+ML-KEM; ML-DSA sharing the NTT | PKI and certification; validated hardware TRNG; ASIC tape-out; signature schemes (ML-DSA, SLH-DSA, LMS); physical anti-tamper |

## Novelty positioning (deliberately modest)
ML-KEM/Kyber accelerators are an active field, including an NTT on Intel Cyclone V
(Fmax 237 MHz, synthesis) [24], compact full designs [25] and industrial cores [26].
We do **not** claim algorithmic novelty. We claim: (1) evaluation on a PACE-style identity
key-exchange flow with protocol-level latency; (2) joint Keccak+NTT acceleration with
system measurements on an Intel SoC-FPGA board (initial search found none; search is not
exhaustive); (3) reproducible verification of constant-time behaviour.

## Business case (qualitative only)
Demand is driven by deadlines (NIST 2030/2035, NSA 2027 [16], BSI hybrid requirement [17])
and national programmes (Sandbox Chip Merah Putih at Peruri [18]; ITB-PERURI e-passport
secure IC pending certification [19][20]; PQC roadmap coordination [21]). Users: secure-IC
and secure-element developers for digital identity, reader/terminal makers, long-lived
embedded devices. Possible model: IP-core licence plus verification kit. **No market size
is claimed.** Priority order stays: feasibility, measurable improvement, verification,
efficiency, differentiation, business relevance.

## Known risks (honest list)
- The HPS Cortex-A9 is far stronger than the 20 MHz MCU in the literature, and bridge
  overhead can erase gains: a speed-up over HPS software may be small or negative. The
  value case rests on constant-time, offload for constrained hosts, and measured evidence.
- DE10-Nano cannot reproduce a card chip's 8-12 KB RAM; results are prototype-level.
- Prior art is dense; novelty is engineering/evaluation, not algorithmic.
- FIPS 203 has a pending NIST correction note (17 Nov 2025); read the errata before
  locking vectors.
- ML-KEM uses SHA-3/Keccak, not SHA-256, so the organisers' TT07 SHA-256 baseline is not
  directly reused (relevant to the declared subtheme).
- Board availability unknown; without a DE10-Nano only simulation and Quartus results exist.

## Open decisions
See `docs/decisions/PENDING.md`.
