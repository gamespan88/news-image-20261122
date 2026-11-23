#!/usr/bin/env python3
"""THE WORLD IN ONE DAY — one-page illustrated newspaper for Sunday 22 Nov 2026.

Deterministic: draws the whole page with PIL from fixed data (stories.py) and
fixed-seed scene details, then writes /output/entry.png. No network, no clock.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image, ImageDraw

import stories
from draw import (ACCENTS, CHIP_COLORS, GREEN, INK, MUTED, NAVY, NAVY_DARK,
                  PAPER, RED, RULE, SCENES, TEAL, block, card_strip, chip,
                  italic, mono, num_badge, sans, sans_b, serif_b, tw,
                  world_map, wrap)

HERO_ACCENTS = [RED, GREEN, TEAL]

W = H = 1024
M = 16
CW = W - 2 * M  # content width = 992


def fit_font(d, text, maxw, start):
    size = start
    while size > 40 and tw(d, text, serif_b(size)) > maxw:
        size -= 2
    return serif_b(size)


def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # 1 — navy strip ------------------------------------------------------
    d.rectangle([0, 0, W, 27], fill=NAVY)
    d.text((M, 7), "THE WORLD IN ONE DAY", font=sans_b(13), fill=(255, 255, 255))
    right = "31 STORIES · 7 REGIONS · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
    d.text((W - M - tw(d, right, sans(10)), 8), right, font=sans(10), fill=(210, 216, 230))

    # 2 — masthead ---------------------------------------------------------
    date = "Sunday 22 November 2026"
    f_date = fit_font(d, date, CW, 80)
    dw = tw(d, date, f_date)
    d.text(((W - dw) / 2, 32), date, font=f_date, fill=RED)
    y = 32 + f_date.size + 12

    stand = ("186 drones over Ukraine in the night · COP31 collapses over fossil fuels · "
             "Iran's radar claim meets Bahrain's denial")
    f_st = italic(15)
    d.text(((W - tw(d, stand, f_st)) / 2, y), stand, font=f_st, fill=RED)
    y += 23
    d.rectangle([M, y, W - M, y + 3], fill=NAVY)
    d.line([M, y + 5, W - M, y + 5], fill=NAVY, width=1)
    y += 10

    # 3 — numbers strip -----------------------------------------------------
    cell = CW / 6
    f_num, f_cap = serif_b(34), sans(10)
    for i, (num, cap) in enumerate(stories.NUMBERS):
        x = M + i * cell
        d.text((x + 2, y), num, font=f_num, fill=RED)
        block(d, x + 2, y + 40, cap, f_cap, INK, cell - 10, 11, max_lines=2)
        if i:
            d.line([x - 5, y + 2, x - 5, y + 56], fill=RULE, width=1)
    y += 63

    # 4 — region band -------------------------------------------------------
    total = sum(n for _, n, _ in stories.REGIONS)
    x = M
    for name, n, color in stories.REGIONS:
        wseg = CW * n / total
        d.rectangle([x, y, x + wseg - 2, y + 19], fill=color)
        label = "%s %d" % (name, n)
        f = sans_b(10)
        d.text((x + (wseg - 2 - tw(d, label, f)) / 2, y + 4), label, font=f,
               fill=(255, 255, 255))
        x += wseg
    y += 24

    # 5 — timeline ----------------------------------------------------------
    tl = stories.TIMELINE
    d.rectangle([M, y - 2, W - M, y + 13], fill=(240, 230, 204))
    d.rectangle([M, y - 2, M + 96, y + 13], fill=RED)
    d.text((M + 7, y + 1), "THE DAY IN UTC", font=sans_b(8), fill=(255, 255, 255))
    tsize = 10
    while tsize > 7 and tw(d, tl, mono(tsize)) > CW - 108:
        tsize -= 1
    f_tl = mono(tsize)
    d.text((M + 104, y), tl, font=f_tl, fill=(70, 64, 50))
    y += 19

    # 6 — heroes -------------------------------------------------------------
    hero_y = y
    pw = (CW - 22) // 3
    panel_h = 0
    for i, h in enumerate(stories.HEROES):
        x = M + i * (pw + 11)
        SCENES[h["scene"]](img, d, (x, hero_y, x + pw, hero_y + 66))
        accent = HERO_ACCENTS[i]
        by = hero_y + 52
        d.rectangle([x, by, x + pw, by + 14], fill=accent)
        d.text((x + 6, by + 2), h["banner"], font=sans_b(9), fill=(255, 255, 255))
        b2 = h["banner2"]
        d.text((x + pw - 6 - tw(d, b2, sans_b(9)), by + 2), b2, font=sans_b(9),
               fill=(255, 255, 255))
        by = hero_y + 70
        num_badge(d, x, by, h["num"], r=8, color=accent)
        d.text((x + 22, by + 2), h["dateline"], font=sans_b(10), fill=accent)
        cw_chip = tw(d, h["chip"], sans_b(9)) + 10
        chip(d, x + pw - cw_chip, by + 1, h["chip"])
        by += 19
        by = block(d, x, by, h["headline"], serif_b(30), NAVY_DARK, pw, 33, max_lines=3)
        by += 2
        by = block(d, x, by, h["summary"], sans(14), INK, pw, 16, max_lines=6)
        panel_h = max(panel_h, by - hero_y)
    y = hero_y + panel_h + 5
    d.line([M, y, W - M, y], fill=RULE, width=1)
    y += 6

    # 7 — cards ---------------------------------------------------------------
    card_w = (CW - 45) // 6
    card_h = 116
    for row in range(2):
        for col in range(6):
            c = stories.CARDS[row * 6 + col]
            x = M + col * (card_w + 9)
            d.rectangle([x, y, x + card_w, y + card_h], fill=(252, 250, 243),
                        outline=RULE, width=1)
            card_strip(d, (x + 1, y + 1, x + card_w - 1, y + 20), c["kind"])
            num_badge(d, x + 4, y + 2, c["num"], r=8,
                      color=ACCENTS[(c["num"] - 4) % len(ACCENTS)])
            dl = c["dateline"]
            f_dl = sans_b(8)
            d.text((x + card_w - 5 - tw(d, dl, f_dl), y + 6), dl, font=f_dl,
                   fill=(255, 255, 255))
            hy = block(d, x + 6, y + 25, c["headline"], serif_b(16), NAVY_DARK,
                       card_w - 11, 19, max_lines=3)
            block(d, x + 6, hy + 2, c["text"], sans(13), INK,
                  card_w - 11, 16, max_lines=2)
        y += card_h + 5
    d.line([M, y, W - M, y], fill=RULE, width=1)
    y += 5

    # 8/9 — map + briefs -------------------------------------------------------
    bot_y = y
    d.rectangle([M, bot_y - 2, M + 262, bot_y + 13], fill=NAVY)
    d.text((M + 7, bot_y + 1), "WHERE IT HAPPENED", font=sans_b(10),
           fill=(255, 255, 255))
    d.text((M + 140, bot_y + 2), "pins = story numbers", font=sans(8),
           fill=(200, 208, 226))
    world_map(d, (M, bot_y + 25, M + 262, bot_y + 143), stories.PINS)

    bx = M + 282
    d.text((bx, bot_y), "ALSO ON SUNDAY 22 NOVEMBER — 16 MORE STORIES",
           font=sans_b(12), fill=NAVY)
    d.line([bx, bot_y + 16, W - M, bot_y + 16], fill=NAVY, width=1)
    col_w = (W - M - bx - 14) // 2
    f_br = sans(12)
    for i, (num, text) in enumerate(stories.BRIEFS):
        col = 0 if i < 8 else 1
        row = i if i < 8 else i - 8
        x = bx + col * (col_w + 14)
        yy = bot_y + 22 + row * 16
        num_badge(d, x, yy - 1, num, r=7, color=ACCENTS[i % len(ACCENTS)])
        d.text((x + 20, yy), text, font=f_br, fill=INK)
    y = bot_y + 149
    d.line([M, y, W - M, y], fill=RULE, width=1)
    y += 5

    # 10 — date check ------------------------------------------------------------
    d.rectangle([M, y, W - M, y + 40], outline=RED, width=2)
    d.text((M + 8, y + 5), "DATE CHECK", font=sans_b(10), fill=RED)
    block(d, M + 92, y + 4, stories.DATE_CHECK, sans(11), INK, CW - 108, 13, max_lines=2)
    y += 43

    # 11 — footer ------------------------------------------------------------------
    block(d, M, y, stories.SOURCES, sans(9), MUTED, CW, 11, max_lines=2)
    legend = [("CONFIRMED", "2+ outlets"), ("OFFICIAL", "on the record"),
              ("REPORTED", "one outlet"), ("CLAIM", "one side says"),
              ("FORECAST", "still to come")]
    lx = M
    ly = y + 23
    d.text((lx, ly), "CERTAINTY:", font=sans_b(9), fill=NAVY)
    lx += tw(d, "CERTAINTY:", sans_b(9)) + 8
    for label, gloss in legend:
        chip(d, lx, ly - 2, label)
        lx += tw(d, label, sans_b(9)) + 12 + 5
        d.text((lx, ly), gloss, font=sans(9), fill=MUTED)
        lx += tw(d, gloss, sans(9)) + 14
    return img


def main():
    img = draw_page()
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, "entry.png"), format="PNG", optimize=True)


if __name__ == "__main__":
    main()
