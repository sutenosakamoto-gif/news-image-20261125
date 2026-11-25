# World News — 25 November 2026 (one-image summary)

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/sutenosakamoto-gif/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/sutenosakamoto-gif/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A one-image broadsheet front page summarising thirty-three world news
stories of Wednesday, 25 November 2026, prepared as an entry
for the make.fun bounty "Sum up 25 November's world news in one image"
(final deadline 2026-11-27 09:00 JST).

## Contents

- `main.py` — the entry point: a standard-library only program that
  copies the finished page to `/output/entry.png` (no network).
- `page.png` — the finished 1024×1024 front page.
- `render.py` — the build-time renderer that drew `page.png` from
  `content.py` with real fonts (system Noto Serif, OFL).
- `content.py` — the day's stories, numbers, timeline and exclusions
  as structured data.
- `SOURCES.md` — the thirty-three stories, their sources (outlet + date)
  and URLs.

## How to run

```bash
python3 main.py   # standard library only, no dependencies
```

Running `python3 main.py` copies `page.png` to `/output/entry.png`,
falling back to `./entry.png` next to the script when `/output` is not
writable. The render is deterministic: repeated runs produce identical
bytes.

To re-render the page from the structured content (build-time only,
needs PIL and the Noto fonts):

```bash
python3 render.py   # writes page.png
```

## The thirty-three stories

Lead panels (large):

1. Houthis say they hit a Saudi refinery and Riyadh finance district;
   coalition says it stopped four drones (Reuters) — CLAIM
2. Asia tumbles as tariff threat kills the AI rebound: MSCI Asia-Pacific
   ex-Japan −2.3%; Seoul −5.3% (Reuters) — new Section 301 tariffs
   REPORTED as imminent, not in force
3. Shenzhou-24 carries the first Pakistani — and first foreign astronaut
   — to Tiangong (Reuters)

Medium panels:

4. Israeli strike kills senior Hamas official and family in Gaza
5. Ukraine drones hit two Russian oil refineries; one killed
6. All Colombia hostages rescued in Cartagena
7. China probes a fourth Politburo member
8. Thanksgiving storms threaten travel and Macy's 100th parade
9. Australia–Solomon Islands sign security pact
10. Ramaphosa wins court bid to overturn 'Farmgate' report
11. EU proposes €50bn sovereign fund to lead in quantum by 2030
12. Greeks strike over wages and public services
13. Rescuers search for 'dozens' trapped in Indonesian mine

Plus twenty briefs (14–33), a world map with numbered pins, a
THE DAY IN NUMBERS strip, a UTC timeline, and a DATE CHECK footer
naming the stories excluded as other days' news.
