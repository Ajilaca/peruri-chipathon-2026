<!-- claim-lint: skip-file (internal investigation record, not proposal text) -->
# GHRD DE10-Nano + C3-P4 dalam satu kompilasi Quartus - eksperimen integrasi

Label: MEASURED = dibaca dari laporan Quartus kompilasi yang terdaftar di Bagian 2; INFERENCE = diturunkan dari
angka terukur (selisih, jumlah, interpretasi); NOT MEASURED = tidak diperoleh dalam eksperimen ini.

## 1. Tujuan
Mengukur, dalam satu kompilasi, apa yang terjadi pada sumber daya dan timing ketika inti Fase 4 C3-P4 berbagi perangkat
dengan shell sistem HPS DE10-Nano, dan membandingkannya dengan dua kompilasi mandiri. C3-P4 dipakai sebagai baseline
integrasi saja. Eksperimen ini tidak memilih P, tidak mengubah ADR 0004 / 0007 / 0008, dan tidak
mengubah RTL apa pun. (Arahan tim yang dinyatakan bersama permintaan: L = 8, P6, anggaran desain 30%; tidak ditindaklanjuti di sini.)

## 2. Revisi sumber dan kompilasi
| Kompilasi | Sumber | Setelan | Peran |
|---|---|---|---|
| C3-P4 (Fase 4) | repo `rtl/` pada `a803386`, `quartus/phase04_pipeline_c3/C3-P4.qsf`, `C3.sdc` | bawaan Quartus | evidence yang ada `quartus_C3-P4.md` |
| C3-P4-ghrdset | RTL, QSF, SDC, dan virtual pin sama dengan C3-P4, ditambah 5 setelan optimasi global QSF GHRD (Bagian 4) | setelan GHRD | inti mandiri dengan setelan yang sama dengan kompilasi gabungan |
| GHRD base (hari ini) | Intel DE10-Nano GHRD, `github.com/intel/de10-nano-hardware` commit `9b5fc81654c61922b625607d007933a69b5fdb52`, revisi `de10-nano-base`, sistem Platform Designer dibangkitkan hari ini | setelan GHRD | shell mandiri, sistem yang dibangkitkan sama dengan kompilasi gabungan |
| Gabungan `de10-nano-c3p4` | proyek GHRD base di atas (disalin) + RTL C3-P4 dirujuk read-only dari repo | setelan GHRD | integrasi |

Keempatnya: device 5CSEBA6U23I7, Quartus Prime Lite 25.1std.0 Build 1129, seed fitter bawaan, Full Compilation
berhasil dengan 0 error (MEASURED). File eksperimen berada di luar repository di
`~/FPGA/Projects/CHIPATON_experiments/` (klon GHRD, proyek gabungan, proyek C3-P4-ghrdset, `metrics.py`).

## 3. Topologi integrasi
- `top_c3p4.v` = `hdl_src/top.v` GHRD dengan hanya dua tambahan: 11 port tingkat atas baru `ntt_*` dan satu instans
  `ntt_core_c3_p4 u_ntt_c3p4` yang tersambung ke port itu. `top.v` asli, file SDC GHRD, dan sistem Platform Designer
  tidak berubah.
- Semua port `ntt_*`, termasuk `ntt_clk_i`, adalah virtual pin, persis seperti kompilasi Fase 4 mandiri.
  NTT punya clock sendiri `ntt_clk_i` dengan batasan Fase 4 (`c3p4_virtual.sdc` =
  `create_clock -name ntt_clk_i -period 40.000`, `derive_clock_uncertainty`, false path dari `ntt_rst_ni`), jadi
  batasan 40.000 ns diterapkan dengan cara yang sama seperti di Fase 4.
- NTT tidak tersambung ke HPS, bridge apa pun, atau sinyal GHRD apa pun. Tidak ada crossing domain clock. Menyambungkannya
  butuh keputusan antarmuka/bridge/CDC (PENDING #3), yang tidak dibuat eksperimen ini.
- QSF gabungan = QSF GHRD dengan `DEVICE` diatur ke 5CSEBA6U23I7, `top.v` diganti `top_c3p4.v`, dan daftar RTL C3-P4
  (identik dengan `C3-P4.qsf`), file SDC NTT, dan assignment virtual pin ditambahkan.

## 4. Pengacau ditemukan sebelum kompilasi: setelan global GHRD
QSF GHRD berisi setelan yang berlaku untuk seluruh proyek, NTT termasuk; kompilasi Fase 4 memakai bawaan:
`OPTIMIZATION_MODE "AGGRESSIVE PERFORMANCE"`, `PHYSICAL_SYNTHESIS_COMBO_LOGIC_FOR_AREA ON`,
`PHYSICAL_SYNTHESIS_REGISTER_DUPLICATION ON`, `BLOCK_RAM_TO_MLAB_CELL_CONVERSION OFF`,
`OPTIMIZE_MULTI_CORNER_TIMING ON`. Tidak ada yang diubah di proyek gabungan; sebagai gantinya kompilasi tambahan
C3-P4-ghrdset (lima setelan sama, tidak ada yang lain berubah) memisahkan efek setelan dari efek integrasi.

## 5. Perintah persis
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

## 6. Sumber daya terukur (MEASURED)
| Metrik | C3-P4 (Fase 4, bawaan) | C3-P4-ghrdset | GHRD base (hari ini) | Gabungan |
|---|---:|---:|---:|---:|
| ALM dibutuhkan | 10,439 | 11,432 | 1,304 | 12,754 (30 %) |
| [A] ditempatkan | 10,695 | 12,183 | 1,588 | 13,991 |
| [B] dapat dipulihkan dengan pengepakan rapat | 388 | 990 | 294 | 1,452 |
| [C] tidak tersedia | 132 | 239 | 10 | 215 |
| Combinational ALUT untuk logika | 13,047 | 17,735 | 2,187 | 19,938 |
| Total register | 4,145 | 4,320 | 2,369 | 6,530 |
| M10K | 26 / 553 | 26 / 553 | 35 / 553 | 60 / 553 |
| Bit memori MLAB | 0 | 0 | 0 | 0 |
| DSP | 9 / 112 | 9 / 112 | 0 / 112 | 9 / 112 |
| PLL fabric / DLL | 0 / 0 | 0 / 0 | 0 / 1 | 0 / 1 |
| LAB terpakai | 1,309 | 1,403 | 208 | 1,645 |
| Kesulitan pengepakan desain | Rendah | Rendah | Rendah | Rendah |
| Interkoneksi rata-rata (total) | 12.4 % | 13.6 % | 1.6 % | 13.8 % |
| Interkoneksi puncak (total) | 55.2 % | 52.7 % | 11.6 % | 48.2 % |
| Estimasi router rata-rata / puncak | 11 % / 49 % | n/a | n/a | 12 % / 45 % |

Per entitas pada kompilasi gabungan (MEASURED): `ntt_core_c3_p4` 11,432.5 ALM, 17,728 ALUT, 4,173 register, 25 M10K,
9 DSP; `soc_system` 1,216.2 ALM, 35 M10K; `sld_hub` 61.5; `debounce` 23.3. GHRD mandiri hari ini: `soc_system`
1,217.8 ALM.

## 7. Timing terukur (MEASURED; terburuk atas corner yang dicetak)
| Clock | C3-P4 (Fase 4) | C3-P4-ghrdset | GHRD base (hari ini) | Gabungan |
|---|---|---|---|---|
| Clock NTT (`clk_i` / `ntt_clk_i`, 40.000 ns): setup / hold | +8.734 / +0.157 | +10.885 / +0.123 | - | +9.204 / +0.149 |
| Fmax NTT, Slow 100C / Slow −40C (MHz) | 32.60 / 31.98 | 34.35 / 34.66 | - | 32.70 / 32.47 |
| `fpga_clk1_50` (20 ns): setup / hold | - | - | +6.102 / +0.135 | +6.890 / +0.126 |
| `fpga_clk1_50` Fmax, Slow 100C / −40C (MHz) | - | - | 85.06 / 87.33 | 84.93 / 88.53 |
| HPS SDRAM `afi_clk_write_clk`: setup / hold | - | - | +1.573 / +0.076 | +1.573 / +0.076 |
| `h2f_user1_clk`: setup / hold | - | - | +18.629 / +0.247 | +18.963 / +0.234 |
| Setup / hold terburuk sistem | - | - | +1.573 / +0.076 | +1.573 / +0.076 (keduanya pada `afi_clk_write_clk`) |

- Gabungan: tidak ada slack setup, hold, recovery, atau removal negatif pada clock mana pun (MEASURED). Domain NTT memenuhi 40.000 ns
  dan domain shell tetap memenuhi batasan GHRD-nya.
- Fmax NTT hanyalah baris `ntt_clk_i`; Fmax shell tidak dipakai untuk NTT.
- Jalur setup terburuk sistem berada di clock SDRAM HPS pada kompilasi mandiri maupun gabungan; node
  jalurnya NOT MEASURED (tidak ada laporan jalur yang dibangkitkan).
- Peringatan kritis, gabungan (MEASURED): 15725 (`ntt_clk_i` adalah virtual pin, seperti di setiap kompilasi Fase 4), 169085
  dan 174073 (penempatan pin GHRD, seperti di GHRD mandiri).

## 8. Selisih integrasi
`integration_delta = combined_ALM − P4_standalone_ALM − GHRD_standalone_ALM` (INFERENCE, aritmetika pada nilai MEASURED):

| Baseline untuk inti | Rumus | Selisih |
|---|---|---|
| C3-P4-ghrdset (setelan sama dengan gabungan) | 12,754 − 11,432 − 1,304 | +18 ALM |
| C3-P4 Fase 4 (setelan bawaan) | 12,754 − 10,439 − 1,304 | +1,011 ALM |
| di antaranya: efek setelan pada inti saja | 11,432 − 10,439 | +993 ALM |

Selisih lain terhadap C3-P4-ghrdset + GHRD (INFERENCE): ALUT +16; register −159; M10K −1 (inti memakai 25 M10K
pada kompilasi gabungan, 26 mandiri); [A] ditempatkan +220; [B] dapat dipulihkan +168; [C] tidak tersedia −34; LAB +34.

Pembacaan (INFERENCE):
- Dengan setelan konsisten, menaruh shell dan inti dalam satu kompilasi mengubah "ALM dibutuhkan" sebesar +18 (0.04 % dari
  perangkat). Hitungan ALM inti sendiri di dalam kompilasi gabungan (11,432.5) sama dengan hitungan mandirinya dengan setelan
  yang sama (11,432). Tidak ada penalti atau keuntungan pengepakan terukur pada metrik yang dipakai anggaran.
- Selisih ~+1,000 ALM antara angka Fase 4 dan angka gabungan berasal dari setelan optimasi global GHRD
  (aggressive performance, physical synthesis dengan duplikasi register), bukan dari integrasi.
- Timing: dengan setelan sama, slack setup NTT terburuk inti adalah +10.885 ns mandiri dan +9.204 ns gabungan
  (Fmax 34.35 → 32.47 MHz pada slow corner terendah, −5.5 %). Ini satu kompilasi masing-masing pada satu seed; sapuan seed Fase 4
  menunjukkan sebaran Fmax 4.8–7.5 % antar seed, jadi selisih ini tidak ditunjukkan sebagai efek integrasi.
- [A] ditempatkan naik 220 sementara "dibutuhkan" naik 18: fitter menyebar logika lebih longgar saat ada ruang
  ([B] dapat dipulihkan naik 168). Ini estimasi pengepakan yang berperilaku seperti pada utilisasi rendah; bukan kongesti.

## 9. Angka anggaran (diminta; tidak ada pemilihan dari angka ini)
| Butir | Nilai |
|---|---|
| ALM gabungan dibutuhkan | 12,754 (MEASURED) |
| % perangkat gabungan | 30.43 % (INFERENCE: 12,754 / 41,910) |
| Margin ke 12,573 (30 %) | −181 ALM (lebih 181) (INFERENCE) |
| Margin ke 41,910 (perangkat) | 29,156 ALM, 69.57 % (INFERENCE) |

Lingkup anggaran 30 % (inti NTT saja, atau inti + shell) tidak didefinisikan di ADR mana pun; file ini melaporkan angkanya
terhadap seluruh desain gabungan sesuai permintaan dan tidak menarik kesimpulan darinya. Dengan setelan GHRD inti sendirian
memakai 11,432 ALM (27.3 %).

*Pembaruan 2026-10-01 (setelah eksperimen ini):* ADR 0009 mendefinisikan angka 30 % / 12,573 ALM sebagai anggaran desain
inti NTT (Fase 4), bukan untuk inti + shell. Total gabungan di atas karenanya bukan pemeriksaan terhadap anggaran itu. Tidak ada
pengukuran di file ini yang diubah.

## 10. Keterbatasan
- NOT MEASURED: koneksi HPS ↔ NTT nyata (bridge, CSR, DMA), crossing domain clock apa pun, clock NTT yang diturunkan
  dari clock papan atau PLL, SignalTap, P6 atau P selain 4, seed lain kompilasi gabungan.
- NTT berjalan pada clock virtual-pin sendiri; hasil 40.000 ns berkata jalur internal inti memenuhi 40 ns di samping
  shell, bukan bahwa clock 25 MHz ada di papan.
- Satu kompilasi per konfigurasi, seed bawaan. Fase 4 menunjukkan sebaran antar seed 32–64 ALM dan Fmax 4.8–7.5 %.
- Catatan reproduksibilitas (MEASURED): commit GHRD, alat, seed, dan setelan device yang sama memberi 1,309 ALM / 2,381
  register pada pagi 2026-10-01 (`ghrd_shell_measured.md`) dan 1,304 / 2,369 setelah membangkitkan ulang
  sistem Platform Designer dalam eksperimen ini. Penyebab tidak ditetapkan (INFERENCE: konstanta yang bergantung generasi seperti
  timestamp `sysid`). Selisih di atas memakai build yang sistem terbangkitnya disalin proyek gabungan.
- Kompilasi gabungan memakai setelan GHRD untuk seluruh desain; kompilasi gabungan dengan bawaan Quartus tidak
  dijalankan (NOT MEASURED).

## 11. Kesimpulan
- MEASURED: GHRD + C3-P4 muat dan terkompilasi bersama di 5CSEBA6U23I7 dengan 12,754 ALM (30 %), 60 M10K, dan 9 DSP; setiap
  clock memenuhi batasannya, termasuk clock NTT pada 40.000 ns (setup terburuk +9.204 ns, Fmax 32.47 MHz).
- INFERENCE: integrasi sendiri memakan sekitar +18 ALM. Selisih dari angka Fase 4 didominasi oleh setelan
  optimasi GHRD (+993 ALM pada inti), yang berarti setelan kompilasi untuk build sistem adalah keputusan yang relevan bagi anggaran
  tersendiri.
- INFERENCE: tidak ada indikator kongesti yang bergeser berarti (kesulitan pengepakan Rendah, interkoneksi rata-rata 13.8 %, puncak
  48.2 %).
