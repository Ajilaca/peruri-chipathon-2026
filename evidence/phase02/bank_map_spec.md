# Spesifikasi peta bank (Fase 2, konfigurasi C1)

Disyaratkan oleh artefak evidence Fase 2 di `docs/ROADMAP.md`: "spesifikasi peta bank, bukti, dan
log enumerasi". File ini adalah spesifikasinya; bukti/log adalah file lain di
direktori ini (`bank_scheme_exploration.txt`, `formal_bank_map.txt`,
`formal_ntt_core_c1_safety.txt`, `cocotb_regression.txt`).

## Masalah

`rtl/ntt/ntt_core.sv` (C0, Fase 1) menyimpan seluruh 256 koefisien polinomial dalam satu array 256x12
tanpa bank (`rtl/ntt/poly_mem.sv`). Memecahnya menjadi `L` bank independen (untuk datapath `L`-lajur
di masa depan, Fase 3) membutuhkan pemetaan alamat ke (bank, offset) sedemikian rupa sehingga, pada setiap
titik algoritma, alamat yang diakses pada waktu yang sama tidak pernah bertabrakan di bank fisik yang sama lebih sering
daripada jumlah port bank itu mengizinkan.

Ini lebih sulit daripada kelihatannya karena algoritma ini in-place: alamat `j` (0..255)
adalah lokasi penyimpanan fisik untuk seluruh run, di semua 7 layer -- ia tidak
ditafsirkan ulang per layer. Jadi fungsi penetapan bank harus satu fungsi tetap dari
alamat, dipilih sekali, yang kebetulan bekerja untuk pola akses setiap layer yang sangat berbeda.

Untuk layer tetap dengan panjang blok `len = 2^log2len`, pasangan butterfly NTT/INTT yang diproses
bersama selalu `(j, j + len)` -- dua alamat yang berbeda pada tepat satu bit, di posisi
`log2len`. Di 7 layer, `log2len` mengambil setiap nilai dalam `{1, ..., 7}` (tidak pernah 0, karena
panjang terkecil adalah 2). Fungsi bank berupa irisan bit tetap dan kecil (misalnya `addr mod L`, atau `log2(L)` bit atas
alamat) hanya mencakup segelintir posisi bit dari 7 itu, jadi ia bertabrakan sepenuhnya pada
setiap layer yang bit pembedanya jatuh di luar irisan -- dikonfirmasi secara empiris, bukan hanya
diargumenkan, dalam pemeriksaan "own-pair" di `bank_scheme_exploration.txt` untuk skema naif yang dicoba
pertama selama eksplorasi desain.

## Skema: penetapan bank XOR-group ("skewed storage")

Diimplementasikan di `tb/mem/bank_model.py:bank_of` (model golden) dan dibangkitkan menjadi
`rtl/mem/bank_map_rom.sv` oleh `scripts/build/gen_bank_map.py`.

Untuk `L` bank (`log2L = log2(L)` bit keluaran): bagi bit alamat `{1, ..., 7}` (bit 0 tidak pernah
dipakai) menjadi `log2L` grup round-robin; bit keluaran bank `i` adalah paritas XOR dari semua bit alamat
di grup `i`. Karena setiap bit 1-7 termasuk tepat satu grup, membalik satu bit mana pun
membalik tepat satu bit keluaran, sehingga `bank(addr) != bank(addr XOR 2^d)` untuk setiap `d` dalam
`1..7` -- ini properti "own-pair", dan ia berlaku apa pun layer yang menghasilkan selisih
`2^d`.

`offset(addr)` didefinisikan sebagai peringkat addr (berbasis 0, menaik) di antara semua 256 alamat yang berbagi
banknya -- ini membuat `(bank(addr), offset(addr))` bijeksi dengan `addr` menurut konstruksi, jadi tidak ada
alamat yang hilang atau beralias; `scripts/build/gen_bank_map.py` mengubahnya langsung menjadi isi ROM
(tidak pernah rumus turunan tangan terpisah).

## Pengelompokan lajur (untuk pemakaian Fase 3 nanti)

Untuk pemrosesan paralel `L` lajur, 128 butterfly satu layer dibagi menjadi `L` blok berurutan
masing-masing `128/L`: lajur `m` (0..L-1) menangani indeks butterfly `p = m*(128/L) + t` untuk
`t = 0..(128/L - 1)` (`tb/mem/bank_model.py:lane_p`). Ini dipilih lawan pengelompokan round-robin/interleaved
(`p = t*L + m`) karena inilah yang menjaga pertentangan bank dalam kapasitas true-dual-port M10K Cyclone V
(lihat di bawah); pengelompokan interleaved dicoba, ditemukan melebihi kapasitas itu
untuk L=4 dan L=8, dan didokumentasikan sebagai kontrol negatif yang ditolak di
`bank_scheme_exploration.txt`, tidak dibuang diam-diam.

## Apa yang diperiksa, dan bagaimana (semuanya di `bank_scheme_exploration.txt`)

| Properti | Metode | Hasil |
|---|---|---|
| Own-pair: `bank(j) != bank(jlen)`, setiap L, setiap layer, setiap p | Python menyeluruh (`tb/mem/bank_model.py` + `scripts/build/gen_bank_map.py`) | 0 tabrakan, semua L |
| Properti sama, pada isi ROM yang dibangkitkan sebenarnya | Formal (SymbiYosys, L=8, BMC kedalaman 1 atas `addr_i`/`d_i` bebas) | PASS (`formal_bank_map.txt`) |
| Keseimbangan bank: setiap bank memuat tepat `256/L` alamat | Python menyeluruh | seimbang, semua L |
| Bijeksi `(bank, offset)` <-> `addr`, nilai dalam rentang | Python menyeluruh | bijektif, semua L |
| Multi-lajur: <=2 akses/bank/siklus (M10K true-dual-port), pengelompokan blok-berurutan | Python menyeluruh, setiap L, setiap layer, setiap `t` | kasus terburuk tepat 2, semua L |
| Sama, pengelompokan interleaved (kontrol negatif) | Python menyeluruh | melebihi 2 untuk L=4 (terburuk 4), L=8 (terburuk 4) -- menegaskan pilihan pengelompokan itu penting, tidak diasumsikan tidak berbahaya |

## Yang TIDAK dibangun atau diklaim pada fase ini

- `rtl/mem/poly_mem_banked.sv` hanya dijalankan pada `NUM_BANKS=1` di fase ini
  (`rtl/mem/ntt_core_c1.sv`, konfigurasi C1); ia dikompilasi (lint bersih, CRG-1/CRG-2) untuk
  `NUM_BANKS` dalam `{2,4,8}` juga, tetapi crossbar baca/tulis multi-bank untuk nilai itu tidak punya
  test cocotb di fase ini -- hanya fungsi alamat `bank_map_rom` mandiri yang diuji dan
  dibuktikan untuk keempat nilai `L`. Membangun dan menguji datapath paralel `L>1` yang sebenarnya
  adalah lingkup Fase 3 (`docs/ROADMAP.md`).
- Tidak ada klaim bahwa perangkat keras `L=2/4/8` terukur atau bahkan terverifikasi penuh ujung ke ujung; hanya
  bahwa pengalamatannya terbukti bebas konflik secara terpisah.
