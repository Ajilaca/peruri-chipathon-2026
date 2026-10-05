# formal/run/

Driver Python untuk analisis formal. Tiap `run_formal_phase*.py` menjalankan semua `.sby` satu fase, memeriksa bahwa hasil
sama dengan yang diharapkan (properti PASS, kontrol negatif FAIL) dan mencetak tabel. Keluarannya disalin ke `evidence/`.

| File | Dipakai untuk |
|---|---|
| `run_formal_slang.py` | basis bersama (menjalankan `sby`, menyiapkan sumber dengan slang); Phase 1 sampai 3 |
| `run_formal_phase4.py`, `phase5*.py`, `phase6.py`, `s10.py` | Phase 4 sampai 6 |
| `run_formal_phase7.py`, `phase8a.py` ... `phase8d.py` | Phase 7 dan 8 |
| `run_formal_phase9a.py`, `9b`, `9c` | Phase 9 |
| `run_formal_phase9m1.py`, `9m3`, `9f1`, `9f1b`, `9s2`, `9s2b`, `9i4` | Phase 9M |

```
. scripts/env.sh
python3 formal/run/run_formal_phase7.py
python3 formal/run/run_formal_phase9i4.py [all|proofs|cover|retry]
```

Skrip membuat salinan sementara di `formal/work/` untuk mutan kontrol negatif; RTL asli tidak diubah.
Beberapa run memerlukan puluhan menit. Skrip uji di [../../scripts/test/](../../scripts/README.md) memanggilnya.
