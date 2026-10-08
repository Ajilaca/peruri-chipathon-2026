# rtl/mlkem_final/

Inti ML-KEM-768 final (K4, `mlkem_core4`) dengan semua file yang dibutuhkan, dikumpulkan dalam satu direktori supaya mudah dicari.
Modul teratas: `mlkem_core4`. Daftar file sama dengan daftar sumber proyek Quartus `quartus/phase09i4_core/K4.qsf` (51 file).

## Hubungan dengan folder lain

- Isi folder ini adalah salinan byte-per-byte dari file di `rtl/arith`, `rtl/ntt`, `rtl/mem`, `rtl/keccak`, `rtl/sample`, `rtl/sched`, dan `rtl/mlkem`. Sumber aslinya tidak diubah dan tidak dipindah, karena proyek Quartus, testbench, formal, dan semua evidence memakai path lama.
- Kalau file asli berubah, salinan di sini harus disalin ulang. Cek dengan `cd rtl/mlkem_final && sha256sum -c SHA256SUMS` (membandingkan salinan dengan daftar hash) atau bandingkan dengan file asli di tabel di bawah.
- Konfigurasi K4 yang diukur memakai parameter `HASH_C5 = 0`, `SMP_C5 = 0`, `NTT_P6 = 1`, `NTT_AR = 1`, `CODEC_W2 = 1` (ADR 0035, 0037, 0038, 0041, 0042). Nilai bawaan di `mlkem_core4.sv` berbeda; parameter di atas diberikan oleh revisi Quartus `quartus/phase09i4_core/` dan oleh testbench.
- Port dan format data dijelaskan di header `mlkem_core4.sv` dan di [../../sw/hps/README.md](../../sw/hps/README.md).

## Isi per kelompok

### mlkem: inti ML-KEM: pengendali, codec, hash, pembanding FO, RAM byte, ROM kendali

| File | Asal |
|---|---|
| `mlkem_bytedst.sv` | `rtl/mlkem/mlkem_bytedst.sv` |
| `mlkem_bytedst2.sv` | `rtl/mlkem/mlkem_bytedst2.sv` |
| `mlkem_core4.sv` | `rtl/mlkem/mlkem_core4.sv` |
| `mlkem_ctl_rom.sv` | `rtl/mlkem/mlkem_ctl_rom.sv` |
| `mlkem_ctl_rom3.sv` | `rtl/mlkem/mlkem_ctl_rom3.sv` |
| `mlkem_fifo4.sv` | `rtl/mlkem/mlkem_fifo4.sv` |
| `mlkem_fo_cmp.sv` | `rtl/mlkem/mlkem_fo_cmp.sv` |
| `mlkem_hash.sv` | `rtl/mlkem/mlkem_hash.sv` |
| `mlkem_ldpoly.sv` | `rtl/mlkem/mlkem_ldpoly.sv` |
| `mlkem_ldpoly2.sv` | `rtl/mlkem/mlkem_ldpoly2.sv` |
| `mlkem_ldpoly2o.sv` | `rtl/mlkem/mlkem_ldpoly2o.sv` |
| `mlkem_pack.sv` | `rtl/mlkem/mlkem_pack.sv` |
| `mlkem_pack2.sv` | `rtl/mlkem/mlkem_pack2.sv` |
| `mlkem_ram.sv` | `rtl/mlkem/mlkem_ram.sv` |
| `mlkem_stpoly.sv` | `rtl/mlkem/mlkem_stpoly.sv` |
| `mlkem_stpoly2.sv` | `rtl/mlkem/mlkem_stpoly2.sv` |
| `mlkem_unpack.sv` | `rtl/mlkem/mlkem_unpack.sv` |
| `mlkem_unpack2.sv` | `rtl/mlkem/mlkem_unpack2.sv` |
| `mlkem_wordbytes.sv` | `rtl/mlkem/mlkem_wordbytes.sv` |
| `mlkem_wordbytes2.sv` | `rtl/mlkem/mlkem_wordbytes2.sv` |

### sched: mesin K-PKE: sequencer, unit PWM, penyimpan polinomial, ROM program

| File | Asal |
|---|---|
| `gamma_rom.sv` | `rtl/sched/gamma_rom.sv` |
| `kpke_sched_smp.sv` | `rtl/sched/kpke_sched_smp.sv` |
| `kpke_sched_smp4.sv` | `rtl/sched/kpke_sched_smp4.sv` |
| `kpke_smp_prog_rom.sv` | `rtl/sched/kpke_smp_prog_rom.sv` |
| `kpke_smp_top_s10.sv` | `rtl/sched/kpke_smp_top_s10.sv` |
| `kpke_smp_top_s10o.sv` | `rtl/sched/kpke_smp_top_s10o.sv` |
| `poly_store_smp.sv` | `rtl/sched/poly_store_smp.sv` |
| `pwm_unit.sv` | `rtl/sched/pwm_unit.sv` |

### ntt: inti NTT/INTT S10 dan paket parameter

| File | Asal |
|---|---|
| `modmul_reduce_staged.sv` | `rtl/ntt/modmul_reduce_staged.sv` |
| `ntt_core_s10.sv` | `rtl/ntt/ntt_core_s10.sv` |
| `ntt_core_s10_p5.sv` | `rtl/ntt/ntt_core_s10_p5.sv` |
| `ntt_pkg.sv` | `rtl/ntt/ntt_pkg.sv` |
| `pipe_delay.sv` | `rtl/ntt/pipe_delay.sv` |
| `twiddle_rom.sv` | `rtl/ntt/twiddle_rom.sv` |

### mem: memori polinomial 16 bank 1R1W (M10K)

| File | Asal |
|---|---|
| `poly_mem_m10k.sv` | `rtl/mem/poly_mem_m10k.sv` |

### arith: aritmetika modular: reducer Barrett dan butterfly

| File | Asal |
|---|---|
| `butterfly_m6.sv` | `rtl/arith/butterfly_m6.sv` |
| `half_mod.sv` | `rtl/arith/half_mod.sv` |
| `modmul_barrett.sv` | `rtl/arith/modmul_barrett.sv` |
| `modmul_fold.sv` | `rtl/arith/modmul_fold.sv` |
| `modmul_montgomery.sv` | `rtl/arith/modmul_montgomery.sv` |
| `modmul_sel.sv` | `rtl/arith/modmul_sel.sv` |
| `twiddle_rom_half.sv` | `rtl/arith/twiddle_rom_half.sv` |

### keccak: Keccak-f[1600] dan sponge SHA3/SHAKE

| File | Asal |
|---|---|
| `keccak_f1600.sv` | `rtl/keccak/keccak_f1600.sv` |
| `keccak_f1600_r2.sv` | `rtl/keccak/keccak_f1600_r2.sv` |
| `keccak_pkg.sv` | `rtl/keccak/keccak_pkg.sv` |
| `keccak_round.sv` | `rtl/keccak/keccak_round.sv` |
| `keccak_sponge.sv` | `rtl/keccak/keccak_sponge.sv` |
| `keccak_sponge_r2.sv` | `rtl/keccak/keccak_sponge_r2.sv` |

### sample: sampler streaming SampleNTT dan CBD2

| File | Asal |
|---|---|
| `cbd2_core.sv` | `rtl/sample/cbd2_core.sv` |
| `keccak_sampler.sv` | `rtl/sample/keccak_sampler.sv` |
| `sample_ntt_core.sv` | `rtl/sample/sample_ntt_core.sv` |

File `SHA256SUMS` berisi hash tiap salinan.
