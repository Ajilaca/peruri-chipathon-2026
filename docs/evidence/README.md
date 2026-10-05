# Evidence per fase

Bukti mentah ada di [`../../evidence/`](../../evidence/README.md), bukan di folder ini. Folder ini hanya indeks.
Bukti tidak dipindah ke `docs/` karena ribuan rujukan di file hasil, ADR, laporan dan skrip memakai path `evidence/...`.

| Fase | Folder | Halaman hasil | Ringkasan |
|---|---|---|---|
| 0 | [phase00](../../evidence/phase00/README.md) | [phase00](../results/phase00.md) | model acuan, ACVP, errata |
| 1 | [phase01](../../evidence/phase01/README.md) | [phase01](../results/phase01.md) | NTT satu lajur (C0) |
| 2 | [phase02](../../evidence/phase02/README.md) | [phase02](../results/phase02.md) | banking memori (C1) |
| 3 | [phase03](../../evidence/phase03/README.md) | [phase03](../results/phase03.md) | multi-lane, L = 8 |
| 4 | [phase04](../../evidence/phase04/README.md) | [phase04](../results/phase04.md) | pipeline P = 6 |
| 5 | [phase05](../../evidence/phase05/README.md) | [phase05](../results/phase05.md) | reducer Barrett |
| 5M | [phase05m](../../evidence/phase05m/README.md) | [phase05m](../results/phase05m.md) | memori dan jadwal, S6 sampai S9 |
| 6 | [phase06](../../evidence/phase06/README.md) | [phase06](../results/phase06.md) | sequencer K-PKE, S10 |
| 7 | [phase07](../../evidence/phase07/README.md) | [phase07](../results/phase07.md) | Keccak-f[1600] |
| 8 | [phase08](../../evidence/phase08/README.md) | [phase08](../results/phase08.md) | Keccak 2 ronde, sampler |
| 9 | [phase09](../../evidence/phase09/README.md) | [phase09](../results/phase09.md) | inti ML-KEM-768 penuh |
| 9M | [phase9m](../../evidence/phase9m/README.md) | [phase9m](../results/phase9m.md) | optimasi inti (K1 sampai K4) |
| Quartus | [quartus](../../evidence/quartus/) | | ekstrak laporan fase awal (C0 sampai C2) |

Fase 10 sampai 12 belum punya evidence.

Output Quartus penuh tidak ada di repository; lihat bagian *Quartus Outputs* di [README root](../../README.md).
Skrip `scripts/quartus/archive_quartus_outputs.py` memindahkan `output_files/` dan `db/` ke luar repository.
