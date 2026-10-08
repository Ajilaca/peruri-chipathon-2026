# Run formal Fase 9F S1 (V6), `formal/run/run_formal_phase9f1.py`, 2026-10-04

MEASURED dengan SymbiYosys (yosys-slang, boolector). Bukti Fase 8d F1-F5 untuk `kpke_sched_smp` (STREAM_A = 1, OVERLAP = 1) dengan sequencer diinstansiasi pada CORE_R2 = 0 (sampler K0) di top formal `formal/phase09m-optimisation/9f1/kpke_sched_smp_formal_top.sv`. Sampler adalah stub protokol 8c, yang mengabaikan CORE_R2, jadi bukti hanya menunjukkan bahwa nilai parameter itu dapat dielaborasi dan properti kendali berlaku; INFERENCE: logika kendali sequencer tidak memakai CORE_R2 (`grep CORE_R2 rtl/sched`: hanya penerusan ke `keccak_sampler`). Bahwa sampler K0 nyata mengikuti protokol stub ditunjukkan oleh simulasi V2 / V3 (sampler K0 8b bit-exact; kelas stall tercakup). Bukti pengendali 9c tidak bergantung pada parameter sampler (mesin adalah stub di sana) dan tidak dijalankan ulang untuk `mlkem_core2` (teks pengendalinya sama dengan `mlkem_core`; INFERENCE). Direktori kerja `formal/work/phase9f1/` (diabaikan git).

| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| A Fase 9F S1 | kpke_sched_smp STREAM_A=1 OVERLAP=1 CORE_R2=0 (F1-F5) | PASS | PASS | basecase=pass, induction=pass | 2.2 | ya |
| B Kontrol negatif | NC-F2: penulisan seed diterima saat sibuk (F2), OVERLAP=1 | FAIL | FAIL | basecase=FAIL; failed assert kpke_sched_smp_formal_top.sv:88 | 1.4 | ya |

SEMUA SESUAI HARAPAN
