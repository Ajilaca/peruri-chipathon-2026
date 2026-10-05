# Phase 8: Keccak, sampler, K-PKE

Status: DONE. Halaman hasil: [../../docs/results/phase08.md](../../docs/results/phase08.md).

**Tujuan.** 8a Keccak dua ronde per siklus, 8b sampler streaming, 8c matriks A on-the-fly, 8d tumpang-tindih sampler dengan aritmetika.

**Yang diuji.** Tiap sub-langkah: kebenaran terhadap model acuan, byte XOF yang dikonsumsi tepat, formal, seed sweep dengan aturan adopsi.

**Alat.** cocotb, SymbiYosys, Quartus.

**Hasil utama.** C5 diadopsi (ADR 0027), sampler W2 (ADR 0028), STREAM (ADR 0029), OVERLAP (ADR 0030). Angka per langkah ada di worksheet masing-masing.

**File penting.**
- [8a/selection_worksheet.md](8a/selection_worksheet.md)
- [8b/selection_worksheet.md](8b/selection_worksheet.md)
- [8c/selection_worksheet.md](8c/selection_worksheet.md)
- [8d/selection_worksheet.md](8d/selection_worksheet.md)
- [8a/test_plan_8a.md](8a/test_plan_8a.md)
- [8d/test_plan_8d.md](8d/test_plan_8d.md)

Semua file di folder ini dibuat oleh alat, bukan diketik tangan. Angka Quartus berasal dari kompilasi kernel-only dengan virtual pin.
