# Test plan Fase 3 - eksplorasi multi-lajur L = 1/2/4/8 (C2), ditulis sebelum RTL apa pun dikodekan (CRG-4)

Lingkup: hanya RTL baru - `rtl/ntt/ntt_core_c2.sv` (berparameter `#(.NUM_LANES(L))`), yang menginstansiasi
`L` salinan `rtl/ntt/butterfly.sv` dan `rtl/ntt/twiddle_rom.sv`, menggerakkan
crossbar multi-bank `rtl/mem/poly_mem_banked.sv #(.NUM_BANKS(L))` (dibangun di Fase 2, alamatnya
terbukti tetapi belum pernah dijalankan datapath - lihat header `rtl/mem/poly_mem_banked.sv`). Tidak ada modul lain
yang berubah: `rtl/ntt/ntt_core.sv` (C0) dan `rtl/mem/ntt_core_c1.sv` (C1) tetap dibekukan.
Acuan: `tb/golden/primitives.py` (`ntt`, `intt`), `tb/mem/bank_model.py` (skema bank/offset,
`lane_p`, dan dua fungsi yang ditambahkan untuk fase ini: `zeta_index_of`, `reference_zeta_trace`).
Kriteria pemilihan jumlah lajur: `docs/decisions/adr/ADR-0004-phase-3-lane-count-l-selection-criterion.md`
(ADR 0004, Accepted) - utama: jumlah siklus minimum dalam anggaran 10,478 ALM (25%); sekunder:
pemeriksaan ulang AT informasi begitu clock yang valid timing ada. Tidak ada RTL di bawah yang ditulis sebelum
rencana ini.

## Catatan arsitektur: indeks zeta per lajur (diverifikasi sebelum RTL, tidak diasumsikan)

Indeks zeta `ntt_core.sv` (C0) adalah satu counter berurutan, bertambah sekali per blok selesai,
dipakai bersama di seluruh inti - itu tidak menggeneralisasi ke `L` lajur yang maju melalui blok berbeda
pada siklus yang sama. Fase 3 sebagai gantinya memberi setiap lajur indeks zeta bentuk tertutup,
`bank_model.zeta_index_of(layer, mode_inv, block)`:

- NTT (maju): `k = 2^layer + block`.
- INTT (mundur): `k = 127 - (blok selesai di layer sebelumnya) - block`.

Ini dicek silang terhadap `bank_model.reference_zeta_trace` - pernyataan ulang aturan pembaruan berurutan C0 sendiri
(Fase 1 CRG-7/CRG-8, sudah terbukti bit-exact/cycle-exact) - untuk semua 127
pasangan `(layer, block)`, kedua arah: 0 ketidakcocokan
(`evidence/phase03/lane_schedule_verification.txt`,
`scripts/build/gen_lane_schedule.py`). Skrip yang sama juga mengonfirmasi, untuk setiap `L ∈ {1,2,4,8}`, setiap
mode, setiap layer: `L` lajur aktif pada setiap sub-siklus `t` (`bank_model.lane_p`) mencakup semua 128
indeks butterfly `p` layer itu tepat sekali - tanpa duplikat, tanpa celah.

Implikasi RTL: setiap lajur menghitung `(j, jlen, zeta)` murni secara kombinasional dari
`(layer_q, lane_id, t_q)`, tanpa ketergantungan antar lajur dan tanpa counter zeta berjalan bersama -
inilah yang menjadikan `L` parameter waktu sintesis, bukan penulisan ulang kendali per `L`.

## Unit: datapath lajur ntt_core_c2, keempat instans L

- Kasus sudut (sama dengan 6 kasus test plan `ntt_core` Fase 1, dijalankan melalui setiap `L`): polinomial
  semua-nol; semua koefisien = q-1; impuls pada koefisien 0; impuls pada koefisien 255;
  bergantian 0/q-1.
- Bit-exact, dicek silang terhadap `tb/golden/primitives.py`:
  - `ntt(f)` dan `intt(f)` cocok untuk setiap kasus sudut + 100 polinomial acak, untuk setiap `L`.
  - `intt(ntt(f)) == f`, 50 polinomial acak, untuk setiap `L`.
- Jumlah siklus (CRG-7), diukur per L, tidak diasumsikan sama dengan C0/C1. Berbeda dengan Fase 2 (hanya banking L=1,
  harus identik siklus dengan C0), datapath `L>1` Fase 3 diharapkan memakai
  lebih sedikit siklus (`128/L` sub-siklus per layer sebagai ganti 128) - inilah besaran yang ingin diukur Fase 3.
  Syarat: jumlah siklus konstan di dalam satu `L` (tanpa stall yang bergantung data -
  argumen siklus-konstan yang sama seperti CRG-7, kini diperiksa per `L`), dan jumlah siklus
  NTT/INTT terukur untuk keempat `L` dicatat di tabel perbandingan `docs/results/phase03.md`.
- Siklus stall = 0 untuk setiap `L` (kriteria PASS Fase 3): tidak ada siklus yang terbuang menunggu konflik bank,
  karena jadwal di atas bebas konflik menurut bukti Fase 2
  (`evidence/phase02/bank_scheme_exploration.txt`) yang diterapkan per `L`.
- Dijalankan dua kali: Icarus dan Verilator (CRG-3), untuk setiap `L`.

## Formal (CRG-8, SymbiYosys), per L

- Jalankan ulang properti keselamatan FSM Fase 1/2 (handshake `busy_o`/`done_o`; `done_o` diaktifkan
  tepat satu siklus) terhadap `ntt_core_c2` pada setiap `L`.
- Rentang alamat: setiap alamat yang digerakkan ke `poly_mem_banked` (per lajur `j`, `jlen`, dan
  alamat pindai untuk lintasan skala INTT) tetap di `[0, 255]` untuk setiap state yang dapat dicapai, untuk
  setiap `L` - membuktikan ulang properti own-pair/rentang Fase 2 tetap berlaku begitu crossbar
  multi-bank benar-benar digerakkan oleh `L>1` lajur bersamaan (bukan hanya dialamatkan satu port sekali
  seperti di C1).

## Quartus: satu revisi per L (evidence CRG-9/CRG-10)

- `quartus/phase03_multilane_c2/` - empat revisi, `C2-L1`, `C2-L2`, `C2-L4`, `C2-L8`, batasan dan seed
  identik dengan C0/C1 (`evidence/quartus/C0.md`,
  `evidence/quartus/C1.md`).
- Dicatat per `L`: ALM, register, M10K, DSP, Fmax (corner terburuk), slack setup/hold terburuk,
  jumlah siklus NTT/INTT terukur, dan apakah `L` dalam anggaran (≤ 10,478 ALM, ADR 0004).
- Situasi M10K yang diwarisi dari Fase 2 (0/553, keterbatasan baca asinkron,
  `docs/results/phase02.md` §"Temuan Jujur") diperkirakan bertahan atau memburuk dengan bank `L>1`;
  laporkan apa adanya per `L`, jangan perlakukan sebagai regresi Fase 3 yang disembunyikan.

## Penerapan pemilihan L (ADR 0004)

`docs/results/phase03.md` harus menunjukkan, berurutan: (1) keempat nilai `L` dengan ALM
terukur lawan anggaran 10,478 - lulus/gagal; (2) jumlah siklus untuk kandidat dalam anggaran; (3) `L`
terpilih (jumlah siklus terendah di antara kandidat dalam anggaran); (4) begitu fase berikutnya menghasilkan
clock yang valid timing, pemeriksaan ulang AT informasi sekunder - ditandai jelas tidak
menimpa pemilihan utama tanpa ADR lanjutan.

## Secara eksplisit di luar lingkup Fase 3 (lihat docs/ROADMAP.md "Belum boleh")

`L > 8`; pipelining butterfly atau perubahan aritmetika (Barrett/Montgomery, reduksi malas -
Fase 5); memilih `L` dari selain tabel perbandingan terukur yang disyaratkan di atas;
membandingkan dengan perangkat lunak atau literatur seolah terukur pada platform yang sama; ADR clock target
(masih terbuka, `docs/decisions/PENDING.md`) - angka Fmax Fase 3 tetap hanya relatif sampai
itu selesai.
