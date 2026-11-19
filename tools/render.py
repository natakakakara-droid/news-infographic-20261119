#!/usr/bin/env python3
"""Render the news-image-20261119 entry: a one-page newspaper summing up the
world news of Thursday 19 November 2026, drawn deterministically with Pillow.
Writes entry.png (1024x1024) next to the repository root.

Run:  python3 tools/render.py   (from the repo root)
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ------------------------------------------------------------------ palette
PAPER = (250, 246, 238)     # warm paper
INK = (22, 32, 44)          # near-black
NAVY = (18, 42, 74)         # deep navy
RED = (176, 32, 38)         # headline red
TEAL = (14, 110, 120)       # accent teal
GOLD = (198, 150, 40)       # gold
GREY = (88, 100, 112)       # secondary text
RULE = (205, 194, 172)      # hairline
CREAM = (238, 232, 214)     # panel fill
SKY = (168, 205, 228)       # pale sky
SEA = (38, 98, 132)         # sea blue
ORANGE = (233, 122, 26)     # sunset orange
WHITE = (255, 255, 255)
DARKPANEL = (24, 48, 80)    # dark icon panel

# ------------------------------------------------------------------ fonts
FDIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FDIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FDIR, "DejaVuSerif.ttf")
SANS_B = os.path.join(FDIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FDIR, "DejaVuSans.ttf")
ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(d, text, fnt, max_w):
    """Greedy wrap; returns lines that fit inside max_w."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def text_block(d, x, y, text, fnt, color, max_w, leading):
    """Draw wrapped text; returns the y just below the last line."""
    for line in wrap_text(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def hline(d, x0, x1, y, color, width=1):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


def kicker(d, x, y, text, fnt, color=RED):
    d.text((x, y), text, font=fnt, fill=color)
    return y + fnt.size + 4


# ------------------------------------------------------------------ icons
def flag_us(d, x, y, w, h):
    """Stars and stripes, simplified: 7 red stripes + blue canton + dots."""
    stripe = h / 13.0
    for i in range(13):
        if i % 2 == 0:
            d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                        fill=RED)
    cw, ch = w * 0.4, stripe * 7
    d.rectangle([x, y, x + cw, y + ch], fill=NAVY)
    for r in range(4):
        for c in range(5):
            px = x + cw * (0.12 + 0.19 * c)
            py = y + ch * (0.16 + 0.24 * r)
            d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=WHITE)


def flag_cn(d, x, y, w, h):
    """China: red field, one big gold star + four small ones."""
    d.rectangle([x, y, x + w, y + h], fill=RED)
    cx, cy, r = x + w * 0.22, y + h * 0.28, h * 0.20
    star(d, cx, cy, r, r * 0.45, GOLD)
    for sx, sy in [(0.52, 0.16), (0.66, 0.28), (0.66, 0.48), (0.52, 0.60)]:
        star(d, x + w * sx, y + h * sy, h * 0.09, h * 0.04, GOLD)


def flag_ru(d, x, y, w, h):
    """Russia: white, blue, red horizontal bands."""
    d.rectangle([x, y, x + w, y + h / 3], fill=WHITE)
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 90, 180))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=RED)


def star(d, cx, cy, r_out, r_in, color):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / 5 - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=color)


def skyline(d, x, y, w, h):
    """Shenzhen dusk skyline: dark towers over a gold horizon."""
    d.rectangle([x, y, x + w, y + h], fill=DARKPANEL)
    horizon = y + h * 0.72
    d.rectangle([x, horizon, x + w, y + h], fill=(214, 164, 62))
    towers = [(0.00, 0.62), (0.10, 0.42), (0.20, 0.55), (0.30, 0.30),
              (0.42, 0.48), (0.52, 0.36), (0.63, 0.58), (0.72, 0.44),
              (0.83, 0.52), (0.92, 0.38)]
    for fx, fh in towers:
        tw = w * 0.09
        tx = x + w * fx
        th = h * fh
        d.rectangle([tx, horizon - th, tx + tw, horizon], fill=INK)
        for wy in range(3):
            for wx in range(2):
                d.rectangle([tx + 3 + wx * (tw - 6) / 2, horizon - th + 6 + wy * 12,
                             tx + 6 + wx * (tw - 6) / 2, horizon - th + 10 + wy * 12],
                            fill=GOLD)
    d.ellipse([x + w * 0.78, y + h * 0.10, x + w * 0.90, y + h * 0.10 + w * 0.12],
              fill=(240, 214, 140))


def capitol(d, x, y, w, h):
    """US Capitol dome, flat navy on cream."""
    d.rectangle([x, y, x + w, y + h], fill=CREAM)
    cx = x + w / 2
    base = y + h * 0.86
    d.rectangle([x + w * 0.12, base, x + w * 0.88, base + h * 0.07], fill=NAVY)
    d.rectangle([x + w * 0.18, base - h * 0.10, x + w * 0.82, base], fill=NAVY)
    for i in range(6):
        colx = x + w * (0.22 + i * 0.115)
        d.rectangle([colx, base - h * 0.34, colx + w * 0.05, base - h * 0.10],
                    fill=NAVY)
    d.rectangle([x + w * 0.18, base - h * 0.40, x + w * 0.82, base - h * 0.34],
                fill=NAVY)
    d.pieslice([cx - w * 0.26, base - h * 0.78, cx + w * 0.26, base - h * 0.26],
               180, 360, fill=NAVY)
    d.rectangle([cx - 2, base - h * 0.92, cx + 2, base - h * 0.72], fill=NAVY)
    d.ellipse([cx - 4, base - h * 0.96, cx + 4, base - h * 0.88], fill=GOLD)


def palm_sun(d, x, y, w, h):
    """Vice City sunset: orange sun disc + black palm silhouette."""
    d.rectangle([x, y, x + w, y + h], fill=(250, 226, 190))
    cx, cy = x + w * 0.5, y + h * 0.46
    for r, col in [(44, (244, 164, 96)), (34, ORANGE), (24, (214, 84, 32))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.rectangle([x, y + h * 0.78, x + w, y + h], fill=(52, 44, 66))
    tx, ty = x + w * 0.30, y + h * 0.80
    d.line([(tx, ty), (tx + 4, ty - h * 0.34), (tx + 8, ty - h * 0.44)],
           fill=INK, width=5, joint="curve")
    top = (tx + 8, ty - h * 0.44)
    for ang in (-80, -45, -10, 25, 60):
        a = math.radians(ang - 90)
        ex = top[0] + 36 * math.cos(a)
        ey = top[1] + 20 * math.sin(a) + 6
        mid = ((top[0] + ex) / 2 + 6, (top[1] + ey) / 2 - 8)
        d.line([top, mid, (ex, ey)], fill=INK, width=4, joint="curve")


def probe(d, x, y, w, h):
    """Voyager 1: dish antenna + bus + boom on a starry navy panel."""
    d.rectangle([x, y, x + w, y + h], fill=DARKPANEL)
    for sx, sy, sr in [(0.15, 0.2, 1.5), (0.8, 0.15, 1.5), (0.65, 0.3, 1),
                       (0.3, 0.75, 1.5), (0.9, 0.7, 1), (0.5, 0.12, 1)]:
        d.ellipse([x + w * sx - sr, y + h * sy - sr, x + w * sx + sr,
                   y + h * sy + sr], fill=WHITE)
    cx, cy = x + w * 0.56, y + h * 0.42
    # dish: tilted open ellipse
    d.ellipse([cx - 32, cy - 17, cx + 32, cy + 17], outline=GOLD, width=5)
    d.line([(cx - 22, cy + 10), (cx + 22, cy - 10)], fill=GOLD, width=2)
    # bus + boom
    d.rectangle([cx - 40, cy + 16, cx - 22, cy + 32], fill=(200, 200, 210))
    d.line([(cx - 31, cy + 24), (cx - 58, cy + 44)], fill=WHITE, width=2)
    d.ellipse([cx - 62, cy + 40, cx - 54, cy + 48], fill=WHITE)
    d.line([(cx + 24, cy + 12), (cx + 50, cy + 34)], fill=GOLD, width=2)


def eu_stars(d, x, y, w, h):
    """EU circle of stars on blue."""
    d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
    cx, cy = x + w * 0.5, y + h * 0.5
    for i in range(12):
        a = 2 * math.pi * i / 12 - math.pi / 2
        sx, sy = cx + 32 * math.cos(a), cy + 32 * math.sin(a)
        star(d, sx, sy, 6, 2.6, GOLD)


def cyclone(d, x, y, w, h):
    """Cyclone spiral: Archimedean spiral + rain drops on pale sky."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 233, 238))
    cx, cy = x + w * 0.5, y + h * 0.46
    pts = []
    for t in range(0, 540, 6):
        a = math.radians(t)
        r = 4 + 0.075 * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.line(pts, fill=TEAL, width=5, joint="curve")
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=TEAL)
    for dx in (-30, 0, 30):
        d.line([(cx + dx, y + h * 0.80), (cx + dx - 4, y + h * 0.94)],
               fill=SEA, width=3)


# ------------------------------------------------------------------ page
def render():
    img = Image.new("RGB", (1024, 1024), PAPER)
    d = ImageDraw.Draw(img)
    M = 36                      # margin
    W = 1024 - 2 * M            # 952 usable

    # ---- masthead: light, red rules, big serif title
    y = 30
    hline(d, M, 1024 - M, y, RED, 3)
    y += 12
    title = "THE WORLD IN ONE DAY"
    tf = load(SERIF_B, 62)
    d.text((512, y), title, font=tf, fill=NAVY, anchor="ma")
    y += 76
    hline(d, M, 1024 - M, y, RED, 2)
    y += 10
    df = load(SANS_B, 23)
    d.text((512, y), "THURSDAY, 19 NOVEMBER 2026",
           font=df, fill=INK, anchor="ma")
    y += 34
    sf = load(SANS, 17)
    d.text((512, y), "ONE DAY  •  ONE PAGE  •  THE NEWS THAT MATTERED",
           font=sf, fill=GREY, anchor="ma")
    y += 30
    hline(d, M, 1024 - M, y, INK, 2)

    # ---- feature row: summit left, two cards right
    fy = y + 14
    fh = 300
    fx, fw = M, 560
    # feature panel
    d.rectangle([fx, fy, fx + fw, fy + fh], outline=RULE, width=1)
    skyline(d, fx + 1, fy + 1, fw - 2, 104)
    # three flags under the skyline
    flag_y = fy + 114
    flag_w, flag_h = 118, 54
    gap = (fw - 3 * flag_w - 2 * 14) / 2
    labels = ["USA", "CHINA", "RUSSIA"]
    painters = [flag_us, flag_cn, flag_ru]
    for i, paint in enumerate(painters):
        fx0 = fx + 14 + i * (flag_w + 14)
        paint(d, fx0, flag_y, flag_w, flag_h)
        d.rectangle([fx0, flag_y, fx0 + flag_w, flag_y + flag_h],
                    outline=RULE, width=1)
        d.text((fx0 + flag_w / 2, flag_y + flag_h + 6), labels[i],
               font=load(SANS_B, 15), fill=GREY, anchor="ma")
    ty = flag_y + flag_h + 28
    hf = load(SERIF_B, 32)
    d.text((fx + 14, ty), "THREE POWERS, ONE TABLE",
           font=hf, fill=INK)
    ty += 42
    bf = load(SANS, 17)
    body = ("Trump, Xi and Putin meet in Shenzhen — the first "
            "trilateral of the three leaders. Ukraine, Iran, "
            "trade and nuclear arms are on the table.")
    ty = text_block(d, fx + 14, ty, body, bf, INK, fw - 28, 23)

    # right column: two stacked cards
    rx, rw = fx + fw + 20, W - fw - 20
    card_h = (fh - 14) // 2
    # card A: Jeffries
    cy = fy
    d.rectangle([rx, cy, rx + rw, cy + card_h], outline=RULE, width=1)
    capitol(d, rx + 1, cy + 1, 100, card_h - 2)
    tx = rx + 114
    kicker(d, tx, cy + 12, "WASHINGTON", load(SANS_B, 14))
    d.text((tx, cy + 34), "JEFFRIES IN LINE\nFOR SPEAKER",
           font=load(SERIF_B, 24), fill=INK)
    text_block(d, tx, cy + 90,
               "Nominated 251–11. A January vote could make him "
               "the first Black Speaker.",
               load(SANS, 14), GREY, rw - 128, 19)
    # card B: GTA VI
    cy = fy + card_h + 14
    d.rectangle([rx, cy, rx + rw, cy + card_h], outline=RULE, width=1)
    palm_sun(d, rx + 1, cy + 1, 100, card_h - 2)
    kicker(d, tx, cy + 12, "VICE CITY", load(SANS_B, 14))
    d.text((tx, cy + 34), "GTA VI IS OUT\nAT LAST",
           font=load(SERIF_B, 24), fill=INK)
    text_block(d, tx, cy + 90,
               "After 13 years, GTA VI launches worldwide; "
               "pre-orders pass $1.5bn.",
               load(SANS, 14), GREY, rw - 128, 19)

    # ---- middle band: three stories
    my = fy + fh + 16
    mh = 252
    col_w = (W - 2 * 16) // 3
    stories = [
        ("SPACE", "VOYAGER 1, ONE\nLIGHT-DAY OUT", probe,
         "After 48 years in space, the probe hits a new "
         "distance mark; NASA holds a briefing today to "
         "confirm it."),
        ("EUROPE", "€45BN LIFELINE\nFOR KYIV", eu_stars,
         "Brussels proposes a big loan for Ukraine's budget, "
         "to be repaid once Russia pays reparations."),
        ("WEATHER", "AKVAN BEARS DOWN\nON INDIA", cyclone,
         "A very severe cyclone nears the Andhra Pradesh "
         "coast; landfall is expected on Friday."),
    ]
    for i, (kick, head, painter, body) in enumerate(stories):
        cx0 = M + i * (col_w + 16)
        d.rectangle([cx0, my, cx0 + col_w, my + mh], outline=RULE, width=1)
        painter(d, cx0 + 1, my + 1, col_w - 2, 96)
        ty = my + 108
        kicker(d, cx0 + 12, ty, kick, load(SANS_B, 14))
        ty += 24
        d.text((cx0 + 12, ty), head, font=load(SERIF_B, 21), fill=INK)
        ty += 56
        text_block(d, cx0 + 12, ty, body, load(SANS, 15), GREY,
                   col_w - 24, 20)

    # ---- also today strip
    ay = my + mh + 16
    ah = 118
    d.rectangle([M, ay, 1024 - M, ay + ah], fill=NAVY)
    d.text((M + 14, ay + 10), "ALSO TODAY", font=load(SANS_B, 16),
           fill=(240, 214, 140))
    items = [
        ("NVIDIA AFTER HUANG", "Pay rises brought forward as "
         "acting chief Kress takes charge; H-chip sales to "
         "China stopped."),
        ("FED POINTS TO MORE HIKES", "Minutes show most officials "
         "expect further rate rises to tame inflation."),
        ("MOSCOW ACCUSES PARIS", "Lavrov says France has "
         "deployed troops to Ukraine, as leaders gather "
         "for APEC."),
    ]
    ix = M + 14
    iw = (W - 28 - 2 * 20) // 3
    for head, body in items:
        d.text((ix, ay + 36), head, font=load(SANS_B, 15), fill=WHITE)
        text_block(d, ix, ay + 58, body, load(SANS, 14),
                   (214, 222, 232), iw, 18)
        ix += iw + 20

    # ---- footer
    fy2 = ay + ah + 12
    hline(d, M, 1024 - M, fy2, RULE, 1)
    ff = load(ITALIC, 14)
    d.text((512, fy2 + 8),
           "Drawn from reports published 19 November 2026",
           font=ff, fill=GREY, anchor="ma")
    d.text((512, fy2 + 28),
           "Sources: Reuters  •  AP  •  CNN  •  NPR  •  NASA  •  AFP",
           font=load(SANS, 14), fill=GREY, anchor="ma")

    img.save(os.path.join(ROOT, "entry.png"), optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    render()
