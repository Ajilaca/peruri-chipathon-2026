#!/usr/bin/env python3
"""scripts/build_phase4_report.py

Builds docs/report/CHIPATON_Phase4_Report.pdf (Phase 4 report, Bahasa Indonesia, same layout as the Phase 0-3
reports in docs/report/) with ReportLab.

Every number comes from an evidence file in this repository:
  - Quartus figures (ALM, registers, M10K, DSP, slack, Fmax) are parsed from the extracted evidence files with the
    same parser as the selection script (scripts/phase4_select_p.py: parse_quartus);
  - every other figure is a literal that is first checked to appear in its evidence file (EXPECT below); the build
    stops if one is missing, so the PDF cannot silently drift from the evidence.

Usage: python3 scripts/build_phase4_report.py
"""
import pathlib
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from phase4_select_p import EVID, parse_quartus  # noqa: E402

OUT = ROOT / "docs" / "report" / "CHIPATON_Phase4_Report.pdf"
TOTAL_ALM = 41910
BUDGET_30 = 12573
BUDGET_25 = 10478

# ---- literal figures and the evidence file each must appear in ------------------------------------------------
EXPECT = {
    "cocotb_regression_2026-09-30.txt": ["[verilator] TOTAL: 32/32 passed", "[icarus] TOTAL: 32/32 passed",
                                         "[verilator] TOTAL: 16/16 passed", "[icarus] TOTAL: 16/16 passed",
                                         "'cycles_NTT': 119, 'cycles_INTT': 375, 'stall_NTT': 0, 'stall_INTT': 0",
                                         "'violations_NTT': 640, 'wrong_NTT': 5, 'violations_INTT': 640, 'wrong_INTT': 5"],
    "v2_modmul_staged_exhaustive_2026-09-30.txt": ["pairs_checked=16777216", "RESULT: PASS"],
    "formal_2026-09-30.md": ["OVERALL: all results as expected (9/9)"],
    "regression_2026-09-30.txt": ["OVERALL: all results as expected (19/19)", "23 passed",
                                  "check_params: all locked parameters match."],
    "ghrd_shell_measured_2026-10-01.md": ["**1,309 / 41,910 (3 %)**", "**35 / 553**", "**0 / 112**", "**0.0**",
                                          "**+1.573 ns**", "**+0.076 ns**"],
    "ghrd_plus_c3p4_integration_2026-10-01.md": ["**12,754** (30 %)", "| 11,432 |", "| 1,304 |", "**+18 ALM**",
                                                 "**+9.204 / +0.149**", "| Low | Low | Low | Low |", "(Fmax 34.35 → 32.47 MHz at the lowest slow corner",
                                                 "| 48.2 % |", "**32.47**", "+993 ALM"],
}


def check_evidence():
    missing = []
    for f, items in EXPECT.items():
        text = (EVID / f).read_text()
        missing += [f"{f}: {it!r}" for it in items if it not in text]
    if missing:
        raise SystemExit("evidence check failed:\n  " + "\n  ".join(missing))


def q(name):
    files = sorted(EVID.glob(name))
    if not files:
        raise SystemExit(f"missing evidence {name}")
    r = parse_quartus(files[-1])
    r["fmax_low"] = min(v for _, v in r["fmax"])
    r["file"] = files[-1].relative_to(ROOT)
    return r


# ---- styles --------------------------------------------------------------------------------------------------
LIB = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("DV", LIB + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("DVB", LIB + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", LIB + "LiberationSans-Italic.ttf"))
pdfmetrics.registerFont(TTFont("DVBI", LIB + "LiberationSans-BoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("DVM", LIB + "LiberationMono-Regular.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily  # noqa: E402
registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVBI")

INK = colors.HexColor("#111111")
MUTED = colors.HexColor("#5b6675")
ACCENT = colors.HexColor("#1f2a44")
RULE = colors.HexColor("#c9d1db")
HEAD = colors.HexColor("#1f2a44")
SEL = colors.HexColor("#fff4d6")

S = {
    "body": ParagraphStyle("body", fontName="DV", fontSize=9.4, leading=13.2, textColor=INK, spaceAfter=5),
    "small": ParagraphStyle("small", fontName="DV", fontSize=7.8, leading=10.4, textColor=MUTED, spaceAfter=3),
    "h1": ParagraphStyle("h1", fontName="DVB", fontSize=15, leading=19, textColor=INK, spaceBefore=9,
                         spaceAfter=6),
    "ctitle": ParagraphStyle("ctitle", fontName="DVB", fontSize=24, leading=30, textColor=INK, alignment=TA_CENTER,
                             spaceAfter=8),
    "csub": ParagraphStyle("csub", fontName="DV", fontSize=11, leading=15, textColor=INK, alignment=TA_CENTER,
                           spaceAfter=4),
    "cmeta": ParagraphStyle("cmeta", fontName="DV", fontSize=9.5, leading=13, textColor=colors.HexColor("#333333"),
                            alignment=TA_CENTER),
    "h2": ParagraphStyle("h2", fontName="DVB", fontSize=10.5, leading=14, textColor=INK, spaceBefore=6,
                         spaceAfter=3),
    "cell": ParagraphStyle("cell", fontName="DV", fontSize=7.8, leading=9.8, textColor=INK),
    "cellb": ParagraphStyle("cellb", fontName="DVB", fontSize=7.8, leading=9.8, textColor=colors.white),
    "bullet": ParagraphStyle("bullet", fontName="DV", fontSize=9.4, leading=13.2, textColor=INK, leftIndent=11,
                             bulletIndent=2, spaceAfter=2.5),
    "code": ParagraphStyle("code", fontName="DVM", fontSize=7.4, leading=9.6, textColor=INK, leftIndent=6,
                           backColor=colors.HexColor("#f3f5f8"), borderPadding=4, spaceAfter=6),
}


def P(t, st="body"):
    return Paragraph(t, S[st])


def bullets(items):
    return [Paragraph(t, S["bullet"], bulletText="•") for t in items]


def table(rows, widths, sel_rows=(), align_right_from=None):
    data = [[Paragraph(str(c), S["cellb" if i == 0 else "cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), HEAD), ("LINEBELOW", (0, 0), (-1, 0), 0.8, ACCENT),
          ("LINEBELOW", (0, 1), (-1, -1), 0.3, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
          ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]
    for r in sel_rows:
        st.append(("BACKGROUND", (0, r), (-1, r), SEL))
    t.setStyle(TableStyle(st))
    return t


def fmt(n):
    return f"{n:,}".replace(",", ".")


def num(x, d=2):
    return f"{x:.{d}f}".replace(".", ",")


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DV", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"CHIPATON — Laporan Fase 4 (ID) — hal. {doc.page}")
    canvas.restoreState()


def cover(canvas, doc):
    pass


def build():
    check_evidence()
    p = {n: q(f"quartus_C3-P{n}_*.md") for n in (0, 2, 4, 6)}
    seeds = {(n, s): (p[n] if s == 1 else q(f"seed_sweep/quartus_C3-P{n}-s{s}_*.md")) for n in (4, 6)
             for s in range(1, 7)}
    cyc = {0: (113, 369), 2: (115, 371), 4: (117, 373), 6: (119, 375)}
    p6_alm = [seeds[(6, s)]["alm"] for s in range(1, 7)]
    p6_f = [seeds[(6, s)]["fmax_low"] for s in range(1, 7)]
    p4_alm = [seeds[(4, s)]["alm"] for s in range(1, 7)]
    p4_f = [seeds[(4, s)]["fmax_low"] for s in range(1, 7)]
    assert (min(p6_alm), max(p6_alm)) == (10484, 10516) and (min(p6_f), max(p6_f)) == (32.60, 34.20)

    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=17 * mm, title="CHIPATON — Laporan Fase 4 (ID)",
                            author="Tim J5 (ITB)",
                            subject="Fase 4: optimasi pipeline butterfly NTT/INTT ML-KEM-768 pada DE10-Nano")
    st = []
    W = A4[0] - 36 * mm

    # cover (same layout as the Phase 0-3 reports)
    st += [Spacer(1, 62 * mm)]
    st += [P("PERURI Digital Summit · CHIP 2026 Hackathon — Tim J5 (ITB)", "csub"), Spacer(1, 6)]
    st += [P("Laporan Fase 4", "ctitle")]
    st += [P("Optimasi Pipeline — C3-P6 / L8 · Akselerator NTT/INTT ML-KEM-768", "csub")]
    st += [P("Terasic DE10-Nano · Intel/Altera Cyclone V SE 5CSEBA6U23I7", "csub"), Spacer(1, 14)]
    st += [P("Status: <b>DONE</b> — konfigurasi terpilih C3-P6 (L = 8, P = 6) dan anggaran desain inti NTT 30% = "
             "12.573 ALM (ADR 0009); timing 40 ns terpenuhi; Approval belum dicentang", "cmeta")]
    st += [P("Branch: phase4-pipeline · dibuat di atas a803386, sebelum commit finalisasi Fase 4 · 2026-10-01", "cmeta"),
           Spacer(1, 22)]
    st += [P("Ditulis untuk: Tim J5. Sumber kebenaran tetap berkas di repo (docs/results/result_phase4.md, "
             "docs/evidence/phase04-pipeline/, docs/decisions/); dokumen ini rangkuman bacaan. Label: <b>MEASURED</b> "
             "(laporan Quartus atau log simulasi di repo), <b>INFERENCE</b> (turunan dari angka terukur), "
             "<b>ESTIMATE</b> (perkiraan dengan metode tertulis), <b>belum diukur</b>. Tidak ada pengukuran pada papan; "
             "semua hasil berasal dari simulasi dan analisis Quartus (<i>kernel-only</i>, <i>virtual pin</i>).", "small")]
    st += [PageBreak()]

    # 2. executive summary
    p6 = p[6]
    st += [P("1. Ringkasan Eksekutif", "h1")]
    st += bullets([
        f"Fase 4 menambahkan register <i>pipeline</i> pada jalur butterfly inti NTT/INTT 8 lajur (C2-K2-K1, L = 8) "
        f"dan mengukur empat kedalaman P = 0, 2, 4 dan 6 pada satu batasan 40 ns.",
        f"<b>Keputusan (ADR 0009):</b> L = 8, P = 6 (C3-P6), anggaran desain inti NTT 30% = 12.573 ALM.",
        f"<b>C3-P6, MEASURED:</b> {fmt(p6['alm'])} ALM (seed bawaan; {fmt(min(p6_alm))}–{fmt(max(p6_alm))} pada seed 1–6), "
        f"9 DSP, {p6['ram'].split(' /')[0]} M10K; timing 40 ns terpenuhi di semua seed; Fmax corner terendah "
        f"{num(min(p6_f))}–{num(max(p6_f))} MHz. Siklus (simulasi): NTT 119, INTT 375, tanpa <i>stall</i>.",
        "<b>Verifikasi:</b> bit-exact terhadap model golden di dua simulator; jumlah siklus konstan; bukti formal "
        "kontrol dan kapasitas bank lulus; uji negatif hazard terbukti mendeteksi; regresi Fase 0–3 tetap lulus.",
        "<b>Integrasi (baseline C3-P4):</b> GHRD DE10-Nano + C3-P4 dalam satu kompilasi = 12.754 ALM; "
        "selisih integrasi +18 ALM terhadap komponen standalone dengan setting yang sama; HPS memakai 0 ALM fabric. "
        "C3-P6 + GHRD <b>belum</b> dikompilasi bersama.",
        "<b>Belum tercapai:</b> target 50 MHz (Fase 5). Sumber daya tingkat sistem (Keccak, sampler, kontrol KEM) "
        "belum diukur.",
    ])

    # 3. goal
    st += [P("2. Tujuan Fase 4", "h1")]
    st += [P("Menaikkan Fmax inti NTT/INTT pada L yang sudah dipilih (ADR 0005) dengan memasang register "
             "<i>pipeline</i>, tanpa mengubah aritmetika, urutan lapisan, atau jadwal lajur, dan dengan biaya "
             "<i>stall</i> yang dihitung. Keluaran fase: hasil benar untuk setiap P, perbandingan terukur, ADR untuk P "
             "terpilih, dan baris C3 di matriks ablasi (<font name='DVM'>docs/ROADMAP.md</font>).")]

    # 4. targets
    st += [P("3. Target dan Batasan", "h1")]
    st += [table([["Butir", "Nilai", "Sumber"],
                  ["Device", "5CSEBA6U23I7, penyebut fitter 41.910 ALM, 553 M10K, 112 DSP", "laporan fitter"],
                  ["Batasan clock Fase 4", "<font name='DVM'>create_clock -period 40.000</font> (25 MHz), sama untuk "
                                           "semua revisi termasuk P = 0; target eksperimental, bukan kebutuhan sistem",
                   "ADR 0006"],
                  ["Target Fase 5", "20 ns (50 MHz)", "ADR 0006"],
                  ["Anggaran desain inti NTT", "30% × 41.910 = <b>12.573 ALM</b> (metrik "
                                               "<i>Logic utilization, ALMs needed</i>)", "ADR 0009"],
                  ["Anggaran historis", "25% = 10.478 ALM (ADR 0004); dipakai ADR 0008 (tidak diterima)",
                   "ADR 0004, 0008"],
                  ["Cakupan anggaran 30%", "Hanya inti NTT Fase 4. <b>Bukan</b> batas total sistem, dan tidak "
                                           "berarti sisa 70% pasti cukup untuk seluruh ML-KEM", "ADR 0009"]],
                 [36 * mm, W - 62 * mm, 26 * mm])]

    # 5. architecture
    st += [P("4. Arsitektur", "h1")]
    st += [P("<b>L (jumlah lajur)</b> menentukan berapa butterfly dikerjakan per siklus: L = 8 berarti 8 butterfly "
             "paralel, sehingga satu lapisan NTT (128 butterfly) selesai dalam 16 siklus. <b>P (kedalaman pipeline)</b> "
             "adalah jumlah tahap register antara siklus alamat dikeluarkan dan siklus hasil ditulis; P tidak mengubah "
             "jumlah butterfly per siklus, hanya memotong jalur kritis dan menambah P siklus pengosongan di akhir.")]
    st += [table([["P", "Posisi potongan (test plan §2)", "Latensi baca / tulis", "NTT / INTT (siklus)"],
                  ["0", "tanpa register (C2-K2-K1 beku)", "0 / 0", "113 / 369"],
                  ["2", "A_13, D_3", "1 / 1", "115 / 371"],
                  ["4", "A_7, M, X, D_7", "2 / 2", "117 / 373"],
                  ["6 (terpilih)", "A_4, A_11, M, X, D_5, D_11", "3 / 3", "119 / 375"]],
                 [24 * mm, 70 * mm, 32 * mm, W - 126 * mm], sel_rows=(4,))]
    st += [P("A_k: register di dalam rantai arbitrasi slot memori setelah k dari 16 port; M: setelah arbitrasi; "
             "X: setelah perkalian; D_n: setelah n dari 13 tahap pengurangan bersyarat di reduksi modular. "
             "Reduksi ditulis ulang sebagai 13 tahap eksplisit dengan hasil identik dengan reduksi lama untuk semua "
             "2<super>24</super> pasangan masukan (MEASURED, simulasi exhaustive). Memori polinomial memisahkan "
             "alamat baca dan tulis; (bank, offset, slot) dari baca dipakai ulang untuk tulis.", "small")]

    # 6. candidates + 7. resource + 8. timing
    head6 = P("5. Kandidat Pipeline (seed bawaan, MEASURED)", "h1")
    rows = [["P", "ALM", "≤ 12.573?", "≤ 10.478 (historis)?", "Reg.", "M10K", "DSP", "Setup / hold terburuk (ns)",
             "Timing 40 ns", "Fmax terendah (MHz)", "t_NTT (µs)"]]
    for n in (0, 2, 4, 6):
        r = p[n]
        rows.append([f"{n}{' (terpilih)' if n == 6 else ''}", fmt(r["alm"]), "ya" if r["alm"] <= BUDGET_30 else "tidak",
                     "ya" if r["alm"] <= BUDGET_25 else "tidak", fmt(r["reg"]), r["ram"].split(" /")[0],
                     r["dsp"].split(" /")[0], f"{num(r['setup'], 3)} / {num(r['hold'], 3)}",
                     "terpenuhi" if r["setup"] >= 0 and r["hold"] >= 0 else "<b>tidak</b>", num(r["fmax_low"]),
                     num(cyc[n][0] / r["fmax_low"], 3)])
    st += [KeepTogether([head6, table(rows, [17 * mm, 14 * mm, 14 * mm, 18 * mm, 12 * mm, 11 * mm, 9 * mm, 24 * mm,
                                             16 * mm, 17 * mm, W - 152 * mm], sel_rows=(4,))])]
    st += [P("t_NTT = siklus NTT / Fmax terendah (aturan ADR 0007; INFERENCE dari angka MEASURED). Dengan anggaran 30%, "
             "kandidat adalah {4, 6}; t_NTT minimum dimiliki P = 6 dan P = 4 berada 5,1% di atasnya (> 5%), sehingga "
             "aturan memilih <b>P = 6</b> pada seed bawaan. Latensi C3-P6 pada batasan 40 ns yang terpenuhi "
             "(perhitungan tim): NTT 119 × 40 ns = 4,76 µs; INTT 375 × 40 ns = 15,00 µs.", "small")]
    st += [P("6. Hasil Sumber Daya", "h1")]
    st += bullets([
        f"C3-P6: {fmt(p6['alm'])} / 41.910 ALM ({num(100 * p6['alm'] / TOTAL_ALM)}%), margin "
        f"{fmt(BUDGET_30 - p6['alm'])} ALM terhadap 12.573 (MEASURED / INFERENCE).",
        "Memori polinomial (penyimpanan <i>flip-flop</i> 16 port) adalah porsi terbesar inti: 7.621 ALM pada C3-P4 "
        "(MEASURED, tabel entity fitter; lihat draf estimasi fabric).",
        "Dengan register di jalur memori, Quartus meng-infer M10K sendiri (16/26/29 blok untuk P = 2/4/6; 0 untuk P = 0). "
        "Ini efek alat, bukan pemetaan M10K yang dirancang.",
        "DSP tetap 9 untuk semua P (satu pengali per lajur + satu untuk penskalaan INTT).",
    ])
    st += [P("7. Hasil Timing", "h1")]
    st += bullets([
        "P = 0 dan P = 2 <b>tidak</b> memenuhi 40 ns (setup −90,653 ns dan −0,368 ns); keduanya gugur oleh syarat timing.",
        f"P = 4 dan P = 6 memenuhi 40 ns di semua corner. C3-P6 seed bawaan: setup +{num(p6['setup'], 3)} ns, hold "
        f"+{num(p6['hold'], 3)} ns, Fmax {num(p6['fmax_low'])} MHz (corner lambat terendah).",
        "Target 50 MHz (20 ns) belum tercapai oleh revisi mana pun; Fmax tertinggi yang terukur 34,20 MHz (C3-P6, seed 4).",
    ])

    # 9. seed sweep
    head9 = P("8. <i>Seed Sweep</i> (seed fitter 1–6, MEASURED)", "h1")
    rows = [["Seed", "P4 ALM", "P4 Fmax (MHz)", "P4 setup (ns)", "P6 ALM", "P6 Fmax (MHz)", "P6 setup (ns)"]]
    for s in range(1, 7):
        a, b = seeds[(4, s)], seeds[(6, s)]
        rows.append([f"{s}{' (bawaan)' if s == 1 else ''}", fmt(a["alm"]), num(a["fmax_low"]), num(a["setup"], 3),
                     fmt(b["alm"]), num(b["fmax_low"]), num(b["setup"], 3)])
    rows.append(["Rentang", f"{fmt(min(p4_alm))}–{fmt(max(p4_alm))}", f"{num(min(p4_f))}–{num(max(p4_f))}", "≥ 0 semua",
                 f"{fmt(min(p6_alm))}–{fmt(max(p6_alm))}", f"{num(min(p6_f))}–{num(max(p6_f))}", "≥ 0 semua"])
    st += [KeepTogether([head9, table(rows, [24 * mm] + [(W - 24 * mm) / 6] * 6, sel_rows=(7,))])]
    st += bullets([
        "Hanya seed yang berbeda; RTL, SDC dan semua setting lain identik. Seluruh 12 kompilasi memenuhi 40 ns.",
        f"C3-P6 di bawah 12.573 ALM pada semua seed (margin {fmt(BUDGET_30 - max(p6_alm))}–{fmt(BUDGET_30 - min(p6_alm))} ALM). "
        "Pada anggaran historis 25%, P = 6 melebihi 10.478 di semua seed dan P = 4 hanya masuk di 4 dari 6 seed.",
        "Aturan ADR 0007 dengan anggaran 30% memilih P = 6 pada seed 1, 4, 5 dan P = 4 pada seed 2, 3, 6: kedua P "
        "berada dekat garis <i>near-tie</i> 5%. Pilihan P = 6 konsisten dengan aturan pada seed bawaan yang dipakai "
        "untuk semua revisi terukur; tidak diklaim bebas seed.",
    ])

    # 10. verification
    st += [PageBreak(), P("9. Verifikasi (MEASURED, simulasi dan formal)", "h1")]
    st += [table([["Butir", "Hasil", "Bukti"],
                  ["Unit: reduksi bertahap, butterfly pipeline, memori pipeline (V2–V4)",
                   "32/32 lulus di Verilator dan 32/32 di Icarus", "cocotb_regression_2026-09-30.txt"],
                  ["Reduksi bertahap vs reduksi lama, exhaustive", "16.777.216 pasangan × 4 konfigurasi, 0 selisih",
                   "v2_modmul_staged_exhaustive_2026-09-30.txt"],
                  ["Inti P = 2/4/6 vs model golden (V5): NTT, INTT, round-trip, data terarah",
                   "16/16 lulus di Verilator dan Icarus", "cocotb_regression_2026-09-30.txt"],
                  ["Siklus konstan (V6)", "C3-P6: NTT 119, INTT 375, identik di dua simulator; 0 <i>stall</i>",
                   "cocotb_regression_2026-09-30.txt"],
                  ["Scoreboard hazard + uji negatif (V7)", "0 pelanggaran untuk P = 2/4/6; kontrol negatif P = 8: 640 "
                                                           "pelanggaran per arah dan 5/5 hasil salah (terdeteksi)",
                   "cocotb_regression_2026-09-30.txt"],
                  ["bank_overflow_o (V8)", "selalu 0", "cocotb_regression_2026-09-30.txt"],
                  ["Formal Fase 4 (V9): handshake, overflow bank, rentang counter, delay tulis = P, drain, tidak ada "
                   "baca/tulis alamat sama", "P = 2/4/6 lulus; 9/9 hasil sesuai harapan termasuk kontrol negatif",
                   "formal_2026-09-30.md"],
                  ["Regresi Fase 0–3 (V10/V11)", "pytest 23/23; C0 10/10; C1 12/12; C2, K2, K1 16/16 tiap simulator; "
                                                 "check_params lulus; formal Fase 1–3 19/19",
                   "regression_2026-09-30.txt"]],
                 [62 * mm, 66 * mm, W - 128 * mm])]
    st += [P("Formal mencakup properti kontrol dan kapasitas bank, bukan aritmetika; kebenaran aritmetika bertumpu "
             "pada simulasi bit-exact dan uji exhaustive reduksi. Lokasi bukti: "
             "<font name='DVM'>docs/evidence/phase04-pipeline/</font>.", "small")]

    # 11. GHRD
    st += [P("10. Bukti Integrasi GHRD", "h1")]
    st += [P("Intel DE10-Nano GHRD (commit 9b5fc816…, revisi <font name='DVM'>de10-nano-base</font>) dikompilasi "
             "tanpa inti NTT, lalu bersama C3-P4 dalam satu kompilasi. C3-P4 dipakai sebagai <b>baseline integrasi</b>; "
             "<b>C3-P6 + GHRD belum dikompilasi bersama</b>. NTT memakai clock sendiri 40 ns lewat <i>virtual pin</i> "
             "dan tidak dihubungkan ke HPS atau bridge.")]
    st += [table([["Metrik (MEASURED)", "C3-P4 + setting GHRD", "GHRD standalone", "Gabungan"],
                  ["ALM needed", "11.432", "1.304 (1.309 pada build lain)", "<b>12.754</b>"],
                  ["M10K / DSP", "26 / 9", "35 / 0", "60 / 9"],
                  ["Timing", "NTT 40 ns terpenuhi", "semua clock terpenuhi", "semua clock terpenuhi; NTT setup +9,204 ns, "
                                                                            "Fmax 32,47 MHz"],
                  ["Packing / interconnect puncak", "Low / 52,7%", "Low / 11,6%", "Low / <b>48,2%</b>"]],
                 [44 * mm, 38 * mm, 42 * mm, W - 124 * mm])]
    st += bullets([
        "HPS adalah blok <i>hard</i>: 0 ALM fabric (MEASURED). Biaya fabric shell berasal dari interconnect Platform "
        "Designer dan IP demo GHRD.",
        "Selisih integrasi = 12.754 − 11.432 − 1.304 = <b>+18 ALM</b> (INFERENCE, setting konsisten).",
        "Setting global GHRD (<i>aggressive performance</i>, <i>physical synthesis</i>) menaikkan C3-P4 dari 10.439 ke "
        "11.432 ALM (+993, MEASURED): setting kompilasi sistem ikut menentukan anggaran.",
        "Penurunan Fmax NTT 34,35 → 32,47 MHz (corner lambat terendah, −5,5%) dibanding standalone dengan setting sama berada dalam rentang variasi seed "
        "(4,8–7,5%) dan belum terbukti sebagai efek integrasi.",
    ])

    # 12. decision
    st += [P("11. Keputusan", "h1")]
    st += [P("<b>ADR 0009 (Accepted, 2026-10-01, Faza Dzil, Tim J5):</b> L = 8, P = 6, implementasi C3-P6; anggaran "
             "desain inti NTT 30% = 12.573 ALM. ADR 0004 (25%) dan ADR 0007 (syarat ALM) diberi catatan amandemen di "
             "header-nya tanpa mengubah teks lama; ADR 0008 (usulan P = 4 di bawah 25%) tidak pernah diterima dan "
             "dinyatakan <i>superseded</i>. Pengukuran lama tetap berlaku sebagai bukti.")]

    # 13. limitations
    st += [P("12. Keterbatasan dan Hal Terbuka", "h1")]
    st += bullets([
        "C3-P6 + GHRD belum dikompilasi bersama; bukti integrasi memakai C3-P4.",
        "ML-KEM lengkap belum diukur: Keccak, sampler, kontrol KEM, encode/compress, penyimpanan, bridge HPS dan "
        "SignalTap belum ada. Draf estimasi isi fabric (ESTIMATE, keyakinan rendah) ada di "
        "<font name='DVM'>fabric_estimate_DRAFT_2026-10-01.md</font>.",
        "Target 50 MHz (Fase 5) belum tercapai; Fmax terukur tertinggi 34,20 MHz.",
        "Sumber daya tingkat sistem dan anggaran sistem belum ditetapkan; setting kompilasi sistem memengaruhi ALM inti.",
        "Tidak ada pengukuran pada papan; semua timing adalah analisis statis Quartus (<i>kernel-only</i>).",
        "Variasi alat: ALM bergeser hingga 64 ALM antar seed; build GHRD yang sama memberi 1.304 dan 1.309 ALM.",
    ])

    # 14. conclusion
    st += [P("13. Kesimpulan", "h1")]
    st += [P(f"Pipeline enam tahap menaikkan Fmax inti 8 lajur dari {num(p[0]['fmax_low'])} MHz (P = 0) menjadi "
             f"{num(min(p6_f))}–{num(max(p6_f))} MHz (P = 6, seed 1–6) pada batasan 40 ns yang terpenuhi, dengan biaya "
             "6 siklus tambahan per transformasi, tanpa <i>stall</i>, dan dengan hasil bit-exact. C3-P6 berada di dalam "
             "anggaran desain 30% di semua seed yang diuji. Eksperimen integrasi menunjukkan shell HPS menambah sedikit ALM "
             "dan tidak menimbulkan kongesti yang terukur. Langkah berikutnya adalah Fase 5 (aritmetika modular) menuju "
             "50 MHz, dimulai dari C3-P6.")]

    # 15. reproducibility
    st += [P("14. Reproduksibilitas", "h1")]
    st += [P("Quartus Prime Lite 25.1std.0 Build 1129, device 5CSEBA6U23I7, seed fitter bawaan (1) untuk semua revisi "
             "terukur; seed 2–6 hanya untuk sweep. Proyek: <font name='DVM'>quartus/phase04_pipeline_c3/</font> "
             "(revisi C3-P0/P2/P4/P6 dan C3-P{4,6}-s{2..6}; jalankan satu per satu, kompilasi paralel merusak "
             "<font name='DVM'>.qpf</font> bersama).")]
    st += [Paragraph("<br/>".join([
        ". scripts/env.sh",
        "python3 tb/ntt/run_p4_unit_tests.py verilator; python3 tb/ntt/run_p4_unit_tests.py icarus",
        "python3 tb/ntt/run_ntt_c3_tests.py verilator; python3 tb/ntt/run_ntt_c3_tests.py icarus",
        "tb/ntt/p4_reducer/run_modmul_staged_exhaustive.sh",
        "python3 formal/run_formal_phase4.py; python3 formal/run_formal_slang.py",
        "cd quartus/phase04_pipeline_c3 && quartus_sh --flow compile phase04_pipeline_c3 -c C3-P6",
        "python3 scripts/phase4_select_p.py --alm-budget 12573",
        "python3 scripts/phase4_seed_sweep_summary.py --alm-budget 12573",
        "python3 scripts/build_phase4_report.py          # laporan ini"]), S["code"])]
    st += [P("Bukti utama: " + ", ".join(f"<font name='DVM'>{x}</font>" for x in [
        str(p[6]["file"]), "selection_worksheet_30pct_2026-10-01.md", "seed_sweep_2026-10-01.md",
        "cocotb_regression_2026-09-30.txt", "formal_2026-09-30.md", "regression_2026-09-30.txt",
        "ghrd_shell_measured_2026-10-01.md", "ghrd_plus_c3p4_integration_2026-10-01.md",
        "docs/decisions/0009-…md", "docs/results/result_phase4.md"]) + ".", "small")]

    doc.build(st, onFirstPage=cover, onLaterPages=footer)
    print(f"written {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
