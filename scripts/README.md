# scripts/

Skrip dikelompokkan menurut fungsi. Jalankan dari root repository dengan Quartus dan OSS CAD Suite sudah ada di PATH dan `.venv` aktif.

## Verifikasi: [test/](test/)

| Skrip | Fungsi |
|---|---|
| `phase5_verify.sh`, `phase5m_verify*.sh`, `phase6_verify.sh`, `phase7_verify.sh`, `phase8a_verify.sh`, `phase8b_verify.sh`, `phase8cd_verify.sh`, `phase9a_verify.sh` ... `phase9c_verify.sh`, `s10_verify.sh` | satu fase penuh: lint, simulasi dua simulator, regresi, formal; baris akhir `OVERALL: PASS` hanya bila semua langkah lolos |
| `phase5_regression.sh`, `phase5m_final_regression.sh` | regresi fase-fase sebelumnya |
| `smoke/` | uji kecil simulator dan proyek Quartus (memeriksa lingkungan) |

## Quartus dan seleksi hasil: [quartus/](quartus/)

| Skrip | Fungsi |
|---|---|
| `select_*.py`, `phase4_select_p.py`, `phase5_select_5b.py`, `phase5_select_5c.py`, `phase5m_select_s*.py` | menerapkan aturan adopsi ke ekstrak Quartus enam seed dan menulis `selection_worksheet.md` |
| `archive_quartus_outputs.py` | memindahkan `output_files/` dan `db/` ke luar repository (tidak pernah di-commit) |
| `*.tcl` | laporan jalur kritis dan segmen untuk Timing Analyzer |
| `phase*_path_classes.py`, `classify_paths_9f.py`, `quartus_entity_breakdown.py`, `phase4_seed_sweep_summary.py` | analisis jalur dan rincian per entitas dari laporan yang sudah ada |

## Analisis (di `test/`)

`phase5_stall_cycles.py`, `phase7_op_cycles.py`, `phase8b_cycles.py`, `pipeline_hazard_slack.py`, `phase5m_s9_port_analysis.py`
menghitung stall, siklus per operasi, slack hazard dan konflik port dari log atau model; hasilnya ditulis ke `evidence/`.

## Utilitas (root `scripts/`)

| File | Fungsi |
|---|---|
| `requirements-dev.txt`, `tooling.env` | versi paket Python dan variabel perkakas |
