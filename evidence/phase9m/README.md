# Phase 9M: optimasi inti

Status: PARTIAL. Halaman hasil: [../../docs/results/phase9m.md](../../docs/results/phase9m.md).

**Tujuan.** Mengecilkan dan mempercepat inti ML-KEM-768 Phase 9 tanpa mengubah matematikanya. Tiap langkah punya
rencana dan aturan adopsi yang ditulis sebelum pengukuran.

**Struktur.**
- `batch1/`: 9m1 (codec dua byte), 9m2 (inti pada 20 ns), 9m3 (hash K0), 9f0 (lokasi batas Fmax), 9f1 (sampler K0, K1), 9f1b (hash latar belakang, K1b).
- `batch2/`: 9s2 (K2, register setelah Barrett), 9s2b (K3, alamat issue terregistrasi), 9i4 (K4, pemuatan di belakang mesin).
- File di tingkat ini: analisis jalur kritis dan profil.

**Yang diuji.** Bit-exact terhadap model acuan dan ACVP di dua simulator, siklus konstan, kontrol negatif, formal (`core3`, `core4`),
Quartus enam seed pada 40 ns dan 15 ns.

**Alat.** cocotb (Verilator, Icarus), SymbiYosys, Quartus.

**Hasil utama (K4, `mlkem_core4`).** 8.416 / 9.611 / 12.989 siklus, 14.222,0 ALM median pada 40 ns,
Fmax median 76,665 MHz, latensi 109,8 / 125,4 / 169,4 µs (perhitungan tim). 15 ns terpenuhi di 6 dari 6 seed.
Tiga bukti formal berbatas (P1 dan NC-E1-4 di `core4`, NC-B7 di `core3`) habis waktu dan dicatat TIMEOUT, jadi M-11 tetap MISSING.
Keputusan atas hasil (ADR 0035, 0037, 0038, 0040 sampai 0043) menunggu tim.

**File penting.**
- [batch2/9i4/result_9i4.md](batch2/9i4/result_9i4.md), [batch2/9i4/selection_worksheet.md](batch2/9i4/selection_worksheet.md), [batch2/9i4/formal.md](batch2/9i4/formal.md)
- [batch2/9s2b/result_9s2b.md](batch2/9s2b/result_9s2b.md), [batch2/9s2/result_9s2.md](batch2/9s2/result_9s2.md)
- [batch1/9f1b/](batch1/9f1b/), [batch1/9m3/](batch1/9m3/), [batch1/9m1/](batch1/9m1/)
- [critical_paths_MW.md](critical_paths_MW.md), [profile.md](profile.md)
