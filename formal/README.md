# formal/

File SymbiYosys (`.sby`), modul properti dan top formal. Dibaca oleh Yosys dengan plugin slang, solver boolector.
Hasil run ada di `evidence/phaseNN/**/formal*.md`.

| Folder | Blok | Properti |
|---|---|---|
| `phase01-ntt` | inti NTT C0 | FSM mencapai done, alamat dalam rentang |
| `phase02-mem` | peta bank, inti C1 | bebas konflik bank, keselamatan |
| [phase03-multilane](phase03-multilane/README.md) | inti C2 (L = 1 sampai 8, K2, K1) | keselamatan per L, ekuivalensi butterfly K1 dengan kontrol negatif |
| `phase04-pipeline` | C3 P = 2, 4, 6 | keselamatan dengan pipeline |
| `phase05-arith` | C4a, C4b, C4c, batas lazy | keselamatan, batas rentang butterfly lazy |
| `phase05m-memsched` | M6, S7, S8 | keselamatan |
| `phase06-scheduling`, `s10/` | sequencer K-PKE, inti S10 | keselamatan, urutan program |
| `phase07-keccak` | sponge K0 | K1 sampai K5 (panjang, padding, handshake) |
| [phase08-keccak-stream](phase08-keccak-stream/README.md) | sponge 2 ronde, sampler, sequencer dengan sampler | keselamatan W1 dan W2 |
| [phase09-integration](phase09-integration/README.md) | codec, hash, FO compare, inti `mlkem_core` | keselamatan, cover, cover dalam |
| [phase09m-optimisation](phase09m-optimisation/README.md) | varian 9M, `core3`, `core4` | keselamatan, BMC berbatas, cover, kontrol negatif |
| [run/](run/README.md) | driver Python `run_formal_*.py` | menjalankan semua `.sby` satu fase dan memeriksa hasil yang diharapkan |
| `work/` | keluaran sementara run (diabaikan Git) | |

## Yang dibuktikan dan yang tidak

Properti dibuktikan dengan induksi atau BMC berbatas, seperti yang tertulis di tiap `.sby`. Ini bukan bukti kebenaran penuh inti.
Blok sekitar (sponge, engine) diganti stub protokol pada bukti inti. Properti penting punya kontrol negatif yang harus gagal; tidak semua properti punya satu.
Run yang habis waktu dicatat TIMEOUT dan tidak dihitung lolos (P1 dan NC-E1-4 di `core4`, NC-B7 di `core3`).
Hubungan dengan test dan regresi: [../tb/README.md](../tb/README.md).
