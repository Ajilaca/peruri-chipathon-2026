<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Run formal Fase 7 (test plan V8), 2026-10-03

Perintah: `. scripts/env.sh && python3 formal/run/run_formal_phase7.py` (SymbiYosys, frontend yosys-slang, mesin smtbmc boolector). Properti K1-K5 dari `formal/phase07-keccak/keccak_sponge_formal_top.sv` pada
`rtl/keccak/keccak_sponge.sv` dengan `keccak_f1600.sv`, semua masukan bebas, kedalaman induksi 30. Hanya properti kendali; nilai digest dicakup simulasi terhadap hashlib (`verify.md`).
Label: MEASURED (keluaran alat formal run ini; RTL seperti di-commit setelah perbaikan enum Icarus).

| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| A Fase 7 | keccak_sponge + keccak_f1600 (K1, K2, K3, K4, K5) | PASS | PASS | basecase=pass, induction=pass | 22.5 | ya |
| B Kontrol negatif | NC-K1: 23 ronde per permutasi (panjang busy K1) | FAIL | FAIL | basecase=FAIL; failed assert keccak_sponge_formal_top.sv:105 | 38.4 | ya |
| B Kontrol negatif | NC-K4: data keluaran bergantung pada out_ready_i (penahanan K4; BMC kedalaman 40: fase squeeze dicapai setelah sekitar 30 siklus) | FAIL | FAIL | bmc=FAIL; failed assert keccak_sponge_formal_top.sv:122 | 38.6 | ya |

SEMUA SESUAI HARAPAN

Pembacaan: A lolos dengan induksi (basis dan langkah), jadi K1 (busy_o persis 24 siklus, counter 0..23, pulsa done hanya setelah ronde 23), K2 (tidak ada xor saat sibuk), K3 (indeks word di bawah rate, lane xor di bawah rate,
indeks keluaran tetap di dalam digest), K4 (word keluaran yang menunggu ditahan) dan K5 (state sah, stop mencapai IDLE) berlaku untuk setiap urutan masukan. NC-K1 (23 ronde) dan NC-K4 (data bergantung pada `out_ready_i`) gagal
sesuai syarat, jadi bukti ini tidak vakum. NC-K4 berjalan sebagai BMC sampai kedalaman 40 karena fase squeeze baru dicapai setelah sekitar 30 siklus (satu word absorb, satu word padding, satu permutasi 26 siklus), melampaui
kedalaman induksi; trik yang sama dengan NC-B Fase 3.
