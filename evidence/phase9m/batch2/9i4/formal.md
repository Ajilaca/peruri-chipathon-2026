# Run formal Fase 9I butir 4, 2026-10-05 (V8)

MEASURED dengan SymbiYosys (yosys-slang, boolector, `formal/run/run_formal_phase9i4.py`; direktori kerja `formal/work/phase9i4_*`, diabaikan git). Alur 9f1b disesuaikan untuk `rtl/mlkem/mlkem_core4.sv` dengan stub protokol sub-blok (`formal/phase09m-optimisation/9i4/`). Hanya kendali dan rentang; nilai dicakup simulasi. Hasil run `proofs` (2026-10-05) dan run `cover`:

| Kelompok | Bukti | Diharapkan | Hasil | Detail mesin | Waktu (s) |
|---|---|---|---|---|---|
| A Fase 9I butir 4 | pengendali mlkem_core4 (E1 non-interferensi termasuk `pend_q` dan `eng_dn_q`, S1-S7, B1-B7) | PASS | PASS | basecase = pass, induction = pass | 8.6 |
| C Keterjangkauan | sebuah muat berjalan saat mesin sibuk dan sebuah slot ditandai; RUNJ dengan mesin selesai; cover 9f1b sebelumnya | PASS | PASS | bmc = pass | 868.9 |
| B Kontrol negatif | NC-JOIN4: RUNJ tidak menunggu mesin (P1) | FAIL | GAGAL seperti diharuskan | bmc = FAIL; failed assert `mlkem_core4_formal_top.sv:200` | 355.5 |
| P Terbatas | P1: tidak ada STP atau SDL saat mesin sibuk (bounded model check, kedalaman 160, RTL nyata) | PASS | TIMEOUT | tidak ada hasil | 1,800 |
| B Kontrol negatif | NC-E1-4: mask interlock bergantung pada satu bit data register file (E1) | FAIL | TIMEOUT | tidak ada hasil | 1,800 |

## Timeout (dinyatakan, tidak disembunyikan)
- P1 tidak terbukti secara formal. Pemeriksaan terbatas (kedalaman 160, panjang program terpanjang) tidak selesai dalam 1.800 s. Percobaan ulang dengan batas 4 jam dimulai pada 2026-10-05 dan dihentikan atas keputusan tim (Jevan) setelah sekitar 2 jam 40 menit tanpa hasil; dicatat sebagai TIMEOUT. P1 hanya dicakup simulasi: ACVP 100 % di kedua simulator, test siklus konstan, dan kontrol `ncjoin` dan `ncgrant` (gagal sesuai syarat), lihat `sim.md`.
- NC-E1-4 tidak selesai (1.800 s; percobaan ulang yang sama). Jadi tidak ada evidence formal bahwa properti E1 menangkap mask interlock yang bergantung pada data; kontrol simulasi `ncilk` dan `ncthrld` menguji interlock tetapi bukan mutasi itu. Properti E1 sendiri lolos (baris A).
- NC-JOIN4 (kontrol negatif P1) gagal sesuai syarat, jadi P1 dapat gagal (ia mendeteksi tunggu yang hilang); ini evidence bahwa properti tidak vakum, bukan bukti P1 pada desain nyata.
- Kelas yang sama dengan batas NC-B7 Batch 1 (`../../batch1/9f1b/formal.md`): pemeriksaan terbatas pada RTL nyata di kedalaman 160 yang tidak selesai dalam waktu yang diberikan. Sebabnya adalah inferensi (ruang pencarian 160 langkah dengan handshake bebas sub-blok stub; tidak ada profil solver, dan run pertama berbagi mesin dengan job Quartus dan simulator).

## Apa yang diubah agar bukti berjalan (dinyatakan)
- Run keselamatan pertama (sebelum properti akhir) gagal induksi untuk dua properti, P1 (mesin tidak sibuk di STP dan SDL) dan P2 (`pend_q` sama dengan 0 saat pengendali idle). Keduanya benar untuk ROM program tetapi memerlukan invarian pada posisi program yang belum ditulis. P2 dibuang dan tidak terbukti (rencana tidak mensyaratkannya; tidak diklaim di mana pun). P1 dipindah ke pemeriksaan terbatas (`mlkem_core4_bmc.sby`, parameter `P1_ON`; run keselamatan memakai `-G P1_ON=0`).
- Top formal memakai mesin stub `kpke_smp_top_s10o` (`stubs_9i4.sv`); parameter `NTT_P6` dan `NTT_AR` diterima dan diabaikan di sana, jadi hasil ini tidak bergantung pada parameter NTT.
- Run `cover` mengelaborasi file working tree pada saat dimulai, setelah run `proofs`; pengendali, varian mesin, dan nilai bawaan `NTT_P6` dan `NTT_AR` sama di kedua run.

## Yang tidak ditunjukkan ini
Tidak ada di sini yang membuktikan aritmetika atau nilai (simulasi mencakupnya); model formal memakai stub protokol untuk mesin, sampler, dan sponge; P1 dan NC-E1-4 tidak punya hasil formal.
