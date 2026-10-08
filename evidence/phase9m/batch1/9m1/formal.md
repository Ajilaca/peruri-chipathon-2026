# Run formal Fase 9M butir 1 (V6), `formal/run/run_formal_phase9m1.py`, 2026-10-04

MEASURED dengan SymbiYosys (yosys-slang, boolector). Properti Fase 9a P1-P5 dan U1-U6 pada modul dua byte `mlkem_pack2` dan `mlkem_unpack2` (beat 2 byte: hitungan 16 d beat, penyangga memuat 32 bit). Kontrol NC-P1 dan NC-U1 memberi UNKNOWN pada run bukti dan FAIL pada BMC kedalaman 300, seperti di 9a (pelanggarannya ada di luar kedalaman induksi); pada teks barisnya "byte" berarti satu beat 16 bit untuk modul 9M-1. Seperti di 9a tidak ada run cover untuk kedua modul ini (V6 test plan 9M-1 menyebut cover; tidak dikerjakan, lihat result_9m1.md). Hanya kendali dan rentang; nilai dicakup simulasi. Direktori kerja `formal/work/phase9m1/` (diabaikan git).

| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| A Fase 9M-1 | mlkem_pack2 (P1 hitungan, P2 keluaran ditahan, P3 idle, P4 keseimbangan bit, P5 hitungan pipeline) | PASS | PASS | basecase=pass, induction=pass | 13.3 | ya |
| B Kontrol negatif | NC-P1: pengemas menerima koefisien ke-257 (hitungan P1); pelanggaran di luar kedalaman 40, jadi bukti tidak boleh lolos | UNKNOWN | UNKNOWN | basecase=pass, induction=FAIL; failed assert mlkem_pack2_formal_top.sv:87 | 421.2 | ya |
| B Kontrol negatif | NC-P1 lagi dengan BMC kedalaman 300: koefisien ke-257 dapat dicapai (hitungan P1) | FAIL | FAIL | bmc=FAIL; failed assert mlkem_pack2_formal_top.sv:87 | 674.2 | ya |
| B Kontrol negatif | NC-P2: byte keluaran berubah saat koefisien dimasukkan selagi ditahan (P2) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_pack2_formal_top.sv:98 | 0.9 | ya |
| A Fase 9M-1 | mlkem_unpack2 (U1 hitungan, U2 keluaran ditahan, U3 idle, U4 keseimbangan bit, U5 register keluaran, U6 rentang) | PASS | PASS | basecase=pass, induction=pass | 12.9 | ya |
| B Kontrol negatif | NC-U1: pembongkar menerima satu byte lebih dari 32 d (hitungan U1); pelanggaran di luar kedalaman 40, jadi bukti tidak boleh lolos | UNKNOWN | UNKNOWN | basecase=pass, induction=FAIL; failed assert mlkem_unpack2_formal_top.sv:85 | 220.7 | ya |
| B Kontrol negatif | NC-U1 lagi dengan BMC kedalaman 300: byte tambahan dapat dicapai (hitungan U1) | FAIL | FAIL | bmc=FAIL; failed assert mlkem_unpack2_formal_top.sv:85 | 446.5 | ya |
| B Kontrol negatif | NC-U6: d = 12 tanpa reduksi mod q (rentang U6) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_unpack2_formal_top.sv:105 | 0.6 | ya |

SEMUA SESUAI HARAPAN
