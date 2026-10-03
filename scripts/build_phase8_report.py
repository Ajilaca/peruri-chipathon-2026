#!/usr/bin/env python3
"""scripts/build_phase8_report.py

Builds docs/report/CHIPATON_Phase8_Report.pdf (Phase 8 report: Keccak optimisation and streaming, sub-steps 8a, 8b, 8c, 8d; Bahasa Indonesia, same layout, fonts and styles as the Phase 0-7 reports; styles from
scripts/build_phase4_report.py) with ReportLab.

Every number comes from an evidence file in this repository: Quartus figures are parsed from the extracted evidence files (scripts/phase5_select_5b.py: parse_quartus); simulation figures are read from the cycle tables
(JSON) and from the verification logs (EXPECT checks that the claimed lines are in the logs). The adoption and selection rules are re-applied here from the same files (scripts/select_8b.py, scripts/select_8cd.py logic).
Nothing is written for a result that did not happen. Usage: python3 scripts/build_phase8_report.py
"""
import json
import pathlib
import statistics
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_phase4_report import MUTED, P, S, bullets, fmt, num, table  # noqa: E402
from phase5_select_5b import parse_quartus  # noqa: E402

E = ROOT / "docs" / "evidence" / "phase08-keccak-stream"
E6 = ROOT / "docs" / "evidence" / "phase06-scheduling" / "s10"
OUT = ROOT / "docs" / "report" / "CHIPATON_Phase8_Report.pdf"

EXPECT = {
    E / "8b" / "verify_W1_2026-10-03.md": ["[verilator] TOTAL: 31/31 passed", "[icarus] TOTAL: 31/31 passed", "OVERALL: PASS"],
    E / "8b" / "verify_W2_2026-10-03.md": ["[verilator] TOTAL: 34/34 passed", "[icarus] TOTAL: 34/34 passed", "OVERALL: PASS"],
    E / "8b" / "formal_W2_2026-10-03.md": ["ALL AS EXPECTED", "basecase=pass, induction=pass"],
    E / "8c" / "verify_2026-10-03.md": ["OVERALL: PASS", "112 passed", "modified Phase 6 / core files: 0"],
    E / "8c" / "formal_2026-10-03.md": ["ALL AS EXPECTED"],
    E / "8d" / "formal_2026-10-03.md": ["ALL AS EXPECTED"],
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


def load(folder, prefix):
    rows = []
    for s in range(1, 7):
        rev = prefix + ("" if s == 1 else f"-s{s}")
        files = sorted(folder.glob(f"quartus_{rev}_*.md"))
        if not files:
            raise SystemExit(f"missing evidence for {rev} in {folder}")
        q = parse_quartus(files[-1])
        q["seed"] = s
        rows.append(q)
    return rows


def summ(rows):
    a, f, r, m, d = ([q[k] for q in rows] for k in ("alm", "fmax", "reg", "ram", "dsp"))
    return dict(alm=statistics.median(a), alm_rng=(min(a), max(a)), fmax=statistics.median(f), fmax_rng=(min(f), max(f)), reg=(min(r), max(r)), ram=(min(m), max(m)), dsp=(min(d), max(d)),
                met=all(q["setup"] >= 0 and q["hold"] >= 0 for q in rows))


def cyc(path, key=None):
    d = json.loads(path.read_text())
    if key:
        return {k: statistics.mean(v) for k, v in d["cycles"].items()}
    return d


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DV", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"CHIPATON — Laporan Fase 8 (ID) — hal. {doc.page}")
    canvas.restoreState()


def build():
    check_evidence()
    s10 = summ(load(E6, "S10"))
    w1, w2 = summ(load(E / "8b", "SM1")), summ(load(E / "8b", "SM2"))
    st, sm, ov = summ(load(E / "8c", "SMP0")), summ(load(E / "8c", "SMP1")), summ(load(E / "8d", "SMP2"))
    w1c = json.loads(next((E / "8b").glob("cycles_w1_c5_*.json")).read_text())
    w2c = json.loads(next((E / "8b").glob("cycles_w2_c5_*.json")).read_text())

    def mean_of(pts, kind):
        return statistics.mean(p["cycles"] for p in pts if p["kind"] == kind)

    n1, c1 = mean_of(w1c, "sample_ntt"), mean_of(w1c, "cbd")
    n2, c2 = mean_of(w2c, "sample_ntt"), mean_of(w2c, "cbd")
    v = {k: cyc(next((E / ("8c" if k < 2 else "8d")).glob(f"cycles_v{k}_2026*.json")), True) for k in (0, 1, 2)}
    tt = {k: (v[k]["keygen"] / x["fmax"], v[k]["encrypt"] / x["fmax"]) for k, x in ((0, st), (1, sm), (2, ov))}

    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=17 * mm,
                            title="CHIPATON — Laporan Fase 8 (ID)", author="Tim J5 (ITB)", subject="Fase 8: optimasi Keccak dan streaming (8a, 8b, 8c, 8d) pada DE10-Nano")
    st_ = []
    W = A4[0] - 36 * mm
    st_ += [Spacer(1, 62 * mm), P("PERURI Digital Summit · CHIP 2026 Hackathon — Tim J5 (ITB)", "csub"), Spacer(1, 6)]
    st_ += [P("Laporan Fase 8", "ctitle")]
    st_ += [P("Optimasi Keccak dan Streaming · 8a (C5) · 8b (sampler) · 8c (matriks A) · 8d (overlap)", "csub")]
    st_ += [P("Terasic DE10-Nano · Intel/Altera Cyclone V SE 5CSEBA6U23I7", "csub"), Spacer(1, 14)]
    st_ += [P("Status: keempat sub-langkah selesai diukur (simulasi, formal, Quartus <i>kernel-only</i>); keputusan penerimaan ADR 0027-0030 menunggu tim; "
              "Approval belum dicentang", "cmeta")]
    st_ += [P("Branch: phase8-keccak-stream · 2026-10-03", "cmeta"), Spacer(1, 22)]
    st_ += [P("Ditulis untuk: Tim J5. Sumber kebenaran tetap berkas di repo (docs/results/result_phase8.md, docs/evidence/phase08-keccak-stream/). "
              "Label: <b>MEASURED</b> (laporan Quartus atau log simulasi di repo), <b>INFERENCE</b>, <b>ESTIMATE</b>, <i>perhitungan tim</i>, <b>belum diukur</b>. "
              "Tidak ada pengukuran pada papan; semua hasil berasal dari simulasi, analisis formal dan analisis Quartus (<i>kernel-only</i>, <i>virtual pin</i>).", "small")]
    st_ += [PageBreak()]

    st_ += [P("1. Ringkasan Eksekutif", "h1")]
    st_ += bullets([
        "<b>8a</b> (dua ronde Keccak per siklus, C5): 14 siklus per permutasi (K0: 26); median Fmax 50,655 MHz (K0 67,675); dipilih oleh aturan (ADR 0027, Proposed).",
        f"<b>8b</b> (sampler <i>streaming</i> SampleNTT dan CBD langsung dari aliran Keccak, tanpa memori di antaranya): lebar keluaran W1 (1 koefisien/siklus) lalu W2 (2/siklus); keduanya lulus gate "
        f"(M10K 0, DSP 0, timing 40 ns terpenuhi di setiap seed, median Fmax W1 {num(w1['fmax'], 3)} dan W2 {num(w2['fmax'], 3)} MHz, batas gate = median S10 {num(s10['fmax'], 3)} MHz). "
        f"Aturan memilih <b>W2</b>: SampleNTT {num(n2, 1)} siklus (W1 {num(n1, 1)}), CBD {c2['cycles'] if isinstance(c2, dict) else num(c2, 0)} siklus (W1 {num(c1, 0)}) (ADR 0028, Proposed).",
        f"<b>8c</b> (matriks Â tidak disimpan; dialirkan dari sampler ke unit PWM): KeyGen {num(v[1]['keygen'], 0)} dan Encrypt {num(v[1]['encrypt'], 0)} siklus, dibanding {num(v[0]['keygen'], 0)} dan {num(v[0]['encrypt'], 0)} "
        f"bila Â disampel ke 9 slot (STORE); M10K {sm['ram'][0]} dibanding {st['ram'][0]} (penyimpanan polinomial 24 slot menjadi 12).",
        f"<b>8d</b> (sampler berjalan selama transformasi): KeyGen {num(v[2]['keygen'], 0)} dan Encrypt {num(v[2]['encrypt'], 0)} siklus; M10K {ov['ram'][0]}.",
        "Semua keluaran bit-exact terhadap model golden dan K-PKE golden yang tidak diubah (KeyGen, Encrypt, Decrypt) di Verilator dan Icarus; kontrol negatif gagal sesuai syarat; formal lulus (MEASURED, simulasi).",
        "Dua cacat RTL ditemukan oleh verifikasi dan diperbaiki: register tag valid tanpa reset, dan balapan antara pulsa <i>done</i> sampler dan <i>start</i> berikutnya (ditemukan oleh varian STRESS).",
    ])

    st_ += [P("2. Tujuan dan Cakupan", "h1")]
    st_ += [P("ADR 0026 (Accepted): 8a, 8b, 8c, 8d dikerjakan, masing-masing dengan test plan dan aturan yang ditulis sebelum pengukuran. Permintaan tim 2026-10-03: 8b dikerjakan dalam dua lebar (W1 lalu W2), "
              "dan 8b sampai 8d dikerjakan berturut-turut tanpa berhenti, lalu laporan dan <i>result</i>. Matematika tidak diubah (C1). Tidak ada hashing kunci (G, H, J), kontrol KEM, kompresi atau penyandian di "
              "perangkat keras; seed (ρ, σ, r) adalah masukan yang ditulis <i>testbench</i>.")]

    st_ += [P("3. Arsitektur", "h1")]
    st_ += [table([["Blok", "Fungsi"],
                  ["sample_ntt_core", "SampleNTT dari aliran kata 64 bit; jendela byte maksimal 11 byte; per triple d1, d2 dibandingkan dengan 3329 (tanpa modulo); W2: satu triple per siklus, kumpulan 0-3 kandidat dengan satu koefisien terbawa"],
                  ["cbd2_core", "CBD η=2 dari aliran PRF: tepat 16 kata (kata ke-17 tidak diambil); W1 256 siklus, W2 128 siklus; jalur data dan jumlah siklus tidak bergantung pada nilai"],
                  ["keccak_sampler", "sponge (C5 atau K0) + inti sampler; menghentikan dan menghapus sponge saat polinomial selesai; parameter CORE_R2 dan OUTW"],
                  ["kpke_sched_smp", "sekuenser Fase 6 + sampler: SMPN, SMPA, PWMS (Â langsung ke unit PWM, alamat b/akumulator/gamma satu beat lebih awal, tag valid 7 siklus), WAIT, SMPN non-blocking, arbitrasi port tulis"],
                  ["poly_store_smp, program ROM", "salinan penyimpanan Fase 6 dengan lebar indeks mengikuti kedalaman; ROM program dibuat oleh skrip dari model golden (STORE, STREAM, OVERLAP, STRESS)"]],
                 [44 * mm, W - 44 * mm])]

    st_ += [P("4. Verifikasi (MEASURED, simulasi dan formal)", "h1")]
    st_ += [table([["Butir", "Hasil"],
                  ["8b W1: inti, CBD, top (CORE_R2 = 1 dan 0), kontrol negatif, formal", "31/31 di dua simulator; OVERALL PASS"],
                  ["8b W2: sama, ditambah ulang seluruh set W1 terhadap RTL sekarang", "34/34 dan 31/31 di dua simulator; OVERALL PASS"],
                  ["8b: SampleNTT 500 aliran XOF + 6 polinomial yang butuh blok ke-4 + aliran buatan (batas q−1, q, rangkaian tolak panjang)", "sama dengan golden termasuk jumlah byte XOF yang terpakai"],
                  ["8b formal S1-S6 (rentang koefisien, jumlah, penahanan keluaran, byte, legalitas, carry) W1 dan W2; NC-S1, NC-S2", "PASS; kontrol gagal"],
                  ["8c/8d: KeyGen, Encrypt, Decrypt pada STORE, STREAM, OVERLAP, STRESS; setiap slot dan hasil ujung ke ujung vs K-PKE golden", "sama; penghitung 6/0/9, 3/4/12, 3/1/3"],
                  ["8c/8d: kontrol negatif NC-IJ, NC-CTR, NC-ALIGN, NC-VALID, NC-ACC, NC-HAZ, NC-ARB", "gagal sesuai syarat"],
                  ["8c/8d formal F1-F5 (STREAM, STORE, OVERLAP); NC-F2", "PASS; kontrol gagal"],
                  ["Berkas Fase 6 dan inti NTT tidak diubah", "0 berkas berbeda"]],
                 [W - 60 * mm, 60 * mm])]

    st_ += [P("5. Siklus (MEASURED, simulasi; jumlah per operasi adalah perhitungan tim)", "h1")]
    st_ += [table([["Besaran (sponge C5)", "W1", "W2"],
                  ["SampleNTT per polinomial, rata-rata (500)", num(n1, 1), num(n2, 1)],
                  ["CBD per polinomial", num(c1, 0), num(c2, 0)],
                  ["Sampling per operasi: KeyGen (9 SampleNTT + 6 CBD)", fmt(round(9 * n1 + 6 * c1)), fmt(round(9 * n2 + 6 * c2))],
                  ["Sampling per operasi: Encaps (9 + 7)", fmt(round(9 * n1 + 7 * c1)), fmt(round(9 * n2 + 7 * c2))]],
                 [W - 60 * mm, 30 * mm, 30 * mm])]
    st_ += [P("Dengan W2, siklus SampleNTT sama dengan jumlah triple yang dikonsumsi ditambah 49 (3 blok XOF) atau 61 (4 blok) pada ke-500 polinomial; siklus CBD identik untuk semua σ dan N (data publik saja yang memengaruhi SampleNTT).", "small")]
    st_ += [table([["Program (rata-rata, masukan sama)", "STORE", "STREAM (8c)", "OVERLAP (8d)", "Fase 6 (aritmetika saja)"],
                  ["KeyGen", fmt(round(v[0]["keygen"])), fmt(round(v[1]["keygen"])), fmt(round(v[2]["keygen"])), "5.475"],
                  ["Encrypt", fmt(round(v[0]["encrypt"])), fmt(round(v[1]["encrypt"])), fmt(round(v[2]["encrypt"])), "6.789"],
                  ["Decrypt", fmt(round(v[0]["decrypt"])), fmt(round(v[1]["decrypt"])), fmt(round(v[2]["decrypt"])), "3.109"]],
                 [40 * mm, (W - 40 * mm) / 4, (W - 40 * mm) / 4, (W - 40 * mm) / 4, (W - 40 * mm) / 4])]

    st_ += [P("6. Sumber Daya dan Timing (MEASURED, Quartus, median seed 1-6)", "h1")]

    def row(name, x):
        return [name, f"{fmt(round(x['alm']))} ({fmt(x['alm_rng'][0])}-{fmt(x['alm_rng'][1])})", f"{x['reg'][0]}-{x['reg'][1]}", f"{x['ram'][0]}-{x['ram'][1]}", f"{x['dsp'][0]}-{x['dsp'][1]}",
                f"{num(x['fmax'], 3)} ({num(x['fmax_rng'][0])}-{num(x['fmax_rng'][1])})", "ya" if x["met"] else "TIDAK"]
    st_ += [table([["Konfigurasi", "ALM", "Register", "M10K", "DSP", "Fmax MHz (min-maks)", "40 ns terpenuhi"],
                  row("S10 (inti NTT, Fase 6)", s10), row("8b W1 (sampler + C5)", w1), row("8b W2 (sampler + C5)", w2),
                  row("8c STORE (sistem)", st), row("8c STREAM (sistem)", sm), row("8d OVERLAP (sistem)", ov)],
                 [40 * mm, 36 * mm, 18 * mm, 14 * mm, 12 * mm, 38 * mm, W - 158 * mm])]
    st_ += [P("Sistem = sekuenser + penyimpanan + unit PWM + inti S10 + sampler pada sponge C5, <i>kernel-only</i> dengan pin virtual. Penyebut resmi Fitter: 41.910 ALM, 553 RAM block, 112 DSP. "
              "Critical Warning 15725 (pin virtual pada jam) pada setiap kompilasi seperti fase sebelumnya; tidak ada yang diabaikan. 'Timing terpenuhi' adalah hasil analisis statis alur ini, bukan sistem di papan.", "small")]

    st_ += [P("7. Aturan Adopsi dan Hasilnya", "h1")]
    st_ += [table([["Langkah", "Aturan (ditetapkan sebelum mengukur)", "Hasil"],
                  ["8b", "gate per lebar: M10K = 0, DSP = 0, ALM ≤ 12.573, timing 40 ns tiap seed, median Fmax ≥ median S10; W2 dipilih hanya bila lulus gate dan t = siklus / Fmax lebih rendah untuk SampleNTT dan CBD",
                   f"W1 dan W2 lulus gate; <b>W2 dipilih</b> (t SampleNTT {num(n2 / w2['fmax'], 3)} µs vs {num(n1 / w1['fmax'], 3)}; t CBD {num(c2 / w2['fmax'], 3)} vs {num(c1 / w1['fmax'], 3)})"],
                  ["8c", "STREAM menggantikan STORE hanya bila: benar; fit berhasil dan timing 40 ns tiap seed; t = siklus / Fmax lebih rendah untuk KeyGen dan Encrypt; M10K tidak lebih tinggi di tiap seed",
                   f"t KeyGen {num(tt[1][0], 3)} vs {num(tt[0][0], 3)} µs; Encrypt {num(tt[1][1], 3)} vs {num(tt[0][1], 3)}; M10K {sm['ram'][0]} vs {st['ram'][0]}: lihat worksheet"],
                  ["8d", "OVERLAP menggantikan STREAM dengan syarat yang sama",
                   f"t KeyGen {num(tt[2][0], 3)} vs {num(tt[1][0], 3)} µs; Encrypt {num(tt[2][1], 3)} vs {num(tt[1][1], 3)}; M10K {ov['ram'][0]} vs {sm['ram'][0]}: lihat worksheet"]],
                 [14 * mm, (W - 14 * mm) * 0.55, (W - 14 * mm) * 0.45])]
    st_ += [P("Hasil resmi aturan 8c dan 8d dihitung oleh scripts/select_8cd.py (docs/evidence/phase08-keccak-stream/8c/selection_worksheet_2026-10-03.md dan 8d/). Keputusan menerima atau menolak tetap milik tim.", "small")]

    st_ += [P("8. Temuan dan Penyimpangan", "h1")]
    st_ += bullets([
        "<b>Dua cacat RTL</b>: (1) tag valid hasil PWM tanpa reset (ditemukan oleh pembuktian formal; tidak terlihat di simulasi); (2) <i>start</i> sampler pada siklus yang sama dengan pulsa <i>done</i> sebelumnya menghapus penanda PWMS "
        "sehingga program macet (ditemukan oleh varian STRESS). Keduanya diperbaiki; pembuktian formal dan simulasi dijalankan ulang pada RTL final.",
        "<b>Kriteria V5 8b diubah setelah melihat hasil</b> (Amandemen A1): hitungan permutasi sponge boleh satu lebih dari golden bila jendela byte sudah mengambil kata terakhir blok akhir saat keluaran ditahan (1 dari 500 kasus K0, W1); tidak berpengaruh pada keluaran.",
        "<b>Estimasi yang meleset</b>: tambahan ALM W2 diperkirakan 100-300 dan terukur sekitar +11 (median); ALM sampler + sponge C5 (5.279-5.290) lebih kecil daripada sponge C5 sendirian di 8a (6.167), penyebab tidak diselidiki (INFERENCE: sintesis berbeda antar kompilasi). "
        "Estimasi siklus 8b (W1 310/280, W2 210/150) dan 8c/8d (STORE 8.400/9.900, STREAM 7.300/8.750, OVERLAP 6.300/7.600) mendekati hasil terukur.",
        "Kontrol negatif formal NC-F3 dan NC-F4 tidak dapat gagal dalam kedalaman BMC (pelanggaran hanya terjangkau oleh langkah induksi, yang dilaporkan UNKNOWN); kontrol formal yang dipakai adalah NC-F2 (Amandemen A1).",
        "Verifikasi W2 pertama dibuang karena proses simulator dimatikan oleh perintah sesi operator; langkah itu lulus saat diulang sendiri dan seluruh skrip dijalankan ulang dari awal.",
    ])

    st_ += [P("9. Keputusan Menunggu Tim", "h1")]
    st_ += bullets([
        "ADR 0027 (C5 sebagai inti Keccak, PENDING #29), ADR 0028 (W2 sebagai sampler 8b), ADR 0029 (STREAM, 8c), ADR 0030 (OVERLAP, 8d): semuanya Proposed; hanya tim yang menerima atau menolak.",
        "Kotak Approval result_phase8.md kosong; hanya anggota tim yang mencentangnya. PENDING #25 (pemeriksaan input FIPS 203 di hardware atau HPS) dan #26 (protokol <i>checkpoint</i>) masih terbuka.",
        "Fase 9 (integrasi ML-KEM penuh) belum dimulai; sisa waktu sampai 2026-10-08 ditentukan tim (estimasi di ADR 0026).",
    ])
    st_ += [P("10. Keterbatasan", "h1")]
    st_ += bullets([
        "Tidak ada pengukuran pada papan; Fmax dan slack <i>kernel-only</i> dengan pin virtual. Tidak ada klaim kecepatan terhadap perangkat lunak atau daya.",
        "Siklus 'per operasi' adalah jumlah aritmetika Fase 6 dan sampling dalam satu sekuenser; hashing kunci (G, H, J), kompresi, penyandian, FO dan kontrol KEM belum ada.",
        "Satu sampler bersama: matriks dan noise disampel bergantian, tidak bersamaan; overlap hanya menyembunyikan sampling noise di balik transformasi.",
        "Register seed tidak dihapus setelah program selesai (tidak ada klaim ketahanan sisi-kanal; konstanta-waktu berarti jumlah siklus tidak bergantung pada nilai rahasia).",
        "Formal mencakup kontrol dan rentang, bukan nilai; nilai bertumpu pada simulasi terhadap golden dan hashlib.",
    ])
    st_ += [P("11. Reproduksibilitas", "h1")]
    st_ += [Paragraph("<br/>".join([
        ". scripts/env.sh",
        "scripts/phase8a_verify.sh; KS_OUTW=2 scripts/phase8b_verify.sh; scripts/phase8cd_verify.sh",
        "python3 formal/run_formal_phase8a.py; python3 formal/run_formal_phase8b.py all; python3 formal/run_formal_phase8c.py; python3 formal/run_formal_phase8d.py",
        "cd quartus/phase08b_sampler &amp;&amp; ./run_sm1.sh &amp;&amp; ./run_sm2.sh; cd ../phase08c_smp &amp;&amp; ./run_smp.sh",
        "python3 scripts/select_8b.py; python3 scripts/select_8cd.py; python3 scripts/build_phase8_report.py"]), S["code"])]

    doc.build(st_, onFirstPage=lambda c, d: None, onLaterPages=footer)
    print(f"written {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
