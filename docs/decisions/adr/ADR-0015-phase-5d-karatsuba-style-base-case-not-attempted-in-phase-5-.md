# ADR 0015: Fase 5d basis perkalian ala Karatsuba tidak dicoba di Fase 5; dipindah ke Fase 6

- Status: Accepted
- Tanggal: 2026-10-01
- Diputuskan oleh: Jevan, Team J5 (chat 2026-10-02, menjawab tiga pertanyaan ADR)

## Konteks
- ROADMAP Fase 5 mendaftar 5d (opsional): perkalian base-case ala Karatsuba, 4 perkalian modular sebagai ganti 5.
  ADR 0011 D3 membiarkan percobaan terbuka sampai setelah 5a / 5b; instruksi S3 hanya meminta usulan.
- Temuan yang dicatat di test plan (`evidence/phase05/test_plan.md`, 5d): `rtl/ntt/base_case_multiply.sv` bukan
  bagian inti NTT C3-P6 / C4. Tidak ada inti yang menginstansiasinya; inti C3 hanya mengerjakan NTT / INTT, jadi 5d
  tidak dapat mengubah kernel yang diukur Fase 5 (perkalian base-case pointwise termasuk datapath berikutnya).
- Penerimaan Fase 5 (ADR 0010, 0012) dinilai pada inti NTT: t_NTT dan t_INTT pada Fmax terukur, ALM <= 12.573.
  Unit 5d tidak mengubah keduanya. Jumlah DSP pengali adalah butir anggaran terpisah (ADR 0013 mencatat DSP 9 -> 18
  untuk Barrett).
- ROADMAP menempatkan pekerjaan jenis Karatsuba bersama butir aritmetika Fase 6 (perkalian pointwise di datapath penuh).

## Opsi yang dipertimbangkan
(a) Tidak dicoba di Fase 5; dipindah ke Fase 6 (tempat pengali base-case menjadi bagian datapath yang dapat diukur
    ujung ke ujung). Biaya: baris ablasi C4 untuk 5d tetap "tidak dicoba" (diizinkan test plan: "atau 'tidak dicoba'").
    Tidak ada upaya Fase 5 yang dihabiskan untuk unit di luar inti terukur.
(b) Dicoba sekarang sebagai unit mandiri `C4d` terhadap kompilasi mandiri `base_case_multiply.sv` yang dibekukan
    (`BCM-ref`), seperti dijelaskan test plan. Biaya: unit RTL baru, bukti menyeluruh atau terbatas atas
    (a0, a1, b0, b1, gamma), dua kompilasi Quartus tambahan (seed sesuai keputusan tim); hasilnya perbandingan
    DSP / ALM mandiri tanpa efek pada t_NTT, t_INTT, atau gerbang Fase 5.

## Keputusan
Opsi (a) diterima 2026-10-02 oleh Jevan, Team J5: 5d tidak dicoba di Fase 5 dan dipindah ke Fase 6.

## Konsekuensi
- Bila (a): baris matriks C4 5d = "tidak dicoba di Fase 5 (ADR 0015)"; `phase05.md` menyatakannya; rencana Fase 6
  membawa butir itu (tim memutuskan posisinya di sana).
- Bila (b): bagian test plan untuk `C4d` dijalankan dengan aturan adopsi sendiri yang ditetapkan sebelum mengukur.
- Matematika (C1) tidak tersentuh pada kedua opsi.

## Bukti
- `evidence/phase05/test_plan.md` (paragraf 5d, bagian tentang `C4d` / `BCM-ref`)
- `docs/decisions/adr/ADR-0011-phase-5-plan-decisions-d1-d8-and-the-5b-selection-rule.md` (D3)
- `docs/ROADMAP.md` (langkah bagian Fase 5)
