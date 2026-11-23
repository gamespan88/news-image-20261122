[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/gamespan88/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/gamespan88/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# THE WORLD IN ONE DAY — Sunday 22 November 2026

One illustrated newspaper page that sums up a single day's world news:
Sunday 22 November 2026. Thirty-one stories from seven regions — three
illustrated front-page leads (186 drones over Ukraine, the COP31 final text,
Iran's radar claim vs Bahrain's denial), twelve illustrated cards, and sixteen
numbered briefs — plus a numbers strip, a UTC timeline, a dotted world map
whose pins match the story numbers, and a DATE CHECK box that lists the
neighbouring days' news deliberately left out.

## How it works

`main.py` is the entrypoint: run in a sandbox with no network, it draws the
whole page with PIL (`draw.py` scenes, `stories.py` content, bundled fonts in
`fonts/`) and writes `/output/entry.png` — a 1024×1024 PNG, byte-identical on
every run. All pictures and the map are original, drawn in code.

## Run it

```sh
python3 main.py   # writes /output/entry.png
```

`preview.png` is a rendered copy of the entry.
