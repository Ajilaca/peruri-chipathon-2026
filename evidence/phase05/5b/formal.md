# Formal Fase 5b (test plan V8) - 2026-10-01

Perintah: `. scripts/env.sh && python3 formal/run/run_formal_phase5.py` (frontend yosys-slang, `memory_map -rom-only`, SymbiYosys, smtbmc boolector). Dijalankan setelah RTL 5b ditambahkan; C4a dibuktikan ulang dengan daftar sumber yang diperluas.
Lingkup: properti kendali dan kapasitas bank H, O, R, A, B, C dari `formal/phase05-arith/ntt_core_c4_formal_top.sv` pada pembungkus Quartus `rtl/ntt/ntt_core_c4a.sv`, `ntt_core_c4b_b.sv`, `ntt_core_c4b_m.sv` (P = 6), dengan masing-masing dua kontrol negatif pada salinan yang dirusak. Bukan aritmetika (dicakup uji reducer menyeluruh dan simulasi bit-exact).

| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| A Fase 5 | c4a (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 15.0 | ya |
| B Kontrol negatif | NC-O c4a: salinan bank_map_rom, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:142 | 12.8 | ya |
| B Kontrol negatif | NC-A c4a: model delay properti A kurang satu siklus | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:143 | 11.2 | ya |
| A Fase 5 | c4b_b (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 28.3 | ya |
| B Kontrol negatif | NC-O c4b_b: salinan bank_map_rom, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:142 | 17.3 | ya |
| B Kontrol negatif | NC-A c4b_b: model delay properti A kurang satu siklus | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:143 | 23.0 | ya |
| A Fase 5 | c4b_m (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 20.1 | ya |
| B Kontrol negatif | NC-O c4b_m: salinan bank_map_rom, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:142 | 16.5 | ya |
| B Kontrol negatif | NC-A c4b_m: model delay properti A kurang satu siklus | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:143 | 19.2 | ya |
OVERALL: semua hasil sesuai harapan (9/9)
