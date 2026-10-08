## Per seed pada 40,000 ns (MEASURED)
| Seed | ALM | Register | Bit memori blok | DSP | Setup / hold terburuk (ns) | Timing terpenuhi @ 40 ns | Fmax slow corner terendah (MHz) | Peringatan kritis | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 298 | 192 | 0 | 2 | 30.143 / 0.168 | ya | 101.45 | 1 | `quartus_CD.md` |
| 2 | 299 | 192 | 0 | 2 | 30.046 / 0.167 | ya | 100.46 | 1 | `quartus_CD-s2.md` |
| 3 | 299 | 193 | 0 | 2 | 30.940 / 0.166 | ya | 110.38 | 1 | `quartus_CD-s3.md` |
| 4 | 299 | 192 | 0 | 2 | 30.624 / 0.167 | ya | 106.66 | 1 | `quartus_CD-s4.md` |
| 5 | 299 | 192 | 0 | 2 | 30.716 / 0.167 | ya | 107.71 | 1 | `quartus_CD-s5.md` |
| 6 | 299 | 192 | 0 | 2 | 30.440 / 0.167 | ya | 104.60 | 1 | `quartus_CD-s6.md` |

Median ALM (min-maks): 299.0 (298-299); register 192-193; DSP 2-2; median Fmax (min-maks): 105.630 (100.46-110.38) MHz

### Aturan lolos (test plan bagian 5, butir 2 dan 3)
- PASS: fit berhasil di setiap seed
- PASS: timing terpenuhi pada 40,000 ns di setiap seed (slack setup dan hold terburuk semua corner tidak negatif)
- dilaporkan sebagai MEASURED: jumlah sumber daya dan Fmax (median Fmax slow-corner terendah atas seed 1-6) di atas; DSP dilaporkan dan tidak dibatasi

- informasi CD-20 (20,000 ns), seed 1: ALM 298, setup terburuk 10.952 ns (terpenuhi), Fmax slow corner terendah 110.52 MHz, `quartus_CD-20.md`

## Siklus per polinomial (MEASURED di simulasi, sink selalu siap, tanpa jeda masukan; identik untuk setiap nilai data pada satu d: test V7)
| d | pack, Icarus | pack, Verilator | unpack, Icarus | unpack, Verilator |
|---|---|---|---|---|
| 1 | 261 | 261 | 259 | 259 |
| 4 | 261 | 261 | 259 | 259 |
| 10 | 325 | 325 | 323 | 323 |
| 12 | 389 | 389 | 387 | 387 |
