<!-- claim-lint: skip-file (internal study, not proposal text) -->
# Fase 5M S9: studi M10K / baca sinkron (hanya dokumentasi; tanpa RTL, tanpa run Quartus)

Rencana: `evidence/phase05m/test_plan_s9.md` (dengan Amandemen A1). Keluaran analisis: `port_analysis.txt` (`scripts/test/phase5m_s9_port_analysis.py`). Tanpa aturan adopsi: tim memilih (C5).
Label: MEASURED (laporan Quartus atau simulasi di repository ini), INFERENCE (aritmetika atau penalaran pada nilai terukur), ESTIMATE (metode ditulis di sebelahnya), NOT VERIFIED / NOT MEASURED.

## 1. Posisi memori saat ini
- Penyimpanan adalah flip-flop, bukan M10K: 256 x 12 bit = 3,072 bit dalam 8 bank berisi 32 word, baca asinkron (kombinasional). MEASURED: kompilasi Fase 2 menginferensi 0 M10K untuk memori berbank
  (`evidence/phase02/quartus_C1_vs_C0.md`, Bagian 4; "M10K NOT achieved, async-read limitation"). Jumlah M10K revisi berikutnya (S7: 31, S8: 33, M6 29) diinferensi alat
  dan tidak dikaitkan ke blok dalam studi ini (INFERENCE: bukan penyimpanan polinomial).
- Biaya (MEASURED, Fase 4, `evidence/phase05/baseline/decision_package.md`): entitas memori 6,964.6 ALM pada P = 2 dan 7,621.2 ALM pada P = 4 (+39.5 dari P = 4 ke P = 6), yaitu sekitar
  7,660 ALM pada P = 6 (INFERENCE, jumlah) dari 10,505 ALM untuk seluruh inti C3-P6. Inti S7 saat ini berjumlah 9,361-9,405 ALM (`s7/selection_worksheet.md`).
- Timing (MEASURED): segmen baca (dekode alamat, arbitrasi slot 16-port, mux baca) 21.292 ns dari jalur 29.345 ns di C3-P6 (`baseline/c3p6_critical_path.md`); memecahnya dengan satu register (S7)
  menaikkan median Fmax dari 34.430 ke 38.720 MHz; register jalur tulis (S8) tidak membantu (37.99 MHz).

## 2. Tuntutan port jadwal (MEASURED oleh model jadwal alamat nyata, `port_analysis.txt`; perhitungan tim, tanpa perangkat keras)
| Kasus | baca / bank / siklus | tulis / bank / siklus | baca + tulis |
|---|---:|---:|---:|
| Peta 8 bank saat ini, NTT dan INTT, tulis P = 7 siklus setelah baca | 2 | 2 | 4 |
| Kandidat 2: 16 bank, `bank = (a1^a2^a3^a4, a7, a6, a5)`, `offset = a[3:0]` | 1 | 1 | 2 |
| Kandidat 1 (turunan tangan pertama) | 2 | 2 | 4 (dibantah) |
| Kontrol negatif `bank = a[7:4]` | 2 | 2 | 4 |
| Kontrol negatif `bank = a[3:0]` | 16 | 16 | 16 |

Pembacaan (INFERENCE): M10K true-dual-port melakukan dua operasi port per siklus (rencana Fase 2 repository menghitung "<= 2 akses per bank per siklus" terhadap kapasitas itu; handbook Intel tidak dibaca ulang dalam
studi ini: NOT VERIFIED di sini). Peta saat ini butuh empat per bank di beberapa siklus (dua baca dan dua tulis), jadi tidak muat satu M10K per bank. Kandidat 2 butuh tepat satu baca dan satu tulis per bank per siklus
sepanjang timeline kedua arah (termasuk setiap batas layer); ia bijektif (256 (bank, offset) berbeda) dan seimbang (16 word per bank). Itu pola simple dual port (1 baca + 1 tulis)
sebuah M10K.

## 3. Opsi (daftar ADR 0017), dengan kebutuhan dan biaya masing-masing
| Opsi | Apa itu | Evidence dalam studi ini | Biaya (ESTIMATE, metode) | Yang harus dibuktikan sebelum RTL |
|---|---|---|---|---|
| A. 16 bank 1R1W (kandidat 2) | 16 bank 16 x 12 bit, satu blok M10K per bank, baca sinkron; crossbar baca (bank -> port butterfly) dan crossbar tulis (port -> bank) digerakkan ROM dari model alamat golden; tanpa arbitrasi slot (riak arbitrasi dan potongan register-nya hilang) | bebas konflik sepanjang timeline (bagian 2); kontrol konflik seperti disyaratkan | M10K: 16 blok (16 x 192 bit, sekitar 2 % dari 10 Kbit tiap blok) = 2.9 % dari 553 milik fitter (perhitungan tim); sekitar 3,000 flip-flop penyimpanan hilang (INFERENCE dari 3,072 bit); crossbar: <= 5 ALM per bit keluaran untuk mux 16:1 (mux 16:1 = empat 4:1 + satu 4:1; 6 masukan per 4:1; mengasumsikan satu ALM per fungsi 6-masukan) x 16 keluaran x 12 bit = <= 960 ALM per crossbar, <= 1,920 ALM untuk keduanya (batas atas, tidak diukur) | latensi baca sinkron dan register keluaran (NOT MEASURED); perilaku read-during-write mode M10K untuk alamat sama dalam satu siklus (jadwal tidak pernah melakukannya: properti formal C dari S7/S8; mode blok tetap harus dipilih dengan sengaja, NOT VERIFIED); ROM crossbar dibangkitkan dari `addr_pair` dan diperiksa entri demi entri; properti bank formal baru (<= 1 baca dan <= 1 tulis per bank); inti lawan golden, scoreboard, kontrol negatif (peta dengan konflik harus gagal); akses host saat IDLE/DONE pada port yang sama; Quartus harus melaporkan 16 blok RAM untuk penyimpanan (pelajaran Fase 2) |
| B. Dua koefisien per word (word 24-bit, kedalaman 128) | satu word memuat a, a ^ (1 << m) | butterfly butuh j dan j + len, yang berbeda tepat di bit log2len; untuk m mana pun hanya layer dengan log2len = m (satu layer per arah) menemukan kedua operand dalam satu word | tanpa estimasi ALM: tidak berguna | tidak dikejar: enam dari tujuh layer tetap butuh dua word per butterfly |
| C. Double-pumping (memori pada 2x clock inti) | dua akses memori per siklus inti | tidak dievaluasi: butuh frekuensi maksimum M10K (NOT VERIFIED) dan domain clock kedua dengan crossing terdokumentasi (aturan 7 CLAUDE.md); dengan kandidat 2 kebutuhannya hilang | tidak diestimasi | hanya bila A ditolak |
| D. Perubahan jadwal (lebih sedikit lajur) | tuntutan port lebih rendah, L = 4 bukan 8 | siklus per layer = 128 / L berlipat dua (INFERENCE); bertentangan dengan tujuan siklus | tidak diestimasi | tidak dikejar |
| E. Pertahankan penyimpanan flip-flop (S7 saat ini) | tanpa perubahan | MEASURED, `s7/selection_worksheet.md` | 0 | tidak ada (keadaan terverifikasi saat ini) |

## 4. Apa yang ditunjukkan dan tidak ditunjukkan studi ini
- Menunjukkan (model jadwal alamat nyata): peta 16-bank bebas-konflik 1R1W ada untuk L = 8, timeline P = 7, kedua arah. Turunan tangan peta pernah salah sekali dan tertangkap oleh skrip (Amandemen A1).
- Tidak menunjukkan: angka Fmax, ALM, atau M10K apa pun untuk memori berbasis M10K (tidak ada yang dikompilasi); bahwa crossbar lebih cepat dari mux baca saat ini; bahwa perilaku read-during-write aman pada mode M10K yang dipilih;
  apa pun tentang pola stall S8 (struktur satu-siklus-isu-ke-tulis yang sama berlaku, tetapi tidak dijalankan ulang untuk P = 8); lalu lintas memori perkalian pointwise (base-case multiply), yang tidak termasuk dalam inti NTT.
- Fakta perangkat Intel (kapasitas M10K sekitar 10 Kbit per blok diturunkan dari tabel produk di `docs/proposal/references.md` [22]: 5,570 Kb atas 557 blok; mode port, mode read-during-write, dan frekuensi maksimum berasal dari
  pengetahuan umum dan NOT VERIFIED di sini: periksa Cyclone V Device Handbook, bab Embedded Memory, sebelum RTL apa pun).

## 5. Keputusan untuk tim (ADR 0022, Proposed)
1. Tidak melakukan apa pun lagi dengan memori sebelum tenggat (S7 adalah yang terbaik terukur; Fase 6 / 7 berlanjut). 2. Buka satu eksperimen "S10: 16 bank M10K 1R1W (opsi A)" sebagai langkah tersendiri dengan test plan dan aturan ADR 0012,
setelah blok kritis-tenggat (Keccak, sampler); ESTIMATE upaya 4-6 jam termasuk formal dan sapuan Quartus enam seed (asumsi: sebanding dengan S7 plus S8 sesi ini). 3. Lainnya.
