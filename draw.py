"""Drawing helpers, flat scenes and the dotted world map for the newspaper page."""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

PAPER = (247, 243, 232)
NAVY = (27, 42, 74)
NAVY_DARK = (18, 29, 54)
RED = (179, 35, 42)
INK = (34, 34, 38)
MUTED = (96, 88, 70)
RULE = (178, 168, 140)
CREAM_CARD = (252, 250, 243)

_cache = {}


def F(name, size):
    key = (name, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    return _cache[key]


def serif_b(size):
    return F("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return F("DejaVuSerif.ttf", size)


def sans(size):
    return F("DejaVuSans.ttf", size)


def sans_b(size):
    return F("DejaVuSans-Bold.ttf", size)


def mono(size):
    return F("DejaVuSansMono.ttf", size)


def italic(size):
    return F("LiberationSerif-Italic.ttf", size)


def tw(d, text, font):
    return d.textlength(text, font=font)


def wrap(d, text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(d, t, font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, text, font, fill, maxw, pitch, max_lines=None, align="left", width=None):
    """Draw wrapped text; return the y just past the last line."""
    lines = wrap(d, text, font, maxw)
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        if align == "center":
            w = tw(d, ln, font)
            d.text((x + ((width or maxw) - w) / 2, y), ln, font=font, fill=fill)
        else:
            d.text((x, y), ln, font=font, fill=fill)
        y += pitch
    return y


CHIP_COLORS = {"REPORTED": NAVY, "CLAIM": RED, "FORECAST": (46, 107, 48)}


def chip(d, x, y, label):
    f = sans_b(9)
    w = tw(d, label, f) + 10
    d.rectangle([x, y, x + w, y + 14], fill=CHIP_COLORS.get(label, NAVY))
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w


def num_badge(d, x, y, num, r=10):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=RED)
    f = sans_b(11 if num < 10 else 9)
    s = str(num)
    w = tw(d, s, f)
    d.text((x + r - w / 2, y + r - 6), s, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- scenes

def scene_drones(img, d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(18, 28, 54))
    rng = random.Random(186)
    for _ in range(46):
        sx = rng.uniform(x0 + 4, x1 - 4)
        sy = rng.uniform(y0 + 3, y0 + (y1 - y0) * 0.55)
        d.point((sx, sy), fill=(220, 224, 235))
    # moon
    d.ellipse([x1 - 34, y0 + 8, x1 - 16, y0 + 26], fill=(232, 230, 210))
    # searchlight beam from lower right, composited over the sky
    bw, bh = x1 - x0, y1 - y0
    beam = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    bd = ImageDraw.Draw(beam)
    bd.polygon([(bw - 26, bh), (60, 14), (92, 10)], fill=(255, 240, 180, 70))
    base = img.crop(box).convert("RGBA")
    img.paste(Image.alpha_composite(base, beam).convert("RGB"), (x0, y0))
    # second, fainter searchlight from lower left
    beam2 = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    bd2 = ImageDraw.Draw(beam2)
    bd2.polygon([(18, bh), (150, 8), (176, 12)], fill=(200, 220, 255, 45))
    base = img.crop(box).convert("RGBA")
    img.paste(Image.alpha_composite(base, beam2).convert("RGB"), (x0, y0))
    # city skyline silhouette across the bottom, with lit windows
    rng3 = random.Random(42)
    sx = x0 + 2
    while sx < x1 - 14:
        swd = rng3.randint(13, 24)
        sht = rng3.randint(10, 24)
        d.rectangle([sx, y1 - sht, sx + swd, y1], fill=(13, 18, 30))
        for _ in range(rng3.randint(1, 3)):
            wx = sx + rng3.randint(2, max(2, swd - 5))
            wy = y1 - sht + rng3.randint(2, max(2, sht - 5))
            d.rectangle([wx, wy, wx + 2, wy + 2], fill=(238, 196, 105))
        sx += swd + rng3.randint(2, 5)
    # drones: small delta silhouettes with red navigation dots
    for (dx, dy, s) in [(x0 + 40, y0 + 20, 9), (x0 + 96, y0 + 12, 7), (x0 + 150, y0 + 26, 8),
                        (x0 + 205, y0 + 16, 6), (x0 + 66, y0 + 40, 6), (x0 + 178, y0 + 38, 5),
                        (x0 + 236, y0 + 30, 7), (x0 + 24, y0 + 34, 5)]:
        d.polygon([(dx, dy), (dx + s * 2, dy + s * 0.5), (dx, dy + s)], fill=(8, 10, 16))
        d.polygon([(dx + s * 0.4, dy + s * 0.5), (dx + s * 2.6, dy + s * 0.2),
                   (dx + s * 2.6, dy + s * 0.8)], fill=(8, 10, 16))
        d.point((dx + s * 1.2, dy + s * 0.5), fill=(255, 70, 60))
    # air-defence tracer streaks rising from the skyline
    for (tx0, tx1, ty1) in [(x0 + 150, x0 + 118, y0 + 18), (x0 + 210, x0 + 188, y0 + 12),
                            (x0 + 262, x0 + 244, y0 + 22)]:
        d.line([tx0, y1 - 8, tx1, ty1], fill=(255, 170, 80), width=1)
        d.point((tx1, ty1), fill=(255, 220, 150))
    # apartment block, lower left
    bx, by, bw, bh = x0 + 14, y1 - 40, 58, 40
    d.rectangle([bx, by, bx + bw, by + bh], fill=(10, 14, 24))
    rng2 = random.Random(7)
    for r in range(4):
        for c in range(5):
            if rng2.random() < 0.55:
                wx, wy = bx + 6 + c * 11, by + 5 + r * 9
                d.rectangle([wx, wy, wx + 6, wy + 5], fill=(250, 205, 110))
    # damaged second block
    bx2 = x0 + 84
    d.rectangle([bx2, y1 - 30, bx2 + 40, y1], fill=(10, 14, 24))
    d.polygon([(bx2, y1 - 30), (bx2 + 18, y1 - 38), (bx2 + 40, y1 - 30)], fill=(10, 14, 24))
    d.polygon([(bx2 + 12, y1 - 26), (bx2 + 20, y1 - 12), (bx2 + 26, y1 - 26),
               (bx2 + 22, y1 - 4), (bx2 + 15, y1 - 12)], fill=(240, 130, 50))
    d.rectangle([x0, y1 - 2, x1, y1], fill=(6, 8, 14))


def scene_cop(img, d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(214, 226, 214))
    d.rectangle([x0, y0, x1, y0 + 16], fill=(168, 190, 175))
    # row of delegates' flags along the top band
    flag_cols = [(60, 90, 170), (200, 60, 60), (70, 140, 80), (230, 190, 60),
                 (150, 70, 140), (50, 130, 170), (210, 110, 40), (90, 90, 90)]
    for i, fc in enumerate(flag_cols):
        fx = x0 + 58 + i * 26
        d.line([fx, y0 + 2, fx, y0 + 13], fill=(90, 90, 90), width=1)
        d.rectangle([fx + 1, y0 + 2, fx + 11, y0 + 8], fill=fc)
    # wall chart: the rising temperature line, next to the clock
    chx, chy = x1 - 108, y0 + 20
    d.rectangle([chx, chy - 12, chx + 52, chy + 14], fill=(250, 250, 246), outline=RULE, width=1)
    d.line([chx + 4, chy + 10, chx + 18, chy + 4, chx + 30, chy + 6, chx + 46, chy - 8],
           fill=RED, width=2)
    d.line([chx + 4, chy - 2, chx + 48, chy - 2], fill=RED, width=1)
    # wall clock
    cx, cy, r = x1 - 30, y0 + 26, 12
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=2, fill=(250, 250, 246))
    d.line([cx, cy, cx, cy - 8], fill=NAVY, width=2)
    d.line([cx, cy, cx + 6, cy + 3], fill=NAVY, width=2)
    # tree at left
    tx, ty = x0 + 26, y0 + 34
    d.rectangle([tx - 2, ty + 12, tx + 2, ty + 30], fill=(110, 78, 45))
    for (ox, oy, rr) in [(-9, 4, 10), (8, 2, 11), (0, -6, 12)]:
        d.ellipse([tx + ox - rr, ty + oy - rr, tx + ox + rr, ty + oy + rr], fill=(74, 124, 74))
    # long table + delegates
    ty2 = y1 - 26
    d.rectangle([x0 + 52, ty2, x1 - 14, ty2 + 10], fill=(122, 84, 50))
    n = 6
    for i in range(n):
        gx = x0 + 66 + i * ((x1 - x0 - 92) / (n - 1))
        d.ellipse([gx - 6, ty2 - 24, gx + 6, ty2 - 12], fill=(226, 188, 150))
        d.polygon([(gx - 9, ty2), (gx + 9, ty2), (gx + 5, ty2 - 13), (gx - 5, ty2 - 13)],
                  fill=NAVY if i % 2 else (122, 60, 60))
        d.rectangle([gx - 5, ty2 - 4, gx + 5, ty2], fill=(250, 250, 246))
    # the rejected text at the centre of the table, crossed out in red
    dcx = (x0 + x1) / 2
    d.rectangle([dcx - 13, ty2 - 9, dcx + 13, ty2 + 3], fill=(252, 252, 248),
                outline=(120, 120, 120), width=1)
    d.line([dcx - 13, ty2 - 9, dcx + 13, ty2 + 3], fill=RED, width=2)
    d.line([dcx - 13, ty2 + 3, dcx + 13, ty2 - 9], fill=RED, width=2)


def scene_bahrain(img, d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(196, 216, 228))
    d.rectangle([x0, y1 - 22, x1, y1], fill=(58, 96, 128))
    # two radar ships
    for (sx, sw) in [(x0 + 26, 92), (x0 + 168, 104)]:
        sy = y1 - 22
        d.polygon([(sx, sy), (sx + sw, sy), (sx + sw - 12, sy - 12), (sx + 10, sy - 12)],
                  fill=(70, 78, 90))
        d.rectangle([sx + sw * 0.38, sy - 30, sx + sw * 0.46, sy - 12], fill=(70, 78, 90))
        # dish
        dcx, dcy = sx + sw * 0.42, sy - 34
        d.arc([dcx - 13, dcy - 10, dcx + 13, dcy + 12], start=300, end=130, fill=NAVY, width=3)
        d.line([dcx, dcy + 4, dcx + 10, dcy - 8], fill=NAVY, width=2)
        # flames on the second ship
        if sx > x0 + 100:
            fx, fy = sx + sw * 0.66, sy - 12
            d.polygon([(fx, fy), (fx + 7, fy - 20), (fx + 12, fy - 6), (fx + 17, fy - 16),
                       (fx + 20, fy)], fill=(238, 120, 40))
            d.polygon([(fx + 5, fy), (fx + 10, fy - 11), (fx + 15, fy)], fill=(250, 200, 80))
            # smoke plume rising and drifting right
            for (ox, oy, rr) in [(6, -22, 5), (13, -29, 7), (22, -35, 9), (33, -40, 11)]:
                d.ellipse([fx + ox - rr, fy + oy - rr * 0.6, fx + ox + rr, fy + oy + rr * 0.6],
                          fill=(105, 108, 115))
    # radar sweep wedge from the first ship's dish
    swx, swy = x0 + 26 + 92 * 0.42, y1 - 22 - 34
    sweep = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sweep)
    sd.polygon([(swx - x0, swy - y0), (swx - x0 + 44, swy - y0 - 16), (swx - x0 + 40, swy - y0 + 2)],
               fill=(70, 140, 90, 60))
    base = img.crop(box).convert("RGBA")
    img.paste(Image.alpha_composite(base, sweep).convert("RGB"), (x0, y0))
    # dotted missile arcs falling toward the second ship
    for t in range(9):
        for (ax, ay, bx2, by2, cx2, cy2) in [(x0 + 96, y0 + 4, x0 + 190, y0 - 14, x0 + 246, y1 - 40),
                                             (x0 + 130, y0 + 2, x0 + 214, y0 - 8, x0 + 258, y1 - 38)]:
            u = t / 8.0
            px = (1 - u) ** 2 * ax + 2 * (1 - u) * u * bx2 + u ** 2 * cx2
            py = (1 - u) ** 2 * ay + 2 * (1 - u) * u * by2 + u ** 2 * cy2
            d.point((px, py), fill=(150, 40, 40))
    # wave strokes on the water + a small third boat at the right edge
    for (wx, wy) in [(x0 + 14, y1 - 14), (x0 + 120, y1 - 8), (x0 + 216, y1 - 15),
                     (x0 + 262, y1 - 7), (x0 + 66, y1 - 5)]:
        d.arc([wx, wy, wx + 16, wy + 6], start=200, end=340, fill=(225, 238, 245), width=1)
    bx3, by3 = x0 + 268, y1 - 22
    d.polygon([(bx3, by3), (bx3 + 30, by3), (bx3 + 24, by3 - 7), (bx3 + 5, by3 - 7)],
              fill=(70, 78, 90))
    d.rectangle([bx3 + 12, by3 - 13, bx3 + 17, by3 - 7], fill=(70, 78, 90))
    # denial arrow arcing back
    ax0, ay0, ax1, ay1 = x0 + 120, y0 + 6, x0 + 210, y0 + 40
    d.arc([ax0, ay0, ax1, ay1], start=200, end=330, fill=RED, width=3)
    ex = ax0 + (ax1 - ax0) * 0.86
    ey = ay0 + 6
    d.polygon([(ex, ey), (ex - 11, ey + 1), (ex - 4, ey + 9)], fill=RED)


SCENES = {"drones": scene_drones, "cop": scene_cop, "bahrain": scene_bahrain}

# ---------------------------------------------------------------- card strips

STRIP_COLORS = {
    "vote": (70, 96, 140), "cricket": (64, 110, 74), "f1": (40, 40, 48),
    "nba": (178, 96, 44), "ship": (58, 96, 128), "power": (146, 116, 32),
    "health": (150, 62, 66), "cyber": (52, 62, 92), "strike": (96, 110, 128),
    "poison": (96, 84, 130), "fire": (168, 70, 34), "quake": (110, 88, 64),
}


def card_strip(d, box, kind):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=STRIP_COLORS.get(kind, NAVY))
    cx, cy = x0 + 42, (y0 + y1) / 2
    W = (255, 255, 255)
    if kind == "vote":
        d.rectangle([cx - 12, cy - 3, cx + 12, cy + 8], outline=W, width=2)
        d.rectangle([cx - 6, cy - 7, cx + 6, cy - 3], fill=W)
    elif kind == "cricket":
        d.ellipse([cx + 4, cy - 7, cx + 14, cy + 3], fill=(240, 240, 230))
        d.polygon([(cx - 12, cy + 8), (cx - 8, cy + 8), (cx + 2, cy - 8), (cx - 2, cy - 8)], fill=W)
    elif kind == "f1":
        for i in range(6):
            for j in range(2):
                if (i + j) % 2 == 0:
                    d.rectangle([cx - 15 + i * 5, cy - 5 + j * 5, cx - 10 + i * 5, cy + j * 5], fill=W)
    elif kind == "nba":
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], outline=W, width=2)
        d.line([cx - 9, cy, cx + 9, cy], fill=W, width=1)
        d.line([cx, cy - 9, cx, cy + 9], fill=W, width=1)
    elif kind == "ship":
        d.polygon([(cx - 14, cy + 4), (cx + 14, cy + 4), (cx + 9, cy + 9), (cx - 9, cy + 9)], fill=W)
        d.rectangle([cx - 3, cy - 8, cx + 1, cy + 4], fill=W)
    elif kind == "power":
        d.polygon([(cx + 2, cy - 10), (cx - 7, cy + 2), (cx - 1, cy + 2), (cx - 3, cy + 10),
                   (cx + 7, cy - 3), (cx + 1, cy - 3)], fill=(255, 214, 90))
    elif kind == "health":
        d.rectangle([cx - 3, cy - 9, cx + 3, cy + 9], fill=W)
        d.rectangle([cx - 9, cy - 3, cx + 9, cy + 3], fill=W)
    elif kind == "cyber":
        d.rectangle([cx - 10, cy - 6, cx + 10, cy + 6], outline=W, width=2)
        d.rectangle([cx - 2, cy - 2, cx + 2, cy + 2], fill=W)
    elif kind == "strike":
        d.polygon([(cx - 14, cy + 2), (cx + 14, cy - 4), (cx + 14, cy + 1), (cx - 14, cy + 7)], fill=W)
        d.line([cx - 12, cy + 9, cx + 12, cy + 9], fill=RED, width=2)
    elif kind == "poison":
        d.rectangle([cx - 5, cy - 4, cx + 5, cy + 9], outline=W, width=2)
        d.rectangle([cx - 3, cy - 8, cx + 3, cy - 4], fill=W)
    elif kind == "fire":
        d.polygon([(cx, cy - 10), (cx + 8, cy + 3), (cx + 5, cy + 9), (cx - 5, cy + 9),
                   (cx - 8, cy + 3)], fill=(255, 170, 60))
        d.polygon([(cx, cy - 2), (cx + 4, cy + 5), (cx, cy + 9), (cx - 4, cy + 5)], fill=(255, 220, 120))
    elif kind == "quake":
        pts = [(cx - 14, cy + 6), (cx - 7, cy - 2), (cx - 2, cy + 5), (cx + 4, cy - 6),
               (cx + 9, cy + 3), (cx + 14, cy - 3)]
        d.line(pts, fill=W, width=2)


# ---------------------------------------------------------------- world map

def _land(col, row):
    """Coarse world: union of ellipses / rects on a 58x24 grid."""
    def ell(cx, cy, rx, ry):
        return ((col - cx) / rx) ** 2 + ((row - cy) / ry) ** 2 <= 1.0
    if ell(10, 4.5, 7.5, 3.4):      # North America
        return True
    if ell(3, 2.5, 3.0, 1.6):       # Alaska
        return True
    if ell(20, 2.0, 2.6, 1.5):      # Greenland
        return True
    if 8 <= col <= 11 and 8 <= row <= 9 and col - 8 <= row - 7:  # Central America
        return True
    if ell(14.5, 14, 3.2, 4.6):     # South America
        return True
    if ell(30, 3.8, 3.6, 2.1):      # Europe
        return True
    if col == 27 and row == 3:      # Britain
        return True
    if ell(32.5, 11, 4.6, 5.0):     # Africa
        return True
    if ell(43, 4.2, 10.5, 3.4):     # Asia (Russia to China)
        return True
    if ell(39.5, 8.6, 2.1, 2.6):    # India
        return True
    if ell(44.5, 9.8, 2.0, 2.0):    # SE Asia
        return True
    if row == 12 and 43 <= col <= 49 and (col % 2 == 0):  # Indonesia
        return True
    if (col, row) in {(50, 5), (51, 4), (51, 5)}:  # Japan
        return True
    if ell(47, 16, 3.6, 2.1):       # Australia
        return True
    if (col, row) in {(54, 20), (55, 21)}:  # New Zealand
        return True
    return False


def world_map(d, box, pins):
    x0, y0, x1, y1 = box
    cols, rows = 58, 24
    cw = (x1 - x0) / cols
    ch = (y1 - y0) / rows
    r = max(1.1, min(cw, ch) * 0.30)
    for row in range(rows):
        for col in range(cols):
            if _land(col, row):
                cx = x0 + (col + 0.5) * cw
                cy = y0 + (row + 0.5) * ch
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(120, 132, 158))
    for (num, lon, lat) in pins:
        fx = (lon + 180) / 360.0
        fy = (78 - lat) / 138.0
        px = x0 + fx * (x1 - x0)
        py = y0 + fy * (y1 - y0)
        pr = 7.5
        d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=RED, outline=(255, 255, 255), width=1)
        f = sans_b(8 if num < 10 else 7)
        s = str(num)
        w = tw(d, s, f)
        d.text((px - w / 2, py - 4), s, font=f, fill=(255, 255, 255))
