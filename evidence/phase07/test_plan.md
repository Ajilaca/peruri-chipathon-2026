<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Fase 7: Keccak-f[1600] + baseline SHA3/SHAKE (K0) - test plan

Ditulis 2026-10-03, sebelum model golden Fase 7, sebelum RTL Fase 7 apa pun, dan sebelum pengukuran Fase 7 apa pun (CRG-4). Lingkup: `docs/ROADMAP.md` Fase 7; ADR 0019 (jalur minimal, satu kompilasi
untuk blok baru tanpa aturan adopsi); ADR 0025 (S10 adalah inti NTT/INTT; tidak disentuh di fase ini). Label: MEASURED, INFERENCE, ESTIMATE, NOT MEASURED, perhitungan tim.
Standar: FIPS 202 (Keccak-p, sponge, SHA3-256, SHA3-512, SHAKE128, SHAKE256) sebagaimana dipakai FIPS 203 (H, J, G, PRF, XOF). Matematika terkunci (C1): tidak ada di sini yang mengubah fungsi hash.

## 1. Apa yang dibangun
| Blok (file baru) | Fungsi |
|---|---|
| `tb/golden/keccak.py` | Keccak golden independen dari RTL: state sebagai 25 lane 64 bit (indeks x + 5y), kelima step map θ, ρ, π, χ, ι menurut FIPS 202, konstanta ronde dihitung oleh LFSR rc(t) (FIPS 202 Alg. 5) dan offset ρ oleh Alg. 2 (tidak diketik), `keccak_round`, `keccak_f1600`, jejak per ronde, `sponge(rate, ds, msg, outlen)` dengan pad10*1, dan keempat fungsi |
| `scripts/build/gen_keccak_consts.py` | Membangkitkan `rtl/keccak/keccak_consts_pkg.sv` (24 konstanta ronde, 25 offset ρ) dari model golden; `--check` membangkitkan ulang byte demi byte |
| `rtl/keccak/keccak_round.sv` | Satu ronde kombinasional θ → ρ → π → χ → ι pada 1600 bit, konstanta ronde sebagai masukan |
| `rtl/keccak/keccak_f1600.sv` | Register state (1600 FF), counter ronde 0..23, satu ronde per siklus, tepat 24 siklus per permutasi (tanpa keluar dini, tanpa kondisi bergantung data); port XOR-lane (absorb), port baca-lane (squeeze), clear |
| `rtl/keccak/keccak_sponge.sv` | Pengendali sponge dan top Quartus K0: mode, absorb dalam word 64-bit, padding di perangkat keras, squeeze dalam word 64-bit |

Antarmuka `keccak_sponge` (ditetapkan di sini agar test dan RTL ditulis terhadap satu kontrak):
- `start_i` dengan `mode_i[1:0]` (0 SHA3-256, 1 SHA3-512, 2 SHAKE128, 3 SHAKE256) dan `len_i[15:0]` (panjang pesan dalam byte, publik). Diterima di IDLE; menghapus state.
- Masukan: `in_valid_i`, `in_ready_o`, `in_data_i[63:0]`. Tepat ceil(len / 8) word diambil; byte k sebuah word (bit 8k+7..8k) adalah byte pesan 8w + k (urutan byte lane FIPS 202). Byte melewati `len` di word terakhir diabaikan.
- Keluaran: `out_valid_o`, `out_ready_i`, `out_data_o[63:0]` (urutan byte sama), `out_last_o` pada word digest terakhir SHA3-256 (4 word) dan SHA3-512 (8 word), lalu IDLE. SHAKE melakukan squeeze tanpa akhir
  (blok baru setiap rate word) sampai `stop_i`.
- `stop_i`: kembali ke IDLE dari state mana pun pada siklus berikutnya (mengakhiri aliran SHAKE). `busy_o`, dan counter permutasi `perm_cnt_o` (hanya test dan evidence).
- Rate (byte / word 64-bit): SHA3-256 136 / 17, SHA3-512 72 / 9, SHAKE128 168 / 21, SHAKE256 136 / 17. Byte domain: 0x06 (SHA3), 0x1F (SHAKE); bit akhir 0x80 pada byte rate − 1.
- Padding: setelah word pesan terakhir byte domain di-XOR pada byte `len mod rate` blok akhir dan 0x80 pada byte rate − 1 (satu byte 0x86 bila `len mod rate = rate − 1`). Bila `len` adalah kelipatan
  rate (termasuk 0) blok akhir hanya memuat padding. Permutasi absorb = floor(len / rate) + 1 untuk setiap panjang.

## 2. Model golden lebih dulu (V2)
`tb/golden/tests/test_keccak.py` (pytest) membandingkan `tb/golden/keccak.py` dengan `hashlib` Python (sha3_256, sha3_512, shake_128, shake_256):
setiap panjang 0 .. 3·rate + 1 per mode, panjang masukan ML-KEM-768 32, 33, 34, 64, 1120, 1184, 50 panjang acak sampai 2,000 byte; panjang keluaran SHAKE 0 .. 3·rate + 1, 128 (PRF, η = 2), 504 dan 840
(aliran SampleNTT); pesan semua-0x00 dan semua-0xFF. Jejak per ronde yang disusun atas 24 ronde harus sama dengan `keccak_f1600`. Baru setelah itu RTL ditulis.

## 3. Kasus sudut (didaftar sebelum test)
- Permutasi: state semua-nol; state semua-satu; setiap state satu-bit (1,600 state); 200 state acak; rantai (keluaran diumpan balik sebagai masukan, 10 kali). Setiap ronde dibandingkan, bukan hanya state akhir.
- Konstanta ronde: ke-24 ronde dicapai di setiap permutasi (ι adalah satu-satunya step yang bergantung ronde: kesalahan satu konstanta hanya tampak di jejak ronde itu).
- Panjang pesan per mode: 0, 1, 7, 8, 9 (batas word), rate − 1, rate, rate + 1, 2·rate − 1, 2·rate, 2·rate + 1, 3·rate; panjang ML-KEM 32, 33, 34, 64, 1120, 1184; panjang acak sampai 1,200.
- Word terakhir: 0 (tanpa word), 1..7 byte valid, 8 byte valid; sampah di byte yang diabaikan word terakhir (tidak boleh mengubah digest).
- Squeeze: digest SHA3 (4 dan 8 word); SHAKE128 tepat satu blok (21 word), 22 word, 63 dan 105 word (3 dan 5 blok); SHAKE256 16 word (keluaran PRF η = 2, 128 byte), 4 word (J).
- Pesan beruntun dengan mode berbeda tanpa reset; `stop_i` di tengah absorb, selama permutasi, dan selama squeeze SHAKE, lalu pesan baru (harus tepat: state dihapus saat start).
- Back-pressure: jeda acak di `in_valid_i` dan `out_ready_i` (digest bit-exact; jumlah siklus tidak dibandingkan di run ini).
- Reset di tengah pesan; `start_i` saat sibuk diabaikan.

## 4. Test
| ID | Pemeriksaan | Alat | Disyaratkan |
|---|---|---|---|
| V1 | Lint setiap modul baru (CRG-1, CRG-2) | Verilator `-Wall`, slang | 0 peringatan, 0 error |
| V2 | Keccak golden sama dengan `hashlib` (bagian 2) | pytest `tb/golden/tests/test_keccak.py` | semua sama |
| V3 | Paket konstanta dibangkitkan dari model golden, dibangkitkan ulang byte demi byte | `scripts/build/gen_keccak_consts.py --check` | 0 selisih |
| V4 | `keccak_f1600`: kasus sudut permutasi bagian 3, state setelah setiap ronde sama dengan jejak golden; done tepat 24 siklus setelah start untuk setiap state | cocotb `tb/keccak/test_keccak_f1600.py`, kedua simulator (CRG-3) | semua sama; latensi 24 di setiap run |
| V5 | `keccak_sponge`: keempat mode, setiap panjang dan kasus squeeze bagian 3, terhadap `hashlib` dan sponge golden; `perm_cnt_o` sama dengan jumlah permutasi golden | cocotb `tb/keccak/test_keccak_sponge.py`, kedua simulator | semua sama |
| V6 | Siklus konstan (CRG-7): untuk setiap mode, panjang, dan panjang keluaran, tiga pesan (acak, semua-0x00, semua-0xFF) tanpa back-pressure memberi jumlah siklus identik; siklus dicatat sebagai tabel dan sebagai rumus dalam `len` dan word keluaran | cocotb (test sama, log siklus `cycles_k0.json`) | identik per (mode, len, out); rumus cocok dengan setiap titik yang dicatat |
| V7 | Kontrol negatif (salinan khusus test): NC-RC satu bit satu konstanta ronde salah; NC-PAD byte domain SHA3 0x1F sebagai ganti 0x06; NC-R 23 ronde | cocotb | pemeriksaan bit-exact FAIL (NC-R juga gagal pada pemeriksaan latensi) |
| V8 | Formal (CRG-8) pada sponge dengan permutasi: K1 counter ronde dalam 0..23 dan permutasi berlangsung tepat 24 siklus; K2 tidak ada word masukan diterima dan tidak ada XOR state selama permutasi; K3 indeks lane absorb dan squeeze < word rate mode; K4 `out_valid_o` tetap tinggi dengan data stabil sampai `out_ready_i`; K5 state FSM legal, `stop_i` mencapai IDLE dalam satu siklus. Kontrol: NC-K1 (23 ronde) dan NC-K4 (valid turun tanpa ready) harus FAIL | SymbiYosys | PASS; kontrol FAIL |
| V9 | Parameter terkunci (CRG-6) dan regresi (CRG-5) | `check_params.py`; skrip Fase 0-6 hanya bila file RTL atau test yang ada dimodifikasi (Amandemen A1 Fase 5M); `git diff --name-status` sebagai evidence | PASS / tidak diperlukan |
| V10 | Quartus (CRG-9): revisi `K0` (top `keccak_sponge`, kernel-only, virtual pin), 40.000 ns, seed 1 (ADR 0019); revisi informasi `K0-20` pada 20.000 ns, seed 1. Satu revisi sekali | `quartus_sh`, `/quartus-report` | evidence diekstrak; timing terpenuhi atau kegagalan didokumentasikan |

## 5. Parameter yang dicatat
| Parameter | Sumber | Label |
|---|---|---|
| ALM, register, M10K, DSP (denominator fitter dikutip) | ringkasan fit `K0` | MEASURED |
| Fmax slow corner terendah, slack setup dan hold terburuk (semua corner), peringatan kritis ditriase | laporan timing `K0`, `K0-20` | MEASURED |
| Siklus per permutasi (harus 24) | V4 | MEASURED (simulasi) |
| Siklus per pesan per mode sebagai fungsi `len` dan word keluaran | V6 | MEASURED (simulasi) |
| Throughput (byte absorb per siklus per mode, pada panjang besar) dan waktu per permutasi pada Fmax | dihitung dari dua baris di atas | perhitungan tim |
| Permutasi per KeyGen / Encaps / Decaps ML-KEM-768 | instrumentasi model golden (43-44 / 44-45 / 44-45 pada tiga seed acak; hitungan SHAKE128 bergantung ρ, publik) | perhitungan tim |

## 6. Kriteria PASS (ROADMAP Fase 7) dan harapan
- PASS: V1-V9 seperti disyaratkan; semua mode bit-exact; latensi permutasi tetap 24 siklus ditunjukkan; evidence Quartus tercatat; baris K0 ROADMAP terisi. Tanpa aturan adopsi: K0 adalah blok baru (baseline), ia
  tidak menggantikan apa pun.
- ESTIMATE (ditulis sebelum mengukur; FSM diasumsikan: satu siklus clear, satu word per siklus, satu siklus padding, 24 siklus per permutasi, satu word per siklus keluar, tanpa tumpang tindih I/O dengan permutasi):
  siklus(len, out_words) ≈ 1 + ceil(len / 8) + 1 + 24·(floor(len / rate) + 1) + out_words + 24·(ceil(out_words / rate_words) − 1). Contoh SHA3-256 1,184 byte (H(ek)): 1 + 148 + 1 + 24·9 + 4 = 370 siklus.
  RTL dapat berbeda beberapa siklus transisi; rumus terukur menggantikan yang ini (dicatat, tidak disetel agar cocok). Per operasi ML-KEM-768 sekitar 44 permutasi × 24 ≈ 1,060 siklus permutasi
  ditambah I/O word (perhitungan tim), terhadap aritmetika KeyGen 5,475 siklus dengan S10 (MEASURED, simulasi).
- ESTIMATE sumber daya: register sekitar 1,700-2,000 (1,600 state + kendali); ALM sekitar 1,500-3,500 (metode: paritas kolom θ 320 bit, keluaran θ 1,600 bit, χ 1,600 bit sebagai fungsi 3-masukan, ditambah pemilih baca 64-bit 25-arah
  dan kendali sponge; pengepakan ALM oleh fitter tidak diketahui); DSP 0; M10K 0 diharapkan (tabel konstanta ronde dapat diinferensi sebagai blok ROM: dilaporkan, tidak diasumsikan).
- Fmax: INFERENCE, satu ronde adalah beberapa level LUT ditambah XOR masukan dan pemilih baca; diharapkan bukan batas sistem. Bukan aturan; 20 ns hanya informasi.

## 7. Tidak boleh di fase ini / tidak dicakup
- Tidak boleh (ROADMAP): dua ronde per siklus atau unrolling; sampler streaming; koneksi ke unit aritmetika Fase 6; tumpang tindih I/O dengan permutasi.
- Tidak dicakup: perangkat keras (tanpa papan); seed selain 1; sampler, kompresi, encoding, dan FO (fase berikutnya). Waktu-konstan di sini berarti jumlah siklus hanya bergantung pada panjang publik; ini bukan klaim side-channel.

## Amandemen A1 (2026-10-03, setelah RTL dan run verifikasi pertama; tidak ada ambang, aturan, atau hasil yang disyaratkan berubah)
Selisih antara rencana ini dan yang dibangun, dicatat apa adanya:
- Nama file: paket konstanta yang dibangkitkan adalah `rtl/keccak/keccak_pkg.sv` (fungsi `keccak_rc`, `keccak_rho`), bukan `keccak_consts_pkg.sv`; `scripts/build/gen_keccak_consts.py --check` adalah V3 seperti direncanakan.
- ESTIMATE siklus bagian 5 / 6: rencana mengasumsikan 24 siklus per permutasi. Pengendali butuh 1 siklus run dan 1 siklus done di sekitar 24 siklus sibuk, jadi satu permutasi adalah 26 siklus di sana; rumus
  terukur dan nilai H(ek) (389 bukan sekitar 370) ada di `keccak_cycles.md`. Angka yang direncanakan tetap di atas sebagaimana tertulis; ia digantikan, tidak diedit. V4 tetap mensyaratkan, dan mengukur, tepat 24 siklus sibuk.
- State juga dihapus pada `stop_i`, pada word digest SHA3 terakhir, dan pada reset (higiene: state memuat nilai antara yang bergantung rahasia); rencana hanya mensyaratkan penghapusan saat start.
- V8: NC-K4 berjalan sebagai BMC sampai kedalaman 40, bukan induksi, karena fase squeeze tercapai setelah sekitar 30 siklus (run induksi pada mutan tidak selesai dalam waktu wajar). Properti dan FAIL yang disyaratkan tidak berubah.
- Perbaikan test run pertama, semuanya di testbench (RTL benar): pemeriksaan akhir digest menurunkan `out_ready_i` sebelum tepi clock (word terakhir tidak pernah diterima); test stop meminta 1 word keluaran dari SHA3 (digest 4 atau 8 word);
  log siklus dihapus oleh build berikutnya (nama file kini per test). RTL punya satu perubahan setelah verifikasi pertama: ternary enum ditulis ulang sebagai if/else karena Icarus menolaknya. Seluruh verifikasi dan run formal
  di `verify.md` dan `formal.md` adalah milik RTL akhir.
- Asersi golden test yang salah (24 konstanta ronde berbeda) dikoreksi ke nilai sebenarnya (22 berbeda: ronde 5 dan 22, dan 6 dan 20, berbagi nilai); semua hash sama dengan hashlib.

