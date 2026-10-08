## Per seed pada 40,000 ns, sponge C5 (MEASURED)
| Seed | ALM | Register | Bit memori blok | DSP | Setup / hold terburuk (ns) | Timing terpenuhi @ 40 ns | Fmax slow corner terendah (MHz) | Peringatan kritis | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 6,745 | 1976 | 0 | 0 | 19.095 / 0.163 | ya | 47.84 | 1 | `quartus_HF.md` |
| 2 | 6,728 | 1976 | 0 | 0 | 19.122 / 0.161 | ya | 47.90 | 1 | `quartus_HF-s2.md` |
| 3 | 6,737 | 1976 | 0 | 0 | 20.400 / 0.162 | ya | 51.02 | 1 | `quartus_HF-s3.md` |
| 4 | 6,712 | 1976 | 0 | 0 | 20.090 / 0.162 | ya | 50.23 | 1 | `quartus_HF-s4.md` |
| 5 | 6,737 | 1976 | 0 | 0 | 20.794 / 0.162 | ya | 52.07 | 1 | `quartus_HF-s5.md` |
| 6 | 6,732 | 1976 | 0 | 0 | 20.508 / 0.162 | ya | 51.30 | 1 | `quartus_HF-s6.md` |

Median ALM (min-maks): 6,734.5 (6,712-6,745); register 1976-1976; DSP 0-0; median Fmax (min-maks): 50.625 (47.84-52.07) MHz

### Aturan lolos (test plan bagian 5, butir 2 dan 3)
- PASS: fit berhasil di setiap seed
- PASS: timing terpenuhi pada 40,000 ns di setiap seed (slack setup dan hold terburuk semua corner tidak negatif)
- dilaporkan sebagai MEASURED: jumlah sumber daya dan Fmax (median Fmax slow-corner terendah atas seed 1-6) di atas; tidak ada alternatif yang dipilih di blok ini
- informasi HF-20 (20,000 ns, sponge C5), seed 1: ALM 6,745, register 1976, setup terburuk 3.843 ns (terpenuhi), Fmax slow corner terendah 61.89 MHz, `quartus_HF-20.md`
- informasi HF-K0 (40,000 ns, sponge K0 (instans hash kedua dengan inti lebih kecil)), seed 1: ALM 4,221, register 1977, setup terburuk 25.719 ns (terpenuhi), Fmax slow corner terendah 70.02 MHz, `quartus_HF-K0.md`

## Siklus (MEASURED di simulasi, sink selalu siap, tanpa jeda masukan; identik untuk setiap nilai data satu operasi: test V6)
| Operasi | sponge C5, Icarus | sponge C5, Verilator | sponge K0, Icarus | sponge K0, Verilator |
|---|---|---|---|---|
| G dari 33 byte | 30 | 30 | 42 | 42 |
| G dari 64 byte | 33 | 33 | 45 | 45 |
| H dari 1184 byte | 282 | 282 | 390 | 390 |
| J dari 1120 byte | 274 | 274 | 382 | 382 |
| perbandingan 1,088 byte (136 beat) | 137 | 137 | - | - |
