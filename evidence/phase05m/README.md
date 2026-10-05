# Phase 5M: memori dan jadwal

Status: DONE. Halaman hasil: [../../docs/results/phase05m.md](../../docs/results/phase05m.md).

**Tujuan.** Memotong jalur kritis memori: INTT tanpa lintasan skala (S6), split baca (S7), register tulis (S8), studi M10K (S9).

**Yang diuji.** Kebenaran tiap langkah, formal, seed sweep, analisis port M10K.

**Alat.** cocotb, SymbiYosys, Quartus, skrip analisis port.

**Hasil utama.** S7 lolos aturan (median 38,720 MHz, 120 siklus). S8 tidak lolos. S9 menemukan peta 16 bank 1R1W bebas konflik, dibangun sebagai S10 di Phase 6.

**File penting.**
- [test_plan.md](test_plan.md)
- [s6/selection_worksheet.md](s6/selection_worksheet.md)
- [s7/selection_worksheet.md](s7/selection_worksheet.md)
- [s8/selection_worksheet.md](s8/selection_worksheet.md)
- [s9/study_m10k.md](s9/study_m10k.md)
- [s9/port_analysis.txt](s9/port_analysis.txt)

Semua file di folder ini dibuat oleh alat, bukan diketik tangan. Angka Quartus berasal dari kompilasi kernel-only dengan virtual pin.
