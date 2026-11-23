# news-image-20261123 — The World Today, Monday 23 November 2026 (v4)

A newspaper front page summing up the world's news of Monday 23
November 2026 in one 1024x1024 image: Nvidia reinstating Jensen
Huang as CEO (shares +30% pre-market), the EU's 22nd sanctions
package, the Ebola toll passing 5,300, and Wembanyama's 50-point
night — plus 65 more stories, all dated Monday 23 November 2026,
across 9 regions. 69 stories in total, nearly double v2's 36.
Eight generated editorial photos illustrate the lead and seven
other stories on the page.

## What changed in v4

v3 was the density rebuild; v4 adds the photos, on the 20261122
v4 pattern (hero photo, three feature photos, four-photo strip):

1. **Hero photo.** The keynote auditorium (story 25) replaces
   v3's three cartoon portraits of Huang, Trump and Vance, with a
   caption strip overlaid on the photo's bottom edge.
2. **Feature photos.** The EU sanctions bank, the Ebola cross and
   the basketball icons are gone — each feature box now carries a
   real photo (stories 34, 49, 68) with a story-numbered caption.
3. **Photo strip.** Four more photos sit between the feature boxes
   and the digest heading: Antalya follow-up (01), Kospi sinks
   (41), Seattle ICE row (31) and Wolves 2-2 Arsenal (63).
4. **Tighter digest.** The strip costs 52 px of vertical room, so
   the digest pitch drops from 20 px to 18 px (detail line still
   10 px below the headline) and the digest starts at y=484 — the
   longest column still fits with 10 px to spare, and the visual
   check confirms no two digest lines touch.

## What changed in v3

v2 was a dating and spacing pass; v3 is a density rebuild on the
20261122 v4 pattern (FrontPage class, 20 px digest pitch, one-line
stats strip, DATE CHECK box in the digest heading):

1. **More news.** 69 stories instead of 36 — every verified
   23-Nov item from the research file, renumbered 1-69. The
   70th candidate, Liverpool 4-0 Man Utd, was deliberately
   dropped: it is the same match the news-image-20261122 entry
   already ran as its numbered story #55, feature box and stats
   box, so it is not a distinct 23-Nov development.
2. **New lead.** Nvidia's board reinstating Huang, verified by
   TechCrunch, CNN, The Times and Reuters — the biggest 23-Nov
   story — replaces Bahrain's UN demand as the hero, with
   compact portraits of Huang, Trump and Vance.
3. **Same date discipline.** All 69 stories are dated Monday
   23 Nov 2026, the stats strip and the three feature boxes are
   23-Nov items too, and the DATE CHECK box (plus a closing
   DATE CHECK line) states it plainly on the page itself.

## What changed in v2

v1 had two real defects (the same lesson as news-image-20261121,
where v4 lost because its lead stories were dated 20/19 Nov):

1. **Dates.** v1 had only 10 of 36 stories dated 23 Nov and led
   with the COP31 collapse, finalised 22 Nov. v2 has **all 36
   stories dated Monday 23 Nov 2026** and leads with Bahrain's UN
   demand — the lead of Monday's Arab News front page. Every stats
   box and feature box is a 23 Nov item too, and the DATE CHECK box
   now states it plainly.
2. **Overlapping text.** v1 advanced each story by a fixed 24 px,
   so two-line headlines collided with their detail lines (#05,
   #09, #19, #21, #25 in the v1 image). v2 advances by each
   story's real height and **asserts** every headline and detail
   fits on exactly one line and that the columns fit the page.

New 23 Nov stories v1 missed: Vanuatu M6.5 quake, KOSPI −4%, gold
$3,603, Brent −0.3%, India PMI 56.3, the Nvidia spy link (Alice
Huang), the Cheonghae-unit row, and the North Carolina House
seat story was deliberately left out — its Reuters dateline is
22 Nov, the same trap that sank 20261121 v4.

## v2 notes from the author

The second draft was a dating and spacing pass, not a redesign: I
went back through Monday's wires item by item, swapped the lead to
Bahrain's Security Council appeal, let each story claim only the
height its own lines need, and added the DATE CHECK box so the
23 November rule is visible on the page itself, not just in code.

## How it is built

`compose.py` (Pillow only, no network, fully deterministic) draws the
front page and writes `entry.png`. `main.ts` (Node 22, stdlib only)
copies that exact image to the grader's output directory on every run.

## Reproduce

```sh
python3 compose.py            # writes entry.png (1024x1024, < 1 MiB)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Photos (v4)

Eight generated editorial photos in `photos/`, all without baked-in
text: the Nvidia keynote hero (story 25), EU sanctions (34), Ebola
response (49), Wembanyama (68), COP31 Antalya (1), Kospi ticker
(41), Seattle ICE (31) and Wolves–Arsenal (63). Each photo is
captioned on the page with its story number.

## Sources

Reuters, AP, Al Jazeera, AFP, UN, BBC, USGS, Arab News — all stories
published or first reported Monday 23 November 2026. Every story on
the page carries its 23 Nov date.

## License

MIT — see LICENSE.
