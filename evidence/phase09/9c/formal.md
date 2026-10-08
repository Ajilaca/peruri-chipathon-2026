# Run formal Fase 9c (CRG-8), `formal/run/run_formal_phase9c.py all`, 2026-10-04

MEASURED dengan SymbiYosys (yosys-slang, boolector). Kelompok C adalah run mode cover (setiap state yang dicakup harus tercapai; menunjukkan bukti tidak vakum), kedalaman 260. Pengendali dibuktikan dengan stub protokol sub-blok (`formal/phase09-integration/9c/stubs_9c.sv`; test plan 9c, Amandemen A2). E1 adalah properti non-interferensi dua salinan: dua salinan pengendali dengan data berbeda dan handshake identik mempertahankan state kendali identik. Hanya properti kendali dan rentang; nilai dicakup simulasi (ACVP). Decaps done dan state S_CMPK tidak tercapai pada kedalaman 260 (state pemberian hash memerlukan 136-148 word); run cover dalam terpisah (`formal_deep_cover.md`, kedalaman 480) mencapai keduanya. Direktori kerja `formal/work/phase9c/` (diabaikan git).

| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| C Keterjangkauan | mlkem_core: KeyGen done, Encaps done, dan sebuah word digest tertulis dapat dicapai (bukti tidak vakum) | PASS | PASS | bmc=pass | 1134.8 | ya |
| A Fase 9c | pengendali mlkem_core (E1 non-interferensi, S1 rentang, S2 busy / done, S3 tidak ada tulis host saat sibuk, S4 strobe, S5 port mesin, S6 alamat, S7 counter) | PASS | PASS | basecase=pass, induction=pass | 5.0 | ya |
| B Kontrol negatif | NC-E1: program counter bergantung pada satu bit data (non-interferensi E1) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_core_formal_top.sv:70 | 3.9 | ya |
| B Kontrol negatif | NC-S3: tulis host diterima saat sibuk, di state LDP (S3) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_core_formal_top.sv:97 | 3.4 | ya |
| B Kontrol negatif | NC-S4: tugas simpan mulai bersamaan dengan tugas muat (S4) | FAIL | FAIL | basecase=FAIL; failed assert mlkem_core_formal_top.sv:99 | 3.3 | ya |

SEMUA SESUAI HARAPAN
