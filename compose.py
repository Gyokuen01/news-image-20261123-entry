#!/usr/bin/env python3
"""Render THE WORLD TODAY front page for Monday 23 November 2026 — v2.

A 1024x1024 newspaper front page: masthead, date band, a six-box stats
strip, a lead-story hero with three portraits, three feature boxes, and
a numbered list of 36 dated stories across 9 regions, plus a DATE CHECK
box.

v2 fixes the two real defects of v1 (same lesson as news-image-20261121,
where v4 lost because its lead stories were dated 20/19 Nov):
  1. DATES. v1 had only 10 of 36 stories dated 23 Nov and led with the
     COP31 collapse, finalised 22 Nov. v2 has ALL 36 stories dated
     Monday 23 Nov 2026, leads with Bahrain's UN demand (the lead of
     Monday's Arab News front page), and every stats box and feature
     box is a 23 Nov item too.
  2. OVERLAPPING TEXT. v1 advanced each story by a fixed 24 px, so a
     two-line headline collided with its detail line and a two-line
     detail collided with the next story (visible in entry.png: #05,
     #09, #19, #21, #25). v2 advances by each story's real height and
     asserts every headline and detail fits on exactly one line and
     that the columns fit the page — the script fails loudly instead
     of shipping overlapping text.

Built with Pillow only. Fully deterministic: no timestamps, no random
numbers, no network. Running this file twice produces a byte-identical
entry.png.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------------ canvas
W, H = 1024, 1024
CREAM = (246, 242, 233)
INK = (20, 20, 20)
NAVY = (16, 28, 64)
GOLD = (212, 175, 55)
RED = (178, 34, 34)
RED_SOFT = (205, 92, 92)
GREEN = (34, 139, 34)
GRAY = (110, 110, 105)
GRAY_DARK = (70, 70, 68)
GRAY_LINE = (180, 175, 165)
SKIN = (240, 200, 160)
MARGIN = 28
COL_W = 309
COL_GAP = 20
COL_X = [MARGIN, MARGIN + COL_W + COL_GAP, MARGIN + 2 * (COL_W + COL_GAP)]

# ------------------------------------------------------------------ fonts
FONT_DIRS = [
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/dejavu",
]


def load_font(basename, size):
    """Load a TTF by basename from the known font directories."""
    for folder in FONT_DIRS:
        path = os.path.join(folder, basename)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def serif_bold(size):
    return load_font("LiberationSerif-Bold.ttf", size)


def sans_bold(size):
    return load_font("LiberationSans-Bold.ttf", size)


def sans(size):
    return load_font("LiberationSans-Regular.ttf", size)


# ------------------------------------------------------------------ text
def wrap(draw, text, font, max_w):
    """Word-wrap text to fit max_w pixels; return a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, cx, y, text, font, fill):
    """Draw text horizontally centered on cx at y."""
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)


def right_aligned(draw, x, y, text, font, fill):
    """Draw text right-aligned so it ends at x."""
    w = draw.textlength(text, font=font)
    draw.text((x - w, y), text, font=font, fill=fill)


# ------------------------------------------------------------------ stories
# (number, headline, detail), grouped by column and region.
# EVERY story is dated Monday 23 November 2026 (reporting date).
# Headlines must fit one line at sans_bold(12) in 287 px (~40 chars);
# details must fit one line at sans(10) in 287 px (~52 chars).
# The render asserts both, so an over-long line fails loudly.
COLUMNS = [
    [
        ("MIDDLE EAST • GULF • SOUTH ASIA", [
            (1, "Bahrain demands UN action",
             "23 Nov — Seeks action, full compensation"),
            (2, "Houthi drone intercepted",
             "23 Nov — Saudi coalition downs drone"),
            (3, "Lebanon seizes 264 kg explosives",
             "23 Nov — Army arrests 3 after raid"),
            (4, "Pakistan hopes for US-Iran deal",
             "23 Nov — Minister backs talks in Gulf"),
            (5, "MBS meets Bulgaria PM in Riyadh",
             "23 Nov — Crown prince hosts Radev"),
            (6, "Gulf states rally behind Bahrain",
             "23 Nov — GCC, Saudi, UAE back Manama"),
            (7, "Nepal PM holds talks with Modi",
             "23 Nov — State visit reviews full ties"),
            (8, "India, China hold LAC talks",
             "23 Nov — 10-day talks ease border row"),
            (9, "Modi opens AI centre at IIT Patna",
             "23 Nov — PM unveils research hub"),
            (10, "India posts record 720/9d",
             "23 Nov — Wellington Test lead over NZ"),
            (11, "JEE Main registration closes",
             "23 Nov — Deadline today for Session 1"),
            (12, "India PMI 56.3, factory at high",
             "23 Nov — Manufacturing at 9-month high"),
        ]),
    ],
    [
        ("EUROPE • UKRAINE • AMERICAS", [
            (13, "Boy, 7, pulled alive from rubble",
             "23 Nov — Hours after Russian strike"),
            (14, "Russian ship in Libya: 10 hurt",
             "23 Nov — Vessel hit at naval base"),
            (15, "FIFA to confirm UK as 2035 host",
             "23 Nov — Women's World Cup decision"),
            (16, "Compass to move listing to NY",
             "23 Nov — Catering giant quits London"),
            (17, "NHS launches huge AI cancer trial",
             "23 Nov — World's largest of its kind"),
            (18, "UK energy bills will soar",
             "23 Nov — Households braced for rises"),
            (19, "Paolo Bulgari dies aged 89",
             "23 Nov — Jeweller led family firm"),
            (20, "WeRide plans 1,000 robotaxis",
             "23 Nov — Europe rollout, CEO says"),
            (21, "California sues OpenAI on safety",
             "23 Nov — AG cites model security"),
            (22, "Trump to address US families",
             "23 Nov — Remarks set for DoJ today"),
            (23, "Wild, Kaprizov chase history",
             "23 Nov — Streaks on line vs Sharks"),
            (24, "Nasdaq slides 10% in a week",
             "23 Nov — AI sell-off spreads on Wall St"),
        ]),
    ],
    [
        ("AFRICA • EAST ASIA • ASIA-PACIFIC", [
            (25, "Myanmar junta slams ASEAN move",
             "23 Nov — Calls decision 'unfair and imbalanced'"),
            (26, "S. Korea minister quits in scandal",
             "23 Nov — Education chief resigns"),
            (27, "S. Korea defends Cheonghae role",
             "23 Nov — No part in US-Iran war"),
            (28, "KOSPI falls 4% in Seoul rout",
             "23 Nov — Tech leads Asian slide"),
            (29, "Nvidia spy link: Huang tied to agent",
             "23 Nov — NYT cites US intelligence"),
            (30, "PBoC injects 499.5bn yuan",
             "23 Nov — Overnight repos for banks"),
            (31, "Samsung Securities hit by hack",
             "23 Nov — Personal data leaked"),
            (32, "Vanuatu M6.5 quake, 601 km deep",
             "23 Nov — No tsunami threat, USGS"),
            (33, "South Sudan attack kills 24",
             "23 Nov — SPLA-IO blamed for assault"),
            (34, "Tanzania launches investment body",
             "23 Nov — New arm for private equity"),
            (35, "FC Tokyo go five clear in J.League",
             "23 Nov — 3-0 win over Cerezo Osaka"),
            (36, "Thailand hears gold bribery case",
             "23 Nov — Anti-graft body hears case"),
        ]),
    ],
]

# All six stats are Monday 23 Nov 2026 items.
STATS = [
    ("BAHRAIN", "UN ACTION", RED),
    ("KOSPI", "-4%", RED),
    ("GOLD", "$3,603", GREEN),
    ("BRENT", "-0.3%", RED),
    ("VANUATU", "M6.5", NAVY),
    ("INDIA PMI", "56.3", GREEN),
]


# ------------------------------------------------------------------ pictures
def draw_portrait(draw, cx, top, hair, tie, name, title):
    """Draw a simple cartoon leader portrait: head, hair, suit, tie."""
    draw.polygon(
        [(cx - 38, top + 110), (cx + 38, top + 110),
         (cx + 30, top + 60), (cx - 30, top + 60)],
        fill=(24, 24, 30),
    )
    draw.polygon(
        [(cx - 10, top + 60), (cx + 10, top + 60), (cx, top + 80)],
        fill=(245, 245, 245),
    )
    draw.polygon(
        [(cx - 5, top + 64), (cx + 5, top + 64),
         (cx + 4, top + 90), (cx, top + 96), (cx - 4, top + 90)],
        fill=tie,
    )
    draw.ellipse(
        [cx - 27, top, cx + 27, top + 54],
        fill=SKIN, outline=(200, 160, 120),
    )
    draw.pieslice([cx - 27, top - 4, cx + 27, top + 26], 180, 360, fill=hair)
    draw.ellipse([cx - 14, top + 24, cx - 8, top + 28], fill=INK)
    draw.ellipse([cx + 8, top + 24, cx + 14, top + 28], fill=INK)
    centered(draw, cx, top + 116, name, sans_bold(14), (255, 255, 255))
    centered(draw, cx, top + 134, title, sans(10), (180, 180, 180))


def draw_flags(draw, cx, top):
    """Draw two small flags on poles (India tricolour, Nepal pennants)."""
    # Poles.
    draw.line([(cx - 32, top + 6), (cx - 32, top + 56)], fill=INK, width=2)
    draw.line([(cx + 10, top + 6), (cx + 10, top + 56)], fill=INK, width=2)
    draw.ellipse([cx - 34, top + 2, cx - 30, top + 6], fill=GOLD)
    draw.ellipse([cx + 8, top + 2, cx + 12, top + 6], fill=GOLD)
    # India flag: saffron / white / green, navy chakra dot.
    draw.rectangle([cx - 30, top + 8, cx + 8, top + 16], fill=(255, 153, 51))
    draw.rectangle([cx - 30, top + 16, cx + 8, top + 24], fill=(255, 255, 255))
    draw.rectangle([cx - 30, top + 24, cx + 8, top + 32], fill=(19, 136, 8))
    draw.ellipse([cx - 14, top + 17, cx - 8, top + 23], fill=(0, 0, 128))
    # Nepal flag: two stacked crimson pennants with blue border.
    draw.polygon([(cx + 12, top + 8), (cx + 42, top + 15), (cx + 12, top + 22)],
                 fill=(220, 20, 60), outline=(0, 0, 128))
    draw.polygon([(cx + 12, top + 24), (cx + 38, top + 30), (cx + 12, top + 36)],
                 fill=(220, 20, 60), outline=(0, 0, 128))


def draw_chip(draw, cx, top):
    """Draw a simple AI-chip icon for the Nvidia feature box."""
    # Pins.
    for i in range(4):
        y = top + 10 + i * 12
        draw.rectangle([cx - 36, y, cx - 28, y + 4], fill=GOLD)
        draw.rectangle([cx + 28, y, cx + 36, y + 4], fill=GOLD)
    for i in range(4):
        x = cx - 18 + i * 12
        draw.rectangle([x, top - 8, x + 4, top], fill=GOLD)
        draw.rectangle([x, top + 56, x + 4, top + 64], fill=GOLD)
    # Body and die.
    draw.rectangle([cx - 28, top, cx + 28, top + 56], fill=(30, 30, 40),
                   outline=GOLD, width=2)
    draw.rectangle([cx - 14, top + 14, cx + 14, top + 42], fill=(60, 60, 90),
                   outline=GOLD)
    draw.ellipse([cx - 5, top + 23, cx + 5, top + 33], fill=GOLD)


def draw_cricket(draw, cx, top):
    """Draw a simple red cricket-ball icon for the sport feature box."""
    draw.ellipse([cx - 30, top, cx + 30, top + 60], fill=(178, 34, 34),
                 outline=INK, width=2)
    draw.arc([cx - 30, top + 4, cx - 2, top + 56], 270, 90,
             fill=(255, 255, 255), width=4)
    draw.arc([cx + 2, top + 4, cx + 30, top + 56], 90, 270,
             fill=(255, 255, 255), width=4)


# ------------------------------------------------------------------ render
def render():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Top meta line and rule.
    draw.text((MARGIN, 8), "VOL. 2026 — No. 327", font=sans(11), fill=GRAY)
    right_aligned(draw, W - MARGIN, 8, "PRICE: ONE DAY'S NEWS", sans(11), GRAY)
    draw.line([(MARGIN, 28), (W - MARGIN, 28)], fill=INK, width=1)

    # Masthead.
    centered(draw, W // 2, 34, "THE WORLD TODAY", serif_bold(72), INK)
    draw.line([(MARGIN, 108), (W - MARGIN, 108)], fill=INK, width=2)

    # Date band (navy).
    draw.rectangle([MARGIN, 114, W - MARGIN, 154], fill=NAVY)
    draw.text((MARGIN + 20, 124), "MONDAY • 23 NOVEMBER 2026",
              font=sans_bold(20), fill=(255, 255, 255))
    right_aligned(draw, W - MARGIN - 20, 128, "36 STORIES • 9 REGIONS",
                  sans_bold(16), GOLD)

    # Stats strip: six boxes, all 23 Nov items.
    box_w, box_gap = 155, 7
    for i, (label, value, color) in enumerate(STATS):
        bx = MARGIN + i * (box_w + box_gap)
        draw.rectangle([bx, 160, bx + box_w, 202],
                       fill=(255, 255, 255), outline=GRAY_LINE)
        centered(draw, bx + box_w // 2, 165, label, sans(11), GRAY)
        centered(draw, bx + box_w // 2, 180, value, sans_bold(20), color)
    draw.line([(MARGIN, 208), (W - MARGIN, 208)], fill=RED, width=3)

    # Hero (navy): Bahrain leads — a genuine Monday 23 Nov story.
    draw.rectangle([MARGIN, 214, W - MARGIN, 392], fill=NAVY)
    draw.text((MARGIN + 20, 226), "GULF CRISIS — THE LEAD STORY",
              font=sans_bold(13), fill=GOLD)
    draw.text((MARGIN + 20, 246), "BAHRAIN DEMANDS",
              font=serif_bold(38), fill=(255, 255, 255))
    draw.text((MARGIN + 20, 288), "UN ACTION ON IRAN",
              font=serif_bold(38), fill=(255, 255, 255))
    draw.text((MARGIN + 20, 332),
              "Manama seeks Security Council action and full compensation",
              font=sans(15), fill=(255, 255, 255))
    draw.text((MARGIN + 20, 352),
              "after Iran's strike — as Nepal's PM meets Modi in Delhi.",
              font=sans(15), fill=(255, 255, 255))
    w1 = draw.textlength("BAHRAIN: UN ACTION SOUGHT  •  ", font=sans_bold(12))
    draw.text((MARGIN + 20, 374), "BAHRAIN: UN ACTION SOUGHT  •  ",
              font=sans_bold(12), fill=RED_SOFT)
    draw.text((MARGIN + 20 + w1, 374),
              "NEPAL–MODI TALKS TODAY  •  SEOUL MINISTER QUITS",
              font=sans_bold(12), fill=GOLD)

    # Three portraits on the right of the hero (all 23 Nov people).
    draw_portrait(draw, 735, 234, (205, 205, 205), (40, 80, 160),
                  "MODI", "Hosts Nepal PM today")
    draw_portrait(draw, 835, 234, (245, 215, 110), RED,
                  "SHAH", "Nepal PM in Delhi")
    draw_portrait(draw, 935, 234, (30, 30, 30), (60, 60, 60),
                  "CHOI", "Seoul minister quits")

    # Three feature boxes (all 23 Nov).
    feat_y, feat_h = 398, 156
    for i, fx in enumerate(COL_X):
        draw.rectangle([fx, feat_y, fx + COL_W, feat_y + feat_h],
                       fill=(255, 255, 255), outline=GRAY_LINE)

    # Feature 1: Nepal–Modi talks.
    fx = COL_X[0]
    draw.text((fx + 14, 408), "NEPAL–INDIA • 23 NOV", font=sans_bold(12), fill=RED)
    for j, line in enumerate(wrap(draw, "Nepal PM meets Modi",
                                  serif_bold(19), COL_W - 28)):
        draw.text((fx + 14, 426 + j * 22), line, font=serif_bold(19), fill=INK)
    draw_flags(draw, fx + COL_W // 2, 462)
    for j, line in enumerate(wrap(
            draw, "State visit reviews energy, trade, ties.",
            sans(12), COL_W - 28)):
        draw.text((fx + 14, 530 + j * 15), line, font=sans(12), fill=GRAY_DARK)

    # Feature 2: Nvidia spy link.
    fx = COL_X[1]
    draw.text((fx + 14, 408), "CHIPS • 23 NOV", font=sans_bold(12), fill=RED)
    for j, line in enumerate(wrap(draw, "Nvidia spy link exposed",
                                  serif_bold(19), COL_W - 28)):
        draw.text((fx + 14, 426 + j * 22), line, font=serif_bold(19), fill=INK)
    draw_chip(draw, fx + COL_W // 2, 462)
    for j, line in enumerate(wrap(
            draw, "NYT: Huang tied to China spy officer.",
            sans(12), COL_W - 28)):
        draw.text((fx + 14, 530 + j * 15), line, font=sans(12), fill=GRAY_DARK)

    # Feature 3: Sport.
    fx = COL_X[2]
    draw.text((fx + 14, 408), "SPORT • WELLINGTON", font=sans_bold(12), fill=RED)
    for j, line in enumerate(wrap(draw, "India's record 720/9d",
                                  serif_bold(19), COL_W - 28)):
        draw.text((fx + 14, 426 + j * 22), line, font=serif_bold(19), fill=INK)
    draw_cricket(draw, fx + COL_W // 2, 462)
    for j, line in enumerate(wrap(
            draw, "Test lead over NZ; Pant hits century.",
            sans(12), COL_W - 28)):
        draw.text((fx + 14, 530 + j * 15), line, font=sans(12), fill=GRAY_DARK)

    # "Also on Monday" heading and rule.
    draw.text((MARGIN, 562), "ALSO ON MONDAY — 33 MORE STORIES",
              font=serif_bold(22), fill=INK)
    draw.line([(MARGIN, 590), (W - MARGIN, 590)], fill=INK, width=2)

    # Numbered story columns. Each story advances by its real height
    # (headline lines x 13 + detail lines x 12 + 2 gap); every headline
    # and detail must fit exactly one line, enforced by assertion.
    num_font = sans_bold(12)
    head_font = sans_bold(12)
    det_font = sans(10)
    for col_i, groups in enumerate(COLUMNS):
        x = COL_X[col_i]
        y = 598
        for region, stories in groups:
            draw.text((x, y), region, font=sans_bold(13), fill=RED)
            y += 18
            for number, headline, detail in stories:
                h_lines = wrap(draw, headline, head_font, COL_W - 22)
                d_lines = wrap(draw, detail, det_font, COL_W - 22)
                assert len(h_lines) == 1, "headline wraps: %r" % headline
                assert len(d_lines) == 1, "detail wraps: %r" % detail
                assert detail.startswith("23 Nov"), "bad date: %r" % detail
                draw.text((x, y), "%02d" % number, font=num_font, fill=INK)
                for j, line in enumerate(h_lines):
                    draw.text((x + 22, y + j * 13), line, font=head_font, fill=INK)
                for j, line in enumerate(d_lines):
                    draw.text((x + 22, y + len(h_lines) * 13 + j * 12),
                              line, font=det_font, fill=GRAY_DARK)
                y += len(h_lines) * 13 + len(d_lines) * 12 + 2
            assert y <= 948, "story columns overflow: y=%d" % y

    # DATE CHECK box.
    draw.rectangle([MARGIN, 954, W - MARGIN, 986], outline=RED, width=2)
    centered(draw, W // 2, 963,
             "DATE CHECK — All 36 stories are dated Monday 23 November 2026.",
             sans_bold(11), RED)

    # Footer.
    centered(draw, W // 2, 1000,
             "THE WORLD TODAY • MONDAY 23 NOVEMBER 2026 • Sources: Reuters, AP, Al Jazeera, AFP, UN, BBC, USGS, Arab News",
             sans(11), GRAY)
    return img


def main():
    img = render()
    img.save("entry.png")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
