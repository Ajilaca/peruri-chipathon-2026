<!-- claim-lint: skip-file (internal investigation record, not proposal text) -->
# GHRD DE10-Nano + C3-P4 in one Quartus compilation — integration experiment

Labels: **MEASURED** = read from a Quartus report of the compiles listed in Section 2; **INFERENCE** = derived from
measured numbers (differences, sums, interpretation); **NOT MEASURED** = not obtained in this experiment.

## 1. Purpose
Measure, in one compilation, what happens to resources and timing when the Phase 4 core C3-P4 shares the device
with the DE10-Nano HPS system shell, and compare that with the two standalone compiles. C3-P4 is used as the
integration **baseline** only. This experiment does not select P, does not change ADR 0004 / 0007 / 0008, and does
not change any RTL. (Team direction stated with the request: L = 8, P6, 30% design budget; not acted on here.)

## 2. Source revisions and compiles
| Compile | Sources | Settings | Role |
|---|---|---|---|
| **C3-P4 (Phase 4)** | repo `rtl/` at `a803386`, `quartus/phase04_pipeline_c3/C3-P4.qsf`, `C3.sdc` | Quartus defaults | existing evidence `quartus_C3-P4_20260930.md` |
| **C3-P4-ghrdset** | same RTL, QSF, SDC and virtual pins as C3-P4, plus the 5 global optimisation settings of the GHRD QSF (Section 4) | GHRD settings | standalone core with the **same settings as the combined compile** |
| **GHRD base (today)** | Intel DE10-Nano GHRD, `github.com/intel/de10-nano-hardware` commit `9b5fc81654c61922b625607d007933a69b5fdb52`, revision `de10-nano-base`, Platform Designer system generated today | GHRD settings | standalone shell, same generated system as the combined compile |
| **Combined `de10-nano-c3p4`** | the GHRD base project above (copied) + C3-P4 RTL referenced read-only from the repo | GHRD settings | integration |

All four: device **5CSEBA6U23I7**, Quartus Prime Lite **25.1std.0 Build 1129**, default fitter seed, Full Compilation
successful with 0 errors (MEASURED). Experiment files live outside the repository in
`~/FPGA/Projects/CHIPATON_experiments/` (GHRD clone, combined project, C3-P4-ghrdset project, `metrics.py`).

## 3. Integration topology
- `top_c3p4.v` = the GHRD `hdl_src/top.v` with two additions only: 11 new top-level ports `ntt_*` and one instance
  `ntt_core_c3_p4 u_ntt_c3p4` connected to them. The original `top.v`, the GHRD SDC files and the Platform Designer
  system are unchanged.
- All `ntt_*` ports, including `ntt_clk_i`, are **virtual pins**, exactly as in the standalone Phase 4 compile.
  The NTT has its own clock `ntt_clk_i` with the Phase 4 constraint (`c3p4_virtual.sdc` =
  `create_clock -name ntt_clk_i -period 40.000`, `derive_clock_uncertainty`, false path from `ntt_rst_ni`), so the
  40.000 ns constraint is applied in the same way as in Phase 4.
- **The NTT is not connected to the HPS, any bridge or any GHRD signal.** No clock-domain crossing exists. Connecting
  it would need an interface/bridge/CDC decision (PENDING #3), which this experiment does not make.
- The combined QSF = GHRD QSF with `DEVICE` set to 5CSEBA6U23I7, `top.v` replaced by `top_c3p4.v`, and the C3-P4 RTL
  list (identical to `C3-P4.qsf`), the NTT SDC file and the virtual-pin assignments appended.

## 4. Confound found before compiling: the GHRD's global settings
The GHRD QSF contains settings that apply to the whole project, the NTT included; the Phase 4 compiles use defaults:
`OPTIMIZATION_MODE "AGGRESSIVE PERFORMANCE"`, `PHYSICAL_SYNTHESIS_COMBO_LOGIC_FOR_AREA ON`,
`PHYSICAL_SYNTHESIS_REGISTER_DUPLICATION ON`, `BLOCK_RAM_TO_MLAB_CELL_CONVERSION OFF`,
`OPTIMIZE_MULTI_CORNER_TIMING ON`. Nothing was changed in the combined project; instead the extra compile
**C3-P4-ghrdset** (same five settings, nothing else changed) separates the settings effect from the integration effect.

## 5. Exact commands
```bash
. scripts/env.sh; export PATH=$QUARTUS_ROOTDIR/sopc_builder/bin:$PATH
cd ~/FPGA/Projects/CHIPATON_experiments
git clone https://github.com/intel/de10-nano-hardware.git ghrd && cd ghrd && git checkout 9b5fc81654c61922b625607d007933a69b5fdb52
make de10-nano-base/output_files/de10-nano-base.sof                      # generate the system once
# combined project = copy of de10-nano-base/{soc_system,soc_system.qsys,soc_system.sopcinfo,QSF} into de10-nano-c3p4/,
# top_c3p4.v, c3p4_virtual.sdc and QSF additions as in Section 3
cd de10-nano-c3p4 && quartus_sh --flow compile de10-nano-c3p4 -c de10-nano-c3p4
cd ../de10-nano-base && quartus_sh --set -rev de10-nano-base DEVICE=5CSEBA6U23I7 de10-nano-base.qpf \
                     && quartus_sh --flow compile de10-nano-base.qpf -c de10-nano-base
cd ../../c3p4_ghrd_settings && quartus_sh --flow compile C3-P4-ghrdset -c C3-P4-ghrdset
python3 ../metrics.py <output_files> <revision> [entity ...]             # read-only extraction
```

## 6. Measured resources (MEASURED)
| Metric | C3-P4 (Phase 4, defaults) | C3-P4-ghrdset | GHRD base (today) | **Combined** |
|---|---:|---:|---:|---:|
| ALMs needed | 10,439 | 11,432 | 1,304 | **12,754** (30 %) |
| [A] placed | 10,695 | 12,183 | 1,588 | 13,991 |
| [B] recoverable by dense packing | 388 | 990 | 294 | 1,452 |
| [C] unavailable | 132 | 239 | 10 | 215 |
| Combinational ALUTs for logic | 13,047 | 17,735 | 2,187 | 19,938 |
| Total registers | 4,145 | 4,320 | 2,369 | 6,530 |
| M10K | 26 / 553 | 26 / 553 | 35 / 553 | 60 / 553 |
| MLAB memory bits | 0 | 0 | 0 | 0 |
| DSP | 9 / 112 | 9 / 112 | 0 / 112 | 9 / 112 |
| Fabric PLLs / DLLs | 0 / 0 | 0 / 0 | 0 / 1 | 0 / 1 |
| LABs used | 1,309 | 1,403 | 208 | 1,645 |
| Difficulty packing design | Low | Low | Low | Low |
| Interconnect average (total) | 12.4 % | 13.6 % | 1.6 % | 13.8 % |
| Interconnect peak (total) | 55.2 % | 52.7 % | 11.6 % | 48.2 % |
| Router estimate average / peak | 11 % / 49 % | n/a | n/a | 12 % / 45 % |

Per entity in the combined compile (MEASURED): `ntt_core_c3_p4` 11,432.5 ALM, 17,728 ALUTs, 4,173 registers, 25 M10K,
9 DSP; `soc_system` 1,216.2 ALM, 35 M10K; `sld_hub` 61.5; `debounce` 23.3. Standalone GHRD today: `soc_system`
1,217.8 ALM.

## 7. Measured timing (MEASURED; worst over the corners printed)
| Clock | C3-P4 (Phase 4) | C3-P4-ghrdset | GHRD base (today) | Combined |
|---|---|---|---|---|
| NTT clock (`clk_i` / `ntt_clk_i`, 40.000 ns): setup / hold | +8.734 / +0.157 | +10.885 / +0.123 | — | **+9.204 / +0.149** |
| NTT Fmax, Slow 100C / Slow −40C (MHz) | 32.60 / 31.98 | 34.35 / 34.66 | — | 32.70 / **32.47** |
| `fpga_clk1_50` (20 ns): setup / hold | — | — | +6.102 / +0.135 | +6.890 / +0.126 |
| `fpga_clk1_50` Fmax, Slow 100C / −40C (MHz) | — | — | 85.06 / 87.33 | 84.93 / 88.53 |
| HPS SDRAM `afi_clk_write_clk`: setup / hold | — | — | +1.573 / +0.076 | +1.573 / +0.076 |
| `h2f_user1_clk`: setup / hold | — | — | +18.629 / +0.247 | +18.963 / +0.234 |
| System worst setup / hold | — | — | +1.573 / +0.076 | **+1.573 / +0.076** (both on `afi_clk_write_clk`) |

- Combined: no negative setup, hold, recovery or removal slack on any clock (MEASURED). The NTT domain meets 40.000 ns
  and the shell domains keep meeting their GHRD constraints.
- The NTT Fmax is the `ntt_clk_i` row only; the shell's Fmax is not used for the NTT.
- The system's worst setup path is on the HPS SDRAM clock in both the standalone and the combined compile; the path
  nodes were **NOT MEASURED** (no path report was generated).
- Critical warnings, combined (MEASURED): 15725 (`ntt_clk_i` is a virtual pin, as in every Phase 4 compile), 169085
  and 174073 (GHRD pin placement, as in the standalone GHRD).

## 8. Integration delta
`integration_delta = combined_ALM − P4_standalone_ALM − GHRD_standalone_ALM` (INFERENCE, arithmetic on MEASURED values):

| Baseline for the core | Formula | Delta |
|---|---|---|
| C3-P4-ghrdset (same settings as combined) | 12,754 − 11,432 − 1,304 | **+18 ALM** |
| C3-P4 Phase 4 (default settings) | 12,754 − 10,439 − 1,304 | **+1,011 ALM** |
| of which: settings effect on the core alone | 11,432 − 10,439 | +993 ALM |

Other deltas against C3-P4-ghrdset + GHRD (INFERENCE): ALUTs +16; registers −159; M10K −1 (the core uses 25 M10K
in the combined compile, 26 standalone); [A] placed +220; [B] recoverable +168; [C] unavailable −34; LABs +34.

Reading (INFERENCE):
- With consistent settings, putting the shell and the core in one compile changed "ALMs needed" by +18 (0.04 % of the
  device). The core's own ALM count inside the combined compile (11,432.5) equals its standalone count with the same
  settings (11,432). No measurable packing penalty or benefit on the metric the budget uses.
- The ~+1,000 ALM between the Phase 4 number and the combined number comes from the GHRD's global optimisation
  settings (aggressive performance, physical synthesis with register duplication), not from integration.
- Timing: with the same settings, the core's worst NTT setup slack is +10.885 ns standalone and +9.204 ns combined
  (Fmax 34.35 → 32.47 MHz at the lowest slow corner, −5.5 %). This is one compile each at one seed; Phase 4's seed
  sweep showed Fmax spreads of 4.8–7.5 % between seeds, so this difference is not shown to be an integration effect.
- [A] placed rises by 220 while "needed" rises by 18: the fitter spreads logic more loosely when there is room
  ([B] recoverable rises by 168). This is the packing estimate behaving as at low utilisation; not congestion.

## 9. Budget figures (requested; no selection is made from them)
| Item | Value |
|---|---|
| Combined ALMs needed | 12,754 (MEASURED) |
| Combined % of device | 30.43 % (INFERENCE: 12,754 / 41,910) |
| Margin to 12,573 (30 %) | **−181 ALM** (over by 181) (INFERENCE) |
| Margin to 41,910 (device) | 29,156 ALM, 69.57 % (INFERENCE) |

The scope of the 30 % budget (NTT core alone, or core + shell) is not defined in any ADR; this file reports the number
against the whole combined design as requested and draws no conclusion from it. With the GHRD settings the core alone
uses 11,432 ALM (27.3 %).

*Update 2026-10-01 (after this experiment):* ADR 0009 defines the 30 % / 12,573 ALM figure as a design budget for the
NTT core (Phase 4), not for core + shell. The combined total above is therefore not a check against that budget. No
measurement in this file was changed.

## 10. Limitations
- **NOT MEASURED:** a real HPS ↔ NTT connection (bridge, CSR, DMA), any clock-domain crossing, an NTT clock derived
  from a board clock or PLL, SignalTap, P6 or any P other than 4, other seeds of the combined compile.
- The NTT runs on its own virtual-pin clock; the 40.000 ns result says the core's internal paths meet 40 ns next to the
  shell, not that a 25 MHz clock exists on the board.
- One compile per configuration, default seed. Phase 4 showed seed-to-seed spreads of 32–64 ALM and 4.8–7.5 % Fmax.
- **Reproducibility note (MEASURED):** the same GHRD commit, tool, seed and device setting gave 1,309 ALM / 2,381
  registers on 2026-10-01 morning (`ghrd_shell_measured_2026-10-01.md`) and 1,304 / 2,369 after regenerating the
  Platform Designer system in this experiment. Cause not established (INFERENCE: a generation-dependent constant such
  as the `sysid` timestamp). The deltas above use the build whose generated system the combined project copied.
- The combined compile uses the GHRD settings for the whole design; a combined compile with Quartus defaults was not
  run (NOT MEASURED).

## 11. Conclusion
- MEASURED: GHRD + C3-P4 fit and compile together on 5CSEBA6U23I7 with 12,754 ALMs (30 %), 60 M10K and 9 DSP; every
  clock meets its constraint, including the NTT clock at 40.000 ns (worst setup +9.204 ns, Fmax 32.47 MHz).
- INFERENCE: integration itself costs about +18 ALM. The difference from the Phase 4 figure is dominated by the GHRD's
  optimisation settings (+993 ALM on the core), which means the compile settings used for a system build are a
  budget-relevant decision in their own right.
- INFERENCE: no congestion indicator moved meaningfully (packing difficulty Low, average interconnect 13.8 %, peak
  48.2 %).
