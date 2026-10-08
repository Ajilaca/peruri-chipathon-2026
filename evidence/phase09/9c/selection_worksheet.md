## Per seed pada 40,000 ns (MEASURED)
| Seed | ALM | Register | Blok M10K | Bit memori blok | DSP | Setup / hold terburuk (ns) | Timing terpenuhi @ 40 ns | Fmax slow corner terendah (MHz) | Peringatan kritis | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 17,613 | 8210 | 54 | 120,350 | 28 | 20.272 / 0.096 | ya | 50.69 | 1 | `quartus_MC.md` |
| 2 | 17,636 | 8272 | 54 | 120,350 | 28 | 19.010 / 0.075 | ya | 47.64 | 1 | `quartus_MC-s2.md` |
| 3 | 17,630 | 8365 | 54 | 120,350 | 28 | 19.395 / 0.104 | ya | 48.53 | 1 | `quartus_MC-s3.md` |
| 4 | 17,623 | 8232 | 54 | 120,350 | 28 | 19.815 / 0.133 | ya | 49.54 | 1 | `quartus_MC-s4.md` |
| 5 | 17,608 | 8272 | 54 | 120,350 | 28 | 20.671 / 0.106 | ya | 51.74 | 1 | `quartus_MC-s5.md` |
| 6 | 17,618 | 8248 | 54 | 120,350 | 28 | 19.599 / 0.104 | ya | 49.02 | 1 | `quartus_MC-s6.md` |

Median ALM (min-maks): 17,620.5 (17,608-17,636); register 8210-8365; M10K 54-54; DSP 28-28; median Fmax (min-maks): 49.280 (47.64-51.74) MHz

### Aturan lolos (test plan bagian 5, butir 2 dan 3)
- PASS: fit berhasil di setiap seed
- PASS: timing terpenuhi pada 40,000 ns di setiap seed (slack setup dan hold terburuk semua corner tidak negatif)
- dilaporkan sebagai MEASURED: jumlah sumber daya dan Fmax (median Fmax slow-corner terendah atas seed 1-6) di atas
- informasi MC-20 (20,000 ns), seed 1: ALM 17,650, register 8374, setup terburuk 4.419 ns (terpenuhi), Fmax slow corner terendah 64.18 MHz, `quartus_MC-20.md`

## Siklus per operasi (MEASURED di simulasi; tanpa stall host; satu operasi dari start_i sampai done_o seperti dilihat driver test)
| Operasi | Icarus | Verilator |
|---|---|---|
| Encaps (konstan untuk setiap m dengan ek yang sama) | [10691] | [10691] |
| Decaps (konstan untuk ciphertext valid dan ditolak dan untuk kunci rahasia berbeda dengan ek yang sama) | [16623] | [16623] |
| KeyGen pada 25 seed ACVP (hanya bergantung rho publik), min - maks | 9035 - 9076 | 9035 - 9076 |
| Encaps pada vektor ACVP (ek berbeda), min - maks | 10664 - 10727 | 10664 - 10727 |
| Decaps pada vektor ACVP (dk berbeda), min - maks | 16601 - 16663 | 16601 - 16663 |
