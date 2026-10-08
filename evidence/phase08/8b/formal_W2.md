<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Run formal Fase 8b, baris W1 dan W2 (test plan V9), 2026-10-03

Perintah: `. scripts/env.sh && python3 formal/run/run_formal_phase8b.py all`. Label: MEASURED (SymbiYosys, boolector, kedalaman induksi 30). Hanya properti kendali dan rentang, bukan nilai koefisien. File W1 `formal_W1.md` dibuat sebelum kode W2 ada.

| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| A Fase 8b W1 | sample_ntt_core OUTW=1 (S1, S2, S3, S4, S5) | PASS | PASS | basecase=pass, induction=pass | 12.4 | ya |
| A Fase 8b W1 | cbd2_core OUTW=1 (S1, S2 dengan paling banyak 16 word, S3, S4, S5) | PASS | PASS | basecase=pass, induction=pass | 8.6 | ya |
| B Kontrol negatif W1 | NC-S1: kandidat sama dengan q diterima (rentang S1), OUTW=1 | FAIL | FAIL | basecase=FAIL; failed assert sample_ntt_core_formal_top.sv:146 | 1.1 | ya |
| B Kontrol negatif W1 | NC-S2: hitungan koefisien mulai dari 1 (relasi hitungan S2: terakhir pada beat terakhir), OUTW=1 | FAIL | FAIL | basecase=FAIL; failed assert sample_ntt_core_formal_top.sv:127 | 1.3 | ya |
| A Fase 8b W2 | sample_ntt_core OUTW=2 (S1, S2, S3, S4, S5, S6 carry) | PASS | PASS | basecase=pass, induction=pass | 17.4 | ya |
| A Fase 8b W2 | cbd2_core OUTW=2 (S1, S2 dengan paling banyak 16 word, S3, S4, S5) | PASS | PASS | basecase=pass, induction=pass | 8.8 | ya |
| B Kontrol negatif W2 | NC-S1: kandidat sama dengan q diterima (rentang S1), OUTW=2 | FAIL | FAIL | basecase=FAIL; failed assert sample_ntt_core_formal_top.sv:146 | 0.8 | ya |
| B Kontrol negatif W2 | NC-S2: hitungan koefisien mulai dari 1 (relasi hitungan S2: terakhir pada beat terakhir), OUTW=2 | FAIL | FAIL | basecase=FAIL; failed assert sample_ntt_core_formal_top.sv:127 | 0.7 | ya |

SEMUA SESUAI HARAPAN
