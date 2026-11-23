# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/gibalers-rgb/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/gibalers-rgb/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One image that sums up the world news of Sunday, 22 November 2026: a
newspaper front page — masthead, stormy globe at dawn, and the six stories
that defined the day. COP31 collapsing with no deal in Antalya; Iran
striking Bahrain and tankers near the Strait of Hormuz; the capture of
cartel boss 'El Chapo Isidro' in Sinaloa; a Russian drone hitting a
five-storey block near Kyiv; US stocks falling into correction as the AI
sell-off spreads; and the World Court's genocide ruling against Myanmar.
The image is drawn once (AI illustration + sharp rendered text) and the
program copies it to the output, byte for byte, every run.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This writes `out/entry.png` (1024×1024 PNG, under 1 MiB) — the whole entry.

## How the image was made

`compose.py` builds `entry.png`: it takes the AI-generated hero illustration
in `assets/` (a stormy globe with missile trails, tankers and a plunging
market chart, no text) and lays out the masthead, date and six story cards
with PIL, so every word is crisp and legible. Rebuild it with
`python3 compose.py`.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
