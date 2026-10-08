<!-- claim-lint: skip-file (internal evidence, not proposal text) -->
# Jalur kritis inti 9M-1 (MW, MW-20), 2026-10-04

MEASURED dengan `quartus_sta -t scripts/quartus/phase5m_top_paths.tcl` (300 jalur setup terburuk, model slow, 1.100 mV, 100 C) pada salinan database terkompilasi `quartus/phase09m1_core` (revisi MW: 40 ns, seed 1; MW-20: 20 ns, seed 1). Klasifikasi menghitung hierarki sumber dan tujuan tiap jalur (keluaran skrip di bawah). INFERENCE pada pembacaan: yang tidak terdaftar punya slack lebih besar dari jalur terakhir yang terdaftar.

## MW-20
```
paths: 300, slack 4.355 .. 5.533 ns
  worst slack   4.355 ns,  195 paths: C5 Keccak (hash instance) -> C5 Keccak (hash instance)
  worst slack   4.361 ns,  105 paths: C5 Keccak (sampler sponge) -> C5 Keccak (sampler sponge)
```
## MW
```
paths: 300, slack 20.825 .. 22.954 ns
  worst slack  20.825 ns,   99 paths: C5 Keccak (sampler sponge) -> C5 Keccak (sampler sponge)
  worst slack  21.750 ns,  149 paths: C5 Keccak (hash instance) -> C5 Keccak (hash instance)
  worst slack  21.990 ns,    7 paths: sponge (hash instance, outside the permutation) -> byte buffer RAM
  worst slack  22.127 ns,   11 paths: NTT core / memory -> NTT core / memory
  worst slack  22.166 ns,   34 paths: sponge (hash instance, outside the permutation) -> register file rf_q
```

## Pembacaan
- Pada 20 ns (MW-20) semua 300 jalur terburuk ada di dalam dua permutasi Keccak-f[1600] jenis C5 (dua ronde per siklus): 195 di instans hash, 105 di sponge sampler mesin. Jalur terburuk punya kedatangan data 21,07 ns terhadap waktu diperlukan 25,43 ns (slack 4,355 ns).
- INFERENCE: setiap jalur MW-20 lain punya slack di atas 5,533 ns, yaitu di luar kedua permutasi desain mengizinkan sekitar 69 MHz pada kompilasi ini; batas berikutnya tidak diidentifikasi oleh laporan ini.
- Pada 40 ns (MW) kedua permutasi yang sama memimpin; kelas lain pertama adalah keluaran sponge hash ke register file dan RAM byte (slack sekitar 22,0-22,9 ns) dan inti NTT / memori (22,127 ns).
