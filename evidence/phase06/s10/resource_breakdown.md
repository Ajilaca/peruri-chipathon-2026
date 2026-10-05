<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# S10 vs S7: where the ALM went (MEASURED, Quartus "Fitter Resource Utilization by Entity", seed 1, 40.000 ns)

Source panels: `quartus/phase05m_memsched/output_files_S7/S7.fit.rpt` and `quartus/phase06_sched/output_files_S10/S10.fit.rpt` (not committed: `output_files*` is git-ignored; the totals are in
`evidence/phase05m/s7/quartus_S7.md` and `evidence/phase06/s10/quartus_S10.md`). Values copied from the reports; differences are INFERENCE.

| Entity | S7 ALMs needed | S10 ALMs needed | S7 registers | S10 registers | S7 block memory bits / M10K | S10 block memory bits / M10K |
|---|---:|---:|---:|---:|---:|---:|
| whole core (`ntt_core_s7_p7` / `ntt_core_s10_p5`) | 9,394.0 | 5,091.0 | 4,317 | 545 | 30,423 / 31 | 4,069 / 24 |
| memory (`poly_mem_multiport_split` / `poly_mem_m10k`) | **7,647.3** | **3,343.4** | 4,018 | 266 | 29,817 / 25 | 3,152 / 17 |
| everything else (butterflies, twiddle ROMs, FSM, delay lines) = core - memory | 1,726.2 | 1,727.1 | 299 | 279 | - | - |

Reading (INFERENCE):
- The whole saving (about 4,300 ALM) is in the memory; the rest of the core is the same size (1,726 vs 1,727 ALM). No function was removed: same schedule, same arithmetic, bit-exact, 118 cycles.
- Removed by S10: (1) the 256 x 12-bit storage in flip-flops with its per-word write decode and 32-word read multiplexers (S7 memory registers 4,018, S10 266; the 3,072 storage bits now sit in 16 RAM blocks of 192
  bits, one per bank, listed as `altsyncram ... g_bank[n].mem` with 192 block memory bits each); (2) the 16-port slot-arbitration ripple and its cut registers (the measured critical path of S7); (3) the 16 bank-map
  ROMs that Quartus had placed in M10K (S7: `bank_map_rom:g_map[0..15]`, 1,280-2,048 bits and 1-2 M10K each), replaced by an XOR of four address bits.
- What remains in the S10 memory (3,343 ALM): the 16-way selects (read offset per bank, write offset / data / enable per bank, read data per port) and the overflow check. The S9 study's upper bound for the
  crossbars (about 1,920 ALM, ESTIMATE by LUT counting) was **too low**: the measured memory entity is 3,343 ALM. The estimate covered the two data crossbars only, not the address selects and the overflow
  logic; recorded here as an estimate error, not changed in the study.
