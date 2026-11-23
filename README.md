# news-image-20261123 — The World Today, Monday 23 November 2026 (v2)

A newspaper front page summing up the world's news of Monday 23
November 2026 in one 1024x1024 image: Bahrain demanding UN action
after Iran's strike, Nepal's PM holding talks with Modi in Delhi, a
boy pulled alive from rubble after a Russian strike, South Korea's
education minister quitting in an AI-cheating scandal, and a M6.5
quake in the Vanuatu region — plus 31 more stories, all dated
Monday 23 November 2026, across 9 regions.

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

## How it is built

`compose.py` (Pillow only, no network, fully deterministic) draws the
front page and writes `entry.png`. `main.ts` (Node 22, stdlib only)
copies that exact image to the grader's output directory on every run.

## Reproduce

```sh
python3 compose.py            # writes entry.png (1024x1024, < 1 MiB)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Sources

Reuters, AP, Al Jazeera, AFP, UN, BBC, USGS, Arab News — all stories
published or first reported Monday 23 November 2026. Every story on
the page carries its 23 Nov date.

## License

MIT — see LICENSE.
