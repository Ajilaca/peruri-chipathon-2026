# Test plan Fase 1 - baseline NTT/INTT (C0), ditulis sebelum test apa pun dikodekan (CRG-4)

Lingkup: `rtl/ntt/modmul_reduce.sv`, `rtl/ntt/base_case_multiply.sv`, `rtl/ntt/butterfly.sv`,
`rtl/ntt/twiddle_rom.sv`, `rtl/ntt/poly_mem.sv`, `rtl/ntt/ntt_core.sv`. Acuan: `tb/golden/primitives.py`
(`ntt`, `intt`, `base_case_multiply`). Tidak ada RTL di bawah yang ditulis sebelum rencana ini.

## Unit: modmul_reduce (a*b mod q)

- Menyeluruh berarti 3329² ≈ 11,08 juta pasangan - terlalu lambat untuk cocotb per-commit, jadi Fase 1 memakai cakupan
  acak; sapuan menyeluruh yang disyaratkan Fase 5 (`docs/ROADMAP.md` §5) ditunda ke sana.
- Kasus sudut: a=0, b=0; a=q-1, b=q-1 (hasil kali maksimum); a=1, b=apa saja (identitas); a=q-1, b=1.
- 2000 pasangan acak a,b ∈ [0,q).

## Unit: base_case_multiply (Algoritma 12)

- Kasus sudut: semua masukan nol; a0=a1=q-1, b0=b1=q-1; gamma=0; gamma=q-1; gamma = nilai
  ζ^(2·BitRev7(i)+1) sebenarnya dari model acuan (i=0 dan i=127, kedua ujung tabel).
- 500 tuple acak (a0,a1,b0,b1,gamma), gamma dibatasi pada nilai nyata dari tabel `_GAMMA` model acuan
  (tidak pernah nilai sembarang, karena perangkat keras nyata hanya memakai 128 konstanta itu).

## Unit: butterfly (CT maju / GS mundur)

- Kasus sudut: a=0,b=0; a=q-1,b=q-1; zeta=1 (entri i=0, tidak dipakai dalam praktik tetapi tidak boleh merusak
  matematika bila diberi); zeta = nilai tabel terbesar; a=0,b=q-1 dan a=q-1,b=0 (batas jalur
  pengurangan-lalu-tambah-q).
- 1000 tuple acak (a,b,zeta) per mode (maju, mundur), zeta dibatasi pada tabel `_ZETA_BITREV` model acuan.
  `_ZETA_BITREV` table.

## Unit: ntt_core (FSM tingkat atas, kedua arah)

- Kasus sudut (diberikan sebagai polinomial masukan 256 koefisien penuh):
  1. Polinomial semua-nol.
  2. Semua koefisien = q-1 (nilai maksimum).
  3. Impuls: f[0]=1, sisanya 0.
  4. Impuls pada koefisien terakhir: f[255]=1, sisanya 0.
  5. Bergantian 0 / q-1.
  6. Polinomial yang NTT-nya sendiri berpola semua-nol atau semua-(q-1) tidak diasumsikan; hanya pola masukan
     literal yang dipakai sebagai kasus sudut, sesuai aturan melarang mengarang vektor.
- Property test, dibandingkan dengan `tb/golden/primitives.py` bit-exact:
  - `ntt(f)` cocok dengan `primitives.ntt(f)` untuk setiap kasus sudut dan 100 polinomial acak.
  - `intt(f_hat)` cocok dengan `primitives.intt(f_hat)` untuk setiap kasus sudut dan 100 polinomial acak.
  - `intt(ntt(f)) == f` untuk 50 polinomial acak (round trip lewat RTL sendiri, bukan hanya
    tiap arah terpisah).
- Pemeriksaan siklus konstan (CRG-7): jalankan `ntt_core` pada setiap kasus sudut dan 20 polinomial acak pada
  arah yang sama; jumlah siklus clock dari `start_i` sampai `done_o` harus identik untuk
  semuanya (algoritma tidak punya cabang bergantung data, jadi ini harus berlaku menurut konstruksi; test
  menjadikannya fakta eksplisit yang dicatat, bukan asumsi).
- Dijalankan dua kali: sekali di Verilator, sekali di Icarus Verilog (CRG-3); selisih antara keduanya
  diselidiki sebelum mempercayai salah satunya.

## Formal (CRG-8, SymbiYosys)

- FSM mencapai `done_o` dari state reset sah mana pun dalam jumlah siklus terbatas (`cover`), dan
  tidak pernah menurunkan `busy_o` tanpa lebih dulu menaikkan `done_o` tepat satu siklus.
- Semua alamat yang diberikan ke `poly_mem` (`j`, `j+len` untuk lintasan butterfly; alamat pindai untuk
  lintasan skala INTT) tetap di `[0, 255]` untuk setiap state yang dapat dicapai (`assert`).

## Secara eksplisit di luar lingkup Fase 1 (lihat docs/ROADMAP.md "Belum boleh")

Banking memori atau banyak lajur, pipelining di luar satu butterfly per siklus, reduksi Montgomery/Barrett,
reduksi malas, Karatsuba, Keccak, integrasi HPS, klaim kinerja atau percepatan apa pun.
