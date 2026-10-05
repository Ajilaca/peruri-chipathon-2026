# quartus/

Proyek Quartus (`.qpf`, `.qsf`, `.sdc`) per fase dan per langkah, dengan skrip menjalankan revisi. Perangkat: 5CSEBA6U23I7.
Semua revisi kernel-only dengan virtual pin; tidak ada proyek sistem dengan HPS selain integrasi GHRD Phase 4 (lihat `evidence/phase04/`).

| Folder | Fase |
|---|---|
| `phase01_ntt_c0`, `phase02_mem_c1`, `phase03_multilane_c2` | 1 sampai 3 |
| `phase04_pipeline_c3`, `phase05_arith_c4` | 4, 5 |
| `phase05m_memsched`, `phase06_sched` | 5M, 6 (S10) |
| `phase07_keccak`, `phase08_keccak`, `phase08b_sampler`, `phase08c_smp` | 7, 8 |
| `phase09a_codec`, `phase09b_hashfo`, `phase09c_core` | 9 |
| `phase09m1_core`, `phase09m2_core`, `phase09m3_core`, `phase09f0_core`, `phase09f1_core`, `phase09f1b_core`, `phase09s2_core`, `phase09s2b_core`, `phase09i4_core` | 9M |

Satu revisi dikompilasi dengan `quartus_sh --flow compile <revisi>`, satu kompilasi pada satu waktu.
Revisi seed berakhiran `-s2` sampai `-s6`; revisi `-15` memakai batasan 15 ns, `-20` batasan 20 ns, tanpa akhiran 40 ns.
Setiap clock didefinisikan di `.sdc`. Pin berasal dari dokumentasi Terasic, tidak dikarang.

`output_files/` dan `db/` diabaikan Git dan dipindah ke luar repository oleh `scripts/quartus/archive_quartus_outputs.py`.
Ekstrak yang dikomit ada di `evidence/` (dibuat oleh skill `/quartus-report`). Output penuh: lihat bagian *Quartus Outputs* di
[../README.md](../README.md).
