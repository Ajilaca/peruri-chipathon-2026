# Cover dalam Fase 9c (kedalaman 480), 2026-10-04

MEASURED dengan SymbiYosys (yosys-slang, boolector), `formal/phase09-integration/9c/mlkem_core_cover_deep.sby` (mode cover, kedalaman 480, `-D DEEP`), dijalankan manual di salinan direktori kerja; lima pernyataan cover yang sama dari `mlkem_core_formal_top.sv` seperti run kedalaman 260 ditambah dua yang memerlukan program terpanjang. Hasil: SELESAI (PASS, rc=0): kelima state yang dicakup tercapai, jadi bukti keselamatan `formal.md` tidak vakum juga untuk program Decaps. Waktu berjalan 0:28:07 (1,687 s). Hanya kendali dan rentang; ini menunjukkan keterjangkauan dengan sub-blok diganti stub protokol yang selesai seketika, bukan timing inti nyata.

| Pernyataan cover | Langkah pertama tercapai |
|---|---|
| sebuah word digest diambil dari stub hash (state S_HGT, `hg_take`) | 18 |
| KeyGen done (`done_a_o` dengan op 0) | 233 |
| Encaps done (`done_a_o` dengan op 1) | 233 |
| state S_CMPK (pembandingan ciphertext hasil enkripsi ulang) | 266 |
| Decaps done (`done_a_o` dengan op 2) | 272 |

(INFERENCE: SymbiYosys mencetak posisi sumber build DEEP dengan offset, jadi tabel menetapkan lima pernyataan yang tercapai ke maknanya lewat panjang tiap pernyataan pada posisi yang tercetak (37 karakter: dua cover `done_a_o`, 35: word digest, 21: S_CMPK) dan urutan langkah; lima pernyataan berbeda yang semuanya tercapai adalah inti run ini.)

Baris ringkasan mentah run:

```
SBY  2:21:27 [out] summary: Elapsed clock time [H:MM:SS (secs)]: 0:28:07 (1687)
SBY  2:21:27 [out] summary: Elapsed process time [H:MM:SS (secs)]: 0:28:54 (1734)
SBY  2:21:27 [out] summary: engine_0 (smtbmc boolector) returned pass
SBY  2:21:27 [out] summary: cover trace: out/engine_0/trace0.vcd
SBY  2:21:27 [out] summary:   reached cover statement mlkem_core_formal_top._witness_.check_1285 at mlkem_core_formal_top.sv:154.7-154.42 step 18
SBY  2:21:27 [out] summary: cover trace: out/engine_0/trace1.vcd
SBY  2:21:27 [out] summary:   reached cover statement mlkem_core_formal_top._witness_.check_1270 at mlkem_core_formal_top.sv:150.7-150.44 step 233
SBY  2:21:27 [out] summary: cover trace: out/engine_0/trace2.vcd
SBY  2:21:27 [out] summary:   reached cover statement mlkem_core_formal_top._witness_.check_1274 at mlkem_core_formal_top.sv:151.7-151.44 step 233
SBY  2:21:27 [out] summary: cover trace: out/engine_0/trace3.vcd
SBY  2:21:27 [out] summary:   reached cover statement mlkem_core_formal_top._witness_.check_1282 at mlkem_core_formal_top.sv:153.7-153.28 step 266
SBY  2:21:27 [out] summary: cover trace: out/engine_0/trace4.vcd
SBY  2:21:27 [out] summary:   reached cover statement mlkem_core_formal_top._witness_.check_1278 at mlkem_core_formal_top.sv:152.7-152.44 step 272
```
