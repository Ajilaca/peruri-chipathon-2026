#!/usr/bin/env python3
"""scripts/build/build_complete_report.py

Builds docs/reports/CHIPATON_COMPLETE_REPORT.pdf: the complete report of Phases 0 to 9M (Bahasa Indonesia, same fonts and styles as scripts/build/build_phase4_report.py) with ReportLab.
The text is the CONTENT string below (markdown-lite: ## section, ### subsection, tables, bullets, numbered lists, **bold**, `code`); every number in it was copied from the result and evidence files of
this repository when the report was written. check_evidence() verifies that the files it cites exist and that the key claimed lines are still in them; nothing is computed here.
Usage: python3 scripts/build/build_complete_report.py
"""
import pathlib
import re
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "scripts" / g) for g in ("build", "quartus")]
from build_phase4_report import MUTED, P, S, table  # noqa: E402

OUT = ROOT / "docs" / "reports" / "CHIPATON_COMPLETE_REPORT.pdf"
E9M = ROOT / "evidence" / "phase9m"
EXPECT = {
    ROOT / "docs" / "results" / "phase9m.md": ["Status: PARTIAL", "14,222.0 ALM"],
    E9M / "batch2" / "9i4" / "sim.md": ["ACVP keyGen: 25 vectors equal", "[verilator] core: 6/6 PASS", "[icarus] core: 6/6 PASS"],
    E9M / "batch2" / "9i4" / "formal.md": ["TIMEOUT", "NC-JOIN4"],
    E9M / "batch2" / "9i4" / "selection_worksheet.md": ["76.665", "109.8 / 125.4 / 169.4"],
    E9M / "batch2" / "9s2b" / "selection_worksheet.md": ["77.555", "NOT met as written"],
    E9M / "batch2" / "9s2" / "selection_worksheet.md": ["74.125"],
    E9M / "batch1" / "9f1b" / "selection_worksheet.md": ["73.855"],
    ROOT / "docs" / "results" / "phase09.md": ["17,620.5", "keyGen 25"],
    ROOT / "docs" / "results" / "phase06.md": ["44.320"],
    ROOT / "docs" / "results" / "phase04.md": ["34.19"],
}
for n in ("0", "1", "2", "3", "4", "5", "5m", "6", "7", "8", "9", "9m"):
    EXPECT.setdefault(ROOT / "docs" / "results" / f"phase{n.zfill(2) if n.isdigit() else n.replace('5m', '05m')}.md", [])


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


def inline(t):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"`([^`]+)`", r'<font name="DVM" size="8">\1</font>', t)
    return t


def col_widths(rows, total):
    """Each column gets at least the width of its longest word (so numbers never break), the rest is shared by text length."""
    n = len(rows[0])
    need = [max(max((len(w) for w in (r[c] if c < len(r) else "").split()), default=1) for r in rows) * 4.3 + 8 for c in range(n)]
    length = [max(len(r[c]) if c < len(r) else 0 for r in rows) for c in range(n)]
    if sum(need) >= total:
        return [total * x / sum(need) for x in need]
    extra = total - sum(need)
    share = [min(max(x, 6), 70) for x in length]
    return [need[c] + extra * share[c] / sum(share) for c in range(n)]


def flow(text, width):
    out, lines, i = [], text.split("\n"), 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln or ln.startswith("<!--"):
            i += 1
        elif ln.startswith("## "):
            out.append(P(inline(ln[3:]), "h1")); i += 1
        elif ln.startswith("### "):
            out.append(P(inline(ln[4:]), "h2")); i += 1
        elif ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            n = len(rows[0])
            rows = [r + [""] * (n - len(r)) for r in rows]
            out += [table([[inline(c) for c in r] for r in rows], col_widths(rows, width)), Spacer(1, 5)]
        elif ln.startswith("- "):
            while i < len(lines) and lines[i].startswith("- "):
                out.append(Paragraph(inline(lines[i][2:]), S["bullet"], bulletText="\u2022")); i += 1
        elif re.match(r"\d+\. ", ln):
            while i < len(lines) and re.match(r"\d+\. ", lines[i]):
                m = re.match(r"(\d+)\. (.*)", lines[i])
                out.append(Paragraph(inline(m.group(2)), S["bullet"], bulletText=m.group(1) + "."))
                i += 1
        elif ln.strip() == "---":
            out.append(Spacer(1, 4)); i += 1
        else:
            out.append(P(inline(ln))); i += 1
    return out


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("DV", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"CHIPATON \u2014 Laporan Lengkap Fase 0-9M (ID) \u2014 hal. {doc.page}")
    canvas.restoreState()


def build():
    check_evidence()
    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=17 * mm,
                            title="CHIPATON \u2014 Laporan Lengkap Fase 0-9M (ID)", author="Tim J5 (ITB)",
                            subject="Akselerator ML-KEM-768 pada DE10-Nano: rekap Fase 0 sampai 9M")
    W = A4[0] - 36 * mm
    st = [Spacer(1, 58 * mm), P("PERURI Digital Summit \u00b7 CHIP 2026 Hackathon \u2014 Tim J5 (ITB)", "csub"), Spacer(1, 6),
          P("Laporan Lengkap", "ctitle"), P("Fase 0 sampai Fase 9M", "ctitle"), Spacer(1, 4),
          P("Akselerator ML-KEM-768 (NIST FIPS 203) pada Terasic DE10-Nano \u00b7 Intel/Altera Cyclone V SE 5CSEBA6U23I7", "csub"), Spacer(1, 14),
          P("Status: simulasi, formal, dan analisis Quartus <i>kernel-only</i>; ACVP ML-KEM-768 100 % pada RTL di dua simulator; tidak ada pengukuran papan; ADR hasil 9M diterima tim, ADR 0033 masih Proposed; kotak Approval Fase 9 dan 9M kosong", "cmeta"),
          P("Repositori: github.com/Ajilaca/peruri-chipathon-2026 \u00b7 disusun 2026-10-05", "cmeta"), Spacer(1, 22),
          P("Berkas di repo tetap sumber kebenaran (docs/results/, evidence/, docs/decisions/). Label: MEASURED (laporan Quartus atau log simulasi di repo), INFERENCE, "
            "ESTIMATE, <i>perhitungan tim</i>. Tidak ada pengukuran pada papan; semua hasil berasal dari simulasi, analisis formal, dan analisis Quartus (<i>kernel-only</i>, <i>virtual pin</i>). "
            "Dokumen ini bukan teks proposal.", "small"), PageBreak()]
    st += flow(CONTENT, W)
    doc.build(st, onFirstPage=lambda c, d: None, onLaterPages=footer)
    print("written", OUT.relative_to(ROOT))


CONTENT = r"""

## 1. Ringkasan eksekutif
- Tujuan: merancang, memverifikasi, dan mengukur akselerator ML-KEM-768 (NIST FIPS 203) dengan Keccak-f[1600] dan NTT/INTT di fabric, alur protokol dan baseline perangkat lunak di HPS, dengan perilaku konstan-waktu dibuktikan lewat invarian jumlah siklus. Matematika dikunci (ADR 0002): q, n, k, η, du, dv, akar satuan, dan aritmetika FIPS 203 tidak berubah di fase mana pun; inovasi hanya pada arsitektur.
- Status teknis (simulasi): inti ML-KEM-768 lengkap (KeyGen, Encaps, Decaps) berjalan di RTL dan lulus semua vektor ACVP resmi yang dipin di dua simulator: keyGen 25, encapsulation 25, decapsulation 10 (termasuk ciphertext yang dimodifikasi). Fase 0–9 selesai (kotak Approval Fase 9 masih kosong); Fase 9M selesai sebagian (lihat butir terakhir).
- Angka akhir (K4, `mlkem_core4`, MEASURED kernel-only): 14.222,0 ALM pada 40 ns (34 % dari 41.910), 53–54 blok RAM, 28 DSP; 8.416 / 9.611 / 12.989 siklus untuk KeyGen / Encaps / Decaps; timing terpenuhi pada 15,000 ns di 6 dari 6 seed (median Fmax 76,665 MHz); latensi pada 15 ns 109,8 / 125,4 / 169,4 µs (perhitungan tim, siklus dibagi Fmax, bukan waktu di papan).
- Dari titik awal ke akhir: inti pertama (C0, L = 1) tidak memenuhi timing pada 20 ns (Fmax 14,64 MHz, 897 siklus per NTT); inti Fase 9 (17.620,5 ALM, 9.095 / 10.735 / 16.667 siklus, median Fmax 49,28 MHz pada 40 ns) menjadi K4 dengan −19 % ALM dan −7,5 % / −10,5 % / −22,1 % siklus.
- Cara kerja: tiap langkah punya rencana uji dan aturan adopsi yang ditulis sebelum pengukuran. Angka hanya dari laporan Quartus atau log di repo. Estimasi yang meleset dicatat di Bagian 7. Hasil yang tidak mendukung hipotesis tetap ditulis (S2 netral, S2b tidak lolos aturannya seperti tertulis).
- Batas yang harus diketahui: tanpa papan, tanpa integrasi HPS, tanpa perbandingan dengan perangkat lunak; konstan-waktu hanya berarti invarian siklus (bukan ketahanan side-channel); tiga bukti formal berbatas habis waktu (P1 dan NC-E1-4 pada core4, NC-B7 pada core3); ADR hasil 9M (0035, 0037, 0038, 0040 sampai 0043) diterima tim pada 2026-10-05; ADR 0033 masih Proposed.

---

## 2. Tujuan, batasan, dan cara kerja

### 2.1 Batasan proyek
| # | Batasan | Dicatat di |
|---|---|---|
| C1 | Matematika dikunci; hanya arsitektur yang diubah | ADR 0002 |
| C2 | Angka hanya dari Quartus atau papan; selain itu diberi label ESTIMATE, sumber bersitasi, atau "perhitungan tim" | `evidence/` |
| C3 | Tidak ada klaim "quantum-proof", ketahanan side-channel, atau percepatan terhadap perangkat lunak tanpa bukti | ADR 0002 |
| C4 | Proposal 6 halaman; Bagian 3 belum ditulis | aturan lomba |
| C5 | Pilihan terbuka diputuskan tim, bukan asisten | `docs/decisions/PENDING.md` |
| C6 | Persetujuan manusia antar fase; verifikasi sebelum optimasi | kotak Approval di `docs/results/` |
| C7 | Repo publik: tanpa rahasia dan data pribadi | `scripts/setup_github.sh` |
| C8 | Hasil hanya-simulasi diberi label; klaim validasi perangkat keras butuh bukti di `evidence/` | `evidence/` |

### 2.2 Alur kerja yang dipakai di semua fase
1. Model emas dulu (`tb/golden/`, Python, independen dari RTL), diuji terhadap vektor resmi dan oracle independen.
2. Rencana uji dan aturan adopsi ditulis sebelum RTL dan sebelum pengukuran; aturan tidak diubah setelah melihat hasil (amandemen bertanggal mencatat temuan dan koreksi).
3. RTL diverifikasi bit-exact terhadap model emas di dua simulator (Verilator dan Icarus), lalu formal (SymbiYosys, boolector) dengan kontrol negatif yang harus gagal.
4. Baru setelah itu Quartus (kompilasi satu per satu, enam seed bila aturan menuntut) dan hasil diekstrak ke berkas bukti.
5. Hasil ditulis di `docs/results/phase<NN>.md`; hanya anggota tim yang mencentang kotak Approval.
6. Keputusan tim dicatat sebagai ADR (Proposed, lalu Accepted oleh tim); angka di ADR menunjuk berkas bukti.

### 2.3 Lingkungan
Ubuntu 24.04, OSS CAD Suite 2026-09-23 (Verilator 5.053, Icarus 14.0 devel, Yosys, slang 11.0, SymbiYosys + boolector), cocotb 2.1.0, Python 3.12, Quartus Prime Lite 25.1std.0 Build 1129 (satu-satunya sumber angka implementasi FPGA). Angka Yosys tidak pernah dilaporkan sebagai sumber daya Cyclone V.

---

## 3. Perjalanan per fase

### Fase 0 — Fondasi: model emas dan vektor resmi (DONE, disetujui 2026-09-29)
- Dibuat: `tb/golden/` (parameter terkunci, primitif FIPS 203, K-PKE, ML-KEM internal), vektor ACVP dipin pada commit `975de31e…` dengan sha256, evidence kesalahan (errata) FIPS 203, ADR 0003.
- Hasil (MEASURED): `check_params.py` 12/12; `pytest` 23/23; ACVP ML-KEM-768 80/80 (keyGen 25, encapsulation 25, decapsulation 10, decapsulationKeyCheck 10, encapsulationKeyCheck 10); lintas-cek oracle independen (kyber-py 1.2.0) 2000/2000 cocok; dua item errata, keduanya non-normatif.
- Catatan: berkas keyGen ACVP menyatakan `isSample: false` (berbeda dari asumsi di `kat_sources.md`), dilaporkan apa adanya. Model Python bukan implementasi konstan-waktu dan tidak diklaim begitu.

### Fase 1 — Baseline RTL minimal: L = 1 NTT/INTT, konfigurasi C0 (DONE, ditetapkan tim 2026-10-05)
- Dibuat: `ntt_core` (satu butterfly per siklus, 7 layer + lintasan skala INTT), memori polinomial tak berbank, ROM twiddle hasil generator, bukti formal keselamatan FSM.
- Hasil: bit-exact di dua simulator (10/10); NTT/INTT 897 / 1.153 siklus, konstan; Quartus: 7.010 ALM, 3 DSP, 0 M10K, Fmax 14,64 MHz, slack setup −48,323 ns pada 20 ns (timing tidak terpenuhi).
- Penyebab (dari laporan jalur): pembagi `%` kombinasional 24/12 bit menghabiskan 38,9 ns (57,5 %) dari jalur data 67,7 ns. Tidak diperbaiki di fase ini dengan sengaja.
- CRG-9 awalnya FAIL (timing) dan ADR target clock belum ada saat fase ini ditutup (target 20 ns di SDC bersifat sementara). Tim menetapkan fase ini DONE pada 2026-10-05; ADR 0006 mencatat target clock kemudian, dan kegagalan timing didokumentasikan.

### Fase 2 — Arsitektur memori: banking dan pembangkit alamat, C1 (DONE, ditetapkan tim 2026-10-05)
- Dibuat: skema bank XOR-grup yang terbukti bebas konflik untuk L = 1, 2, 4, 8 (eksaustif + formal pada ROM nyata), memori berbank, ROM peta bank hasil generator.
- Hasil: siklus identik C0 (0 stall); 6.749 ALM; Fmax 14,99 MHz; timing masih gagal (−46,720 ns).
- Temuan: M10K tidak terpakai (0/553) walau judul fase menyebut M10K, karena pembacaan asinkron tidak bisa dipetakan Quartus ke RAM; dicatat dan dibiarkan sebagai keputusan fase berikutnya. Satu kompilasi Quartus rusak karena direktori kerja terhapus tak sengaja; yang dipakai hanya hasil ulang yang bersih.

### Fase 3 — Eksplorasi multi-lane L = 1/2/4/8, C2 (DONE, ditetapkan tim 2026-10-05)
| | L = 1 | L = 2 | L = 4 | L = 8 |
|---|---|---|---|---|
| ALM (C2) | 6.018 | 5.728 | 7.629 | 11.446 |
| ALM (C2-K2-K1) | 5.566 | 5.374 | 6.775 | 9.754 |
| DSP (C2-K2-K1) | 2 | 3 | 5 | 9 |
| Siklus NTT / INTT | 897 / 1.153 | 449 / 705 | 225 / 481 | 113 / 369 |
| Fmax (C2, 20 ns) | 14,76 | 13,54 | 11,60 | 7,62 MHz |
- Eksperimen tambahan K1 (satu pengali termodulasi per butterfly) membuat L = 8 masuk anggaran ALM (724 di bawah batas); ADR 0005: titik kerja C2-K2-K1 pada L = 8.
- Celah formal L = 2/4/8 (UNKNOWN) ternyata artefak harness (ROM dimodelkan sebagai state bebas pada langkah induksi); diperbaiki di harness dengan `memory_map -rom-only`, RTL tidak berubah; PASS di keempat L dan empat kontrol negatif gagal sesuai syarat.

### Fase 4 — Pipeline butterfly P = 0/2/4/6, C3 (DONE, disetujui 2026-10-01)
| | P = 0 | P = 2 | P = 4 | P = 6 |
|---|---|---|---|---|
| ALM | 9.723 | 9.696 | 10.439 | 10.505 |
| Slack setup pada 40 ns | −90,653 | −0,368 | +8,734 | +10,753 ns |
| Fmax (MHz) | 7,65 | 24,77 | 31,98 | 34,19 |
| Siklus NTT / INTT | 113 / 369 | 115 / 371 | 117 / 373 | 119 / 375 |
- Siklus persis 113 + P dan 369 + P (0 stall). Reducer bertahap sama dengan reducer beku untuk semua 2^24 masukan.
- ADR 0009: L = 8, P = 6 (C3-P6) dengan anggaran desain inti NTT 30 % (12.573 ALM); ADR 0008 (P = 4 pada anggaran 25 %) digantikan. Kompilasi GHRD shell dan integrasi GHRD + C3-P4 / P6 tersedia sebagai bukti.

### Fase 5 — Aritmetika modular, C4 (DONE, disetujui Jevan 2026-10-03)
| | C3-P6 | C4a (fold) | C4b-B (Barrett) | C4b-M (Montgomery) | C4c (lazy INTT) |
|---|---|---|---|---|---|
| ALM (median 6 seed) | — | 9.847 (1 seed) | 9.171 | 9.286,5 | 9.032–9.094 (rentang) |
| DSP | 9 | 9 | 18 | 9 | 18 |
| Fmax median (MHz) | 33,11 | — | 34,515 | 33,780 | 33,100 |
- Aturan ADR 0011 memilih Barrett (Fmax median tertinggi; biaya DSP 9 → 18, ADR 0013). C4c (INTT lazy) benar tetapi tidak diadopsi (ADR 0014). 5d (basis Karatsuba) tidak dicoba (ADR 0015).
- Analisis: reducer menghemat area (≈1.300 ALM) tetapi tidak menggeser Fmax melebihi derau seed; jalur kritis adalah pembacaan memori (ADR 0010). Kompilasi informasi pada 20 ns tidak terpenuhi untuk C3-P6 maupun C4b-B.

### Fase 5M — Memori dan jadwal (DONE, disetujui Jevan 2026-10-03)
| | C4b-B | M6 (S6) | S7 | S8 |
|---|---|---|---|---|
| ALM median | 9.171 | 9.421,5 | 9.391 | 9.443,5 |
| Fmax median (MHz) | 34,515 | 34,430 | 38,720 | 37,990 |
| Siklus NTT / INTT | 119 / 375 | 119 / 119 | 120 / 120 | 122 / 122 |
| DSP / M10K | 18 / 29 | 16 / 29 | 16 / 31 | 16 / 33 |
- S6 (INTT tanpa lintasan skala, setengah di tiap layer, terbukti sama dengan Algoritma 10 FIPS 203): INTT 375 → 119 siklus; aturan tidak mengadopsinya (selisih 0,008 µs), tetapi tim memilihnya sebagai dasar (ADR 0020). S7 (pembacaan memori terbelah) lolos aturan (+12,5 % Fmax). S8 tidak lolos. S9: peta 16 bank 1R1W bebas konflik ada (peta pertama yang diturunkan tangan salah dan ditolak skrip).

### Fase 6 — Penjadwalan tingkat operasi dan S10 (DONE, disetujui Jevan 2026-10-03)
- Sequencer aritmetika K-PKE menjalankan KeyGen, Encrypt, Decrypt sebagai program tetap, bit-exact terhadap K-PKE emas tanpa perubahan, dengan jumlah transformasi acuan dan siklus konstan: 5.493 / 6.810 / 3.121 dengan inti S7, 5.475 / 6.789 / 3.109 dengan S10.
- S10 (memori 16 × 1R1W tanpa arbitrase slot) lolos aturannya dan diterima (ADR 0025): ALM 5.077 (S7: 9.391), median Fmax 44,320 MHz pada 40 ns, 118 siklus, timing terpenuhi pada 20 ns di 6 dari 6 seed.
- Perpindahan data lewat port host (1 koefisien/siklus) memakan 3.102 dari 5.493 siklus KeyGen (56 %): petunjuk awal untuk Fase 9M.

### Fase 7 — Keccak-f[1600] dan SHA3/SHAKE, K0 (DONE, disetujui Jose 2026-10-03)
- Keccak iteratif satu ronde per siklus (24 siklus sibuk per permutasi, 26 dilihat sponge) dan sponge untuk SHA3-256/512, SHAKE128/256, sama dengan `hashlib` untuk semua panjang yang diuji di dua simulator; formal K1–K5.
- Quartus (seed 1): 3.572 ALM, 1.653 register, 0 M10K, 0 DSP; timing terpenuhi di 40 ns (56,99 MHz) dan 20 ns (76,30 MHz). Siklus Keccak per operasi ML-KEM sekitar 2.026 / 2.078 / 2.070 (perhitungan tim), sekitar dua kali perkiraan awal 1.060 yang melewatkan siklus kontrol.
- Estimasi meleset dan dicatat: ALM 2 % di atas rentang tertulis; register di bawah rentang.

### Fase 8 — Optimasi Keccak dan streaming (DONE, disetujui Jose 2026-10-03)
| Langkah | Hasil terukur |
|---|---|
| 8a: C5 (dua ronde per siklus) | 6.167 ALM (K0: 3.566,5), median Fmax 50,655 (K0: 67,675); 14 siklus per permutasi (K0: 26); H(ek) 281 vs 389 siklus; diadopsi aturan (ADR 0027) |
| 8b: sampler streaming | W2 (dua koefisien per siklus) dipilih atas W1: SampleNTT 206,48 vs 305,23 siklus, CBD 152 vs 280, 5.290 ALM, 0 M10K (ADR 0028) |
| 8c: matriks A langsung ke unit PWM | STREAM atas STORE: KeyGen 7.089 vs 8.268 siklus, M10K 44 vs 55 (ADR 0029) |
| 8d: noise tumpang-tindih dengan transformasi | OVERLAP atas STREAM: KeyGen 6.344 dan Encrypt 7.655 siklus (STREAM 7.089 / 8.549; aritmetika saja 5.475 / 6.789), ALM ≈ 10.992 (ADR 0030) |
- Dua cacat RTL ditemukan verifikasi dan diperbaiki: tag valid pipeline PWMS tanpa reset (ditemukan formal, tak terlihat di simulasi) dan sampler yang mulai bersamaan dengan pulsa `done_o` sebelumnya (hanya ditemukan program uji STRESS). Satu nilai harapan berubah setelah melihat hasil (8b A1) dan dicatat.

### Fase 9 — ML-KEM-768 lengkap dalam RTL, simulasi (DONE; kotak Approval kosong)
- Tiga blok: 9a codec (299 ALM, 2 DSP; 389 siklus per polinomial d = 12), 9b hash wrapper dan pembanding FO konstan-waktu (6.734,5 ALM; H(ek) 282, J 274, pembanding 137 siklus), 9c inti `mlkem_core` sebagai program mikro lurus tanpa cabang di atas mesin K-PKE 8d.
- ACVP 100 % di dua simulator (keyGen 25, encapsulation 25, decapsulation 10). Siklus: Encaps 10.691 dan Decaps 16.623 (sama untuk ciphertext valid, ditolak, dan kunci rahasia berbeda dengan ek yang sama), KeyGen 9.035–9.076 (bergantung ρ publik).
- Quartus kernel-only (6 seed, 40 ns): 17.620,5 ALM (42 %), 54 blok RAM, 28 DSP, median Fmax 49,280 MHz, timing terpenuhi di setiap seed. Pemeriksaan masukan FIPS 203 dilakukan HPS, bukan RTL (ADR 0031).
- Bukti formal pertama 9b vacuous (stub `(* anyseq *) logic` dibaca hanya di kode prosedural diperlakukan konstan): ditemukan lewat cek jangkauan, dibuang, diganti `wire`, dan diulang. Estimasi meleset: ALM inti 20.000 diperkirakan vs 17.620,5 terukur; siklus Encaps 11.500 vs 10.691.

### Fase 9M — Optimasi inti (lihat `CHIPATON_Phase9M_Report.pdf` untuk rincian)
| Konfigurasi | ALM 40 ns | Fmax 15 ns (MHz) | Siklus KeyGen / Encaps / Decaps | Latensi 15 ns (µs) |
|---|---|---|---|---|
| Inti Fase 9 | 17.620,5 | — (20 ns: 63,645) | 9.095 / 10.735 / 16.667 | — |
| MW (9M-1, codec dua byte) | 17.654,0 | 73,635 (2 seed) | 8.327 / 10.159 / 15.515 | 113,6 / 138,5 / 211,6 |
| MK (9M-3, hash K0) | 15.917,5 | — | 8.447 / 10.279 / 15.635 | — |
| K1 (S1, sampler K0) | 14.061,0 | 73,070 | 8.795 / 10.627 / 15.983 | 120,4 / 145,4 / 218,7 |
| K1b (S1b, hash latar) | 14.335,0 | 73,855 | 8.404 / 10.236 / 15.597 | 113,8 / 138,6 / 211,2 |
| K2 (S2, P = 6) | 14.213,0 | 74,125 | 8.416 / 10.250 / 15.619 | 113,5 / 138,3 / 210,7 |
| K3 (S2b, alamat terregistrasi) | 14.115,5 | 77,555 | 8.416 / 10.250 / 15.619 | 108,5 / 132,2 / 201,4 |
| K4 (item 4, muat di belakang mesin) | 14.222,0 | 76,665 | 8.416 / 9.611 / 12.989 | 109,8 / 125,4 / 169,4 |
- K4 terhadap MW pada 15 ns (indikatif, MW hanya dua seed): latensi −3,3 % / −9,5 % / −19,9 %. K4 terhadap inti Fase 9: ALM −3.398,5 (−19,3 %), siklus −7,5 % / −10,5 % / −22,1 %.
- Batas pelaporan Fmax 15 ns (ADR 0039): sweep S0 menemukan batas inti MW di antara 13 dan 14 ns.

---

## 4. Evolusi inti NTT/INTT (Fase 1–6)
Semua MEASURED (Quartus kernel-only; siklus dari simulasi). Kolom Fmax pada batasan yang tertera; angka antar batasan tidak sebanding.
| Konfigurasi | Perubahan | ALM | DSP / M10K | Siklus NTT / INTT | Fmax (MHz) |
|---|---|---|---|---|---|
| C0 | L = 1, memori tak berbank | 7.010 | 3 / 0 | 897 / 1.153 | 14,64 (20 ns, gagal) |
| C1 | memori berbank (1 bank) | 6.749 | 3 / 0 | 897 / 1.153 | 14,99 (gagal) |
| C2 (L = 8) | 8 lane | 11.446 | 17 / 0 | 113 / 369 | 7,62 (gagal) |
| C2-K2-K1 (L = 8) | pengali bersama | 9.754 | 9 / 0 | 113 / 369 | 7,68 (gagal) |
| C3-P6 | pipeline P = 6 | 10.505 | 9 / 29 | 119 / 375 | 34,19 (40 ns, terpenuhi) |
| C4b-B | reducer Barrett | 9.171 (median) | 18 / 29 | 119 / 375 | 34,515 (median) |
| M6 | INTT tanpa lintasan skala | 9.421,5 | 16 / 29 | 119 / 119 | 34,430 |
| S7 | pembacaan memori terbelah | 9.391 | 16 / 31 | 120 / 120 | 38,720 |
| S10 | 16 bank 1R1W, tanpa arbitrase | 5.077 | 16 / 24 | 118 / 118 | 44,320 (40 ns); terpenuhi di 20 ns, 6/6 seed |
Pola yang konsisten dengan data (INFERENCE): ketika satu dinding dihilangkan, dinding berikutnya muncul. Pembagi `%` dan memori tak berbank membatasi C0–C2; pembacaan memori membatasi C3–C4; arbitrase slot membatasi M6–S8; pada 9M jalur reducer lalu jalur alamat issue lalu jalur sequencer ke alamat bergantian menjadi dinding.

## 5. Verifikasi (apa yang benar-benar diuji)
| Aspek | Bukti |
|---|---|
| Model emas | 23 tes properti; ACVP 80/80; oracle independen 2000/2000; matematika dikunci (`check_params.py` lulus di setiap fase) |
| RTL vs model | bit-exact di Verilator dan Icarus untuk NTT/INTT, memori, Keccak, SHA3/SHAKE (terhadap `hashlib`), sampler, codec, K-PKE, dan seluruh inti (ACVP) |
| Invarian siklus | Fase 1–4 konstan per konfigurasi; Keccak data-independen; Encaps dan Decaps inti identik untuk masukan valid, ditolak, dan kunci berbeda (K4: Encaps 9.555 dan Decaps 12.933 pada masukan uji; selisih terhadap K3 sama dengan pada masukan profil) |
| Formal | FSM safety, rentang alamat, konflik bank, handshake, non-interferensi E1 (dua salinan kontroler dengan data berbeda dan handshake sama menjaga keadaan kontrol identik), S1–S7, B1–B7, cover; selalu dengan kontrol negatif |
| Kontrol negatif | peta bank tanpa bit XOR, penulisan satu siklus kurang, panjang hash kurang satu byte, offset z salah, tulis ganda, join tanpa menunggu, interlock dilepas, dan lainnya: harus gagal dan gagal |
| Regresi | setiap fase menjalankan ulang fase sebelumnya; nilai bawaan parameter baru mereproduksi hitungan siklus lama (118 / 118, K1b, K2); berkas Fase 6–8 beku tidak diubah |
| Quartus | 6 seed untuk tiap keputusan; satu kompilasi sekali jalan; ekstrak per revisi di `evidence/` (keluaran mentah tidak di-commit, diarsipkan di luar repo) |

## 6. Daftar keputusan (ADR)
| Rentang | Isi | Status |
|---|---|---|
| 0001–0003 | ide proyek; kebijakan lingkup dan klaim (matematika dikunci); penanganan errata FIPS 203 | Accepted |
| 0004–0009 | kriteria L; kriteria P; target clock; L = 8, P = 6 dengan anggaran 30 % (0008 digantikan 0009) | Accepted |
| 0010–0015 | 50 MHz sebagai target terbaik-upaya; rencana Fase 5; aturan setelah Fase 5; Barrett; 5c tidak diadopsi; 5d dipindah | Accepted |
| 0016 | lisensi MIT | Accepted |
| 0017–0025 | Fase 5M (S6–S9), jalur minimal sampai 2026-10-08 (0018 digantikan 0019), S6 sebagai dasar (0020), S7/S8/S9 (0021–0023 digantikan 0025), Fase 6 dan S10 | Accepted |
| 0026–0030 | Fase 8a–8d berjalan; C5; sampler W2; STREAM; OVERLAP | Accepted |
| 0031–0032 | pemeriksaan masukan di HPS; satu STOP per blok | Accepted |
| 0033 | inti Fase 9 sebagaimana dibangun | Proposed |
| 0034, 0036, 0039 | lingkup 9M; rencana Fmax dan aturan latensi; 15 ns batas pelaporan | Accepted |
| 0035, 0037, 0038, 0040, 0041, 0042, 0043 | hasil 9M-1, 9M-3, S1, S1b, S2, S2b, item 4 | Accepted (2026-10-05) |

## 7. Kegagalan, kesalahan, dan estimasi yang meleset
Hasil yang tidak sesuai harapan: C0–C2 tidak memenuhi timing (penyebab terukur: pembagi dan memori tak berbank); M10K tidak terpakai di Fase 2; C4c dan S8 tidak diadopsi; S2 netral; S2b tidak lolos aturannya seperti tertulis; Fmax seed terendah K4 69,43 MHz.
Estimasi yang meleset: ALM dan register Keccak K0 (Fase 7), siklus Keccak per operasi (≈2 × perkiraan), ALM penambahan W2 (+11 vs +100–300), sampler + C5 lebih kecil dari sponge sendirian (tidak diselidiki), ALM inti 9c (20.000 vs 17.620,5), siklus Encaps 9c (11.500 vs 10.691), S2 siklus (+12/+14/+22 vs +6/+7/+11), Fmax S2 (74,1 vs 76–80), latensi S2.
Cacat dan kesalahan proses yang ditemukan dan diperbaiki: kondisi balapan start di testbench Fase 1; properti formal salah yang ditangkap k-induksi; harness formal yang membuat ROM jadi state bebas (Fase 3); dua cacat RTL Fase 8 (tag valid tanpa reset, sampler bersamaan dengan `done_o`); bukti formal vacuous Fase 9b; kontrol negatif pertama yang tidak valid (Fase 5, 9a, item 4 `ncthrld` dan `ncgrant`); `%Warning` palsu "0 warnings" dari top yang tak ditemukan (Fase 5M); perintah `pkill -f` yang mematikan shell sendiri; direktori Quartus terhapus saat kompilasi (Fase 2); VS Code crash mematikan kompilasi paralel (9M); salah baca satu pertanyaan status sehingga antrean dihentikan lalu dipulihkan.
Batas waktu formal (TIMEOUT): P1 dan NC-E1-4 pada `mlkem_core4`, NC-B7 pada `mlkem_core3`. P2 pada core4 dibuang karena gagal induksi tanpa invarian posisi program dan tidak diklaim terbukti.
Urutan kerja yang menyimpang dari rencana: rencana item 4 ditulis setelah RTL dan simulasi pertamanya (rencana menyatakannya); rencana 8c/8d dan 5M-S8 punya penyimpangan serupa yang dicatat di rencana masing-masing; tiga seed tambahan S2b dipilih setelah melihat enam seed (dilaporkan di samping, tidak ada yang dibuang); Fase 2 dimulai sebelum kotak Approval Fase 1 dicentang (atas instruksi tim; dicatat di `phase02.md`).

## 8. Apa yang tidak ditunjukkan
- Tidak ada hasil papan, tidak ada integrasi HPS (Fase 10), tidak ada perbandingan dengan perangkat lunak (Fase 11), tidak ada fitur keamanan lanjutan (Fase 12). Tidak ada klaim percepatan terhadap perangkat lunak, daya, atau ketahanan side-channel. Risiko yang sudah diketahui: HPS Cortex-A9 jauh lebih kuat daripada MCU 20 MHz di literatur dan overhead jembatan dapat menghapus keuntungan.
- Fmax dan latensi dari timing statis kernel-only dengan virtual pin; tidak mencakup pin I/O, jembatan HPS-FPGA, atau clock nyata di papan. Derau seed 3–11 MHz membatasi pernyataan di bawah ukuran itu.
- Vektor ACVP yang dipakai adalah vektor sampel NIST (keyGen 25, encapsulation 25, decapsulation 10 untuk ML-KEM-768); ML-KEM-512 dan 1024 tidak diuji.
- Model formal memakai stub protokol; sifat yang dibuktikan adalah kontrol dan rentang, bukan nilai.
- Konstan-waktu = invarian jumlah siklus; KeyGen bervariasi sedikit karena pengambilan sampel penolakan matriks A dari ρ publik (8.344–8.397 siklus pada seed ACVP).

## 9. Yang masih menunggu tim
1. ADR 0033 (inti Fase 9 sebagaimana dibangun) masih Proposed (PENDING #33). ADR hasil 9M diterima 2026-10-05 (K4 di atas K3, K2, K1b); ADR 0042 (K3) tidak lolos aturannya seperti tertulis, tetapi diterima tim.
2. Papan DE10-Nano (#8; tidak ada papan per 2026-09-24): tanpa papan, Fase 10–12 tidak bisa dikerjakan. Lingkup proposal berhenti di Fase 9 (keputusan Jo 2026-10-04).
3. Pilihan lain yang masih terbuka: #1, #3 sampai #7, #10, #12 (sisi target, DMA, sumber keacakan, mode hibrida, baseline perangkat lunak kedua, alur protokol, penelusuran karya terdahulu, hitungan halaman lampiran). Subtema yang dipilih adalah 02, Hardware Cryptography Accelerator.
4. Kotak Approval `phase09.md` dan `phase9m.md` masih kosong; hanya anggota tim yang mencentangnya.
5. Bagian 3 proposal (halaman 4–6) belum ditulis.
6. Pekerjaan Batch 2 (S2, S2b, item 4) sudah di-commit di branch `phase9-submission`. Keluaran Quartus tidak pernah di-commit.

## 10. Peta berkas
| Kebutuhan | Lokasi |
|---|---|
| Hasil per fase | `docs/results/phase00.md` … `phase09.md`, `phase05m.md`, `phase9m.md` |
| Bukti per fase | `evidence/phase00` ... `evidence/phase09`, `evidence/phase05m`, `evidence/phase9m` (dengan `batch1/` dan `batch2/`), `evidence/quartus` |
| Keputusan | `docs/decisions/adr/ADR-0001 … ADR-0043`, ringkasan `docs/decisions/SUMMARY.md`, daftar terbuka `docs/decisions/PENDING.md` |
| RTL | `rtl/ntt`, `rtl/arith`, `rtl/mem`, `rtl/sched`, `rtl/keccak`, `rtl/sample`, `rtl/mlkem` |
| Uji dan model emas | `tb/golden`, `tb/*` (cocotb) |
| Skrip | `scripts/build` (generator ROM, pembangun laporan), `scripts/test` (verifikasi, regresi, smoke), `scripts/quartus` (seleksi hasil, analisis jalur, arsip) |
| Formal | `formal/phase*` (properti), `formal/run/` (`run_formal_*.py`) |
| Quartus | `quartus/phase*_*/` (proyek dan SDC; keluaran diarsipkan di luar repo) |
| Laporan PDF per fase (0–9) | `docs/reports/CHIPATON_Phase<N>_Report.pdf`; laporan lengkap ini: `docs/reports/CHIPATON_COMPLETE_REPORT.pdf` (dibangun oleh `scripts/build/build_complete_report.py`); laporan Fase 9M: `docs/reports/CHIPATON_Phase9M_Report.pdf` (dibangun oleh `scripts/build/build_phase9m_report.py`) |

"""

if __name__ == "__main__":
    build()
