# Formal Fase 5a (test plan V8) - 2026-10-01

Perintah: `. scripts/env.sh && python3 formal/run/run_formal_phase5.py` (frontend yosys-slang, `memory_map -rom-only`, SymbiYosys, smtbmc boolector).
Lingkup: properti kendali dan kapasitas bank H, O, R, A, B, C dari `formal/phase05-arith/ntt_core_c4_formal_top.sv` pada pembungkus Quartus `rtl/ntt/ntt_core_c4a.sv` (P = 6), dengan dua kontrol negatif pada salinan yang dirusak. Bukan aritmetika (dicakup uji reducer menyeluruh dan simulasi bit-exact).

| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| A Fase 5 | c4a (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 12.2 | ya |
| B Kontrol negatif | NC-O c4a: salinan bank_map_rom, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:135 | 10.1 | ya |
| B Kontrol negatif | NC-A c4a: model delay properti A kurang satu siklus | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:136 | 14.7 | ya |
OVERALL: semua hasil sesuai harapan (3/3)
