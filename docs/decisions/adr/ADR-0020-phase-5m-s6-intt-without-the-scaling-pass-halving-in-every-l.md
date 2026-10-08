# ADR 0020: Fase 5M S6: INTT tanpa lintasan skala (pembagian dua di tiap layer), hasil terukur dan vonis adopsi

- Status: Accepted
- Tanggal: 2026-10-02
- Diputuskan oleh: Jevan, Team J5 (chat 2026-10-02: "gunakan M6 karena nantinya kita akan mengambil s7 dan s8 kemudian kita masuk ke fase selanjutnya")

## Konteks
- ADR 0017 (Accepted) langkah S6; test plan dan aturan adopsi ditulis sebelum RTL dan sebelum mengukur
  (`evidence/phase05m/test_plan.md`, commit f47efcc); basis C4b-B (ADR 0013 Accepted).
- ADR 0019 pada awalnya mengurangi Fase 5M menjadi S6 (diedit 2026-10-03 atas permintaan tim: S7, S8, dan S9 kemudian
  dikerjakan, lihat ADR 0019 catatan amandemen 3; teks aslinya berbunyi "S7-S9 tidak dikerjakan sebelum batas waktu
  2026-10-08").

## Opsi yang dipertimbangkan
(a) Mengadopsi M6 sebagai desain INTT (INTT 375 -> 119 siklus, 16 DSP, sekitar +250 ALM, Fmax NTT tidak berubah dalam
    derau seed): aturan yang ditetapkan lebih dulu menyatakan tidak diadopsi (bagian NTT ADR 0012 gagal 0,008 us);
    mengadopsi memerlukan keputusan tim yang mengubah aturan.
(b) Melaporkan M6 seperti terukur, tidak diadopsi aturan; C4b-B tetap konfigurasi NTT/INTT untuk lingkup batas waktu.
(c) Tim menetapkan aturan lain untuk kasus ini (misalnya "t_NTT tidak boleh lebih buruk dari sebaran seed"). Tidak
    dibuat oleh asisten.

## Keputusan
M6 diadopsi sebagai basis S7 dan S8 atas keputusan tim (Jevan, 2026-10-02), opsi (c) dari daftar di atas. Aturan test
plan yang ditetapkan lebih dulu tidak diubah dan hasilnya tetap tercatat seperti terukur: M6 tidak diadopsi oleh aturan
(hanya bagian NTT ADR 0012 yang gagal, t_NTT 3,456 us lawan 3,448 us, selisih median Fmax 0,25 % di dalam sebaran
seed). Alasan tim: S7 dan S8 mengikuti di basis ini, dan INTT turun dari 375 menjadi 119 siklus. Konsekuensi pilihan
tim, dinyatakan agar tidak terlupa:
- konfigurasi NTT/INTT mulai sekarang adalah M6 (revisi `M6`, `rtl/ntt/ntt_core_m6_p6.sv`), 16 DSP, sekitar 250 ALM
  lebih banyak dari C4b-B, INTT = NTT = 119 siklus;
- perbandingan ADR 0012 untuk S7 terhadap median Fmax M6 (34,430 MHz; t_NTT = t_INTT = 3,456 us), bukan terhadap C4b-B;
- ADR 0013 (Barrett) tidak berubah.

## Argumen kesetaraan (matematika tidak diubah, C1)
1. q = 3329 ganjil, jadi 2^-1 ada: 2 * 1665 = 3330 = 1 (mod q). Untuk x di [0, q): x/2 mod q = x/2 (x genap) atau
   (x + q)/2 (x ganjil), keduanya < q; `half_mod` menghitung persis ini dan diperiksa untuk semua 3.329 masukan (RTL,
   kedua simulator) dan terhadap fungsi acuan.
2. zeta * (b - a) / 2 = (zeta * 1665 mod q) * (b - a) (mod q): keluaran b butterfly yang dibagi dua adalah keluaran b
   standar dikali 2^-1; keluaran a adalah keluaran a standar dikali 2^-1 menurut (1).
3. Satu layer yang dibagi dua = layer standar dikali skalar 2^-1. Tujuh layer memberi 2^-7 kali INTT tanpa skala;
   128 * 3303 = 127 * 3329 + 1, jadi 2^-7 = 3303 (mod q), yang persis perkalian akhir FIPS 203 Algoritma 10 baris 14.
   Karena itu hasilnya sama dengan Algoritma 10 untuk semua masukan di [0, q)^256.
4. Diperiksa, tidak diasumsikan: `intt_halving()` acuan sama dengan `intt()` pada 256 vektor satuan, 256 vektor
   satuan (q-1), vektor tepi, dan 1.000 vektor acak; INTT RTL sama dengan kedua model acuan pada 512 vektor satuan dan
   100 polinomial acak + sudut; tiga kontrol negatif (layer model acuan dibuang, bypass `half_mod` RTL, entri ROM RTL
   satu layer tidak dibagi dua) gagal sesuai syarat.

## Konsekuensi
- Terukur (MEASURED, Quartus, seed 1-6, 40,000 ns; `evidence/phase05m/s6/selection_worksheet.md`): ALM 9.394-9.441
  (C4b-B 9.166-9.208), register sekitar 4.030-4.080, M10K 29, DSP 16 (C4b-B 18), median Fmax 34,430 MHz (C4b-B
  34,515), timing terpenuhi di setiap seed, siklus NTT / INTT 119 / 119 (C4b-B 119 / 375, simulasi). t_NTT 3,456 us
  (C4b-B 3,448), t_INTT 3,456 us (C4b-B 10,865) pada median Fmax (perhitungan tim).
- Rentang Fmax saling tumpang tindih (M6 32,35-35,04 lawan C4b-B 33,46-34,84 MHz), jadi selisih median 0,25 % tidak
  dapat dibedakan dari derau seed (INFERENCE).
- ALM naik sekitar 250 (INFERENCE: tabel twiddle INTT menggandakan ROM per lajur dan delapan unit `half_mod`
  ditambahkan, diimbangi reducer skala yang dihapus; tidak diurai per entitas).
- Regresi Fase 0-5 penuh (V9) tidak dijalankan untuk S6 (Amandemen A1; tidak ada file yang ada yang diubah). Branch 5M
  membawa kodenya; bila tim kelak menginginkan keuntungan siklus INTT (INTT mandiri 119 sebagai ganti 375 siklus),
  catatan ini tempat memulai.
- Tidak tercakup: perangkat keras, seed atau batasan lain, analisis jalur untuk Fmax NTT.

## Bukti
- `evidence/phase05m/test_plan.md` (aturan, Amandemen A1), `s6/verify.md`, `s6/formal.md`,
  `s6/verification_status.json`, `s6/selection_worksheet.md`, `s6/quartus_M6[-s2..s6].md`
