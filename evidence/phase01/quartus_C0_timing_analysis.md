# MEASURED - Analisis timing Quartus C0 (baseline Fase 1, BUKAN hasil optimasi)

- Dibangkitkan: 2026-09-29 UTC oleh `quartus/phase01_ntt_c0/extract_c0_timing_evidence.py` (nilai disalin dari teks laporan Quartus; angka turunan menyatakan cara penurunannya).
- Kompilasi: Quartus Prime Lite 25.1std, revisi `C0`, top `ntt_core`, device 5CSEBA6U23I7, clock sementara `create_clock -period 20.000` pada virtual pin `clk_i` (`quartus/phase01_ntt_c0/C0.sdc`).
- Pendalaman: `quartus_sta -t quartus/phase01_ntt_c0/report_critical_paths.tcl` pada netlist pasca-fit yang ada (hanya baca: tanpa kompilasi ulang, RTL/QSF/SDC tidak berubah), corner Slow 1100mV 100C.
- Lihat juga ekstrak ringkasan fitter/STA `evidence/quartus/C0.md`.

## 1. Apakah setiap tahap selesai?

| Tahap | Pesan Quartus (kata demi kata) |
|---|---|
| Analysis & Synthesis | Quartus Prime Analysis & Synthesis was successful. 0 errors, 8 warnings |
| Fitter | Quartus Prime Fitter was successful. 0 errors, 2 warnings |
| Assembler | Quartus Prime Assembler was successful. 0 errors, 1 warning |
| Timing Analyzer | Quartus Prime Timing Analyzer was successful. 0 errors, 5 warnings |

Keempat tahap selesai tanpa error. Selesai tidak sama dengan memenuhi timing: Timing Analyzer menaikkan `Critical Warning (332148): Timing requirements not met` sebanyak 4 kali (sekali per corner yang dianalisis).

## 2. Sumber daya dan timing terukur

| Besaran | Nilai (kata demi kata) | Sumber |
|---|---|---|
| Logic utilization (in ALMs) | 7,010 / 41,910 ( 17 % ) | `C0.fit.summary` |
| Total registers | 3104 | `C0.fit.summary` |
| Total block memory bits | 0 / 5,662,720 ( 0 % ) | `C0.fit.summary` |
| Total RAM Blocks | 0 / 553 ( 0 % ) | `C0.fit.summary` |
| Total DSP Blocks | 3 / 112 ( 3 % ) | `C0.fit.summary` |
| Total virtual pins | 39 | `C0.fit.summary` |
| Fmax, Slow 1100mV 100C Model | 14.64 MHz (restricted 14.64 MHz, clock clk_i) | `C0.sta.rpt` |
| Fmax, Slow 1100mV -40C Model | 14.69 MHz (restricted 14.69 MHz, clock clk_i) | `C0.sta.rpt` |

| Corner / check | Slack (ns) | TNS (ns) |
|---|---|---|
| Slow 1100mV 100C Model Setup 'clk_i' | -48.323 | -143688.194 |
| Slow 1100mV 100C Model Hold 'clk_i' | 0.531 | 0.000 |
| Slow 1100mV 100C Model Minimum Pulse Width 'clk_i' | 9.255 | 0.000 |
| Slow 1100mV -40C Model Setup 'clk_i' | -48.059 | -143216.393 |
| Slow 1100mV -40C Model Hold 'clk_i' | 0.562 | 0.000 |
| Slow 1100mV -40C Model Minimum Pulse Width 'clk_i' | 9.149 | 0.000 |
| Fast 1100mV 100C Model Setup 'clk_i' | -17.039 | -49249.473 |
| Fast 1100mV 100C Model Hold 'clk_i' | 0.230 | 0.000 |
| Fast 1100mV 100C Model Minimum Pulse Width 'clk_i' | 9.566 | 0.000 |
| Fast 1100mV -40C Model Setup 'clk_i' | -11.893 | -34032.465 |
| Fast 1100mV -40C Model Hold 'clk_i' | 0.211 | 0.000 |
| Fast 1100mV -40C Model Minimum Pulse Width 'clk_i' | 9.557 | 0.000 |

- Slack setup terburuk: -48.323 ns (keempat corner negatif) -> timing TIDAK terpenuhi pada periode sementara 20.000 ns.
- Slack hold terburuk: 0.211 ns (positif di semua corner -> hold terpenuhi).
- TNS setup terburuk: -143688.194 ns.
- Pemeriksaan silang (turunan): 1 / (20.000 ns + 48.323 ns) = 14.64 MHz, sama dengan panel Fmax.

## 3. Apa yang dibangun sintesis (menjelaskan jalurnya)

Pesan Analysis & Synthesis (kata demi kata):

```
Info (276004): RAM logic "twiddle_rom:u_rom|rom_zeta" is uninferred due to inappropriate RAM size File: /home/ajil/FPGA/Projects/CHIPATON/rtl/ntt/twiddle_rom.sv Line: 19
Info (278004): Inferred divider/modulo megafunction ("lpm_divide") from the following logic: "butterfly:u_bfly|modmul_reduce:u_inv_mul|Mod0" File: /home/ajil/FPGA/Projects/CHIPATON/rtl/ntt/modmul_reduce.sv Line: 26
Info (278004): Inferred divider/modulo megafunction ("lpm_divide") from the following logic: "modmul_reduce:u_scale_mul|Mod0" File: /home/ajil/FPGA/Projects/CHIPATON/rtl/ntt/modmul_reduce.sv Line: 26
Info (278004): Inferred divider/modulo megafunction ("lpm_divide") from the following logic: "butterfly:u_bfly|modmul_reduce:u_fwd_mul|Mod0" File: /home/ajil/FPGA/Projects/CHIPATON/rtl/ntt/modmul_reduce.sv Line: 26
Info (12134): Parameter "LPM_WIDTHN" = "24"
Info (12134): Parameter "LPM_WIDTHD" = "12"
```

Penggunaan DSP fitter (baris kata demi kata, dipotong setelah kolom penempatan):

```
; butterfly:u_bfly|modmul_reduce:u_inv_mul|Mult0~mac ; Two Independent 18x18 ; DSP_X20_Y4_N0 ;
; modmul_reduce:u_scale_mul|Mult0~mac                ; Two Independent 18x18 ; DSP_X86_Y2_N0 ;
; butterfly:u_bfly|modmul_reduce:u_fwd_mul|Mult0~mac ; Two Independent 18x18 ; DSP_X20_Y6_N0 ;
```

Fitter Resource Utilization by Entity (ALM dibutuhkan / ALUT kombinasional / register khusus):

| Node hierarki | ALM dibutuhkan | Comb. ALUT | Register |
|---|---|---|---|
| `|ntt_core` | 7010.0 (155.3) | 4144 (201) | 3104 (32) |
| `|butterfly:u_bfly|` | 463.8 (76.6) | 907 (143) | 0 (0) |
| `|modmul_reduce:u_fwd_mul|` | 196.0 (0.0) | 388 (0) | 0 (0) |
| `|modmul_reduce:u_inv_mul|` | 191.2 (0.0) | 376 (0) | 0 (0) |
| `|modmul_reduce:u_scale_mul|` | 189.9 (0.0) | 376 (0) | 0 (0) |
| `|poly_mem:u_mem|` | 6171.0 (6171.0) | 2624 (2624) | 3072 (3072) |
| `|twiddle_rom:u_rom|` | 29.7 (29.7) | 36 (36) | 0 (0) |

(ALM setiap baris `modmul_reduce` seluruhnya berada di dalam anak `lpm_divide:Mod0`-nya; baris anak dihilangkan. Angka dalam tanda kurung adalah sumber daya milik node itu sendiri.)

Pembacaan: setiap `%` di `rtl/ntt/modmul_reduce.sv` menjadi `lpm_divide` kombinasional 24-bit / 12-bit (3 instans); `poly_mem` 256x12 menjadi 3072 flip-flop ditambah multiplekser baca/tulis (0 blok RAM terpakai); ROM twiddle tidak dipetakan ke RAM.

## 4. Jalur setup terburuk (Slow 1100mV 100C)

- Dari (titik awal): `layer_q[2]`
- Ke (titik akhir): `poly_mem:u_mem|mem[64][5]`
- Data tiba 73.704 ns, data dibutuhkan 25.381 ns, slack -48.323 (VIOLATED)
- Jalur clock peluncuran 6.020 ns; jalur clock penahan 5.441 ns (di antaranya pessimism clock yang dihapus 2.185 ns); clock uncertainty -0.060 ns.
- Delay jalur data 67.684 ns = sel 29.959 ns + interkoneksi 37.725 ns.

Sel pada jalur (ns kumulatif dari keluaran register peluncur, inkremen, elemen):

```
   0.000  +0.000  layer_q[2]|q
   1.166  +0.538  Mux7~0|combout
   2.037  +0.308  ShiftRight0~3|combout
   2.809  +0.544  ShiftRight0~5|combout
   3.920  +0.480  ShiftLeft0~0|combout
   5.322  +0.912  Add0~13|sumout
   6.584  +0.932  Add2~5|sumout
   8.019  +1.169  Add3~1|cout
   8.357  +0.338  Add3~25|sumout
   9.952  +0.354  mem_addr_b[3]~1|combout
  12.091  +0.079  u_mem|Mux15~47|combout
  13.895  +0.222  u_mem|Mux15~51|combout
  14.615  +0.508  u_mem|Mux15~62|combout
  15.456  +0.512  u_mem|Mux15~84|combout
  19.236  +3.100  u_bfly|u_fwd_mul|Mult0~mac|resulta[13]
  22.125  +0.359  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|op_4~1|sumout
  23.058  +0.097  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|StageOut[145]~108|combout
  25.040  +0.154  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|op_5~1|sumout
  25.909  +0.084  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|StageOut[157]~93|combout
  27.991  +0.154  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|op_6~1|sumout
  29.484  +0.084  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|StageOut[170]~26|combout
  31.420  +0.154  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|op_7~1|sumout
  32.386  +0.097  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|StageOut[183]~21|combout
  34.035  +0.154  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|op_8~1|sumout
  35.172  +0.087  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|StageOut[198]~27|combout
  37.114  +0.154  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|op_9~1|sumout
  38.064  +0.084  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|StageOut[213]~95|combout
  40.063  +0.154  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|op_10~1|sumout
  41.035  +0.081  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|StageOut[224]~10|combout
  43.023  +0.154  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|op_11~1|sumout
  44.035  +0.083  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|StageOut[237]~33|combout
  45.794  +0.154  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|op_12~1|sumout
  47.206  +0.303  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|StageOut[248]~6|combout
  49.371  +0.154  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|op_14~1|sumout
  50.471  +0.083  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|StageOut[261]~4|combout
  52.224  +0.154  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|op_15~1|sumout
  53.321  +0.079  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|StageOut[280]~12|combout
  55.017  +0.154  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|op_16~1|sumout
  55.803  +0.564  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|StageOut[293]~35|combout
  57.326  +0.154  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|op_17~5|sumout
  58.162  +0.080  u_bfly|u_fwd_mul|Mod0|auto_generated|divider|divider|StageOut[300]~0|combout
  59.361  +0.301  u_bfly|Add6~9|shareout
  59.867  +0.506  u_bfly|Add6~13|cout
  59.867  +0.000  u_bfly|Add6~17|cout
  59.917  +0.050  u_bfly|Add6~21|cout
  59.917  +0.000  u_bfly|Add6~25|cout
  59.967  +0.050  u_bfly|Add6~33|cout
  59.967  +0.000  u_bfly|Add6~37|cout
  60.031  +0.064  u_bfly|Add6~49|cout
  60.031  +0.000  u_bfly|Add6~29|cout
  60.447  +0.416  u_bfly|Add6~41|sumout
  61.222  +0.558  u_bfly|LessThan2~2|combout
  61.968  +0.498  mem_wdata_b[0]~0|combout
  63.014  +0.080  mem_wdata_b[5]~11|combout
  64.946  +0.518  mem_wdata_b[5]~5|combout
  67.422  +0.075  u_mem|mem[64][5]~feeder|combout
  67.684  +0.262  poly_mem:u_mem|mem[64][5]
```
(sel `cout` carry-chain di dalam `Mod0` dihilangkan demi panjang; setiap stage `op_N...sumout` / `StageOut` dipertahankan. Daftar lengkap ada di .json.)

## 5. Atribusi delay per struktur (diturunkan oleh `segment_path.py`, aturan di docstring-nya)

### terburuk (lewat u_fwd_mul, NTT/CT): slack -48.323 (VIOLATED), `layer_q[2]` -> `poly_mem:u_mem|mem[64][5]`

| Struktur | Delay (ns) | Porsi |
|---|---|---|
| pembagi modulo (lpm_divide) | 38.926 | 57.5 % |
| logika kendali / alamat | 9.952 | 14.7 % |
| mux tulis memori + register penyimpanan | 6.462 | 9.5 % |
| mux baca memori (poly_mem) | 5.504 | 8.1 % |
| pengali DSP | 3.780 | 5.6 % |
| add/sub mod butterfly | 3.060 | 4.5 % |
| total jalur data | 67.684 | sel 29.959 / interkoneksi 37.725 |

### lewat u_inv_mul (INTT/GS): slack -47.787 (VIOLATED), `layer_q[2]` -> `poly_mem:u_mem|mem[51][1]`

| Struktur | Delay (ns) | Porsi |
|---|---|---|
| pembagi modulo (lpm_divide) | 36.096 | 53.8 % |
| logika kendali / alamat | 9.952 | 14.8 % |
| add/sub mod butterfly | 6.194 | 9.2 % |
| mux baca memori (poly_mem) | 5.294 | 7.9 % |
| mux tulis memori + register penyimpanan | 5.234 | 7.8 % |
| pengali DSP | 4.381 | 6.5 % |
| total jalur data | 67.151 | sel 31.561 / interkoneksi 35.590 |

### lewat u_scale_mul (skala INTT x3303): slack -46.444 (VIOLATED), `layer_q[2]` -> `poly_mem:u_mem|mem[80][9]`

| Struktur | Delay (ns) | Porsi |
|---|---|---|
| pembagi modulo (lpm_divide) | 37.329 | 56.7 % |
| logika kendali / alamat | 12.068 | 18.3 % |
| mux baca memori (poly_mem) | 7.010 | 10.7 % |
| pengali DSP | 6.540 | 9.9 % |
| mux tulis memori + register penyimpanan | 2.846 | 4.3 % |
| total jalur data | 65.793 | sel 28.426 / interkoneksi 37.367 |

### ke layer_q (hanya kendali): slack -3.829 (VIOLATED), `layer_q[1]` -> `layer_q[2]`

| Struktur | Delay (ns) | Porsi |
|---|---|---|
| logika kendali / alamat | 23.679 | 100.0 % |
| total jalur data | 23.679 | sel 1.738 / interkoneksi 21.941 |

### ke zeta_idx_q (hanya kendali): slack 0.351, `layer_q[2]` -> `zeta_idx_q[0]`

| Struktur | Delay (ns) | Porsi |
|---|---|---|
| logika kendali / alamat | 19.418 | 100.0 % |
| total jalur data | 19.418 | sel 4.496 / interkoneksi 14.922 |

## 6. Semua titik akhir setup (`report_timing -npaths 5000 -nworst 1`, satu jalur terburuk per titik akhir)

- Titik akhir dianalisis: 3104; melanggar: 3074.
- Titik akhir yang melanggar menurut jenis: {'poly_mem storage register': 3072, 'layer_q': 2}
- Titik awal jalur terburuk ke setiap titik akhir yang melanggar: {'layer_q[*]': 3074}
- Jumlah titik akhir per rentang slack (ns): {'[-50, -40)': 3072, '[-40, -30)': 0, '[-30, -20)': 0, '[-20, -10)': 0, '[-10, 0)': 2, '[0, 25)': 30}
- Jumlah slack terburuk per titik akhir yang negatif (turunan): -143688.194 ns (TNS STA untuk corner ini: -143688.194 ns).

## 7. Bukti metodologi clock / batasan

```
Critical Warning (15725): clock port is fed by virtual pin "clk_i~input"; timing analysis treats input to the clock port as a ripple clock
Info (15717): Design contains 39 virtual pins; timing numbers associated with paths containing virtual pins are estimates
```

- Sumber clock di setiap jalur yang dilaporkan adalah `clk_i` di `LABCELL_X1_Y36_N15` (sel logika, karena `clk_i` adalah virtual pin), lalu `clk_i~CLKENA0` pada `CLKCTRL_G3` (clock global, fan-out 3104).
- Suku terkait clock pada jalur terburuk: skew -0.579 ns (baris ringkasan) dan uncertainty -0.060 ns, terhadap delay jalur data 67.684 ns dan periode 20.000 ns.
- 23 port masukan dan 14 port keluaran tidak dibatasi (`C0.sta.rpt`, Unconstrained Paths Summary); jalur I/O karenanya tidak dianalisis. Jalur yang gagal adalah register-ke-register.

