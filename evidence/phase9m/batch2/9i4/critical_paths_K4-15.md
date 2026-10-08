<!-- claim-lint: skip-file (internal evidence, not proposal text) -->
# Jalur kritis K4 pada 15 ns (K4-15-s6, seed dengan slack terkecil), 2026-10-05

MEASURED dengan `quartus_sta -t scripts/quartus/phase5m_top_paths.tcl` (300 jalur setup terburuk, model slow, 1.100 mV, 100 C) pada salinan database terkompilasi `quartus/phase09i4_core`, diklasifikasikan oleh `scripts/quartus/classify_paths_9f.py` (laporan mentah tidak disimpan). K4-15-s6: slack setup +0,596 ns pada semua corner, Fmax 69,43 MHz, seed terendah.

```
## K4-15-s6_paths_slow100_summary.rpt
paths: 300, slack 0.736 .. 2.434 ns
  worst slack   0.736 ns,   29 paths: engine sequencer -> NTT core / memory / PWM
  worst slack   1.759 ns,  207 paths: engine sequencer -> Keccak permutation (sampler sponge)
  worst slack   1.971 ns,   60 paths: NTT core / memory / PWM -> NTT core / memory / PWM
  worst slack   2.083 ns,    4 paths: hash wrapper / sponge control -> register file
```
| Jalur | Slack terburuk (ns) | Dari | Ke |
|---|---|---|---|
| 21 + 3 + 5 | 0.736 | `cnt_q` sequencer mesin | alamat issue terregistrasi `jlen_r` / `j_r` inti NTT (S2b) |
| 189 + 18 | 1.759 | `opc_q` sequencer mesin | state Keccak sponge sampler |
| 48 | 1.990 | delay posisi baca inti NTT | reducer Barrett |
| 8 | 1.971 | delay operand sisi | bank M10K |

## Pembacaan
- Jalur terburuk K4 bukan hal baru dari butir 4: ia milik S2b. Elemen demi elemen (MEASURED, laporan penuh jalur terburuk): `cnt_q[6]` -> `Equal8~0` (`cnt_q != 0`) -> `core_hwe_o` -> `mode_q~1` (suku `start_go` dari `mode_n`) -> `ShiftRight8` / `ShiftLeft14` (alamat blok dan start) -> `Add23`, `Add25` (j, j + len) -> `jlen_r`. Sequencer menggerakkan enable tulis host NTT dari counternya, dan S2b membuat alamat terregistrasi bergantung padanya lewat `start_go`.
- Butir 4 sendiri (pemberian tulis host, interlock, `pend_q`) tidak muncul di antara 300 jalur terburuk; kelas terdekat pada +1,759 ns adalah jalur yang sudah ada dari register opcode mesin ke state Keccak sampler (207 jalur), kelas yang sama yang sudah tertinggal 2,4 ns di K1b.
