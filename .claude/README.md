# .claude/

- `skills/`: lima skill proyek. Tiap skill menjaga satu aturan yang mudah dilanggar saat kerja cepat.

| Skill | Dipakai saat | Alasan ada |
|---|---|---|
| `mlkem-guard` | pekerjaan NTT, Keccak, sampler, FO, KAT, atau ada usul mengubah matematika | matematika FIPS 203 dikunci (ADR 0002). `check_params.py` memeriksa `tb/golden/params.py` |
| `quartus-report` | butuh angka ALM, register, RAM, DSP, Fmax, slack | angka implementasi hanya dari Quartus. `extract_quartus_report.py` menulis ekstrak MEASURED ke `evidence/` |
| `phase-gate` | menanyakan fase selesai atau belum, sebelum fase baru | fase selesai bila bukti ada untuk tiap kriteria. `check_result.py` memeriksa `docs/results/phaseNN.md`; kotak Approval hanya diisi manusia |
| `decision-record` | tim memutuskan sesuatu atau ada pilihan terbuka | keputusan milik tim. `new_adr.py` membuat `docs/decisions/adr/ADR-NNNN-*.md` dan menolak *accepted* tanpa nama pemutus |
| `proposal-claims` | menulis atau mengubah teks untuk juri, README, laporan | mencegah klaim berlebihan (kebal kuantum, side-channel, percepatan tanpa bukti). `claim_lint.py` memeriksa teks |

Skill dipanggil dengan `/<nama>`. Isi tiap skill ada di `skills/<nama>/SKILL.md`, skrip di `skills/<nama>/scripts/`.
