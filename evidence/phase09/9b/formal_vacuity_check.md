# Pemeriksaan sinyal bebas (`(* anyseq *)`) pada stub formal, 2026-10-03

Mengapa: saat membuktikan `mlkem_hash` (Fase 9b) sebuah bukti memberi PASS padahal stub sponge tidak pernah mencapai state squeeze-nya (test plan 9b, Amandemen A1, butir 2). Stub formal lain di repository yang memakai `(* anyseq *)` diperiksa dengan pernyataan cover (salinan scratch, file repository tidak diubah). Semua hasil di bawah MEASURED dengan SymbiYosys (mode cover, boolector).

| Stub / bukti | Apa yang dicakup | Hasil |
|---|---|---|
| `formal/phase09-integration/9b/keccak_sponge_r2_stub.sv`, sinyal dideklarasikan `logic` (versi pertama) | state squeeze, word digest setelah 3 word, `done_o` | tidak tercapai (`f_go` bebas ternyata konstanta): bukti itu vakum dan dibuang |
| yang sama dengan sinyal dideklarasikan `wire` (versi repository) | yang sama | semua tercapai (langkah 3-9); bukti dan kontrolnya dijalankan ulang |
| `formal/phase08-keccak-stream/8c/keccak_sampler_stub.sv` (sinyal dideklarasikan `logic`, dibaca di assignment kontinu), top `kpke_sched_smp_formal_top.sv`, kedalaman 20 dan 140 | sampler sibuk, sebuah beat ditawarkan (`smp_cvalid`), sebuah beat ditulis ke penyimpanan (`smp_wr`), state sampling, `smp_in_ready`, `smp_clast`, `smp_bytes != 0` | semua tercapai pada langkah 5, jadi sinyal bebas stub itu memang bebas di 8c; state PWMS (`st == SPwms`) tidak tercapai dalam kedalaman 140: itu efek kedalaman (PWMS pertama datang setelah enam polinomial tersampel masing-masing minimal 128 beat), bukan bukti vakum; properti PWMS 8c bersifat induktif dan tidak ditunjukkan oleh jejak basis |
| `formal/phase03-multilane/modmul_reduce_uf.sv` (`uf_p`, `logic`) | tidak dicakup terpisah: kontrolnya `k1_negctl_noack.sby` (bukti tanpa batasan konsistensi harus FAIL) gagal sesuai syarat di evidence Fase 3, yang hanya dapat terjadi bila `uf_p` bebas | konsisten dengan bebas |
