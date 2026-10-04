#!/usr/bin/env python3
"""scripts/build_phase9m_report.py

Builds docs/report/CHIPATON_Phase9M_Report.pdf (Phase 9M report: optimisation of the ML-KEM-768 core, Bahasa Indonesia, same fonts and styles as scripts/build_phase4_report.py and the converter of
scripts/build_complete_report.py) with ReportLab. The text is the CONTENT string below; every number in it was copied from the result and evidence files of this repository when the report was written.
check_evidence() verifies that the files it cites exist and that the key claimed lines are still in them; nothing is computed here. Usage: python3 scripts/build_phase9m_report.py
"""
import pathlib
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, SimpleDocTemplate, Spacer

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_phase4_report import MUTED, P  # noqa: E402
from build_complete_report import flow  # noqa: E402

OUT = ROOT / "docs" / "report" / "CHIPATON_Phase9M_Report.pdf"
E9M = ROOT / "docs" / "evidence" / "phase09m-optimisation"
EXPECT = {
    ROOT / "docs" / "results" / "result_phase9m.md": ["Status: PARTIAL", "14,222.0 ALM"],
    E9M / "9i4" / "sim_2026-10-05.md": ["ACVP keyGen: 25 vectors equal", "[verilator] core: 6/6 PASS", "[icarus] core: 6/6 PASS"],
    E9M / "9i4" / "formal_2026-10-05.md": ["TIMEOUT", "NC-JOIN4"],
    E9M / "9i4" / "selection_worksheet_2026-10-05.md": ["76.665", "109.8 / 125.4 / 169.4"],
    E9M / "9s2b" / "selection_worksheet_2026-10-05.md": ["77.555", "NOT met as written"],
    E9M / "9s2" / "selection_worksheet_2026-10-04.md": ["74.125"],
    E9M / "9f1b" / "selection_worksheet_2026-10-04.md": ["73.855"],
    E9M / "9f1" / "selection_worksheet_2026-10-04.md": ["73.070"],
    E9M / "9m1" / "selection_worksheet_2026-10-04.md": ["17,654.0"],
    E9M / "9m3" / "selection_worksheet_2026-10-04.md": ["15,917.5"],
    E9M / "9f0" / "selection_worksheet_2026-10-04.md": ["75.31"],
}


def check_evidence():
    missing = []
    for f, items in EXPECT.items():
        if not f.exists():
            missing.append(f"{f.relative_to(ROOT)}: file missing")
            continue
        t = f.read_text()
        missing += [f"{f.relative_to(ROOT)}: {it!r}" for it in items if it not in t]
    if missing:
        raise SystemExit("evidence check failed:\n  " + "\n  ".join(missing))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DV", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"CHIPATON \u2014 Laporan Fase 9M (ID) \u2014 hal. {doc.page}")
    canvas.restoreState()


def build():
    check_evidence()
    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=17 * mm,
                            title="CHIPATON \u2014 Laporan Fase 9M (ID)", author="Tim J5 (ITB)",
                            subject="Fase 9M: optimasi inti ML-KEM-768 (siklus, area, Fmax) pada DE10-Nano")
    W = A4[0] - 36 * mm
    st = [Spacer(1, 58 * mm), P("PERURI Digital Summit \u00b7 CHIP 2026 Hackathon \u2014 Tim J5 (ITB)", "csub"), Spacer(1, 6),
          P("Laporan Fase 9M", "ctitle"), P("Optimasi inti ML-KEM-768: siklus, area, Fmax", "csub"),
          P("Terasic DE10-Nano \u00b7 Intel/Altera Cyclone V SE 5CSEBA6U23I7", "csub"), Spacer(1, 14),
          P("Status: sembilan langkah selesai diukur (simulasi, formal, Quartus <i>kernel-only</i>); ACVP 100 % di dua simulator; tiga bukti formal berbatas habis waktu; ADR 0035-0043 Proposed; kotak Approval kosong", "cmeta"),
          P("Branch: phase9m-optimisation \u00b7 2026-10-04/05 \u00b7 Batch 1 di-commit, Batch 2 belum", "cmeta"), Spacer(1, 22),
          P("<b>Ditulis untuk: Tim J5.</b> Berkas di repo tetap sumber kebenaran (docs/results/result_phase9m.md, docs/evidence/phase09m-optimisation/). Label: <b>MEASURED</b> (laporan Quartus atau log simulasi di repo), "
            "<b>INFERENCE</b>, <b>ESTIMATE</b>, <i>perhitungan tim</i>. Tidak ada pengukuran pada papan; semua hasil berasal dari simulasi, analisis formal, dan analisis Quartus (<i>kernel-only</i>, <i>virtual pin</i>). "
            "Dokumen ini bukan teks proposal.", "small"), PageBreak()]
    st += flow(CONTENT, W)
    doc.build(st, onFirstPage=lambda c, d: None, onLaterPages=footer)
    print("written", OUT.relative_to(ROOT))


CONTENT = r"""
## 1. Ringkasan eksekutif
- Inti Fase 9 (`mlkem_core`, 17.620,5 ALM, 9.095 / 10.735 / 16.667 siklus untuk KeyGen / Encaps / Decaps) menjadi **K4 (`mlkem_core4`): 14.222,0 ALM pada 40 ns (−19 %) dan 8.416 / 9.611 / 12.989 siklus (−7,5 % / −10,5 % / −22,1 %)**. Timing 15,000 ns terpenuhi di 6 dari 6 seed (median Fmax 76,665 MHz, lowest slow corner). Latensi pada 15 ns: **109,8 / 125,4 / 169,4 µs**.
- ACVP 100 % di dua simulator (keyGen 25, encapsulation 25, decapsulation 10). Siklus Encaps dan Decaps identik untuk semua masukan yang diuji (bukti invarian siklus, bukan ketahanan side-channel).
- Sembilan langkah dikerjakan, masing-masing dengan rencana uji dan aturan adopsi yang ditulis sebelum pengukuran: 9M-1, 9M-2, 9M-3, S0, S1, S1b (Batch 1), S2, S2b, item 4 (Batch 2). Item 5 (sampler kedua) sengaja tidak dibangun.
- **Hasil jujur:** S2 netral (+0,27 MHz, di dalam derau seed); S2b menaikkan median 3,43 MHz tetapi **tidak lolos aturannya seperti tertulis**; item 4 lolos aturannya dan memberi penghematan terbesar di Encaps dan Decaps. K4 berdiri di atas K3, jadi keputusan rantai ADR 0038 → 0043 ada di tangan tim.
- **Batas bukti:** tiga bukti formal berbatas (P1 dan NC-E1-4 pada core4, NC-B7 pada core3) habis waktu dan tidak punya hasil formal; semuanya dicatat sebagai TIMEOUT.

## 2. Mengapa ada Fase 9M
Profil siklus inti Fase 9 (simulasi) menunjukkan: mesin K-PKE 65–72 % dari siklus, pemuatan polinomial ke mesin 0–23 %, penyimpanan 9–26 %, hash dan pembanding sekitar 3 %. Pemuatan dan penyimpanan dibatasi jalur satu byte per siklus pada codec, bukan oleh port mesin. ADR 0034 (Accepted, Faza Dzil, 2026-10-04) memilih item 1–4; item 5 disimpan sebagai ide. ADR 0036 menambah rencana Fmax (S0–S2) dan ADR 0039 menetapkan **15 ns sebagai batas pelaporan Fmax** (14 ns disimpan untuk nanti; gerbang 40 ns tetap).

## 3. Langkah-langkah dan hasilnya
Median enam seed, kernel-only, virtual pin. Denominator fitter: 41.910 ALM, 553 blok RAM, 112 DSP. Blok RAM 53–54 dan DSP 28 di semua konfigurasi.

| Langkah | Perubahan | Parameter | ALM 40 ns | Fmax 15 ns (MHz) | Siklus KeyGen / Encaps / Decaps | Latensi 15 ns (µs) | Aturan |
|---|---|---|---|---|---|---|---|
| Inti Fase 9 | dasar (C7-core) | — | 17.620,5 | tidak diukur (20 ns: 63,645) | 9.095 / 10.735 / 16.667 | (20 ns: 142,9 / 168,7 / 261,9) | — |
| 9M-1 (MW) | dua byte per siklus di jalur codec | `CODEC_W2 = 1` | 17.654,0 | 73,635 (2 seed) | 8.327 / 10.159 / 15.515 | 113,6 / 138,5 / 211,6 | lolos |
| 9M-2 | inti pada 20 ns, enam seed | tanpa RTL baru | — | (20 ns: 63,990, terpenuhi 6/6) | — | — | lolos |
| 9M-3 (MK) | sponge hash K0 | `HASH_C5 = 0` | 15.917,5 | tidak diukur | 8.447 / 10.279 / 15.635 | — | lolos |
| S0 | mencari batas Fmax inti MW | sweep 16 → 13 ns | — | batas antara 13 dan 14 ns | — | — | — |
| S1 (K1) | sampler K0 + hash K0 | `SMP_C5 = 0` | 14.061,0 | 73,070 | 8.795 / 10.627 / 15.983 | 120,4 / 145,4 / 218,7 | lolos; lebih kecil, bukan lebih cepat |
| S1b (K1b) | hash di sidecar latar belakang | `mlkem_core3` | 14.335,0 | 73,855 | 8.404 / 10.236 / 15.597 | 113,8 / 138,6 / 211,2 | lolos |
| S2 (K2) | register setelah reducer Barrett (P = 5 → 6) | `NTT_P6 = 1` | 14.213,0 | 74,125 | 8.416 / 10.250 / 15.619 | 113,5 / 138,3 / 210,7 | lolos, tetapi netral |
| S2b (K3) | alamat issue NTT dihitung lebih awal dan diregistrasi | `NTT_AR = 1` | 14.115,5 | 77,555 | 8.416 / 10.250 / 15.619 | 108,5 / 132,2 / 201,4 | **tidak lolos seperti tertulis** (butir 5) |
| **Item 4 (K4)** | pemuatan polinomial di belakang mesin K-PKE | `mlkem_core4` | **14.222,0** | **76,665** | **8.416 / 9.611 / 12.989** | **109,8 / 125,4 / 169,4** | lolos |

### 3.1 Item 1 (9M-1): jalur codec dua byte per siklus
Beban satu polinomial d = 12 turun dari 391 ke 263 siklus; penyimpanan 393 → 265. Siklus KeyGen / Encaps / Decaps turun 8,4 % / 5,4 % / 6,9 % tanpa perubahan aritmetika. Pada d = 1 dan 4 tidak ada perubahan (dibatasi port mesin, 1 koefisien per siklus). Biaya: +33,5 ALM (derau).

### 3.2 Item 2 (9M-2) dan S0: seberapa cepat inti bisa berjalan
Inti memenuhi 20,000 ns di 6 dari 6 seed untuk kedua inti (Fase 9 dan 9M-1). Sweep S0 (2 seed, bawaan Quartus) memenuhi 16, 15, 14 ns di kedua seed; pada 13 ns satu dari dua seed terpenuhi. Batas inti MW ada di antara 13 dan 14 ns. Upaya performa tinggi pada 14 ns tidak membantu (lebih banyak ALM dan register, slack lebih buruk). Dari sini 15 ns dipilih sebagai batas pelaporan.

### 3.3 Item 3 (9M-3) dan S1: mengecilkan Keccak
Sponge K0 (satu ronde per siklus) menggantikan sponge C5 (dua ronde per siklus) pada instans hash: −1.736,5 ALM (−9,8 %) dengan +120 siklus per operasi. Sampler K0 pada mesin (S1) menghemat 3.593 ALM total terhadap MW (−20,4 %) dengan +468 siklus. Pada 15 ns K1 sedikit lebih lambat daripada MW pada batas yang sama (3–6 %): K1 lebih kecil, bukan lebih cepat.

### 3.4 S1b: hash di latar belakang
Tiga hash independen (H(ek) di KeyGen dan Encaps, J di Decaps) berjalan di sidecar saat pengendali memuat atau menyimpan. Siklus turun 391 / 391 / 386 terhadap K1 dengan +274 ALM. Sidecar tidak pernah menunda pengendali utama.

### 3.5 S2 dan S2b: Fmax
S2 menambah satu register di akhir reducer Barrett (`MUL_REG` bit 3; 119 siklus per transformasi). Jalur reducer ke memori naik dari +1,170 ke +2,349 ns slack, **tetapi dinding berikutnya ternyata jalur penghitung layer ke alamat memori** yang sudah ada di K1b, sehingga median Fmax naik hanya 0,27 MHz. Perkiraan rencana (76–80 MHz) meleset.
S2b menghitung alamat issue satu siklus lebih awal dan meregistrasikannya (128 register). Kelas `layer_q` ke memori hilang dari 300 jalur terburuk. Median 77,555 MHz lawan 74,125 MHz (+3,43 MHz), lima dari enam seed K3 di atas semua seed K2. Aturan butir 5 (gain lebih besar dari spread seed K3 6,35 MHz atau seed terendah K3 di atas seed tertinggi K2) **tidak terpenuhi seperti tertulis** (seed 4: 73,02 MHz). Tiga seed tambahan (amandemen A2, dipilih setelah hasil dan dilaporkan di samping) memberi median sembilan seed 77,320 MHz. Ekor seed rendah ditelusuri kemudian pada laporan jalur K4: suku `start_go` pada logika S2b membuat alamat terregistrasi bergantung pada `host_we_i` yang dikendalikan sequencer dari `cnt_q != 0` (INFERENCE untuk K3 sendiri).

### 3.6 Item 4: pemuatan di belakang mesin
Pengendali menjalankan program mesin (`RUNS`), memuat polinomial lain di belakangnya, lalu bergabung (`RUNJ`). Varian mesin `kpke_sched_smp4` memberi port tulis host saat berjalan (prioritas terendah); interlock per slot menahan operasi mesin yang memakai slot yang belum dimuat; pemuat `mlkem_ldpoly2o` memakai backpressure. Penyimpanan tetap berderet dan KeyGen tidak diubah. Hasil: Encaps −639 (−6,2 %) dan Decaps −2.630 (−16,8 %) siklus; biaya sekitar +190 ALM (+1,3 %) dan beberapa puluh register; Fmax −0,89 MHz (di dalam spread). Jalur terburuk seed terlemah (69,43 MHz) adalah jalur S2b, bukan item 4.

## 4. Pengujian dan verifikasi (K4)
| Pengujian | Hasil |
|---|---|
| ACVP (keyGen 25, encapsulation 25, decapsulation 10), 20 kasus acak, rantai, protokol, siklus konstan | 6/6 di Verilator dan 6/6 di Icarus (simulasi) |
| Kontrol negatif (`nclen`, `ncoff`, `ncrom`, `ncprio`, `ncwr`, `ncjob`, `ncilk`, `ncgrant`, `ncjoin`) | gagal sesuai syarat |
| Port host yang di-throttle (`ncthr`, `ncthrld`) dengan interlock utuh | lolos seluruh target |
| Lint | Verilator `-Wall` 0 peringatan; slang 0 error, 0 peringatan |
| ROM pengendali | sama dengan hasil generator; pemeriksaan statis lolos |
| Formal (protokol stub) | E1 non-interference, S1–S7, B1–B7: PASS (induksi); cover PASS; NC-JOIN4 gagal sesuai syarat; **P1 dan NC-E1-4: TIMEOUT** |
| Quartus | 12 kompilasi K4, semua rc=0; terpenuhi 6/6 di 40 ns dan 6/6 di 15 ns |

Dua kontrol dibangun salah pada percobaan pertama (`ncthrld`: pencacah throttle berjalan bebas; `ncgrant`: mutasi pada gerbang yang sudah diterapkan pemuat). Keduanya perbaikan kontrol, bukan desain, lalu dijalankan ulang.

## 5. Apa yang tidak ditunjukkan (batas)
- Tidak ada hasil papan, tidak ada hasil HPS, tidak ada klaim kecepatan terhadap perangkat lunak, daya, atau ketahanan side-channel. Konstan-waktu berarti invarian jumlah siklus saja.
- Derau seed 3 MHz (awal) sampai 11 MHz (spread K4): selisih di bawah itu tidak disebut gain.
- P1 dan NC-E1-4 (core4) serta NC-B7 (core3) tidak punya hasil formal; P1 bertumpu pada simulasi dan kontrol NC-JOIN4. P2 dibuang karena gagal induksi tanpa invarian posisi program, dan tidak diklaim terbukti.
- Model formal memakai stub protokol untuk engine, sampler, dan sponge; ia membuktikan sifat kontrol dan rentang, bukan nilai.
- Item 5 (sampler kedua, ESTIMATE 1–4 % latensi untuk sekitar +3.500 ALM) tidak dibangun.

## 6. Kesalahan dan temuan proses (dicatat apa adanya)
1. VS Code crash mematikan dua kompilasi Quartus paralel dan satu proses formal; sejak itu kompilasi berjalan satu per satu dengan sisa RAM minimal 2 GB.
2. Satu pertanyaan status disalahartikan dan antrean kompilasi dihentikan, lalu dipulihkan; tercatat di amandemen A1 rencana S2b.
3. Banyak estimasi rencana meleset dan tercatat di hasil masing-masing: S2 siklus +12 / +14 / +22 (bukan +6 / +7 / +11), Fmax S2 74,1 MHz (bukan 76–80), ALM S2 −122 (bukan +0..+250).
4. Rencana item 4 ditulis setelah RTL dan simulasi pertama (rencana menyatakannya); aturan ditulis sebelum kompilasi Quartus dan sebelum kontrol.
5. Tiga seed tambahan S2b dipilih setelah hasil enam seed; dilaporkan di samping, tidak ada seed yang dibuang.

## 7. Keputusan yang menunggu tim
PENDING #34–#40 (ADR 0035, 0037, 0038, 0040, 0041, 0042, 0043; semuanya Proposed). Rantai bersarang: K4 memerlukan K3, K3 memerlukan K2, K2 memerlukan K1b. Tim dapat berhenti di tautan mana pun, tetapi pengukuran berikutnya harus diulang pada dasar yang baru. Kotak Approval `result_phase9m.md` kosong dan hanya dicentang anggota tim.

## 8. Berkas
`docs/results/result_phase9m.md`; `docs/evidence/phase09m-optimisation/{9m1,9m2,9m3,9f0,9f1,9f1b,9s2,9s2b,9i4}/` (rencana, hasil, worksheet, simulasi, formal, ekstrak Quartus); `quartus/phase09*_core/`; `formal/run_formal_phase9*.py`; `docs/decisions/0034 .. 0043`.

"""

if __name__ == "__main__":
    build()
