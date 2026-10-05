<!-- claim-lint: skip-file (internal plan, not proposal text) -->
# Phase 9: full ML-KEM-768 in RTL (simulation) - plan of the blocks

Written 2026-10-03, before any Phase 9 RTL and before any Phase 9 measurement. Scope: `docs/ROADMAP.md` Phase 9; ADR 0019 (path and tiers), ADR 0027-0030 (Accepted: C5 sponge, W2 sampler, STREAM, OVERLAP), ADR 0031 (Accepted: FIPS 203 input checks on the HPS, not in the RTL), ADR 0032 (Accepted: one STOP per block). Labels: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED, perhitungan tim. The mathematics is locked (C1).

## 1. What exists and what is missing
Exists (all bit-exact, simulation and Quartus MEASURED in Phases 6-8): the NTT/INTT core S10, the K-PKE operation sequencer `kpke_sched_smp` (VAR = 2, OVERLAP) with the slot store, the PWM unit and the streaming samplers, and the sponge (C5). The sequencer takes the seeds `rho` and `sd` through a seed port and moves coefficients through a host port (`tb_we_i`, `tb_slot_i`, `tb_addr_i`, `tb_wdata_i`, `tb_rdata_o`, one 12-bit coefficient per cycle, while the sequencer is idle). The inputs of a program are written into slots and the results are read from slots through that port; hashing of keys and byte encoding are not in hardware (Phase 8 header).
Missing for ML-KEM (FIPS 203 Algorithms 16-18): (1) ByteEncode / ByteDecode and Compress / Decompress between bytes and coefficients; (2) the hashes G (SHA3-512), H (SHA3-256), J (SHAKE256) on assembled messages; (3) the FO pieces of Decaps: re-encryption, constant-time comparison, selection of K or the implicit-rejection key; (4) the controller that orders all of it, with byte buffers for ek, dk, c.
Not in the RTL by ADR 0031: the FIPS 203 input checks (Sections 7.2 and 7.3). The core assumes checked inputs.

## 2. Blocks (one STOP after each, ADR 0032; the split is the assistant's proposal)
| Block | Content | Done when |
|---|---|---|
| **9a** | `mlkem_pack` (coefficients -> Compress_d -> ByteEncode_d bytes) and `mlkem_unpack` (bytes -> ByteDecode_d -> Decompress_d coefficients) for d in {1, 4, 10, 12}; division-free Compress (constants proved on all 3,329 inputs) | bit-exact against `primitives` for every d, exhaustively for the arithmetic, both simulators, controls fail, formal, Quartus kernel-only |
| **9b** | Hash and FO pieces: a message feeder for G, H and J on top of the sponge (words from a byte buffer, constant prefix words), `mlkem_fo_cmp` (constant-time 1,088-byte comparison and mask select of K / K_bar) | each bit-exact against `hashlib` / golden, fixed cycles, both simulators, controls fail, formal, Quartus |
| **9c** | `mlkem_core` controller: KeyGen_internal, Encaps_internal, Decaps_internal on byte buffers, the K-PKE engine as a black box; all pinned ACVP groups; constant-cycle evidence for Decaps; Quartus full core | ACVP keyGen (25), encapsulation (25), decapsulation (10) 100% on both simulators; constant cycles; Quartus; the key-check groups are not run against the RTL (ADR 0031) |

## 3. Architecture decisions inside the plan (INFERENCE from the existing interfaces, to be shown by the tests)
- The K-PKE engine and its tb port stay untouched (frozen Phase 6-8 files). The controller moves coefficients between the codec and the slots through the host port while the engine is idle; at one coefficient per cycle this costs 256 cycles per polynomial (ESTIMATE, from the port width), small against the engine's thousands of cycles. No change to the engine.
- Every loop of the codec and of the controller has a fixed length: 256 coefficients and 32 * d bytes per polynomial, fixed message and ciphertext lengths. No branch, address or count depends on a secret; the only variable length is the rejection sampling of A (public rho / ek).
- The sponge for G, H, J is a second instance (the sampler has its own inside `keccak_sampler`). Its core (C5 or K0) is a parameter; C5 is the default (ADR 0027); K0 is smaller and the hashing time is not critical; the measured area decides whether to keep the default (reported, not decided here).
- Randomness enters as input ports (`d`, `z`, `m`) as the roadmap says; no RNG in the RTL.

## 4. Costs (ESTIMATE, perhitungan tim; replaced by Quartus numbers when measured)
The device has 41,910 ALM (datasheet) and the 8d engine measured 10,993 ALM, 44 M10K, 26 DSP (kernel-only, median of seeds 1-6). The ek / dk / c buffers need 1,184 + 2,400 + 1,088 bytes = 4,672 bytes = 37,376 bits, about 4 M10K blocks of 10 Kb at best (more with width and port rounding). The codec and the controller are small FSMs and byte registers; no estimate of their ALM is made here; they are measured.

## 5. Common rules for every block (as in Phases 5-8)
- A test plan with the adoption or pass rule is written before the RTL of its block; changes after the first runs are recorded as Amendments, the rule is not changed after measuring.
- Verilator `-Wall` and slang lint 0 warnings; cocotb on Verilator and Icarus; negative controls on test-only copies; SymbiYosys for control properties; Quartus 25.1std Lite kernel-only, virtual pins, seeds 1-6, one revision at a time, timing at 40.000 ns (20.000 ns information).
- Each RTL file starts with `` `default_nettype none `` and ends with `` `default_nettype wire ``; reset strategy: asynchronous active-low on control state, none on datapath registers (as Phases 6-8), stated in each file.
- Simulation results are labelled simulation only. No claim about the board (no DE10-Nano), no speed-up claim against software, no side-channel claim: constant-time means cycle-count invariance only.

## 6. Amendment A1 (2026-10-03, written at the start of 9b; nothing above is edited)
The plan of 9b in section 2 spoke of "a message feeder (words from a byte buffer, constant prefix words)". Reading the sponge interface (`rtl/keccak/keccak_sponge_r2.sv`: 64-bit words, byte k of word w is message byte 8w + k, the length in bytes is given at start) shows that no byte feeder is needed: every message segment of Algorithms 16-18 is a multiple of 8 bytes (d, z, m, h, K: 32 bytes; ek: 1,184; c: 1,088) and starts on a word boundary when the segments are concatenated; the only exception is `d || k` (G(d || 3), 33 bytes), whose last word is `0x03` and is supplied by the controller. 9b therefore builds `mlkem_hash` (a wrapper of the sponge with the three modes H, G, J, digest counting and the stop of the SHAKE256 squeeze) and `mlkem_fo_cmp` (constant-time compare of two 136-word ciphertexts and the mask selection of K or the implicit-rejection key), both with 64-bit word interfaces. The byte buffers, the segment order and the assembly of messages are the controller's work in 9c.
