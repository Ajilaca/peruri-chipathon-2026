<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Fase 9F langkah S0: inti 9M-1 di bawah batasan lebih ketat - test plan dan aturan

Ditulis 2026-10-04 sebelum kompilasi S0 apa pun. Lingkup: ADR 0036 (Accepted, Faza Dzil: urutan S0 -> S1 -> S2, aturan latensi, Fmax dilaporkan pada batasan lebih ketat di samping 40 ns). Tanpa perubahan RTL. Label: MEASURED, ESTIMATE, INFERENCE, perhitungan tim.

## 1. Mengapa
Laporan jalur kritis inti 9M-1 (`../../critical_paths_MW.md`) menunjukkan bahwa pada 20 ns setiap dari 300 jalur terburuk berada di dalam permutasi Keccak C5 (slack +4.355 ns) dan, INFERENCE, bahwa di luar itu desain mengizinkan sekitar 69 MHz (14.5 ns). S0 mencari seberapa jauh batasan dapat diperketat pada desain yang ada (batas permutasi C5), sebelum S1 menggantinya. Ini adalah baseline untuk S1 dan untuk pelaporan Fmax pada batasan lebih ketat yang diputuskan di ADR 0036.

## 2. Revisi (satu proyek `quartus/phase09f0_core`, satu per satu; inti = 9M-1, `CODEC_W2 = 1`, `HASH_C5 = 1`, sumber seperti `quartus/phase09m1_core/MW.qsf`)
| Revisi | Batasan | Seed | Upaya |
|---|---|---|---|
| F16-s1, F16-s2 | 16.000 ns | 1, 2 | bawaan Quartus |
| F15-s1, F15-s2 | 15.000 ns | 1, 2 | bawaan Quartus |
| F14-s1, F14-s2 | 14.000 ns | 1, 2 | bawaan Quartus |
| H14-s1, H14-s2 | 14.000 ns | 1, 2 | `OPTIMIZATION_MODE "HIGH PERFORMANCE EFFORT"`, `OPTIMIZATION_TECHNIQUE SPEED` |
Hanya seed 1 dan 2 (sapuan untuk mencari batas, bukan pernyataan enam seed yang diminta ADR 0036 pada batasan pelaporan akhir; itu datang bersama S1). Anggaran ALM rencana adalah 20,000.

## 3. Estimasi yang ditulis sebelum mengukur (ESTIMATE)
Dari laporan jalur MW-20: slack terburuk +4.355 ns pada 20 ns, yaitu periode sekitar 15.6 ns untuk jalur terburuk sebagaimana ditinggalkan fitter di bawah batasan 20 ns; di bawah batasan lebih ketat fitter bekerja lebih keras. ESTIMATE: 16 ns terpenuhi di kedua seed; 15 ns terpenuhi di satu atau kedua seed; 14 ns tidak terpenuhi pada upaya bawaan; upaya high-performance mendapat 0.3-1 ns pada jalur terburuk di 14 ns dan mungkin memenuhinya atau tidak. ALM dalam +/- 3 % dari 17,654 (upaya dan replikasi dapat menambah ALM); register +/- 3 %; blok RAM 54 dan DSP 28 tidak berubah. Jika sebuah batasan gagal, slack yang gagal dilaporkan sebagai MEASURED; tidak ada setelan yang diubah sesudahnya untuk membuatnya hijau.

## 4. Parameter yang diukur (per revisi, dari ekstrak `.claude/skills/quartus-report/scripts/extract_quartus_report.py`)
ALM (dan % dari denominator fitter), register, blok RAM, DSP, slack setup dan hold terburuk (semua corner), timing terpenuhi ya / tidak, Fmax slow corner terendah, peringatan kritis; per batasan: terpenuhi di k dari 2 seed. Latensi pada Fmax yang dicapai: t = siklus / Fmax (perhitungan tim; siklus masukan profil inti 9M-1: 8,327 / 10,159 / 15,515) untuk batasan yang terpenuhi di kedua seed, dengan Fmax yang lebih rendah dari dua seed. Klasifikasi jalur kritis (skrip `scripts/quartus/phase5m_top_paths.tcl` pada salinan) dibuat untuk batasan paling ketat yang terpenuhi di kedua seed.

## 5. Aturan (ditetapkan sebelum mengukur)
Informasi; tanpa adopsi di antara kandidat. Batas desain yang ada adalah batasan paling ketat yang terpenuhi di kedua seed; bila tidak ada batasan yang terpenuhi di kedua seed, batasnya adalah yang paling longgar dari sapuan yang terpenuhi di satu seed, dinyatakan dengan seed yang gagal. Langkah ini berguna bagi S1 bila ia menyebut blok yang membatasi timing pada batasan itu.

## 6. Prosedur
`quartus/phase09f0_core/run_f0.sh` mengompilasi delapan revisi benar-benar satu per satu (.qpf bersama; dipulihkan setelah tiap kompilasi), mencatat `compile_<rev>.log`; mengekstrak ke `evidence/phase9m/batch1/9f0/`; `scripts/quartus/select_9f0.py` menulis `selection_worksheet_<date>.md` dari ekstrak; klasifikasi jalur seperti di `../../critical_paths_MW.md`. Tidak perlu simulasi atau run formal (tanpa perubahan RTL). Kompilasi berjalan di samping kompilasi butir 3 `quartus/phase09m3_core` (direktori proyek berbeda; mesin dipakai bersama, yang dapat memperpanjang waktu run tetapi tidak mengubah hasil).

## 7. Amandemen A2 (2026-10-04, setelah sapuan pertama; tidak ada di atas yang diedit)
Sapuan bagian 2-6 (16, 15, 14 ns; `result_9f0.md`) menemukan setiap batasan terpenuhi, jadi ia tidak menemukan batasnya. Faza Dzil, chat 2026-10-04: perluas sapuan dan "check sampai fail; jika pada 10 ns masih pass kita stop di sana saja".
- Revisi tambahan: F13, F12, F11, F10, masing-masing pada seed 1 dan 2, bawaan Quartus (setelan sama seperti F14: tanpa upaya high performance, bentuk SDC S0 tanpa false path reset, `C-13.sdc` .. `C-10.sdc`). Dijalankan oleh `quartus/phase09f0_core/run_f0x.sh`, benar-benar satu kompilasi sekali.
- Aturan (ditetapkan sebelum run): batasan dicoba berurutan 13, 12, 11, 10 ns, kedua seed sebuah batasan setiap kali. Sapuan berhenti setelah batasan pertama yang salah satu seed-nya memiliki slack setup atau hold negatif di corner mana pun di `sta.summary` (batasan itu lalu dilaporkan tidak terpenuhi di k dari 2 seed, dan batasnya terletak antara itu dan yang sebelumnya); ia berhenti setelah 10 ns bila setiap batasan sampai 10 ns terpenuhi (maka batasnya di bawah 10 ns dan tidak dicari lebih jauh).
- Estimasi yang ditulis sebelum run (ESTIMATE): ketiga kelas permutasi dan kelas NTT berada dalam 0.55 ns pada 14 ns (slack +0.721 ns, yaitu jalur terburuk sekitar 13.3 ns); fitter sejauh ini mampu menggeser jalur, jadi kegagalan pertama diharapkan di 12 atau 11 ns; 13 ns terpenuhi di kedua seed. Area naik saat batasan makin ketat (replikasi: ALM naik sampai sekitar +3 %, register sampai +10 %).
- Aturan pembacaan: seperti di bagian 5 (informasi, tanpa adopsi); klasifikasi jalur kritis (`scripts/quartus/classify_paths_9f.py` pada `phase5m_top_paths.tcl`) dibuat untuk batasan paling ketat yang terpenuhi di kedua seed dan untuk yang pertama tidak terpenuhi.
