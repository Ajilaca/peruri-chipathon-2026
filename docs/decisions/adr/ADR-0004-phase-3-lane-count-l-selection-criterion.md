# ADR 0004: Kriteria pemilihan jumlah lajur (L) Fase 3

- Status: Accepted
- Diubah 2026-10-01 oleh ADR 0009: nilai 25 % / 10.478 ALM di bawah digantikan untuk inti NTT mulai Fase 4
  oleh anggaran desain 30 % / 12.573 ALM. Teks di bawah dibiarkan apa adanya sebagai catatan keputusan 2026-09-29.
- Tanggal: 2026-09-29
- Diputuskan oleh: Faza Dzil, Team J5

## Konteks
`docs/ROADMAP.md` Fase 3 menyapu jumlah lajur L dalam {1, 2, 4, 8} di atas memori berbank Fase 2 (konfigurasi
C2-L1..C2-L8), dan mengukur ALM, register, M10K, DSP, Fmax, dan jumlah siklus untuk tiap L. Spesifikasi Fase 3
mensyaratkan: "Kriteria seleksi (misalnya AT terendah dalam anggaran sumber daya tertentu) ditulis di ADR
sebelum sapuan diukur." Catatan ini ada untuk menetapkan kriteria itu sebelum empat kompilasi Quartus berjalan,
supaya pilihan L tidak diambil dengan melihat tabel perbandingan setelahnya.

Dua kondisi sebelumnya memengaruhi keputusan ini dan harus disebut, bukan disembunyikan:
1. Fase 1 (C0) dan Fase 2 (C1) sama-sama GAGAL timing (CRG-9) pada clock sementara 20,000 ns; belum ada ADR clock
   target. Angka area x waktu (AT) yang dihitung dari Fmax yang tidak memenuhi timing hanya perbandingan relatif
   antar L, bukan klaim mutlak bahwa desain memenuhi target clock apa pun.
2. Target M10K Fase 2 tidak tercapai (0/553 M10K; keterbatasan pembacaan asinkron). Bila ini masih belum selesai
   saat sapuan L berjalan, keempat konfigurasi L juga akan menunjukkan 0 M10K, dan pemakaian ALM akan naik
   bersama L terutama lewat replikasi memori berbasis LUT, bukan banking block-RAM. Itu mengubah arti
   "anggaran sumber daya" untuk sapuan ini dan harus diputuskan bersama ADR ini, bukan diserap diam-diam.

## Opsi yang dipertimbangkan
Contoh dalam spesifikasi Fase 3 adalah "AT terendah dalam anggaran sumber daya tertentu". Konkretnya, untuk
diputuskan tim J5:

1. AT (Area x Time) terendah, tanpa anggaran tetap - untuk tiap L, AT = ALM_terpakai x (1 / Fmax_terukur). Pilih L
   dengan AT terkecil. Peringkat satu angka yang sederhana; tetapi pada Cyclone V 5CSEBA6U23I7 (batas datasheet
   41.910 ALM), L besar masih bisa menang di AT sambil menghabiskan bagian device yang tidak praktis, tanpa menyisakan
   ruang untuk Keccak, sampler, atau logika protokol di fabric yang sama.
2. AT terendah dalam anggaran ALM tertentu (misalnya menyisihkan X % dari 41.910 ALM untuk blok NTT/INTT;
   menggugurkan L yang melewatinya, lalu meranking sisanya dengan AT). Sesuai contoh spesifikasi. Memerlukan tim
   menyatakan persentase anggaran sekarang, sebagai bagian ADR ini, bukan sebagai filter setelahnya.
3. Throughput tertinggi (total siklus NTT+INTT+pointwise terendah) dalam anggaran ALM yang sama, mengabaikan
   perbedaan Fmax antar L (karena C0-C1 belum memenuhi timing, metrik throughput dalam siklus bisa dibilang lebih
   jujur daripada yang dibobot Fmax saat ini).
4. Biarkan L dapat dikonfigurasi, tunda pilihan - kirim keempat konfigurasi, jadikan L parameter waktu sintesis, dan
   biarkan Fase 4+ (pipelining) atau proposal akhir memilih sesuai konteks. Memenuhi "menjaga L tetap dapat
   dikonfigurasi" yang diizinkan kriteria PASS Fase 3, tetapi menunda keputusan yang diminta spesifikasi untuk
   ditetapkan sebelum pengukuran.

Belum ada yang diukur (belum ada evidence Quartus C2-L* saat ini ditulis); ADR ini tentang aturan, bukan hasil.

## Keputusan
Kriteria dua tahap, berurutan menurut prioritas:

1. Utama - minimalkan jumlah siklus, dengan anggaran ALM 25 % dari device target (5CSEBA6U23I7, batas datasheet
   41.910 ALM) -> anggaran = 10.478 ALM. Setiap L yang kompilasi Quartus C2-L<n>-nya melewati 10.478 ALM gugur
   berapa pun jumlah siklusnya. Di antara L yang tersisa (dalam anggaran), yang punya total siklus terendah
   (NTT + INTT + perkalian titik, dari cocotb; syarat siklus identik dari Fase 2 tetap berlaku di dalam tiap L)
   menang. Ini opsi 3 dari daftar di atas, dipilih karena timing C0/C1 masih belum terpenuhi, sehingga siklus
   adalah metrik yang lebih jujur saat ini daripada hasil kali AT berbobot Fmax.
2. Sekunder - hanya informasi, tidak otomatis menimpa pilihan utama. Begitu ada clock terbatas yang valid secara
   timing (yaitu begitu ADR clock target ada dan sebuah konfigurasi benar-benar memenuhi timing), evaluasi ulang
   hasil kali AT (ALM x 1/Fmax) dari L terpilih utama terhadap anggaran 10.478 ALM yang sama, untuk catatan. Bila
   evaluasi sekunder ini menyarankan L lain lebih baik di AT, itu tidak diterapkan otomatis - mengubah L terpilih
   setelah ADR ini memerlukan ADR baru (atau pembaruan ADR ini) yang menyebut alasannya.

Bila tidak ada L yang masuk anggaran 10.478 ALM, atau bila target M10K Fase 2 (keterbatasan pembacaan asinkron,
`docs/results/phase02.md`) masih belum selesai saat sapuan berjalan (semua konfigurasi L lalu bersaing dengan
replikasi memori berbasis LUT, bukan banking block-RAM), itu dilaporkan sebagai temuan di
`docs/results/phase03.md`, bukan diserap diam-diam - ADR ini tidak memutuskan lebih dulu apa yang terjadi bila
anggaran tidak layak.

## Konsekuensi
- Sapuan Fase 3 harus menjalankan keempat L dalam {1,2,4,8} lewat Quartus dan cocotb apa pun hasil kriteria
  utama (kriteria PASS menuntut keempatnya diukur dan dibandingkan), lalu menerapkan filter anggaran ALM dan
  peringkat jumlah siklus untuk memilih satu.
- `docs/results/phase03.md` harus menunjukkan: nilai anggaran ALM (10.478), L mana yang lolos atau gagal anggaran,
  jumlah siklus kandidat dalam anggaran, L terpilih, dan - begitu timing valid di fase berikutnya - evaluasi ulang
  AT sekunder, ditandai eksplisit sebagai informasi.
- Setiap perubahan L terpilih di masa depan harus menyebut ADR ini dan menggantikannya atau menambah ADR lanjutan;
  tidak boleh berupa perubahan diam-diam di `docs/ROADMAP.md` saja.
- Ini tidak menyelesaikan PENDING #3 (DMA lawan transfer memory-mapped) atau ADR clock target yang belum ada;
  keduanya tetap terbuka dan disebut, bukan diputuskan, di sini.

## Bukti
Spesifikasi Fase 3 (ditempel tim, 2026-09-29, bagian Fase 3 di `docs/ROADMAP.md`).
Status timing Fase 1/2: `docs/results/phase01.md`, `docs/results/phase02.md`.
