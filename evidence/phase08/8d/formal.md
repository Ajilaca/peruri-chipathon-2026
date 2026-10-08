<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Run formal Fase 8d (test plan V7), 2026-10-03

Perintah: `. scripts/env.sh && python3 formal/run/run_formal_phase8d.py`. Label: MEASURED (SymbiYosys, boolector, kedalaman induksi 12; OVERLAP = 1; inti NTT diabstraksikan, sampler diganti stub protokol). Hanya properti kendali, bukan nilai.

| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| A Fase 8d | kpke_sched_smp STREAM_A=1 OVERLAP=1 (F1-F5) | PASS | PASS | basecase=pass, induction=pass | 3.0 | ya |
| B Kontrol negatif | NC-F2: penulisan seed diterima saat sibuk (F2), OVERLAP=1 | FAIL | FAIL | basecase=FAIL; failed assert kpke_sched_smp_formal_top.sv:87 | 1.4 | ya |

SEMUA SESUAI HARAPAN
