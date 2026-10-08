# Formal Fase 5c (test plan A4 V8 / V8-lazy) - 2026-10-01

Perintah: `. scripts/env.sh && python3 formal/run/run_formal_phase5.py` (frontend yosys-slang, `memory_map -rom-only`, SymbiYosys, smtbmc boolector). Properti kendali / kapasitas bank untuk setiap pembungkus C4 termasuk C4c, dan bukti batas nilai `rtl/arith/lazy_bfly_io.sv` (P1 u < 2q dan s < 2q; P2 u kongruen dengan b - a, NTT u = b; P3 keluaran < q dan sama dengan persamaan acuan) dengan kontrol negatif (nilai sisi keluaran INTT tidak direduksi -> harus FAIL). Lingkup: kendali, kapasitas bank, dan batas I/O; reducer untuk u di [0, 2q) dicakup uji menyeluruh, bukan oleh bukti ini.

| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| A Fase 5c | batas lazy_bfly_io (P1-P3) | PASS | PASS | basecase=pass, induction=pass | 0.8 | ya |
| B Kontrol negatif | NC-L: nilai sisi keluaran INTT tidak direduksi | FAIL | FAIL | basecase=FAIL, induction=FAIL; failed assert lazy_bfly_io_formal_top.sv:54 | 0.4 | ya |
| A Fase 5 | c4c (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 51.4 | ya |
| B Kontrol negatif | NC-O c4c: salinan bank_map_rom, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:145 | 10.5 | ya |
| B Kontrol negatif | NC-A c4c: model delay properti A kurang satu siklus | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c4_formal_top.sv:146 | 11.9 | ya |

Run yang sama membuktikan ulang C4a, C4b-B, dan C4b-M setelah perubahan inti (semua PASS, kontrol negatif FAIL): 14/14 hasil sesuai harapan.
