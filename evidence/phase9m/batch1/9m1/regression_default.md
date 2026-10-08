# Regresi Fase 9M-1 pada parameter bawaan (V7), 2026-10-04

MEASURED. Dengan `CODEC_W2 = 0` (bawaan) inti harus berperilaku persis seperti di Fase 9. Dijalankan di branch `phase9m-optimisation` (inti kini punya blok generate dan file baru ada, tetapi bawaannya menginstansiasi tugas Fase 9): `scripts/test/phase9c_verify.sh` (lint, pemeriksaan ROM, model acuan, seluruh himpunan ACVP di kedua simulator, lalu `phase9a_verify.sh` dan `phase9b_verify.sh` dengan formal, lalu pemeriksaan blok beku terhadap main), `formal/run/run_formal_phase9c.py all`, dan profil `../../profile.md` diulang pada nilai bawaan (identik dengan profil Fase 9: KeyGen 9.095, Encaps 10.735, Decaps 16.667 siklus, setiap hitungan per-state dan per-operasi sama). Hanya header bagian dan baris hasil log mentah yang disimpan.

## scripts/test/phase9c_verify.sh
```
## V1 verilator --lint-only -Wall mlkem_core (whole design)
rc=0
## V1 slang mlkem_core (whole design)
rc=0
## V2 ROM equals the generated ROM, static checks
rc=0
## V2 golden control model against ACVP and the unmodified golden
rc=0
## V3-V8 verilator
[verilator] TOTAL: 11/11 passed
rc=0
## V3-V8 icarus
[icarus] TOTAL: 11/11 passed
rc=0
## V10 regression: scripts/test/phase9a_verify.sh (without formal)
rc=0
rc=0
rc=0
rc=0
rc=0
[verilator] TOTAL: 17/17 passed
rc=0
[icarus] TOTAL: 17/17 passed
rc=0
OVERALL: PASS
rc=0
## V10 regression: scripts/test/phase9b_verify.sh (with formal)
rc=0
rc=0
rc=0
rc=0
rc=0
rc=0
[verilator] TOTAL: 23/23 passed
rc=0
[icarus] TOTAL: 23/23 passed
rc=0
rc=0
OVERALL: PASS
rc=0
## V10 frozen blocks: files of rtl/sched rtl/ntt rtl/mem rtl/arith rtl/sample rtl/keccak that differ from main
differing files: 0
OVERALL: PASS
```

## formal/run/run_formal_phase9c.py all (parameter bawaan)

| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| C Keterjangkauan | mlkem_core: KeyGen done, Encaps done, dan sebuah word digest tertulis dapat dicapai (bukti tidak vakum) | PASS | PASS | bmc=pass | 926.3 | ya |
| A Fase 9c | pengendali mlkem_core (E1 non-interferensi, S1 rentang, S2 busy / done, S3 tidak ada tulis host saat sibuk, S4 strobe, S5 port mesin, S6 alamat, S7 counter) | PASS | PASS | basecase=pass, induction=pass | 3.5 | ya |
| B Kontrol negatif | NC-E1: program counter bergantung pada satu bit data (non-interferensi E1) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_core_formal_top.sv:80 | 2.5 | ya |
| B Kontrol negatif | NC-S3: tulis host diterima saat sibuk, di state LDP (S3) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_core_formal_top.sv:107 | 2.3 | ya |
| B Kontrol negatif | NC-S4: tugas simpan mulai bersamaan dengan tugas muat (S4) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_core_formal_top.sv:109 | 2.4 | ya |

SEMUA SESUAI HARAPAN
