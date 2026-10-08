# sw/hps/

Kode untuk HPS (ARM Cortex-A9, Linux) pada DE10-Nano. Folder ini masih kosong karena belum ada papan (PENDING #8) dan Fase 10 sampai 12 belum dimulai.
Di bawah ini dicatat apa yang nanti dikerjakan di sini dan apa yang sudah pasti dari sisi RTL.

## Tugas HPS menurut rancangan

| Tugas | Keterangan |
|---|---|
| Driver inti | Menulis masukan ke port host inti, memberi perintah KeyGen, Encaps, atau Decaps, menunggu `done_o`, dan membaca hasil |
| Pemeriksaan masukan FIPS 203 | Pemeriksaan kunci enkapsulasi dan masukan dekapsulasi dilakukan di HPS, bukan di RTL (ADR 0031). Acuannya `check_encapsulation_key` dan `check_decapsulation_input` di `tb/golden/mlkem.py` |
| Keacakan | Nilai `d`, `z`, dan `m` disediakan HPS dan ditulis sebagai data. Sumber keacakan belum diputuskan (PENDING #4) |
| Alur protokol | Emulasi pertukaran kunci gaya PACE antara "dokumen" dan "pembaca" (alur pesan belum diputuskan, PENDING #7) |
| Baseline perangkat lunak | Implementasi ML-KEM-768 di Cortex-A9 pada papan yang sama dengan akselerator, untuk perbandingan latensi di Fase 11 |
| Pengukuran | Waktu ujung-ke-ujung di HPS, overhead transfer, dan counter siklus fabric yang dibaca HPS |

## Antarmuka inti (dari RTL, `mlkem_core4`)

- Port host hanya bisa dipakai saat inti idle; penulisan saat sibuk diabaikan. Data berupa word 64 bit, byte ke-k dari word w adalah byte 8w + k. Data baca valid satu siklus setelah alamat.
- Alamat `h_addr_i[11:10]` memilih wilayah: 0 = KB, 1 = CB, 2 = CB2, 3 = RF. `h_addr_i[8:0]` memilih word.
- KB (300 word): `dk_pke` di word 0 (144 word), `ek` di word 144 (148 word; `rho` di word 288), H(ek) di word 292, `z` di word 296. CB (136 word): ciphertext. CB2 (136 word): ciphertext hasil enkripsi ulang.
- RF (32 word, 8 register masing-masing 4 word): 0 `d`, 1 `z`, 2 `m` (m' pada Decaps), 3 `rho`, 4 `sigma` / `r`, 5 `K` (K' pada Decaps; kunci bersama setelah Encaps dan Decaps), 6 `K_bar`, 7 H(ek).
- Operasi: `op_i` (0 KeyGen, 1 Encaps, 2 Decaps) dan `start_i` diterima hanya saat idle; `busy_o` aktif sampai `done_o` (satu pulsa).
- Satu domain clock `clk_i`; reset asinkron aktif rendah pada kendali.

Detail lengkap ada di header [rtl/mlkem_final/mlkem_core4.sv](../../rtl/mlkem_final/mlkem_core4.sv).

## Rencana uji di papan

Aturan dari [docs/ROADMAP.md](../../docs/ROADMAP.md), Fase 10 dan 11: vektor ACVP yang sama dengan simulasi dijalankan dari HPS, uji silang acak terhadap model acuan, soak test banyak iterasi, dan benchmark terhadap perangkat lunak dengan metode (jumlah run, median, sebaran) yang ditetapkan sebelum mengukur.
Tidak ada hasil papan dan tidak ada klaim kecepatan terhadap perangkat lunak sampai bukti itu ada.

## Status

Kosong. Fase 10 menunggu papan DE10-Nano.
