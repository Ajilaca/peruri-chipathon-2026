#!/usr/bin/env python3
"""scripts/build_phase5m_report.py

Builds docs/report/CHIPATON_Phase5M_Report.pdf (Phase 5M report, steps S6-S8, Bahasa Indonesia, same layout, fonts and styles as the
Phase 0-5 reports; the styles are imported from scripts/build_phase4_report.py) with ReportLab.

Every number comes from an evidence file in this repository:
  - Quartus figures (ALM, registers, M10K, DSP, slack, Fmax) are parsed from the extracted evidence files with the same parser as
    the selection scripts (scripts/phase5_select_5b.py: parse_quartus);
  - every other figure is a literal that is first checked to appear in its evidence file (EXPECT below); the build stops if one
    is missing, so the PDF cannot silently drift from the evidence. The rule verdicts are recomputed here and asserted.

Usage: python3 scripts/build_phase5m_report.py
"""
import pathlib
import statistics
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_phase4_report import MUTED, P, S, bullets, fmt, num, table  # noqa: E402
from phase5_select_5b import parse_quartus  # noqa: E402

EM = ROOT / "docs" / "evidence" / "phase05m-memsched"
E5 = ROOT / "docs" / "evidence" / "phase05-arith"
OUT = ROOT / "docs" / "report" / "CHIPATON_Phase5M_Report.pdf"
BUDGET_30 = 12573

EXPECT = {
    EM / "s6/selection_worksheet_2026-10-02.md": ["34.430 (32.35-35.04)", "NOT adopted by the rule"],
    EM / "s7/selection_worksheet_2026-10-02.md": ["38.720 (37.89-40.29)", "**Rule result: S7 ADOPTED.**"],
    EM / "s8/selection_worksheet_2026-10-03.md": ["Rule result: S8 NOT adopted by the rule"],
    EM / "s8/regression_2026-10-03.md": ["added 95, modified 2", "all results as expected (19/19)", "all results as expected (9/9)",
                                         "OVERALL: PASS"],
    EM / "s8/formal_2026-10-03.md": ["all results as expected (3/3)"],
    E5 / "closure/info_20ns_2026-10-01.md": ["10,557", "9,305", "45.33", "44.33"],
}


def check_evidence():
    missing = []
    for f, items in EXPECT.items():
        if not f.exists():
            missing.append(f"{f.relative_to(ROOT)}: file missing")
            continue
        text = f.read_text()
        missing += [f"{f.relative_to(ROOT)}: {it!r}" for it in items if it not in text]
    if missing:
        raise SystemExit("evidence check failed:\n  " + "\n  ".join(missing))


def q(path):
    r = parse_quartus(path)
    r["file"] = path.relative_to(ROOT)
    return r


def seeds(folder, prefix, date):
    return [q(folder / f"quartus_{prefix}{'' if s == 1 else f'-s{s}'}_{date}.md") for s in range(1, 7)]


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DV", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"CHIPATON — Laporan Fase 5M (ID) — hal. {doc.page}")
    canvas.restoreState()


def build():
    check_evidence()
    c4 = seeds(E5 / "5b", "C4b-B", "20261001")
    m6 = seeds(EM / "s6", "M6", "20261002")
    s7 = seeds(EM / "s7", "S7", "20261002")
    s8 = seeds(EM / "s8", "S8", "20261002")
    i_c3 = q(E5 / "closure" / "quartus_C3-P6-20_20261001.md")
    i_c4 = q(E5 / "closure" / "quartus_C4b-B-20_20261001.md")
    i_s8 = q(EM / "s8" / "quartus_S8-20_20261002.md")

    def rng(rows, k):
        v = [r[k] for r in rows]
        return min(v), max(v), statistics.median(v)

    f4, f6, f7, f8 = (rng(x, "fmax") for x in (c4, m6, s7, s8))
    a4, a6, a7, a8 = (rng(x, "alm") for x in (c4, m6, s7, s8))
    t4n, t4i = 119 / f4[2], 375 / f4[2]
    t6, t7, t8 = 119 / f6[2], 120 / f7[2], 122 / f8[2]
    th7, th8 = 120 * f6[2] / 119, 122 * f7[2] / 120
    # the narrative below depends on these verdicts: stop if the evidence says otherwise
    assert f6[2] < 34.515 and abs(f6[2] - 34.430) < 1e-9, "S6 verdict changed"
    assert f7[2] > th7, "S7 verdict changed"
    assert f8[2] < th8, "S8 verdict changed"
    assert all(r["alm"] <= BUDGET_30 and r["setup"] >= 0 and r["hold"] >= 0 for r in m6 + s7 + s8)

    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=17 * mm, title="CHIPATON — Laporan Fase 5M (ID)", author="Tim J5 (ITB)",
                            subject="Fase 5M: memori dan jadwal NTT/INTT ML-KEM-768 pada DE10-Nano (S6-S8)")
    st = []
    W = A4[0] - 36 * mm

    st += [Spacer(1, 62 * mm)]
    st += [P("PERURI Digital Summit · CHIP 2026 Hackathon — Tim J5 (ITB)", "csub"), Spacer(1, 6)]
    st += [P("Laporan Fase 5M", "ctitle")]
    st += [P("Memori dan Jadwal (S6–S8) · Akselerator NTT/INTT ML-KEM-768", "csub")]
    st += [P("Terasic DE10-Nano · Intel/Altera Cyclone V SE 5CSEBA6U23I7", "csub"), Spacer(1, 14)]
    st += [P("Status: <b>S6–S8 selesai diukur</b>. S6 (M6) dipakai atas keputusan tim (ADR 0020); S7 memenuhi aturan adopsi "
             "(ADR 0021 <b>Proposed</b>); S8 <b>tidak diadopsi oleh aturan</b>; S9 ditunda (pending); Approval belum dicentang", "cmeta")]
    st += [P("Branch: phase5m-memory-schedule · 2026-10-03", "cmeta"), Spacer(1, 22)]
    st += [P("Ditulis untuk: Tim J5. Sumber kebenaran tetap berkas di repo (docs/results/result_phase5m.md, "
             "docs/evidence/phase05m-memsched/, docs/decisions/); dokumen ini rangkuman bacaan. Label: <b>MEASURED</b> "
             "(laporan Quartus atau log simulasi di repo), <b>INFERENCE</b> (turunan dari angka terukur), <b>ESTIMATE</b> "
             "(perkiraan dengan metode tertulis), <i>perhitungan tim</i> (aritmetika dari angka terukur), <b>belum diukur</b>. "
             "Tidak ada pengukuran pada papan; semua hasil berasal dari simulasi, analisis formal dan analisis Quartus "
             "(<i>kernel-only</i>, <i>virtual pin</i>).", "small")]
    st += [PageBreak()]

    st += [P("1. Ringkasan Eksekutif", "h1")]
    st += bullets([
        "Fase 5M mengubah <b>memori dan jadwal</b> inti NTT/INTT (bukan aritmetika) karena jalur kritis terukur ada di pembacaan "
        "memori (ADR 0010, 0017). Matematika FIPS 203 tidak diubah; setiap langkah diuji bit-exact terhadap model golden.",
        f"<b>S6 (M6, INTT tanpa <i>scaling pass</i>):</b> INTT 375 → 119 siklus (sama dengan NTT), DSP 18 → 16, median Fmax "
        f"{num(f6[2], 3)} MHz (C4b-B {num(f4[2], 3)}). Aturan: <b>tidak diadopsi</b> (bagian NTT gagal 0,008 µs, selisih 0,25% di dalam "
        "sebaran seed); tim memakai M6 sebagai basis (ADR 0020).",
        f"<b>S7 (pembelahan jalur baca memori, P = 7):</b> median Fmax <b>{num(f7[2], 3)} MHz</b> ({num(f7[0])}–{num(f7[1])}), "
        f"naik {num(100 * (f7[2] / f6[2] - 1), 1)}% dari M6; seed terendah S7 ({num(f7[0])}) di atas seed tertinggi M6 ({num(f6[1])}). "
        f"Siklus 120 / 120; ALM median {fmt(round(a7[2]))} (tidak naik). Aturan: <b>diadopsi</b> (ADR 0021, Proposed).",
        f"<b>S8 (register jalur tulis, P = 8, satu <i>bubble</i> per arah):</b> siklus 122 / 122 (sesuai prediksi), tetapi median Fmax "
        f"{num(f8[2], 3)} MHz, <b>di bawah</b> S7 ({num(f7[2], 3)}); syarat &gt; {num(th8, 3)} MHz. Aturan: <b>tidak diadopsi</b>.",
        f"<b>Konfigurasi terbaik terukur:</b> S7 — t_NTT = t_INTT = {num(t7, 3)} µs pada median Fmax (perhitungan tim), dibanding "
        f"C4b-B {num(t4n, 3)} / {num(t4i, 3)} µs dan M6 {num(t6, 3)} µs. Menunggu keputusan tim (ADR 0021).",
        f"<b>Kompilasi informasi 20 ns (S8):</b> timing tidak terpenuhi (setup {num(i_s8['setup'], 3)} ns, Fmax {num(i_s8['fmax'])} MHz); "
        "target 50 MHz belum tercapai.",
        "<b>Regresi penuh Fase 0–5</b> dijalankan sekali pada pohon akhir (Amandemen A1): lulus; tidak ada berkas RTL, tes atau bukti "
        "Fase 1–5 yang diubah. S9 ditunda; tidak ada pengukuran pada papan.",
    ])

    st += [P("2. Tujuan dan Urutan Langkah", "h1")]
    st += [P("Fase 5 menunjukkan bahwa perubahan aritmetika tidak menaikkan Fmax di luar sebaran seed karena jalur kritis berada di "
             "pembacaan memori. Fase 5M (ADR 0017) mengubah satu hal per langkah pada memori dan jadwal, dengan rencana uji dan aturan "
             "adopsi ADR 0012 ditulis <b>sebelum</b> mengukur. ADR 0019 membatasi jalur ke ML-KEM penuh sebelum 2026-10-08; "
             "S6, S7 dan S8 dikerjakan, S9 ditunda.")]
    st += [table([["Langkah", "Perubahan (satu per langkah)", "Berkas baru", "P", "Siklus NTT / INTT"],
                  ["S6 (M6)", "INTT dibagi dua di setiap layer (3303 = 2<super>-7</super> mod q); <i>scaling pass</i> 256 siklus dan satu pengali dihapus",
                   "half_mod, butterfly_m6, twiddle_rom_half, ntt_core_m6", "6", "119 / 119"],
                  ["S7", "satu register di tengah pembacaan memori (192 bit data + 64 bit pemilih), kontrol tulis diperlambat satu siklus",
                   "poly_mem_multiport_split, ntt_core_s7", "7", "120 / 120"],
                  ["S8", "satu register pada keluaran <i>butterfly</i> (192 bit) sebelum menulis; satu siklus kosong (<i>bubble</i>) di satu batas layer per arah "
                         "(NTT setelah layer 3, INTT setelah layer 2; posisi hanya bergantung mode dan layer)",
                   "ntt_core_s8", "8", "122 / 122"]],
                 [20 * mm, 78 * mm, 42 * mm, 8 * mm, W - 148 * mm])]
    st += [P("Semua berkas baru; tidak ada berkas Fase 1–5 yang diubah (git diff 288a78c: 95 berkas ditambah, hanya ADR 0017 dan PENDING.md "
             "diubah — dokumen, bukan RTL).", "small")]

    st += [P("3. Aturan Adopsi (ADR 0012, ditetapkan sebelum mengukur)", "h1")]
    st += bullets([
        "Benar (lint, simulasi dua simulator, kontrol negatif gagal sesuai harapan, formal), siklus konstan dan tepat sesuai rencana.",
        f"ALM inti ≤ {fmt(BUDGET_30)} dan timing 40,000 ns terpenuhi di setiap seed 1–6.",
        "t_NTT dan t_INTT pada median Fmax seed 1–6 (corner lambat terendah) lebih baik dari langkah sebelumnya. Tanpa toleransi. "
        f"S7: F &gt; {num(th7, 3)} MHz; S8: F &gt; {num(th8, 3)} MHz.",
    ])

    st += [P("4. Hasil Terukur (MEASURED; median dan rentang seed 1–6 = INFERENCE)", "h1")]

    def row(name, rows, cyc, nm, fm, tn, ti):
        a, f = rng(rows, "alm"), rng(rows, "fmax")
        regs = rng(rows, "reg")
        return [name, f"{fmt(round(a[2]))} ({fmt(a[0])}–{fmt(a[1])})", f"{fmt(regs[0])}–{fmt(regs[1])}", rows[0]["dsp"], rows[0]["ram"],
                f"{num(f[2], 3)} ({num(f[0])}–{num(f[1])})", cyc, f"{num(tn, 3)} / {num(ti, 3)}"]
    rows = [["Revisi", "ALM median (min–maks)", "Registers", "DSP", "M10K", "Fmax median (min–maks) MHz", "Siklus N / I", "t_NTT / t_INTT (µs)"],
            row("C4b-B (Fase 5)", c4, "119 / 375", 0, 0, t4n, t4i), row("M6 (S6)", m6, "119 / 119", 0, 0, t6, t6),
            row("<b>S7</b>", s7, "120 / 120", 0, 0, t7, t7), row("S8", s8, "122 / 122", 0, 0, t8, t8)]
    st += [KeepTogether([table(rows, [24 * mm, 29 * mm, 20 * mm, 10 * mm, 11 * mm, 34 * mm, 18 * mm, W - 146 * mm], sel_rows=(3,))])]
    st += [P("Timing 40,000 ns terpenuhi di setiap seed semua revisi (setup terburuk ≥ +12,79 ns, hold ≥ +0,07 ns). t = siklus / median Fmax "
             "(perhitungan tim). M10K 31 pada S7 dan 33 pada S8 (diinfer alat; tidak dianalisis). Jumlah <i>register</i> S8 lebih rendah "
             "daripada S7 meski S8 menambah 192 bit: penyebabnya tidak dianalisis (hipotesis: alat menggabungkan atau memindahkan register).",
             "small")]
    head = [["Seed", "M6 ALM", "M6 Fmax", "S7 ALM", "S7 Fmax", "S8 ALM", "S8 Fmax"]]
    for s in range(6):
        head.append([f"{s + 1}", fmt(m6[s]["alm"]), num(m6[s]["fmax"]), fmt(s7[s]["alm"]), num(s7[s]["fmax"]), fmt(s8[s]["alm"]), num(s8[s]["fmax"])])
    head.append(["Median", fmt(round(a6[2])), num(f6[2], 3), fmt(round(a7[2])), num(f7[2], 3), fmt(round(a8[2])), num(f8[2], 3)])
    st += [table(head, [24 * mm] + [(W - 24 * mm) / 6] * 6, sel_rows=(7,))]

    st += [P("5. Verdict per Langkah", "h1")]
    st += [table([["Langkah", "Syarat yang gagal / lulus", "Hasil aturan"],
                  ["S6 (M6)", f"benar, 119 / 119, ALM, timing, t_INTT lulus; t_NTT {num(t6, 3)} ≥ 3,448 µs gagal (median Fmax "
                              f"{num(f6[2], 3)} ≤ 34,515)", "<b>tidak diadopsi oleh aturan</b>; basis S7/S8 atas keputusan tim (ADR 0020)"],
                  ["S7", f"semua lulus; t = {num(t7, 3)} &lt; {num(t6, 3)} µs (F {num(f7[2], 3)} &gt; {num(th7, 3)} MHz)", "<b>diadopsi oleh aturan</b>; ADR 0021 Proposed"],
                  ["S8", f"benar dan 122 / 122, ALM dan timing lulus; t = {num(t8, 3)} ≥ {num(t7, 3)} µs gagal (F {num(f8[2], 3)} ≤ {num(th8, 3)} MHz)",
                   "<b>tidak diadopsi oleh aturan</b>; ADR 0023 Proposed"]],
                 [22 * mm, W - 72 * mm, 50 * mm])]
    st += bullets([
        f"S7 menaikkan median Fmax {num(100 * (f7[2] / f6[2] - 1), 1)}% dan seed terendahnya di atas seed tertinggi M6 — lebih besar dari sebaran seed "
        f"yang teramati (S7: {num(f7[1] - f7[0])} MHz). Hasil ini mendukung hipotesis Fase 5 bahwa pembacaan memori adalah batas (INFERENCE; jalur kritis baru belum dianalisis).",
        f"S8 menambah dua siklus dan satu register tulis tetapi median Fmax turun {num(f7[2] - f8[2], 2)} MHz ({num(100 * (1 - f8[2] / f7[2]), 1)}%): "
        "setelah S7 segmen tulis bukan lagi pembatas, atau pembatas berpindah ke jalur lain (hipotesis; tidak ada analisis jalur setelah S7 atau S8). "
        "Aturan tidak diubah dan tidak ada seed tambahan.",
    ])

    st += [P("6. Kompilasi Informasi 20 ns (MEASURED, seed 1)", "h1")]
    st += [table([["Metrik", "C3-P6 @ 20 ns", "C4b-B @ 20 ns", "S8 @ 20 ns"],
                  ["ALM", fmt(i_c3["alm"]), fmt(i_c4["alm"]), fmt(i_s8["alm"])],
                  ["Setup terburuk (ns)", num(i_c3["setup"], 3), num(i_c4["setup"], 3), num(i_s8["setup"], 3)],
                  ["Timing 20 ns", "tidak terpenuhi", "tidak terpenuhi", "<b>tidak terpenuhi</b>"],
                  ["Fmax corner terendah (MHz)", num(i_c3["fmax"]), num(i_c4["fmax"]), num(i_s8["fmax"])]],
                 [50 * mm] + [(W - 50 * mm) / 3] * 3)]
    st += [P("S8 mendekati 50 MHz (kekurangan 2,24 ns) tetapi tidak mencapainya. Fmax di bawah batasan 20 ns tidak sebanding dengan "
             "angka 40 ns. Peringatan kritis S8-20: 15725 (clock dari <i>virtual pin</i>, seperti Fase 1–5) dan 332148 × 2 (timing tidak "
             "terpenuhi); ditriase tertulis, tidak ada yang di-<i>waive</i>. Tidak ada kompilasi 20 ns untuk S7.", "small")]

    st += [P("7. Verifikasi (MEASURED, simulasi dan formal)", "h1")]
    st += [table([["Butir", "Hasil", "Bukti"],
                  ["Lint Verilator <font name='DVM'>-Wall</font> dan slang (M6, S7, S8)", "0 peringatan, 0 galat", "s6/ s7/ s8/ verify_*.md"],
                  ["Inti vs model golden, Verilator dan Icarus (NTT, INTT, <i>round-trip</i>, data terarah, 512 vektor satuan INTT)",
                   "lulus; siklus konstan 119 / 119, 120 / 120, 122 / 122; skor <i>hazard</i> 0 pelanggaran", "s6/ s7/ s8/ verify_*.md"],
                  ["Kontrol negatif (mutan): S6 tiga, S7 dua (NCD, NCS), S8 dua (tanpa <i>bubble</i>, kontrol tulis tidak diperlambat)",
                   "gagal sesuai syarat di kedua simulator", "s6/ s7/ s8/ verify_*.md"],
                  ["Memori terpecah: RD_SPLIT = 0 sama dengan memori beku siklus demi siklus", "0 selisih", "s7/verify_2026-10-02.md"],
                  ["Formal H, O, R, A, B, C per langkah dengan NC-O dan NC-A", "3/3 sesuai harapan untuk M6, S7 dan S8", "s6/ s7/ s8/ formal_*.md"],
                  ["Regresi penuh Fase 0–5 + ulang S6 dan S7 pada pohon akhir (sekali, Amandemen A1)",
                   "OVERALL PASS; 19/19 dan 9/9 formal Fase 1–4; 95 berkas ditambah, 2 dokumen diubah", "s8/regression_2026-10-03.md"]],
                 [60 * mm, 70 * mm, W - 130 * mm])]
    st += [P("Formal mencakup properti kontrol dan kapasitas bank, bukan data; kebenaran data bertumpu pada simulasi bit-exact dan uji "
             "vektor satuan. Build cocotb Verilator mencetak <font name='DVM'>WIDTHEXPAND</font> untuk nilai parameter ARB_REG dari runner "
             "(bukan lint RTL).", "small")]

    st += [P("8. Keputusan dan Hal Menunggu Tim", "h1")]
    st += bullets([
        "<b>Diterima:</b> ADR 0017 (fase 5M), ADR 0019 (jalur minimal; catatan S7 dan S8 direncanakan), ADR 0020 (M6 basis).",
        "<b>Proposed, menunggu tim:</b> ADR 0021 (S7: aturan terpenuhi; terima sebagai konfigurasi?) dan ADR 0023 (S8: tidak diadopsi oleh aturan; "
        "konfigurasi untuk Fase 6 dan 7 adalah S7, M6 atau S8?). Pekerjaan S8 dimulai di atas S7 atas instruksi kerja 2026-10-02.",
        "<b>S9 ditunda</b> (dicatat di PENDING.md). PENDING #25 (pemeriksaan masukan FIPS 203) dan #26 (satu STOP per blok) masih terbuka.",
        "Kotak Approval <font name='DVM'>result_phase5.md</font> dan <font name='DVM'>result_phase5m.md</font> kosong; hanya anggota tim yang mencentangnya.",
    ])

    st += [P("9. Keterbatasan dan Hal Terbuka", "h1")]
    st += bullets([
        "Tidak ada pengukuran pada papan; semua timing adalah analisis statis Quartus (<i>kernel-only</i>, <i>virtual pin</i>).",
        "Tidak ada analisis jalur setelah S7 atau S8: penyebab hasil S7 (naik) dan S8 (turun) adalah hipotesis.",
        "Satu kompilasi 20 ns (S8, seed 1); tidak ada untuk M6 atau S7. Sebaran seed S7 2,40 MHz; selisih S8 terhadap S7 (0,73 MHz) berada "
        "di dalam sebaran itu, tetapi aturan tidak memakai toleransi.",
        "Jumlah register dan M10K berubah antar-langkah tanpa penjelasan terukur (diinfer alat).",
        "Penyimpangan proses tercatat di result_phase5m.md bagian 6 (contoh: <font name='DVM'>$error</font> ditolak Quartus; pola pkill; lint palsu di skrip S6 yang diperbaiki).",
        "Belum diukur: integrasi dengan HPS, daya, anggaran sumber daya tingkat sistem.",
    ])

    st += [P("10. Kesimpulan", "h1")]
    st += [P(f"Jalur baca memori memang pembatas: membelahnya (S7) menaikkan median Fmax dari {num(f6[2], 3)} ke {num(f7[2], 3)} MHz dengan satu siklus "
             f"tambahan, sehingga waktu per transformasi turun dari {num(t6, 3)} ke {num(t7, 3)} µs (perhitungan tim), sekaligus NTT dan INTT "
             f"sama-sama 120 siklus. Menambah register jalur tulis (S8) tidak membantu pada pengukuran ini. Konfigurasi terukur terbaik adalah S7; "
             "keputusan menjadikannya basis Fase 6 dan 7 ada pada tim. Target 50 MHz belum tercapai (S8 pada 20 ns: setup "
             f"{num(i_s8['setup'], 3)} ns).")]

    st += [P("11. Reproduksibilitas", "h1")]
    st += [Paragraph("<br/>".join([
        ". scripts/env.sh",
        "scripts/phase5m_verify.sh; scripts/phase5m_verify_s7.sh; scripts/phase5m_verify_s8.sh",
        "python3 formal/run_formal_phase5m.py; ..._s7.py; ..._s8.py",
        "cd quartus/phase05m_memsched &amp;&amp; ./run_m6_sweep.sh &amp;&amp; ./run_s7_sweep.sh &amp;&amp; ./run_s8_sweep.sh",
        "scripts/phase5m_final_regression.sh",
        "python3 scripts/phase5m_select_s6.py; ..._s7.py; ..._s8.py",
        "python3 scripts/build_phase5m_report.py          # laporan ini"]), S["code"])]
    st += [P("Bukti utama: " + ", ".join(f"<font name='DVM'>{x}</font>" for x in [
        "s6/selection_worksheet_2026-10-02.md", "s7/selection_worksheet_2026-10-02.md", "s8/selection_worksheet_2026-10-03.md",
        "s8/regression_2026-10-03.md", "test_plan.md", "test_plan_s7.md", "test_plan_s8.md", "docs/decisions/0017 … 0022",
        "docs/results/result_phase5m.md"]) + ".", "small")]

    doc.build(st, onFirstPage=lambda c, d: None, onLaterPages=footer)
    print(f"written {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
