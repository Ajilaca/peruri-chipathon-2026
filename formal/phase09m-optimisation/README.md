# formal/phase09m-optimisation/

Satu folder per langkah 9M.

| Folder | Blok |
|---|---|
| `9m1` | codec dua byte (`mlkem_pack2`, `mlkem_unpack2`) dan inti `W2` |
| `9m3` | hash sponge K0 |
| `9f1` | sequencer dengan sampler K0 |
| `9f1b` | `mlkem_core3`: keselamatan, BMC, cover |
| `9s2`, `9s2b` | inti NTT S10 dengan P = 6 dan alamat terregistrasi |
| `9i4` | `mlkem_core4`: keselamatan (E1, S1 sampai S7, B1 sampai B7), BMC P1, cover, kontrol negatif |

P1 dan NC-E1-4 (di `9i4`) serta NC-B7 (di `9f1b`) habis waktu (TIMEOUT) dan tidak dihitung lolos.
Hasil: [../../evidence/phase9m/](../../evidence/phase9m/README.md).
