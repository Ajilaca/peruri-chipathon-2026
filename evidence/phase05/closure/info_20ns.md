<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Phase 5 closure: information compiles at 20.000 ns (ADR 0011 D1, ADR 0010)

Not a Phase 5 gate: 50 MHz is a best-effort target (ADR 0010). One compile per configuration, default seed 1, Quartus
defaults, same device and QSF assignments; the only change is `quartus/phase05_arith_c4/C4-20.sdc` (20.000 ns instead of
40.000 ns). Revisions: `C4b-B-20` (final C4 configuration) and `C3-P6-20` (Phase 4 RTL, unchanged).

| Quantity (MEASURED) | C3-P6 at 20.000 ns | C4b-B at 20.000 ns |
|---|---|---|
| ALM (of 41,910) | 10,557 | 9,305 |
| Registers / M10K / DSP | 4,316 / 29 / 9 | 4,272 / 29 / 18 |
| Worst setup slack (corner) | -2.059 ns (Slow -40C) | -2.557 ns (Slow 100C) |
| Worst hold slack | +0.147 ns | +0.151 ns |
| Timing met at 20.000 ns | **no** | **no** |
| Fmax, lowest slow corner (MHz) | 45.33 | 44.33 |
| Evidence | `quartus_C3-P6-20.md` | `quartus_C4b-B-20.md` |

Reading (INFERENCE, one seed each, so differences of this size are inside the seed spread measured at 40 ns):
- Neither configuration meets 20.000 ns. The shortfall is 2.06 ns (C3-P6) and 2.56 ns (C4b-B).
- Under the 20 ns constraint the fitter works harder, so the reported Fmax (44-45 MHz) is higher than at 40 ns
  (33-35 MHz); the two Fmax values are not comparable across constraints.
- The final C4 configuration is 1,252 ALM smaller than C3-P6 at 20 ns (10,557 - 9,305) and has 9 more DSP, but its Fmax
  is not higher (44.33 vs 45.33 MHz). This agrees with ADR 0010: arithmetic changes do not reach 20 ns while the memory read path
  dominates (`evidence/phase05/baseline/c3p6_critical_path.md`).
- Critical warnings (3 per compile, same in both): 15725 (clock fed by the virtual pin `clk_i`, expected for the
  kernel-only compile, as in Phases 1-4) and 332148 x2 (timing requirements not met, the 20 ns result above). Triaged,
  not waived; no assignment was added.
- No path analysis was run at 20 ns (not requested).
