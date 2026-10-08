<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Run formal Fase 8a (test plan V8), 2026-10-03

Perintah: `. scripts/env.sh && python3 formal/run/run_formal_phase8a.py` (SymbiYosys, yosys-slang, smtbmc boolector). Properti K1-K5 dari `formal/phase08-keccak-stream/keccak_sponge_r2_formal_top.sv` pada `rtl/keccak/keccak_sponge_r2.sv` dengan
`keccak_f1600_r2.sv`, semua masukan bebas, kedalaman induksi 30; K1 adalah "busy_o persis 12 siklus, counter 0..11". Hanya properti kendali. Label: MEASURED (keluaran alat formal run ini).

| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| A Fase 8a | keccak_sponge_r2 + keccak_f1600_r2 (K1, K2, K3, K4, K5) | PASS | PASS | basecase=pass, induction=pass | 81.6 | ya |
| B Kontrol negatif | NC-K1: 11 siklus per permutasi (panjang busy K1) | FAIL | FAIL | basecase=FAIL; failed assert keccak_sponge_r2_formal_top.sv:105 | 35.4 | ya |
| B Kontrol negatif | NC-K4: data keluaran bergantung pada out_ready_i (penahanan K4; BMC kedalaman 40: fase squeeze dicapai setelah sekitar 30 siklus) | FAIL | FAIL | bmc=FAIL; failed assert keccak_sponge_r2_formal_top.sv:122 | 31.1 | ya |

SEMUA SESUAI HARAPAN

Pembacaan: bukti lolos dengan induksi (basis dan langkah); NC-K1 (11 siklus) dan NC-K4 (data bergantung pada `out_ready_i`) gagal sesuai syarat. Teks runner NC-K4 menyebut "fase squeeze dicapai setelah sekitar 30 siklus", disalin dari
Fase 7; dengan 14 siklus per permutasi fase squeeze dicapai setelah sekitar 18 siklus (1 start, 1 absorb, 1 padding, 14 permutasi, 1 squeeze); BMC kedalaman 40 tetap mencakupnya, hasil tidak berubah.
