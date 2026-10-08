<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Run formal Fase 8b tahap W1 (test plan V9), 2026-10-03

Perintah: `. scripts/env.sh && python3 formal/run/run_formal_phase8b.py`. Label: MEASURED (SymbiYosys, boolector, kedalaman induksi 30). Hanya properti kendali dan rentang, bukan nilai koefisien.

| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| A Fase 8b | sample_ntt_core (S1, S2, S3, S4, S5) | PASS | PASS | basecase=pass, induction=pass | 5.1 | ya |
| A Fase 8b | cbd2_core (S1, S2 dengan paling banyak 16 word, S3, S4, S5) | PASS | PASS | basecase=pass, induction=pass | 3.3 | ya |
| B Kontrol negatif | NC-S1: kandidat sama dengan q diterima (rentang S1) | FAIL | FAIL | basecase=FAIL; failed assert sample_ntt_core_formal_top.sv:138 | 0.5 | ya |
| B Kontrol negatif | NC-S2: hitungan koefisien mulai dari 1 (relasi hitungan S2: terakhir pada ke-256) | FAIL | FAIL | basecase=FAIL; failed assert sample_ntt_core_formal_top.sv:118 | 0.5 | ya |

SEMUA SESUAI HARAPAN
