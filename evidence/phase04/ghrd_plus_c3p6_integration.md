<!-- claim-lint: skip-file (internal investigation record, not proposal text) -->
# GHRD DE10-Nano + C3-P6 in one Quartus compilation - integration experiment

Labels: **MEASURED** = read from a Quartus report of the compiles listed in Section 2; **INFERENCE** = derived from
measured numbers (differences, sums, interpretation); **NOT MEASURED** = not obtained in this experiment.
This file closes the gap named in ADR 0009 ("P = 6 + GHRD was not compiled"). It repeats
`ghrd_plus_c3p4_integration.md` with C3-P6, the configuration selected by ADR 0009. No RTL, ADR or earlier
evidence file was changed.

## 1. Purpose
Measure, in one compilation, what happens to resources and timing when the selected core C3-P6 shares the device with
the DE10-Nano HPS system shell, and compare it with the standalone compiles made with the same settings.

## 2. Source revisions and compiles
| Compile | Sources | Settings | Role |
|---|---|---|---|
| **C3-P6 (Phase 4)** | repo `rtl/` (unchanged since Phase 4), `quartus/phase04_pipeline_c3/C3-P6.qsf`, `C3.sdc` | Quartus defaults | existing evidence `quartus_C3-P6.md` |
| **C3-P6-ghrdset** | same RTL, SDC, virtual pins and default seed as C3-P6, plus the 5 global settings of the GHRD QSF (Section 4) | GHRD settings | standalone core with the same settings as the combined compile |
| **GHRD base (fresh build)** | Intel DE10-Nano GHRD, `github.com/intel/de10-nano-hardware` commit `9b5fc81654c61922b625607d007933a69b5fdb52`, revision `de10-nano-base`, same generated Platform Designer system as the combined project | GHRD settings | standalone shell |
| **Combined `de10-nano-c3p6`** | the GHRD base project (copied) + C3-P6 RTL referenced read-only from the repo | GHRD settings | integration |

All: device **5CSEBA6U23I7**, Quartus Prime Lite **25.1std.0 Build 1129**, default fitter seed, Full Compilation
successful with 0 errors (MEASURED). Elapsed time: combined 15 min 03 s, C3-P6-ghrdset 12 min 23 s, GHRD base 8 min 32 s.
Experiment files live outside the repository in the team's experiments folder (GHRD clone, combined project,
standalone project, `metrics.py`, the sequential compile script).

**Process note (stated plainly).** The first run of the GHRD base compile was skipped by Quartus smart recompilation
(log: "Smart recompilation skipped module Fitter because it is not required", 5 s); its reports were the earlier build's.
That run was **not** used. The old database was moved aside and the compile was repeated in full (log has no
"skipped" line, 8 min 32 s, fitter finished 14:48 local time). The fresh build gave the same numbers as the earlier one
(1,304 ALM, 2,369 registers, 35 M10K).

## 3. Integration topology
Same as the C3-P4 experiment: `top_c3p6.v` = the GHRD `hdl_src/top.v` with the same 11 `ntt_*` ports (all virtual pins,
own clock `ntt_clk_i`) and one instance of `ntt_core_c3_p6`; SDC = `create_clock -name ntt_clk_i -period 40.000`,
`derive_clock_uncertainty`, false path from `ntt_rst_ni`, content identical to `quartus/phase04_pipeline_c3/C3.sdc`
(checked: the standalone project's `C3.sdc` is byte-identical to the repo's). The RTL file list is the one of
`C3-P6.qsf`. **The NTT is not connected to the HPS, any bridge or any GHRD signal**; no clock-domain crossing exists
(PENDING #3).

## 4. Compile settings (confound handled as in the P4 experiment)
GHRD global settings applied to the whole project, the core included: `OPTIMIZATION_MODE "AGGRESSIVE PERFORMANCE"`,
`PHYSICAL_SYNTHESIS_COMBO_LOGIC_FOR_AREA ON`, `PHYSICAL_SYNTHESIS_REGISTER_DUPLICATION ON`,
`BLOCK_RAM_TO_MLAB_CELL_CONVERSION OFF`, `OPTIMIZE_MULTI_CORNER_TIMING ON`. The standalone C3-P6-ghrdset compile
separates the settings effect from the integration effect.

## 5. Exact commands
```bash
. scripts/env.sh; export PATH=$QUARTUS_ROOTDIR/sopc_builder/bin:$PATH
cd <experiments>/ghrd/de10-nano-c3p6   && quartus_sh --flow compile de10-nano-c3p6 -c de10-nano-c3p6        # combined
cd <experiments>/c3p6_ghrd_settings    && quartus_sh --flow compile C3-P6-ghrdset -c C3-P6-ghrdset          # standalone, GHRD settings
cd <experiments>/ghrd/de10-nano-base   && quartus_sh --flow compile de10-nano-base.qpf -c de10-nano-base    # after moving db/ and output_files/ aside
python3 <experiments>/metrics.py <output_files> <revision> [entity ...]                                     # read-only extraction
```
The three compiles ran one at a time (parallel runs corrupt the shared `.qpf`).

## 6. Measured resources (MEASURED)
| Metric | C3-P6 (Phase 4, defaults) | C3-P6-ghrdset | GHRD base (fresh) | **Combined** |
|---|---:|---:|---:|---:|
| ALMs needed | 10,505 | 11,053 | 1,304 | **12,375** (30 %) |
| [A] placed | - | 11,998 | 1,588 | 13,468 |
| [B] recoverable by dense packing | - | 1,197 | 294 | 1,338 |
| [C] unavailable | - | 252 | 10 | 245 |
| Combinational ALUTs for logic | - | 17,656 | 2,187 | 19,819 |
| Total registers | 4,168 | 4,790 | 2,369 | 6,876 |
| M10K | 29 / 553 | 28 / 553 | 35 / 553 | 62 / 553 |
| DSP | 9 / 112 | 9 / 112 | 0 / 112 | 9 / 112 |
| Fabric PLLs / DLLs | 0 / 0 | 0 / 0 | 0 / 1 | 0 / 1 |
| LABs used | - | 1,363 | 208 | 1,580 |
| Difficulty packing design | - | Low | Low | Low |
| Interconnect average (total) | - | 11.9 % | 1.6 % | 10.9 % |
| Interconnect peak (total) | - | 51.8 % | 11.6 % | 37.0 % |
| Router estimate average / peak | - | 10 % / 44 % | 1 % / 10 % | 9 % / 33 % |

"-" = not extracted for the Phase 4 evidence file (see `quartus_C3-P6.md` for what it contains).
Per entity in the combined compile (MEASURED): `ntt_core_c3_p6` 11,050.0 ALM, 17,604 ALUTs, 4,490 registers, 27 M10K,
9 DSP; `soc_system` 1,219.3 ALM, 35 M10K; `sld_hub` 61.5; `debounce` 23.7. Standalone GHRD: `soc_system` 1,217.8 ALM.

## 7. Measured timing (MEASURED; worst over the corners printed)
| Clock | C3-P6 (Phase 4) | C3-P6-ghrdset | GHRD base (fresh) | Combined |
|---|---|---|---|---|
| NTT clock (`clk_i` / `ntt_clk_i`, 40.000 ns): setup / hold | +10.753 / +0.140 | +16.017 / +0.152 | - | **+11.364 / +0.129** |
| NTT Fmax, Slow 100C / Slow −40C (MHz) | 34.19 / 34.5 | 41.74 / 41.7 | - | 34.92 / **35.58** |
| `fpga_clk1_50` (20 ns): setup / hold | - | - | +6.102 / +0.135 | +6.358 / +0.143 |
| `fpga_clk1_50` Fmax, Slow 100C / −40C (MHz) | - | - | 85.06 / 87.33 | 77.35 / 78.29 |
| HPS SDRAM `afi_clk_write_clk`: setup / hold | - | - | +1.573 / +0.076 | +1.573 / +0.076 |
| `h2f_user1_clk`: setup / hold | - | - | +18.629 / +0.247 | +18.919 / +0.229 |
| `altera_reserved_tck` (JTAG): setup / hold | - | - | +6.255 / +0.107 | +6.255 / +0.120 |
| System worst setup / hold | - | - | +1.573 / +0.076 | **+1.573 / +0.076** (both on `afi_clk_write_clk`) |

- Combined: no negative setup, hold, recovery or removal slack on any clock (MEASURED). The NTT domain meets 40.000 ns
  and the shell domains keep meeting their GHRD constraints.
- The NTT Fmax is the `ntt_clk_i` row only. Lowest slow-corner NTT Fmax: combined 34.92 MHz; C3-P6-ghrdset 41.70 MHz;
  C3-P6 Phase 4 34.19 MHz.
- Setup slack in the "C3-P6 (Phase 4)" column is at Slow 100C and hold at Fast −40C, as in `quartus_C3-P6.md`;
  the other columns use the minimum over every corner `metrics.py` printed, so the comparison is indicative.
- The system's worst setup path is on the HPS SDRAM clock in the standalone and combined compile; the path nodes were
  **NOT MEASURED** (no path report generated).
- Critical warnings (MEASURED): combined 15725 (`ntt_clk_i` virtual pin, as in every Phase 4 compile), 169085 and 174073
  (GHRD pin placement, also in the standalone GHRD); C3-P6-ghrdset 15725 only; GHRD base 169085 and 174073. No 332148.

## 8. Integration delta
`integration_delta = combined − P6_standalone − GHRD_standalone` (INFERENCE, arithmetic on MEASURED values):

| Baseline for the core | Formula | Delta |
|---|---|---|
| C3-P6-ghrdset (same settings as combined) | 12,375 − 11,053 − 1,304 | **+18 ALM** |
| C3-P6 Phase 4 (default settings) | 12,375 − 10,505 − 1,304 | **+566 ALM** |
| of which: settings effect on the core alone | 11,053 − 10,505 | +548 ALM |

Other deltas against C3-P6-ghrdset + GHRD (INFERENCE): ALUTs −24; registers −283; M10K −1; [A] placed −118;
[B] recoverable −153; [C] unavailable −17; LABs +9.

Reading (INFERENCE):
- With consistent settings, the shared compile changed "ALMs needed" by +18 (0.04 % of the device), the same value as the
  C3-P4 experiment. The core's own ALM count in the combined compile (11,050.0) is within 3 ALM of its standalone count
  with the same settings (11,053). No measurable packing penalty on the metric the budget uses.
- The GHRD settings added +548 ALM to C3-P6 (+993 to C3-P4). The settings effect is therefore not a fixed amount; it was
  measured here for one seed per revision and is not generalised.
- Against the C3-P4 experiment: combined 12,375 (P6) vs 12,754 (P4), 379 lower; C3-P6-ghrdset 11,053 vs C3-P4-ghrdset
  11,432, also 379 lower. Under GHRD settings the deeper pipeline came out smaller; under Quartus defaults it is
  larger (10,505 vs 10,439). One compile per revision at one seed; the cause is not established.
- Timing: the NTT clock meets 40.000 ns in the combined compile; setup +11.364 ns. NTT Fmax 34.92 MHz combined vs
  41.74 MHz standalone with the same settings. Phase 4's seed sweep showed Fmax spreads up to about 5 % between seeds
  at default settings; a 16 % difference was not tested for seed dependence, so it is not attributed to integration.
- Congestion indicators: packing difficulty Low, interconnect average 10.9 %, peak 37.0 % (INFERENCE: no congestion).

## 9. Budget figures (requested; no pass/fail is drawn)
| Item | Value |
|---|---|
| Combined ALMs needed | 12,375 (MEASURED) |
| Combined % of device | 29.53 % (INFERENCE: 12,375 / 41,910) |
| Combined vs 12,573 | 198 ALM below (INFERENCE) |
| Margin to 41,910 (device) | 29,535 ALM, 70.47 % (INFERENCE) |
| Core alone, GHRD settings (C3-P6-ghrdset) | 11,053 ALM = 26.37 % (INFERENCE) |

ADR 0009 defines 12,573 as a design budget for the NTT core, not for core + shell, so the combined total is **not** a
check against it. The comparison with 12,573 above is arithmetic only, as requested. Keccak, samplers, controller,
storage, bridge and SignalTap are not in this compile.

## 10. Limitations
- **NOT MEASURED:** a real HPS ↔ NTT connection (bridge, CSR, DMA), any clock-domain crossing, an NTT clock derived
  from a board clock or PLL, SignalTap, other seeds of the combined compile, a combined compile with Quartus defaults,
  any board run.
- The NTT runs on its own virtual-pin clock; 40.000 ns met means the core's internal paths meet 40 ns next to the
  shell, not that a 25 MHz clock exists on the board. 50 MHz (20 ns) was not tried here.
- One compile per configuration at the default seed (Phase 4: 32–64 ALM and 4.8–7.5 % Fmax between seeds).
- The GHRD base gave 1,304 ALM in both builds made after the system was regenerated (the earlier-morning build gave
  1,309; cause not established, see `ghrd_plus_c3p4_integration.md` Section 10).

## 11. Conclusion
- MEASURED: GHRD + C3-P6 fit and compile together on 5CSEBA6U23I7 with 12,375 ALMs (30 %), 62 M10K and 9 DSP; every
  clock meets its constraint, including the NTT clock at 40.000 ns (setup +11.364 ns, Fmax 34.92 MHz).
- INFERENCE: integration itself costs about +18 ALM, the same as for C3-P4. The 566 ALM between the Phase 4 core number
  and the combined number is dominated by the GHRD's optimisation settings (+548 ALM on the core).
- The Phase 4 evidence gap (P6 + GHRD not compiled) is closed for resources and timing of the unconnected core.
