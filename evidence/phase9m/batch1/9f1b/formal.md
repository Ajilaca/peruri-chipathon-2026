# Run formal Fase 9F S1b (V7), `formal/run/run_formal_phase9f1b.py`, 2026-10-04

MEASURED dengan SymbiYosys (yosys-slang, boolector). Non-interferensi dua salinan (E1) dan properti pengendali S1-S7 Fase 9c untuk `mlkem_core3` (tugas dua byte, sidecar hash latar belakang), ditambah B1-B7 sidecar (`formal/phase09m-optimisation/9f1b/mlkem_core3_formal_top.sv`; stub protokol untuk sub-blok). Hanya kendali dan rentang; nilai dicakup simulasi. Direktori kerja `formal/work/phase9f1b_*` (diabaikan git). Run dibuat dalam tiga bagian (`proofs`, `cover`, dan percobaan ulang NC-B7 kemudian): run penuh pertama menunjukkan (1) sasaran cover "KeyGen done / Encaps done" tidak terjangkau pada kedalaman 260 (job 148 word saja memerlukan lebih dari itu; sasaran dipindah ke balik -D DEEP dan cover dikurangi menjadi penulisan digest dan pembacaan sidecar), (2) kegagalan induksi bukti keselamatan yang memerlukan satu invarian pendukung (sidecar berjalan hanya selagi pengendali utama tidak idle; ditambahkan, lalu bukti lolos).

## proofs (keselamatan dan kontrol negatif, bounded model check kontrol pada kedalaman 160)
| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| A Fase 9F S1b | pengendali mlkem_core3 (E1 non-interferensi dengan sidecar, S1-S7, B1 satu pemilik hash, B2 done hanya dengan sidecar idle, B3 JN menunggu, B4 / B5 / B7 bus, B6 counter) | PASS | PASS | basecase=pass, induction=pass | 6.3 | ya |
| B Kontrol negatif | NC-B3: JN maju selagi job berjalan (B3) | FAIL | FAIL | bmc=FAIL; failed assert mlkem_core3_formal_top.sv:194 | 116.6 | ya |
| B Kontrol negatif | NC-B7: penulisan digest sidecar mengabaikan penulisan utama pada siklus yang sama (B7) | FAIL | TIMEOUT |  | 1800.0 | TIDAK |
| B Kontrol negatif | NC-E1: start job bergantung pada satu bit data (non-interferensi E1) | FAIL | FAIL | bmc=FAIL; failed assert mlkem_core3_formal_top.sv:92 | 5.0 | ya |

## cover (kedalaman 200)
| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| C Keterjangkauan | mlkem_core3: word digest sidecar tertulis dan pembacaan sidecar yang diterbitkan dapat dicapai (bukti tidak vakum) | PASS | PASS | bmc=pass | 491.3 | ya |

## Percobaan ulang NC-B7 lebih lama (timeout 3 jam)
Run pertama kontrol NC-B7 (penulisan digest sidecar mengabaikan penulisan utama pada siklus yang sama) habis waktu setelah 1.800 s pada kedalaman 160 (tidak ada pelanggaran ditemukan sampai langkah 94). Percobaan ulang dengan batas 3 jam dimulai (dua kali: percobaan ulang pertama dimatikan oleh restart sesi). Pada saat file ini ditulis ia belum punya hasil; bila menemukan pelanggaran akan ditambahkan di sini, bila tidak kontrol B7 hanya ditunjukkan oleh simulasi (NC-WR di `sim.md`: KeyGen ACVP gagal), bukan oleh run formal.
