# peruri-chipathon-2026

Tim J5 (Institut Teknologi Bandung), CHIP 2026 Hackathon (PERURI Digital Summit),
kategori *IC Chip Design & FPGA Implementation*.

**Ide:** akselerator perangkat keras **ML-KEM-768** (NIST FIPS 203, kriptografi pasca-kuantum)
dengan pendekatan *hardware/software co-design* pada Terasic DE10-Nano (Intel Cyclone V SoC
5CSEBA6U23I7): Keccak-f[1600] dan NTT/INTT di FPGA, alur protokol dan baseline perangkat lunak
di HPS (ARM Cortex-A9). Target utama: eksekusi waktu-konstan yang dibuktikan, hasil bit-exact
terhadap vektor uji resmi, dan angka sumber daya/timing yang diukur dari Quartus.

## Status
Tahap awal. **Belum ada hasil sintesis, simulasi RTL, atau pengukuran papan.** Angka apa pun yang
kelak muncul di repositori ini hanya berasal dari laporan Quartus atau uji pada papan dan
disimpan sebagai bukti di `docs/evidence/`. Rencana: `docs/ROADMAP.md`.

## Batas klaim
- Parameter ML-KEM tidak diubah; inovasi hanya pada arsitektur perangkat keras.
- Ketahanan terhadap serangan side-channel (daya/EM) **tidak diklaim** pada tahap inti; itu tahap lanjut.
- Tidak ada klaim "kebal kuantum" atau percepatan sebelum ada pengukuran.

## Peta repositori
| Folder | Isi |
|---|---|
| `rtl/` | SystemVerilog yang dapat disintesis |
| `tb/` | testbench cocotb dan model acuan Python (`tb/golden/`) |
| `formal/` | properti SymbiYosys |
| `quartus/` | proyek Quartus, Platform Designer, `.sdc` |
| `sw/hps/` | kode sisi HPS (ARM Linux) |
| `docs/` | brief proyek, roadmap, keputusan (ADR), bukti, referensi proposal |
| `scripts/` | penyiapan lingkungan dan uji dasar |
| `.claude/` | pengaturan dan skill Claude Code untuk tim |

## Menyiapkan lingkungan (Ubuntu 24.04)
```bash
scripts/setup_tooling.sh check      # laporan saja, tidak mengubah apa pun
scripts/setup_tooling.sh install    # OSS CAD Suite, .venv, plugin Claude Code, lalu verifikasi
. scripts/env.sh                    # PATH alat + aktifkan .venv
```
Quartus Prime Lite dan Questa dipasang manual (butuh unduhan dan lisensi); skrip hanya mendeteksi
dan menguji.

## Lisensi
Belum ditentukan (keputusan tim, lihat `docs/decisions/PENDING.md`).
