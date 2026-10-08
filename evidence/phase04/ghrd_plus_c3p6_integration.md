<!-- claim-lint: skip-file (internal investigation record, not proposal text) -->
# GHRD DE10-Nano + C3-P6 dalam satu kompilasi Quartus - eksperimen integrasi

Label: MEASURED = dibaca dari laporan Quartus kompilasi yang terdaftar di Bagian 2; INFERENCE = diturunkan dari
angka terukur (selisih, jumlah, interpretasi); NOT MEASURED = tidak diperoleh dalam eksperimen ini.
File ini menutup celah yang disebut di ADR 0009 ("P = 6 + GHRD tidak dikompilasi"). Ia mengulang
`ghrd_plus_c3p4_integration.md` dengan C3-P6, konfigurasi yang dipilih ADR 0009. Tidak ada RTL, ADR, atau
file evidence sebelumnya yang diubah.

## 1. Tujuan
Mengukur, dalam satu kompilasi, apa yang terjadi pada sumber daya dan timing ketika inti terpilih C3-P6 berbagi perangkat dengan
shell sistem HPS DE10-Nano, dan membandingkannya dengan kompilasi mandiri yang dibuat dengan setelan sama.

## 2. Revisi sumber dan kompilasi
| Kompilasi | Sumber | Setelan | Peran |
|---|---|---|---|
| C3-P6 (Fase 4) | repo `rtl/` (tidak berubah sejak Fase 4), `quartus/phase04_pipeline_c3/C3-P6.qsf`, `C3.sdc` | bawaan Quartus | evidence yang ada `quartus_C3-P6.md` |
| C3-P6-ghrdset | RTL, SDC, virtual pin, dan seed bawaan sama dengan C3-P6, ditambah 5 setelan global QSF GHRD (Bagian 4) | setelan GHRD | inti mandiri dengan setelan sama dengan kompilasi gabungan |
| GHRD base (build baru) | Intel DE10-Nano GHRD, `github.com/intel/de10-nano-hardware` commit `9b5fc81654c61922b625607d007933a69b5fdb52`, revisi `de10-nano-base`, sistem Platform Designer terbangkit sama dengan proyek gabungan | setelan GHRD | shell mandiri |
| Gabungan `de10-nano-c3p6` | proyek GHRD base (disalin) + RTL C3-P6 dirujuk read-only dari repo | setelan GHRD | integrasi |

Semuanya: device 5CSEBA6U23I7, Quartus Prime Lite 25.1std.0 Build 1129, seed fitter bawaan, Full Compilation
berhasil dengan 0 error (MEASURED). Waktu berlalu: gabungan 15 min 03 s, C3-P6-ghrdset 12 min 23 s, GHRD base 8 min 32 s.
File eksperimen berada di luar repository di folder eksperimen tim (klon GHRD, proyek gabungan,
proyek mandiri, `metrics.py`, skrip kompilasi berurutan).

Catatan proses (dinyatakan apa adanya). Run pertama kompilasi GHRD base dilewati oleh smart recompilation Quartus
(log: "Smart recompilation skipped module Fitter because it is not required", 5 s); laporannya adalah milik build sebelumnya.
Run itu tidak dipakai. Database lama dipindahkan dan kompilasi diulang penuh (log tanpa baris
"skipped", 8 min 32 s, fitter selesai pukul 14:48 waktu lokal). Build baru memberi angka sama dengan yang sebelumnya
(1,304 ALM, 2,369 register, 35 M10K).

## 3. Topologi integrasi
Sama seperti eksperimen C3-P4: `top_c3p6.v` = `hdl_src/top.v` GHRD dengan 11 port `ntt_*` yang sama (semuanya virtual pin,
clock sendiri `ntt_clk_i`) dan satu instans `ntt_core_c3_p6`; SDC = `create_clock -name ntt_clk_i -period 40.000`,
`derive_clock_uncertainty`, false path dari `ntt_rst_ni`, isi identik dengan `quartus/phase04_pipeline_c3/C3.sdc`
(diperiksa: `C3.sdc` proyek mandiri identik byte demi byte dengan milik repo). Daftar file RTL adalah milik
`C3-P6.qsf`. NTT tidak tersambung ke HPS, bridge apa pun, atau sinyal GHRD apa pun; tidak ada crossing domain clock
(PENDING #3).

## 4. Setelan kompilasi (pengacau ditangani seperti di eksperimen P4)
Setelan global GHRD berlaku untuk seluruh proyek, inti termasuk: `OPTIMIZATION_MODE "AGGRESSIVE PERFORMANCE"`,
`PHYSICAL_SYNTHESIS_COMBO_LOGIC_FOR_AREA ON`, `PHYSICAL_SYNTHESIS_REGISTER_DUPLICATION ON`,
`BLOCK_RAM_TO_MLAB_CELL_CONVERSION OFF`, `OPTIMIZE_MULTI_CORNER_TIMING ON`. Kompilasi mandiri C3-P6-ghrdset
memisahkan efek setelan dari efek integrasi.

## 5. Perintah persis
```bash
. scripts/env.sh; export PATH=$QUARTUS_ROOTDIR/sopc_builder/bin:$PATH
cd <experiments>/ghrd/de10-nano-c3p6   && quartus_sh --flow compile de10-nano-c3p6 -c de10-nano-c3p6        # combined
cd <experiments>/c3p6_ghrd_settings    && quartus_sh --flow compile C3-P6-ghrdset -c C3-P6-ghrdset          # standalone, GHRD settings
cd <experiments>/ghrd/de10-nano-base   && quartus_sh --flow compile de10-nano-base.qpf -c de10-nano-base    # after moving db/ and output_files/ aside
python3 <experiments>/metrics.py <output_files> <revision> [entity ...]                                     # read-only extraction
```
Ketiga kompilasi berjalan satu per satu (run paralel merusak `.qpf` bersama).

## 6. Sumber daya terukur (MEASURED)
| Metrik | C3-P6 (Fase 4, bawaan) | C3-P6-ghrdset | GHRD base (baru) | Gabungan |
|---|---:|---:|---:|---:|
| ALM dibutuhkan | 10,505 | 11,053 | 1,304 | 12,375 (30 %) |
| [A] ditempatkan | - | 11,998 | 1,588 | 13,468 |
| [B] dapat dipulihkan dengan pengepakan rapat | - | 1,197 | 294 | 1,338 |
| [C] tidak tersedia | - | 252 | 10 | 245 |
| Combinational ALUT untuk logika | - | 17,656 | 2,187 | 19,819 |
| Total register | 4,168 | 4,790 | 2,369 | 6,876 |
| M10K | 29 / 553 | 28 / 553 | 35 / 553 | 62 / 553 |
| DSP | 9 / 112 | 9 / 112 | 0 / 112 | 9 / 112 |
| PLL fabric / DLL | 0 / 0 | 0 / 0 | 0 / 1 | 0 / 1 |
| LAB terpakai | - | 1,363 | 208 | 1,580 |
| Kesulitan pengepakan desain | - | Rendah | Rendah | Rendah |
| Interkoneksi rata-rata (total) | - | 11.9 % | 1.6 % | 10.9 % |
| Interkoneksi puncak (total) | - | 51.8 % | 11.6 % | 37.0 % |
| Estimasi router rata-rata / puncak | - | 10 % / 44 % | 1 % / 10 % | 9 % / 33 % |

"-" = tidak diekstrak untuk file evidence Fase 4 (lihat `quartus_C3-P6.md` untuk isinya).
Per entitas pada kompilasi gabungan (MEASURED): `ntt_core_c3_p6` 11,050.0 ALM, 17,604 ALUT, 4,490 register, 27 M10K,
9 DSP; `soc_system` 1,219.3 ALM, 35 M10K; `sld_hub` 61.5; `debounce` 23.7. GHRD mandiri: `soc_system` 1,217.8 ALM.

## 7. Timing terukur (MEASURED; terburuk atas corner yang dicetak)
| Clock | C3-P6 (Fase 4) | C3-P6-ghrdset | GHRD base (baru) | Gabungan |
|---|---|---|---|---|
| Clock NTT (`clk_i` / `ntt_clk_i`, 40.000 ns): setup / hold | +10.753 / +0.140 | +16.017 / +0.152 | - | +11.364 / +0.129 |
| Fmax NTT, Slow 100C / Slow −40C (MHz) | 34.19 / 34.5 | 41.74 / 41.7 | - | 34.92 / 35.58 |
| `fpga_clk1_50` (20 ns): setup / hold | - | - | +6.102 / +0.135 | +6.358 / +0.143 |
| `fpga_clk1_50` Fmax, Slow 100C / −40C (MHz) | - | - | 85.06 / 87.33 | 77.35 / 78.29 |
| HPS SDRAM `afi_clk_write_clk`: setup / hold | - | - | +1.573 / +0.076 | +1.573 / +0.076 |
| `h2f_user1_clk`: setup / hold | - | - | +18.629 / +0.247 | +18.919 / +0.229 |
| `altera_reserved_tck` (JTAG): setup / hold | - | - | +6.255 / +0.107 | +6.255 / +0.120 |
| Setup / hold terburuk sistem | - | - | +1.573 / +0.076 | +1.573 / +0.076 (keduanya pada `afi_clk_write_clk`) |

- Gabungan: tidak ada slack setup, hold, recovery, atau removal negatif pada clock mana pun (MEASURED). Domain NTT memenuhi 40.000 ns
  dan domain shell tetap memenuhi batasan GHRD-nya.
- Fmax NTT hanyalah baris `ntt_clk_i`. Fmax NTT slow corner terendah: gabungan 34.92 MHz; C3-P6-ghrdset 41.70 MHz;
  C3-P6 Fase 4 34.19 MHz.
- Slack setup pada kolom "C3-P6 (Fase 4)" adalah pada Slow 100C dan hold pada Fast −40C, seperti di `quartus_C3-P6.md`;
  kolom lain memakai minimum atas setiap corner yang dicetak `metrics.py`, jadi perbandingannya indikatif.
- Jalur setup terburuk sistem berada di clock SDRAM HPS pada kompilasi mandiri dan gabungan; node jalurnya
  NOT MEASURED (tidak ada laporan jalur yang dibangkitkan).
- Peringatan kritis (MEASURED): gabungan 15725 (virtual pin `ntt_clk_i`, seperti di setiap kompilasi Fase 4), 169085 dan 174073
  (penempatan pin GHRD, juga di GHRD mandiri); C3-P6-ghrdset hanya 15725; GHRD base 169085 dan 174073. Tidak ada 332148.

## 8. Selisih integrasi
`integration_delta = combined − P6_standalone − GHRD_standalone` (INFERENCE, aritmetika pada nilai MEASURED):

| Baseline untuk inti | Rumus | Selisih |
|---|---|---|
| C3-P6-ghrdset (setelan sama dengan gabungan) | 12,375 − 11,053 − 1,304 | +18 ALM |
| C3-P6 Fase 4 (setelan bawaan) | 12,375 − 10,505 − 1,304 | +566 ALM |
| di antaranya: efek setelan pada inti saja | 11,053 − 10,505 | +548 ALM |

Selisih lain terhadap C3-P6-ghrdset + GHRD (INFERENCE): ALUT −24; register −283; M10K −1; [A] ditempatkan −118;
[B] dapat dipulihkan −153; [C] tidak tersedia −17; LAB +9.

Pembacaan (INFERENCE):
- Dengan setelan konsisten, kompilasi bersama mengubah "ALM dibutuhkan" sebesar +18 (0.04 % dari perangkat), nilai yang sama dengan
  eksperimen C3-P4. Hitungan ALM inti sendiri di kompilasi gabungan (11,050.0) dalam 3 ALM dari hitungan mandirinya
  dengan setelan yang sama (11,053). Tidak ada penalti pengepakan terukur pada metrik yang dipakai anggaran.
- Setelan GHRD menambah +548 ALM pada C3-P6 (+993 pada C3-P4). Efek setelan karenanya bukan jumlah tetap; ia
  diukur di sini untuk satu seed per revisi dan tidak digeneralisasi.
- Terhadap eksperimen C3-P4: gabungan 12,375 (P6) lawan 12,754 (P4), 379 lebih rendah; C3-P6-ghrdset 11,053 lawan C3-P4-ghrdset
  11,432, juga 379 lebih rendah. Di bawah setelan GHRD pipeline yang lebih dalam keluar lebih kecil; di bawah bawaan Quartus ia
  lebih besar (10,505 lawan 10,439). Satu kompilasi per revisi pada satu seed; penyebabnya tidak ditetapkan.
- Timing: clock NTT memenuhi 40.000 ns pada kompilasi gabungan; setup +11.364 ns. Fmax NTT 34.92 MHz gabungan lawan
  41.74 MHz mandiri dengan setelan sama. Sapuan seed Fase 4 menunjukkan sebaran Fmax sampai sekitar 5 % antar seed
  pada setelan bawaan; selisih 16 % tidak diuji ketergantungan seed-nya, jadi tidak dikaitkan dengan integrasi.
- Indikator kongesti: kesulitan pengepakan Rendah, interkoneksi rata-rata 10.9 %, puncak 37.0 % (INFERENCE: tidak ada kongesti).

## 9. Angka anggaran (diminta; tidak ada lulus/gagal yang ditarik)
| Butir | Nilai |
|---|---|
| ALM gabungan dibutuhkan | 12,375 (MEASURED) |
| % perangkat gabungan | 29.53 % (INFERENCE: 12,375 / 41,910) |
| Gabungan lawan 12,573 | 198 ALM di bawah (INFERENCE) |
| Margin ke 41,910 (perangkat) | 29,535 ALM, 70.47 % (INFERENCE) |
| Inti sendirian, setelan GHRD (C3-P6-ghrdset) | 11,053 ALM = 26.37 % (INFERENCE) |

ADR 0009 mendefinisikan 12,573 sebagai anggaran desain untuk inti NTT, bukan untuk inti + shell, jadi total gabungan bukan
pemeriksaan terhadapnya. Perbandingan dengan 12,573 di atas hanya aritmetika, sesuai permintaan. Keccak, sampler, pengendali,
penyimpanan, bridge, dan SignalTap tidak ada di kompilasi ini.

## 10. Keterbatasan
- NOT MEASURED: koneksi HPS ↔ NTT nyata (bridge, CSR, DMA), crossing domain clock apa pun, clock NTT yang diturunkan
  dari clock papan atau PLL, SignalTap, seed lain kompilasi gabungan, kompilasi gabungan dengan bawaan Quartus,
  run papan apa pun.
- NTT berjalan pada clock virtual-pin sendiri; 40.000 ns terpenuhi berarti jalur internal inti memenuhi 40 ns di samping
  shell, bukan bahwa clock 25 MHz ada di papan. 50 MHz (20 ns) tidak dicoba di sini.
- Satu kompilasi per konfigurasi pada seed bawaan (Fase 4: 32–64 ALM dan Fmax 4.8–7.5 % antar seed).
- GHRD base memberi 1,304 ALM pada kedua build yang dibuat setelah sistem dibangkitkan ulang (build pagi sebelumnya memberi
  1,309; penyebab tidak ditetapkan, lihat `ghrd_plus_c3p4_integration.md` Bagian 10).

## 11. Kesimpulan
- MEASURED: GHRD + C3-P6 muat dan terkompilasi bersama di 5CSEBA6U23I7 dengan 12,375 ALM (30 %), 62 M10K, dan 9 DSP; setiap
  clock memenuhi batasannya, termasuk clock NTT pada 40.000 ns (setup +11.364 ns, Fmax 34.92 MHz).
- INFERENCE: integrasi sendiri memakan sekitar +18 ALM, sama seperti untuk C3-P4. Selisih 566 ALM antara angka inti Fase 4
  dan angka gabungan didominasi oleh setelan optimasi GHRD (+548 ALM pada inti).
- Celah evidence Fase 4 (P6 + GHRD tidak dikompilasi) ditutup untuk sumber daya dan timing inti yang tidak tersambung.
