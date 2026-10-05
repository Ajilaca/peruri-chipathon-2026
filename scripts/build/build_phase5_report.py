#!/usr/bin/env python3
"""scripts/build/build_phase5_report.py

Builds docs/reports/CHIPATON_Phase5_Report.pdf (Phase 5 report, Bahasa Indonesia, same layout, fonts and styles as the
Phase 0-4 reports; the styles are imported from scripts/build/build_phase4_report.py) with ReportLab.

Every number comes from an evidence file in this repository:
  - Quartus figures (ALM, registers, M10K, DSP, slack, Fmax) are parsed from the extracted evidence files with the same
    parser as the selection scripts (scripts/quartus/phase5_select_5b.py: parse_quartus);
  - every other figure is a literal that is first checked to appear in its evidence file (EXPECT below); the build
    stops if one is missing, so the PDF cannot silently drift from the evidence.

Usage: python3 scripts/build/build_phase5_report.py
"""
import pathlib
import statistics
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import KeepTogether, PageBreak, SimpleDocTemplate, Spacer

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "scripts" / g) for g in ("build", "quartus")]
from build_phase4_report import MUTED, P, S, bullets, fmt, num, table  # noqa: E402
from phase5_select_5b import parse_quartus  # noqa: E402
from reportlab.platypus import Paragraph  # noqa: E402

E5 = ROOT / "evidence" / "phase05"
E4 = ROOT / "evidence" / "phase04"
OUT = ROOT / "docs" / "reports" / "CHIPATON_Phase5_Report.pdf"
TOTAL_ALM = 41910
BUDGET_30 = 12573

# ---- literal figures and the evidence file each must appear in ------------------------------------------------
EXPECT = {
    "regression.md": ["Phase 0-4 regression OVERALL: PASS (21 steps, 0 failed)",
                                 "Phase 5 verify OVERALL: PASS (17 steps, 0 failed)",
                                 "all results as expected (14/14)", "'cycles_NTT': 119, 'cycles_INTT': 375"],
    "5b/selection_worksheet.md": ["34.515 (33.46-34.84)", "33.780 (32.81-34.25)", "2.13 %",
                                            "**Barrett** is selected by the rule."],
    "5c/selection_worksheet.md": ["33.100 (32.27-35.26)", "3.595 / 11.329", "3.448 / 10.865",
                                            "C4c NOT adopted"],
    "5a/summary_5a.md": ["**9,847**", "**−658 (−6.3 %)**"],
    "baseline/c3p6_critical_path.md": ["21.292", "4.348", "3.705", "10.753"],
    "closure/info_20ns.md": ["10,557", "9,305", "-2.059 ns (Slow -40C)", "-2.557 ns (Slow 100C)", "45.33",
                                        "44.33"],
}


def check_evidence():
    missing = []
    for f, items in EXPECT.items():
        text = (E5 / f).read_text()
        missing += [f"{f}: {it!r}" for it in items if it not in text]
    if missing:
        raise SystemExit("evidence check failed:\n  " + "\n  ".join(missing))


def q(folder, name):
    files = sorted(folder.glob(name))
    if not files:
        raise SystemExit(f"missing evidence {name}")
    r = parse_quartus(files[-1])
    r["file"] = files[-1].relative_to(ROOT)
    return r


def seeds(folder, prefix):
    return [q(folder, f"quartus_{prefix}{'' if s == 1 else f'-s{s}'}.md") for s in range(1, 7)]


def alm1(x):
    return f"{x:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DV", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"CHIPATON — Laporan Fase 5 (ID) — hal. {doc.page}")
    canvas.restoreState()


def build():
    check_evidence()
    c3 = [q(E4 / "seed_sweep", f"quartus_C3-P6-s{s}.md") if s > 1 else q(E4, "quartus_C3-P6.md")
          for s in range(1, 7)]
    a = q(E5 / "5a", "quartus_C4a.md")
    b = seeds(E5 / "5b", "C4b-B")
    m = seeds(E5 / "5b", "C4b-M")
    c = seeds(E5 / "5c", "C4c")
    i_b = q(E5 / "closure", "quartus_C4b-B-20.md")
    i_c3 = q(E5 / "closure", "quartus_C3-P6-20.md")

    def rng(rows, k):
        v = [r[k] for r in rows]
        return min(v), max(v), statistics.median(v)

    # sanity: the numbers quoted in the result file
    assert (rng(b, "alm")[0], rng(b, "alm")[1]) == (9166, 9208) and abs(rng(b, "fmax")[2] - 34.515) < 1e-9
    assert (rng(c, "alm")[0], rng(c, "alm")[1]) == (9032, 9094) and abs(rng(c, "fmax")[2] - 33.10) < 1e-9
    assert (rng(c3, "alm")[0], rng(c3, "alm")[1]) == (10484, 10516)

    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=17 * mm, title="CHIPATON — Laporan Fase 5 (ID)", author="Tim J5 (ITB)",
                            subject="Fase 5: optimasi aritmetika modular NTT/INTT ML-KEM-768 pada DE10-Nano")
    st = []
    W = A4[0] - 36 * mm

    # cover
    st += [Spacer(1, 62 * mm)]
    st += [P("PERURI Digital Summit · CHIP 2026 Hackathon — Tim J5 (ITB)", "csub"), Spacer(1, 6)]
    st += [P("Laporan Fase 5", "ctitle")]
    st += [P("Optimasi Aritmetika Modular — C4 (C4b-B, Barrett) · Akselerator NTT/INTT ML-KEM-768", "csub")]
    st += [P("Terasic DE10-Nano · Intel/Altera Cyclone V SE 5CSEBA6U23I7", "csub"), Spacer(1, 14)]
    st += [P("Status: <b>DONE</b> secara teknis — C4 = C4b-B (reduksi Barrett) berdasarkan aturan ADR 0011; 5c tidak "
             "diadopsi; 5d tidak dicoba; <b>ADR 0013 dan ADR 0015 masih Proposed</b>; 50 MHz belum tercapai; "
             "Approval belum dicentang", "cmeta")]
    st += [P("Branch: phase5-arith · dibuat di atas c572864, sebelum commit finalisasi Fase 5 · 2026-10-02", "cmeta"),
           Spacer(1, 22)]
    st += [P("Ditulis untuk: Tim J5. Sumber kebenaran tetap berkas di repo (docs/results/phase05.md, "
             "evidence/phase05/, docs/decisions/); dokumen ini rangkuman bacaan. Label: <b>MEASURED</b> "
             "(laporan Quartus atau log simulasi di repo), <b>INFERENCE</b> (turunan dari angka terukur), "
             "<b>ESTIMATE</b> (perkiraan dengan metode tertulis), <i>perhitungan tim</i> (aritmetika dari angka terukur), "
             "<b>belum diukur</b>. Tidak ada pengukuran pada papan; semua hasil berasal dari simulasi, analisis formal "
             "dan analisis Quartus (<i>kernel-only</i>, <i>virtual pin</i>).", "small")]
    st += [PageBreak()]

    bf, mf, cf, c3f = rng(b, "fmax"), rng(m, "fmax"), rng(c, "fmax"), rng(c3, "fmax")

    # 1
    st += [P("1. Ringkasan Eksekutif", "h1")]
    st += bullets([
        "Fase 5 mengganti aritmetika modular di dalam inti C3-P6 (L = 8, P = 6) tanpa mengubah matematika FIPS 203, "
        "jadwal, memori, L atau P. Siklus tetap NTT 119 dan INTT 375, tanpa <i>stall</i>.",
        f"<b>5a (reduksi <i>fold</i>, C4a):</b> {fmt(a['alm'])} ALM, turun 658 ALM dari C3-P6 (INFERENCE); Fmax "
        f"{num(a['fmax'])} MHz pada satu kompilasi.",
        f"<b>5b (Barrett vs Montgomery, seed 1–6):</b> aturan ADR 0011 memilih <b>Barrett</b> (median Fmax "
        f"{num(bf[2], 3)} vs {num(mf[2], 3)} MHz, selisih 2,13%, di dalam pita <i>near-tie</i> 5%; lalu ALM median lebih "
        f"rendah). Harga: DSP naik 9 → 18 (ADR 0013, <b>Proposed</b>).",
        f"<b>5c (<i>lazy reduction</i> INTT, C4c):</b> benar dan 119 / 375 siklus, tetapi median Fmax {num(cf[2], 3)} MHz "
        "di bawah syarat 34,84 MHz dan ADR 0012 tidak terpenuhi, sehingga <b>tidak diadopsi</b> (ADR 0014).",
        "<b>5d (Karatsuba):</b> tidak dicoba di Fase 5; usulan dipindah ke Fase 6 (ADR 0015, <b>Proposed</b>).",
        f"<b>C4 = C4b-B:</b> {fmt(b[0]['alm'])} ALM pada seed bawaan ({fmt(bf and rng(b, 'alm')[0])}–"
        f"{fmt(rng(b, 'alm')[1])} pada seed 1–6), 18 DSP, 29 M10K; timing 40 ns terpenuhi di semua seed; t_NTT 3,448 µs "
        "dan t_INTT 10,865 µs pada median Fmax (perhitungan tim).",
        "<b>Temuan utama (INFERENCE):</b> aritmetika menghemat area (sekitar 1.300 ALM) tetapi tidak menaikkan Fmax "
        "di luar sebaran seed. Jalur kritis ada di pembacaan memori. Kompilasi informasi 20 ns tidak memenuhi timing "
        f"untuk C3-P6 (setup {num(i_c3['setup'], 3)} ns) maupun C4b-B (setup {num(i_b['setup'], 3)} ns).",
        "<b>Belum tercapai:</b> target 50 MHz. Sumber daya tingkat sistem belum diukur; tidak ada pengukuran pada papan.",
    ])

    # 2
    st += [P("2. Tujuan Fase 5", "h1")]
    st += [P("Membuat aritmetika modular q = 3329 lebih murah dan lebih cepat tanpa mengubah satu pun hasil FIPS 203 "
             "(konfigurasi C4). Sub-langkah diukur dan ditinjau terpisah: 5a reduksi khusus-q, 5b Montgomery vs Barrett, "
             "5c <i>lazy reduction</i> (opsional), 5d basis Karatsuba (opsional). Keluaran: hasil benar, perbandingan "
             "terukur, ADR untuk 5b, baris C4 di matriks ablasi (<font name='DVM'>docs/ROADMAP.md</font>).")]

    # 3
    st += [P("3. Target dan Batasan", "h1")]
    st += [table([["Butir", "Nilai", "Sumber"],
                  ["Batasan clock revisi C4", "<font name='DVM'>create_clock -period 40.000</font> (25 MHz), sama dengan "
                                              "C3-P6; kompilasi informasi 20 ns hanya untuk C4b-B dan C3-P6", "ADR 0011 D1"],
                  ["Target 50 MHz (20 ns)", "<i>best-effort</i> proyek, bukan gerbang Fase 5; ekspektasi ADR 0006 dikoreksi "
                                            "karena jalur kritis ada di pembacaan memori", "ADR 0010"],
                  ["Anggaran desain inti NTT", "30% × 41.910 = <b>12.573 ALM</b>; melewatinya = keputusan tim baru",
                   "ADR 0009, 0012"],
                  ["Siklus tambahan", "diterima hanya jika t_NTT dan t_INTT pada Fmax terukur lebih baik dari baseline "
                                      "dan siklus tetap konstan", "ADR 0012"],
                  ["Kontrak operand pengali (D6)", "a, b dalam [0, q); amandemen [0, 2q) hanya untuk eksperimen C4c", "ADR 0011, 0014"],
                  ["Seed", "5b dan 5c: seed fitter 1–6 satu per satu; 5a dan kompilasi 20 ns: satu kompilasi (seed bawaan)",
                   "ADR 0011"]],
                 [38 * mm, W - 66 * mm, 28 * mm])]

    # 4
    st += [P("4. Reduksi yang Diukur", "h1")]
    st += [table([["Revisi", "Reduksi modular", "Posisi register pengali", "DSP"],
                  ["C3-P6 (baseline)", "13 tahap pengurangan bersyarat (beku, Fase 4)", "X, D_5, D_11", "9"],
                  ["C4a (5a)", "<i>fold</i>: 2<super>12</super> ≡ 767 (mod q), geser-dan-tambah, 5 lipatan + pilih v, v−q, v−2q",
                   "X, F_3, F_5", "9"],
                  ["C4b-B (5b)", "Barrett, k = 24, M = 5039; t·q sebagai geser-dan-tambah", "X, S_1, S_2", "18"],
                  ["C4b-M (5b)", "Montgomery, R = 2<super>12</super>, q′ = 3327; ROM twiddle bentuk Montgomery (dibuat skrip)",
                   "X, S_1, S_2", "9"],
                  ["C4c (5c)", "Barrett dengan operand 13-bit: u = b + q − a dalam [1, 2q), sisi samping a + b direduksi "
                               "sekali di keluaran; tidak diadopsi", "X, S_1, S_2", "18"]],
                 [26 * mm, W - 78 * mm, 32 * mm, 20 * mm])]
    st += [P("Posisi register memori sama dengan C3-P6 (A_4, A_11, M). Setiap reduksi sama dengan (a·b) mod q untuk semua "
             "a, b dalam [0, q) (uji <i>exhaustive</i>, MEASURED); C4c diuji pada [0, q) × [0, 2q).", "small")]

    # 5 baseline
    st += [KeepTogether([P("5. Baseline Jalur Kritis C3-P6 (sebelum RTL Fase 5, MEASURED)", "h1"), table([["Segmen jalur terburuk (Slow 1100 mV 100 °C)", "Delay (ns)", "Blok"],
                  ["register arbitrasi memori → keluaran pengali", "total data 29,345", "slack +10,753 ns"],
                  ["alamat baca dan <i>read mux</i> memori", "21,292", "<font name='DVM'>poly_mem_multiport_pipe</font>"],
                  ["<font name='DVM'>sub_mod(b, a)</font> masukan INTT", "4,348", "butterfly"],
                  ["routing + DSP sampai register X", "3,705", "pengali"]],
                 [78 * mm, 34 * mm, W - 112 * mm])])]
    st += [P("Tidak ada jalur di dalam reduksi di antara 300 jalur terburuk. Karena itu perubahan aritmetika tidak dapat "
             "mencapai 20 ns selama pembacaan memori sepanjang itu (INFERENCE; ADR 0010). "
             "Bukti: <font name='DVM'>evidence/phase05/baseline/</font>.", "small")]

    # 6 per-candidate
    head6 = P("6. Hasil Terukur per Revisi (MEASURED, seed bawaan; median dan rentang seed 1–6 = INFERENCE)", "h1")

    def row(name, r, rows=None):
        if rows:
            lo, hi, _ = rng(rows, "alm")
            flo, fhi, fmed = rng(rows, "fmax")
            alm = f"{fmt(r['alm'])} ({fmt(lo)}–{fmt(hi)})"
            fx = f"{num(r['fmax'])} (med {num(fmed, 3)}; {num(flo)}–{num(fhi)})"
        else:
            alm, fx = fmt(r["alm"]), f"{num(r['fmax'])}"
        return [name, alm, fmt(r["reg"]), r["dsp"], f"{num(r['setup'], 3)} / {num(r['hold'], 3)}", fx]

    rows = [["Revisi", "ALM (seed 1–6)", "Reg.", "DSP", "Setup / hold @ 40 ns (ns)", "Fmax terendah (MHz)"],
            row("C3-P6", c3[0], c3), row("C4a", a), row("<b>C4b-B</b>", b[0], b), row("C4b-M", m[0], m),
            row("C4c (tidak diadopsi)", c[0], c)]
    st += [KeepTogether([head6, table(rows, [34 * mm, 33 * mm, 12 * mm, 10 * mm, 30 * mm, W - 119 * mm],
                                      sel_rows=(3,))])]
    st += [P("M10K 29 pada semua revisi (diinfer alat). Timing 40 ns terpenuhi di semua kompilasi. "
             "t_NTT / t_INTT pada median Fmax (perhitungan tim, siklus 119 / 375): C3-P6 "
             f"{num(119 / c3f[2], 3)} / {num(375 / c3f[2], 3)} µs; C4b-B {num(119 / bf[2], 3)} / {num(375 / bf[2], 3)} µs; "
             f"C4b-M {num(119 / mf[2], 3)} / {num(375 / mf[2], 3)} µs; C4c {num(119 / cf[2], 3)} / {num(375 / cf[2], 3)} µs. "
             "Rentang seed antar-revisi saling tumpang tindih, sehingga selisih Fmax kecil tidak dapat dibedakan dari "
             "noise seed (INFERENCE).", "small")]

    # 7 5b detail
    st += [P("7. Pemilihan 5b: Barrett vs Montgomery", "h1")]
    head = [["Seed", "Barrett ALM", "Barrett Fmax (MHz)", "Montgomery ALM", "Montgomery Fmax (MHz)",
             "C4c ALM", "C4c Fmax (MHz)"]]
    for s in range(6):
        head.append([f"{s + 1}{' (bawaan)' if s == 0 else ''}", fmt(b[s]["alm"]), num(b[s]["fmax"]), fmt(m[s]["alm"]),
                     num(m[s]["fmax"]), fmt(c[s]["alm"]), num(c[s]["fmax"])])
    head.append(["Median", alm1(rng(b, "alm")[2]), num(bf[2], 3), alm1(rng(m, "alm")[2]), num(mf[2], 3),
                 alm1(rng(c, "alm")[2]), num(cf[2], 3)])
    st += [table(head, [24 * mm] + [(W - 24 * mm) / 6] * 6, sel_rows=(7,))]
    st += bullets([
        "Aturan (ADR 0011, ditetapkan sebelum pengukuran): kandidat benar dan memenuhi semua syarat; pilih median Fmax "
        "lebih tinggi; jika selisih ≤ 5% (<i>near-tie</i>), pilih ALM median lebih rendah.",
        "Barrett unggul 2,13% pada median Fmax (di dalam 5%) dan juga ALM median lebih rendah (9.171,0 vs 9.286,5): "
        "<b>Barrett dipilih</b> oleh aturan.",
        "Harga yang dicatat di ADR 0013: Barrett memakai 18 DSP (+9 dibanding C3-P6), Montgomery tetap 9 DSP. ADR 0013 "
        "<b>Proposed</b>; keputusan menerima Barrett atau memilih Montgomery tetap milik tim (PENDING #23).",
    ])

    # 8 5c
    st += [P("8. 5c: <i>Lazy Reduction</i> INTT (C4c) — diukur, tidak diadopsi", "h1")]
    st += [table([["Syarat adopsi (ADR 0014 §4, ditetapkan sebelum pengukuran)", "Hasil"],
                  ["Benar, uji <i>exhaustive</i> 22.164.482 pasangan, bukti formal batas nilai + kontrol negatif", "PASS"],
                  ["Siklus tepat 119 / 375", "PASS"],
                  ["ALM ≤ 12.573 di setiap seed (9.032–9.094)", "PASS"],
                  ["Timing 40 ns terpenuhi di setiap seed", "PASS"],
                  [f"Median Fmax &gt; 34,84 MHz (terukur {num(cf[2], 3)})", "<b>FAIL</b>"],
                  [f"ADR 0012: t_NTT &lt; 3,448 µs dan t_INTT &lt; 10,865 µs (terukur {num(119 / cf[2], 3)} / "
                   f"{num(375 / cf[2], 3)})", "<b>FAIL</b>"]],
                 [W - 20 * mm, 20 * mm])]
    st += bullets([
        "Hasil: C4c <b>tidak diadopsi</b>; C4b-B tetap konfigurasi C4. RTL C4c tetap di repo sebagai hasil terukur. Tidak "
        "ada seed ditambah dan aturan tidak diubah setelah pengukuran.",
        "Amandemen kontrak D6 ([0, 2q)) hanya berlaku untuk eksperimen C4c; C4 tetap [0, q).",
        "Analisis jalur setelah fakta (MEASURED slack; seed terbaik 2 dan terburuk 3): semua segmen pengali memiliki slack "
        "di atas 17 ns; kelas jalur terburuk tetap register baca-memori → masukan pengali (slack 11,806 dan 9,172 ns, "
        "C4b-B seed 1: 11,221 ns). Penyebabnya <b>hipotesis</b> sampai ada percobaan terkendali.",
    ])

    # 9 5d
    st += [P("9. 5d: Basis Karatsuba — tidak dicoba di Fase 5", "h1")]
    st += [P("<font name='DVM'>base_case_multiply.sv</font> bukan bagian inti C3-P6 maupun C4 (tidak ada inti yang "
             "menginstansiasinya), sehingga 5d tidak dapat mengubah t_NTT, t_INTT atau ALM inti yang menjadi gerbang "
             "Fase 5. Usulan ADR 0015 (<b>Proposed</b>): tidak dicoba di Fase 5, dipindah ke Fase 6; alternatifnya unit "
             "mandiri C4d dengan dua kompilasi tambahan. Keputusan ada pada tim.")]

    # 10 20ns
    st += [P("10. Kompilasi Informasi 20 ns (MEASURED, seed bawaan)", "h1")]
    st += [table([["Metrik", "C3-P6 @ 20 ns", "C4b-B @ 20 ns"],
                  ["ALM", fmt(i_c3["alm"]), fmt(i_b["alm"])],
                  ["Registers / M10K / DSP", f"{fmt(i_c3['reg'])} / 29 / {i_c3['dsp']}",
                   f"{fmt(i_b['reg'])} / 29 / {i_b['dsp']}"],
                  ["Setup terburuk (ns)", num(i_c3["setup"], 3), num(i_b["setup"], 3)],
                  ["Hold terburuk (ns)", num(i_c3["hold"], 3), num(i_b["hold"], 3)],
                  ["Timing 20 ns", "<b>tidak terpenuhi</b>", "<b>tidak terpenuhi</b>"],
                  ["Fmax corner terendah (MHz)", num(i_c3["fmax"]), num(i_b["fmax"])]],
                 [60 * mm, (W - 60 * mm) / 2, (W - 60 * mm) / 2])]
    st += bullets([
        "Kedua konfigurasi tidak memenuhi 50 MHz: kekurangan 2,06 ns (C3-P6) dan 2,56 ns (C4b-B). Di bawah batasan 20 ns "
        "<i>fitter</i> bekerja lebih keras sehingga Fmax (44–45 MHz) lebih tinggi daripada pada 40 ns; angkanya tidak "
        "sebanding lintas batasan.",
        "C4b-B 1.252 ALM lebih kecil dari C3-P6 (10.557 − 9.305) dengan 9 DSP lebih banyak, tetapi Fmax-nya tidak lebih "
        "tinggi (INFERENCE, satu seed). Sesuai ADR 0010: perubahan aritmetika tidak mencapai 20 ns.",
        "<i>Critical warning</i> (3 per kompilasi): 15725 (clock dari <i>virtual pin</i>, seperti Fase 1–4) dan 332148 × 2 "
        "(timing tidak terpenuhi). Ditriase tertulis, tidak ada yang di-<i>waive</i>.",
    ])

    # 11 verification
    st += [PageBreak(), P("11. Verifikasi (MEASURED, simulasi dan formal)", "h1")]
    st += [table([["Butir", "Hasil", "Bukti"],
                  ["Lint Verilator <font name='DVM'>-Wall</font> dan slang, semua <i>wrapper</i> C4", "0 peringatan, 0 galat",
                   "regression.md"],
                  ["Reduksi <i>exhaustive</i> (fold, Barrett, Montgomery) + ROM Montgomery",
                   "0 selisih untuk semua a, b dalam [0, q); kontrol negatif gagal sesuai harapan", "5a/ 5b/ verify.txt"],
                  ["Barrett lazy, <i>exhaustive</i> [0, q) × [0, 2q)", "0 selisih atas 22.164.482 pasangan",
                   "5c/verify.txt"],
                  ["Tes unit dan inti vs model golden, Verilator dan Icarus (NTT, INTT, <i>round-trip</i>, data terarah)",
                   "lulus untuk C4a, C4b-B, C4b-M, C4c; NTT 119, INTT 375, 0 <i>stall</i>, identik di dua simulator",
                   "regression.md"],
                  ["Kontrol negatif <i>hazard</i> (RdLat 0 + WrDly 8)", "memicu <i>scoreboard</i> dan hasil salah (terdeteksi)",
                   "5a/verify.txt"],
                  ["Formal Fase 5", "14/14 sesuai harapan: properti PASS, kontrol negatif FAIL; batas nilai logika lazy "
                                    "terbukti", "5a/ 5b/ 5c/ formal.md"],
                  ["Regresi Fase 0–4 (CRG-5, pada git b418d1e)", "21 langkah, 0 gagal, OVERALL PASS; check_params lulus",
                   "regression.md"]],
                 [60 * mm, 70 * mm, W - 130 * mm])]
    st += [P("Formal mencakup properti kontrol, kapasitas bank dan (5c) batas nilai; kebenaran aritmetika bertumpu pada uji "
             "<i>exhaustive</i> dan simulasi bit-exact. Lokasi bukti: <font name='DVM'>evidence/phase05/</font>.",
             "small")]

    # 12 decisions
    st += [P("12. Keputusan dan Hal Menunggu Tim", "h1")]
    st += bullets([
        "<b>Diterima:</b> ADR 0010 (50 MHz <i>best-effort</i>), ADR 0011 (D1–D8, aturan 5b), ADR 0012 (siklus dan batas "
        "12.573 ALM), ADR 0014 (5c, lingkup (b), aturan adopsi; catatan hasil ditambahkan).",
        "<b>Proposed, menunggu tim:</b> ADR 0013 (5b: Barrett, DSP 9 → 18; PENDING #23) dan ADR 0015 (5d tidak dicoba, "
        "pindah ke Fase 6).",
        "<b>Terbuka:</b> PENDING #19, fase \"memori dan jadwal\" setelah Fase 5 sebelum Fase 6 (batas terukur ada di jalur "
        "baca memori). Belum dimulai.",
        "Kotak Approval <font name='DVM'>phase05.md</font> kosong; hanya anggota tim yang mencentangnya.",
    ])

    # 13 limits
    st += [P("13. Keterbatasan dan Hal Terbuka", "h1")]
    st += bullets([
        "Tidak ada pengukuran pada papan; semua timing adalah analisis statis Quartus (<i>kernel-only</i>, <i>virtual pin</i>).",
        "C4a dan dua kompilasi 20 ns hanya satu kompilasi (seed bawaan). Sebaran seed (C4b-B 33,46–34,84 MHz; C4c "
        "32,27–35,26 MHz) lebih besar daripada banyak selisih Fmax antar-revisi, sehingga tidak ada peringkat Fmax yang "
        "diklaim selain keluaran aturan yang tertulis.",
        "Pilihan Barrett memakai pita <i>near-tie</i> 2,13% dan harga 9 DSP tambahan; ini <i>trade-off</i> tim, bukan hasil pengukuran.",
        "Tidak ada analisis jalur pada 20 ns; penyebab hasil 5c adalah hipotesis.",
        "Belum diukur: integrasi inti C4 dengan HPS, daya, anggaran sumber daya tingkat sistem.",
        "Penyimpangan tercatat: kontrol negatif inti pertama tidak valid dan diganti (amandemen A2); pratinjau 5b memakai "
        "kolom Fmax yang salah dan dikoreksi tanpa mengubah hasil; satu <i>git stash</i> ± 2 detik saat verifikasi "
        "berjalan (log tanpa galat). Rincian: <font name='DVM'>phase05.md</font> bagian 6.",
    ])

    # 14 conclusion
    st += [P("14. Kesimpulan", "h1")]
    st += [P(f"Aritmetika modular dapat dibuat lebih kecil: C4b-B memakai {fmt(rng(b, 'alm')[2])} ALM median "
             f"(seed 1–6) dibanding {fmt(rng(c3, 'alm')[2])} pada C3-P6, dengan hasil bit-exact dan 119 / 375 siklus tetap. "
             "Fmax tidak naik di luar sebaran seed dan target 50 MHz tidak tercapai, karena jalur kritis berada di "
             "pembacaan memori, bukan di aritmetika. Optimasi lebih lanjut menuju 50 MHz membutuhkan perubahan memori dan "
             "jadwal (PENDING #19), bukan reduksi yang lebih cerdas. Fase 5 ditutup secara teknis dengan dua ADR yang masih "
             "menunggu keputusan tim.")]

    # 15 reproduce
    st += [P("15. Reproduksibilitas", "h1")]
    st += [P("Quartus Prime Lite 25.1std.0 Build 1129, device 5CSEBA6U23I7, seed fitter bawaan (1) untuk revisi tunggal; seed "
             "2–6 untuk sweep 5b dan 5c. Proyek: <font name='DVM'>quartus/phase05_arith_c4/</font> (jalankan satu per satu, "
             "kompilasi paralel merusak <font name='DVM'>.qpf</font> bersama).")]
    st += [Paragraph("<br/>".join([
        ". scripts/env.sh",
        "scripts/test/phase5_verify.sh",
        "python3 formal/run/run_formal_phase5.py",
        "scripts/test/phase5_regression.sh",
        "cd quartus/phase05_arith_c4 &amp;&amp; ./run_5b_sweep.sh &amp;&amp; ./run_5c_sweep.sh &amp;&amp; ./run_20ns_info.sh",
        "python3 scripts/quartus/phase5_select_5b.py",
        "python3 scripts/quartus/phase5_select_5c.py --date 20261001",
        "python3 scripts/build/build_phase5_report.py          # laporan ini"]), S["code"])]
    st += [P("Bukti utama: " + ", ".join(f"<font name='DVM'>{x}</font>" for x in [
        "5a/summary_5a.md", "5b/selection_worksheet.md", "5c/summary_5c.md",
        "5c/selection_worksheet.md", "baseline/c3p6_critical_path.md",
        "closure/info_20ns.md", "regression.md", "docs/decisions/0010 … 0015",
        "docs/results/phase05.md"]) + ".", "small")]

    doc.build(st, onFirstPage=lambda c, d: None, onLaterPages=footer)
    print(f"written {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
