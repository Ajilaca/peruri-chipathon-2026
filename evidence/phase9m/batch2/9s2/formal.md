# Run formal Fase 9F S2, 2026-10-04 (V5)

MEASURED (formal, hanya kendali dan kapasitas bank). Perintah: `. scripts/env.sh && python3 formal/run/run_formal_phase9s2.py` (kedalaman 9 = P + 3, `smtbmc boolector`, direktori kerja `formal/work/phase9s2/`, tidak disimpan). Properti H, O, R, A, B, C dari `formal/phase09m-optimisation/9s2/ntt_core_s10_p6_formal_top.sv` (salinan `formal/s10/ntt_core_s10_formal_top.sv` dengan P = 6 dan parameter pembungkus `P6 = 1`) pada `rtl/ntt/ntt_core_s10_p5.sv`. Tidak ada di sini yang membuktikan aritmetika NTT/INTT atau data memori (simulasi V2 mencakupnya).

```
| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |
|---|---|---|---|---|---|---|
| A S2 | s10 at P = 6 (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 15.6 | yes |
| B Negative control | NC-O p6: bank map without the XOR bit (two ports on one bank) | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_s10_p6_formal_top.sv:131 | 7.3 | yes |
| B Negative control | NC-A p6: delay model of property A one cycle short | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_s10_p6_formal_top.sv:132 | 9.9 | yes |

OVERALL: all results as expected (3/3)
```

Pembacaan: tabel tiga baris adalah alur S10 pada P = 6. Bukti berlaku pada P = 6 (setiap penulisan terjadi tepat 6 siklus setelah permintaannya, dikosongkan di S_DONE, tidak ada baca dan tulis satu lokasi pada siklus yang sama, tidak ada overflow bank); kedua kontrol negatif gagal sesuai syarat (NC-O peta bank tanpa bit XOR; NC-A model delay kurang satu siklus). Batas: hanya kendali dan kapasitas bank (basis dan induksi pada kedalaman 9, seperti di S10); jalur aritmetika lewat register baru dicakup simulasi bit-exact (V2, V7), bukan bukti ini.
