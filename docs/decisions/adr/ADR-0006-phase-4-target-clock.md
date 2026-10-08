# ADR 0006: Target clock Fase 4

- Status: Accepted
- Ekspektasi dikoreksi 2026-10-01 oleh ADR 0010: 50 MHz tetap menjadi target proyek secara terbaik-upaya tetapi tidak
  diharapkan dari aritmetika Fase 5 saja (jalur kritis C3-P6 ada di jalur pembacaan memori). Teks di bawah dibiarkan
  apa adanya sebagai catatan 2026-09-30.
- Tanggal: 2026-09-30
- Diputuskan oleh: Faza Dzil, Team J5

## Konteks
`docs/ROADMAP.md` ("Protokol pengukuran") mensyaratkan clock target dicatat sebagai ADR pada gerbang Fase 1. ADR itu
tidak pernah ditulis: Fase 1, 2, dan 3 semuanya dikompilasi dengan `create_clock -period 20.000` (50 MHz) sementara
dan disetujui sebagai baseline terdokumentasi dengan timing tidak terpenuhi (`docs/results/phase01.md`,
`phase02.md`, `phase03.md`).

Tujuan Fase 4 adalah menaikkan Fmax dengan mem-pipeline butterfly. Tanpa target tidak ada definisi "cukup",
dan pemeriksaan AT sekunder ADR 0004 tidak bisa dijalankan.

Titik awal MEASURED, konfigurasi C2-K2-K1 pada L = 8 (ADR 0005), clock sementara 20,000 ns
(`evidence/quartus/C2-K2-K1-L8.md`):
- Fmax 7,68 MHz (Slow 100C), slack setup terburuk −110,494 ns; hold terpenuhi.
- Jalur terburuk, per blok (`evidence/phase04/k1_l8_worst_path_breakdown.md`):
  delay data 129,6 ns, dengan jalur akses memori (arbitrasi slot bank, read mux) sekitar 57 ns, pembagi
  (`%` di `modmul_reduce`) sekitar 44 ns, pembangkit alamat sekitar 5 ns, pengali sekitar 4 ns, jalur tulis
  sekitar 9 ns.

ESTIMATE dari panjang segmen itu (mengabaikan overhead register dan routing ulang; membatasi ekspektasi, tidak
memprediksi Fmax): pembagian merata memerlukan sekitar 7 tahap pipeline untuk 20 ns dan sekitar 4 untuk 40 ns;
periode di bawah sekitar 57 ns memerlukan register di dalam jalur akses memori, dan di bawah sekitar 44 ns juga
satu di dalam rantai pembagi.

Sumber clock: yang benar-benar terdokumentasi.
- Board, 50 MHz - ada sumbernya. Reference design DE10-Nano dari Intel (GHRD), repository
  <https://github.com/intel/de10-nano-hardware>, commit `9b5fc81654c61922b625607d007933a69b5fdb52`
  (2022-08-04): `hdl_src/top.v` mendeklarasikan input FPGA `fpga_clk1_50`, `fpga_clk2_50`,
  `fpga_clk3_50`, dan `hdl_src/soc_system_timing.sdc` membatasi desain dengan
  `# 50MHz board input clock` / `create_clock -period 20 [get_ports fpga_clk1_50]`. Jadi input clock 50 MHz ke
  fabric FPGA ada di board. (Lokasi pin tidak dicatat di sini; bila perlu diambil dari dokumentasi Terasic atau
  GHRD itu, tidak pernah dari ingatan - lihat aturan Quartus.)
- Board, 25 MHz ke fabric FPGA - tidak ada sumbernya. Tidak ada dokumen yang diperiksa untuk ADR ini yang
  menunjukkan input clock 25 MHz ke fabric. *DE10-Nano User Manual* Terasic tidak dapat diambil saat catatan ini
  ditulis (mirror unduhan menolak akses otomatis atau sertifikatnya kedaluwarsa), jadi tidak ada yang diklaim
  darinya; manual itu harus dibaca dan dikutip sebelum rencana clock tingkat board ditulis.
- Device. Fitter melaporkan 6 PLL pada device ini (misalnya "Total PLLs 0 / 6" di
  `evidence/quartus/C2-K2-K1-L8.md`), jadi clock 25 MHz dapat diturunkan dari input 50 MHz. Itu akan menjadi
  pilihan desain dengan spesifikasi dan entri `.sdc` sendiri; rencana clock seperti itu belum ada.
- Proyek. Tidak ada spesifikasi proyek yang mendefinisikan clock untuk akselerator. Setiap kompilasi sejauh ini
  adalah kompilasi kernel-only dengan `clk_i` sebagai virtual pin dan periode `create_clock` yang dipilih tim;
  clock antarmuka HPS-ke-FPGA belum diputuskan (PENDING #3, #7). Tidak ada papan (PENDING #8), jadi setiap Fmax
  adalah angka Quartus, bukan pengukuran perangkat keras.

Akibatnya: 50 MHz adalah frekuensi input clock board yang nyata tetapi bukan persyaratan sistem yang dinyatakan
proyek ini; 25 MHz tidak punya persyaratan perangkat keras atau sistem sama sekali.

Catatan keterbandingan batasan: fitter digerakkan timing, jadi mengubah periode SDC mengubah penempatan dan
angka yang dilaporkan. Periode apa pun yang dipilih, referensi P = 0 (C2-K2-K1-L8) harus dikompilasi ulang pada
periode itu agar setiap baris Fase 4 memakai satu batasan; baris Fase 1-3 tetap seperti terukur pada 20,000 ns.

## Opsi yang dipertimbangkan
1. Mempertahankan 20,000 ns (50 MHz) sebagai target mutlak.
   Kriteria: timing terpenuhi (slack setup dan hold tidak negatif, semua corner) pada 20 ns.
   Untuk: tidak ada perubahan batasan, jadi baris Fase 4 langsung sebanding dengan Fase 1-3; target paling
   menuntut dan karena itu paling informatif.
   Melawan: memerlukan kenaikan Fmax sekitar 6,5x; menurut estimasi di atas itu berarti sekitar 7 tahap dengan
   register di dalam jalur akses memori dan pembagi. Mungkin tidak tercapai di Fase 4 saja (optimasi aritmetika,
   yang memperpendek pembagi, ada di Fase 5), dan dalam hal itu Fase 4 berakhir "timing tidak terpenuhi" lagi
   menurut definisi.
2. Menetapkan target mutlak lebih rendah, misalnya 40,000 ns (25 MHz).
   Kriteria: timing terpenuhi pada 40 ns.
   Untuk: menurut estimasi sekitar 4 tahap; target yang masuk akal dipenuhi Fase 4, memberi konfigurasi pertama
   yang valid secara timing dan membuka pemeriksaan AT ADR 0004.
   Melawan: memerlukan clock yang belum punya sumber di desain (clock turunan PLL harus didefinisikan di spesifikasi
   dan `.sdc`); referensi P = 0 harus dikompilasi ulang pada 40 ns; nilai 25 MHz adalah kemudahan, tidak diturunkan
   dari persyaratan sistem.
3. Tanpa target mutlak di Fase 4 (hanya kriteria relatif).
   Pertahankan 20,000 ns sebagai batasan, laporkan Fmax per P, dan nilai Fase 4 dengan kriteria ADR 0007
   (misalnya latensi dalam ns pada Fmax tiap P). Tetapkan target mutlak setelah Fase 5.
   Untuk: tidak ada angka tanpa dukungan yang dikomit; tidak ada kompilasi ulang referensi; jujur tentang apa yang
   diketahui hari ini.
   Melawan: ADR clock target yang hilang di ROADMAP tetap terbuka; CRG-9 tetap FAIL untuk Fase 4 menurut
   konstruksi; "jangan menyebut latensi tanpa clock-nya" berarti latensi harus dikutip pada Fmax terukur tiap
   konfigurasi, yang bukan clock yang dibatasi pada desain.
4. Dua tingkat: milestone Fase 4 ditambah tujuan akhir yang dinyatakan.
   Misalnya: tujuan akhir 20 ns (50 MHz) setelah Fase 5; milestone Fase 4 40 ns (25 MHz), atau "minimal Nx Fmax
   P = 0". Fase 4 lolos atau gagal terhadap milestone; tujuan akhir dicatat tetapi tidak menjadi gerbang di sini.
   Untuk: memisahkan apa yang seharusnya diberikan pipelining saja dari apa yang memerlukan kerja aritmetika.
   Melawan: dua angka yang harus dijaga konsisten; perlu keputusan periode mana yang membatasi kompilasi Fase 4
   (periode milestone membuat Fase 4 konsisten sendiri, periode tujuan akhir menjaga keterbandingan dengan Fase 1-3).

Opsi apa pun yang menyebut frekuensi selain 50 MHz sementara harus menyebut sumbernya (osilator board, setelan PLL,
atau clock jembatan HPS) di spesifikasi dan `.sdc` sebelum RTL bergantung padanya.

## Keputusan
Opsi 4, dua tingkat.
1. Milestone Fase 4: 40,000 ns (25 MHz). Ini target eksperimen yang dipilih agar Fase 4 punya tujuan yang dapat
   dicapai dan diperiksa. Ini bukan persyaratan perangkat keras dan bukan persyaratan sistem: tidak ada clock
   25 MHz ke fabric yang terdokumentasi untuk board dan tidak ada spesifikasi proyek yang memintanya
   (lihat "Sumber clock" di atas).
2. Tujuan akhir: 20,000 ns (50 MHz), setelah Fase 5. Dicatat sebagai arah perjalanan; sesuai dengan input clock FPGA
   50 MHz board yang terdokumentasi. Bukan gerbang Fase 4.
3. Satu batasan untuk seluruh Fase 4. Setiap revisi Quartus Fase 4 - termasuk referensi P = 0
   (C2-K2-K1 pada L = 8, dikompilasi ulang) - memakai SDC yang sama, `create_clock -period 40.000` pada
   `clk_i`, dengan device, seed, dan metode virtual pin yang sama seperti sebelumnya.
4. ADR 0004 tidak diubah.

## Konsekuensi
- "Timing terpenuhi" di Fase 4 (CRG-9) berarti slack setup dan hold terburuk tidak negatif di semua corner pada
  40,000 ns. Fmax tetap dilaporkan untuk setiap revisi; apakah suatu revisi juga akan memenuhi 20,000 ns dilaporkan
  hanya sebagai informasi.
- Referensi P = 0 harus dikompilasi ulang pada 40,000 ns. Baris Fase 4 lalu sebanding satu sama lain; tidak
  langsung sebanding dengan baris Fase 1-3, yang tetap seperti terukur pada 20,000 ns sementara dan tidak diukur
  ulang. Matriks ablasi harus menyatakan batasan tiap baris.
- Bila revisi Fase 4 memenuhi timing pada 40 ns, pemeriksaan AT sekunder (informasi) ADR 0004 dapat dijalankan
  untuk pertama kalinya; menurut ADR 0004 itu tetap tidak mengubah L terpilih tanpa ADR baru.
- Latensi dikutip bersama clock-nya (protokol pengukuran ROADMAP): pada 40,000 ns hanya untuk revisi yang
  memenuhinya; selain itu pada Fmax terukur revisi, dengan label demikian.
- Sebelum akselerator dihubungkan di papan, rencana clock tetap diperlukan (input board mana, setelan PLL bila 25 MHz
  atau clock turunan dipakai, hubungan dengan clock jembatan HPS, reset per domain) dengan sumber yang dikutip -
  ADR ini tidak menyediakannya.
- Mencapai 50 MHz diperkirakan memerlukan kerja aritmetika Fase 5 selain pipelining (ESTIMATE di Konteks); bila
  Fase 4 memenuhi 40 ns tetapi tidak 20 ns, itu hasil yang direncanakan, bukan kegagalan.

## Bukti
- GHRD DE10-Nano Intel: <https://github.com/intel/de10-nano-hardware> pada commit
  `9b5fc81654c61922b625607d007933a69b5fdb52`, file `hdl_src/top.v`, `hdl_src/soc_system_timing.sdc`
  (dibaca 2026-09-30)
- `evidence/quartus/C2-K2-K1-L8.md`
- `evidence/phase04/k1_l8_worst_path_breakdown.md`
- `evidence/phase01/quartus_C0_timing_analysis.md`
- `docs/ROADMAP.md` (Protokol pengukuran; Fase 4), `docs/decisions/adr/ADR-0004-phase-3-lane-count-l-selection-criterion.md`,
  `docs/decisions/adr/ADR-0005-apply-adr-0004-l-selection-to-the-c2-k2-k1-supplementary-con.md`
