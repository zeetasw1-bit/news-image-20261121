#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news summary image (1024x1024 PNG).

Local build tool only: it runs on this machine (needs Pillow + DejaVu fonts)
and writes entry.png. The graded entrypoint is main.py, which only copies
entry.png into the output directory, so the graded run needs no network and
no third-party library and is byte-for-byte deterministic.
"""

import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (247, 242, 231)
INK = (20, 32, 48)
NAVY = (20, 38, 63)
NAVY_DARK = (13, 27, 45)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
MUTED = (90, 96, 104)
RULE = (210, 203, 188)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_text(draw, text, fnt_path, start_size, max_w, max_lines, min_size=14):
    """Largest font size (<= start_size) whose wrap fits max_lines."""
    size = start_size
    while size > min_size:
        fnt = font(fnt_path, size)
        if len(wrap(draw, text, fnt, max_w)) <= max_lines:
            return fnt, wrap(draw, text, fnt, max_w)
        size -= 1
    fnt = font(fnt_path, min_size)
    return fnt, wrap(draw, text, fnt, max_w)


def draw_lines(draw, lines, fnt, x, y, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def star_points(cx, cy, r_out, r_in, points=5, rot=-90):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def flag_us(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    for i in range(7):
        if i % 2 == 0:
            d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7], fill=(178, 34, 52))
    d.rectangle([x, y, x + w * 0.4, y + h * 4 / 7], fill=(30, 58, 95))
    for r in range(3):
        for c in range(4):
            sx = x + 6 + c * (w * 0.4 - 12) / 3
            sy = y + 5 + r * (h * 4 / 7 - 10) / 2
            d.ellipse([sx, sy, sx + 3, sy + 3], fill=WHITE)


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=INK, width=2)
    d.polygon(star_points(x + w * 0.22, y + h * 0.28, h * 0.22, h * 0.09), fill=(255, 222, 0))
    for sx, sy in [(0.55, 0.18), (0.68, 0.32), (0.66, 0.55), (0.5, 0.62)]:
        d.polygon(star_points(x + w * sx, y + h * sy, h * 0.10, h * 0.04), fill=(255, 222, 0))


def flag_ru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    d.rectangle([x, y, x + w, y + h / 3], fill=WHITE)
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))


# ---- icons, drawn inside a square box (x, y, s) ---------------------------

def icon_ship(d, x, y, s, color):
    # tanker hull + containers + flame, over waves
    d.rectangle([x + s * 0.08, y + s * 0.55, x + s * 0.92, y + s * 0.72],
                fill=color)
    d.polygon([(x + s * 0.08, y + s * 0.55), (x + s * 0.92, y + s * 0.55),
               (x + s * 0.82, y + s * 0.72), (x + s * 0.18, y + s * 0.72)],
              fill=color)
    d.rectangle([x + s * 0.55, y + s * 0.30, x + s * 0.85, y + s * 0.55],
                fill=color)
    d.rectangle([x + s * 0.15, y + s * 0.38, x + s * 0.50, y + s * 0.55],
                outline=color, width=4)
    d.polygon([(x + s * 0.30, y + s * 0.30), (x + s * 0.42, y + s * 0.02),
               (x + s * 0.54, y + s * 0.30)], fill=(230, 126, 34))
    for i, wx in enumerate([0.05, 0.35, 0.65]):
        d.arc([x + s * wx, y + s * 0.78, x + s * (wx + 0.30), y + s * 0.98],
              180, 360, fill=color, width=4)


def icon_leaf_globe(d, x, y, s, color):
    cx, cy, r = x + s * 0.42, y + s * 0.52, s * 0.34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=5)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=color, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=color, width=3)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 360, fill=color, width=3)
    lx, ly = x + s * 0.78, y + s * 0.22
    d.polygon([(lx, ly - s * 0.16), (lx + s * 0.16, ly + s * 0.05),
               (lx, ly + s * 0.20), (lx - s * 0.16, ly + s * 0.05)],
              fill=(46, 139, 87))
    d.line([lx, ly + s * 0.18, lx - s * 0.05, ly + s * 0.32], fill=(46, 139, 87), width=4)


def icon_chart_down(d, x, y, s, color):
    pts = [(x + s * 0.06, y + s * 0.25), (x + s * 0.30, y + s * 0.42),
           (x + s * 0.52, y + s * 0.38), (x + s * 0.72, y + s * 0.62),
           (x + s * 0.94, y + s * 0.80)]
    d.line(pts, fill=color, width=7, joint="curve")
    ax, ay = pts[-1]
    d.polygon([(ax, ay), (ax - s * 0.16, ay - s * 0.02), (ax - s * 0.02, ay - s * 0.16)],
              fill=color)
    for gx in [0.06, 0.30, 0.52, 0.72, 0.94]:
        d.line([x + s * gx, y + s * 0.88, x + s * gx, y + s * 0.94],
               fill=MUTED, width=3)


def icon_badge(d, x, y, s, color):
    cx, cy = x + s * 0.5, y + s * 0.48
    d.polygon(star_points(cx, cy, s * 0.42, s * 0.18), fill=color)
    d.ellipse([cx - s * 0.13, cy - s * 0.13, cx + s * 0.13, cy + s * 0.13],
              fill=WHITE)
    d.ellipse([cx - s * 0.06, cy - s * 0.06, cx + s * 0.06, cy + s * 0.06],
              fill=color)


def icon_quake(d, x, y, s, color):
    pts = []
    xs = [0.04, 0.16, 0.26, 0.38, 0.48, 0.60, 0.70, 0.82, 0.96]
    ys = [0.55, 0.55, 0.20, 0.80, 0.45, 0.65, 0.30, 0.70, 0.55]
    for fx, fy in zip(xs, ys):
        pts.append((x + s * fx, y + s * fy))
    d.line(pts, fill=color, width=6, joint="curve")
    d.line([x + s * 0.04, y + s * 0.88, x + s * 0.96, y + s * 0.88],
           fill=color, width=5)
    for cx in [0.22, 0.55, 0.82]:
        d.line([x + s * cx, y + s * 0.88, x + s * (cx - 0.05), y + s * 0.99],
               fill=color, width=4)


def icon_bridge(d, x, y, s, color):
    d.arc([x + s * 0.05, y + s * 0.30, x + s * 0.95, y + s * 1.10], 180, 360,
          fill=color, width=7)
    d.line([x + s * 0.05, y + s * 0.72, x + s * 0.95, y + s * 0.72],
           fill=color, width=7)
    for fx in [0.20, 0.38, 0.50, 0.62, 0.80]:
        top = y + s * (0.72 - 0.30 * (1 - ((fx - 0.5) * 2) ** 2))
        d.line([x + s * fx, top, x + s * fx, y + s * 0.72], fill=color, width=4)
    d.polygon([(x + s * 0.06, y + s * 0.30), (x + s * 0.16, y + s * 0.08),
               (x + s * 0.26, y + s * 0.30)], fill=color)


# ---- page -----------------------------------------------------------------

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 124], fill=GOLD)
    title_f = font(SERIF_B, 52)
    d.text((32, 20), "THE WORLD IN ONE DAY", font=title_f, fill=WHITE)
    date_f = font(SANS_B, 27)
    d.text((32, 82), "SATURDAY  ·  21 NOVEMBER 2026", font=date_f, fill=GOLD)

    # Hero: trilateral summit
    hx, hy, hw, hh = 24, 140, W - 48, 220
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=CARD, outline=RULE, width=2)
    d.rectangle([hx, hy, hx + 10, hy + hh], fill=RED)
    fw, fh = 96, 64
    fx = hx + 34
    d.rectangle([fx - 10, hy + 20, fx + 3 * fw + 2 * 12 + 10, hy + 20 + fh + 20],
                fill=(238, 233, 220))
    flag_us(d, fx, hy + 30, fw, fh)
    flag_cn(d, fx + fw + 12, hy + 30, fw, fh)
    flag_ru(d, fx + 2 * (fw + 12), hy + 30, fw, fh)
    tx = fx + 3 * fw + 2 * 12 + 26
    kick_f = font(SANS_B, 21)
    d.text((tx, hy + 26), "SUMMIT  ·  SHENZHEN, CHINA", font=kick_f,
           fill=RED)
    head_f, head_lines = fit_text(
        d, "Trump, Xi & Putin meet in first trilateral summit",
        SANS_B, 40, hw - (tx - hx) - 28, 2)
    y = draw_lines(d, head_lines, head_f, tx, hy + 56, INK, 48)
    sub_f, sub_lines = fit_text(
        d, "Leaders agree to open talks on cutting nuclear risks at the APEC gathering.",
        SANS, 24, hw - (tx - hx) - 28, 2)
    draw_lines(d, sub_lines, sub_f, tx, y + 6, MUTED, 31)
    # small caption under the flags
    cap_f = font(SANS, 17)
    d.text((fx, hy + 200), "U.S.  ·  China  ·  Russia", font=cap_f, fill=MUTED)

    # Story tiles
    stories = [
        ("CONFLICT · GULF", (178, 34, 34), icon_ship,
         "Hormuz attacks at wartime high",
         "Iran strikes a Bahrain industrial site; oil shipments through the strait fall 15%."),
        ("CLIMATE · ANTALYA", (34, 120, 70), icon_leaf_globe,
         "COP31 deadlocked over fossil fuels",
         "Climate talks run into overtime over fossil fuels."),
        ("MARKETS · NEW YORK", (178, 34, 34), icon_chart_down,
         "AI sell-off sinks US stocks",
         "S&P 500 falls 3.7% into correction; Nvidia halts H200 AI chip exports to China."),
        ("JUSTICE · MEXICO", (146, 110, 32), icon_badge,
         "Mexico captures 'El Chapo Isidro'",
         "Cartel boss Meza Flores arrested in Sinaloa; 11 killed in the violence."),
        ("DISASTER · PERU", (196, 90, 20), icon_quake,
         "Magnitude 6.9 quake hits Peru",
         "Earthquake shakes the Andes in central Peru."),
        ("DIPLOMACY · EUROPE", (30, 80, 160), icon_bridge,
         "UK and EU seal post-Brexit reset",
         "Food, carbon and youth-mobility deals agreed after years of talks."),
    ]
    cols, rows = 3, 2
    gx0, gy0 = 24, 376
    gap = 16
    tw_ = (W - 2 * 24 - (cols - 1) * gap) // cols
    th_ = 280
    for i, (kick, color, icon, head, sub) in enumerate(stories):
        r, c = divmod(i, cols)
        x = gx0 + c * (tw_ + gap)
        y = gy0 + r * (th_ + gap)
        d.rectangle([x, y, x + tw_, y + th_], fill=CARD, outline=RULE, width=2)
        d.rectangle([x, y, x + tw_, y + 8], fill=color)
        icon(d, x + 18, y + 24, 64, color)
        kf = font(SANS_B, 16)
        d.text((x + 92, y + 34), kick, font=kf, fill=color)
        hf, hlines = fit_text(d, head, SANS_B, 28, tw_ - 36, 2)
        yy = draw_lines(d, hlines, hf, x + 18, y + 108, INK, 34)
        sf, slines = fit_text(d, sub, SANS, 19, tw_ - 36, 3)
        draw_lines(d, slines, sf, x + 18, yy + 10, MUTED, 25)

    # Footer
    fy = gy0 + 2 * th_ + gap + 12
    d.line([24, fy, W - 24, fy], fill=RULE, width=2)
    ff = font(SANS, 18)
    d.text((24, fy + 12),
           "All stories happened or were first reported on 21 November 2026  ·  Sources: wire reports of the day",
           font=ff, fill=MUTED)

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT}: {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
