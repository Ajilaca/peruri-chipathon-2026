# Run formal Fase 9a (V9), `formal/run/run_formal_phase9a.py`, 2026-10-03

MEASURED dengan SymbiYosys (yosys-slang, boolector). Direktori kerja `formal/work/phase9a/` (diabaikan git).

| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| A Fase 9a | mlkem_pack (P1 hitungan, P2 keluaran ditahan, P3 idle, P4 keseimbangan bit, P5 hitungan pipeline) | PASS | PASS | basecase=pass, induction=pass | 17.4 | ya |
| B Kontrol negatif | NC-P1: pengemas menerima koefisien ke-257 (hitungan P1); pelanggaran di luar kedalaman 40, jadi bukti tidak boleh lolos | UNKNOWN | UNKNOWN | basecase=pass, induction=FAIL; failed assert mlkem_pack_formal_top.sv:87 | 441.6 | ya |
| B Kontrol negatif | NC-P1 lagi dengan BMC kedalaman 300: koefisien ke-257 dapat dicapai (hitungan P1) | FAIL | FAIL | bmc=FAIL; failed assert mlkem_pack_formal_top.sv:87 | 548.2 | ya |
| B Kontrol negatif | NC-P2: byte keluaran berubah saat koefisien dimasukkan selagi ditahan (P2) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_pack_formal_top.sv:98 | 0.6 | ya |
| A Fase 9a | mlkem_unpack (U1 hitungan, U2 keluaran ditahan, U3 idle, U4 keseimbangan bit, U5 register keluaran, U6 rentang) | PASS | PASS | basecase=pass, induction=pass | 11.9 | ya |
| B Kontrol negatif | NC-U1: pembongkar menerima satu byte lebih dari 32 d (hitungan U1); pelanggaran di luar kedalaman 40, jadi bukti tidak boleh lolos | UNKNOWN | UNKNOWN | basecase=pass, induction=FAIL; failed assert mlkem_unpack_formal_top.sv:85 | 192.0 | ya |
| B Kontrol negatif | NC-U1 lagi dengan BMC kedalaman 300: byte tambahan dapat dicapai (hitungan U1) | FAIL | FAIL | bmc=FAIL; failed assert mlkem_unpack_formal_top.sv:85 | 377.5 | ya |
| B Kontrol negatif | NC-U6: d = 12 tanpa reduksi mod q (rentang U6) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_unpack_formal_top.sv:105 | 0.6 | ya |

SEMUA SESUAI HARAPAN
