<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Fase 9M butir 1 (9M-1): jalur byte codec dua byte per siklus - test plan dan aturan adopsi

Ditulis 2026-10-04 sebelum RTL 9M-1 apa pun dan sebelum pengukuran 9M-1 apa pun. Lingkup: ADR 0034 (Accepted, Faza Dzil), butir 1. Baseline: inti C7-core Fase 9 sebagaimana digabung (main 49bebf7). Label: MEASURED, ESTIMATE, INFERENCE, perhitungan tim. Matematika terkunci (C1): byte dan koefisien persis seperti Fase 9; hanya berapa banyak yang berpindah per siklus yang berubah.

## 1. Mengapa (dari `../../profile.md`, MEASURED dalam simulasi)
Memuat atau menyimpan satu polinomial memakan 391-393 siklus pada d = 12 dan 326-329 pada d = 10 karena codec memindahkan satu byte per siklus (384 dan 320 byte), sedangkan port mesin memindahkan satu koefisien per siklus (256). Dengan dua byte per siklus, setiap d dibatasi oleh port mesin (256 koefisien per polinomial).

## 2. Desain (file baru; file Fase 9 menjaga perilakunya)
| File baru | Peran | Selisih dari modul Fase 9 |
|---|---|---|
| `rtl/mlkem/mlkem_unpack2.sv` | ByteDecode_d + Decompress_d | beat masukan 16 bit (byte 2i di bit 7:0, byte 2i+1 di bit 15:8), bit buffer 32-bit, sebuah beat diambil bila paling banyak 16 bit tersisa setelah koefisien siklus ini; 16 d beat per polinomial |
| `rtl/mlkem/mlkem_pack2.sv` | Compress_d + ByteEncode_d | beat keluaran 16 bit bila paling sedikit 16 bit terbuffer, buffer 32-bit; 16 d beat; `beat_last_o` pada beat 16 d - 1 |
| `rtl/mlkem/mlkem_wordbytes2.sv` | word 64-bit ke beat 16-bit | empat beat per word, read-ahead sama seperti Fase 9 |
| `rtl/mlkem/mlkem_bytedst2.sv` | beat 16-bit ke word 64-bit | empat beat per word |
| `rtl/mlkem/mlkem_ldpoly2.sv`, `mlkem_stpoly2.sv` | task load / store | task Fase 9 pada modul di atas; port sama |
| `rtl/mlkem/mlkem_codec2_top.sv` | top test | packer dan unpacker berdampingan (seperti `mlkem_codec_top.sv`) |
`rtl/mlkem/mlkem_core.sv` mendapat satu parameter `CODEC_W2` (bawaan 0). Pada 0 ia menginstansiasi persis `mlkem_ldpoly` / `mlkem_stpoly` Fase 9; pada 1 yang baru. Tidak ada baris lain inti yang berubah; mikro-program (ROM) tidak berubah. Compress / Decompress memakai konstanta sama seperti Fase 9 (dibuktikan pada semua 3,329 masukan di 9a). Tidak ada kendali yang bergantung pada nilai data.

## 3. Estimasi yang ditulis sebelum mengukur (ESTIMATE, dari profil dan desain)
| Besaran | Fase 9 (MEASURED) | 9M-1 ESTIMATE |
|---|---|---|
| LDP / STP d = 12 (siklus) | 391 / 393 | sekitar 263 / 265 |
| LDP / STP d = 10 | 326-327 / 329 | sekitar 263 / 265 |
| LDP / STP d = 1 atau 4 | 263 / 265 | tidak berubah |
| KeyGen, Encaps, Decaps dengan masukan profil | 9,095 / 10,735 / 16,667 | sekitar 8,330 / 10,160 / 15,520 (-8 %, -5 %, -7 %) |
| ALM (inti, median seed 1-6) | 17,620.5 | +100 sampai +500 |
| Register / blok RAM / DSP | 8,210-8,365 / 54 / 28 | sekitar +100 / 54 / 28 |
| Fmax slow corner terendah, median | 49.280 MHz | 47-51 MHz (codec tidak berada di jalur kritis: INFERENCE) |

## 4. Test (kedua simulator, Verilator dan Icarus; kontrol negatif pada salinan, RTL repository tidak pernah dimutasi)
| # | Test | Syarat lulus |
|---|---|---|
| V1 | lint Verilator `-Wall` dan slang inti dengan `CODEC_W2 = 1` dan top codec2 | 0 peringatan, 0 error |
| V2 | codec2: test pack dan unpack 9a pada `mlkem_codec2_top` dengan dua byte per beat (Compress / Decompress menyeluruh, semua nilai 12-bit, polinomial khusus dan acak untuk d = 1, 4, 10, 12, pola valid / ready selalu, acak, runs, start saat sibuk diabaikan, keluaran ditahan, siklus konstan) | bit-exact terhadap `primitives` golden yang tidak diubah, kedua simulator |
| V3 | inti dengan `CODEC_W2 = 1`: seluruh target `core` Fase 9c (ACVP keyGen 25, enkapsulasi 25, dekapsulasi 10; cross-check acak; rantai; protokol; siklus konstan) | 100 % sama, kedua simulator |
| V4 | profil dengan `CODEC_W2 = 1` (masukan sama seperti `../../profile.md`) | dicatat; KeyGen, Encaps, Decaps masing-masing lebih sedikit siklus dari Fase 9 |
| V5 | kontrol negatif: NC-W-ORD (dua byte beat pack ditukar) -> V2 pack harus FAIL; NC-W-CNT (unpack mengambil beat saat 20 bit tersisa) -> V2 unpack harus FAIL; NC-W-CORE (`mlkem_ldpoly2` menulis indeks koefisien + 1) -> V3 ACVP harus FAIL | masing-masing gagal seperti disyaratkan |
| V6 | formal: properti pack2 dan unpack2 seperti 9a (P1 hitungan dengan 16 d beat, P2 beat ditahan, P3 idle, P4 keseimbangan bit dengan 16 bit per beat, P5 hitungan pipeline; properti U serupa), dengan kontrol; formal inti 9c dengan `CODEC_W2 = 1` tidak diperlukan (task load / store adalah stub di sana dan menjaga protokolnya) | bukti PASS, kontrol FAIL, cover tercapai |
| V7 | regresi: skrip Fase 9 (9a, 9b, 9c) pada parameter bawaan; tidak ada file Fase 6-8 yang berbeda dari main | PASS |
| V8 | Quartus: revisi MW (inti, `CODEC_W2 = 1`), seed 1-6 pada 40.000 ns, satu per satu, kernel-only seperti MC | ekstrak evidence; timing terpenuhi atau kegagalan didokumentasikan |

## 5. Parameter yang dilaporkan (untuk Faza Dzil, dari laporan dan log)
ALM (median, min-maks, % dari denominator fitter), register, blok RAM, bit memori blok, DSP, slack setup dan hold terburuk, timing terpenuhi per seed, Fmax slow corner terendah (median, min-maks); siklus per operasi (masukan profil dan rentang ACVP), per operasi mikro; latensi t = siklus / median Fmax (perhitungan tim); jumlah ACVP per simulator; hasil siklus konstan; hasil formal; peringatan kritis.

## 6. Aturan adopsi (ditetapkan sebelum mengukur; tidak diubah sesudahnya)
9M-1 diadopsi (sebagai konfigurasi untuk butir 9M berikutnya) bila semua berikut berlaku:
1. V1-V3, V5-V7 lulus seperti dinyatakan (kebenaran lebih dulu; ketidakcocokan ACVP apa pun menolaknya).
2. Timing terpenuhi pada 40.000 ns di setiap seed 1-6 (V8).
3. Untuk masing-masing KeyGen, Encaps, dan Decaps (masukan profil), t = siklus / median Fmax MW lebih rendah dari t Fase 9 (siklus `../../profile.md` / 49.280 MHz).
4. Median ALM MW paling banyak 1,000 di atas 17,620.5 (jauh di dalam perangkat; biaya lebih besar berarti desain bukan yang dijelaskan bagian 2).
Bila tidak, ia tidak diadopsi dan inti tetap pada `CODEC_W2 = 0`. Hasilnya dicatat sebagai ADR Proposed; tim yang menerimanya.

## 7. Bukan bagian butir ini
Seed 20 ns (butir 2), hash K0 (butir 3), dan tumpang tindih dengan mesin (butir 4) adalah butir terpisah dengan rencana masing-masing. Tanpa hasil papan; tanpa klaim kecepatan terhadap perangkat lunak; waktu-konstan berarti invarian jumlah siklus saja.

## 8. Amandemen A1 (2026-10-04, ditulis setelah run; tidak ada di atas yang diedit dan aturan bagian 6 tidak berubah)
1. Sintaks Quartus (kesalahan saya, bukan perubahan desain): kompilasi MW pertama berhenti dalam hitungan detik dengan error Quartus 10170 (`if` generate di `mlkem_core.sv` ditulis tanpa `generate` / `endgenerate`; Verilator, slang, dan kedua simulator menerimanya, Quartus 25.1 tidak). Keluarannya tidak pernah dipakai. Kedua blok generate dibungkus `generate` ... `endgenerate` (tanpa perubahan logika), lint diulang (0 peringatan, 0 error, kedua nilai parameter), dan simulasi inti V3 dan V5 serta ketujuh revisi Quartus dijalankan ulang pada file akhir. Run Icarus pertama pada file sebelumnya dihentikan lewat process id-nya dan dimulai ulang.
2. Ditambahkan setelah rencana: `formal/phase09m-optimisation/9m1/mlkem_core_w2_safety.sby` membuktikan properti pengendali 9c (E1 dan S1-S7) dengan inti pada `CODEC_W2 = 1` (stub `stubs_9m1.sv`); bagian 4 V6 berkata ini tidak diperlukan. Bukti 9c pada parameter bawaan dijalankan ulang (V7) karena inti kini punya blok generate dan `mlkem_core_formal_top.sv` memilih instans task dengan makro.
3. Tidak dilakukan: V6 menyebut cover untuk pack2 dan unpack2; bukti 9a untuk modul satu-byte juga tidak punya, jadi tidak ditulis. Keterjangkauan ditunjukkan oleh simulasi (setiap run berakhir dengan done_o dan keluaran yang benar).
4. Estimasi lawan pengukuran: lihat `result_9m1.md` (estimasi siklus mendekati; estimasi ALM +100 sampai +500 terlalu tinggi, median terukur +33.5).
