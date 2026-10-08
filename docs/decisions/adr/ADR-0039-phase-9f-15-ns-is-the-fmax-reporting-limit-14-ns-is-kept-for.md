# ADR 0039: Fase 9F: 15 ns adalah batas pelaporan Fmax; 14 ns disimpan untuk dipertimbangkan nanti

- Status: Accepted
- Tanggal: 2026-10-04
- Diputuskan oleh: Faza Dzil (Team J5), chat 2026-10-04

## Konteks
ADR 0036 (Accepted, Faza Dzil) meminta Fmax dilaporkan pada batasan lebih ketat di samping gerbang 40 ns dan menyebut
15 ns. Langkah S0 (`evidence/phase9m/batch1/9f0/result_9f0.md`) mengukur inti 9M-1 pada 16, 15, 14, dan 13 ns: 15 dan
14 ns terpenuhi di kedua seed, 13 ns di satu dari dua; batas desain itu ada di antara 13 dan 14 ns. Langkah S1 mengukur
K1 pada 15 ns (terpenuhi di 6 dari 6 seed, median Fmax 73,07 MHz, `batch1/9f1/result_9f1.md`); K1 tidak dikompilasi di
bawah 15 ns.

## Opsi yang dipertimbangkan
1. Melaporkan dan membandingkan hanya pada 15 ns (enam seed per konfigurasi), menyimpan 14 ns sebagai titik nanti.
2. Juga menyapu setiap konfigurasi (K1, K1b, langkah berikutnya) pada 14, 13 ns dan di bawahnya sampai kegagalan
   pertama: 4-6 kompilasi lagi per konfigurasi (ESTIMATE 2-3 jam masing-masing).

## Keputusan
Faza Dzil, chat 2026-10-04: "kita ambil 15 ns saja sebagai batas; 14 ns bisa jadi bahan pertimbangan karena pass namun
bisa dikerjakan nanti".
- 15 ns adalah batasan tempat Fmax dan latensi dilaporkan dan dibandingkan di Fase 9F (enam seed per konfigurasi, di
  samping gerbang 40 ns).
- 14 ns disimpan untuk dipertimbangkan: inti 9M-1 memenuhinya di kedua seed (S0); tidak diukur untuk K1, K1b, atau
  langkah berikutnya sekarang dan dapat dikerjakan nanti.
- Tidak ada sapuan lebih lanjut di bawah 15 ns yang dimulai untuk K1b atau langkah Batch 2 kecuali tim memintanya.

## Konsekuensi
S1b (K1b) dikompilasi pada 40 ns dan 15 ns, enam seed masing-masing, seperti di rencana; aturan adopsinya memakai
hasil 15 ns. Pernyataan "timing terpenuhi pada 15 ns" memerlukan keenam seed; 14 ns tetap pernyataan untuk inti 9M-1 di
dua seed saja (S0), diberi label demikian. Latensi tetap perhitungan tim dari timing statis kernel-only; tidak ada
klaim papan.

## Bukti
`evidence/phase9m/batch1/9f0/result_9f0.md`, `evidence/phase9m/batch1/9f1/result_9f1.md`,
`docs/decisions/adr/ADR-0036-phase-9f-fmax-plan-s0-s1-s2-latency-rule-and-reporting-at-a-.md`.
