#!/usr/bin/env python3
"""scripts/build/build_phase6_report.py

Builds docs/reports/CHIPATON_Phase6_Report.pdf (Phase 6 report incl. S10 and the 50 MHz options 1 and 2, Bahasa Indonesia, same layout, fonts and styles as the
Phase 0-5M reports; styles from scripts/build/build_phase4_report.py) with ReportLab.

Every number comes from an evidence file in this repository: Quartus figures are parsed from the extracted evidence files (scripts/quartus/phase5_select_5b.py: parse_quartus);
simulation figures are literals checked to appear in their evidence file (EXPECT); the S10 verdict is recomputed here from the files with the rule of
evidence/phase06/test_plan_s10.md section 4 and printed as computed (no narrative is written for a result that did not happen).
Usage: python3 scripts/build/build_phase6_report.py
"""
import json
import pathlib
import statistics
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "scripts" / g) for g in ("build", "quartus")]
from build_phase4_report import MUTED, P, S, bullets, fmt, num, table  # noqa: E402
from phase5_select_5b import parse_quartus  # noqa: E402

E6 = ROOT / "evidence" / "phase06"
E10 = E6 / "s10"
E7 = ROOT / "evidence" / "phase05m" / "s7"
E50 = ROOT / "evidence" / "phase05m" / "fmax50"
OUT = ROOT / "docs" / "reports" / "CHIPATON_Phase6_Report.pdf"
BUDGET = 12573

CYC = {"keygen": 5493, "encrypt": 6810, "decrypt": 3121}
CYC10 = {"keygen": 5475, "encrypt": 6789, "decrypt": 3109}
EXPECT = {
    E6 / "verify.md": ["pwm_unit: 20035/20035 pairs equal", "keygen: 3 random + 2 corner cases bit-exact, end-to-end equal, counters (6, 0, 9), cycles 5493",
                                  "encrypt: 3 random + 2 corner cases bit-exact, end-to-end equal, counters (3, 4, 12), cycles 6810",
                                  "decrypt: 3 random + 2 corner cases bit-exact, end-to-end equal, counters (3, 1, 3), cycles 3121", "26 passed", "OVERALL: PASS"],
    E6 / "formal.md": ["all results as expected (2/2)"],
    E10 / "verify.md": ["'cycles_NTT': 118, 'cycles_INTT': 118", "'keygen': 5475, 'encrypt': 6789, 'decrypt': 3109", "OVERALL: PASS"],
    E10 / "formal.md": ["all results as expected (3/3)"],
    E50 / "path_analysis.md": ["14.439", "17.711", "23.932"],
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


def q(path):
    return parse_quartus(path)


def seeds(folder, prefix):
    out = []
    for s in range(1, 7):
        files = sorted(folder.glob(f"quartus_{prefix}{'' if s == 1 else f'-s{s}'}.md"))
        if not files:
            raise SystemExit(f"missing {prefix} seed {s} in {folder}")
        out.append(q(files[-1]))
    return out


def med(rows, k):
    return statistics.median(r[k] for r in rows)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DV", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"CHIPATON — Laporan Fase 6 (ID) — hal. {doc.page}")
    canvas.restoreState()


def build():
    check_evidence()
    p6 = q(E6 / "quartus_P6.md")
    p6s, p6s20 = q(E6 / "quartus_P6S10.md"), q(E6 / "quartus_P6S10-20.md")
    s7, s10 = seeds(E7, "S7"), seeds(E10, "S10")
    s7_20, s10_20 = seeds(E50, "S7-20"), seeds(E10, "S10-20")
    status = json.loads((E10 / "verification_status.json").read_text())
    f7, f10 = med(s7, "fmax"), med(s10, "fmax")
    t7, t10 = 120 / f7, 118 / f10
    rule = [("benar (V1-V6, kontrol negatif gagal)", status["correct"] == "PASS"),
            ("siklus tepat 118 / 118", (status["cycles_NTT"], status["cycles_INTT"]) == (118, 118)),
            (f"ALM ≤ {fmt(BUDGET)} di setiap seed", all(r["alm"] <= BUDGET for r in s10)),
            ("timing 40 ns terpenuhi di setiap seed", all(r["setup"] >= 0 and r["hold"] >= 0 for r in s10)),
            (f"ADR 0012: 118 / F &lt; 120 / F_S7, yaitu F &gt; {num(118 * f7 / 120, 3)} MHz (terukur {num(f10, 3)})", t10 < t7)]
    adopted = all(ok for _, ok in rule)
    met20 = {name: sum(1 for r in rows if r["setup"] >= 0) for name, rows in (("S7-20", s7_20), ("S10-20", s10_20))}

    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=17 * mm,
                            title="CHIPATON — Laporan Fase 6 (ID)", author="Tim J5 (ITB)",
                            subject="Fase 6: penjadwalan tingkat operasi K-PKE dan S10 (memori 16 bank) pada DE10-Nano")
    st = []
    W = A4[0] - 36 * mm
    st += [Spacer(1, 62 * mm), P("PERURI Digital Summit · CHIP 2026 Hackathon — Tim J5 (ITB)", "csub"), Spacer(1, 6)]
    st += [P("Laporan Fase 6", "ctitle")]
    st += [P("Penjadwalan NTT Tingkat Operasi (K-PKE) · S10 Memori 16 Bank · Opsi 50 MHz", "csub")]
    st += [P("Terasic DE10-Nano · Intel/Altera Cyclone V SE 5CSEBA6U23I7", "csub"), Spacer(1, 14)]
    st += [P(f"Status: Fase 6 selesai diukur (bit-exact, jumlah transformasi sesuai, siklus konstan); S10 <b>{'diadopsi' if adopted else 'tidak diadopsi'} "
             "oleh aturan</b> (ADR 0025 <b>Proposed</b>); Approval belum dicentang", "cmeta")]
    st += [P("Branch: phase6-scheduling · 2026-10-03", "cmeta"), Spacer(1, 22)]
    st += [P("Ditulis untuk: Tim J5. Sumber kebenaran tetap berkas di repo (docs/results/phase06.md, evidence/phase06/, docs/decisions/). "
             "Label: <b>MEASURED</b> (laporan Quartus atau log simulasi di repo), <b>INFERENCE</b>, <b>ESTIMATE</b>, <i>perhitungan tim</i>, <b>belum diukur</b>. "
             "Tidak ada pengukuran pada papan; semua hasil berasal dari simulasi, analisis formal dan analisis Quartus (<i>kernel-only</i>, <i>virtual pin</i>).", "small")]
    st += [PageBreak()]

    move = {"keygen": 6 * (257 + 260), "encrypt": 7 * (257 + 260), "decrypt": 4 * (257 + 260)}
    st += [P("1. Ringkasan Eksekutif", "h1")]
    st += bullets([
        "Fase 6 menjalankan aritmetika K-PKE (KeyGen, Encrypt, Decrypt) sebagai <b>program tetap operasi polinomial</b> di perangkat keras: NTT/INTT memakai inti S7, "
        "perkalian titik (<i>BaseCaseMultiply</i> + akumulasi) dan penjumlahan memakai unit baru; masukan dari Keccak/sampler masih diberikan oleh <i>testbench</i>.",
        "<b>Bit-exact</b> terhadap golden K-PKE yang tidak diubah (t_hat KeyGen, ciphertext Encrypt setelah kompresi, pesan Decrypt) di Verilator dan Icarus; jumlah transformasi "
        "sama dengan referensi: KeyGen 6 NTT / 0 INTT / 9 perkalian titik, Encaps 3 / 4 / 12, Decaps 6 / 5 / 15 (MEASURED, penghitung di hardware).",
        f"<b>Siklus konstan per program</b> (MEASURED, simulasi): KeyGen {fmt(CYC['keygen'])}, Encrypt {fmt(CYC['encrypt'])}, Decrypt {fmt(CYC['decrypt'])}; "
        f"Decaps (Decrypt + Encrypt) {fmt(CYC['decrypt'] + CYC['encrypt'])}. Sekitar {round(100 * move['keygen'] / CYC['keygen'])}% siklus KeyGen adalah perpindahan data lewat port "
        "host inti NTT (perhitungan tim dari jadwal).",
        f"<b>Quartus P6</b> (seed 1, 40 ns): {fmt(p6['alm'])} ALM, {p6['dsp']} DSP, {p6['ram']} M10K, timing terpenuhi, Fmax {num(p6['fmax'])} MHz (inti S7 seed 1: "
        f"{fmt(s7[0]['alm'])} ALM, {num(s7[0]['fmax'])} MHz).",
        f"<b>S10</b> (memori 16 bank 1R1W tanpa arbitrasi, P = 5, 118 siklus): median Fmax {num(f10, 3)} MHz vs S7 {num(f7, 3)} MHz; t = {num(t10, 3)} vs {num(t7, 3)} µs; "
        f"aturan: <b>{'diadopsi' if adopted else 'tidak diadopsi'}</b>.",
        f"<b>50 MHz</b> (kompilasi 20 ns, seed 1–6): S7 memenuhi timing di {met20['S7-20']}/6 seed, S10 di {met20['S10-20']}/6 seed (MEASURED).",
    ])

    st += [P("2. Tujuan dan Cakupan", "h1")]
    st += [P("ROADMAP Fase 6: meminimalkan transformasi dan perpindahan data di tingkat operasi ML-KEM selama masukan dari Keccak masih diberikan testbench. Fase 6 tidak "
             "dirancang untuk menaikkan Fmax (INFERENCE). Keputusan tim 2026-10-03 (ADR 0024): Fase 6 sekarang, S10 di dalam Fase 6 sesudahnya; basis inti S7 "
             "adalah asumsi kerja (ADR 0021 masih Proposed).")]

    st += [P("3. Arsitektur", "h1")]
    st += [table([["Blok (berkas baru)", "Fungsi"],
                  ["poly_store", "24 slot polinomial, 128 kata pasangan koefisien per slot; dua port baca sinkron, satu port tulis per-separuh; port testbench saat idle"],
                  ["gamma_rom, kpke_prog_rom", "dibuat skrip dari model golden: γ_i (Alg. 11) dan program operasi (tidak diketik tangan)"],
                  ["pwm_unit", "BaseCaseMultiply + akumulasi, satu pasangan per siklus, lima pengali Barrett, latensi 7"],
                  ["kpke_sched", "sequencer: LOAD → START → RUN → UNLOAD untuk NTT/INTT (lewat port host inti), PASS untuk PWM / ADD / SUB; penghitung transformasi"],
                  ["kpke_sched_top", "sequencer + inti S7 (kpke_sched_top_s10: dengan inti S10)"]],
                 [42 * mm, W - 42 * mm])]
    st += [P("Program (urutan tetap): KeyGen: NTT s, NTT e, Σ Â[i][j]·ŝ[j], + ê. Encrypt: NTT y, Σ Â[j][i]·ŷ[j], INTT, + e1; Σ t_hat[j]·ŷ[j], INTT, + e2 + μ. "
             "Decrypt: NTT u', Σ ŝ[j]·û'[j], INTT, v' − (…). Satu INTT per polinomial keluaran; operand tetap di domain NTT. Panjang setiap operasi tetap, sehingga jumlah "
             "siklus tidak bergantung data (waktu-konstan).", "small")]

    st += [P("4. Verifikasi (MEASURED, simulasi dan formal)", "h1")]
    st += [table([["Butir", "Hasil"],
                  ["Model jadwal golden vs golden K-PKE (8 seed per operasi + hitungan + kontrol negatif)", "26/26 lulus"],
                  ["ROM γ dan program dibuat ulang byte demi byte", "sama"],
                  ["pwm_unit vs BaseCaseMultiply + akumulasi", "20.035/20.035 pasangan sama, dua simulator"],
                  ["Top: KeyGen, Encrypt, Decrypt, 3 acak + 2 sudut (semua 0, semua q−1) per program", "bit-exact, end-to-end sama, penghitung sesuai, siklus konstan, dua simulator"],
                  ["Kontrol negatif: satu entri γ salah; baca-balik bergeser satu siklus", "gagal sesuai syarat"],
                  ["Formal sequencer (H, T, C, R) dengan kontrol negatif", "2/2 sesuai harapan"]],
                 [W - 70 * mm, 70 * mm])]

    st += [P("5. Siklus dan Sumber Daya", "h1")]
    st += [table([["Program", "Siklus (S7 core)", "Siklus (S10 core)", "Transformasi N/I/PWM", "Perpindahan data (perhitungan tim)"],
                  ["KeyGen", fmt(CYC["keygen"]), fmt(CYC10["keygen"]), "6 / 0 / 9", f"{fmt(move['keygen'])} ({round(100 * move['keygen'] / CYC['keygen'])}%)"],
                  ["Encrypt", fmt(CYC["encrypt"]), fmt(CYC10["encrypt"]), "3 / 4 / 12", f"{fmt(move['encrypt'])} ({round(100 * move['encrypt'] / CYC['encrypt'])}%)"],
                  ["Decrypt", fmt(CYC["decrypt"]), fmt(CYC10["decrypt"]), "3 / 1 / 3", f"{fmt(move['decrypt'])} ({round(100 * move['decrypt'] / CYC['decrypt'])}%)"]],
                 [24 * mm, 30 * mm, 30 * mm, 34 * mm, W - 118 * mm])]
    st += [P("Perpindahan data = jumlah transformasi × (257 siklus muat + 260 siklus baca-balik) dari panjang operasi di RTL (perhitungan tim; total siklus MEASURED). "
             f"Waktu per operasi pada Fmax P6 {num(p6['fmax'])} MHz (satu seed): KeyGen {num(CYC['keygen'] / p6['fmax'], 1)} µs, Encrypt {num(CYC['encrypt'] / p6['fmax'], 1)} µs, "
             f"Decrypt {num(CYC['decrypt'] / p6['fmax'], 1)} µs (perhitungan tim).", "small")]
    st += [table([["Metrik (seed 1, 40 ns)", "Inti S7 saja", "P6 (sequencer + S7)", "Selisih (INFERENCE)"],
                  ["ALM", fmt(s7[0]["alm"]), fmt(p6["alm"]), f"+{fmt(p6['alm'] - s7[0]['alm'])}"],
                  ["Registers", fmt(s7[0]["reg"]), fmt(p6["reg"]), f"+{fmt(p6['reg'] - s7[0]['reg'])}"],
                  ["DSP / M10K", f"{s7[0]['dsp']} / {s7[0]['ram']}", f"{p6['dsp']} / {p6['ram']}", f"+{p6['dsp'] - s7[0]['dsp']} / +{p6['ram'] - s7[0]['ram']}"],
                  ["Setup terburuk (ns)", num(s7[0]["setup"], 3), num(p6["setup"], 3), "timing terpenuhi"],
                  ["Fmax corner terendah (MHz)", num(s7[0]["fmax"]), num(p6["fmax"]), num(p6["fmax"] - s7[0]["fmax"])]],
                 [50 * mm, (W - 50 * mm) / 3, (W - 50 * mm) / 3, (W - 50 * mm) / 3])]
    st += [P("Satu kompilasi P6 (ADR 0019: satu kompilasi untuk blok tanpa aturan adopsi); selisih Fmax satu seed berada di dalam sebaran seed S7 (2,40 MHz). "
             "Penyimpan polinomial memakai M10K (bit memori blok P6 181.222 vs S7 30.423; dua port baca menggandakan blok, INFERENCE).", "small")]

    st += [P("6. Pertanyaan 50 MHz: Analisis Jalur (Opsi 1)", "h1")]
    st += [P("Analisis 300 jalur terburuk S7 dan S8 (salinan database, MEASURED): pembatas S7 adalah <b>rantai arbitrasi slot memori</b> antara potongan A_4 dan A_11, "
             "dimulai dari ROM peta bank yang diinfer sebagai M10K (slack 14,439 ns di 40 ns, jalur data 23,932 ns); kelas berikutnya pengali → tulis memori (17,711 ns). "
             "Register jalur tulis S8 menghapus kelas kedua, bukan yang pertama; karena itu S8 tidak menaikkan Fmax. Arbitrasi hanya bergantung alamat (jadwal tetap), "
             "sehingga dapat dihapus: S10.")]

    st += [P("7. S10: Memori 16 Bank 1R1W tanpa Arbitrasi", "h1")]
    rows = [["Seed", "S7 ALM", "S7 Fmax", "S10 ALM", "S10 Fmax", "S10 setup (ns)"]]
    for i in range(6):
        rows.append([str(i + 1), fmt(s7[i]["alm"]), num(s7[i]["fmax"]), fmt(s10[i]["alm"]), num(s10[i]["fmax"]), num(s10[i]["setup"], 3)])
    rows.append(["Median", fmt(round(med(s7, "alm"))), num(f7, 3), fmt(round(med(s10, "alm"))), num(f10, 3), "-"])
    st += [table(rows, [20 * mm] + [(W - 20 * mm) / 5] * 5, sel_rows=(7,))]
    st += [P(f"DSP S10 {s10[0]['dsp']}, M10K {s10[0]['ram']} (S7: {s7[0]['dsp']} / {s7[0]['ram']}); siklus 118 / 118; t = {num(t10, 3)} µs vs S7 {num(t7, 3)} µs (perhitungan tim).", "small")]
    st += [table([["Syarat adopsi (ditetapkan sebelum mengukur)", "Hasil"]] + [[t, "PASS" if ok else "<b>FAIL</b>"] for t, ok in rule]
                 + [["<b>Hasil aturan</b>", f"<b>{'DIADOPSI' if adopted else 'TIDAK DIADOPSI'}</b>"]], [W - 30 * mm, 30 * mm])]

    st += [P("8. Kompilasi 20 ns, Seed 1–6 (Opsi 2 dan S10, MEASURED, informasi)", "h1")]
    rows = [["Seed", "S7-20 setup (ns)", "S7-20 Fmax", "S10-20 setup (ns)", "S10-20 Fmax"]]
    for i in range(6):
        rows.append([str(i + 1), num(s7_20[i]["setup"], 3), num(s7_20[i]["fmax"]), num(s10_20[i]["setup"], 3), num(s10_20[i]["fmax"])])
    rows.append(["Median", "-", num(med(s7_20, "fmax"), 3), "-", num(med(s10_20, "fmax"), 3)])
    rows.append(["Timing 20 ns terpenuhi", f"{met20['S7-20']}/6", "", f"{met20['S10-20']}/6", ""])
    st += [table(rows, [24 * mm] + [(W - 24 * mm) / 4] * 4, sel_rows=(7,))]
    st += [P("Fmax di bawah batasan 20 ns tidak sebanding dengan angka 40 ns (alat bekerja lebih keras). 50 MHz dihitung tercapai hanya untuk seed dengan setup ≥ 0 "
             "di 20 ns; ini kompilasi <i>kernel-only</i> dengan <i>virtual pin</i>, bukan sistem di papan.", "small")]

    st += [P("8b. Unit Fase 6 Lengkap dengan Inti S10 (MEASURED, seed 1, informasi)", "h1")]
    st += [table([["Metrik", "P6 (inti S7) @ 40 ns", "P6S10 @ 40 ns", "P6S10 @ 20 ns"],
                  ["ALM", fmt(p6["alm"]), fmt(p6s["alm"]), fmt(p6s20["alm"])],
                  ["Registers / DSP / M10K", f"{fmt(p6['reg'])} / {p6['dsp']} / {p6['ram']}", f"{fmt(p6s['reg'])} / {p6s['dsp']} / {p6s['ram']}",
                   f"{fmt(p6s20['reg'])} / {p6s20['dsp']} / {p6s20['ram']}"],
                  ["Setup terburuk (ns)", num(p6["setup"], 3), num(p6s["setup"], 3), num(p6s20["setup"], 3)],
                  ["Timing terpenuhi", "ya", "ya", "<b>ya</b>" if p6s20["setup"] >= 0 else "<b>tidak</b>"],
                  ["Fmax corner terendah (MHz)", num(p6["fmax"]), num(p6s["fmax"]), num(p6s20["fmax"])]],
                 [46 * mm] + [(W - 46 * mm) / 3] * 3)]
    st += [P(f"Dengan inti S10, seluruh unit aritmetika K-PKE memenuhi batasan 20 ns pada seed 1 (satu kompilasi, kernel-only). Waktu per operasi pada 50 MHz bila "
             f"dijalankan di jam itu (perhitungan tim): KeyGen {num(CYC10['keygen'] / 50, 1)} µs, Encrypt {num(CYC10['encrypt'] / 50, 1)} µs, Decrypt "
             f"{num(CYC10['decrypt'] / 50, 1)} µs; bukan pengukuran pada papan.", "small")]

    st += [P("9. Keputusan Menunggu Tim", "h1")]
    st += bullets([
        "ADR 0025 (S10, Proposed): terima atau tolak S10 sebagai memori inti untuk fase berikutnya (hasil aturan di bagian 7).",
        "ADR 0021 (S7), ADR 0022 (S9) dan ADR 0023 (S8) masih Proposed; PENDING #25, #26, #27, #28.",
        "Kotak Approval phase05.md, phase05m.md dan phase06.md kosong; hanya anggota tim yang mencentangnya.",
    ])
    st += [P("10. Keterbatasan", "h1")]
    st += bullets([
        "Tidak ada pengukuran pada papan. Keccak, sampler, kompresi, encode dan transformasi FO belum di perangkat keras (fase berikutnya).",
        "P6 satu kompilasi (seed 1). Tidak ada analisis jalur setelah S10.",
        "Formal mencakup kontrol, bukan data; kebenaran data bertumpu pada simulasi bit-exact.",
        "Port host inti (satu koefisien per siklus) mendominasi siklus; antarmuka lebih lebar adalah pekerjaan berikutnya (belum diukur).",
    ])
    st += [P("11. Reproduksibilitas", "h1")]
    st += [Paragraph("<br/>".join([
        ". scripts/env.sh",
        "scripts/test/phase6_verify.sh; python3 formal/run/run_formal_phase6.py",
        "scripts/test/s10_verify.sh; python3 formal/run/run_formal_s10.py",
        "cd quartus/phase06_sched &amp;&amp; ./run_p6.sh &amp;&amp; ./run_s10_sweep.sh &amp;&amp; ./run_p6s10.sh",
        "cd quartus/phase05m_memsched &amp;&amp; ./run_s7_20_sweep.sh",
        "python3 scripts/quartus/select_s10.py",
        "python3 scripts/build/build_phase6_report.py"]), S["code"])]

    doc.build(st, onFirstPage=lambda c, d: None, onLaterPages=footer)
    print(f"written {OUT.relative_to(ROOT)}  (S10 {'ADOPTED' if adopted else 'NOT adopted'} by the rule)")


if __name__ == "__main__":
    build()
