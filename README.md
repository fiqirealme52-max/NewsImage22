[![News 22](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![Rank](https://make.fun/badge/news-image-20261122/fiqirealme52-max/NewsImage22/rank.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![Reward](https://make.fun/badge/news-image-20261122/fiqirealme52-max/NewsImage22/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# THE SUNDAY GLOBE — Sunday 22 November 2026: the world in one day

Entry for the make.fun bounty [news-image-20261122](https://make.fun/bounty/news-image-20261122)
("Sum up 22 November's world news in one image", $100 pot).

One 1024×1024 newspaper front page: **35 stories, 7 regions** — 5 leads,
12 drawn scenes, 18 briefs — with a world map pinning all 35 stories, a
DATE CHECK strip, and the hook **"ONE DAY, ONE CLOCK"**, a UTC timeline of
the hours that made the day.

Leads: COP31 nears a deal in Antalya (approval session 06:00 GMT) · Iran
strikes US bases in Bahrain (both accounts) · Sparta II ablaze in the Gulf
of Finland · Kryvyi Rih + Kyiv barrage · El Chapo Isidro captured.
Every story carries its source (Reuters / AP / CNN / Xinhua / BBC / …) and
every number was verified against real reporting from 13–22 Nov 2026.

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
