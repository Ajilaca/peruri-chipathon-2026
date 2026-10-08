<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Worksheet seleksi Fase 8d, 2026-10-03

Perintah: `python3 scripts/quartus/select_8cd.py` (aturan `test_plan_8d.md` bagian 5, ditetapkan sebelum mengukur; setiap nilai dibaca dari file evidence yang disebut di tabel). Label: MEASURED (laporan Quartus, simulasi); median, t = siklus / Fmax, dan aturan adalah INFERENCE / perhitungan tim.
t dalam mikrodetik (siklus dibagi MHz); mencakup aritmetika program ditambah sampling, dalam satu sequencer, siklus simulasi dengan Fmax kompilasi kernel-only.

## 8d: OVERLAP (sampling noise selama transformasi) lawan STREAM
| Seed | Konfigurasi | ALM | Register | M10K | DSP | Setup / hold terburuk (ns) | Timing terpenuhi @ 40 ns | Fmax slow corner terendah (MHz) | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | STREAM | 10,975 | 3385 | 44 | 26 | 17.441 / 0.091 | ya | 44.33 | `quartus_SMP1.md` |
| 2 | STREAM | 10,989 | 3389 | 44 | 26 | 18.100 / 0.096 | ya | 45.66 | `quartus_SMP1-s2.md` |
| 3 | STREAM | 10,958 | 3377 | 44 | 26 | 16.616 / 0.085 | ya | 42.76 | `quartus_SMP1-s3.md` |
| 4 | STREAM | 11,002 | 3395 | 44 | 26 | 17.243 / 0.130 | ya | 43.94 | `quartus_SMP1-s4.md` |
| 5 | STREAM | 11,032 | 3391 | 44 | 26 | 15.231 / 0.103 | ya | 40.37 | `quartus_SMP1-s5.md` |
| 6 | STREAM | 11,018 | 3385 | 44 | 26 | 16.621 / 0.094 | ya | 42.77 | `quartus_SMP1-s6.md` |
| 1 | OVERLAP | 10,987 | 3405 | 44 | 26 | 17.049 / 0.146 | ya | 43.57 | `quartus_SMP2.md` |
| 2 | OVERLAP | 10,963 | 3414 | 44 | 26 | 17.242 / 0.086 | ya | 43.94 | `quartus_SMP2-s2.md` |
| 3 | OVERLAP | 11,009 | 3402 | 44 | 26 | 18.440 / 0.086 | ya | 46.38 | `quartus_SMP2-s3.md` |
| 4 | OVERLAP | 11,012 | 3387 | 44 | 26 | 16.269 / 0.082 | ya | 42.14 | `quartus_SMP2-s4.md` |
| 5 | OVERLAP | 10,998 | 3399 | 44 | 26 | 17.037 / 0.075 | ya | 43.55 | `quartus_SMP2-s5.md` |
| 6 | OVERLAP | 10,954 | 3368 | 44 | 26 | 17.925 / 0.082 | ya | 45.30 | `quartus_SMP2-s6.md` |

| | Median ALM (min-maks) | Register | M10K | DSP | Median Fmax (min-maks) MHz | Siklus KeyGen (rerata) | Siklus Encrypt (rerata) | Siklus Decrypt (rerata) | t KeyGen (us) | t Encrypt (us) |
|---|---|---|---|---|---|---|---|---|---|---|
| STREAM | 10,995.5 (10,958-11,032) | 3377-3395 | 44-44 | 26-26 | 43.355 (40.37-45.66) | 7089.1 | 8548.6 | 3109.0 | 163.5138 | 197.1761 |
| OVERLAP | 10,992.5 (10,954-11,012) | 3368-3414 | 44-44 | 26-26 | 43.755 (42.14-46.38) | 6344.1 | 7654.6 | 3109.0 | 144.9924 | 174.9416 |

Sumber siklus: `cycles_v1.json`, `cycles_v2.json` (masukan sama untuk setiap varian).

### Aturan adopsi (OVERLAP atas STREAM)
- PASS: benar (verification_status: V1-V8, kedua simulator, kontrol gagal, formal)
- PASS: fit berhasil untuk keduanya dan timing terpenuhi pada 40,000 ns di setiap seed untuk OVERLAP
- PASS: t = c / F lebih rendah untuk OVERLAP daripada STREAM untuk KeyGen (144.9924 < 163.5138 us) dan untuk Encrypt (174.9416 < 197.1761 us)
- PASS: M10K(OVERLAP) <= M10K(STREAM) di setiap seed

Hasil aturan: OVERLAP DIADOPSI.

- informasi STREAM (SMP1-20, 20,000 ns, seed 1): ALM 11,031, M10K 44, setup terburuk 1.783 ns (terpenuhi), Fmax slow corner terendah 54.89 MHz, `quartus_SMP1-20.md`
- informasi OVERLAP (SMP2-20, 20,000 ns, seed 1): ALM 11,049, M10K 44, setup terburuk 1.535 ns (terpenuhi), Fmax slow corner terendah 54.16 MHz, `quartus_SMP2-20.md`

