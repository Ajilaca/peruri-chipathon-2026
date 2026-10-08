# ADR 0017: Fase memori dan jadwal antara Fase 5 dan Fase 6 (PENDING 19): lingkup S6-S9, aturan, branch

- Status: Accepted
- Tanggal: 2026-10-02
- Diputuskan oleh: Jevan, Team J5 (chat 2026-10-02, menjawab tiga pertanyaan ADR)

## Konteks
- ADR 0010 (Accepted): 50 MHz adalah target proyek terbaik-upaya, bukan gerbang Fase 5; jalur kritis C3-P6 adalah
  pembacaan memori (MEASURED: 21,292 ns dari 29,345 ns, lalu `sub_mod` 4,348 ns dan DSP 3,705 ns,
  `evidence/phase05/baseline/c3p6_critical_path.md`). Fase 5 menetapkan jadwal, memori, L, dan P tetap.
- Hasil Fase 5 (`docs/results/phase05.md`): perubahan aritmetika menghemat area (C4b-B 9.166-9.208 ALM lawan C3-P6
  10.484-10.516) tetapi tidak menggeser Fmax melewati sebaran seed; kompilasi informasi pada 20,000 ns gagal untuk
  C3-P6 (setup -2,059 ns) dan C4b-B (-2,557 ns) (`evidence/phase05/closure/info_20ns.md`).
- Paket keputusan (`evidence/phase05/baseline/decision_package.md`) mendaftar tuas memori / pipeline dengan biaya
  ESTIMATE; ADR 0012 menetapkan aturan adopsi (t_NTT dan t_INTT pada median Fmax seed 1-6 lebih baik dari langkah
  sebelumnya, siklus konstan, ALM inti NTT <= 12.573).
- PENDING #19 menanyakan nama dan posisi fase yang memuat pekerjaan ini. Instruksi tim (2026-10-01, S5) meminta fase
  "memori dan jadwal" setelah Fase 5 dan sebelum Fase 6, berisi langkah S6-S9.
- Basis kerja untuk langkah di bawah: C4b-B (Barrett). ADR 0013 (Barrett) saat itu masih Proposed (PENDING #23); bila
  tim memilih Montgomery, basis berubah dan angka baseline diukur ulang.

## Opsi yang dipertimbangkan
(a) Fase terpisah antara Fase 5 dan Fase 6, dengan branch, test plan, artefak hasil, dan gerbang Approval sendiri
    (nama usulan: "Fase 5M: memori dan jadwal"; penomoran urusan tim, misalnya "Fase 5.5"). Biaya: satu fase lagi di
    roadmap dan satu persetujuan lagi; manfaat: jalur memori diubah di bawah aturan bukti yang sama seperti setiap
    fase sebelumnya, dan Fase 6 mulai dari basis terukur.
(b) Sub-fase di dalam Fase 6 (penjadwalan tingkat operasi). Biaya: mencampur perubahan timing tingkat kernel dengan
    jadwal tingkat operasi, sehingga hasil tidak bisa dikaitkan dengan satu perubahan; Fase 6 sudah punya lingkup sendiri.
(c) Tidak ada fase seperti itu: tetap di sekitar 35 MHz dan menganggap 50 MHz tidak terjangkau. Biaya: target proyek
    ADR 0010 dilepas tanpa langkah terukur yang mungkin mencapainya; tidak ada risiko RTL baru.

## Keputusan
Opsi (a) diterima 2026-10-02 oleh Jevan, Team J5: fase terpisah antara Fase 5 dan Fase 6, dengan isi dan aturan di
bawah. Nama usulan "Fase 5M: memori dan jadwal" dipakai sebagai nama kerja (jawaban memilih opsi (a), yang teksnya
mengusulkannya; tim boleh menamai ulang). Basis kerja: C4b-B (Barrett, ADR 0013 diterima).

Isi (tiap langkah satu perubahan, satu test plan ditulis sebelum mengukur, satu STOP untuk tim):
| Langkah | Perubahan | Aturan |
|---|---|---|
| S6 | INTT tanpa lintasan skala: bagi dua di tiap layer (3303 = 2^-7 mod q, 7 layer), `intt_halving()` acuan sama dengan `intt()` pada 256 vektor basis, basis x (q-1), vektor acak dan tepi; konstanta dari skrip; hapus S_SCALE dan pengali skala | ADR dengan argumen kesetaraan; `half_mod` menyeluruh atas 3.329 nilai; siklus INTT = siklus NTT; kontrol negatif (satu layer tanpa pembagian dua) harus gagal |
| S7 | Membelah read mux memori (tuas 1 paket keputusan: P -> 7, tanpa stall, +1 siklus) | scoreboard hazard ditambah kontrol negatif; adopsi ADR 0012 |
| S8 | Register jalur tulis (tuas 4: P -> 8, satu stall independen-data per transformasi) | adopsi ADR 0012 ditambah kompilasi informasi 20 ns |
| S9 | Studi M10K / baca-sinkron: hanya dokumentasi, tanpa RTL; kebutuhan port lawan M10K, opsi (bank 1R1W lebih banyak, dua koefisien per word, double-pumping, perubahan jadwal), syarat bukti bebas konflik, ALM / M10K berlabel ESTIMATE | tim memilih; tidak ada aturan adopsi (tanpa RTL) |

Aturan bersama: matematika tetap dikunci (C1); setiap file RTL mengikuti aturan RTL proyek; lint Verilator `-Wall` dan
slang; simulasi Verilator dan Icarus; Quartus seed 1-6 satu per satu di latar belakang; gerbang CRG penuh; satu commit
lokal per langkah, asisten tidak pernah push; kotak Approval hanya dicentang anggota tim. Alasan urutan yang diusulkan
(INFERENCE): S6 menghapus satu pengali dan satu lintasan (area, tanpa perubahan memori), S7 dan S8 menyasar segmen
kritis terukur, S9 adalah studi yang memutuskan apakah perubahan memori lebih besar layak menjadi fase terpisah.

Branch dan persetujuan: setelah tim menyetujui, branch baru dibuat dari hasil Fase 5 (nama usulan
`phase5m-memory-schedule`, atau sesuai keputusan penomoran). Catatan ini tidak membuatnya.

## Konsekuensi
- Bila diterima: PENDING #19 ditutup; `docs/ROADMAP.md` mendapat fase baru (kriteria selesai, folder evidence, gerbang
  Approval) dalam perubahan terpisah; Fase 6 mulai hanya setelah Approval fase ini.
- Bila ditolak: S6-S9 tidak dimulai; 50 MHz tetap target terbaik-upaya tanpa jalur yang direncanakan.
- Batas 12.573 ALM dan aturan siklus ADR 0012 tetap berlaku; melewati salah satunya perlu keputusan tim baru.
- Tuas 1 dan 4 bersama dapat menelan hingga sekitar 1.300 ALM pada kasus terburuk rentang per-tahap terukur
  (ESTIMATE, paket keputusan), dibanding margin terukur; hasil terukur yang memutuskan, bukan estimasi ini.

## Bukti
- `docs/decisions/adr/ADR-0010-*.md`, `ADR-0012-*.md`, `ADR-0013-*.md`
- `evidence/phase05/baseline/c3p6_critical_path.md`, `decision_package.md`, `stall_cycles.txt`
- `evidence/phase05/closure/info_20ns.md`, `docs/results/phase05.md`

## Catatan amandemen (2026-10-02, Jevan, Team J5; keputusan di atas tidak berubah)
"Gerbang CRG penuh" pada aturan bersama dijalankan sebagai regresi Fase 0-5 sekali, di S8, pada pohon akhir S6-S8
(bukan setelah tiap langkah); tiap langkah tetap menjalankan test khusus, bukti formal, dan seed Quartus sendiri.
Rincian: `evidence/phase05m/test_plan.md`, Amandemen A1.
