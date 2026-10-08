<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Fase 9M butir 2 (9M-2): inti pada 20,000 ns, seed 1-6 - test plan dan aturan

Ditulis 2026-10-04 sebelum kompilasi 9M-2 apa pun. Lingkup: ADR 0034 (Accepted, Faza Dzil), butir 2 ("lanjut 2", chat 2026-10-04). Tanpa perubahan RTL. Label: MEASURED, ESTIMATE, INFERENCE, perhitungan tim.

## 1. Mengapa
Fase 9 mengukur inti pada batasan 40,000 ns (gerbang Fase 5-9) dan, sebagai informasi, pada 20,000 ns hanya untuk seed 1 (MC-20: terpenuhi, +4,419 ns). Satu seed bukan tren. Butir ini mengompilasi seed 2-6 pada 20,000 ns, sehingga "timing terpenuhi pada 20 ns" dapat dinyatakan dengan seed 1-6 yang sama seperti hasil 40 ns, dan latensi pada 20 ns dapat dikutip (perhitungan tim). 20,000 ns adalah 50 MHz, clock DE10-Nano; seperti di Fase 5-9 ini timing statis kernel-only dengan virtual pin, bukan sistem di papan (ADR 0010: informasi, bukan gerbang).

## 2. Konfigurasi (satu direktori proyek `quartus/phase09m2_core`, revisi dijalankan satu per satu)
| Revisi | Inti | Seed |
|---|---|---|
| MC-20-s2 ... MC-20-s6 | Inti Fase 9, `CODEC_W2 = 0`, `HASH_C5 = 1` (sumber sama dengan `quartus/phase09c_core/MC-20.qsf`) | 2-6 |
| MW-20-s2 ... MW-20-s6 | Inti 9M-1, `CODEC_W2 = 1` (sumber sama dengan `quartus/phase09m1_core/MW-20.qsf`) | 2-6 |
Seed 1 keduanya diambil dari evidence yang ada (`evidence/phase09/9c/quartus_MC-20.md`, `evidence/phase9m/batch1/9m1/quartus_MW-20.md`); setelannya identik (bawaan Quartus, `C-20.sdc`), hanya seed yang berbeda. Inti Fase 9 diukur karena ADR 0035 (9M-1) belum diterima; inti 9M-1 karena ia basis kandidat untuk butir 3 dan 4.

## 3. Estimasi yang ditulis sebelum mengukur (ESTIMATE)
Pada 40 ns Fmax slow corner terendah seed 1-6 adalah 47,64-51,74 MHz (MC) dan 46,85-52,15 MHz (MW), yaitu sebagian seed di bawah 50 MHz saat batasannya 40 ns. Di bawah batasan 20 ns fitter bekerja lebih keras (MC-20 seed 1: 64,18 MHz, MW-20 seed 1: 63,92 MHz). ESTIMATE: timing terpenuhi pada 20,000 ns di sebagian besar atau semua seed, Fmax slow corner terendah 55-66 MHz, slack setup terburuk +1 sampai +5 ns; ALM dalam +/- 1 % dari median 40 ns; satu seed atau lebih mungkin gagal. Kegagalan dilaporkan sebagai MEASURED, tidak disembunyikan.

## 4. Parameter yang diukur
Per revisi: ALM, register, blok RAM, bit memori blok, DSP, slack setup dan hold terburuk (semua corner), timing terpenuhi ya / tidak, Fmax slow corner terendah, peringatan kritis (dari ekstrak, `.claude/skills/quartus-report/scripts/extract_quartus_report.py`). Per konfigurasi: median, minimum, dan maksimum atas seed 1-6; jumlah seed yang memenuhi 20,000 ns. Latensi pada 20 ns: t = siklus / Fmax dengan siklus masukan profil (Fase 9: 9.095 / 10.735 / 16.667; 9M-1: 8.327 / 10.159 / 15.515) dan median Fmax slow corner terendah konfigurasi (perhitungan tim, bukan pengukuran papan). Catatan: inti yang memenuhi batasan 20 ns tidak di-clock lebih cepat karena hal itu; angka yang boleh dikutip adalah "memenuhi 50 MHz (20 ns) pada timing statis kernel-only".

## 5. Aturan (ditetapkan sebelum mengukur)
Informasi, bukan adopsi di antara kandidat. Pernyataan "inti memenuhi timing pada 20,000 ns" dibuat untuk sebuah konfigurasi hanya bila slack setup dan hold terburuk tidak negatif di keenam seed; selain itu pernyataannya "terpenuhi di k dari 6 seed" dengan seed yang gagal disebut. Tidak ada run yang diulang dengan setelan lain untuk membuat seed yang gagal menjadi hijau.

## 6. Prosedur
`quartus/phase09m2_core/run_20.sh` mengompilasi sepuluh revisi benar-benar satu per satu (berbagi satu .qpf; skrip memulihkan .qpf yang ditulis ulang alat), mencatat `compile_<rev>.log`; mengekstrak dengan skrip `quartus-report`; `scripts/quartus/select_9m2.py` menulis `selection_worksheet_<date>.md` dari ekstrak. Tidak perlu simulasi atau run formal (tanpa perubahan RTL; file RTL adalah milik 9M-1, diverifikasi di sana).
