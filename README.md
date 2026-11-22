[![News 22](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![Rank](https://make.fun/badge/news-image-20261122/fiqirealme52-max/NewsImage22/rank.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![Reward](https://make.fun/badge/news-image-20261122/fiqirealme52-max/NewsImage22/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# Sunday 22 November 2026 — one day, everything that happened: 35 stories, 7 regions

Entry for the make.fun bounty [news-image-20261122](https://make.fun/bounty/news-image-20261122)
("Sum up 22 November's world news in one image", $100 pot).

One 1024×1024 one-day evidence board: **35 stories, 7 regions** — a giant
date masthead, a strip of 6 checkable numbers (35 stories · 7 regions ·
856 Hong Kong candidates · $500bn Nvidia value wiped · 629/6 India's record
in NZ · 227 m Kerch Bridge arch), 3 leads + 10 mediums with drawn scenes,
a correct-geography world map pinning the 13 drawn stories, 22 briefs, a
one-line BY THE CLOCK strip, and a DATE CHECK box that names its one
exception (Kerch Bridge, 16–17 Nov) instead of hiding it.

Leads: COP31's new text goes to objections (03:00 UTC) and approval
(06:00 UTC) in Antalya — no deal adopted yet · Hong Kong votes, 856
candidates for 723 seats · India 629/6, a record total in New Zealand.
Every story carries its source (Reuters / AP / AFP / SCMP / BBC / …) and
every number was verified against real reporting from 20–22 Nov 2026.

## Files

- `entry.png` — the image (1024×1024 PNG, ~204 KB)
- `main.ts` — entrypoint: copies `entry.png` to `/output/entry.png`
  (Node 22, standard library only, no network)

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# -> out/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
