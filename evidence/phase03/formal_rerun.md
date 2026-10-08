<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Run ulang formal dengan alur yang dikoreksi - Fase 1–3 (2026-09-30)

- Dibangkitkan oleh: `python3 formal/run/run_formal_slang.py` (SymbiYosys, smtbmc + boolector, frontend yosys-slang)
- RTL: tidak berubah. Hanya file di bawah `formal/` dan `.gitignore` yang diedit untuk run ulang ini.
- Menggantikan kesimpulan (bukan log mentah)
  `evidence/phase03/formal_verification.txt`, dan baris L>1 di
  `k2_formal.txt` / `k1_formal.txt`: hasil UNKNOWN itu adalah artefak
  harness formal, dijelaskan di bawah. `docs/results/phase03.md` (CRG-8) BELUM diperbarui; itu
  butuh persetujuan tim.

## 1. Mengapa NUM_LANES > 1 sebelumnya UNKNOWN
Statusnya UNKNOWN, bukan FAIL dan bukan timeout: base case (kedalaman 6) lulus dan langkah induksi
gagal pada `assert (!bank_overflow_o)` dalam hitungan detik.

Analisis jejak (C2, L=2, frontend yosys-slang, langkah induksi 5): `state_q`=S_RUN, NTT, `layer_q`=0,
`t_q`=0 - siklus pertama setiap NTT - dengan empat alamat port 0, 128, 64, 192 persis seperti
dijadwalkan. Instans `bank_map_rom` untuk port 0 menerima alamat 0 tetapi mengeluarkan bank 1; sumber
RTL berkata `8'd0: bank_o = 1'd0` dan `tb/mem/bank_model.py` setuju. State FSM yang sama lulus di base
case. Jadi dalam model formal keluaran ROM bukan fungsi murni dari alamatnya.

Akar masalah: pass `proc_rom` Yosys mengubah `case` 256-entri `bank_map_rom` (satu per port) dan
`twiddle_rom` menjadi sel memori `$mem_v2`. Isi memori adalah state bagi solver. Di base case
isinya dikunci pada nilai awal; di langkah induksi solver boleh mulai dari state apa pun, jadi
ia memilih isi ROM yang bukan tabel sebenarnya dan "menemukan" overflow. Contoh tandingan itu adalah
state yang tak dapat dicapai (ROM yang isinya berbeda dari konstantanya): artefak harness formal, bukan
masalah RTL, bukan masalah reset, bukan asersi yang terlalu kuat.

Perbaikan (hanya harness): `memory_map -rom-only` setelah `prep`, yang memetakan ROM kembali ke logika konstan. Ini
menyatakan fakta desain (isi ROM adalah konstanta), bukan asumsi tambahan. Alur
`read -formal` asli menunjukkan perilaku yang sama (L=2 lulus dengan baris yang sama), jadi
deskripsi sebelumnya - "artefak pembaca `-formal` pada ROM case 256-entri" - benar soal lokasi tetapi
salah soal mekanisme, dan invarian `t_q`/`layer_q` yang ditambahkan saat itu tidak mengatasinya.
L=1 lulus selama ini karena dengan hanya 2 port kapasitas 2-akses-per-bank tidak dapat terlampaui
apa pun isi ROM.

Terpisah, alur kini memakai frontend yosys-slang karena `read -formal` asli membiarkan hasil `add_mod`/`sub_mod`
`ntt_pkg` tidak digerakkan (`k1_experiment.md`, caveat 4). `initial assume (!rst_ni);` di top formal
ditulis ulang sebagai register flag siklus-pertama yang setara, yang diterima frontend itu.
frontend accepts.

## 2. Hasil
| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) | Sesuai harapan |
|---|---|---|---|---|---|---|
| A Fase 3 | C2 L=1 | PASS | PASS | basecase=pass, induction=pass | 0.9 | ya |
| A Fase 3 | C2 L=2 | PASS | PASS | basecase=pass, induction=pass | 1.3 | ya |
| A Fase 3 | C2 L=4 | PASS | PASS | basecase=pass, induction=pass | 2.5 | ya |
| A Fase 3 | C2 L=8 | PASS | PASS | basecase=pass, induction=pass | 5.8 | ya |
| A Fase 3 | C2-K2 L=1 | PASS | PASS | basecase=pass, induction=pass | 0.8 | ya |
| A Fase 3 | C2-K2 L=2 | PASS | PASS | basecase=pass, induction=pass | 1.1 | ya |
| A Fase 3 | C2-K2 L=4 | PASS | PASS | basecase=pass, induction=pass | 2.1 | ya |
| A Fase 3 | C2-K2 L=8 | PASS | PASS | basecase=pass, induction=pass | 5.5 | ya |
| A Fase 3 | C2-K2-K1 L=1 | PASS | PASS | basecase=pass, induction=pass | 0.8 | ya |
| A Fase 3 | C2-K2-K1 L=2 | PASS | PASS | basecase=pass, induction=pass | 1.4 | ya |
| A Fase 3 | C2-K2-K1 L=4 | PASS | PASS | basecase=pass, induction=pass | 2.6 | ya |
| A Fase 3 | C2-K2-K1 L=8 | PASS | PASS | basecase=pass, induction=pass | 5.2 | ya |
| B Kontrol negatif | NC-A: salinan bank_map_rom, NUM_BANKS=2: bank(128) 1 -> 0 (pelanggaran di siklus NTT pertama -> harus tertangkap base case) | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c2_formal_top.sv:57 | 1.1 | ya |
| B Kontrol negatif | NC-B: salinan bank_map_rom, NUM_BANKS=2: bank(40) 0 -> 1 (pelanggaran melewati kedalaman 6 -> base case lulus, induksi harus gagal) | UNKNOWN | UNKNOWN | basecase=pass, induction=FAIL; failed assert ntt_core_c2_formal_top.sv:57 | 1.5 | ya |
| B Kontrol negatif | NC-B/bmc60: salinan bank_map_rom, NUM_BANKS=2: bank(40) 0 -> 1 (kerusakan sama, BMC kedalaman 60 -> pelanggaran nyata dan dapat dicapai) | FAIL | FAIL | bmc=FAIL; failed assert ntt_core_c2_formal_top.sv:57 | 4.3 | ya |
| B Kontrol negatif | NC-C: salinan bank_map_rom, NUM_BANKS=8: bank(128) 2 -> 3 (konfigurasi terpilih C2-K2-K1 L=8, pelanggaran di siklus NTT pertama) | FAIL | FAIL | basecase=FAIL; failed assert ntt_core_c2_k2_k1_formal_top.sv:58 | 5.7 | ya |
| C Run ulang Fase 1/2 | Fase 1 ntt_core (C0) keselamatan FSM | PASS | PASS | basecase=pass, induction=pass | 0.5 | ya |
| C Run ulang Fase 1/2 | Fase 2 ntt_core_c1 (C1) keselamatan FSM | PASS | PASS | basecase=pass, induction=pass | 0.7 | ya |
| C Run ulang Fase 1/2 | Fase 2 bank_map_rom own-pair (NUM_BANKS=8) | PASS | PASS | bmc=pass | 0.4 | ya |

OVERALL: semua hasil sesuai harapan (19/19)

Kontrol negatif dibangkitkan saat run dari salinan `rtl/mem/bank_map_rom.sv` yang dirusak
(satu entri bank dibalik); RTL repository tidak diubah. NC-B menunjukkan mengapa UNKNOWN tidak boleh dibaca
sebagai PASS atau FAIL: di sana kegagalan induksi adalah pelanggaran nyata yang dapat dicapai (dikonfirmasi oleh BMC kedalaman
60), sedangkan sebelum perbaikan itu adalah state yang tak dapat dicapai.

## 3. Apa yang dibuktikan dan tidak dibuktikan bukti ini
Terbukti, untuk C2, C2-K2, dan C2-K2-K1 pada NUM_LANES = 1, 2, 4, 8 (k-induksi, kedalaman 6):
- `bank_overflow_o` tidak pernah aktif (tidak pernah lebih dari 2 akses ke satu bank dalam satu siklus);
- handshake FSM: satu siklus setelah `busy_o` turun, `done_o` bernilai 1;
- `t_q` dan `layer_q` tetap dalam rentangnya.
Bukti keselamatan FSM Fase 1 (C0) dan Fase 2 (C1) serta bukti own-pair peta bank Fase 2 tetap lulus
di bawah alur yang sama, jadi hasil PASS mereka sebelumnya tetap berlaku.

TIDAK dibuktikan oleh bukti ini: bit-exact NTT/INTT inti, integritas data memori, liveness
(bahwa `done_o` akhirnya tercapai), atau properti rentang alamat. Bit-exact bertumpu pada regresi
cocotb (dua simulator) dan, untuk butterfly K1, pada evidence ekuivalensi
(`k1_equiv_abstraction.txt`, `k1_exhaustive_equivalence.txt`).

## 4. Reproduksi
```bash
. scripts/env.sh
python3 formal/run/run_formal_slang.py          # all of the above; exit code 0 only if all as expected
(cd formal/phase03-multilane && sby -f ntt_core_c2_k2_k1_l8_safety.sby)   # a single proof
```
