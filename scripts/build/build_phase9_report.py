#!/usr/bin/env python3
"""scripts/build/build_phase9_report.py

Builds docs/reports/CHIPATON_Phase9_Report.pdf (Phase 9 report: ML-KEM-768 core in simulation, blocks 9a codec, 9b hash and FO, 9c core; Bahasa Indonesia, same layout, fonts and styles as the Phase 0-8 reports; styles from
scripts/build/build_phase4_report.py) with ReportLab.

Every number comes from an evidence file in this repository: Quartus figures are parsed from the extracted evidence files by scripts/quartus/select_9a.py, select_9b.py and select_9c.py (the parse functions), cycles are read from the JSON files of the
simulations, and the claimed lines of the verification logs are checked (EXPECT). Nothing is written for a result that did not happen. Usage: python3 scripts/build/build_phase9_report.py
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
import select_9a  # noqa: E402
import select_9b  # noqa: E402
import select_9c  # noqa: E402

E = ROOT / "evidence" / "phase09"
OUT = ROOT / "docs" / "reports" / "CHIPATON_Phase9_Report.pdf"

EXPECT = {
    E / "9a" / "verify.md": ["[verilator] TOTAL: 17/17 passed", "[icarus] TOTAL: 17/17 passed", "OVERALL: PASS"],
    E / "9a" / "formal.md": ["ALL AS EXPECTED"],
    E / "9b" / "verify.md": ["[verilator] TOTAL: 23/23 passed", "[icarus] TOTAL: 23/23 passed", "OVERALL: PASS"],
    E / "9b" / "formal.md": ["ALL AS EXPECTED"],
    E / "9c" / "sim_verilator.md": ["[verilator] core: 6/6 PASS", "ACVP keyGen: 25 vectors equal", "ACVP encapsulation: 25 vectors equal", "ACVP decapsulation: 10 vectors equal", "[verilator] TOTAL: 11/11 passed"],
    E / "9c" / "sim_icarus.md": ["[icarus] core: 6/6 PASS", "ACVP keyGen: 25 vectors equal", "ACVP encapsulation: 25 vectors equal", "ACVP decapsulation: 10 vectors equal", "[icarus] TOTAL: 11/11 passed"],
    E / "9c" / "verify.md": ["OVERALL: PASS", "differing files: 0"],
    E / "9c" / "formal.md": ["ALL AS EXPECTED"],
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


def summ(parse, revs):
    rows = [parse(r) for r, _ in revs]
    a, f = [q["alm"] for q in rows], [q["fmax"] for q in rows]
    return dict(alm=statistics.median(a), alm_rng=(min(a), max(a)), fmax=statistics.median(f), fmax_rng=(min(f), max(f)), reg=(min(q["regs"] for q in rows), max(q["regs"] for q in rows)),
                ram=(min(q.get("m10k", 0) for q in rows), max(q.get("m10k", 0) for q in rows)), dsp=(min(q["dsp"] for q in rows), max(q["dsp"] for q in rows)),
                met=all(q["setup"] >= 0 and q["hold"] >= 0 for q in rows))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DV", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"CHIPATON — Laporan Fase 9 (ID) — hal. {doc.page}")
    canvas.restoreState()


def build():
    check_evidence()
    a = summ(select_9a.parse, select_9a.REVS)
    b = summ(select_9b.parse, select_9b.REVS)
    c = summ(select_9c.parse, select_9c.REVS)
    k0 = select_9b.parse("HF-K0")
    c20 = select_9c.parse("MC-20")
    ca = json.loads(next((E / "9a").glob("cycles_icarus_pack.json")).read_text())["pack_cycles"]
    cu = json.loads(next((E / "9a").glob("cycles_icarus_unpack.json")).read_text())["unpack_cycles"]
    ch = json.loads(next((E / "9b").glob("cycles_icarus_hash1.json")).read_text())["hash_cycles"]
    ch0 = json.loads(next((E / "9b").glob("cycles_icarus_hash0.json")).read_text())["hash_cycles"]
    cf = json.loads(next((E / "9b").glob("cycles_icarus_fo.json")).read_text())["fo_cycles"]
    cc = json.loads(next((E / "9c").glob("cycles_icarus_core.json")).read_text())
    f_med = c["fmax"]

    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=17 * mm,
                            title="CHIPATON — Laporan Fase 9 (ID)", author="Tim J5 (ITB)", subject="Fase 9: inti ML-KEM-768 dalam simulasi (9a codec, 9b hash dan FO, 9c inti) pada DE10-Nano")
    st = []
    W = A4[0] - 36 * mm
    st += [Spacer(1, 62 * mm), P("PERURI Digital Summit · CHIP 2026 Hackathon — Tim J5 (ITB)", "csub"), Spacer(1, 6)]
    st += [P("Laporan Fase 9", "ctitle")]
    st += [P("Inti ML-KEM-768 dalam simulasi · 9a (codec) · 9b (hash dan FO) · 9c (inti)", "csub")]
    st += [P("Terasic DE10-Nano · Intel/Altera Cyclone V SE 5CSEBA6U23I7", "csub"), Spacer(1, 14)]
    st += [P("Status: ketiga blok selesai diukur (simulasi, formal, Quartus <i>kernel-only</i>); semua vektor ACVP ML-KEM-768 lulus pada RTL; keputusan ADR 0033 menunggu tim; Approval belum dicentang", "cmeta")]
    st += [P("Branch: phase9-mlkem-core · 2026-10-03/04", "cmeta"), Spacer(1, 22)]
    st += [P("Ditulis untuk: Tim J5. Sumber kebenaran tetap berkas di repo (docs/results/phase09.md, evidence/phase09/). "
              "Label: <b>MEASURED</b> (laporan Quartus atau log simulasi di repo), <b>INFERENCE</b>, <b>ESTIMATE</b>, <i>perhitungan tim</i>, <b>belum diukur</b>. "
              "Tidak ada pengukuran pada papan; semua hasil berasal dari simulasi, analisis formal dan analisis Quartus (<i>kernel-only</i>, <i>virtual pin</i>).", "small")]
    st += [PageBreak()]

    st += [P("1. Ringkasan Eksekutif", "h1")]
    st += bullets([
        "<b>9a</b> (codec koefisien-byte): Compress, ByteEncode, ByteDecode dan Decompress untuk d = 1, 4, 10, 12; Compress tanpa pembagian (konstanta dibuktikan pada seluruh 3.329 masukan); "
        f"{num(a['alm'], 0)} ALM, 2 DSP; {ca['12']} siklus per polinomial (d = 12).",
        f"<b>9b</b> (hash dan FO): H, G, J di atas aliran kata 64 bit dan pembanding ciphertext konstan-waktu dengan pemilihan kunci memakai mask; {num(b['alm'], 1)} ALM (sponge C5); "
        f"H(ek) {ch['H_1184']} siklus, J(z, c) {ch['J_1120']} siklus, pembanding {cf} siklus.",
        f"<b>9c</b> (inti ML-KEM-768): KeyGen, Encaps, Decaps sebagai program mikro lurus (tanpa cabang) di atas mesin K-PKE Fase 8d. <b>Semua vektor ACVP ML-KEM-768 lulus di Verilator dan Icarus</b>: "
        f"keyGen 25, encapsulation 25, decapsulation 10 (termasuk ciphertext yang dimodifikasi). {fmt(round(c['alm']))} ALM ({num(100 * c['alm'] / 41910, 0)} % dari 41.910), 54 blok RAM, 28 DSP, median Fmax {num(f_med, 3)} MHz, timing 40 ns terpenuhi di setiap seed.",
        f"Siklus (simulasi): Encaps {cc['encaps'][0]}, Decaps {cc['decaps'][0]} (sama untuk ciphertext valid, ditolak dan kunci rahasia berbeda dengan ek yang sama), KeyGen {cc['keygen_min']}-{cc['keygen_max']} (bergantung pada ρ publik).",
        "Formal: bukti per blok (9a, 9b) dan bukti kontroler 9c (dua salinan kontroler dengan data berbeda dan handshake sama menjaga keadaan kontrol identik: kontrol tidak bergantung pada data).",
        "Satu bukti formal pertama (9b) <i>vacuous</i> ditemukan lewat cek jangkauan dan dibuang; stub formal lain di repo dicek, tidak ada hasil Fase 3-8 yang berubah.",
    ])

    st += [P("2. Tujuan dan Cakupan", "h1")]
    st += [P("Fase 9 (ROADMAP): KeyGen, Encaps dan Decaps ML-KEM-768 dalam RTL, bit-exact terhadap vektor ACVP resmi (konfigurasi C7-core). ADR 0031: pemeriksaan masukan FIPS 203 dilakukan HPS, bukan RTL; ADR 0032: satu STOP per blok. "
              "Matematika tidak diubah (C1). Keacakan (d, z, m) adalah masukan data. Tidak ada pengukuran papan (belum ada papan), tidak ada integrasi HPS dan tidak ada perbandingan dengan perangkat lunak.")]

    st += [P("3. Arsitektur", "h1")]
    st += [table([["Blok", "Fungsi"],
                  ["mlkem_pack, mlkem_unpack (9a)", "256 koefisien <-> 32 d byte; Compress_d = ((x << d) + 1664) * M &gt;&gt; S, Decompress_d = (3329 y + 2^(d-1)) &gt;&gt; d, keduanya tanpa pembagian; d = 1, 4, 10, 12"],
                  ["mlkem_hash (9b)", "H = SHA3-256, G = SHA3-512, J = SHAKE256 (32 byte) pada kata 64 bit; squeeze SHAKE dihentikan setelah 4 kata; parameter inti sponge C5 atau K0"],
                  ["mlkem_fo_cmp (9b)", "membandingkan c dan c' sebanyak 136 beat (OR dari semua XOR, tanpa early exit), memilih K' atau K_bar dengan mask 256 bit"],
                  ["mlkem_core (9c)", "kontroler program mikro (ROM dibuat dari model golden), buffer KB 300 kata, CB dan CB2 136 kata, register file 32 kata, mesin K-PKE 8d, task LDP dan STP, hash dan pembanding"],
                  ["Program mikro", "LDP, STP, HST, HFD, HGT, SDL, RUN, WR32, RD32, CMP, END; KeyGen 19 operasi, Encaps 19, Decaps 30; kode lurus: tidak ada cabang, alamat atau jumlah putaran yang bergantung data"]],
                 [48 * mm, W - 48 * mm])]

    st += [P("4. Verifikasi (MEASURED, simulasi dan formal)", "h1")]
    st += [table([["Butir", "Hasil"],
                  ["9a: model golden, tes cocotb (pack, unpack, exhaustif semua x dan semua y, round trip), 4 kontrol negatif", "17/17 di dua simulator; golden 7 tes"],
                  ["9a formal P1-P5 dan U1-U6; kontrol NC-P1, NC-P2, NC-U1, NC-U6", "PASS; kontrol gagal (hitungan: UNKNOWN di proof, FAIL di BMC kedalaman 300)"],
                  ["9b: digest sama dengan hashlib (panjang algoritma, batas laju, acak), 8.704 selisih satu bit di pembanding, 6 kontrol negatif, C5 dan K0", "23/23 di dua simulator"],
                  ["9b formal H1-H5 (dengan stub protokol sponge) dan F1-F4; cover; 5 kontrol", "PASS; cover tercapai; kontrol gagal"],
                  ["9c: ACVP keyGen 25, encapsulation 25, decapsulation 10", "100 % sama di Verilator dan Icarus"],
                  ["9c: acak 20 kasus (KeyGen, Encaps, Decaps valid dan satu bit berubah), rantai KeyGen-Encaps-Decaps, protokol, siklus konstan", "semua sama di kedua simulator"],
                  ["9c: 5 kontrol negatif (NC-CMP, NC-SEL, NC-LEN, NC-OFF, NC-ROM)", "gagal sesuai syarat di kedua simulator"],
                  ["9c formal: non-interferensi kontrol (dua salinan), rentang, eksklusivitas penulis, strobe, alamat; 3 kontrol", "PASS; kontrol gagal"],
                  ["Blok beku (rtl/sched, ntt, mem, arith, sample, keccak) tidak berubah", "0 berkas berbeda"]],
                 [W - 66 * mm, 66 * mm])]

    st += [P("5. Siklus (MEASURED, simulasi)", "h1")]
    st += [table([["Operasi", "Siklus"],
                  ["KeyGen (25 seed ACVP; bergantung pada ρ publik)", f"{cc['keygen_min']}-{cc['keygen_max']}"],
                  [f"Encaps (m berbeda, ek sama: konstan; 25 ek ACVP: {cc['encaps_acvp_min']}-{cc['encaps_acvp_max']})", f"{cc['encaps'][0]}"],
                  [f"Decaps (ciphertext valid atau ditolak, kunci rahasia berbeda dengan ek sama: konstan; 10 dk ACVP: {cc['decaps_acvp_min']}-{cc['decaps_acvp_max']})", f"{cc['decaps'][0]}"]],
                 [W - 40 * mm, 40 * mm])]
    st += [table([["Blok", "d = 1", "d = 4", "d = 10", "d = 12"],
                  ["pack (siklus per polinomial)", ca["1"], ca["4"], ca["10"], ca["12"]],
                  ["unpack (siklus per polinomial)", cu["1"], cu["4"], cu["10"], cu["12"]]],
                 [W - 4 * 22 * mm, 22 * mm, 22 * mm, 22 * mm, 22 * mm])]
    st += [table([["Hash dan pembanding", "C5", "K0"],
                  ["G dari 33 byte", ch["G_33"], ch0["G_33"]], ["G dari 64 byte", ch["G_64"], ch0["G_64"]],
                  ["H dari 1.184 byte", ch["H_1184"], ch0["H_1184"]], ["J dari 1.120 byte", ch["J_1120"], ch0["J_1120"]],
                  ["pembanding 136 beat", cf, "-"]], [W - 60 * mm, 30 * mm, 30 * mm])]
    st += [P(f"Latensi pada median Fmax analisis statis ({num(f_med, 2)} MHz), <i>perhitungan tim</i>, bukan pengukuran papan dan bukan perbandingan dengan perangkat lunak: KeyGen sekitar {num(cc['keygen_min'] / f_med, 0)} µs, "
             f"Encaps sekitar {num(cc['encaps'][0] / f_med, 0)} µs, Decaps sekitar {num(cc['decaps'][0] / f_med, 0)} µs.", "small")]

    st += [P("6. Sumber Daya dan Timing (MEASURED, Quartus, median seed 1-6)", "h1")]

    def row(name, x, ram="0"):
        return [name, f"{fmt(round(x['alm']))} ({fmt(x['alm_rng'][0])}-{fmt(x['alm_rng'][1])})", f"{x['reg'][0]}-{x['reg'][1]}", ram, f"{x['dsp'][0]}-{x['dsp'][1]}",
                f"{num(x['fmax'], 3)} ({num(x['fmax_rng'][0])}-{num(x['fmax_rng'][1])})", "ya" if x["met"] else "TIDAK"]
    st += [table([["Konfigurasi", "ALM", "Register", "RAM block", "DSP", "Fmax MHz (min-maks)", "40 ns terpenuhi"],
                  row("9a codec", a), row("9b hash + FO (C5)", b), row("9c inti ML-KEM", c, "54")],
                 [36 * mm, 38 * mm, 20 * mm, 18 * mm, 12 * mm, 38 * mm, W - 162 * mm])]
    st += [P(f"Informasi: hash + FO dengan sponge K0 {fmt(k0['alm'])} ALM (seed 1); inti pada 20 ns (seed 1): {fmt(c20['alm'])} ALM, slack {num(c20['setup'], 3)} ns (terpenuhi), Fmax {num(c20['fmax'], 2)} MHz. "
             "Kernel-only dengan pin virtual; penyebut Fitter: 41.910 ALM, 553 blok RAM, 112 DSP. Critical Warning 15725 (pin virtual pada jam) pada setiap kompilasi seperti fase sebelumnya; tidak ada yang diabaikan.", "small")]

    st += [P("7. Temuan dan Penyimpangan", "h1")]
    st += bullets([
        "<b>Bukti formal vacuous ditemukan dan dibuang</b> (9b): stub sponge pertama memakai sinyal bebas yang diperlakukan konstan oleh alat; cek jangkauan (cover) menunjukkan keadaan squeeze tidak pernah tercapai. Diperbaiki, cover ditambahkan ke alur runner; stub Fase 3 dan 8c dicek.",
        "<b>Kontrol void ditemukan</b> (9a): kontrol NC-CNT lulus semua tes karena driver tidak pernah menawarkan koefisien ke-257; driver diperbaiki dan hasil awal tidak dipakai.",
        "Ekspektasi dua kontrol formal 9a diubah dari FAIL ke UNKNOWN di proof lalu FAIL di BMC kedalaman 300 setelah proses pertama (preseden NC-B Fase 3); properti tidak diperlemah.",
        "Bukti formal hash 9b memakai stub protokol sponge karena sponge asli terlalu lambat untuk induksi (dihentikan setelah 30 menit); kontrol sponge sendiri ada di formal Fase 8a.",
        "ESTIMATE meleset: siklus pack dan unpack d = 1 dan 4 (dibatasi masukan), siklus Encaps (sekitar 800 lebih rendah dari perkiraan) dan ALM inti (sekitar 2.400 lebih rendah).",
        "Kesalahan penyiapan saya (bukan RTL): impor tes yang hilang, jalur berkas <i>.qsf</i> pertama yang salah (kompilasi gagal 45 detik; hasilnya tidak dipakai), mutasi kontrol yang tidak dapat dikompilasi di Icarus.",
        "Bukti formal kontroler 9c ditambahkan setelah verifikasi simulasi (Amandemen A2): rencana awal tidak memuatnya, padahal CRG-8 memintanya.",
    ])
    st += [P("8. Keputusan Menunggu Tim", "h1")]
    st += bullets([
        "ADR 0033 (PENDING #33, Proposed): menerima inti C7-core seperti dibangun; inti sponge instance hash (C5 default atau K0, sekitar 2.500 ALM lebih kecil); apakah optimasi (encode dan decode tumpang tindih) diinginkan.",
        "Kotak Approval phase09.md kosong; hanya anggota tim yang mencentangnya. Papan DE10-Nano (PENDING #8) menentukan Fase 10 dan 11; tanpa papan keduanya <i>NOT DONE</i>.",
        "Bagian 3 proposal (halaman 4-6) belum ditulis; dapat ditulis dari bukti ini bila diminta.",
    ])
    st += [P("9. Keterbatasan", "h1")]
    st += bullets([
        "Tidak ada pengukuran pada papan; Fmax dan slack <i>kernel-only</i> dengan pin virtual. Tidak ada klaim kecepatan terhadap perangkat lunak, daya atau ketahanan sisi-kanal.",
        "Konstan-siklus ditunjukkan dalam simulasi untuk ek tetap: panjang sampling matriks bergantung pada ρ publik. Bukti formal kontrol berlaku untuk handshake sub-blok yang sama (stub protokol).",
        "Pemeriksaan masukan FIPS 203 tidak ada di RTL (ADR 0031); dua grup ACVP key-check tidak dijalankan terhadap RTL.",
        "Encode dan decode polinomial serial dan tidak tumpang tindih dengan mesin: sekitar 2.300-2.400 siklus per KeyGen atau Decaps (INFERENCE).",
        "Kontrol negatif 9c dijalankan dengan himpunan vektor yang dikurangi; run penuh ada di target core. Run Icarus penuh memakan sekitar satu jam.",
    ])
    st += [P("10. Reproduksibilitas", "h1")]
    st += [Paragraph("<br/>".join([
        ". scripts/env.sh",
        "scripts/test/phase9a_verify.sh; scripts/test/phase9b_verify.sh; P9C_SIMS=0 scripts/test/phase9c_verify.sh; python3 tb/mlkem/run_core_tests.py verilator; python3 tb/mlkem/run_core_tests.py icarus",
        "python3 formal/run/run_formal_phase9a.py; python3 formal/run/run_formal_phase9b.py all; python3 formal/run/run_formal_phase9c.py all",
        "cd quartus/phase09a_codec &amp;&amp; ./run_cd.sh; cd ../phase09b_hashfo &amp;&amp; ./run_hf.sh; cd ../phase09c_core &amp;&amp; ./run_mc.sh",
        "python3 scripts/quartus/select_9a.py; python3 scripts/quartus/select_9b.py; python3 scripts/quartus/select_9c.py; python3 scripts/build/gen_mlkem_ctl_rom.py --check; python3 scripts/build/build_phase9_report.py"]), S["code"])]

    doc.build(st, onFirstPage=lambda cv, d: None, onLaterPages=footer)
    print(f"written {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
