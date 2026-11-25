#!/usr/bin/env python3
"""Render the 25 November 2026 world-news front page to page.png.

Build-time renderer: run with PIL + real TTF fonts (system Noto, OFL)
during the build session. The entry program (main.py) only copies the
finished page.png to /output/entry.png. Output is deterministic:
1024x1024 PNG, no network, no timestamps in the file.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C

W, H = 1024, 1024
MARGIN = 28
CW = W - 2 * MARGIN  # 968

PAPER = (247, 240, 219)
INK = (26, 26, 26)
RED = (166, 30, 34)
MUTED = (107, 98, 82)
RULE = (26, 26, 26)
LIGHT_RULE = (180, 168, 140)
PANEL = (252, 247, 232)
SEA = (198, 214, 208)
LAND = (232, 216, 176)
LAND_EDGE = (150, 132, 96)
SKY = (31, 58, 92)

FDIR = "/usr/share/fonts/truetype/noto/"


def font(name, size):
    return ImageFont.truetype(FDIR + name, size)


F_BLACK = lambda s: font("NotoSerifDisplay-Black.ttf", s)
F_DBOLD = lambda s: font("NotoSerifDisplay-Bold.ttf", s)
F_DSEMI = lambda s: font("NotoSerifDisplay-SemiBold.ttf", s)
F_SBOLD = lambda s: font("NotoSerif-Bold.ttf", s)
F_SERIF = lambda s: font("NotoSerif-Regular.ttf", s)
F_ITAL = lambda s: font("NotoSerif-Italic.ttf", s)
F_SANS = lambda s: font("NotoSans-Regular.ttf", s)
F_SANSB = lambda s: font("NotoSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_lines(draw, x, y, lines, fnt, fill, leading=None, align="left", box_w=None):
    """Draw lines starting at (x, y); returns y after the last line."""
    if leading is None:
        leading = int(fnt.size * 1.18)
    for line in lines:
        if align == "center":
            w = draw.textlength(line, font=fnt)
            draw.text((x + (box_w - w) / 2, y), line, font=fnt, fill=fill)
        else:
            draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def chip(d, x, y, text, fnt, bg, fg=(255, 255, 255), pad_x=5, pad_y=2):
    """Small pill label; returns its width."""
    w = int(d.textlength(text, font=fnt)) + 2 * pad_x
    h = fnt.size + 2 * pad_y
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    d.text((x + pad_x, y + pad_y - 1), text, font=fnt, fill=fg)
    return w


TAG_COLOURS = {
    "CONFIRMED": (46, 107, 52),
    "OFFICIAL": (31, 78, 121),
    "REPORTED": (146, 96, 0),
    "CLAIM": (166, 30, 34),
}


def tag(d, x, y, label):
    return chip(d, x, y, label, F_SANSB(8), TAG_COLOURS[label])


# ------------------------------------------------------------------ map data
# Simplified continent outlines as (lon, lat) polygons.
NA = [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-65, 62),
      (-55, 47), (-60, 45), (-70, 42), (-75, 35), (-80, 26), (-84, 30),
      (-90, 21), (-97, 16), (-92, 15), (-83, 9), (-79, 9), (-85, 14),
      (-97, 16), (-105, 20), (-112, 25), (-117, 32), (-122, 37), (-124, 48),
      (-130, 55), (-140, 60), (-155, 58), (-165, 60)]
SA = [(-79, 9), (-77, 4), (-75, 6), (-70, 10), (-62, 10), (-55, 6), (-51, 4),
      (-50, 0), (-44, -3), (-35, -8), (-38, -15), (-41, -22), (-48, -28),
      (-53, -33), (-58, -38), (-65, -42), (-68, -50), (-70, -54), (-73, -48),
      (-73, -40), (-72, -30), (-70, -20), (-76, -14), (-80, -5), (-81, 1),
      (-80, 6)]
EU = [(-10, 36), (-9, 43), (-2, 44), (-1, 48), (2, 51), (5, 53), (8, 57),
      (12, 58), (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (30, 70),
      (25, 71), (20, 70), (15, 68), (12, 65), (6, 61), (5, 58), (8, 55),
      (10, 54), (14, 54), (18, 52), (20, 50), (23, 47), (23, 44), (20, 42),
      (16, 40), (12, 42), (8, 44), (3, 43), (0, 40), (-2, 37), (-6, 36),
      (-9, 37)]
AF = [(-17, 15), (-16, 21), (-15, 27), (-10, 31), (-6, 34), (0, 36),
      (10, 37), (11, 34), (20, 32), (30, 31), (32, 31), (34, 28), (37, 22),
      (39, 18), (43, 12), (48, 11), (51, 11), (48, 5), (42, 0), (40, -6),
      (38, -12), (35, -18), (33, -25), (29, -31), (26, -34), (20, -35),
      (17, -31), (15, -27), (13, -20), (12, -15), (13, -10), (9, -4), (9, 1),
      (9, 5), (4, 6), (-3, 5), (-8, 5), (-13, 8), (-17, 12)]
AS = [(28, 41), (33, 42), (36, 42), (40, 41), (44, 41), (48, 40), (52, 38),
      (56, 38), (60, 39), (65, 40), (70, 42), (75, 44), (80, 46), (85, 50),
      (90, 54), (95, 58), (100, 60), (105, 62), (110, 64), (115, 66),
      (120, 68), (125, 70), (130, 71), (135, 72), (140, 72), (145, 72),
      (150, 70), (155, 70), (160, 69), (165, 68), (170, 67), (175, 66),
      (178, 65), (178, 62), (172, 60), (165, 60), (160, 55), (158, 52),
      (155, 50), (150, 48), (145, 44), (142, 42), (140, 39), (138, 37),
      (135, 35), (132, 34), (130, 33), (128, 33), (126, 35), (124, 38),
      (122, 39), (120, 35), (122, 32), (120, 28), (116, 23), (112, 21),
      (109, 18), (106, 10), (104, 9), (103, 2), (101, 4), (100, 7), (99, 10),
      (97, 15), (94, 17), (92, 21), (89, 22), (86, 20), (83, 17), (80, 13),
      (80, 8), (77, 8), (74, 13), (72, 20), (69, 22), (66, 25), (61, 25),
      (57, 25), (56, 26), (59, 22), (55, 17), (48, 14), (43, 12), (39, 20),
      (37, 25), (35, 29), (34, 31), (36, 36), (33, 36), (30, 36)]
JP = [(130, 31), (132, 33), (134, 34), (137, 35), (139, 37), (140, 39),
      (141, 41), (143, 42), (145, 44), (142, 44), (140, 40), (138, 37),
      (136, 35), (133, 34)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
      (-3, 50)]
AU = [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
      (140, -38), (147, -39), (150, -37), (153, -27), (146, -19), (142, -11),
      (135, -12), (130, -13), (126, -14), (122, -17), (118, -20)]
NZ = [(167, -45), (170, -42), (174, -39), (177, -38), (174, -41), (171, -43)]


def project(lon, lat, bx, by, bw, bh):
    x = bx + (lon + 168.0) / 360.0 * bw
    y = by + (78.0 - lat) / 123.0 * bh
    return (x, y)


def draw_map(d, bx, by, bw, bh):
    d.rectangle([bx, by, bx + bw, by + bh], fill=SEA)
    for poly in (NA, SA, EU, AF, AS, JP, UK, AU, NZ):
        pts = [project(lon, lat, bx, by, bw, bh) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # equator + tropics, faint
    for lat, col in ((0, (150, 165, 158)), (23.4, (160, 172, 162))):
        _, ey = project(0, lat, bx, by, bw, bh)
        d.line([bx, ey, bx + bw, ey], fill=col, width=1)
    for num, lon, lat, region, dx, dy in C.PINS:
        px, py = project(lon, lat, bx, by, bw, bh)
        cx, cy = px + dx, py + dy
        col = C.REGION_COLOURS[region]
        if dx or dy:
            d.line([px, py, cx, cy], fill=col, width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=col)
        r = 8
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col,
                  outline=(255, 255, 255), width=1)
        f = F_SANSB(9)
        tw = d.textlength(str(num), font=f)
        d.text((cx - tw / 2, cy - 6), str(num), font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- illustrations
def banner(d, x, y, w, text, fnt=None):
    """Emblematic figure as a banner across the bottom of an illustration."""
    fnt = fnt or F_SANSB(11)
    tw = d.textlength(text, font=fnt)
    bw = min(w, tw + 12)
    d.rectangle([x, y, x + bw, y + fnt.size + 7], fill=RED)
    d.text((x + 6, y + 3), text, font=fnt, fill=(255, 255, 255))


def ill_lead1(d, x, y, w, h):
    # Arabian peninsula + Red Sea, drone arrows from Yemen, burst at Ras Tanura
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    arabia = [(0.30, 0.05), (0.42, 0.02), (0.55, 0.10), (0.62, 0.25),
              (0.60, 0.45), (0.55, 0.62), (0.45, 0.75), (0.34, 0.72),
              (0.28, 0.55), (0.24, 0.35), (0.26, 0.15)]
    pts = [(x + fx * w, y + fy * h) for fx, fy in arabia]
    d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # Red Sea (left of Arabia)
    d.polygon([(x + 0.18 * w, y + 0.30 * h), (x + 0.26 * w, y + 0.28 * h),
               (x + 0.30 * w, y + 0.62 * h), (x + 0.24 * w, y + 0.70 * h)],
              fill=(150, 185, 200))
    # Gulf (right)
    d.polygon([(x + 0.60 * w, y + 0.28 * h), (x + 0.66 * w, y + 0.26 * h),
               (x + 0.68 * w, y + 0.48 * h), (x + 0.62 * w, y + 0.50 * h)],
              fill=(150, 185, 200))
    # drone arrows from Yemen (bottom-left) toward Ras Tanura (top-right)
    for i, (sx, sy) in enumerate([(0.30, 0.68), (0.34, 0.72), (0.38, 0.66)]):
        ex, ey = x + 0.64 * w, y + 0.30 * h
        ax, ay = x + sx * w, y + sy * h
        d.line([ax, ay, ex - 12, ey + 12], fill=RED, width=2)
        d.polygon([(ex, ey), (ex - 12, ey + 2), (ex - 2, ey + 12)], fill=RED)
    # burst at Ras Tanura
    bx, by = x + 0.64 * w, y + 0.30 * h
    for ang in range(0, 360, 45):
        import math
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d.line([bx + dx * 5, by + dy * 5, bx + dx * 13, by + dy * 13],
               fill=(200, 90, 20), width=2)
    d.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=(200, 90, 20))
    d.text((x + 8, y + 4), "RED SEA", font=F_SANSB(8), fill=MUTED)
    d.text((x + w - 52, y + 4), "GULF", font=F_SANSB(8), fill=MUTED)
    banner(d, x, y + h - 19, w, "4 DRONES DOWN")


def ill_lead2(d, x, y, w, h):
    # Falling market chart
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.text((x + 10, y + 3), "MSCI ASIA-PAC. ex-JAPAN", font=F_SANSB(8),
           fill=MUTED)
    gx, gy, gw, gh = x + 10, y + 14, w - 20, h - 40
    d.rectangle([gx, gy, gx + gw, gy + gh], outline=LIGHT_RULE, width=1)
    for i in range(1, 4):
        yy = gy + gh * i / 4
        d.line([gx, yy, gx + gw, yy], fill=(230, 225, 210), width=1)
    fracs = [(0.0, 0.12), (0.18, 0.22), (0.35, 0.35), (0.5, 0.42),
             (0.65, 0.58), (0.8, 0.68), (1.0, 0.88)]
    pts = [(gx + gw * f, gy + gh * v) for f, v in fracs]
    d.line(pts, fill=RED, width=3, joint="curve")
    for px, py in pts[1:-1:2]:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    banner(d, x, y + h - 19, w, "-2.3% MSCI ASIA")


def ill_lead3(d, x, y, w, h):
    # Night launch: rocket rising to the station
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    import random
    rng = random.Random(25)
    for _ in range(26):
        sx, sy = rng.uniform(0, w), rng.uniform(0, h * 0.6)
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                  fill=(255, 255, 255))
    # Tiangong station, top right
    sx, sy = x + w - 58, y + 12
    d.rectangle([sx, sy, sx + 34, sy + 6], fill=(200, 205, 215))
    d.rectangle([sx + 12, sy - 6, sx + 22, sy + 12], fill=(220, 224, 232))
    d.line([sx, sy + 3, sx - 12, sy + 3], fill=(160, 168, 180), width=3)
    d.line([sx + 34, sy + 3, sx + 46, sy + 3], fill=(160, 168, 180), width=3)
    # rocket, centre-left, rising
    rx, ry = x + w * 0.38, y + h * 0.30
    d.polygon([(rx, ry - 22), (rx + 7, ry - 8), (rx + 7, ry + 14),
               (rx - 7, ry + 14), (rx - 7, ry - 8)], fill=(240, 240, 240))
    d.polygon([(rx, ry - 22), (rx + 7, ry - 8), (rx - 7, ry - 8)], fill=RED)
    d.polygon([(rx - 7, ry + 14), (rx - 14, ry + 24), (rx - 7, ry + 18)],
              fill=RED)
    d.polygon([(rx + 7, ry + 14), (rx + 14, ry + 24), (rx + 7, ry + 18)],
              fill=RED)
    d.polygon([(rx - 4, ry + 14), (rx + 4, ry + 14), (rx, ry + 30)],
              fill=(255, 170, 40))
    d.text((x + 8, y + 4), "JIUQUAN  00:18 UTC", font=F_SANSB(8),
           fill=(255, 255, 255))
    banner(d, x, y + h - 19, w, "1ST PAKISTANI IN ORBIT")


def ill_middle(d, x, y, w, h, num):
    """One literal mini-scene per middle story (numbered 4-13)."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 230, 205))
    if num == 4:  # Gaza: apartment block + blast
        for i, bx in enumerate((0.08, 0.30, 0.52)):
            d.rectangle([x + bx * w, y + h * 0.30, x + (bx + 0.18) * w,
                         y + h * 0.92], fill=(120, 110, 95))
            for r in range(3):
                for c in range(2):
                    d.rectangle([x + (bx + 0.03 + c * 0.08) * w,
                                 y + h * (0.38 + r * 0.18),
                                 x + (bx + 0.07 + c * 0.08) * w,
                                 y + h * (0.50 + r * 0.18)],
                                fill=(255, 235, 160))
        cx, cy = x + 0.80 * w, y + 0.35 * h
        for ang in range(0, 360, 30):
            import math
            dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            d.line([cx + dx * 6, cy + dy * 6, cx + dx * 14, cy + dy * 14],
                   fill=(200, 90, 20), width=2)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(200, 90, 20))
    elif num == 5:  # refinery towers + flames
        for bx in (0.10, 0.30, 0.50):
            d.rectangle([x + bx * w, y + h * 0.35, x + (bx + 0.10) * w,
                         y + h * 0.92], fill=(140, 135, 125))
            d.rectangle([x + (bx + 0.03) * w, y + h * 0.22,
                         x + (bx + 0.07) * w, y + h * 0.35],
                        fill=(120, 115, 105))
        for bx in (0.15, 0.35, 0.55):
            d.polygon([(x + bx * w, y + h * 0.22), (x + (bx + 0.05) * w,
                       y + h * 0.02), (x + (bx + 0.10) * w, y + h * 0.22)],
                      fill=(230, 120, 30))
        d.ellipse([x + 0.72 * w, y + h * 0.30, x + 0.92 * w, y + h * 0.50],
                  fill=(230, 120, 30))
    elif num == 6:  # supermarket storefront
        d.rectangle([x + 0.06 * w, y + h * 0.28, x + 0.94 * w, y + h * 0.92],
                    fill=(70, 110, 160))
        d.rectangle([x + 0.06 * w, y + h * 0.28, x + 0.94 * w, y + h * 0.48],
                    fill=(240, 240, 240))
        d.text((x + 0.10 * w, y + h * 0.30), "SUPERMARKET",
               font=F_SANSB(11), fill=RED)
        for i in range(4):
            d.rectangle([x + (0.12 + i * 0.20) * w, y + h * 0.56,
                         x + (0.28 + i * 0.20) * w, y + h * 0.90],
                        fill=(255, 255, 255))
    elif num == 7:  # Shanghai skyline, Oriental Pearl tower
        d.rectangle([x, y + h * 0.75, x + w, y + h], fill=(90, 90, 100))
        for bx, bh in ((0.05, 0.45), (0.18, 0.60), (0.62, 0.55), (0.75, 0.40),
                       (0.86, 0.50)):
            d.rectangle([x + bx * w, y + h * (1 - bh), x + (bx + 0.10) * w,
                         y + h * 0.92], fill=(60, 60, 75))
        tx = x + 0.38 * w
        d.rectangle([tx, y + h * 0.15, tx + 6, y + h * 0.92], fill=(60, 60, 75))
        d.ellipse([tx - 6, y + h * 0.28, tx + 12, y + h * 0.48],
                  fill=(200, 60, 60))
        d.ellipse([tx - 3, y + h * 0.55, tx + 9, y + h * 0.68],
                  fill=(200, 60, 60))
    elif num == 8:  # storm cloud + balloons
        d.ellipse([x + 0.06 * w, y + h * 0.10, x + 0.38 * w, y + h * 0.45],
                  fill=(70, 80, 95))
        d.ellipse([x + 0.24 * w, y + h * 0.02, x + 0.56 * w, y + h * 0.40],
                  fill=(85, 95, 110))
        d.ellipse([x + 0.44 * w, y + h * 0.12, x + 0.72 * w, y + h * 0.45],
                  fill=(70, 80, 95))
        for i in range(5):
            d.line([x + (0.12 + i * 0.13) * w, y + h * 0.52,
                    x + (0.10 + i * 0.13) * w, y + h * 0.68],
                   fill=(31, 78, 121), width=2)
        for bx, col in ((0.74, (200, 60, 60)), (0.86, (230, 170, 40))):
            d.ellipse([x + bx * w, y + h * 0.55, x + (bx + 0.12) * w,
                       y + h * 0.80], fill=col)
            d.line([x + (bx + 0.06) * w, y + h * 0.80,
                    x + (bx + 0.06) * w, y + h * 0.92], fill=INK, width=1)
    elif num == 9:  # two flags + pact table
        for bx, col1, col2 in ((0.12, (0, 40, 90), (255, 255, 255)),
                               (0.62, (0, 90, 60), (255, 215, 0))):
            d.line([x + bx * w, y + h * 0.08, x + bx * w, y + h * 0.85],
                   fill=INK, width=2)
            d.polygon([(x + bx * w, y + h * 0.08),
                       (x + (bx + 0.22) * w, y + h * 0.16),
                       (x + bx * w, y + h * 0.24)], fill=col1)
        d.rectangle([x + 0.30 * w, y + h * 0.70, x + 0.70 * w, y + h * 0.78],
                    fill=(120, 85, 50))
        d.ellipse([x + 0.44 * w, y + h * 0.55, x + 0.56 * w, y + h * 0.70],
                  fill=(255, 255, 255), outline=INK, width=1)
    elif num == 10:  # courthouse columns + gavel
        d.rectangle([x + 0.10 * w, y + h * 0.18, x + 0.90 * w, y + h * 0.30],
                    fill=(120, 110, 95))
        for bx in (0.14, 0.32, 0.50, 0.68):
            d.rectangle([x + bx * w, y + h * 0.30, x + (bx + 0.08) * w,
                         y + h * 0.85], fill=(150, 140, 120))
        d.rectangle([x + 0.08 * w, y + h * 0.85, x + 0.92 * w, y + h * 0.92],
                    fill=(120, 110, 95))
        d.line([x + 0.84 * w, y + h * 0.42, x + 0.96 * w, y + h * 0.60],
               fill=(90, 60, 30), width=3)
    elif num == 11:  # quantum chip + circuit
        d.rectangle([x + 0.30 * w, y + h * 0.20, x + 0.70 * w, y + h * 0.80],
                    fill=(31, 58, 92))
        d.rectangle([x + 0.42 * w, y + h * 0.38, x + 0.58 * w, y + h * 0.62],
                    fill=(255, 255, 255))
        d.text((x + 0.46 * w, y + h * 0.40), "\u20ac", font=F_SANSB(13),
               fill=RED)
        for i in range(3):
            yy = y + h * (0.30 + i * 0.20)
            d.line([x + 0.30 * w, yy, x + 0.08 * w, yy], fill=(31, 58, 92),
                   width=2)
            d.line([x + 0.70 * w, yy, x + 0.92 * w, yy], fill=(31, 58, 92),
                   width=2)
    elif num == 12:  # strike placards + crowd
        for bx, txt in ((0.08, "PAY"), (0.40, "FAIR"), (0.70, "NOW")):
            d.line([x + (bx + 0.10) * w, y + h * 0.30, x + (bx + 0.10) * w,
                    y + h * 0.75], fill=INK, width=2)
            d.rectangle([x + bx * w, y + h * 0.08, x + (bx + 0.22) * w,
                         y + h * 0.32], fill=(255, 255, 255), outline=RED,
                        width=2)
            d.text((x + (bx + 0.03) * w, y + h * 0.14), txt, font=F_SANSB(9),
                   fill=RED)
        for bx in (0.10, 0.30, 0.50, 0.70, 0.88):
            d.ellipse([x + bx * w, y + h * 0.72, x + (bx + 0.08) * w,
                       y + h * 0.88], fill=(90, 80, 65))
    else:  # 13: mine shaft cross-section
        d.rectangle([x, y, x + w, y + h], fill=(150, 120, 85))
        d.rectangle([x + 0.30 * w, y, x + 0.70 * w, y + h], fill=(60, 45, 30))
        d.line([x + 0.30 * w, y, x + 0.30 * w, y + h], fill=INK, width=2)
        d.line([x + 0.70 * w, y, x + 0.70 * w, y + h], fill=INK, width=2)
        for i in range(4):
            yy = y + h * (0.15 + i * 0.20)
            d.line([x + 0.30 * w, yy, x + 0.70 * w, yy], fill=(120, 95, 65),
                   width=3)
        d.ellipse([x + 0.42 * w, y + h * 0.55, x + 0.58 * w, y + h * 0.72],
                  fill=(255, 215, 0))
        d.rectangle([x + 0.48 * w, y + h * 0.50, x + 0.52 * w, y + h * 0.56],
                    fill=(255, 215, 0))


# ------------------------------------------------------------------ page
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 6

    # ---- masthead
    f_mast = F_BLACK(30)
    d.line([MARGIN, y + 2, W - MARGIN, y + 2], fill=RULE, width=2)
    d.text((MARGIN, y + 6), "EST. 2026", font=F_SANSB(9), fill=MUTED)
    mw = d.textlength(C.MASTHEAD, font=f_mast)
    d.text(((W - mw) / 2, y + 4), C.MASTHEAD, font=f_mast, fill=INK)
    rw = d.textlength("No. 25", font=F_SANSB(9))
    d.text((W - MARGIN - rw, y + 6), "No. 25", font=F_SANSB(9), fill=MUTED)
    y += 38
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=3)
    y += 4

    # ---- date, largest type on the page
    f_date = F_BLACK(50)
    dw = d.textlength(C.DATE_LINE, font=f_date)
    d.text(((W - dw) / 2, y), C.DATE_LINE, font=f_date, fill=INK)
    y += 58
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=2)
    y += 5

    # ---- red italic subhead, one line
    f_sub = F_ITAL(17)
    sub = "  \u00b7  ".join([
        "Houthis say they hit a Saudi refinery",
        "Asia tumbles on a tariff threat",
        "First Pakistani in orbit",
    ])
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, y), sub, font=f_sub, fill=RED)
    y += 24

    # ---- region counts line
    f_reg = F_SANSB(11)
    rw = d.textlength(C.REGION_LINE, font=f_reg)
    d.text(((W - rw) / 2, y), C.REGION_LINE, font=f_reg, fill=INK)
    y += 17
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=2)
    y += 5

    # ---- THE DAY IN NUMBERS
    d.text((MARGIN, y), "THE DAY IN NUMBERS", font=F_SANSB(11), fill=RED)
    y += 14
    cell_w = CW / 7
    f_fig = F_DBOLD(21)
    f_cap = F_SANS(9)
    for i, (fig, cap) in enumerate(C.NUMBERS):
        cx = MARGIN + i * cell_w
        if i:
            d.line([cx - 4, y, cx - 4, y + 42], fill=LIGHT_RULE, width=1)
        fw = d.textlength(fig, font=f_fig)
        d.text((cx + (cell_w - 8 - fw) / 2, y), fig, font=f_fig, fill=INK)
        cap_lines = wrap(d, cap, f_cap, cell_w - 10)
        text_lines(d, cx, y + 26, cap_lines[:2], f_cap, MUTED, leading=11)
    y += 48
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=2)
    y += 5

    # ---- leads: 3 columns
    lead_w = (CW - 2 * 10) / 3
    lead_h = 150
    for i, (num, region, cert, head, body, _chip) in enumerate(C.LEADS):
        lx = MARGIN + i * (lead_w + 10)
        d.rectangle([lx, y, lx + lead_w, y + lead_h], outline=RULE, width=1)
        d.rectangle([lx, y, lx + lead_w, y + 16], fill=INK)
        d.text((lx + 6, y + 2), f"{num}  \u00b7  {region}", font=F_SANSB(9),
               fill=(255, 255, 255))
        _tw = d.textlength(cert, font=F_SANSB(8)) + 10
        tag(d, lx + lead_w - 6 - _tw, y + 2, cert)
        # illustration
        ix, iy, iw, ih = lx + 1, y + 17, lead_w - 2, 54
        (ill_lead1, ill_lead2, ill_lead3)[i](d, ix, iy, iw, ih)
        hy = y + 17 + 54 + 4
        f_head = F_DBOLD(17)
        hl = wrap(d, head, f_head, lead_w - 12)
        hy = text_lines(d, lx + 6, hy, hl[:2], f_head, INK, leading=19)
        f_body = F_SERIF(11)
        bl = wrap(d, " ".join(body), f_body, lead_w - 12)
        hy = text_lines(d, lx + 6, hy + 1, bl[:3], f_body, (60, 60, 60),
                        leading=12)
    y += lead_h + 6

    # ---- middle: 5 cols x 2 rows
    mid_w = (CW - 4 * 8) / 5
    mid_h = 110
    for i, (num, region, cert, head, body, _chip) in enumerate(C.MIDDLE):
        row, col = divmod(i, 5)
        mx = MARGIN + col * (mid_w + 8)
        my = y + row * (mid_h + 6)
        d.rectangle([mx, my, mx + mid_w, my + mid_h], outline=RULE, width=1)
        ill_middle(d, mx + 1, my + 1, mid_w - 2, 44, num)
        _tw = d.textlength(cert, font=F_SANSB(8)) + 10
        tag(d, mx + mid_w - 5 - _tw, my + 3, cert)
        f_h = F_SBOLD(12)
        hl = wrap(d, head, f_h, mid_w - 10)
        ty = text_lines(d, mx + 5, my + 49, hl[:2], f_h, INK, leading=13)
        f_b = F_SERIF(10)
        bl = wrap(d, " ".join(body), f_b, mid_w - 10)
        text_lines(d, mx + 5, ty + 1, bl[:2], f_b, (60, 60, 60), leading=11)
        d.text((mx + mid_w - 18, my + mid_h - 13), str(num),
               font=F_SANSB(10), fill=MUTED)
    y += 2 * mid_h + 6 + 5

    # ---- ALSO list: 5 cols x 4 rows
    d.text((MARGIN, y), "ALSO ON 25 NOVEMBER", font=F_SANSB(11), fill=RED)
    y += 16
    also_w = (CW - 4 * 10) / 5
    f_ah = F_SANSB(10)
    f_at = F_SANS(9)
    for i, (num, head, txt) in enumerate(C.ALSO):
        row, col = divmod(i, 5)
        ax = MARGIN + col * (also_w + 10)
        ay = y + row * 24
        d.text((ax, ay), f"{num}.", font=F_SANSB(10), fill=RED)
        hl = wrap(d, head, f_ah, also_w - 22)
        text_lines(d, ax + 20, ay, hl[:1], f_ah, INK, leading=11)
        tl = wrap(d, txt, f_at, also_w - 20)
        text_lines(d, ax + 20, ay + 11, tl[:1], f_at, MUTED, leading=10)
    y += 4 * 24 + 3
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=2)
    y += 4

    # ---- map
    d.text((MARGIN, y), "WHERE IT HAPPENED  \u2014  pins match story numbers",
           font=F_SANSB(11), fill=RED)
    y += 14
    map_h = 96
    draw_map(d, MARGIN, y, CW, map_h)
    y += map_h + 4
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=2)
    y += 4

    # ---- UTC timeline
    d.text((MARGIN, y), "THE DAY IN TIME  (UTC)", font=F_SANSB(11), fill=RED)
    y += 14
    tl_w = CW / 8
    f_tt = F_SANSB(10)
    f_tl = F_SANS(9)
    for i, (t, label) in enumerate(C.TIMELINE):
        tx = MARGIN + i * tl_w
        if i:
            d.line([tx - 4, y, tx - 4, y + 32], fill=LIGHT_RULE, width=1)
        d.text((tx, y), t, font=f_tt, fill=RED if "DUE" in label else INK)
        ll = wrap(d, label, f_tl, tl_w - 10)
        text_lines(d, tx, y + 12, ll[:3], f_tl, MUTED, leading=10)
    y += 38
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=2)
    y += 4

    # ---- DATE CHECK
    d.text((MARGIN, y), "DATE CHECK  \u2014  not 25 November news, excluded by name",
           font=F_SANSB(11), fill=RED)
    y += 14
    f_dc = F_SANS(10)
    col_w = CW / 2
    for i, (day, txt) in enumerate(C.DATE_CHECK):
        cx = MARGIN + (i // 5) * col_w
        cy = y + (i % 5) * 12
        d.text((cx, cy), day, font=F_SANSB(9), fill=RED)
        d.text((cx + 62, cy), txt, font=f_dc, fill=MUTED)
    y += 5 * 12 + 2
    f_ny = F_SANSB(10)
    d.text((MARGIN, y), C.NOT_YET, font=f_ny, fill=INK)
    y += 14
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=2)
    y += 4

    # ---- footer: legend + note
    f_leg = F_SANS(9)
    lw = d.textlength(C.LEGEND, font=f_leg)
    d.text(((W - lw) / 2, y), C.LEGEND, font=f_leg, fill=MUTED)
    y += 12
    fw = d.textlength(C.FOOTER_NOTE, font=f_leg)
    d.text(((W - fw) / 2, y), C.FOOTER_NOTE, font=f_leg, fill=MUTED)
    y += 11

    assert y <= H, f"layout overflow: y={y}"
    return img, y


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "page.png")
    img, used = render()
    img.save(out, optimize=True)
    print(f"wrote {out}  {os.path.getsize(out)} bytes  used height {used}/1024")
    # quantise if over the 1 MiB cap (flat art: no visible loss)
    if os.path.getsize(out) > 1048576:
        q = img.convert("P", palette=Image.ADAPTIVE, colors=256)
        q.save(out, optimize=True)
        print(f"quantised to {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
