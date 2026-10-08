# Run formal Fase 9b (V8), `formal/run/run_formal_phase9b.py`, 2026-10-03

MEASURED dengan SymbiYosys (yosys-slang, boolector). Baris kelompok C adalah run mode cover (setiap state yang dicakup harus tercapai; menunjukkan bukti tidak vakum). Pembungkus hash dibuktikan dengan stub protokol sponge (test plan 9b, Amandemen A1 butir 1 dan 2). Direktori kerja `formal/work/phase9b/` (diabaikan git).

| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| C Keterjangkauan | mlkem_hash: word digest setelah 3 word diterima dan done_o untuk H, G, dan J dapat dicapai (bukti tidak vakum) | PASS | PASS | bmc=pass | 1.2 | ya |
| A Fase 9b | mlkem_hash (H1 hitungan word digest, H2 done, H3 word ditahan, H4 idle, H5 sponge idle setelah word terakhir) | PASS | PASS | basecase=pass, induction=pass | 6.4 | ya |
| B Kontrol negatif | NC-H1: G berhenti setelah 4 word digest (H1 word terakhir) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_hash_formal_top.sv:104 | 0.6 | ya |
| B Kontrol negatif | NC-H5: J tidak pernah menghentikan squeeze (H5 sponge idle) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_hash_formal_top.sv:91 | 0.6 | ya |
| C Keterjangkauan | mlkem_fo_cmp: done_o dengan neq_o = 1 dan dengan neq_o = 0 dapat dicapai (bukti tidak vakum) | PASS | PASS | bmc=pass | 0.8 | ya |
| A Fase 9b | mlkem_fo_cmp (F1 beat dan done, F2 hasil ditahan, F3 akumulator dan neq, F4 pemilihan mask) | PASS | PASS | basecase=pass, induction=pass | 11.8 | ya |
| B Kontrol negatif | NC-F3: pembanding hanya melihat 32 bit rendah (akumulator F3) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_fo_cmp_formal_top.sv:84 | 0.6 | ya |
| B Kontrol negatif | NC-F4: pemilihan kunci dibalik (F4) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_fo_cmp_formal_top.sv:105 | 1.3 | ya |
| B Kontrol negatif | NC-F1: pembandingan berakhir pada selisih pertama (F1 done setelah tepat WORDS beat) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_fo_cmp_formal_top.sv:90 | 0.6 | ya |

SEMUA SESUAI HARAPAN
