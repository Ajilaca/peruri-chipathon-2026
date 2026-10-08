<!-- claim-lint: skip-file (internal evidence, not proposal text) -->
# Jalur kritis inti 9M-1 pada 14 ns (F14-s1, H14-s2), 2026-10-04

MEASURED dengan `quartus_sta -t scripts/quartus/phase5m_top_paths.tcl` (300 jalur setup terburuk, model slow, 1.100 mV, 100 C) pada salinan database terkompilasi `quartus/phase09f0_core` (revisi F14-s1: bawaan, dan H14-s2: upaya kinerja tinggi, keduanya 14,000 ns); diklasifikasikan oleh `scripts/quartus/classify_paths_9f.py` dari nama hierarki node From dan To (skrip yang sama mereproduksi kelas `../../critical_paths_MW.md`). File laporan mentah disimpan di salinan scratch dan tidak disimpan (masing-masing 300 baris).

```
## F14-s1_paths_slow100_summary.rpt
paths: 300, slack 0.721 .. 1.689 ns
  worst slack   0.721 ns,  133 paths: Keccak permutation (hash instance) -> Keccak permutation (hash instance)
  worst slack   1.055 ns,   84 paths: NTT core / memory / PWM -> NTT core / memory / PWM
  worst slack   1.266 ns,   83 paths: Keccak permutation (sampler sponge) -> Keccak permutation (sampler sponge)
## H14-s2_paths_slow100_summary.rpt
paths: 300, slack 0.423 .. 1.184 ns
  worst slack   0.423 ns,  126 paths: Keccak permutation (hash instance) -> Keccak permutation (hash instance)
  worst slack   0.453 ns,  146 paths: Keccak permutation (sampler sponge) -> Keccak permutation (sampler sponge)
  worst slack   0.906 ns,   19 paths: hash wrapper / sponge control -> register file
  worst slack   1.024 ns,    3 paths: hash wrapper / sponge control -> byte buffer RAM
  worst slack   1.063 ns,    6 paths: Keccak permutation (hash instance) -> register file
```

## Pembacaan
- Pada 14 ns dengan nilai bawaan jalur terburuk masih ada di dalam permutasi Keccak C5 instans hash (+0,721 ns, 133 dari 300 jalur); kelas inti NTT / memori / PWM menyusul pada +1,055 ns (84 jalur) dan permutasi sponge sampler pada +1,266 ns (83 jalur). Ketiga kelas berada dalam 0,55 ns satu sama lain: tidak ada satu blok yang mendominasi pada batasan ini.
- Dengan upaya kinerja tinggi kedua permutasi Keccak memimpin (+0,423 ns hash, +0,453 ns sampler) dan kelas berikutnya (pembungkus hash ke register file, +0,906 ns) tertinggal sekitar 0,5 ns.
- INFERENCE: mengganti permutasi C5 dengan K0 (S1) menghapus kelas permutasi dari daftar kritis; kelas inti NTT / memori / PWM (+1,055 ns pada 14 ns, yaitu jalur sekitar 12,9 ns untuk run fitter ini) lalu menjadi batas berikutnya, jadi S1 mungkin tidak menaikkan Fmax jauh melampaui dinding NTT. S1 mengukurnya (test plan V9).

## Ditambahkan setelah amandemen A2: 13 ns (F13-s2: batasan pertama yang tidak terpenuhi; F13-s1: terpenuhi)
```
## F13-s2_paths_slow100_summary.rpt
paths: 300, slack -0.185 .. 0.532 ns
  worst slack  -0.185 ns,  171 paths: NTT core / memory / PWM -> NTT core / memory / PWM
  worst slack  -0.030 ns,   33 paths: Keccak permutation (hash instance) -> Keccak permutation (hash instance)
  worst slack   0.178 ns,   96 paths: Keccak permutation (sampler sponge) -> Keccak permutation (sampler sponge)
## F13-s1_paths_slow100_summary.rpt
paths: 300, slack 0.227 .. 1.086 ns
  worst slack   0.227 ns,  130 paths: Keccak permutation (hash instance) -> Keccak permutation (hash instance)
  worst slack   0.571 ns,   65 paths: NTT core / memory / PWM -> NTT core / memory / PWM
  worst slack   0.716 ns,  105 paths: Keccak permutation (sampler sponge) -> Keccak permutation (sampler sponge)
```
- Pada 13 ns seed 2 (tidak terpenuhi, -0,185 ns) kelas terburuk adalah inti NTT / memori / PWM (171 dari 300 jalur); permutasi Keccak instans hash juga negatif (-0,030 ns) dan permutasi sponge sampler +0,178 ns. Pada seed 1 (terpenuhi, +0,227 ns) permutasi instans hash memimpin dan kelas NTT menyusul pada +0,571 ns.
- Jadi pada batas, inti NTT / memori dan permutasi C5 gagal bersama dalam 0,2 ns: dinding NTT sekitar 13,2 ns (sekitar 75 MHz) untuk desain ini dan setelan ini. INFERENCE untuk S1: mengganti permutasi tidak mengangkat dinding kelas NTT; S1 mengukurnya.
