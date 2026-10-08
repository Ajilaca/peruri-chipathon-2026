<!-- claim-lint: skip-file (internal evidence record, not proposal text) -->
# Worksheet seleksi Fase 8c, 2026-10-03

Perintah: `python3 scripts/quartus/select_8cd.py` (aturan `test_plan_8c.md` bagian 5, ditetapkan sebelum mengukur; setiap nilai dibaca dari file evidence yang disebut di tabel). Label: MEASURED (laporan Quartus, simulasi); median, t = siklus / Fmax, dan aturan adalah INFERENCE / perhitungan tim.
t dalam mikrodetik (siklus dibagi MHz); mencakup aritmetika program ditambah sampling, dalam satu sequencer, siklus simulasi dengan Fmax kompilasi kernel-only.

## 8c: STREAM (A_hat disampel langsung ke unit PWM) lawan STORE (A_hat disampel ke slot)
| Seed | Konfigurasi | ALM | Register | M10K | DSP | Setup / hold terburuk (ns) | Timing terpenuhi @ 40 ns | Fmax slow corner terendah (MHz) | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| 1 | STORE | 10,967 | 3364 | 55 | 26 | 15.734 / 0.131 | ya | 41.21 | `quartus_SMP0.md` |
| 2 | STORE | 10,969 | 3342 | 55 | 26 | 16.417 / 0.098 | ya | 42.40 | `quartus_SMP0-s2.md` |
| 3 | STORE | 10,959 | 3362 | 55 | 26 | 15.789 / 0.094 | ya | 41.30 | `quartus_SMP0-s3.md` |
| 4 | STORE | 10,944 | 3345 | 55 | 26 | 17.415 / 0.125 | ya | 44.28 | `quartus_SMP0-s4.md` |
| 5 | STORE | 10,941 | 3354 | 55 | 26 | 16.272 / 0.134 | ya | 42.14 | `quartus_SMP0-s5.md` |
| 6 | STORE | 10,957 | 3378 | 55 | 26 | 17.119 / 0.091 | ya | 43.70 | `quartus_SMP0-s6.md` |
| 1 | STREAM | 10,975 | 3385 | 44 | 26 | 17.441 / 0.091 | ya | 44.33 | `quartus_SMP1.md` |
| 2 | STREAM | 10,989 | 3389 | 44 | 26 | 18.100 / 0.096 | ya | 45.66 | `quartus_SMP1-s2.md` |
| 3 | STREAM | 10,958 | 3377 | 44 | 26 | 16.616 / 0.085 | ya | 42.76 | `quartus_SMP1-s3.md` |
| 4 | STREAM | 11,002 | 3395 | 44 | 26 | 17.243 / 0.130 | ya | 43.94 | `quartus_SMP1-s4.md` |
| 5 | STREAM | 11,032 | 3391 | 44 | 26 | 15.231 / 0.103 | ya | 40.37 | `quartus_SMP1-s5.md` |
| 6 | STREAM | 11,018 | 3385 | 44 | 26 | 16.621 / 0.094 | ya | 42.77 | `quartus_SMP1-s6.md` |

| | Median ALM (min-maks) | Register | M10K | DSP | Median Fmax (min-maks) MHz | Siklus KeyGen (rerata) | Siklus Encrypt (rerata) | Siklus Decrypt (rerata) | t KeyGen (us) | t Encrypt (us) |
|---|---|---|---|---|---|---|---|---|---|---|
| STORE | 10,958.0 (10,941-10,969) | 3342-3378 | 55-55 | 26-26 | 42.270 (41.21-44.28) | 8268.1 | 9727.6 | 3109.0 | 195.6031 | 230.1294 |
| STREAM | 10,995.5 (10,958-11,032) | 3377-3395 | 44-44 | 26-26 | 43.355 (40.37-45.66) | 7089.1 | 8548.6 | 3109.0 | 163.5138 | 197.1761 |

Sumber siklus: `cycles_v0.json`, `cycles_v1.json` (masukan sama untuk setiap varian).

### Aturan adopsi (STREAM atas STORE)
- PASS: benar (verification_status: V1-V8, kedua simulator, kontrol gagal, formal)
- PASS: fit berhasil untuk keduanya dan timing terpenuhi pada 40,000 ns di setiap seed untuk STREAM
- PASS: t = c / F lebih rendah untuk STREAM daripada STORE untuk KeyGen (163.5138 < 195.6031 us) dan untuk Encrypt (197.1761 < 230.1294 us)
- PASS: M10K(STREAM) <= M10K(STORE) di setiap seed

Hasil aturan: STREAM DIADOPSI.

- informasi STORE (SMP0-20, 20,000 ns, seed 1): ALM 11,058, M10K 55, setup terburuk 0.992 ns (terpenuhi), Fmax slow corner terendah 52.61 MHz, `quartus_SMP0-20.md`
- informasi STREAM (SMP1-20, 20,000 ns, seed 1): ALM 11,031, M10K 44, setup terburuk 1.783 ns (terpenuhi), Fmax slow corner terendah 54.89 MHz, `quartus_SMP1-20.md`

