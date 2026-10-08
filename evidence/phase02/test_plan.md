# Test plan Fase 2 - banking memori (C1), ditulis sebelum test apa pun dikodekan (CRG-4)

Lingkup: `rtl/mem/bank_map_rom.sv`, `rtl/mem/poly_mem_banked.sv`, `rtl/mem/ntt_core_c1.sv`.
Acuan: `tb/mem/bank_model.py` (skema bank/offset), `tb/golden/primitives.py` (`ntt`, `intt`).
Tidak ada RTL di bawah yang ditulis sebelum rencana ini.

## Bukti bebas konflik pemetaan bank (bukan test cocotb; pemeriksaan menyeluruh/formal mandiri)

Disyaratkan oleh `docs/ROADMAP.md` Fase 2: "untuk setiap L ∈ {1, 2, 4, 8}, setiap layer dan setiap siklus,
tidak ada dua akses yang menuju port bank yang sama" ditambah "tidak ada alamat di luar rentang".

- Pemeriksaan pasangan sendiri: untuk setiap L, setiap dari 7 layer NTT dan 7 layer INTT, setiap indeks butterfly
  p (0..127): `bank(j) != bank(jlen)` (benar secara trivial untuk L=1, satu bank).
- Keseimbangan bank: setiap bank memuat tepat 256/L alamat, untuk setiap L.
- Bijektivitas offset: `(bank(addr), offset(addr))` adalah bijeksi dengan `addr` untuk setiap L
  (jadi tidak ada alamat yang hilang atau beralias).
- Kapasitas multi-lane: untuk setiap L, setiap layer, setiap "sub-siklus" t (0..128/L-1), 2·L
  alamat yang dihasilkan L lajur aktif pada siklus itu mengenai tidak lebih dari 2 kali satu bank (kapasitas
  true-dual-port M10K Cyclone V) -- diperiksa untuk pengelompokan lajur blok-kontigu
  (`tb/mem/bank_model.py:lane_p`) dan, sebagai kontrol negatif terdokumentasi, pengelompokan round-robin/interleaved
  (diharapkan dan terkonfirmasi gagal untuk L=4 dan L=8 -- dicatat, tidak disembunyikan).
- Pemeriksaan rentang: `bank < L` dan `offset < 256/L` untuk setiap alamat, setiap L (struktural, tetapi
  diperiksa, tidak hanya diasumsikan).
- Formal: properti pasangan sendiri diperiksa ulang pada isi ROM yang dibangkitkan sebenarnya
  (`rtl/mem/bank_map_rom.sv`, instans L=8 -- kasus yang harus membedakan layer paling banyak)
  lewat SymbiYosys, terlepas dari model acuan Python, untuk menangkap bug generator yang tidak bisa
  ditangkap Python-lawan-Python.

## Unit: bank_map_rom (keempat instans L)

- Kasus sudut: addr=0, addr=255, addr=128 (melintasi batas bank L=2), addr=127/129
  (bersebelahan dengan batas itu).
- Menyeluruh: semua 256 alamat, untuk setiap L ∈ {1, 2, 4, 8}, bit-exact terhadap
  `tb/mem/bank_model.py:bank_of` / tabel offset dari `build_maps`.

## Unit: poly_mem_banked (NUM_BANKS=1, satu-satunya konfigurasi yang dibangun di fase ini)

- Kasus sudut: tulis lalu baca-balik segera alamat 0 dan alamat 255; tulis semua 256
  alamat lalu baca kembali semua 256 dalam urutan berbeda.
- Properti: dengan NUM_BANKS=1, perilaku harus identik dengan `rtl/ntt/poly_mem.sv` (Fase 1) untuk
  urutan operasi yang sama -- diperiksa tidak langsung lewat regresi `ntt_core_c1` di bawah,
  yang merupakan pemeriksaan seluruh inti yang lebih kuat.

## Regresi: ntt_core_c1 (konfigurasi C1 = FSM/butterfly C0 + memori berbank pada NUM_BANKS=1)

Test yang sama dengan `tb/ntt/test_ntt_core.py` Fase 1, dijalankan terhadap top baru `ntt_core_c1`, untuk
membuktikan perubahan memori tidak mengubah perilaku atau jumlah siklus (kriteria PASS roadmap:
"siklus stall terukur = 0 pada L = 1"; "jumlah siklus konstan"; "bit-exact"):

- `ntt(f)` dan `intt(f)` bit-exact terhadap `tb/golden/primitives.py`, 5 polinomial sudut yang sama +
  100 acak masing-masing arah seperti Fase 1.
- `intt(ntt(f)) == f`, 50 polinomial acak.
- Pemeriksaan siklus konstan: jumlah siklus dari `busy_o` naik sampai `done_o` naik harus sama dengan nilai terukur
  Fase 1 persis (NTT 897, INTT 1153, menurut
  `evidence/phase01/cocotb_regression.txt`) untuk setiap kasus sudut
  dan 20 polinomial acak per arah -- penyimpangan apa pun berarti memori berbank memperkenalkan siklus
  stall, yang merupakan FAIL menurut kriteria roadmap sendiri, bukan sesuatu untuk dijelaskan.
- Dijalankan dua kali (Icarus dan Verilator), sama seperti Fase 1 (CRG-3).

## Secara eksplisit di luar lingkup Fase 2 (lihat docs/ROADMAP.md "Belum boleh")

Mengaktifkan lebih dari satu lajur di datapath sebenarnya (L tetap 1 di `ntt_core_c1`); perubahan pipeline;
perubahan aritmetika (kegagalan timing Fase 1 di `modmul_reduce.sv` tidak disentuh di sini,
sengaja -- itu lingkup Fase 4/5); Keccak.
