# MEASURED - Quartus results for revision `de10-nano-base`

- Generated: 2026-10-01 04:23 UTC by `extract_quartus_report.py` (values copied from the reports, not computed)
- Source directory: `<session scratch directory>/ghrd/de10-nano-base/output_files` (local path redacted before commit; public repository, CLAUDE.md C7 - no measured value changed)
- Note: Intel DE10-Nano GHRD (github.com/intel/de10-nano-hardware, commit 9b5fc81654c61922b625607d007933a69b5fdb52), revision de10-nano-base, no NTT core; DEVICE set to 5CSEBA6U23I7 (the GHRD default is 5CSEBA6U23I7DK, which gave identical fitter figures); Quartus Prime Lite 25.1std.0 Build 1129; system shell overhead investigation for the ALM-budget review

## Fitter (`de10-nano-base.fit.summary`)

| Item | Value (verbatim) |
|---|---|
| Fitter Status | Successful - Thu Oct  1 11:14:03 2026 |
| Quartus Prime Version | 25.1std.0 Build 1129 10/21/2025 SC Lite Edition |
| Revision Name | de10-nano-base |
| Top-level Entity Name | top |
| Family | Cyclone V |
| Device | 5CSEBA6U23I7 |
| Timing Models | Final |
| Logic utilization (in ALMs) | 1,309 / 41,910 ( 3 % ) |
| Total registers | 2381 |
| Total pins | 265 / 314 ( 84 % ) |
| Total block memory bits | 263,424 / 5,662,720 ( 5 % ) |
| Total RAM Blocks | 35 / 553 ( 6 % ) |
| Total DSP Blocks | 0 / 112 ( 0 % ) |
| Total PLLs | 0 / 6 ( 0 % ) |
| Total DLLs | 1 / 4 ( 25 % ) |

Denominators above are the fitter's own; quote them as printed.

## Timing (`de10-nano-base.sta.summary`)

| Type | Slack (ns) | TNS |
|---|---|---|
| Slow 1100mV 100C Model Setup 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk' | 1.574 | 0.000 |
| Slow 1100mV 100C Model Setup 'fpga_clk1_50' | 6.202 | 0.000 |
| Slow 1100mV 100C Model Setup 'altera_reserved_tck' | 6.255 | 0.000 |
| Slow 1100mV 100C Model Setup 'soc_inst|hps_0|fpga_interfaces|clocks_resets|h2f_user1_clk' | 18.984 | 0.000 |
| Slow 1100mV 100C Model Hold 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk' | 0.164 | 0.000 |
| Slow 1100mV 100C Model Hold 'fpga_clk1_50' | 0.328 | 0.000 |
| Slow 1100mV 100C Model Hold 'altera_reserved_tck' | 0.366 | 0.000 |
| Slow 1100mV 100C Model Hold 'soc_inst|hps_0|fpga_interfaces|clocks_resets|h2f_user1_clk' | 0.458 | 0.000 |
| Slow 1100mV 100C Model Recovery 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk' | 3.040 | 0.000 |
| Slow 1100mV 100C Model Recovery 'fpga_clk1_50' | 4.564 | 0.000 |
| Slow 1100mV 100C Model Recovery 'altera_reserved_tck' | 14.381 | 0.000 |
| Slow 1100mV 100C Model Removal 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk' | 0.562 | 0.000 |
| Slow 1100mV 100C Model Removal 'altera_reserved_tck' | 0.971 | 0.000 |
| Slow 1100mV 100C Model Removal 'fpga_clk1_50' | 1.008 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|pll_write_clk_dq_write_clk' | 0.523 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk' | 0.540 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'soc_inst|hps_0|fpga_interfaces|peripheral_i2c2|out_clk' | 4.508 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'fpga_clk1_50' | 8.829 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'soc_inst|hps_0|fpga_interfaces|clocks_resets|h2f_user1_clk' | 9.305 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'hps_usb1_CLK' | 10.137 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'altera_reserved_tck' | 15.572 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'hps_i2c0_SCL' | 499.730 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'hps_i2c1_SCL' | 499.730 | 0.000 |
| Slow 1100mV -40C Model Setup 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk' | 1.573 | 0.000 |
| Slow 1100mV -40C Model Setup 'altera_reserved_tck' | 6.388 | 0.000 |
| Slow 1100mV -40C Model Setup 'fpga_clk1_50' | 6.410 | 0.000 |
| Slow 1100mV -40C Model Setup 'soc_inst|hps_0|fpga_interfaces|clocks_resets|h2f_user1_clk' | 18.967 | 0.000 |
| Slow 1100mV -40C Model Hold 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk' | 0.216 | 0.000 |
| Slow 1100mV -40C Model Hold 'fpga_clk1_50' | 0.305 | 0.000 |
| Slow 1100mV -40C Model Hold 'altera_reserved_tck' | 0.352 | 0.000 |
| Slow 1100mV -40C Model Hold 'soc_inst|hps_0|fpga_interfaces|clocks_resets|h2f_user1_clk' | 0.477 | 0.000 |
| Slow 1100mV -40C Model Recovery 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk' | 3.130 | 0.000 |
| Slow 1100mV -40C Model Recovery 'fpga_clk1_50' | 4.663 | 0.000 |
| Slow 1100mV -40C Model Recovery 'altera_reserved_tck' | 14.593 | 0.000 |
| Slow 1100mV -40C Model Removal 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk' | 0.590 | 0.000 |
| Slow 1100mV -40C Model Removal 'fpga_clk1_50' | 0.823 | 0.000 |
| Slow 1100mV -40C Model Removal 'altera_reserved_tck' | 0.952 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|pll_write_clk_dq_write_clk' | 0.525 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk' | 0.546 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'soc_inst|hps_0|fpga_interfaces|peripheral_i2c2|out_clk' | 4.401 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'fpga_clk1_50' | 8.790 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'soc_inst|hps_0|fpga_interfaces|clocks_resets|h2f_user1_clk' | 9.232 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'hps_usb1_CLK' | 10.144 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'altera_reserved_tck' | 15.581 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'hps_i2c0_SCL' | 499.754 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'hps_i2c1_SCL' | 499.754 | 0.000 |
| Fast 1100mV 100C Model Setup 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk' | 2.113 | 0.000 |
| Fast 1100mV 100C Model Setup 'fpga_clk1_50' | 7.486 | 0.000 |
| Fast 1100mV 100C Model Setup 'altera_reserved_tck' | 8.962 | 0.000 |
| Fast 1100mV 100C Model Setup 'soc_inst|hps_0|fpga_interfaces|clocks_resets|h2f_user1_clk' | 19.492 | 0.000 |
| Fast 1100mV 100C Model Hold 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk' | 0.083 | 0.000 |
| Fast 1100mV 100C Model Hold 'fpga_clk1_50' | 0.177 | 0.000 |
| Fast 1100mV 100C Model Hold 'altera_reserved_tck' | 0.228 | 0.000 |
| Fast 1100mV 100C Model Hold 'soc_inst|hps_0|fpga_interfaces|clocks_resets|h2f_user1_clk' | 0.249 | 0.000 |
| Fast 1100mV 100C Model Recovery 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk' | 3.731 | 0.000 |
| Fast 1100mV 100C Model Recovery 'fpga_clk1_50' | 7.412 | 0.000 |
| Fast 1100mV 100C Model Recovery 'altera_reserved_tck' | 15.849 | 0.000 |
| Fast 1100mV 100C Model Removal 'altera_reserved_tck' | 0.383 | 0.000 |
| Fast 1100mV 100C Model Removal 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk' | 0.497 | 0.000 |
| Fast 1100mV 100C Model Removal 'fpga_clk1_50' | 0.515 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|pll_write_clk_dq_write_clk' | 0.883 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk' | 0.891 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'soc_inst|hps_0|fpga_interfaces|peripheral_i2c2|out_clk' | 4.557 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'fpga_clk1_50' | 8.499 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'soc_inst|hps_0|fpga_interfaces|clocks_resets|h2f_user1_clk' | 9.578 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'hps_usb1_CLK' | 9.767 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'altera_reserved_tck' | 15.505 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'hps_i2c0_SCL' | 499.347 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'hps_i2c1_SCL' | 499.347 | 0.000 |
| Fast 1100mV -40C Model Setup 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk' | 2.113 | 0.000 |
| Fast 1100mV -40C Model Setup 'fpga_clk1_50' | 7.719 | 0.000 |
| Fast 1100mV -40C Model Setup 'altera_reserved_tck' | 9.343 | 0.000 |
| Fast 1100mV -40C Model Setup 'soc_inst|hps_0|fpga_interfaces|clocks_resets|h2f_user1_clk' | 19.531 | 0.000 |
| Fast 1100mV -40C Model Hold 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk' | 0.076 | 0.000 |
| Fast 1100mV -40C Model Hold 'fpga_clk1_50' | 0.151 | 0.000 |
| Fast 1100mV -40C Model Hold 'altera_reserved_tck' | 0.182 | 0.000 |
| Fast 1100mV -40C Model Hold 'soc_inst|hps_0|fpga_interfaces|clocks_resets|h2f_user1_clk' | 0.230 | 0.000 |
| Fast 1100mV -40C Model Recovery 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk' | 3.843 | 0.000 |
| Fast 1100mV -40C Model Recovery 'fpga_clk1_50' | 7.946 | 0.000 |
| Fast 1100mV -40C Model Recovery 'altera_reserved_tck' | 16.116 | 0.000 |
| Fast 1100mV -40C Model Removal 'altera_reserved_tck' | 0.309 | 0.000 |
| Fast 1100mV -40C Model Removal 'fpga_clk1_50' | 0.443 | 0.000 |
| Fast 1100mV -40C Model Removal 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk' | 0.463 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|pll_write_clk_dq_write_clk' | 0.887 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk' | 0.895 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'soc_inst|hps_0|fpga_interfaces|peripheral_i2c2|out_clk' | 4.515 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'fpga_clk1_50' | 8.423 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'soc_inst|hps_0|fpga_interfaces|clocks_resets|h2f_user1_clk' | 9.566 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'hps_usb1_CLK' | 9.690 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'altera_reserved_tck' | 15.480 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'hps_i2c0_SCL' | 499.274 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'hps_i2c1_SCL' | 499.274 | 0.000 |

- Worst setup slack: **1.573 ns** (Slow 1100mV -40C Model Setup 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk')
- Worst hold slack: **0.076 ns** (Fast 1100mV -40C Model Hold 'soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk')

## Fmax (`de10-nano-base.sta.rpt`, Fmax Summary panels)

| Model | Fmax | Restricted Fmax | Clock Name | Note |
|---|---|---|---|---|
| Slow 1100mV 100C Model Fmax Summary | 48.02 MHz | 48.02 MHz | altera_reserved_tck |  |
| Slow 1100mV 100C Model Fmax Summary | 94.71 MHz | 94.71 MHz | fpga_clk1_50 |  |
| Slow 1100mV 100C Model Fmax Summary | 980.39 MHz | 650.2 MHz | soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk | limit due to minimum period restriction (tmin) |
| Slow 1100mV 100C Model Fmax Summary | 984.25 MHz | 650.2 MHz | soc_inst|hps_0|fpga_interfaces|clocks_resets|h2f_user1_clk | limit due to minimum period restriction (tmin) |
| Slow 1100mV -40C Model Fmax Summary | 48.64 MHz | 48.64 MHz | altera_reserved_tck |  |
| Slow 1100mV -40C Model Fmax Summary | 92.73 MHz | 92.73 MHz | fpga_clk1_50 |  |
| Slow 1100mV -40C Model Fmax Summary | 968.05 MHz | 650.2 MHz | soc_inst|hps_0|fpga_interfaces|clocks_resets|h2f_user1_clk | limit due to minimum period restriction (tmin) |
| Slow 1100mV -40C Model Fmax Summary | 1007.05 MHz | 650.2 MHz | soc_system:soc_inst|soc_system_hps_0:hps_0|soc_system_hps_0_hps_io:hps_io|soc_system_hps_0_hps_io_border:border|hps_sdram:hps_sdram_inst|hps_sdram_pll:pll|afi_clk_write_clk | limit due to minimum period restriction (tmin) |

## Compile log message counts

- Critical warnings: 2
- Warnings: 255
- Errors: 0

Critical warnings must be triaged in writing (CLAUDE.md rule 10).

