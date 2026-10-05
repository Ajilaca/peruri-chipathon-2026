<!-- claim-lint: skip-file (internal investigation record, not proposal text) -->
# DE10-Nano system shell (Intel GHRD, no NTT core) — measured fabric overhead

- Date (UTC): 2026-10-01. Investigation for the review of the 25% ALM budget (ADR 0004); no ADR, RTL or Phase 4
  result was changed. Not a design decision and not a final system.
- Labels: **MEASURED** = read from this compile's Quartus reports; **INFERENCE** = a conclusion drawn from measured
  numbers (sums, subsets), not compiled as such.

## 1. Source and identity
| Item | Value |
|---|---|
| Design | Intel DE10-Nano GHRD, <https://github.com/intel/de10-nano-hardware> (repository archived by Intel) |
| Commit | `9b5fc81654c61922b625607d007933a69b5fdb52` (the commit cited in ADR 0006) |
| Revision | `de10-nano-base` (HPS + Platform Designer system of the GHRD; **no NTT core**) |
| Tool | Quartus Prime Lite **25.1std.0 Build 1129** (the GHRD was written for 17.1; no source change was needed) |
| Device | **5CSEBA6U23I7** (set with `quartus_sh --set DEVICE=5CSEBA6U23I7`; the GHRD default `5CSEBA6U23I7DK` was compiled first and gave identical fitter figures) |
| Result | Full Compilation **successful**, 0 errors |
| Location | Built outside this repository (session scratch directory); raw reports are not committed |
| Standard extract | `evidence/phase04/quartus_GHRD-de10-nano-base.md`, written by `.claude/skills/quartus-report/scripts/extract_quartus_report.py` (the project's existing extractor, unchanged; it only reads the reports) |

Commands:
```bash
. scripts/env.sh
export PATH=$QUARTUS_ROOTDIR/sopc_builder/bin:$PATH        # qsys-script, qsys-generate, ip-make-ipx
git clone https://github.com/intel/de10-nano-hardware.git ghrd && cd ghrd
git checkout 9b5fc81654c61922b625607d007933a69b5fdb52
make de10-nano-base/output_files/de10-nano-base.sof         # create project -> qsys-script -> qsys-generate -> compile
cd de10-nano-base
quartus_sh --set -rev de10-nano-base DEVICE=5CSEBA6U23I7 de10-nano-base.qpf
quartus_sh --flow compile de10-nano-base.qpf -c de10-nano-base
# extract (from the repo root):
python3 .claude/skills/quartus-report/scripts/extract_quartus_report.py <ghrd>/de10-nano-base/output_files de10-nano-base \
    --log <compile log> --out evidence/phase04/quartus_GHRD-de10-nano-base.md --note "..."
```

## 2. Resources (MEASURED, fitter report)
| Item | Value |
|---|---|
| Logic utilization (ALMs needed, same metric as the C3 evidence) | **1,309 / 41,910 (3 %)** |
| [A] ALMs placed / [B] recoverable by dense packing / [C] unavailable | 1,601 / 303 / 11 |
| Combinational ALUTs for logic | 2,187 |
| Total registers | **2,381** |
| RAM blocks (M10K) | **35 / 553** (263,424 block-memory bits) |
| MLAB memory bits | 0 |
| DSP blocks | **0 / 112** |
| Pins | 265 / 314 (real pins; the C3 compiles use virtual pins) |
| Fabric PLLs / DLLs / Hard Memory Controller | 0 / 6, 1 / 4, 1 / 1 (HPS DDR3) |
| Difficulty packing design | Low |
| Interconnect usage, average / peak (total) | 1.7 % / 12.9 % |
| LABs partially or completely used | 194 / 4,191 |

### Per entity (MEASURED, "Fitter Resource Utilization by Entity"; ALMs needed)
| Block | ALM | Comb. ALUTs | Registers | M10K |
|---|---|---|---|---|
| **HPS `hps_0` (incl. `fpga_interfaces`, `hps_io`)** | **0.0** | 0 | 0 | 0 |
| `mm_interconnect_0`: HPS H2F AXI master → `onchip_memory2_0` | 433.0 | 718 | 386 | 0 |
| `mm_interconnect_1`: HPS LW H2F AXI master → `lw_mm_bridge` | 274.7 | 467 | 297 | 1 |
| `mm_interconnect_2`: `lw_mm_bridge` → **11 slave Avalon** (list below) | 207.0 | 366 | 400 | 0 |
| `lw_mm_bridge` (Avalon-MM pipeline bridge) | 35.1 | 43 | 115 | 0 |
| PIO/GPIO, 8 blocks: `arduino_gpio` 24.7, `button_pio` 6.3, `dipsw_pio` 6.7, `gpio_0_a` 40.8, `gpio_0_b` 36.7, `gpio_1_a` 36.2, `gpio_1_b` 38.2, `led_pio` 3.1 | **192.7 (≈ 193)** | 293 | 540 | 0 |
| `jtag_uart` | 67.4 | 129 | 120 | 2 |
| `onchip_memory2_0` (32 KB demo memory) | 0.0 | 0 | 0 | 32 |
| `altchip_id_0` | 10.0 | 19 | 144 | 0 |
| Reset: `rst_controller` 1.8, `_002` 0.2, `_003` 0.0, `_004` 0.0, `por` 1.5 | 3.5 | 11 | 43 | 0 |
| `sld_hub` (JTAG debug hub, outside `soc_system`) | 61.5 | 96 | 78 | 0 |
| `debounce` (top-level HDL) | 23.4 | 44 | 32 | 0 |

The children of `soc_system` add up to 1,223.4 ALM against the fitter's 1,223.3 for `soc_system` (rounding).
`sysid_qsys` and `chip_id_read_mm_0` have no separate row in the entity table.

**Correction (2026-10-01):** an earlier chat summary said `mm_interconnect_2` serves 12 slaves; the generated
interconnect (`soc_system_mm_interconnect_2.v`) has **11** slave translators. The 207 ALM figure is unchanged.
The 11 slaves: 1 `arduino_gpio`, 2 `button_pio`, 3 `chip_id` (`chip_id_read_mm_0`), 4 `dipsw_pio`, 5 `gpio_0_a`,
6 `gpio_0_b`, 7 `gpio_1_a`, 8 `gpio_1_b`, 9 `jtag_uart`, 10 `led_pio`, 11 `sysid` (`sysid_qsys`).

## 3. Timing (MEASURED, Timing Analyzer; all clocks constrained by the GHRD's own SDC)
- Worst setup slack **+1.573 ns** (Slow 1100mV −40C, HPS SDRAM `afi_clk_write_clk`).
- Worst hold slack **+0.076 ns** (Fast 1100mV −40C, same clock).
- No negative slack for setup, hold, recovery, removal or minimum pulse width at any corner; 0 unconstrained clocks.
- `fpga_clk1_50` (constrained at 20 ns): Fmax 94.71 MHz (Slow 100C), 92.73 MHz (Slow −40C).
- This is the timing of the shell logic only; it says nothing about the NTT core or a combined design.

## 4. Messages (MEASURED)
- Critical warnings, 2, both pin placement and both outside the scope of a resource measurement:
  169085 (72 of 265 pins without an exact location) and 174073 (1 RUP/RDN/RZQ pin without an exact location).
- `qsys-script` printed "ERROR: Device family can not be determined" three times while adding `altera_hps`; the
  system was still generated (58 modules) and compiled. Not investigated further.

## 5. Comparison with the Phase 4 core (INFERENCE — sums of separate compiles)
Separate compiles do not add exactly: in one combined compile the fitter packs differently. Device = 41,910 ALM.
C3 figures: `evidence/phase04/seed_sweep.md` (seeds 1–6).

| Case | ALM | % of device | Remaining ALM | Remaining % |
|---|---|---|---|---|
| GHRD base shell alone (MEASURED) | 1,309 | 3.12 % | 40,601 | 96.88 % |
| C3-P4 seed 1 + GHRD base | 11,748 | 28.03 % | 30,162 | 71.97 % |
| C3-P4 seeds 1–6 + GHRD base | 11,748–11,812 | 28.03–28.18 % | 30,098–30,162 | 71.82–71.97 % |
| C3-P6 seed 1 + GHRD base | 11,814 | 28.19 % | 30,096 | 71.81 % |
| C3-P6 seeds 1–6 + GHRD base | 11,793–11,825 | 28.14–28.22 % | 30,085–30,117 | 71.78–71.86 % |

**LW-bridge subset (INFERENCE):** HPS (0) + `mm_interconnect_1` (274.7) + `lw_mm_bridge` (35.1) + reset (3.5) ≈ **313 ALM
(0.75 %)** and 1 M10K, i.e. the part of this shell an NTT slave behind the lightweight bridge would need at least.
It excludes the slave-side fan-out (`mm_interconnect_2`, 207 ALM for 11 slaves), whose cost for a single NTT slave was
not measured. With this subset, C3-P4 / C3-P6 + shell ≈ 10,752–10,829 ALM (25.66–25.84 %). Not compiled as such.

M10K (INFERENCE, sum): C3-P4 26 + 35 = 61 / 553; C3-P6 29 + 35 = 64 / 553; 32 of the shell's 35 are the demo
on-chip memory. DSP: C3 9 + shell 0.

## 6. What this does and does not show
- MEASURED: the HPS hard block uses no ALMs; the shell's fabric cost is Platform Designer interconnect plus the
  GHRD's demo IP (PIO/GPIO, JTAG UART, on-chip memory).
- MEASURED: the complete GHRD base uses 3.12 % of the ALMs, with low packing difficulty and interconnect usage, and
  meets timing.
- Not shown: a combined compile (shell + NTT core), the cost of the bridge actually chosen (PENDING #3), clock-domain
  crossing between the core clock and the bridge clock, SignalTap overhead, and the blocks of Phases 5–9.
