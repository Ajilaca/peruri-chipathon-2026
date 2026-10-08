# MEASURED - Perbandingan Quartus C1 lawan C0 (Fase 2, konfigurasi C1: memori berbank pada NUM_BANKS=1)

- Dibangkitkan: 2026-09-29 UTC, dari `evidence/quartus/C0.md`,
  `evidence/quartus/C1.md`, dan pendalaman `quartus_sta` hanya-baca
  (`quartus/phase02_mem_c1/report_worst_path.tcl`) pada netlist pasca-fit C1 yang ada.
- Batasan sementara sama dengan C0: `quartus/phase02_mem_c1/C1.sdc` = `quartus/phase01_ntt_c0/C0.sdc`
  persis sama (20.000 ns pada `clk_i`), device sama (5CSEBA6U23I7), metodologi virtual-pin sama.
- C1 = FSM/butterfly/ROM twiddle C0, byte demi byte, dengan `rtl/ntt/poly_mem.sv` diganti
  `rtl/mem/poly_mem_banked.sv #(.NUM_BANKS(1))` (`rtl/mem/ntt_core_c1.sv`).

## 1. Apakah setiap tahap selesai?

Keempatnya (Analysis & Synthesis, Fitter, Assembler, Timing Analyzer) selesai dengan 0 error, sama
seperti C0. `Critical Warning (332148): Timing requirements not met` milik Timing Analyzer tetap muncul
4 kali (sekali per corner) -- tidak berubah dari C0. (Catatan: hitungan peringatan kritis otomatis
`extract_quartus_report.py` di `evidence/quartus/C1.md` terbaca 0 karena ia diarahkan ke
`C1.flow.rpt`, yang tidak memuat peringatan kritis tahap Timing-Analyzer; hitungan yang benar,
dibaca langsung dari `C1.sta.rpt`, adalah 4 -- sama seperti C0. Dicatat di sini agar "0" otomatis itu tidak
disalahartikan sebagai "tidak ada peringatan kritis".)

## 2. Perbandingan terukur

| Besaran | C0 (Fase 1) | C1 (Fase 2) | Perubahan |
|---|---|---|---|
| ALM | 7,010 / 41,910 (17%) | 6,749 / 41,910 (16%) | -261 ALM |
| Register | 3,104 | 3,105 | +1 |
| Blok RAM (M10K) | 0 / 553 | 0 / 553 | tidak berubah -- lihat Bagian 4 |
| Bit memori blok | 0 / 5,662,720 | 0 / 5,662,720 | tidak berubah |
| Blok DSP | 3 / 112 | 3 / 112 | tidak berubah |
| Fmax, Slow 100C | 14.64 MHz | 14.99 MHz | +0.35 MHz |
| Fmax, Slow -40C | 14.69 MHz | 15.05 MHz | +0.36 MHz |
| Slack setup terburuk, Slow 100C | -48.323 ns | -46.720 ns | +1.603 ns (masih gagal) |
| TNS setup terburuk, Slow 100C | -143,688.194 ns | -139,926.248 ns | membaik, masih sangat negatif |
| Slack hold terburuk | 0.211 ns (terpenuhi) | 0.168 ns (terpenuhi) | masih terpenuhi |
| Siklus NTT / INTT (simulasi) | 897 / 1153 | 897 / 1153 | 0 -- identik, 0 siklus stall |

Sumber: `evidence/quartus/C0.md`, `evidence/quartus/C1.md`,
`evidence/phase01/quartus_C0_timing_analysis.md`,
`evidence/phase02/cocotb_regression.txt`.

## 3. Akar masalah -- tidak berubah dari C0

Jalur terburuk tetap register-ke-register lewat aritmetika, berakhir di register memori:
`layer_q[0]` -> `poly_mem_banked:u_mem|g_bank[0].mem[28][1]`, delay data 66.087 ns (lawan
67.684 ns milik C0), 46 level logika, 252 referensi ke sel `lpm_divide` kombinasional yang sama yang diinferensi
dari `%` di `rtl/ntt/modmul_reduce.sv` pada jalur (`quartus/phase02_mem_c1/output_files/C1_worst_setup_path.rpt`).
Fase 2 tidak menyentuh `rtl/ntt/modmul_reduce.sv` atau aritmetika lain mana pun, jadi ini diharapkan,
bukan temuan baru -- perbaikan slack kecil (~1.6 ns) dikaitkan dengan hasil penempatan/routing yang berbeda di sekitar modul memori yang ditukar,
bukan perbaikan aritmetika atau timing apa pun.
Memperbaikinya adalah lingkup Fase 4 (pipelining) / Fase 5 (aritmetika), menurut `docs/ROADMAP.md`.

## 4. Temuan jujur: M10K TIDAK dipakai, meskipun judul Fase 2 sendiri

Lingkup implementasi Fase 2 di `docs/ROADMAP.md` berkata "penyimpanan polinomial M10K". Hasil
terukur adalah 0 / 553 blok RAM terpakai -- identik dengan C0. Dari log Analysis & Synthesis
(`quartus/phase02_mem_c1/output_files/C1.map.rpt`):

```
Info (276014): Found 5 instances of uninferred RAM logic
    Info (276007): RAM logic "poly_mem_banked:u_mem|bank_map_rom:u_map_b|Ram0" is uninferred due to asynchronous read logic
    Info (276007): RAM logic "poly_mem_banked:u_mem|bank_map_rom:u_map_b|Ram1" is uninferred due to asynchronous read logic
    Info (276007): RAM logic "poly_mem_banked:u_mem|bank_map_rom:u_map_a|Ram0" is uninferred due to asynchronous read logic
    Info (276007): RAM logic "poly_mem_banked:u_mem|bank_map_rom:u_map_a|Ram1" is uninferred due to asynchronous read logic
    Info (276004): RAM logic "twiddle_rom:u_rom|rom_zeta" is uninferred due to inappropriate RAM size
```

Hanya `bank_map_rom` dan `twiddle_rom` yang disebut di sini -- array penyimpanan 256-entri `poly_mem_banked` sendiri
bahkan tidak dikenali sebagai kandidat RAM di log ini, dan hitungan register yang hampir tidak berubah
(3104 -> 3105) mengonfirmasi ia masih dibangun dari flip-flop, persis seperti `poly_mem.sv` milik C0.
Perubahan `-261 ALM` karenanya dikaitkan dengan logika `bank_map_rom` (kecil, murah)
dan pengepakan flip-flop/mux yang berbeda di sekitar modul yang ditukar, bukan dengan penghematan blok RAM mana pun.

Akar masalah: baik `rtl/ntt/poly_mem.sv` (C0) maupun `rtl/mem/poly_mem_banked.sv` (C1) memakai
port baca asinkron (kombinasional), sehingga butterfly satu-siklus (baca kedua operand,
hitung, tulis kedua hasil, siklus sama) dapat selesai tanpa stage register latensi baca.
Inferensi M10K Quartus mensyaratkan baca sinkron karena alasan persis ini (pesan 276007
di atas menyatakannya langsung). Mencapai M10K butuh desain yang membaca operandnya ke
register satu siklus sebelum dipakai -- perubahan penjadwalan, bukan sesuatu yang diam-diam disusulkan ke C1
tanpa tinjauan tim, karena ia mengubah jumlah siklus FSM (saat ini terbukti
identik dengan C0 pada 897/1153 -- syarat CRG-7 fase ini sendiri).

Ini dicatat sebagai keterbatasan, tidak dikoreksi di fase ini: kriteria PASS Fase 2 `docs/ROADMAP.md` sendiri
("Bebas konflik terbukti untuk keempat nilai L; siklus stall terukur = 0 pada
L = 1; bit-exact; jumlah siklus konstan; baris C1 terisi") tidak mensyaratkan pemakaian M10K bukan nol, dan
tidak ada kata dalam kriteria itu yang dilemahkan di sini -- angka 0 yang jujur itulah yang diisi ke baris
C1 (`docs/ROADMAP.md`).
