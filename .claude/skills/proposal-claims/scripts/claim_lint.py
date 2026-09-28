#!/usr/bin/env python3
"""Lint proposal/docs text for claims this project does not allow (see CLAUDE.md §3, §8).

  claim_lint.py [paths...] [--words]      default path: docs/proposal
  claim_lint.py --selftest

Exit code 1 if any ERROR is found; WARN never fails the run. Heuristic, not a proof:
a clean run does not mean the text is correct, only that these known problems are absent.
Suppress a single line on purpose with  <!-- claim-lint: ok (reason) -->  in Markdown.
"""
import argparse, os, re, sys, tempfile

# Words that mark a sentence as *negating or scoping* a claim, so it is not an overclaim.
SCOPING = re.compile(r"\b(bukan|tidak|belum|tanpa|tahap lanjut|later stage|not|no longer|never|jangan|hindari|avoid)\b", re.I)

# Provenance markers: a quantitative sentence needs at least one of these.
PROVENANCE = re.compile(
    r"(\[\d+\]|\[[a-z ]*\d+[a-z ]*\]|ESTIMATE|MEASURED|perhitungan tim|inferensi tim|literatur|"
    r"\bTBD\b|\[\.\.\.\]|docs/evidence|datasheet|product table|tabel (produk )?Intel|Intel\'?s? (product )?table|fitter|hasil kutipan)", re.I)

METRIC = re.compile(
    r"\b(ALM|ALMs|LUT|LEs?|register|flip-?flop|M10K|DSP|Fmax|MHz|GHz|latensi|latency|throughput|"
    r"µs|us|ns|ms|siklus|cycles?|percepatan|speed-?up|lebih cepat|faster|watt|mW|daya|power|energi|energy)\b", re.I)

RULES = [
    # id, severity, regex, message, allow_if_scoped
    ("R1", "ERROR", r"kebal (terhadap )?(komputer )?kuantum|quantum[- ]?proof|unbreakable|tidak dapat (ditembus|dibobol)|100 ?% aman",
     "Overclaim. Allowed wording: 'dirancang mengikuti standar pasca-kuantum' / 'designed to follow PQC standards'.", True),
    ("R2", "ERROR", r"(terlindungi|dilindungi|tahan|kebal|resisten|protect\w*|resist\w*)\W+(\w+\W+){0,3}(side[- ]?channel|kanal samping|SCA|power analysis|analisis daya)",
     "Side-channel protection is NOT claimed at core stage (constant-time only; TVLA/masking = later stage). Scope it or remove it.", True),
    ("R3", "ERROR", r"\b415[.,]?000\b",
     "Template error: Cyclone V 5CSEBA6U23I7 has 166,036 registers (Intel product table). Use the datasheet/fitter value.", False),
    ("R4", "ERROR", r"yosys[^.\n]{0,80}(cyclone|ALM)|(cyclone|ALM)[^.\n]{0,80}yosys",
     "Yosys/generic-synthesis numbers must never be presented as Cyclone V resources (CLAUDE.md §5.1).", True),
    ("R5", "WARN", r"boros daya|power[- ]hungry|hemat daya|energy[- ]efficient|hemat energi",
     "Power/energy claim needs a measurement plan or a source. None exists yet.", True),
    ("R6", "WARN", r"\b(pertama (di|kali)|first (implementation|to)|belum pernah ada|tidak ada (yang lain|kompetitor)|novel first)\b",
     "Novelty absolutes are unsafe: prior art exists (e.g. Kyber NTT on Cyclone V). Scope with 'sejauh penelusuran kami'.", True),
    ("R7", "WARN", r"(lebih cepat|faster|percepatan|speed-?up|mempercepat)\W+(\w+\W+){0,6}(software|perangkat lunak|HPS|CPU|baseline)",
     "Speed-up vs software is unmeasured (HPS Cortex-A9 is far stronger than the 20 MHz MCU in the literature). Needs MEASURED evidence.", True),
    ("R8", "WARN", r"\b(secure|aman)\b[^.\n]{0,40}\b(dijamin|guaranteed)\b|\bdijamin aman\b",
     "'Guaranteed secure' is not something a prototype can claim.", True),
]


LIST_START = re.compile(r"^\s*([-*+•]\s|\d+[.)]\s|#{1,6}\s|\|)")


def paragraphs(text):
    """Yield (first_line_no, joined_text). Hard-wrapped lines of one paragraph are joined so
    a citation or a negation on the next line still counts; list items, headings and table
    rows stay separate."""
    buf, start = [], 0
    for lineno, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            if buf:
                yield start, " ".join(buf); buf = []
            continue
        if "claim-lint: ok" in line:
            continue
        if LIST_START.match(line) and buf:
            yield start, " ".join(buf); buf = []
        if not buf:
            start = lineno
        buf.append(line.strip())
    if buf:
        yield start, " ".join(buf)


def sentences(text):
    for lineno, para in paragraphs(text):
        for s in re.split(r"(?<=[.!?;])\s+(?=[A-Z0-9\u2018\u201c\[(])", para):
            if s.strip():
                yield lineno, s


def lint_text(text):
    findings = []
    for lineno, s in sentences(text):
        for rid, sev, rx, msg, allow_scoped in RULES:
            if re.search(rx, s, re.I):
                if allow_scoped and SCOPING.search(s):
                    continue
                if rid == "R3" and re.search(r"166[.,]?036", s):
                    continue        # sentence corrects the template with the datasheet value
                if rid == "R7" and re.search(r"\b(may|might|could|can|dapat|mungkin|bisa|small or negative)\b", s, re.I):
                    continue        # hedged statement about a risk, not a claim
                findings.append((sev, rid, lineno, msg, s.strip()))
        # Metric words + digits, ignoring calendar years and "siklus hidup" (= life cycle).
        probe = re.sub(r"siklus hidup|life ?cycle", " ", s, flags=re.I)
        probe = re.sub(r"\b(19|20)\d{2}\b", " ", probe)
        probe = re.sub(r"^\s*(\d+[.)]|[-*+•])\s+", "", probe)   # list marker is not a data point
        probe = re.sub(r"^\|\s*\d+\s*\|", " ", probe)          # table index cell
        probe = re.sub(r"\(\d+\)", " ", probe)                   # enumerators (1) (2)
        probe = re.sub(r"\b\d+\s*[x×]\s*\d+\b", " ", probe)     # multiplier modes 18x18
        probe = re.sub(r"\b(Phase|Fase|PENDING\s*#?|ADR|Section|Bagian|halaman|hlm|§)\s*\d+(-\d+)?", " ", probe, flags=re.I)
        if METRIC.search(probe) and re.search(r"(?<![A-Za-z\-\d])\d", probe) and not PROVENANCE.search(s):
            findings.append(("WARN", "R9", lineno,
                             "Quantitative claim without provenance: add a citation [n], or label ESTIMATE / MEASURED / 'perhitungan tim'.", s.strip()))
    return findings


def iter_files(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, _, files in os.walk(p):
                for f in sorted(files):
                    if f.lower().endswith((".md", ".txt", ".tex", ".rst")):
                        yield os.path.join(root, f)
        elif os.path.isfile(p):
            yield p


def run(paths, words=False):
    errors = warns = 0
    total_words = 0
    files = list(iter_files(paths))
    if not files:
        print(f"claim-lint: no .md/.txt files found in {paths}. Nothing was checked (this is NOT a pass).")
        return 2
    for f in files:
        text = open(f, encoding="utf-8", errors="replace").read()
        if "claim-lint: skip-file" in "\n".join(text.splitlines()[:6]):
            print(f"{f}: skipped (internal register; marked claim-lint: skip-file)")
            continue
        if words:
            n = len(re.findall(r"\w+", text)); total_words += n
            print(f"{f}: {n} words")
        for sev, rid, ln, msg, s in lint_text(text):
            print(f"{sev:5} {rid} {f}:{ln}: {msg}\n      > {s[:200]}")
            errors += sev == "ERROR"; warns += sev == "WARN"
    if words:
        print(f"total: {total_words} words (very rough: ~500-600 words per A4 page of plain text; tables/figures take more)")
    print(f"\nclaim-lint: {errors} error(s), {warns} warning(s)")
    return 1 if errors else 0


def selftest():
    bad = ("Desain ini kebal terhadap komputer kuantum. Chip terlindungi dari serangan side-channel. "
           "Template menulis 415.000 flip-flop. Hasil Yosys menunjukkan 3000 ALM pada Cyclone V. "
           "Sistem ini boros daya. Ini implementasi pertama di dunia. Akselerator 5x lebih cepat dari software. "
           "Desain memakai 2.500 ALM dan 240 MHz.")
    ids = {f[1] for f in lint_text(bad)}
    for want in ("R1", "R2", "R3", "R4", "R5", "R6", "R7", "R9"):
        assert want in ids, f"rule {want} did not fire: {sorted(ids)}"
    good = ("Klaim keamanan dinyatakan sebagai 'dirancang mengikuti standar pasca-kuantum', bukan 'kebal kuantum'. "
            "Ketahanan side-channel tidak diklaim pada tahap inti. "
            "Cyclone V 5CSEBA6U23I7 memiliki 41.910 ALM [22]. Satu polinomial 3.072 bit (perhitungan tim). "
            "OCAKE memerlukan 1,39 detik pada STM32 20 MHz [11]. Kutipan ESTIMATE: 3.000 ALM (metode: analitis).")
    got = lint_text(good)
    assert not [f for f in got if f[0] == "ERROR"], got
    assert not [f for f in got if f[1] == "R9"], got
    quiet = ("Kami memilih (1) evaluasi latensi pada alur PACE dan (2) verifikasi. DSP mode 18x18 dipakai di Phase 1.\n"
             "| 6 | Baseline kedua | Percepatan dapat kecil atau bahkan negatif | Phase 5 |\n"
             "Templat menulis 415.000 flip-flop, padahal tabel Intel menyebut 166.036 register.")
    got = [f for f in lint_text(quiet) if f[0] == "ERROR" or f[1] in ("R7", "R9")]
    assert not got, got
    still = lint_text("Desain memakai 3000 ALM dan 240 MHz (1).")
    assert any(f[1] == "R9" for f in still), "R9 must still fire on real numbers"
    print("selftest OK (claim_lint.py)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", default=["docs/proposal"])
    ap.add_argument("--words", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    return run(a.paths, a.words)


if __name__ == "__main__":
    sys.exit(main())
