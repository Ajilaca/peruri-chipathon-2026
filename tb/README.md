# tb/

Testbench cocotb dan model acuan Python. Tiap test membandingkan RTL bit-exact dengan [`golden/`](golden/README.md)
dan dijalankan di Verilator dan Icarus. Kasus sudut ditulis di test plan fase (`evidence/phaseNN/test_plan*.md`) sebelum test dibuat.

| Folder | Menguji | Driver |
|---|---|---|
| [golden/](golden/README.md) | model acuan ML-KEM-768, model sampler, codec, FO, sequencer; uji model sendiri di `golden/tests/` | `pytest tb/golden`, `run_kat.py` |
| `vectors/acvp/` | vektor ACVP (keyGen, encapsulation/decapsulation) | diambil oleh `golden/fetch_acvp_vectors.py` |
| `ntt/` | butterfly, modmul, inti NTT C1 sampai C3, memori pipeline; uji menyeluruh di `k1_exhaustive/`, `p4_reducer/` | `run_ntt_tests.py`, `run_ntt_c2_tests.py`, `run_ntt_c3_tests.py` |
| `mem/` | peta bank dan inti C1 | `run_mem_tests.py` |
| [arith/](arith/README.md) | reducer Barrett, fold, Montgomery, lazy; inti C4 | `run_c4_unit_tests.py`, `run_c4_core_tests.py` |
| `phase5m/` | M6, S7, S8, `half_mod` | `run_m6_tests.py`, `run_s7_tests.py`, `run_s8_tests.py` |
| `s10/` | inti S10 dan memori M10K | `run_s10_tests.py` |
| `keccak/` | Keccak-f[1600] dan sponge terhadap `hashlib` | `run_keccak_tests.py` |
| `sample/` | CBD2, SampleNTT, wrapper sampler | `run_sample_tests.py` |
| `sched/`, `smp/` | sequencer K-PKE, unit PWM, sequencer dengan sampler | `run_sched_tests.py`, `run_smp_tests.py` |
| `mlkem/` | codec, hash, FO compare, inti `mlkem_core*` dengan ACVP | `run_codec_tests.py`, `run_hashfo_tests.py`, `run_core_tests.py` |

## Hubungan antar lapisan

1. **Unit test** menguji satu modul terhadap fungsi di `golden/primitives.py` (reducer, butterfly, sponge, pack).
2. **Core test** menjalankan inti penuh (NTT, K-PKE, ML-KEM) terhadap model acuan dan ACVP, dan mencatat siklus per operasi.
3. **Formal** ([../formal/](../formal/README.md)) membuktikan properti kendali yang tidak bisa dicakup test: tidak ada alamat di luar rentang, FSM selesai, interlock.
4. **Regresi** ([../scripts/test/](../scripts/README.md)) menjalankan ulang semua fase sebelumnya; skrip `phaseN_verify.sh` memanggil ketiganya untuk satu fase.

Test dijalankan lewat driver `run_*.py` (membuat `sim_build_*` sementara) atau lewat `pytest`.
Folder `sim_build_*`, `__pycache__` dan `results.xml` adalah keluaran, bukan sumber.
