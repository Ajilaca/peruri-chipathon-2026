<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Fase 8d: tumpang tindih sampler dengan aritmetika - test plan dan aturan adopsi

Ditulis 2026-10-03, sebelum perubahan RTL 8d apa pun dan sebelum pengukuran 8d apa pun (CRG-4). Lingkup: `docs/ROADMAP.md` Fase 8d; ADR 0026 (Accepted); chat 2026-10-03 (tanpa nama): kerjakan 8b, 8c, dan 8d tanpa berhenti, lalu laporan dan hasilnya.
Basis: sequencer 8c `rtl/sched/kpke_sched_smp.sv` (build STREAM, `evidence/phase08/8c/`), file Fase 6 dan sampler 8b, semuanya apa adanya. Label: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED, perhitungan tim. Matematika terkunci (C1): hanya urutan dan waktu polinomial noise disampel yang berubah.

## 1. Apa yang dibangun (satu perubahan: sampling polinomial noise berjalan saat transformasi menghitung)
Di 8c sampler menganggur saat inti NTT mentransformasi dan saat INTT berjalan (sekitar 635 siklus per transformasi dalam operasi Fase 6) dan sequencer menunggu setiap `SMPN`. Di 8d polinomial noise disampel tanpa memblokir: sampler mulai dan sequencer lanjut ke operasi berikutnya; beat sampler
ditulis ke store kapan pun port tulis store bebas; sequencer selalu punya prioritas pada port itu. Entri matriks tetap di-streaming (`PWMS`, yang butuh sampler dan karenanya menunggu sampai idle: sampler adalah satu unit bersama, jadi matriks dan noise disampel satu setelah yang lain, tidak pernah bersamaan).
- `rtl/sched/kpke_sched_smp.sv` (file 8c, diperluas; parameter `OVERLAP`, bawaan 0, jadi build 8c tidak berubah): dengan `OVERLAP = 1` operasi `SMPN` dengan `first = 1` tidak memblokir, `WAIT` menunggu sampai sampler idle, tulis store sebuah beat sampler diizinkan hanya bila sequencer tidak menulis
  (`wr_free = !seq_wr && !idle`), dan sebuah `END` menunggu sampler yang sibuk. Ini sudah ada di sumber 8c sebagai jalur tidak aktif (dipilih oleh parameter); evidence 8c diambil dengan `OVERLAP = 0`, dan jalurnya dijalankan dan diukur hanya di sini.
- Set program OVERLAP (`VAR` = 2), dibangkitkan dari `tb/golden/kpke_smp_model.py` (diperluas) oleh `scripts/build/gen_kpke_smp_roms.py`: program STREAM dengan sampling noise dipindahkan. KeyGen: s0 memblokir; lalu setiap polinomial noise berikutnya dimulai tanpa memblokir tepat sebelum transformasi yang sebelumnya, dan sebuah `WAIT` mengikuti setiap transformasi
  (s1 saat NTT s0, s2 saat NTT s1, e0 saat NTT s2, e1 saat NTT e0, e2 saat NTT e1; NTT e2 butuh e2). Encrypt: y0 memblokir; y1 dan y2 saat NTT y0 dan y1; e1_0 saat NTT y2; e1_1, e1_2, dan e2 masing-masing dimulai tepat sebelum INTT pass sebelumnya (polinomial pertama dibutuhkan di ADD setelah
  pass PWMS berikutnya, yang menunggu sampler juga); sebuah `WAIT` sebelum setiap operasi yang membaca polinomial yang disampel tanpa memblokir dan tidak dipisahkan dari awalnya oleh `PWMS`. Decrypt tidak punya sampling dan tidak berubah. Nomor slot seperti STREAM (12 slot).
- Set program STRESS (`VAR` = 3, hanya untuk test, tidak pernah dikompilasi di Quartus): Encrypt STREAM dengan e1_2 (slot 14) dimulai tanpa memblokir tepat sebelum `ADD` pertama (pass yang menulis store pada 128 dari 130 siklusnya), sehingga beat sampler dan tulis sequencer siap di siklus yang sama dan arbitrasi diuji; KeyGen seperti OVERLAP. Hasil sama menurut konstruksi.
Tidak berubah: sampler, inti NTT, store, unit PWM, file Fase 6.

## 2. Model golden lebih dulu
`tb/golden/tests/test_kpke_smp_model.py` diperluas: program OVERLAP dan STRESS yang dijalankan dengan primitives golden memberi slot logis yang sama dengan STREAM dan hasil akhir yang sama dengan K-PKE golden yang tidak diubah; hitungan operasi tidak berubah; setiap `WAIT` diperiksa secara statis terhadap aliran data: tidak ada operasi yang membaca slot yang ditulis `SMPN` tanpa memblokir
kecuali sebuah `WAIT` atau `PWMS` (yang menunggu sampler) berada di antaranya (pemeriksa di model, bahaya ada tepat bila ini gagal).

## 3. Kasus sudut
- Beat sampler saat sequencer menulis store: selama pass `ADD` (STRESS), selama unload transformasi, selama tulis slot akhir pass `PWMS`; beat ditahan (valid dan data stabil) dan ditulis sesudahnya; indeks pasangan penulis beat benar sesudahnya.
- Sampel tanpa memblokir yang masih berjalan saat sequencer mencapai operasi sampling berikutnya atau `PWMS` (menunggu), `WAIT` dengan sampler idle (tanpa delay selain fetch), `END` dengan sampler sibuk.
- Slot yang sama tidak pernah dibaca sebelum sampelnya lengkap (pemeriksa bahaya); polinomial noise yang dipakai transformasi berikutnya benar untuk setiap ctr.
- Siklus konstan: rho tetap, rahasia bervariasi memberi siklus identik (sampling noise punya panjang tetap; tumpang tindih tidak membuat selisih yang bergantung rahasia); masukan sama dua kali, hitungan sama.
- Reset di tengah program dengan sampel tanpa memblokir berjalan; start saat sibuk diabaikan.

## 4. Test
| ID | Pemeriksaan | Alat | Disyaratkan |
|---|---|---|---|
| V1 | Lint sequencer untuk `OVERLAP` = 1 dan ROM (CRG-1, CRG-2) | Verilator `-Wall`, slang | 0 peringatan, 0 error |
| V2 | Model golden, pemeriksa bahaya, ROM dibangkitkan ulang byte demi byte | pytest, `scripts/build/gen_kpke_smp_roms.py --check` | semua sama |
| V3 | Top dengan OVERLAP dan STRESS: setiap slot yang dibaca balik sama dengan model, hasil akhir sama dengan K-PKE golden, counter seperti sebelumnya (hitungan smp 6 / 7 / 0) | cocotb, kedua simulator | semua sama |
| V4 | Tumpang tindih terlihat: di OVERLAP siklus KeyGen dan Encrypt lebih rendah dari STREAM sekitar sampling yang tersembunyi; di STRESS paling sedikit satu beat sampler ditahan oleh tulis sequencer (probe `smp_cvalid && !smp_cready`) | cocotb | terlihat |
| V5 | Siklus konstan seperti bagian 3 (OVERLAP dan STRESS) | cocotb | identik per rho tetap |
| V6 | Kontrol negatif (salinan khusus test): NC-HAZ `WAIT` diabaikan (transformasi membaca slot terlalu awal); NC-ARB tanpa arbitrasi (`wr_free` selalu 1), dijalankan pada STRESS di mana beat dan tulis sequencer bertabrakan | cocotb | pemeriksaan bit-exact FAIL |
| V7 | Formal: properti 8c F1-F5 untuk `OVERLAP` = 1 (F4 kini bergantung pada arbitrasi: tidak ada tulis sequencer dan tulis beat di siklus yang sama) | SymbiYosys | PASS |
| V8 | Regresi: test 8c untuk STORE dan STREAM (file yang sama kini punya jalur OVERLAP) dan skrip 8b dan 8a | skrip | PASS |
| V9 | Quartus: `kpke_smp_top_s10` OVERLAP (NPOLY 12, `OVERLAP` = 1), 40.000 ns, seed 1-6, satu per satu; informasi: seed 1 pada 20.000 ns. Revisi STREAM 8c adalah baseline | `quartus_sh`, `/quartus-report` | evidence diekstrak |

## 5. Aturan adopsi (gaya ADR 0012, ditetapkan sebelum mengukur; tanpa toleransi)
OVERLAP diadopsi atas STREAM hanya bila semua berikut berlaku: 1. V1-V8 PASS di kedua simulator dan kontrol gagal seperti disyaratkan; 2. timing terpenuhi pada 40.000 ns di setiap seed untuk OVERLAP dan fit berhasil; 3. dengan F median atas seed 1-6 dari Fmax slow corner terendah pada 40 ns dan c rata-rata siklus atas himpunan rho yang sama:
t = c / F lebih rendah untuk OVERLAP daripada STREAM untuk KeyGen dan untuk Encrypt; 4. M10K(OVERLAP) <= M10K(STREAM). Jika aturan gagal, 8d dicatat sebagai terukur dan tidak diadopsi dan STREAM tetap.

## 6. ESTIMATE yang ditulis sebelum mengukur (bukan pengukuran)
- Siklus (perhitungan tim dari angka STREAM 8c pada simulasi yang sama, KeyGen sekitar 7,090 dan Encrypt sekitar 8,550, dan waktu sampling satu polinomial noise, sekitar 160 siklus dengan overhead sequencer): KeyGen menyembunyikan 5 dari 6 polinomial noise, sekitar 5 x 160 = sekitar 800 siklus: sekitar 6,300; Encrypt menyembunyikan 6 dari 7: sekitar 960 siklus: sekitar 7,600 (sekitar 11 % lebih sedikit dari STREAM).
  Polinomial pertama setiap program tidak dapat disembunyikan (tidak ada yang bisa ditumpang).
- Sumber daya: jalur OVERLAP adalah beberapa pembanding dan satu state lagi; ALM, register, dan M10K dalam beberapa puluh dari STREAM; Fmax: arbitrasi menaruh `seq_wr` (fungsi state sequencer) ke jalur ready beat, jalur pendek; harapkan Fmax dalam sebaran seed STREAM (INFERENCE, tidak diukur).

## 7. Tidak dicakup
Perangkat keras (tanpa papan); lebih dari satu sampler (matriks tidak dapat disampel saat noise disampel); tumpang tindih streaming matriks dengan transformasi (butuh sampler kedua atau buffer); hashing kunci dan seluruh KEM; seed selain 6.

## 8. Amandemen A1 (2026-10-03, ditulis setelah run pertama program OVERLAP dan STRESS; aturan adopsi bagian 5 tidak berubah)
1. Temuan run STRESS (RTL berubah): ketika sequencer memulai sampler pada siklus yang sama saat sampel tanpa-memblokir sebelumnya melaporkan pulsa `done_o`-nya, cabang `done` menghapus `smp_pwm_q` setelah cabang start mengaturnya, sehingga pass `PWMS` berikutnya tidak pernah menerima beat dan program tidak pernah selesai (`done_o` tidak pernah naik dalam 120,000 siklus).
   Program OVERLAP tidak pernah menghasilkan kebetulan itu (transformasinya memakan ratusan siklus); Encrypt STRESS menghasilkannya (`PWMS` tepat di belakang sampel tanpa-memblokir). Cabang `done` kini datang sebelum cabang start, sehingga start menang. Evidence 8c tidak terpengaruh secara fungsional (kasusnya butuh sampel tanpa-memblokir), tetapi file berubah, jadi revisi Quartus 8c dikompilasi ulang dari file akhir.
2. NC-HAZ diwujudkan secara berbeda: mengabaikan `WAIT` tidak merusak program OVERLAP (setiap sampel dimulai jauh sebelum dipakai: transformasi yang ditumpangi memakan 635 siklus dan sampel noise sekitar 160), jadi kontrol itu akan lulus. Kontrolnya adalah salinan ROM khusus test di mana transformasi pertama KeyGen OVERLAP membaca slot yang baru saja dimulai sampel tanpa-memblokir: pemeriksaan bit-exact harus gagal.
   Ini juga menunjukkan bahwa operasi `WAIT` adalah properti keselamatan jadwal, bukan kebutuhan terukur; pemeriksa bahaya statis (V2) yang menjaganya.
3. Kontrol formal: untuk OVERLAP = 1 kontrolnya NC-F2 seperti di 8c (F4 berlaku menurut konstruksi lewat `wr_free`; pelanggarannya hanya dapat dicapai oleh langkah induksi, yang dilaporkan SymbiYosys sebagai UNKNOWN).
4. Pemeriksaan ESTIMATE: run smoke memberi KeyGen OVERLAP 6,326-6,351 dan Encrypt 7,655-7,665 siklus (ESTIMATE sekitar 6,300 dan 7,600); di STRESS 545 siklus beat sampler ditahan oleh tulis sequencer (arbitrasi diuji).
