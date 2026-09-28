<!-- claim-lint: skip-file (internal register: lists sources and claims to check) -->
# Claims register (Sections 1-2 as submitted 2026-09-28)

Type: **S** = cited source · **T** = team arithmetic · **L** = literature value about another
platform (context, not our result) · **M?** = must become MEASURED by our own runs.
Update the status column only from evidence.

## A. Claims resting on sources

| # | Claim in the proposal | Ref | Type | Note |
|---|---|---|---|---|
| 1 | RSA/ECDSA/ECDH broken by Shor; NIST proposes deprecated after 2030 and disallowed after 2035 | [1][2] | S | IR 8547 is still a **draft**; say "proposes" |
| 2 | "Harvest Now, Decrypt Later" | [3] | S | |
| 3 | No cryptographically relevant quantum computer exists | [4] | S | |
| 4 | RSA-2048 estimate fell from ~20 M to < 1 M noisy qubits | [5] | S | The 2019 figure is quoted by the 2025 paper |
| 5 | eMRTD (ICAO Doc 9303) security uses DH/ECDH; ICAO is specifying PQC | [6][7][8] | S | |
| 6 | Indonesian e-passports last 5 or 10 years | [9] | S | |
| 7 | A 10-year passport issued in 2026 is valid to 2036, past 2035 | | T | Arithmetic |
| 8 | FIPS 203 published 13 Aug 2024; NIST page notes a pending correction (17 Nov 2025) | [10] | S | Read the errata |
| 9 | eMRTD chips: RAM 8-12 KB, CPU 12-32 bit | [11] | S | |
| 10 | OCAKE on STM32 20 MHz: 0.98 / 1.39 / 1.92 s (ML-KEM-512/768/1024) | [11] | L | Motivation only; **not** our platform |
| 11 | NXP study: hardware accelerators can help | [12] | S | |
| 12 | KyberSlash exploits timing variation | [13] | S | |
| 13 | > 50 % of software cycles are in Keccak; then the critical path moves to NTT | [14][15] | S | |
| 14 | NSA: quantum-resistant acquisitions from 2027; BSI requires hybrid | [16][17] | S | |
| 15 | Sandbox Chip Merah Putih; ITB-PERURI e-passport IC awaiting certification; PQC roadmap meeting | [18]-[21] | S | News sources |
| 16 | Cyclone V 5CSEBA6U23I7: 41,910 ALM, 5,570 Kb M10K, 112 DSP; DSP block modes | [22][23] | S | Use the **fitter's** denominators when measuring |
| 17 | Prior art: Kyber NTT on Cyclone V (237 MHz, synthesis); compact full design; industrial core | [24][25][26] | S/L | Basis for the modest novelty claim |
| 18 | X^256+1 splits only into 128 quadratic factors: 7-layer "incomplete" NTT | [30][31] | S | Design constraint |

## B. Team arithmetic
- One polynomial = 256 x 12 bit = 3,072 bit.
- ML-KEM-768 sizes ek 1184 / dk 2400 / ct 1088 bytes follow from k=3, du=10, dv=4 (source in
  `references.md` [27], currently not cited in the text).

## C. Claims that must become MEASURED before they may be stated as results
| Item | Evidence needed | Status |
|---|---|---|
| ALM, registers, M10K, DSP, Fmax per block and for the full design | `docs/evidence/quartus/*.md` | not measured |
| Cycles / µs for KeyGen, Encaps, Decaps | testbench + board logs in `docs/evidence/` | not measured |
| Constant cycle count across inputs (incl. failing-ciphertext path) | test log in `docs/evidence/` | not measured |
| Speed-up vs software on the same board | baseline + accelerator runs | not measured (may be small or negative) |
| Bit-exact match with official KATs | `docs/evidence/golden/` | MEASURED: golden model passed 80/80 ML-KEM-768 cases from NIST's pinned ACVP-Server sample vector set (commit `975de31eb...b892`), and matched an independent implementation (kyber-py) on 2000/2000 random trials. ML-KEM-512/1024 not tested; not exhaustive coverage; see `docs/results/result_phase0.md` |
| Anything about power/EM leakage | TVLA data | later stage; **no claim** |

## D. Reference hygiene (found 2026-09-28)
- **[27] [28] [29] are in the reference list but are not cited** in the text of Sections 1-2
  (left over from an earlier, longer Background). Either cite them in Section 3 (sizes;
  power-analysis attack; Adams Bridge leakage) or remove them and renumber deliberately.
- Reference [15] points to a mirror of a NIST PQC-forum attachment; consider a cleaner source.
