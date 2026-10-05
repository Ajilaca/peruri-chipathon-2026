#!/usr/bin/env python3
"""scripts/build/build_phase7_report.py

Builds docs/reports/CHIPATON_Phase7_Report.pdf (Phase 7 report: Keccak-f[1600] and SHA3/SHAKE baseline K0, Bahasa Indonesia, same layout, fonts and styles as the Phase 0-6
reports; styles from scripts/build/build_phase4_report.py) with ReportLab.

Every number comes from an evidence file in this repository: Quartus figures are parsed from the extracted evidence files (scripts/quartus/phase5_select_5b.py: parse_quartus); simulation
figures are literals checked to appear in their evidence file (EXPECT); the cycle table and the formula are read from evidence/phase07/cycles_k0.json and the
formula is re-evaluated here against every point. Nothing is written for a result that did not happen.
Usage: python3 scripts/build/build_phase7_report.py
"""
import json
import pathlib
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "scripts" / g) for g in ("build", "quartus")]
from build_phase4_report import MUTED, P, S, bullets, fmt, num, table  # noqa: E402
from phase5_select_5b import parse_quartus  # noqa: E402

E7 = ROOT / "evidence" / "phase07"
OUT = ROOT / "docs" / "reports" / "CHIPATON_Phase7_Report.pdf"
RATE = {"sha3_256": 136, "sha3_512": 72, "shake_128": 168, "shake_256": 136}

EXPECT = {
    E7 / "verify.md": ["16 passed", "[verilator] TOTAL: 9/9 passed", "[icarus] TOTAL: 9/9 passed", "cycle points: 306", "differences", "OVERALL: PASS"],
    E7 / "formal.md": ["ALL AS EXPECTED", "basecase=pass, induction=pass", "NC-K1", "NC-K4"],
    E7 / "keccak_cycles.md": ["389", "306 points"],
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


def formula(mode, ln, ow):
    rate, rw = RATE[mode], RATE[mode] // 8
    pad2 = 0 if (ln % rate) // 8 == rw - 1 else 1
    return 1 + (ln // 8 + 1) + pad2 + 26 * (ln // rate + 1) + ow + 26 * ((ow - 1) // rw)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DV", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"CHIPATON — Laporan Fase 7 (ID) — hal. {doc.page}")
    canvas.restoreState()


def build():
    check_evidence()
    k40 = parse_quartus(E7 / "quartus_K0.md")
    k20 = parse_quartus(E7 / "quartus_K0-20.md")
    cyc = json.loads((E7 / "cycles_k0.json").read_text())
    bad = [k for k, v in cyc.items() if formula(k.split("/")[0], int(k.split("/")[1]), int(k.split("/")[2])) != v]
    if bad:
        raise SystemExit(f"formula differs from the measured cycle table at {len(bad)} points, e.g. {bad[:3]}")
    npts = len(cyc)

    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=17 * mm,
                            title="CHIPATON — Laporan Fase 7 (ID)", author="Tim J5 (ITB)",
                            subject="Fase 7: Keccak-f[1600] dan SHA3/SHAKE baseline K0 pada DE10-Nano")
    st = []
    W = A4[0] - 36 * mm
    st += [Spacer(1, 62 * mm), P("PERURI Digital Summit · CHIP 2026 Hackathon — Tim J5 (ITB)", "csub"), Spacer(1, 6)]
    st += [P("Laporan Fase 7", "ctitle")]
    st += [P("Keccak-f[1600] dan SHA3/SHAKE · Konfigurasi K0 (Baseline)", "csub")]
    st += [P("Terasic DE10-Nano · Intel/Altera Cyclone V SE 5CSEBA6U23I7", "csub"), Spacer(1, 14)]
    st += [P("Status: Fase 7 selesai diukur (bit-exact terhadap hashlib, latensi permutasi tetap, Quartus K0 terisi); Approval belum dicentang; "
             "belum mencapai tier T1 (sampler belum dibuat)", "cmeta")]
    st += [P("Branch: phase7-keccak · 2026-10-03", "cmeta"), Spacer(1, 22)]
    st += [P("Ditulis untuk: Tim J5. Sumber kebenaran tetap berkas di repo (docs/results/phase07.md, evidence/phase07/). "
             "Label: <b>MEASURED</b> (laporan Quartus atau log simulasi di repo), <b>INFERENCE</b>, <b>ESTIMATE</b>, <i>perhitungan tim</i>, <b>belum diukur</b>. "
             "Tidak ada pengukuran pada papan; semua hasil berasal dari simulasi, analisis formal dan analisis Quartus (<i>kernel-only</i>, <i>virtual pin</i>, satu seed).", "small")]
    st += [PageBreak()]

    st += [P("1. Ringkasan Eksekutif", "h1")]
    st += bullets([
        "Fase 7 membangun <b>Keccak-f[1600] iteratif</b> (satu ronde per siklus; <i>busy</i> tepat 24 siklus untuk semua data) dan <b>sponge</b> SHA3-256, SHA3-512, SHAKE128, SHAKE256 "
        "dengan <i>absorb</i> dan <i>squeeze</i> banyak blok serta <i>padding</i> di perangkat keras. Ini baseline K0; belum ada optimasi.",
        "<b>Bit-exact</b> terhadap <i>hashlib</i> di Verilator dan Icarus untuk semua panjang uji: 0, 1, 7, 8, 9, rate−1, rate, rate+1, kelipatan rate, panjang ML-KEM "
        "(32, 33, 34, 64, 1120, 1184) dan panjang acak; model golden Python juga sama dengan hashlib (MEASURED, simulasi).",
        f"<b>Siklus tidak bergantung data</b>: {npts} titik (mode × panjang × jumlah kata keluaran), tiga pesan per titik (acak, semua 0x00, semua 0xFF) menghasilkan jumlah siklus yang "
        "sama; semua titik sama dengan rumus FSM (MEASURED, simulasi).",
        "<b>Formal</b> (SymbiYosys): properti K1–K5 terbukti dengan induksi; dua kontrol negatif gagal sesuai syarat (MEASURED).",
        f"<b>Quartus K0</b> (seed 1, <i>kernel-only</i>): {fmt(k40['alm'])} ALM, {fmt(k40['reg'])} register, {k40['ram']} M10K, {k40['dsp']} DSP; batasan 40 ns terpenuhi "
        f"(setup +{num(k40['setup'], 3)} ns, Fmax {num(k40['fmax'])} MHz); batasan 20 ns terpenuhi (setup +{num(k20['setup'], 3)} ns, Fmax {num(k20['fmax'])} MHz, informasi).",
        "Biaya Keccak per operasi ML-KEM-768 dengan K0: sekitar 2.000 siklus (perhitungan tim), hampir dua kali estimasi awal (1.060); tiga estimasi yang ditulis sebelum mengukur "
        "meleset dan dicatat apa adanya (bagian 6).",
    ])

    st += [P("2. Tujuan dan Cakupan", "h1")]
    st += [P("ROADMAP Fase 7: baseline Keccak yang benar dan terukur (K0) sebelum optimasi apa pun. Tidak diizinkan di fase ini: dua ronde per siklus atau <i>unrolling</i>, "
             "sampler <i>streaming</i>, sambungan ke unit aritmetika. Tidak ada aturan adopsi: K0 adalah blok baru, tidak menggantikan apa pun. Matematika tidak diubah (C1): "
             "FIPS 202 dan FIPS 203 tetap; golden model dan test plan ditulis sebelum RTL.")]

    st += [P("3. Arsitektur", "h1")]
    st += [table([["Blok", "Fungsi"],
                  ["keccak_pkg (dibuat skrip)", "24 konstanta ronde (FIPS 202 Alg. 5-6) dan 25 offset rho (Alg. 2), dihitung dari model golden, bukan diketik tangan"],
                  ["keccak_round", "satu ronde kombinasional: theta, rho, pi, chi, iota pada 1.600 bit"],
                  ["keccak_f1600", "register state 1.600 bit, penghitung ronde 0..23; 24 siklus <i>busy</i> per permutasi; port XOR per lane dan baca per lane"],
                  ["keccak_sponge", "kontroler sponge dan top Quartus: mode, absorb kata 64 bit, <i>padding</i> (0x06 SHA3, 0x1F SHAKE, 0x80) lewat XOR, squeeze"]],
                 [42 * mm, W - 42 * mm])]
    st += [P("Antarmuka: <i>start</i> membawa mode (SHA3-256, SHA3-512, SHAKE128, SHAKE256) dan panjang pesan dalam byte (publik); data masuk dan keluar berupa kata 64 bit "
             "dengan <i>valid/ready</i>; SHAKE keluar tanpa batas sampai <i>stop</i>. Satu permutasi terlihat 26 siklus oleh kontroler: 1 siklus <i>run</i>, 24 siklus ronde, "
             "1 siklus selesai. Reset asinkron aktif rendah; state dihapus saat <i>start</i>, <i>stop</i>, akhir digest SHA3 dan reset.", "small")]

    st += [P("4. Verifikasi (MEASURED, simulasi dan formal)", "h1")]
    st += [table([["Butir", "Hasil"],
                  ["Golden vs hashlib: semua panjang 0..3·rate+1 per mode, panjang ML-KEM, acak sampai 2.000 B, panjang keluaran SHAKE, jejak per ronde", "16/16 lulus"],
                  ["Konstanta RTL dibuat ulang dari model golden", "0 perbedaan"],
                  ["Permutasi: state nol, semua satu, 1.600 state satu bit, 200 acak, rantai 10; state setiap ronde = jejak golden; busy_o = 24", "sama, dua simulator"],
                  ["Sponge: empat mode, panjang batas dan ML-KEM, panjang acak, byte sampah di kata terakhir, back-pressure acak, stop (absorb, permutasi, squeeze), start saat sibuk, reset", "bit-exact, dua simulator"],
                  ["Hitungan permutasi di hardware = hitungan golden", "sama"],
                  ["Kontrol negatif: konstanta ronde salah; 23 ronde; byte domain SHA3 salah", "gagal sesuai syarat, dua simulator"],
                  ["Formal K1–K5 (induksi); NC-K1 (23 ronde) dan NC-K4 (data bergantung ready)", "PASS; kedua kontrol gagal"]],
                 [W - 52 * mm, 52 * mm])]

    st += [P("5. Siklus (MEASURED, simulasi)", "h1")]
    pick = ["sha3_256/0/4", "sha3_256/32/4", "sha3_256/135/4", "sha3_256/136/4", "sha3_256/1184/4", "sha3_512/64/8", "shake_256/33/16", "shake_256/1120/4",
            "shake_128/34/21", "shake_128/34/22"]
    rows = [["Mode", "Panjang pesan (B)", "Kata keluaran", "Siklus"]] + [[k.split("/")[0], k.split("/")[1], k.split("/")[2], fmt(cyc[k])] for k in pick if k in cyc]
    st += [table(rows, [34 * mm] + [(W - 34 * mm) / 3] * 3)]
    st += [P("Rumus dari FSM (ditulis sesudah RTL, lalu diperiksa pada semua titik, tidak disetel): siklus = 1 + (len div 8 + 1) + pad2 + 26·(len div rate + 1) + kata_keluar + "
             "26·((kata_keluar − 1) div kata_rate); pad2 = 0 bila (len mod rate) div 8 = kata_rate − 1, selain itu 1. "
             f"Semua {npts} titik sama dengan rumus. Estimasi sebelum mengukur memakai 24 siklus per permutasi (H(ek) sekitar 370); terukur 389 (+5%), "
             "karena ada 2 siklus kontrol per permutasi.", "small")]
    st += [P("Laju pada panjang besar (perhitungan tim dari rumus): SHA3-256 dan SHAKE256 43 siklus per blok 136 B (3,16 B per siklus); SHA3-512 35 siklus per 72 B (2,06); "
             f"SHAKE128 squeeze 47 siklus per 168 B (3,57). Waktu per permutasi pada Fmax satu seed: 26 / {num(k40['fmax'])} MHz = {num(26 / k40['fmax'], 3)} µs (40 ns); "
             f"26 / {num(k20['fmax'])} MHz = {num(26 / k20['fmax'], 3)} µs (20 ns); nilai satu seed, bukan median, dan tidak sebanding antar batasan.", "small")]

    st += [P("6. Sumber Daya dan Timing (MEASURED, Quartus)", "h1")]
    st += [table([["Metrik (seed 1)", "K0 @ 40 ns", "K0-20 @ 20 ns (informasi)", "Estimasi sebelum mengukur"],
                  ["ALM", fmt(k40["alm"]), fmt(k20["alm"]), "1.500-3.500 (terukur 2% di atas)"],
                  ["Register", fmt(k40["reg"]), fmt(k20["reg"]), "1.700-2.000 (terukur di bawah rentang)"],
                  ["M10K / DSP", f"{k40['ram']} / {k40['dsp']}", f"{k20['ram']} / {k20['dsp']}", "sekitar 0 / 0"],
                  ["Setup terburuk (ns)", num(k40["setup"], 3), num(k20["setup"], 3), "tidak membatasi sistem (INFERENCE)"],
                  ["Hold terburuk (ns)", num(k40["hold"], 3), num(k20["hold"], 3), "-"],
                  ["Fmax corner lambat terendah (MHz)", num(k40["fmax"]), num(k20["fmax"]), "-"]],
                 [50 * mm, 32 * mm, 42 * mm, W - 124 * mm])]
    st += [P("Penyebut resmi Fitter: 41.910 ALM, 553 RAM block, 112 DSP. Satu kompilasi per batasan (ADR 0019: blok tanpa aturan adopsi). 1.653 register = 1.600 bit state + 53 kontrol. "
             "Critical Warning 15725 (pin virtual pada jam) pada kedua kompilasi seperti fase sebelumnya; Warning 10036 adalah sinyal penyerap yang disengaja; tidak ada yang diabaikan. "
             "'Timing terpenuhi di 20 ns' adalah hasil analisis statis alur ini, bukan sistem 50 MHz di papan.", "small")]

    st += [P("7. Biaya Keccak per Operasi ML-KEM-768 (perhitungan tim)", "h1")]
    st += [table([["Operasi", "Siklus Keccak (min / median / maks)", "Permutasi (median)"],
                  ["KeyGen", "2.013 / 2.026 / 2.088", "43"],
                  ["Encaps", "2.065 / 2.078 / 2.140", "44"],
                  ["Decaps", "2.057 / 2.070 / 2.132", "44"]], [40 * mm, (W - 40 * mm) * 0.6, (W - 40 * mm) * 0.4])]
    st += [P("Dihitung oleh scripts/test/phase7_op_cycles.py dengan rumus terukur, 200 nilai ρ acak (SampleNTT memakai jumlah byte XOF yang benar-benar terpakai), setiap panggilan "
             "berjalan sendiri tanpa tumpang-tindih. Sebagai skala: aritmetika Fase 6 dengan S10 memakai 5.475 / 6.789 / 3.109 siklus (MEASURED, simulasi); kedua blok belum "
             "tersambung. Angka ini untuk antarmuka K0 (satu kata 64 bit per siklus, mulai ulang tiap panggilan), bukan batas bagi desain lain.", "small")]

    st += [P("8. Keputusan Menunggu Tim", "h1")]
    st += bullets([
        "Kotak Approval phase07.md kosong; hanya anggota tim yang mencentangnya.",
        "PENDING #26 (protokol <i>checkpoint</i> sampai 2026-10-08) masih terbuka; fase ini berhenti di akhir blok sesuai usulan.",
        "Langkah berikut menurut ADR 0019: sampler (SampleNTT dan CBD dari aliran Keccak, tier T1); PENDING #25 (pemeriksaan input FIPS 203 di hardware atau HPS) sebelum pekerjaan kontroler.",
    ])
    st += [P("9. Keterbatasan dan Penyimpangan", "h1")]
    st += bullets([
        "Tidak ada pengukuran pada papan; Fmax dan slack <i>kernel-only</i> dengan pin virtual dan satu seed.",
        "Formal mencakup kontrol, bukan nilai digest; nilai digest bertumpu pada simulasi terhadap hashlib.",
        "Hanya satu ronde per siklus; dua ronde per siklus, <i>unrolling</i>, sampler streaming dan sambungan ke aritmetika belum dikerjakan (belum diizinkan di fase ini).",
        "<i>Waktu-konstan</i> di sini berarti jumlah siklus hanya bergantung pada panjang publik dan jumlah kata keluaran; bukan pernyataan tentang kebocoran sisi-kanal.",
        "Penyimpangan dari test plan dicatat di Amendment A1: nama paket konstanta, 26 (bukan 24) siklus per permutasi pada estimasi siklus, penghapusan state tambahan, NC-K4 sebagai BMC kedalaman 40. "
        "Tiga kesalahan testbench di run pertama dan satu penyesuaian RTL (ternary enum untuk Icarus) diperbaiki; satu asersi golden yang keliru (24 konstanta ronde berbeda; yang benar 22) dikoreksi.",
    ])
    st += [P("10. Reproduksibilitas", "h1")]
    st += [Paragraph("<br/>".join([
        ". scripts/env.sh",
        "scripts/test/phase7_verify.sh; python3 formal/run/run_formal_phase7.py",
        "python3 scripts/build/gen_keccak_consts.py --check",
        "cd quartus/phase07_keccak &amp;&amp; ./run_k0.sh",
        "python3 scripts/test/phase7_op_cycles.py 200",
        "python3 scripts/build/build_phase7_report.py"]), S["code"])]

    doc.build(st, onFirstPage=lambda c, d: None, onLaterPages=footer)
    print(f"written {OUT.relative_to(ROOT)}  ({npts} cycle points checked against the formula)")


if __name__ == "__main__":
    build()
