# ADR 0005: Menerapkan seleksi L ADR 0004 pada konfigurasi tambahan C2-K2-K1

- Status: Accepted
- Tanggal: 2026-09-30
- Diputuskan oleh: Faza Dzil, Team J5

## Konteks
ADR 0004 (Accepted) menetapkan kriteria jumlah lajur Fase 3: minimalkan jumlah siklus di antara nilai L yang ALM
Quartus-nya dalam 25 % device (10.478 ALM, ADR 0004 / perhitungan tim). Diterapkan pada sapuan C2
(`docs/results/phase03.md`), L=8 (MEASURED 11.446 ALM, `evidence/quartus/C2-L8.md`) gugur dan L=4 adalah hasil yang
dilaporkan (menunggu persetujuan tim).

Tim kemudian menyetujui dua eksperimen optimasi tambahan pada C2, dijalankan sebagai konfigurasi terpisah agar
baseline C2 tetap dapat direproduksi:
- K2 (`evidence/phase03/k2_experiment.md`): counter sub-siklus lebih sempit.
  Valid tetapi tidak cukup sendirian (L=8: MEASURED 11.232 ALM, `evidence/quartus/C2-L8-K2.md`).
- K1 (`evidence/phase03/k1_experiment.md`): satu pengali modular bersama per butterfly sebagai ganti satu per
  mode, di atas K2 (konfigurasi C2-K2-K1). Ini mengubah datapath butterfly, jadi di luar lingkup implementasi
  Fase 3 yang tertulis ("butterfly, aritmetika, dan memori seperti Fase 2"); tim menyetujuinya sebagai
  eksperimen tambahan atas dasar itu.

MEASURED C2-K2-K1 (Quartus, `evidence/quartus/C2-K2-K1-L{1,2,4,8}.md`; device/batasan/seed sama seperti C2;
simulasi bit-exact di dua simulator; jumlah siklus identik dengan C2):

| L | ALM | Dalam 10.478? | Siklus NTT / INTT |
|---|---|---|---|
| 1 | 5.566 | ya | 897 / 1153 |
| 2 | 5.374 | ya | 449 / 705 |
| 4 | 6.775 | ya | 225 / 481 |
| 8 | 9.754 | ya (724 di bawah) | 113 / 369 |

Menerapkan aturan ADR 0004 tanpa perubahan pada keluarga ini memberi L=8 (siklus terendah, dalam anggaran).
Pemeriksaan AT sekunder ADR 0004 tetap belum bisa dijalankan: tidak ada konfigurasi yang memenuhi timing pada clock
mana pun.

Butir terbuka yang berkaitan dengan keputusan ini (dari catatan K1): packing ALM oleh fitter bervariasi hingga
sekitar 370 ALM (MEASURED, `k1_entity_breakdown.txt`, K2-L1) antar kompilasi logika yang identik, dibanding margin
724 ALM; K1 menurunkan Fmax sedikit pada L=1/2/4 (MEASURED, file evidence Quartus yang sama).
Sudah ditutup sejak draf pertama: kesetaraan `butterfly` dan `butterfly_shared` ditetapkan oleh bukti formal dengan
pengali diabstraksikan (PASS, dua kontrol negatif FAIL) dan oleh simulasi menyeluruh atas semua
73.785.560.578 masukan (0 selisih); lihat `k1_experiment.md`, catatan 5.
Juga ditutup: celah formal inti untuk L>1 adalah artefak harness; C2-K2-K1 kini PASS k-induction pada
L=1/2/4/8 untuk bank_overflow_o, handshake busy/done, dan rentang counter (`formal_rerun.md`).

## Opsi yang dipertimbangkan
1. Mengadopsi C2-K2-K1 sebagai keluarga konfigurasi Fase 3 dan memilih L=8 berdasarkan aturan ADR 0004.
   Throughput: 8 butterfly/siklus, NTT 113 / INTT 369 siklus (MEASURED di simulasi, `k1_cocotb_regression.txt`).
   Biaya: menerima perubahan butterfly di luar lingkup Fase 3 yang tertulis, dicatat di sini sebagai penyimpangan
   yang disengaja; Fase 4 lalu mulai dari C2-K2-K1-L8.
2. Mengadopsi C2-K2-K1 tetapi tetap L=4 (misalnya untuk ruang ALM lebih besar bagi Keccak/sampler, atau timing,
   yang lebih buruk pada L lebih besar). Bertentangan dengan aturan ADR 0004 kecuali kriteria baru dinyatakan.
3. Mempertahankan hasil C2 (L=4) untuk Fase 3 dan membawa K1 ke fase berikutnya (misalnya Fase 5, optimasi
   aritmetika). Menjaga Fase 3 tetap dalam lingkup tertulis; L=8 ditinjau lagi nanti.
4. Menunda (misalnya sampai sapuan seed mengukur margin packing ALM).

## Keputusan
Opsi 1. Tim mengadopsi konfigurasi teroptimasi C2-K2-K1 sebagai keluarga konfigurasi Fase 3 dan, dengan menerapkan
aturan ADR 0004 tanpa perubahan, memilih L = 8 (MEASURED 9.754 ALM, dalam anggaran 10.478 ALM; NTT 113 / INTT 369
siklus; 8 butterfly per siklus).

Ini penyimpangan yang disengaja dan tercatat dari lingkup implementasi Fase 3 yang tertulis ("butterfly,
aritmetika, dan memori seperti Fase 2"): K1 mengubah datapath butterfly (satu pengali bersama per butterfly).
Metode reduksi modular (`modmul_reduce.sv`) dan setiap parameter FIPS 203 yang dikunci tidak berubah (ADR 0002 tetap
berlaku). ADR 0004 sendiri tidak diedit; catatan ini menerapkannya.

## Konsekuensi
- Fase 4 (pipelining) mulai dari C2-K2-K1 pada L = 8 (`rtl/ntt/ntt_core_c2_k2_k1.sv`,
  `rtl/ntt/butterfly_shared.sv`), bukan dari C2 pada L = 4. Hasil ADR 0004 sebelumnya pada keluarga C2
  (L = 4, `docs/results/phase03.md` Bagian 3) disimpan sebagai pembanding baseline terukur, bukan titik operasi
  terpilih.
- RTL C2, C2-K2, dan C2-K2-K1 beserta file evidence-nya tetap di repository agar perbandingan dapat direproduksi.
- Diterima dengan batas yang diketahui ini, yang tidak diselesaikan keputusan ini: timing tidak terpenuhi untuk
  semua konfigurasi (Fase 4; belum ada ADR clock target); pemeriksaan AT sekunder ADR 0004 tetap belum bisa
  dijalankan; margin 724 ALM di bawah anggaran lebih besar dari, tetapi tidak jauh di atas, ayunan packing fitter
  terbesar yang teramati (sekitar 370 ALM) dan belum ada sapuan seed; 0 blok M10K dipakai.
- Setiap perubahan L terpilih atau keluarga konfigurasi di masa depan memerlukan ADR baru.
- Keputusan ini tidak mencentang kotak Approval `docs/results/phase03.md`; itu tetap persetujuan manusia yang
  terpisah.

## Bukti
- `evidence/phase03/k1_experiment.md`, `k1_entity_breakdown.txt`,
  `k1_cocotb_regression.txt`, `k1_formal.txt`
- `evidence/quartus/C2-K2-K1-L{1,2,4,8}.md`
- `evidence/phase03/k2_experiment.md`,
  `evidence/quartus/C2-L{1,2,4,8}-K2.md`
- `docs/decisions/adr/ADR-0004-phase-3-lane-count-l-selection-criterion.md`, `docs/results/phase03.md`
