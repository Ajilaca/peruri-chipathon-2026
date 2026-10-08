# ADR 0026: Langkah bagian Fase 8 8a, 8b, 8c, dan 8d semuanya dikerjakan (menggantikan pelewatan 8a, 8c, dan 8d di ADR 0019 butir 2)

- Status: Accepted
- Tanggal: 2026-10-03
- Diputuskan oleh: Jose, Team J5, chat 2026-10-03: "8a 8b 8c 8d dikerjakan , adr tolong diganti , approval fase 7 acc"

## Konteks
- ADR 0019 (Accepted 2026-10-02, Jevan) butir 2 melewati Fase 6 dan langkah bagian Fase 8 8a (dua ronde per siklus),
  8c (matriks A on-the-fly) dan 8d (tumpang-tindih Keccak dengan aritmetika) untuk mencapai ML-KEM penuh sebelum
  Kamis 2026-10-08. Fase 6 dikembalikan oleh ADR 0024; bagian 8a/8c/8d dari pelewatan masih berlaku.
- Fase 7 (Keccak K0) selesai secara teknis dan kotak Approval-nya dicentang Jose pada 2026-10-03 (commit 1154a20,
  `docs/results/phase07.md`). K0 terukur (seed 1, kernel-only): 3.572 ALM, 1.653 register, 0 M10K, 0 DSP, 26 siklus
  per permutasi di sponge (24 sibuk), Fmax 56,99 MHz pada 40 ns.
- Langkah bagian Fase 8 di ROADMAP masing-masing "diukur dan ditinjau sendiri": 8a dua ronde per siklus (konfigurasi
  C5), 8b sampler streaming (CBD dari aliran PRF, SampleNTT dari aliran XOF), 8c matriks A dibangkitkan on the fly,
  8d tumpang-tindih sampling dengan aritmetika kernel; 8b sampai 8d bersama membentuk C6.
- Estimasi yang diberikan ke tim pada 2026-10-03 (ESTIMATE, dari laju Fase 6 dan 7): 8a sekitar 4-6 jam, 8b sekitar
  3-5 jam, 8c dan 8d sekitar 6-10 jam masing-masing; dengan Fase 9 (19-32 jam) totalnya melebihi apa yang muat
  sebelum 2026-10-08. Risikonya dinyatakan di chat 2026-10-03: tingkat T3 (ML-KEM penuh terhadap ACVP) adalah butir
  yang paling mungkin dipotong.

## Opsi yang dipertimbangkan
(a) Mempertahankan ADR 0019 seperti adanya: integrasi Fase 9 berikutnya, 8a/8c/8d hanya bila waktu tersisa.
(b) Mengerjakan keempat langkah bagian 8a, 8b, 8c, 8d (pilihan tim).
(c) Mengerjakan hanya 8a dan 8b.

## Keputusan
Opsi (b), oleh Jose (Team J5): 8a, 8b, 8c, dan 8d semuanya dikerjakan. Pelewatan 8a, 8c, dan 8d di ADR 0019 butir 2
digantikan (catatan amandemen 5 ADR 0019). Urutan: urutan ROADMAP 8a, 8b, 8c, 8d, masing-masing dengan test plan dan
aturan adopsi atau pernyataan "tanpa aturan" sendiri yang ditulis sebelum mengukur, masing-masing diukur dan ditinjau
sendiri (STOP setelah tiap langkah bagian menurut default yang disarankan PENDING #26, yang tetap terbuka). Segala hal
lain di ADR 0019 (tingkat pelaporan, peringanan proses, pembekuan evidence Rabu malam 2026-10-07) tidak berubah.

## Konsekuensi
- Ketergantungan dicatat sekarang, tidak diputuskan: 8c memerlukan entri matriks mencapai unit pointwise dari aliran
  sampler (penyimpanan Fase 6 saat ini menyimpan matriks di slot); 8d memerlukan antarmuka penjadwal antara
  sequencer Fase 6 dan sampler (ROADMAP: "antarmuka penjadwal"); keduanya belum dibangun. Keduanya dirancang di test
  plan masing-masing, dan bila 8c atau 8d terbukti tidak layak dalam waktu tersisa, itu dilaporkan sebagai "tidak
  selesai", tidak pernah sebagai hasil (C3).
- Fase 9 (integrasi, tingkat T2 dan T3) pindah ke belakang langkah bagian Fase 8 kecuali tim mengurutkan ulang; risiko
  jadwal untuk T2/T3 sebelum 2026-10-08 milik tim, dinyatakan di sini: langkah bagian Fase 8 diperkirakan 19-31 jam
  (ESTIMATE) ditambah Fase 9 19-32 jam tidak muat di hari yang tersisa pada 6-8 jam per hari. Tim boleh berhenti atau
  mengurutkan ulang di STOP mana pun.
- 8a menggantikan inti permutasi K0, jadi punya aturan adopsi (gaya ADR 0012, seed 1-6 pada 40 ns, seed K0 2-6
  dikompilasi untuk baseline) yang ditulis sebelum mengukur; file K0 tidak diedit, 8a adalah file baru.
- Baris ROADMAP C5 dan C6 (C6b, C6c, C6d) diisi saat langkah bagian diukur. PENDING #25 dan #26 tetap terbuka.

## Bukti
- Chat 2026-10-03 (dikutip di header); `docs/results/phase07.md` (Approval dicentang, commit 1154a20);
  `docs/decisions/adr/ADR-0019-minimal-path-to-a-full-ml-kem-768-core-before-thursday-2026-.md` butir 2;
  `docs/ROADMAP.md` Fase 8.

## Catatan amandemen 1 (2026-10-03, chat, tanpa nama: "8b melakukan keduanya saja jadi pertama kita test 1 siklus dan setelah itu 2 siklus setelah itu selesai baru kita mulai 8c"; "tidak perlu menanyakan permisi, lakukan hingga fase 8 beres semua hingga 8d selesai dan kemudian buat report dan result seperti biasa baru berhenti")
Dua hal, dicatat tanpa mengedit keputusan di atas: (1) langkah bagian 8b dikerjakan pada dua lebar keluaran, W1 (satu
koefisien per siklus) lalu W2 (dua), dan aturan yang ditulis sebelum mengukur memilih di antara keduanya
(`evidence/phase08/8b/test_plan_8b.md`); (2) STOP setelah tiap langkah bagian pada paragraf Keputusan tidak diambil
antara 8b, 8c, dan 8d: ketiganya dikerjakan berurutan, masing-masing dengan rencana sendiri yang ditulis sebelum
pengukurannya, dan laporan serta hasil ditulis di akhir. Pertanyaan PENDING #25 dan #26 tetap terbuka.
