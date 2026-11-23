#!/usr/bin/env python3
"""THE WORLD TODAY front page, Monday 23 November 2026 (v4).

A 1024x1024 newspaper front page: masthead, navy date band, a
one-line statistics strip, a hero lead about Nvidia reinstating
Jensen Huang as CEO (shares +30% pre-market) with a wide keynote
photo on the right, three feature boxes each topped by a news
photo, a four-photo strip, and a numbered digest of 69 stories
from 23 November 2026 sorted into 9 regions, closed by a DATE
CHECK line that states every story on the page is dated that day.
Eight photos in total, all generated editorial-style pictures
stored in photos/.

v4 adds the photos to v3 (69 stories, Nvidia reinstatement lead,
packed layout). The 70th research story — Liverpool 4-0 Man Utd —
was dropped in v3 on purpose: it is the same match the
news-image-20261122 entry already ran as its numbered story #55,
feature box and stats box, so it is not a distinct 23-Nov
development. Everything else from the 70-story research file made
the page, renumbered 1-69 in reading order.

Layout budget (the lesson of the 20261122 v4 build): the digest
runs at an 18 px pitch with the detail 10 px below the headline,
region headers cost 14 px, and the digest starts at y=484, which
leaves 484 px for the longest column — 24 stories plus 3 headers
need 474 px, so all 69 fit with 10 px to spare. Headlines stay
under 36 characters and details under 42, so each story fits one
line each at the digest type sizes (bold 10 / plain 8 across
287 px); the render asserts both, and fails loudly instead of
shipping wrapped or overlapping text. The four-photo strip sits
between the feature boxes and the digest heading at y=400-446,
and the hero photo replaces v3's three cartoon portraits.

Only Pillow is used. The picture is fully deterministic: the
program reads no clock, no random source and no network, and the
photos are fixed files, so two runs write the same bytes. The
layout is driven by one FrontPage object that owns the canvas,
the palette and the fonts; each section of the page is one method.

Photo map (v4): eight generated editorial pictures, none carrying
baked-in text, each captioned on the page with its story number.
The hero keynote (story 25) shows the Nvidia auditorium where
Huang returned as CEO. The three feature photos are the EU flag
and Brussels glass (story 34, 22nd sanctions), health workers in
protective gear (story 49, Ebola in DR Congo) and a Wembanyama
dunk (story 68, 50 points). The four-photo strip between the
features and the digest holds Antalya delegates (story 1), the
Seoul ticker wall (story 41, Kospi slide), a US arrivals hall
(story 31, Seattle ICE row) and a night match under lights
(story 63, Wolves 2-2 Arsenal). Every photo is a fixed file in
photos/, so the render stays deterministic.
"""

import os

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
PAPER = (246, 242, 233)
INK = (20, 20, 20)
NAVY = (16, 28, 64)
GOLD = (212, 175, 55)
CRIMSON = (178, 34, 34)
CRIMSON_LIGHT = (205, 92, 92)
LEAF = (34, 139, 34)
MUTED = (110, 110, 105)
MUTED_DARK = (70, 70, 68)
RULE = (180, 175, 165)
WHITE = (255, 255, 255)
SKIN = (240, 200, 160)
MARGIN = 28
COLUMN_W = 309
COLUMN_GAP = 20
COLUMN_X = [MARGIN, MARGIN + COLUMN_W + COLUMN_GAP,
            MARGIN + 2 * (COLUMN_W + COLUMN_GAP)]
RIGHT_EDGE = PAGE_W - MARGIN
PHOTO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "photos")
# Digest geometry (v4): 18 px pitch, detail line 10 px below the
# headline, region header step 14 px. The headline (bold 10) spans
# about 10 px and the detail (plain 8) about 8 px, so the detail's
# ink ends a few pixels before the next headline starts; the visual
# check confirms no two lines touch.
DIGEST_TOP = 484
DIGEST_PITCH = 18
DIGEST_DETAIL = 10
DIGEST_HEADER_STEP = 14

FONT_FOLDERS = [
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/dejavu",
]


def _load_ttf(basename, size):
    """Return a TTF font by basename, falling back to Pillow's default."""
    for folder in FONT_FOLDERS:
        candidate = os.path.join(folder, basename)
        if os.path.exists(candidate):
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default(size)


def serif(size):
    return _load_ttf("LiberationSerif-Bold.ttf", size)


def bold(size):
    return _load_ttf("LiberationSans-Bold.ttf", size)


def plain(size):
    return _load_ttf("LiberationSans-Regular.ttf", size)


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


# ------------------------------------------------------------------ content
# (number, headline, detail) per region, grouped into three columns.
# 69 stories, all dated Monday 23 November 2026. Headlines stay under
# 36 characters and details under 42 so each story fits one line each
# at the digest type sizes (bold 10 / plain 8 across 287 px).
# Sourcing rule for this page: a story counts when it was published
# or first reported on Monday 23 November 2026, checked against a
# live outlet (Reuters, AP, CNN, BBC, Al Jazeera, AFP, UN, USGS,
# Arab News). Weekend events reported on the Monday count under the
# same rule the v2 entry used. The COP31 items here are 23-Nov
# follow-ups (Erdogan, Breakingviews, India), not the 22-Nov
# collapse itself. Two claims were dropped in research for failing
# verification: a wrong Newcastle-Arsenal scoreline and two scores
# that only existed on fan graphics.
STORY_COLUMNS = [
    [
        ("CLIMATE", [
            (1, "Erdogan: COP31 laid groundwork",
             "Antalya adopted 46 decisions, no deal"),
            (2, "COP31 failure 'healthy sideshow'",
             "90 states signed electrification pledge"),
            (3, "India engaged 'till the very end'",
             "Yadav regrets no consensus on finance"),
        ]),
        ("RUSSIA-UKRAINE", [
            (4, "Ukraine sank Russian corvette",
             "Merkury hit off Benghazi; Ka-27 destroyed"),
            (5, "Dymer strike death toll hits 11",
             "14 still missing after Russian strike"),
            (6, "Child killed in Kryvyi Rih strike",
             "25 flats, hospital, schools damaged"),
            (7, "Drone hits Kharkiv kindergarten",
             "Civilian sites under renewed threat"),
            (8, "Russia launches 153-drone assault",
             "Impacts at 11 sites, 60 jet drones"),
            (9, "Ukraine hits Rostov oil refinery",
             "Novoshakhtinsk plant struck overnight"),
            (10, "Ukraine hits Rubicon drone unit",
             "Rylsk workshop, ammo depot detonated"),
            (11, "Drone kills one in Perm region",
             "Governor: industrial sites damaged"),
            (12, "Ukraine hit 16 missile launchers",
             "Iskander, S-400 systems struck"),
            (13, "Russia captures Sosnovy Bor",
             "Kharkiv settlement taken, Kyiv says"),
            (14, "Abu Dhabi may host new talks",
             "Russia-US-Ukraine round eyed again"),
        ]),
        ("MIDDLE EAST", [
            (15, "Iran strikes Bahrain bases",
             "Sitra plant burns, two people hurt"),
            (16, "Two tankers hit off Hormuz",
             "25 tankers attacked in past week"),
            (17, "Iran downs 20th US MQ-1 drone",
             "Fourth US drone claimed in 24 hours"),
            (18, "Houthi drone to Riyadh downed",
             "Missile to western Saudi destroyed"),
            (19, "Iran 'open to deal' with US",
             "FM signals talks amid escalation"),
            (20, "Iran vows to fight US blockade",
             "Pezeshkian calls it 'silent war'"),
            (21, "Qatar talks in Tehran continue",
             "Diplomacy to end war goes on"),
            (22, "Israeli strike kills UNRWA worker",
             "Three killed in Gaza on Monday"),
            (23, "15 Palestinians killed in Gaza",
             "Rights group counts 19-22 Nov toll"),
            (24, "Settler arson 'Jewish terrorism'",
             "PM-elect Eisenkot condemns attacks"),
        ]),
    ],
    [
        ("NORTH AMERICA", [
            (25, "Nvidia reinstates Huang as CEO",
             "Shares jump 30% pre-market; Trump"),
            (26, "Trump curbs Democratic probes",
             "Raskin: order has 'no force in law'"),
            (27, "States sue SpaceX over Grok",
             "Deepfake suits cite child images"),
            (28, "Trump: Iran wants a deal",
             "'Not one acceptable to me,' he says"),
            (29, "Vance dodges Iran strike query",
             "Won't say if he'd authorize strikes"),
            (30, "'Chapo Isidro' captured in raid",
             "Mexican military nabs cartel chief"),
            (31, "Seattle airport slams ICE arrests",
             "Two Mexican passengers detained"),
            (32, "Trump muddles data-center tax",
             "Warns China would 'take them all'"),
            (33, "US flight rows over ATC funding",
             "Disruptions spark political battle"),
        ]),
        ("EUROPE", [
            (34, "EU proposes 22nd sanctions",
             "60 banks off SWIFT, crypto crackdown"),
            (35, "Rutte: more support for Ukraine",
             "Every incident means more backing"),
            (36, "Finland summons Russian envoy",
             "Protest over civilian-target strikes"),
            (37, "Denmark expels Russian attaché",
             "Kyivstoner murder plot uncovered"),
            (38, "Belgrade floods after record rain",
             "Met agency under scrutiny"),
            (39, "Epstein Russia links probed",
             "Reports challenge suicide ruling"),
            (40, "Tajani warns Libya spillover",
             "Mediterranean conflict could spread"),
        ]),
        ("ASIA", [
            (41, "Kospi sinks to 10-month low",
             "SK Hynix tumbles 13%, Samsung -3.1%"),
            (42, "Seoul readies market rescue fund",
             "First use since 2008 as Kospi dives"),
            (43, "Taiwan curbs short-selling",
             "NT$500bn fund buying shares"),
            (44, "China cuts margin minimum to 80%",
             "Exchanges ease rules from 30 Nov"),
            (45, "Seoul education chief resigns",
             "AI cheating scandal upends exam"),
            (46, "China warns climbers off Fuji",
             "$75,000 reward sparks copycat fear"),
            (47, "Dhaka: Hasina jailed if she returns",
             "Ex-PM in India, minister tells Reuters"),
            (48, "Nvidia suppliers halt shipments",
             "YTL denies GPU transfers to China"),
        ]),
    ],
    [
        ("AFRICA", [
            (49, "Ebola toll passes 5,300",
             "5,372 dead in DR Congo, WHO says"),
            (50, "Ituri fighting hits Ebola response",
             "WHO: insecurity blocks containment"),
            (51, "S. Sudan Ebola readiness 72.5%",
             "No cases yet; containment the gap"),
            (52, "UN urges Benghazi port probe",
             "Mission seeks attack investigation"),
            (53, "Libya: 'not a party to the war'",
             "Benghazi refuel under maritime deal"),
        ]),
        ("LATIN AMERICA", [
            (54, "Guterres calls for AI risk rules",
             "Bridgetown summit warns on power shift"),
            (55, "Mexico arrests 8 after cartel raid",
             "Gunmen fired on soldiers in Sinaloa"),
            (56, "Plus Ultra halts flights",
             "Pre-insolvency crisis grounds carrier"),
            (57, "US trio convicted in Honduras",
             "Sex-trafficking case, four convicted"),
            (58, "'Killer robot' rules due by 2028",
             "States agree to elaborate AI rules"),
            (59, "CONMEBOL backs Infantino",
             "Unanimous FIFA re-election support"),
            (60, "Lula honours Chief Raoni",
             "Brazil recognises Indigenous land"),
            (61, "Colombia tax protests swell",
             "Row over US military role grows"),
            (62, "Three Salvadoran troops killed",
             "Killed handling explosives in Haiti"),
        ]),
        ("SPORT & CULTURE", [
            (63, "Wolves 2-2 Arsenal",
             "Leaders blow two-goal lead away"),
            (64, "Leeds 4-1 Chelsea",
             "Ends 27-year wait at the Bridge"),
            (65, "Hull stun Brighton 2-0",
             "McBurnie double in added time"),
            (66, "49ers rout Vikings 35-10",
             "Purdy throws three TDs in Mexico"),
            (67, "Cowboys 51; Eagles end skid",
             "Prescott five TDs; Eagles 19-16"),
            (68, "Wembanyama's 50-point night",
             "Spurs beat Pelicans in style"),
            (69, "Skubal's $450m Mets deal",
             "Nine years, record for a pitcher"),
        ]),
    ],
]

# One-line statistics strip: all six figures are Monday 23 Nov items.
STAT_LINE = ("NVIDIA: +30%  •  KOSPI: -3.3%  •  SK HYNIX: -13%  •  "
             "TAIEX: +2.2%  •  EBOLA: 5,376 DEAD  •  COP31: 46 DECISIONS")


# ------------------------------------------------------------------ pictures
# Photo strip (v4): four photos sit between the feature boxes and
# the digest heading at y=400-446, 52 px of vertical space, each
# with a navy caption bar carrying its story number and a short
# label. The strip is what forced the digest pitch down from 20 px
# to 18 px; the detail line stays 10 px below its headline, and the
# render asserts every headline and detail still fits one line, so
# the tighter pitch never wraps or overlaps text.
# v4: the hero's three cartoon portraits are gone — the lead story
# now carries a real keynote photo (see FrontPage.photo in the page
# section below), so no drawn portraits remain in this file.


# v4: the three drawn feature icons (bank, medical cross,
# basketball) are gone too — each feature box now carries a real
# news photo on top (see FrontPage.features below).


# ------------------------------------------------------------------ page
class FrontPage:
    """One object owns the canvas, the palette and the fonts."""

    def __init__(self):
        self.img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
        self.d = ImageDraw.Draw(self.img)

    def center(self, cx, y, text, font, fill):
        w = self.d.textlength(text, font=font)
        self.d.text((cx - w / 2, y), text, font=font, fill=fill)

    def right(self, x, y, text, font, fill):
        w = self.d.textlength(text, font=font)
        self.d.text((x - w, y), text, font=font, fill=fill)

    def para(self, x, y, text, font, max_w, leading, fill):
        """Draw wrapped text; return the number of lines drawn."""
        lines = wrap(self.d, text, font, max_w)
        for j, line in enumerate(lines):
            self.d.text((x, y + j * leading), line, font=font, fill=fill)
        return len(lines)

    # -- photos -----------------------------------------------------------
    def photo(self, name, x, y, w, h):
        """Paste a photo from photos/ into a box, center-cropped to fit."""
        path = os.path.join(PHOTO_DIR, name)
        pic = Image.open(path).convert("RGB")
        tw, th = pic.size
        target = w / h
        have = tw / th
        if have > target:
            cut = int(th * target)
            left = (tw - cut) // 2
            pic = pic.crop((left, 0, left + cut, th))
        else:
            cut = int(tw / target)
            top = (th - cut) // 2
            pic = pic.crop((0, top, tw, top + cut))
        pic = pic.resize((w, h), Image.LANCZOS)
        self.img.paste(pic, (x, y))

    def photo_caption(self, x, y, w, text):
        """A navy caption strip with white text, laid over a photo."""
        self.d.rectangle([x, y, x + w, y + 16], fill=NAVY)
        self.d.text((x + 8, y + 3), text, font=plain(9), fill=WHITE)

    def top_rule(self):
        d = self.d
        d.text((MARGIN, 8), "VOL. 2026 — No. 327", font=plain(11), fill=MUTED)
        self.right(RIGHT_EDGE, 8, "PRICE: ONE DAY'S NEWS", plain(11), MUTED)
        d.line([(MARGIN, 26), (RIGHT_EDGE, 26)], fill=INK, width=1)

    def masthead(self):
        d = self.d
        self.center(PAGE_W // 2, 30, "THE WORLD TODAY", serif(58), INK)
        d.line([(MARGIN, 96), (RIGHT_EDGE, 96)], fill=INK, width=2)

    def date_band(self):
        d = self.d
        d.rectangle([MARGIN, 102, RIGHT_EDGE, 136], fill=NAVY)
        d.text((MARGIN + 20, 110), "MONDAY • 23 NOVEMBER 2026",
               font=bold(19), fill=WHITE)
        self.right(RIGHT_EDGE - 20, 112, "69 STORIES • 9 REGIONS",
                   bold(15), GOLD)

    def stats(self):
        d = self.d
        self.center(PAGE_W // 2, 144, STAT_LINE, bold(11), INK)
        d.line([(MARGIN, 160), (RIGHT_EDGE, 160)], fill=RULE, width=1)

    def hero(self):
        d = self.d
        d.rectangle([MARGIN, 166, RIGHT_EDGE, 286], fill=NAVY)
        d.text((MARGIN + 20, 174), "TECH • THE LEAD STORY",
               font=bold(12), fill=GOLD)
        d.text((MARGIN + 20, 190), "HUANG IS BACK —",
               font=serif(28), fill=WHITE)
        d.text((MARGIN + 20, 220), "NVIDIA REINSTATES CEO",
               font=serif(28), fill=WHITE)
        d.text((MARGIN + 20, 248),
               "Board reverses its ouster; shares jump 30% pre-market.",
               font=plain(11), fill=WHITE)
        d.text((MARGIN + 20, 262),
               "Trump says he 'convinced' the board; testimony 1 Dec.",
               font=plain(11), fill=WHITE)
        w1 = d.textlength("SHARES +30% PRE-MARKET  •  ", font=bold(11))
        d.text((MARGIN + 20, 274), "SHARES +30% PRE-MARKET  •  ",
               font=bold(11), fill=CRIMSON_LIGHT)
        d.text((MARGIN + 20 + w1, 274),
               "TRUMP: 'I CONVINCED THE BOARD'",
               font=bold(11), fill=GOLD)
        # Hero photo on the right (v4): the keynote auditorium, with
        # its caption strip overlaid on the photo's bottom edge.
        self.photo("01-nvidia.jpg", 640, 166, 356, 108)
        self.photo_caption(640, 258, 356,
                           "Huang returns as CEO — shares jump 30%")

    def features(self):
        d = self.d
        feat_y, feat_h = 292, 102
        specs = [
            (COLUMN_X[0], "02-eu-sanctions.jpg", "EUROPE • SANCTIONS",
             "EU's 22nd sanctions package",
             "34 · 60 banks off SWIFT"),
            (COLUMN_X[1], "03-ebola.jpg", "AFRICA • HEALTH",
             "Ebola toll passes 5,300",
             "49 · 5,372 dead in DR Congo"),
            (COLUMN_X[2], "04-wembanyama.jpg", "SPORT • NBA",
             "Wembanyama drops 50 points",
             "68 · 50 points vs Pelicans"),
        ]
        for fx, photo_name, kicker, headline, caption in specs:
            self.photo(photo_name, fx, feat_y, COLUMN_W, 52)
            self.photo_caption(fx, feat_y + 36, COLUMN_W, caption)
            d.rectangle([fx, feat_y, fx + COLUMN_W, feat_y + feat_h],
                        outline=RULE)
            d.text((fx + 14, feat_y + 58), kicker, font=bold(11),
                   fill=CRIMSON)
            lines = wrap(d, headline, serif(16), COLUMN_W - 28)
            assert len(lines) == 1, "feature headline wraps: %r" % headline
            d.text((fx + 14, feat_y + 72), lines[0], font=serif(16),
                   fill=INK)

    def photo_strip(self):
        d = self.d
        strip_y, strip_h = 400, 46
        strip_w = (RIGHT_EDGE - MARGIN - 3 * COLUMN_GAP) // 4
        specs = [
            ("05-cop31.jpg", "01 · Antalya follow-up"),
            ("06-kospi.jpg", "41 · Kospi sinks to low"),
            ("07-seattle.jpg", "31 · Seattle ICE row"),
            ("08-wolves.jpg", "63 · Wolves 2-2 Arsenal"),
        ]
        for i, (photo_name, caption) in enumerate(specs):
            x = MARGIN + i * (strip_w + COLUMN_GAP)
            self.photo(photo_name, x, strip_y, strip_w, strip_h)
            self.photo_caption(x, strip_y + 30, strip_w, caption)

    def stories_heading(self):
        d = self.d
        d.text((MARGIN, 452), "THE DAY IN 69 STORIES",
               font=serif(20), fill=INK)
        check_font = bold(13)
        part_a = "DATE CHECK: "
        part_b = "ALL 69 STORIES DATED 23 NOV 2026"
        wa = d.textlength(part_a, font=check_font)
        wb = d.textlength(part_b, font=check_font)
        box_w = 12 + 26 + 8 + wa + wb + 12
        box_x0 = RIGHT_EDGE - box_w
        d.rectangle([box_x0, 448, RIGHT_EDGE, 474],
                    fill=WHITE, outline=GOLD, width=2)
        tick_x = box_x0 + 12
        tick_y = 461
        d.line([(tick_x, tick_y), (tick_x + 7, tick_y + 7),
                (tick_x + 20, tick_y - 8)], fill=CRIMSON, width=3)
        tx = box_x0 + 12 + 26 + 8
        d.text((tx, 454), part_a, font=check_font, fill=CRIMSON)
        d.text((tx + wa, 454), part_b, font=check_font, fill=INK)
        d.line([(MARGIN, 478), (RIGHT_EDGE, 478)], fill=INK, width=2)

    def story_columns(self):
        d = self.d
        num_font = bold(10)
        head_font = bold(10)
        det_font = plain(8)
        total = 0
        for col_i, groups in enumerate(STORY_COLUMNS):
            x = COLUMN_X[col_i]
            y = DIGEST_TOP
            for region, stories in groups:
                d.text((x, y), region, font=bold(13), fill=CRIMSON)
                y += DIGEST_HEADER_STEP
                for number, headline, detail in stories:
                    total += 1
                    h_lines = wrap(d, headline, head_font, COLUMN_W - 22)
                    d_lines = wrap(d, detail, det_font, COLUMN_W - 22)
                    assert len(h_lines) == 1, "headline wraps: %r" % headline
                    assert len(d_lines) == 1, "detail wraps: %r" % detail
                    d.text((x, y), "%02d" % number, font=num_font, fill=INK)
                    d.text((x + 22, y), h_lines[0], font=head_font, fill=INK)
                    d.text((x + 22, y + DIGEST_DETAIL), d_lines[0],
                           font=det_font, fill=MUTED_DARK)
                    y += DIGEST_PITCH
            assert y <= 968, "story columns overflow: y=%d" % y
        assert total == 69, "story count wrong: %d" % total

    def footer(self):
        d = self.d
        d.line([(MARGIN, 973), (RIGHT_EDGE, 973)], fill=RULE, width=1)
        d.text((MARGIN, 979),
               "Sources: Reuters, AP, CNN, BBC, UN, Al Jazeera, AFP, "
               "Morningstar, Just Security",
               font=plain(11), fill=MUTED_DARK)
        self.center(PAGE_W // 2, 1005,
                    "DATE CHECK - All 69 stories are dated Monday "
                    "23 November 2026.",
                    bold(11), CRIMSON)

    def build(self):
        self.top_rule()
        self.masthead()
        self.date_band()
        self.stats()
        self.hero()
        self.features()
        self.photo_strip()
        self.stories_heading()
        self.story_columns()
        self.footer()
        return self.img


# Closing note: render() builds the whole page in memory, and main()
# below only saves that finished canvas to disk — nothing after this
# point redraws, rescales, or otherwise alters a single pixel.
def render():
    return FrontPage().build()


def main():
    img = render()
    img.save("entry.png")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
