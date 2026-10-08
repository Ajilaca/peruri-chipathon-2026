<!-- claim-lint: skip-file (internal analysis record, not proposal text) -->
# Pra-pemeriksaan 5c: apakah `sub_mod` ada di segmen kritis C4b-B? (sebelum RTL 5c apa pun)

Label: MEASURED (Timing Analyzer Quartus pada salinan database C4b-B seed 1), INFERENCE, ESTIMATE.
Database: revisi `C4b-B` (seed 1, 40,000 ns, bawaan Quartus), kompilasi
`evidence/phase05/5b/quartus_C4b-B.md` (slack setup terburuk +11,044 ns, cocok). Skrip:
`scripts/quartus/phase5_top_paths.tcl` (jalur penuh jalur terburuk) dan kueri `get_timing_paths -to *u_bfly|u_side|*` (jalur terburuk
ke delay line sisi butterfly). Corner: hanya Slow 1100mV 100C.

## 1. Jalur terburuk (MEASURED, slack +11,044 ns): memori -> `mul_in` -> pengali
| Segmen (kedatangan kumulatif, ns) | Delay (ns) | Blok |
|---|---:|---|
| 6.030 → 27.062 | 21.03 | memory read decode + read mux (`raddr0`, `Mux206`, `Mux365`, `Mux357`) |
| 27.062 → 31.279 | **4.22** | butterfly input `sub_mod(b, a)` (`Add1`, `LessThan0`, `mul_in` select) |
| 31.279 → 34.869 | 3.59 | routing into the DSP + Barrett product to cut X |

Jawaban: ya - `sub_mod` ada di segmen kritis (4,22 dari 28,84 ns jalur data).

## 2. Kelas jalur kedua (MEASURED, slack +12,102 ns): memori -> `side_in` -> delay line sisi
Operand sisi `a + b` butterfly INTT melewati read mux yang sama, lalu `add_mod(a, b)`, ke delay line sisi butterfly,
yang oleh Quartus diimplementasikan sebagai shift register di M10K (`pipe_delay:u_side|altshift_taps`):
| Segmen (kedatangan kumulatif, ns) | Delay (ns) | Blok |
|---|---:|---|
| 6.030 → 27.136 | 21.11 | memory read decode + read mux |
| 27.136 → 31.099 | **3.96** | butterfly input `add_mod(a, b)` (`Add3`, `LessThan1`, `side_in` select) |
| 31.099 → 33.362 | 2.26 | routing into the M10K data input |

## 3. Pembacaan (INFERENCE / ESTIMATE)
- Menghapus hanya `sub_mod` dari jalur pengali menyisakan jalur sisi (§2) sebagai jalur terburuk: sekitar 40 − 12,102 =
  27,9 ns periode pada seed 1, yaitu batas Fmax sekitar 35,8 MHz (INFERENCE, satu seed). Ambang adopsi 5c
  adalah median Fmax di atas 34,84 MHz (puncak rentang seed 5b Barrett), jadi perubahan hanya-`sub_mod` paling banter melewatinya
  dengan margin kecil.
- Membuat kedua masukan butterfly INTT malas - masukan pengali `b + q − a` di [1, 2q) dan operand sisi `a + b` di
  [0, 2q), yang terakhir direduksi sekali di keluaran (satu pengurangan bersyarat di segmen tulis, yang punya slack
  +17,125 ns, `5b/c4b_segments_slow100.txt`) - menghapus compare/select dari kedua jalur. ESTIMATE: jalur terburuk sekitar
  21 + 1 + 3,6 ≈ 26 ns (≈ 38 MHz); bukan prediksi Fmax; hanya kompilasi yang bisa memastikan.
- Bagaimanapun bagian pembacaan memori (≈ 21 ns) tetap; 50 MHz tidak terjangkau di 5c (ADR 0010).
