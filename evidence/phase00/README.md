# Phase 0: model acuan dan vektor

Status: DONE. Halaman hasil: [../../docs/results/phase00.md](../../docs/results/phase00.md).

Tujuan. Membuat model acuan ML-KEM-768 yang mandiri dan memastikannya cocok dengan vektor resmi.

Yang diuji. Parameter terkunci, vektor ACVP (NIST sample set), uji silang acak dengan kyber-py, temuan errata FIPS 203.

Alat. Python, pytest, `check_params.py`, kyber-py (venv terpisah).

Hasil utama. Model acuan mereproduksi vektor ACVP ML-KEM-768. Dua temuan errata, keduanya non-normatif (ADR 0003). Tidak ada RTL.

File penting.
- [kat_mlkem768.txt](kat_mlkem768.txt)
- [crosscheck_kyberpy.txt](crosscheck_kyberpy.txt)
- [fips203_errata.md](fips203_errata.md)

Semua file di folder ini dibuat oleh alat, bukan diketik tangan. Angka Quartus berasal dari kompilasi kernel-only dengan virtual pin.
