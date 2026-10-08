<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# S10 lawan S7: ke mana ALM pergi (MEASURED, "Fitter Resource Utilization by Entity" Quartus, seed 1, 40,000 ns)

Panel sumber: `quartus/phase05m_memsched/output_files_S7/S7.fit.rpt` dan `quartus/phase06_sched/output_files_S10/S10.fit.rpt` (tidak di-commit: `output_files*` diabaikan git; totalnya ada di
`evidence/phase05m/s7/quartus_S7.md` dan `evidence/phase06/s10/quartus_S10.md`). Nilai disalin dari laporan; selisih adalah INFERENCE.

| Entitas | ALM dibutuhkan S7 | ALM dibutuhkan S10 | Register S7 | Register S10 | Bit memori blok / M10K S7 | Bit memori blok / M10K S10 |
|---|---:|---:|---:|---:|---:|---:|
| seluruh inti (`ntt_core_s7_p7` / `ntt_core_s10_p5`) | 9,394.0 | 5,091.0 | 4,317 | 545 | 30,423 / 31 | 4,069 / 24 |
| memori (`poly_mem_multiport_split` / `poly_mem_m10k`) | 7,647.3 | 3,343.4 | 4,018 | 266 | 29,817 / 25 | 3,152 / 17 |
| semua yang lain (butterfly, ROM twiddle, FSM, delay line) = inti - memori | 1,726.2 | 1,727.1 | 299 | 279 | - | - |

Pembacaan (INFERENCE):
- Seluruh penghematan (sekitar 4,300 ALM) ada di memori; sisa inti berukuran sama (1,726 lawan 1,727 ALM). Tidak ada fungsi yang dihapus: jadwal sama, aritmetika sama, bit-exact, 118 siklus.
- Dihapus oleh S10: (1) penyimpanan 256 x 12 bit di flip-flop dengan decode tulis per word dan multiplexer baca 32 word (register memori S7 4,018, S10 266; 3,072 bit penyimpanan kini ada di 16 blok RAM masing-masing 192
  bit, satu per bank, terdaftar sebagai `altsyncram ... g_bank[n].mem` dengan 192 bit memori blok masing-masing); (2) riak arbitrasi slot 16-port dan register potongnya (jalur kritis S7 yang terukur); (3) 16 ROM peta bank
  yang ditempatkan Quartus di M10K (S7: `bank_map_rom:g_map[0..15]`, 1,280-2,048 bit dan 1-2 M10K masing-masing), diganti XOR empat bit alamat.
- Yang tersisa di memori S10 (3,343 ALM): pemilih 16 arah (offset baca per bank, offset / data / enable tulis per bank, data baca per port) dan pemeriksaan overflow. Batas atas studi S9 untuk
  crossbar (sekitar 1,920 ALM, ESTIMATE hitungan LUT) terlalu rendah: entitas memori terukur adalah 3,343 ALM. Estimasi itu mencakup dua crossbar data saja, tidak pemilih alamat dan logika
  overflow; dicatat di sini sebagai kesalahan estimasi, tidak diubah di studi.
