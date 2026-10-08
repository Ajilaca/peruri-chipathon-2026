# ADR 0001: Ide proyek - akselerator ML-KEM-768 (HW/SW co-design) di DE10-Nano

- Status: Accepted
- Tanggal: 2026-09-28
- Diputuskan oleh: tim J5 (dasar: draf proposal tim, judul dan Bagian 1-2 seperti yang ditulis tim)

## Konteks
Penyaringan awal membandingkan banyak ide di empat subtema resmi. Draf proposal tim memakai judul
"Akselerasi ML-KEM pada Hardware FPGA: Prototipe Kriptografi Pasca-Kuantum untuk
Perlindungan Data" dan menjelaskan ML-KEM-768 dengan Keccak-f[1600] dan NTT/INTT di fabric.

## Keputusan
Membangun akselerator ML-KEM-768 (HW/SW co-design) di DE10-Nano. HPS: alur protokol,
baseline, pengukuran waktu. Fabric: NTT/INTT + pointwise, Keccak, sampler, compress/encode, kendali.

## Konsekuensi
- Roadmap: `docs/ROADMAP.md`.
- Subtema lomba yang dideklarasikan adalah keputusan terpisah (lihat PENDING.md).
- Ide lain yang disaring tidak dikejar kecuali ADR baru membukanya kembali.

## Bukti
`docs/proposal/references.md`.
