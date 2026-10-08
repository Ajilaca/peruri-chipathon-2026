# Run formal Fase 9F S2b, 2026-10-05 (V4)

MEASURED (formal, hanya kendali dan kapasitas bank). Perintah: `. scripts/env.sh && python3 formal/run/run_formal_phase9s2b.py` (kedalaman 9 = P + 3, `smtbmc boolector`, direktori kerja `formal/work/phase9s2b/`, tidak disimpan; run yang sama dibuat pada 2026-10-04 dengan hasil sama dan keluarannya tidak disimpan). Properti H, O, R, A, B, C dari `formal/phase09m-optimisation/9s2b/ntt_core_s10_p6a_formal_top.sv` (top S2 dengan parameter pembungkus `AREG = 1`) pada `rtl/ntt/ntt_core_s10_p5.sv`. Tidak ada di sini yang membuktikan aritmetika NTT/INTT atau data memori (simulasi mencakupnya).

```
| Group | Proof | Expected | Result | Engine detail | Time (s) | As expected |
|---|---|---|---|---|---|---|
| A S2b | s10 at P = 6, AREG = 1 (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 109.7 | yes |
| B Negative control | NC-O p6a: bank map without the XOR bit (two ports on one bank) | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_s10_p6a_formal_top.sv:131 | 13.4 | yes |
| B Negative control | NC-A p6a: delay model of property A one cycle short | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_s10_p6a_formal_top.sv:132 | 14.6 | yes |

OVERALL: all results as expected (3/3)
```

Pembacaan: bukti berlaku dengan alamat issue terregistrasi (setiap penulisan terjadi tepat 6 siklus setelah permintaannya, dikosongkan di S_DONE, tidak ada baca dan tulis satu lokasi pada siklus yang sama, tidak ada overflow bank); kedua kontrol negatif gagal sesuai syarat. Ini evidence untuk pernyataan rencana bahwa alamat terregistrasi menyajikan nilai yang sama pada siklus yang sama: probe sisi memori pada bukti tidak berubah. Batas: hanya kendali dan kapasitas bank.
