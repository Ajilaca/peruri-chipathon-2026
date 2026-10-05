#!/usr/bin/env python3
"""Draw docs/roadmap.png: the phases as one connected flow (5 per row, arrows join every phase).

Status and the one-line results are copied from docs/results/*.md and docs/ROADMAP.md.
Phases 10-12 are pending and are enclosed by a dashed frame.
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "roadmap.png"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

NAVY, LIGHT, LINE, WHITE = "#0b2545", "#cfe3f7", "#2c6cb0", "#ffffff"

# (label, title, detail lines, status)  status: done | partial | current | pending
PHASES = [
    ("0", "Golden model", ["FIPS 203 in Python", "ACVP vectors", "errata checked"], "done"),
    ("1", "NTT baseline", ["L = 1", "NTT 897 cycles", "INTT 1153 cycles"], "done"),
    ("2", "Memory banking", ["bank map, 0 stalls", "at L = 1", "same cycle counts"], "done"),
    ("3", "Multi-lane", ["L = 1, 2, 4, 8", "L = 8 chosen", "NTT 113 / INTT 369"], "done"),
    ("4", "Pipeline", ["P = 6 (C3-P6)", "NTT 119 / INTT 375", "40 ns met"], "done"),
    ("5", "Arithmetic", ["Barrett reducer", "9,166-9,208 ALM", "18 DSP"], "done"),
    ("5M", "Memory, schedule", ["S10: 16 banks 1R1W", "NTT = INTT = 118", "median 44.32 MHz"], "done"),
    ("6", "K-PKE sequencer", ["cycles per op:", "KG 5,493, Enc 6,810", "Dec 3,121"], "done"),
    ("7", "Keccak-f[1600]", ["1 round per cycle", "SHA3 / SHAKE", "formal K1-K5"], "done"),
    ("8", "Keccak, samplers", ["2 rounds per cycle", "streaming samplers", "matrix A on the fly"], "done"),
    ("9", "Full ML-KEM-768", ["KeyGen, Encaps,", "Decaps in RTL", "ACVP 100% (sim)"], "current"),
    ("9M", "Optimisation", ["K4: 8,416 / 9,611 /", "12,989 cycles", "formal: 3 timeouts"], "partial"),
    ("10", "HPS integration", ["DE10-Nano board", "blocked: no board", "PENDING #8"], "pending"),
    ("11", "Benchmark", ["vs software on", "the same board", "not started"], "pending"),
    ("12", "Security", ["optional", "masking, TVLA", "not started"], "pending"),
]
BADGE = {"done": "DONE", "partial": "PARTIAL", "current": "CURRENT", "pending": "PENDING"}

S = 2  # supersampling factor
COLS, BW, BH, GX, GY, PAD = 5, 330, 280, 90, 170, 70
TOP = 200
rows = (len(PHASES) + COLS - 1) // COLS
W = PAD * 2 + COLS * BW + (COLS - 1) * GX
H = TOP + rows * BH + (rows - 1) * GY + 90
img = Image.new("RGB", (W * S, H * S), WHITE)
d = ImageDraw.Draw(img)


def F(path, size):
    return ImageFont.truetype(path, size * S)


f_title, f_label, f_name, f_text, f_small = F(BOLD, 44), F(BOLD, 36), F(BOLD, 27), F(FONT, 25), F(FONT, 24)


def S2(v):
    return v * S


def line(pts, width=4, color=LINE):
    d.line([(S2(x), S2(y)) for x, y in pts], fill=color, width=S2(width), joint="curve")


def arrow_head(x, y, direction):
    a = 14
    pts = {"r": [(x, y), (x - 2 * a, y - a), (x - 2 * a, y + a)],
           "d": [(x, y), (x - a, y - 2 * a), (x + a, y - 2 * a)]}[direction]
    d.polygon([(S2(px), S2(py)) for px, py in pts], fill=LINE)


def text(x, y, s, font, fill, anchor="la"):
    d.text((S2(x), S2(y)), s, font=font, fill=fill, anchor=anchor)


def dashed_rect(x0, y0, x1, y1, color, width=5, dash=16, gap=14, r=30):
    def hl(y, xa, xb):
        x = xa
        while x < xb:
            line([(x, y), (min(x + dash, xb), y)], width, color); x += dash + gap

    def vl(x, ya, yb):
        y = ya
        while y < yb:
            line([(x, y), (x, min(y + dash, yb))], width, color); y += dash + gap

    hl(y0, x0 + r, x1 - r); hl(y1, x0 + r, x1 - r); vl(x0, y0 + r, y1 - r); vl(x1, y0 + r, y1 - r)
    for cx, cy, a0 in ((x0 + r, y0 + r, 180), (x1 - r, y0 + r, 270), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90)):
        d.arc((S2(cx - r), S2(cy - r), S2(cx + r), S2(cy + r)), a0, a0 + 90, fill=color, width=S2(width))


text(PAD, 40, "ML-KEM-768 accelerator on DE10-Nano: project phases", f_title, NAVY)
text(PAD, 104, "Team J5 ITB, CHIP 2026. Current: Phase 9, submission. Results are simulation, formal and Quartus (kernel-only); no board yet.", f_small, LINE)

pos = []
for i in range(len(PHASES)):
    r, c = divmod(i, COLS)
    pos.append((PAD + c * (BW + GX), TOP + r * (BH + GY)))
idx = {p[0]: i for i, p in enumerate(PHASES)}

# dashed frame around the pending phases 10-12 (last three boxes, same row)
x10, y10 = pos[idx["10"]]
x12, _ = pos[idx["12"]]
dashed_rect(x10 - 34, y10 - 62, x12 + BW + 34, y10 + BH + 34, NAVY)
text((x10 + x12 + BW) / 2, y10 - 36, "PENDING: planned, not started", f_label, NAVY, "mm")

# arrows: horizontal inside a row, elbow from the end of a row to the start of the next
for i in range(len(PHASES) - 1):
    (x, y), (nx, ny) = pos[i], pos[i + 1]
    if ny == y:
        line([(x + BW + 6, y + BH / 2), (nx - 8, y + BH / 2)])
        arrow_head(nx - 4, y + BH / 2, "r")
    else:
        ym = y + BH + GY / 2
        line([(x + BW / 2, y + BH + 6), (x + BW / 2, ym), (nx + BW / 2, ym), (nx + BW / 2, ny - 12)])
        arrow_head(nx + BW / 2, ny - 4, "d")

for i, (lab, title, lines, st) in enumerate(PHASES):
    x, y = pos[i]
    d.rounded_rectangle((S2(x), S2(y), S2(x + BW), S2(y + BH)), radius=S2(18), fill=LIGHT, outline=LINE, width=S2(4))
    text(x + 24, y + 18, f"Phase {lab}", f_label, NAVY)
    text(x + 24, y + BH - 36, BADGE[st], f_small, LINE)
    text(x + 24, y + 70, title, f_name, NAVY)
    line([(x + 24, y + 112), (x + BW - 24, y + 112)], 2, LINE)
    for k, s in enumerate(lines):
        text(x + 24, y + 128 + k * 34, s, f_text, NAVY)

img = img.resize((W, H), Image.LANCZOS)
img.save(OUT)
print("wrote", OUT.relative_to(ROOT), img.size)
