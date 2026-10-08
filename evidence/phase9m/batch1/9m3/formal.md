# Run formal Fase 9M-3 (V5), `formal/run/run_formal_phase9m3.py hash`, 2026-10-04

MEASURED dengan SymbiYosys (yosys-slang, boolector). Properti pembungkus hash Fase 9b H1-H5 untuk `mlkem_hash` dengan `CORE_R2 = 0` (instans sponge K0), sponge diganti stub protokol `keccak_sponge_stub.sv` (stub 9b dari sponge C5 dengan nama K0, port dan protokol sama). INFERENCE: bahwa sponge K0 nyata mengikuti protokol stub didukung oleh bukti Fase 7 dan simulasi ACVP dan hash V2 (digest dibandingkan dengan hashlib di 9b, varian K0 `hash0`). Hanya properti kendali dan hasil. Direktori kerja `formal/work/phase9m3/` (diabaikan git).

| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| C Keterjangkauan | mlkem_hash (stub K0): word digest setelah 3 word diterima dan done_o untuk H, G, dan J dapat dicapai (bukti tidak vakum) | PASS | PASS | bmc=pass | 1.6 | ya |
| A Fase 9M-3 | mlkem_hash dengan stub K0 (H1 hitungan word digest, H2 done, H3 word ditahan, H4 idle, H5 sponge idle setelah word terakhir) | PASS | PASS | basecase=pass, induction=pass | 5.6 | ya |
| B Kontrol negatif | NC-H1: G berhenti setelah 4 word digest (H1 word terakhir) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_hash_k0_formal_top.sv:104 | 0.9 | ya |
| B Kontrol negatif | NC-H5: J tidak pernah menghentikan squeeze (H5 sponge idle) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_hash_k0_formal_top.sv:91 | 0.7 | ya |

SEMUA SESUAI HARAPAN
