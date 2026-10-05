# rtl/

SystemVerilog yang dapat disintesis, satu modul per file. Setiap file diawali `` `default_nettype none `` dan diakhiri
`` `default_nettype wire ``. Satu domain clock, reset asinkron aktif rendah pada kendali.
Tidak ada blok yang ditulis sebelum model acuannya ada (lihat [../docs/ROADMAP.md](../docs/ROADMAP.md)).
Angka sumber daya dan timing hanya dari Quartus.

| Folder | Isi | Fase |
|---|---|---|
| [arith/](arith/README.md) | reducer modular (fold, Barrett, Montgomery), butterfly, ROM twiddle | 5, 5M |
| [ntt/](ntt/README.md) | inti NTT/INTT: varian per fase dan wrapper revisi Quartus | 1 sampai 6 |
| `mem/` | memori polinomial: banked, multiport, M10K 16 bank (`poly_mem_m10k`), ROM peta bank | 2, 5M, 6 |
| `keccak/` | Keccak-f[1600] 1 ronde (`keccak_f1600`) dan 2 ronde (`_r2`), sponge SHA3/SHAKE | 7, 8a |
| `sample/` | sampler streaming: SampleNTT, CBD2, wrapper `keccak_sampler` | 8b |
| `sched/` | sequencer K-PKE, unit PWM, ROM program, penyimpan polinomial | 6, 8c, 8d, 9M |
| `mlkem/` | inti ML-KEM: `mlkem_core` ... `mlkem_core4`, codec, hash, FO compare, ROM kendali | 9, 9M |

## Aturan membaca folder ini

- File lama tidak dihapus. Konfigurasi yang sudah diukur dibekukan sebagai bukti, dan varian baru berupa file baru
  (`ntt_core_c3_p6`, `ntt_core_s10`, `mlkem_core4`, ...) atau parameter.
- Wrapper tipis `*_p6.sv`, `*_c4b_b.sv` dan sejenisnya hanya menetapkan parameter satu revisi Quartus. Tidak ada logika di dalamnya.
- File `twiddle_rom*.sv`, `bank_map_rom.sv`, `gamma_rom.sv`, `*_prog_rom*.sv`, `mlkem_ctl_rom*.sv` dibangkitkan oleh skrip di
  [../scripts/build/](../scripts/README.md). Jangan diedit tangan; jalankan ulang generatornya.
- Inti yang sedang dipakai: `mlkem_core4` (K4, status *Proposed*) di atas `kpke_smp_top_s10o`, `ntt_core_s10`, `poly_mem_m10k`.
  Blok dan urutan panggilnya terbaca dari header tiap file.
