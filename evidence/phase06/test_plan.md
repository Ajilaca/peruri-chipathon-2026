<!-- claim-lint: skip-file (internal test plan, not proposal text) -->
# Fase 6: penjadwalan NTT di tingkat operasi - test plan

Ditulis 2026-10-03, sebelum RTL Fase 6 apa pun dan sebelum pengukuran Fase 6 apa pun (CRG-4). Lingkup: `docs/ROADMAP.md` Fase 6, ADR 0024 (Accepted: Fase 6 sekarang, S10 sesudahnya). Label: MEASURED,
INFERENCE, ESTIMATE, NOT MEASURED. Asumsi kerja dinyatakan di ADR 0024 (tim boleh menolaknya): inti NTT/INTT = S7 (`rtl/ntt/ntt_core_s7_p7.sv`, ADR 0021 masih Proposed); lingkup ROADMAP penuh.

## 1. Apa yang dibangun
Unit aritmetika K-PKE yang menjalankan aritmetika polinomial K-PKE.KeyGen (Alg. 13 baris 16-18), K-PKE.Encrypt (Alg. 14 baris 18-21 tanpa kompresi dan encoding) dan K-PKE.Decrypt
(Alg. 15 baris 6 tanpa kompresi) sebagai program tetap operasi polinomial. Masukan yang kelak datang dari Keccak dan sampler (matriks Â, s, e, y, e1, e2, pesan terdekompresi
μ, u', v') ditulis oleh testbench; tidak ada tentang Keccak, sampling, kompresi, atau encoding di perangkat keras (ROADMAP "belum boleh").

| Blok (file baru) | Fungsi |
|---|---|
| `rtl/sched/poly_store.sv` | NPOLY = 24 slot polinomial, masing-masing 128 word pasangan koefisien (separuh genap dan ganjil disimpan sebagai dua array 12-bit); dua port baca sinkron, satu port tulis dengan enable per separuh; satu port testbench (dipakai hanya saat idle) |
| `rtl/sched/gamma_rom.sv` (dibangkitkan) | γ_i = ζ^(2·BitRev7(i)+1) mod q, i = 0..127 (FIPS 203 Alg. 11), dibangkitkan oleh `scripts/gen_gamma_rom.py` dari `tb/golden/primitives.py` |
| `rtl/sched/pwm_unit.sv` | BaseCaseMultiply-accumulate, satu pasangan koefisien per siklus: c0 = acc0 + a0·b0 + a1·(b1·γ), c1 = acc1 + a0·b1 + a1·b0 (mod q); lima pengali Barrett (`modmul_barrett`, 3 potongan masing-masing), latensi tetap |
| `rtl/sched/kpke_sched.sv` | Sequencer: ROM program per operasi, mesin op XFER (store -> port host inti -> NTT/INTT -> kembali), PWM (pass pertama / tengah / terakhir dengan akumulator 128 x 24-bit), ADD, SUB; counter transformasi |
| `rtl/sched/kpke_sched_top.sv` | Top Quartus: sequencer + store + PWM + inti S7 |

Program (nomor slot; Â[i][j] di slot 3i + j untuk KeyGen dan Encrypt; slot sementara 15):
- KeyGen: NTT s (9-11), NTT e (12-14); untuk i: PWM Â[i][j] ∘ ŝ[j] atas j ke 15; ADD 12+i = 15 + 12+i (t̂ menggantikan ê). Hitungan 6 NTT / 0 INTT / 9 PWM.
- Encrypt: NTT y (9-11); untuk i: PWM Â[j][i] ∘ ŷ[j] ke 15; INTT 15; ADD 12+i = 15 + 12+i (u menggantikan e1); PWM t̂[j] (16-18) ∘ ŷ[j] ke 15; INTT 15; ADD 19 = 15 + 19; ADD 19 = 19 + 20 (μ). Hitungan 3 / 4 / 12.
- Decrypt: NTT u' (12-14); PWM ŝ[j] (9-11) ∘ û'[j] ke 15; INTT 15; SUB 19 = 19 − 15 (w menggantikan v'). Hitungan 3 / 1 / 3. Decaps = Decrypt + Encrypt: 6 / 5 / 15.

## 2. Model golden lebih dulu
`tb/golden/kpke_sched_model.py`: program yang sama pada slot Python dengan `ntt`, `intt`, `multiply_ntts` golden; diperiksa dari ujung ke ujung terhadap K-PKE golden yang tidak diubah (`tb/golden/kpke.py`):
t̂ KeyGen sama dengan `byte_decode(12, ek_PKE)`; u, v Encrypt terkompresi dan ter-encode sama dengan ciphertext `k_pke_encrypt`; w Decrypt terkompresi sama dengan pesan `k_pke_decrypt`, untuk seed acak.
`tb/golden/op_counts.py` mereproduksi hitungan ROADMAP (selesai: KeyGen 6/0/9, Encaps 3/4/12, Decaps 6/5/15).

## 3. Kasus sudut (didaftar sebelum test)
- ROM γ: semua 128 entri (dibangkitkan, dicek terhadap daftar golden); pasangan i = 0, 63, 64, 127.
- PWM: operand semua-nol dan semua-(q−1) (hasil kali terbesar, akumulasi tiga pass dengan setiap suku q−1); pass FIRST dengan akumulator basi tak-nol (harus diabaikan); ADD / SUB in-place (dst = a atau b).
- XFER: latensi baca inti (4 untuk S7) pada koefisien pertama dan terakhir; start tepat setelah tulis host terakhir (guard tulis inti).
- Siklus konstan: jumlah siklus program sama untuk setiap masukan (seed acak, semua-nol, semua-(q−1)); tanpa cabang, alamat, atau jumlah loop yang bergantung data di sequencer.
- Reset di tengah program; start saat sibuk diabaikan; tulis testbench saat sibuk diabaikan.

## 4. Test
| ID | Pemeriksaan | Alat | Disyaratkan |
|---|---|---|---|
| V1 | Lint setiap modul baru dan top | Verilator `-Wall`, slang | 0 peringatan, 0 error |
| V2 | Model jadwal golden sama dengan K-PKE golden (bagian 2) | pytest `tb/golden/tests/test_kpke_sched_model.py` | semua seed sama; hitungan op sama |
| V3 | ROM γ dibangkitkan dari model golden, dibangkitkan ulang byte demi byte | `scripts/gen_gamma_rom.py --check` | 0 selisih |
| V4 | `pwm_unit` lawan `base_case_multiply` + akumulasi: pasangan sudut dan 20,000 pasangan acak | cocotb, kedua simulator | semua sama |
| V5 | Top: KeyGen, Encrypt, Decrypt pada seed acak dan masukan sudut, keluaran dibaca balik dan dibandingkan dengan model golden; counter transformasi 6/0/9, 3/4/12, 3/1/3; siklus konstan per program | cocotb `tb/sched/test_kpke_sched.py`, kedua simulator | semua PASS |
| V6 | Kontrol negatif (salinan khusus test): NC-G satu entri γ salah; NC-R pembacaan balik selaras satu siklus lebih awal | cocotb | pemeriksaan bit-exact FAIL |
| V7 | Formal: properti kendali sequencer (handshake busy/done, tidak ada tulis store dari port testbench saat sibuk, program counter dan counter op dalam rentang) | SymbiYosys | PASS; satu kontrol negatif GAGAL |
| V8 | Regresi Fase 0-5M (tidak ada file yang ada dimodifikasi; evidence `git diff --name-status`) | skrip | menurut Amandemen A1 Fase 5M: hanya bila file yang ada dimodifikasi |
| V9 | Quartus: satu revisi `P6` (top dengan inti S7), 40.000 ns, seed 1 (ADR 0019: satu kompilasi untuk blok tanpa aturan adopsi) | `quartus_sh` | evidence diekstrak; dibandingkan dengan S7 |

## 5. Kriteria PASS (ROADMAP Fase 6) dan harapan
- Bit-exact (V2, V4, V5); hitungan cocok; siklus konstan dan dicatat per program; evidence Quartus tercatat. Tanpa aturan adopsi: Fase 6 menambah blok, bukan menggantikan.
- ESTIMATE (ditulis sebelum mengukur): per transformasi sekitar 256 (muat) + 120 (inti) + 260 (baca balik) siklus, per PWM atau ADD sekitar 128 + latensi; KeyGen sekitar 6 x 640 + 9 x 140 + 3 x 130, yaitu sekitar 5,700 siklus;
  perpindahan data lewat port host satu-koefisien milik inti mendominasi. DSP +10 (lima pengali Barrett), penyimpanan 24 x 256 x 12 = 73,728 bit (M10K bila alat menginferensinya; flip-flop bila tidak).
  Fmax: tidak diharapkan naik (INFERENCE); jalur baru dapat menurunkannya.

## 6. Tidak dicakup
Perangkat keras (tanpa papan); Keccak, sampler, kompresi, encoding, transformasi FO (fase berikutnya); sub-langkah 6b (radix-4) tidak dicoba kecuali tim memintanya; seed selain 1.
