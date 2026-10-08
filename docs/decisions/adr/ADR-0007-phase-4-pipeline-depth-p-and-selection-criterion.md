# ADR 0007: Kedalaman pipeline P Fase 4 dan kriteria seleksi

- Status: Accepted
- Diubah 2026-10-01 oleh ADR 0009: syarat kandidat 3 memakai 12.573 ALM (30 %) sebagai ganti 10.478 ALM; aturan,
  himpunan kandidat, dan syarat lain tidak berubah. Teks di bawah dibiarkan apa adanya sebagai catatan 2026-09-30.
- Tanggal: 2026-09-30
- Diputuskan oleh: Faza Dzil, Team J5

## Konteks
Fase 4 (`docs/ROADMAP.md`) mem-pipeline butterfly dari konfigurasi terpilih, C2-K2-K1 pada L = 8
(ADR 0005), sebagai konfigurasi C3: "kedalaman pipeline P sebagai parameter pada himpunan kecil terdokumentasi;
penanganan hazard antar layer NTT (stall atau jadwal), dengan biaya stall dihitung. Tanpa perubahan aritmetika;
tanpa penggabungan layer." Kriteria PASS meminta ADR untuk P terpilih. Seperti ADR 0004 untuk L, himpunan nilai
P dan aturan memilih di antaranya harus ditetapkan sebelum apa pun diukur.

Definisi yang diusulkan. P = jumlah tahap register pada jalur satu butterfly dari siklus alamatnya
diterbitkan sampai siklus hasilnya ditulis ke memori. P = 0 adalah C2-K2-K1 hari ini: baca, hitung, dan tulis
dalam satu siklus. Butterfly yang diterbitkan pada siklus t menulis pada siklus t + P.

Fakta yang tersedia hari ini (tidak ada kompilasi baru untuk ADR ini):
- Jalur terburuk MEASURED dari titik awal P = 0, per blok
  (`evidence/phase04/k1_l8_worst_path_breakdown.md`): delay data 129,6 ns =
  pembangkit alamat sekitar 5 ns, akses memori (arbitrasi slot bank di 16 port, read mux)
  sekitar 57 ns, logika pra/pasca butterfly sekitar 5 ns, pengali sekitar 4 ns, pembagi (`%` di
  `modmul_reduce`) sekitar 44 ns, jalur tulis sekitar 9 ns.
  Posisi register kandidat yang mengikutinya: (c1) setelah pembangkit alamat / pemetaan bank,
  (c2) di dalam jalur akses memori, (c3) setelah pembacaan memori, (c4) antara pengali dan pembagi,
  (c5) di dalam rantai pembagi, (c6) sebelum penulisan memori.
- Hazard, dari pemeriksaan menyeluruh atas jadwal lajur yang ada
  (`evidence/phase04/layer_boundary_slack.txt`, perhitungan tim): di dalam sebuah
  layer setiap alamat dibaca dan ditulis tepat sekali, jadi tidak ada hazard read-after-write di dalam layer
  untuk P mana pun. Di batas layer, layer berikutnya tidak boleh membaca alamat yang penulisannya masih di
  pipeline; untuk L = 8 batas tersempit punya slack 7 siklus di kedua arah, jadi
  P ≤ 7 tidak memerlukan stall di batas layer mana pun dengan jadwal tidak berubah. P > 7 akan memerlukan siklus
  stall atau jadwal yang diubah.
- ALM: C2-K2-K1-L8 ada di 9.754 ALM, 724 di bawah anggaran 10.478 ALM ADR 0004; packing fitter saja pernah
  menggeser total hingga sekitar 370 ALM (`k1_experiment.md`, catatan 1).

Konsekuensi pipelining yang berlaku untuk setiap opsi di bawah:
- Latensi / siklus. Untuk P ≤ 7 (tanpa stall batas): NTT = 7 x 16 sub-siklus + P siklus untuk mengosongkan
  pipeline + overhead yang ada, yaitu 113 + P siklus (ESTIMATE dari struktur FSM, akan diukur di simulasi). INTT
  juga punya lintasan skala 256 siklus x3303 (369 siklus hari ini); naik sebesar P untuk pengosongan, dan lebih
  bila lintasan skala memakai ulang pengali yang di-pipeline. Jumlah siklus tetap tidak bergantung data (syarat
  waktu-konstan) dan diukur ulang per P.
- Throughput. Yang penting adalah waktu per transformasi = siklus(P) / Fmax(P). Pipeline lebih dalam menambah
  beberapa siklus (sekitar 1-6 % pada L = 8 untuk P ≤ 7) dan hanya bermanfaat bila Fmax naik lebih dari itu.
- Sumber daya. Setiap tahap yang membawa register datapath 2 x 12 bit data dan 2 x 8 bit alamat tulis per
  lajur, sekitar 320 flip-flop per tahap pada L = 8 (ESTIMATE dari lebar sinyal; tahap di sisi alamat membawa
  lebih sedikit, tahap di dalam pembagi membawa sisa parsial per lajur). Register sering masuk ke ALM yang sudah
  terpakai, tetapi itu tidak dijamin; margin 724 ALM bisa habis.
- Port memori. Hari ini tiap port membaca dan menulis alamat yang sama pada siklus yang sama. Dengan P > 0 satu
  siklus membawa pembacaan satu himpunan butterfly dan penulisan himpunan sebelumnya, jadi satu bank melihat
  hingga 2 pembacaan dan 2 penulisan alamat berbeda per siklus. Memori flip-flop bisa melayaninya, tetapi
  `poly_mem_multiport` memerlukan pengalamatan baca dan tulis terpisah (file varian baru; memori C2 tetap
  dibekukan), dan bukti Fase 2/3 "paling banyak 2 akses per bank per siklus" lalu berlaku untuk pembacaan dan
  penulisan secara terpisah, bukan sebagai satu anggaran 2-port. Pembacaan teregistrasi (c3) juga prasyarat
  inferensi M10K, tetapi 2R + 2W per bank tidak dipetakan ke satu M10K true-dual-port; M10K tetap pertanyaan
  terpisah (tidak diputuskan di sini).
- Verifikasi. Hanya file RTL baru (C2, C2-K2, dan C2-K2-K1 tetap dibekukan); bit-exact terhadap model acuan di
  kedua simulator untuk setiap P; test khusus di batas layer; jumlah siklus konstan; properti formal
  `bank_overflow_o` dinyatakan ulang untuk jadwal baca dan tulis terpisah.

## Opsi yang dipertimbangkan
### A. Nilai P mana yang dibangun dan diukur
1. P ∈ {0, 1, 2, 3}, register hanya di batas blok (c1, c3, c4, c6; tidak ada di dalam jalur akses memori atau
   pembagi).
   Untuk: perubahan RTL terkecil; jelas dalam "tanpa perubahan aritmetika"; 4 revisi Quartus.
   Melawan: menurut rincian jalur, periode clock tidak bisa turun di bawah blok tunggal terpanjang, sekitar
   57 ns (sekitar 17 MHz, ESTIMATE) - paling banter sekitar 2x Fmax sekarang, jauh dari 50 MHz dan kurang dari
   25 MHz.
2. P ∈ {0, 2, 4, 6}, register juga di dalam jalur akses memori (c2) dan pembagi (c5).
   Untuk: satu-satunya jenis himpunan yang dapat mendekati 20-40 ns menurut estimasi; semua nilai ≤ 7, jadi tidak
   ada stall batas; 4 revisi.
   Melawan: perubahan RTL lebih besar (varian memori dengan arbitrasi slot bertahap; `%` ditulis sebagai logika
   bertahap eksplisit atau pembagi yang diinstansiasi dengan tahap pipeline). Memerlukan keputusan tim bahwa
   register di dalam reduksi - metode sama, hasil sama, diperiksa menyeluruh terhadap `modmul_reduce` - bukan
   "perubahan aritmetika" dalam arti ROADMAP. Register lebih banyak, jadi risiko anggaran ALM lebih besar.
3. P ∈ {0, 1, 2, 4, 7}: sapuan lebih lebar sampai kedalaman bebas-stall terbesar.
   Untuk: menunjukkan seluruh kurva, termasuk di mana hasilnya menurun.
   Melawan: 5 revisi (sekitar 16 menit masing-masing pada L = 8) dan 5 varian RTL untuk diverifikasi; P = 7 tepat
   di batas hazard, jadi test batasnya paling berisiko.
4. Dibantu retiming: tambahkan P tahap register biasa di satu batas dan biarkan Quartus memindahkannya.
   Untuk: RTL minimal; posisi potongan dipilih alat.
   Melawan: hasil bergantung alat dan lebih sulit dijelaskan; apakah Quartus Prime Lite 25.1std melakukan retiming
   melewati pembagi yang diinferensi dan blok DSP pada device ini belum dicoba - perlu kompilasi percobaan sebelum
   apa pun direncanakan di sekitarnya.

Posisi register tepat untuk tiap P adalah bagian test plan Fase 4 (CRG-4), himpunan mana pun yang dipilih.

### B. Cara memilih P setelah diukur
1. P terkecil yang memenuhi clock target ADR 0006 (timing terpenuhi di semua corner), di antara P yang
   bit-exact, siklus konstan, dan dalam anggaran ALM. Bila tidak ada P yang memenuhi: laporkan, jangan pilih apa
   pun, tim memutuskan. Memerlukan ADR 0006 menetapkan target mutlak.
2. Waktu per NTT minimum, siklus(P) / Fmax(P) (Fmax Slow-corner dari panel Fmax Summary), di antara P yang
   bit-exact, siklus konstan, dan dalam anggaran ALM; INTT dilaporkan di sampingnya; hasil hampir seri jatuh ke P
   lebih kecil. Bekerja tanpa target mutlak, tetapi mengutip latensi pada Fmax terukur, bukan pada clock terbatas.
3. Fmax tertinggi dalam anggaran ALM. Sederhana; mengabaikan siklus tambahan.

Saran draf pertama, digantikan oleh Keputusan di bawah: B.1 sebagai aturan utama bila ADR 0006 menetapkan target
mutlak, B.2 bila tidak. Tim memilih B.2, dengan "timing terpenuhi pada 40,000 ns" sebagai syarat menjadi kandidat
(lihat Keputusan).

## Keputusan
Himpunan P: opsi A.2 - P ∈ {0, 2, 4, 6}.
- Tahap register diperbolehkan di dalam jalur akses memori dan di dalam pembagi, selain di batas blok.
- Fungsi matematika tidak boleh berubah: setiap P menghasilkan hasil NTT/INTT yang sama bit demi bit dengan model
  acuan (dan dengan P = 0). Pipelining hanya boleh mengubah timing dan latensi. Tidak ada perubahan pada q, hasil
  metode reduksi, nilai twiddle, atau besaran FIPS 203 lain (ADR 0002).
- P = 0 adalah konfigurasi C2-K2-K1 L = 8, dikompilasi ulang dengan batasan Fase 4 dari ADR 0006 agar keempat
  revisi memakai satu batasan dan seed.

Aturan seleksi: opsi B.2 - waktu per NTT minimum - diterapkan hanya pada kandidat yang memenuhi syarat.

Langkah 1 - ukur semuanya. Keempat nilai P dibangun, diverifikasi, dan dikompilasi sebelum aturan diterapkan;
tidak ada yang dipilih dari sapuan parsial.

Langkah 2 - himpunan kandidat. Sebuah nilai P adalah kandidat hanya bila keempat syarat terpenuhi:
  1. bit-exact: PASS (kedua simulator, terhadap model acuan);
  2. jumlah siklus konstan: PASS;
  3. ALM ≤ 10.478 (fitter Quartus);
  4. timing terpenuhi pada 40,000 ns (milestone Fase 4 ADR 0006): slack setup terburuk tidak negatif dan slack
     hold terburuk tidak negatif di setiap corner yang dilaporkan Timing Analyzer.

Langkah 3 - besaran yang dibandingkan.
- siklus_NTT(P): jumlah siklus NTT terukur di simulasi (start sampai done; jumlah sama di kedua simulator dan untuk
  setiap masukan, menurut syarat 2).
- Fmax(P): Fmax terendah di antara hasil slow-corner yang benar-benar dilaporkan Fmax Summary Timing Analyzer
  untuk `clk_i` pada revisi itu, yaitu

      Fmax(P) = min atas setiap slow corner c yang dilaporkan dari  Fmax_c(P)

  (pada kompilasi sejauh ini slow corner yang dilaporkan adalah Slow 1100mV 100C dan Slow 1100mV −40C; tidak ada
  corner yang diasumsikan bila tidak ada di laporan). Ini dipilih sebagai nilai slow-corner kasus terburuk: clock
  yang bisa dijalankan desain harus bertahan di slow corner paling lambat, jadi angka yang lebih pesimistis yang
  dipakai. Nilai diambil sebagaimana tercetak di laporan, dalam MHz.
- Waktu per NTT, dalam mikrodetik (siklus dibagi MHz):

      t_NTT(P) = siklus_NTT(P) / Fmax(P)

- Dilaporkan di samping untuk setiap P, kandidat atau bukan, tetapi tidak dipakai untuk seleksi:

      t_INTT(P) = siklus_INTT(P) / Fmax(P)

Langkah 4 - seleksi dengan aturan hampir-seri. Misalkan C himpunan kandidat dan

      t_min = min atas P di C dari t_NTT(P)
      d(P)  = ( t_NTT(P) − t_min ) / t_min          untuk P di C

  Sebuah kandidat hampir seri dengan yang terbaik bila d(P) ≤ 0,05 (waktu per NTT-nya paling banyak 5 % di atas
  minimum global t_min pada himpunan kandidat; kandidat tidak dibandingkan berpasangan). Kedalaman terpilih adalah
  P terkecil seperti itu:

      P_terpilih = min { P di C : d(P) ≤ 0,05 }      (setara  t_NTT(P) ≤ 1,05 x t_min)

  Jadi kandidat dengan t_NTT minimum dipilih kecuali ada P lebih kecil dalam 5 % darinya, dalam hal itu P yang
  lebih kecil dipilih. Perbandingan memakai hasil bagi yang tidak dibulatkan.

Bila C kosong (tidak ada P yang memenuhi keempat syarat), tidak ada P yang dipilih otomatis: semua hasil terukur
dilaporkan dan tim dimintai keputusan.

## Konsekuensi
- Aturan kini konsisten dengan ADR 0006: P yang tidak memenuhi timing pada 40,000 ns tidak bisa dipilih, jadi
  P terpilih selalu memenuhi milestone Fase 4 (CRG-9 PASS untuk revisi itu).
- P = 0 diukur dan dilaporkan sebagai referensi tetapi tidak diharapkan menjadi kandidat: Fmax titik awal adalah
  7,68 MHz pada batasan sementara (MEASURED, `evidence/quartus/C2-K2-K1-L8.md`), jauh di bawah 25 MHz yang
  diperlukan 40,000 ns.
- Bila tidak ada P yang memenuhi keempat syarat - misalnya tidak ada P ∈ {2, 4, 6} yang memenuhi 40,000 ns, atau
  setiap P > 0 melewati 10.478 ALM - tidak ada yang dipilih; pengukuran dilaporkan dan tim memutuskan. Keduanya
  mungkin terjadi: estimasi jalur menyarankan sekitar 4 tahap diperlukan untuk 40 ns, dan margin 724 ALM titik awal
  tidak jauh di atas ayunan packing fitter yang teramati (sekitar 370 ALM).
- Karena register boleh masuk ke pembagi, `%` di `modmul_reduce.sv` harus diganti, di file baru, dengan bentuk
  bertahap yang dapat menampung register. `modmul_reduce.sv`, `butterfly.sv`, `butterfly_shared.sv`,
  `poly_mem_multiport.sv`, dan inti C2 / C2-K2 / C2-K2-K1 tetap dibekukan; reducer bertahap harus ditunjukkan
  sama dengan `modmul_reduce` untuk setiap a, b di [0, q) (3329² = 11.082.241 pasangan masukan, cukup kecil
  untuk diperiksa menyeluruh) sebelum dipakai.
- Karena register boleh masuk ke jalur akses memori, varian memori baru dengan pengalamatan baca dan tulis terpisah
  diperlukan (Konteks, "Port memori"); properti kapasitas bank dibuktikan ulang untuk jadwal baca dan jadwal tulis
  secara terpisah.
- Semua kedalaman terpilih ≤ 7, jadi menurut analisis jadwal tidak ada stall di batas layer; jumlah siklus yang
  diharapkan (NTT sekitar 113 + P) adalah ESTIMATE sampai diukur, dan jumlah stall terukur dilaporkan per P
  seperti disyaratkan ROADMAP.
- Empat revisi Quartus pada L = 8 (sekitar 16 menit masing-masing di mesin ini, dari kompilasi Fase 3), dinamai
  menurut ID konfigurasi yang akan ditambahkan ke matriks ablasi.
- Posisi register tepat untuk P = 2, 4, 6, test hazard di batas layer, dan pemeriksaan kesetaraan ditetapkan di
  test plan Fase 4 (CRG-4), ditulis setelah ADR ini diterima dan sebelum RTL apa pun.
- Opsi A.1, A.3, A.4 dan B.1, B.3 di atas tidak dikejar.

## Bukti
- `evidence/phase04/k1_l8_worst_path_breakdown.md`
- `evidence/phase04/layer_boundary_slack.txt` (`scripts/test/pipeline_hazard_slack.py`)
- `evidence/quartus/C2-K2-K1-L8.md`, `evidence/phase03/k1_experiment.md`
- `docs/ROADMAP.md` (Fase 4), `docs/decisions/adr/ADR-0006-phase-4-target-clock.md`
