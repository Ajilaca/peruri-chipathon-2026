<!-- claim-lint: skip-file (internal verification record, not proposal text) -->
# Hasil formal Fase 4 (test plan V9, CRG-8) - C3, P = 2 / 4 / 6

- Dibuat: 2026-09-30 16:06 UTC. Perintah: `. scripts/env.sh && python3 formal/run/run_formal_phase4.py`
- Alat: SBY v0.69; Yosys 0.69+136 (git sha1 0fa1478ce-dirty, Release, Clang /us; frontend yosys-slang, `memory_map -rom-only`, smtbmc boolector; k-induksi kedalaman P + 3.
- Desain yang dibuktikan: pembungkus Quartus `rtl/ntt/ntt_core_c3_p2.sv`, `_p4.sv`, `_p6.sv` di dalam `formal/phase04-pipeline/ntt_core_c3_formal_top.sv`.
- Lingkup: hanya properti kendali dan kapasitas bank. Tidak ada di sini yang membuktikan aritmetika NTT/INTT atau integritas data memori; itu bertumpu pada simulasi (`cocotb_regression.txt`, `v2_modmul_staged_exhaustive.txt`).

## Properti
| | Properti |
|---|---|
| H | penurunan `busy_o` diikuti `done_o` satu siklus kemudian (modul properti Fase 1, dipakai ulang) |
| O | `bank_overflow_o` == 0 |
| R | rentang counter: `t_q`, `layer_q`, `state_q`, `drain_q`, `hw_q` (di-assert di `rtl/ntt/ntt_core_c3.sv` di bawah `FORMAL`) |
| A | setiap penulisan memori terjadi tepat P siklus setelah permintaannya (bit write-valid == `en & wr` permintaan ditunda P siklus di model delay independen) |
| B | dikosongkan: di `S_DONE` tidak ada penulisan yang diminta dalam P siklus terakhir yang tertunda dan tidak ada penulisan yang terjadi |
| C | tidak ada baca dan tulis satu lokasi penyimpanan pada siklus yang sama untuk lalu lintas transformasi (permintaan `S_RUN` / `S_SCALE`) |

## Hasil
| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| A Phase 4 | C3 P=2 (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 6.8 | ya |
| A Phase 4 | C3 P=4 (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 8.2 | ya |
| A Phase 4 | C3 P=6 (H, O, R, A, B, C) | PASS | PASS | basecase=pass, induction=pass | 12.7 | ya |
| B Kontrol negatif | NC-O P=2: salinan bank_map_rom, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c3_formal_top.sv:144 | 7.5 | ya |
| B Kontrol negatif | NC-O P=6: salinan bank_map_rom, NUM_BANKS=8: bank(128) 2 -> 3 | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c3_formal_top.sv:144 | 11.7 | ya |
| B Kontrol negatif | NC-A P=2: model delay properti A kurang satu siklus | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c3_formal_top.sv:145 | 8.5 | ya |
| B Kontrol negatif | NC-B P=2: pengosongan kurang satu siklus (induksi harus gagal) | UNKNOWN | UNKNOWN | basecase=pass, induction=FAIL; failed assert ntt_core_c3_formal_top.sv:147 | 13.3 | ya |
| B Kontrol negatif | NC-B/bmc125 P=2: mutan yang sama, BMC kedalaman 125 (pelanggaran dapat dicapai) | FAIL | FAIL | bmc=FAIL; failed assert ntt_core_c3_formal_top.sv:147 | 2130.1 | ya |
| B Kontrol negatif | NC-C P=2: lintasan skala boleh mengulang alamat (induksi harus gagal) | UNKNOWN | UNKNOWN | basecase=pass, induction=FAIL; failed assert ntt_core_c3_formal_top.sv:150 | 18.5 | ya |

OVERALL: semua hasil sesuai harapan (9/9)

## Membaca kontrol negatif
Semuanya dijalankan pada salinan yang dirusak di bawah `formal/work/phase04/` (diabaikan git); RTL repository tidak diubah.
- NC-O (satu bank salah di salinan `bank_map_rom`) dan NC-A (model delay kurang satu siklus) gagal pada basis, jadi
  properti O dan A tidak vakum.
- NC-B (pengosongan kurang satu siklus) dan NC-C (lintasan skala boleh mengulang alamat) adalah pelanggaran yang terletak lebih dari 100
  siklus dari reset, di luar kedalaman basis; langkah induksi gagal, jadi mutan itu tidak terbukti (UNKNOWN,
  yang tidak sama dengan kegagalan yang didemonstrasikan). Untuk NC-B pemeriksaan terbatas kedalaman 125 mencapai pelanggaran dan
  GAGAL. Pelanggaran NC-C ada di lintasan skala INTT, lebih dari 112 siklus setelah start; tidak ada run terbatas dalam yang dibuat
  untuknya, jadi untuk NC-C buktinya hanya bahwa bukti tidak berhasil.
