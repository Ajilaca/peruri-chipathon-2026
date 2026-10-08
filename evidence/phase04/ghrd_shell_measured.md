<!-- claim-lint: skip-file (internal investigation record, not proposal text) -->
# Shell sistem DE10-Nano (Intel GHRD, tanpa inti NTT) - overhead fabric terukur

- Tanggal (UTC): 2026-10-01. Investigasi untuk peninjauan anggaran ALM 25% (ADR 0004); tidak ada ADR, RTL, atau hasil
  Fase 4 yang diubah. Bukan keputusan desain dan bukan sistem akhir.
- Label: MEASURED = dibaca dari laporan Quartus kompilasi ini; INFERENCE = kesimpulan yang ditarik dari angka
  terukur (jumlah, himpunan bagian), tidak dikompilasi seperti itu.

## 1. Sumber dan identitas
| Butir | Nilai |
|---|---|
| Desain | Intel DE10-Nano GHRD, <https://github.com/intel/de10-nano-hardware> (repository diarsipkan oleh Intel) |
| Commit | `9b5fc81654c61922b625607d007933a69b5fdb52` (commit yang dikutip di ADR 0006) |
| Revisi | `de10-nano-base` (sistem HPS + Platform Designer milik GHRD; tanpa inti NTT) |
| Alat | Quartus Prime Lite 25.1std.0 Build 1129 (GHRD ditulis untuk 17.1; tidak ada perubahan sumber yang diperlukan) |
| Device | 5CSEBA6U23I7 (diatur dengan `quartus_sh --set DEVICE=5CSEBA6U23I7`; bawaan GHRD `5CSEBA6U23I7DK` dikompilasi lebih dulu dan memberi angka fitter identik) |
| Hasil | Full Compilation berhasil, 0 error |
| Lokasi | Dibangun di luar repository ini (direktori scratch sesi); laporan mentah tidak di-commit |
| Ekstrak standar | `evidence/phase04/quartus_GHRD-de10-nano-base.md`, ditulis oleh `.claude/skills/quartus-report/scripts/extract_quartus_report.py` (ekstraktor proyek yang sudah ada, tidak berubah; ia hanya membaca laporan) |

Perintah:
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

## 2. Sumber daya (MEASURED, laporan fitter)
| Butir | Nilai |
|---|---|
| Pemakaian logika (ALM dibutuhkan, metrik sama dengan evidence C3) | 1,309 / 41,910 (3 %) |
| [A] ALM ditempatkan / [B] dapat dipulihkan dengan pengepakan rapat / [C] tidak tersedia | 1,601 / 303 / 11 |
| Combinational ALUT untuk logika | 2,187 |
| Total register | 2,381 |
| Blok RAM (M10K) | 35 / 553 (263,424 bit memori blok) |
| Bit memori MLAB | 0 |
| Blok DSP | 0 / 112 |
| Pin | 265 / 314 (pin nyata; kompilasi C3 memakai virtual pin) |
| PLL fabric / DLL / Hard Memory Controller | 0 / 6, 1 / 4, 1 / 1 (HPS DDR3) |
| Kesulitan pengepakan desain | Rendah |
| Pemakaian interkoneksi, rata-rata / puncak (total) | 1.7 % / 12.9 % |
| LAB terpakai sebagian atau penuh | 194 / 4,191 |

### Per entitas (MEASURED, "Fitter Resource Utilization by Entity"; ALM dibutuhkan)
| Blok | ALM | Comb. ALUTs | Register | M10K |
|---|---|---|---|---|
| HPS `hps_0` (termasuk `fpga_interfaces`, `hps_io`) | 0.0 | 0 | 0 | 0 |
| `mm_interconnect_0`: master AXI H2F HPS → `onchip_memory2_0` | 433.0 | 718 | 386 | 0 |
| `mm_interconnect_1`: master AXI LW H2F HPS → `lw_mm_bridge` | 274.7 | 467 | 297 | 1 |
| `mm_interconnect_2`: `lw_mm_bridge` → 11 slave Avalon (daftar di bawah) | 207.0 | 366 | 400 | 0 |
| `lw_mm_bridge` (bridge pipeline Avalon-MM) | 35.1 | 43 | 115 | 0 |
| PIO/GPIO, 8 blok: `arduino_gpio` 24.7, `button_pio` 6.3, `dipsw_pio` 6.7, `gpio_0_a` 40.8, `gpio_0_b` 36.7, `gpio_1_a` 36.2, `gpio_1_b` 38.2, `led_pio` 3.1 | 192.7 (≈ 193) | 293 | 540 | 0 |
| `jtag_uart` | 67.4 | 129 | 120 | 2 |
| `onchip_memory2_0` (memori demo 32 KB) | 0.0 | 0 | 0 | 32 |
| `altchip_id_0` | 10.0 | 19 | 144 | 0 |
| Reset: `rst_controller` 1.8, `_002` 0.2, `_003` 0.0, `_004` 0.0, `por` 1.5 | 3.5 | 11 | 43 | 0 |
| `sld_hub` (hub debug JTAG, di luar `soc_system`) | 61.5 | 96 | 78 | 0 |
| `debounce` (HDL level atas) | 23.4 | 44 | 32 | 0 |

Anak-anak `soc_system` berjumlah 1,223.4 ALM terhadap 1,223.3 milik fitter untuk `soc_system` (pembulatan).
`sysid_qsys` dan `chip_id_read_mm_0` tidak punya baris terpisah di tabel entitas.

Koreksi (2026-10-01): ringkasan chat sebelumnya mengatakan `mm_interconnect_2` melayani 12 slave; interkoneksi
yang dibangkitkan (`soc_system_mm_interconnect_2.v`) punya 11 translator slave. Angka 207 ALM tidak berubah.
Sebelas slave itu: 1 `arduino_gpio`, 2 `button_pio`, 3 `chip_id` (`chip_id_read_mm_0`), 4 `dipsw_pio`, 5 `gpio_0_a`,
6 `gpio_0_b`, 7 `gpio_1_a`, 8 `gpio_1_b`, 9 `jtag_uart`, 10 `led_pio`, 11 `sysid` (`sysid_qsys`).

## 3. Timing (MEASURED, Timing Analyzer; semua clock dibatasi SDC milik GHRD sendiri)
- Slack setup terburuk +1.573 ns (Slow 1100mV −40C, HPS SDRAM `afi_clk_write_clk`).
- Slack hold terburuk +0.076 ns (Fast 1100mV −40C, clock yang sama).
- Tidak ada slack negatif untuk setup, hold, recovery, removal, atau minimum pulse width di corner mana pun; 0 clock tanpa batasan.
- `fpga_clk1_50` (dibatasi pada 20 ns): Fmax 94.71 MHz (Slow 100C), 92.73 MHz (Slow −40C).
- Ini timing logika shell saja; tidak menyatakan apa pun tentang inti NTT atau desain gabungan.

## 4. Pesan (MEASURED)
- Peringatan kritis, 2, keduanya penempatan pin dan keduanya di luar lingkup pengukuran sumber daya:
  169085 (72 dari 265 pin tanpa lokasi pasti) dan 174073 (1 pin RUP/RDN/RZQ tanpa lokasi pasti).
- `qsys-script` mencetak "ERROR: Device family can not be determined" tiga kali saat menambah `altera_hps`; sistem
  tetap dibangkitkan (58 modul) dan dikompilasi. Tidak diselidiki lebih lanjut.

## 5. Perbandingan dengan inti Fase 4 (INFERENCE - jumlah dari kompilasi terpisah)
Kompilasi terpisah tidak menjumlah persis: dalam satu kompilasi gabungan fitter mengepak secara berbeda. Device = 41,910 ALM.
Angka C3: `evidence/phase04/seed_sweep.md` (seed 1–6).

| Kasus | ALM | % dari device | ALM tersisa | % tersisa |
|---|---|---|---|---|
| Shell dasar GHRD saja (MEASURED) | 1,309 | 3.12 % | 40,601 | 96.88 % |
| C3-P4 seed 1 + GHRD dasar | 11,748 | 28.03 % | 30,162 | 71.97 % |
| C3-P4 seed 1–6 + GHRD dasar | 11,748–11,812 | 28.03–28.18 % | 30,098–30,162 | 71.82–71.97 % |
| C3-P6 seed 1 + GHRD dasar | 11,814 | 28.19 % | 30,096 | 71.81 % |
| C3-P6 seed 1–6 + GHRD dasar | 11,793–11,825 | 28.14–28.22 % | 30,085–30,117 | 71.78–71.86 % |

Himpunan bagian LW-bridge (INFERENCE): HPS (0) + `mm_interconnect_1` (274.7) + `lw_mm_bridge` (35.1) + reset (3.5) ≈ 313 ALM
(0.75 %) dan 1 M10K, yaitu bagian shell ini yang paling sedikit dibutuhkan slave NTT di belakang lightweight bridge.
Ia tidak mencakup fan-out sisi slave (`mm_interconnect_2`, 207 ALM untuk 11 slave), yang biayanya untuk satu slave NTT
tidak diukur. Dengan himpunan bagian ini, C3-P4 / C3-P6 + shell ≈ 10,752–10,829 ALM (25.66–25.84 %). Tidak dikompilasi seperti itu.

M10K (INFERENCE, jumlah): C3-P4 26 + 35 = 61 / 553; C3-P6 29 + 35 = 64 / 553; 32 dari 35 milik shell adalah memori
on-chip demo. DSP: C3 9 + shell 0.

## 6. Apa yang ditunjukkan dan tidak ditunjukkan ini
- MEASURED: blok keras HPS tidak memakai ALM; biaya fabric shell adalah interkoneksi Platform Designer ditambah
  IP demo GHRD (PIO/GPIO, JTAG UART, memori on-chip).
- MEASURED: GHRD dasar lengkap memakai 3.12 % ALM, dengan kesulitan pengepakan dan pemakaian interkoneksi rendah, dan
  memenuhi timing.
- Tidak ditunjukkan: kompilasi gabungan (shell + inti NTT), biaya bridge yang benar-benar dipilih (PENDING #3), crossing
  domain clock antara clock inti dan clock bridge, overhead SignalTap, dan blok Fase 5–9.
