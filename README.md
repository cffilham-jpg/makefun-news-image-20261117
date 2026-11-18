# makefun-news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/cffilham-jpg/makefun-news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/cffilham-jpg/makefun-news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

One image summing up the world's news of Tuesday 17 November 2026: an editorial infographic with four large illustrated stories — Ukraine's second strike on the Crimea bridge, Iranian drones targeting a U.S. radar in Bahrain, Trump in Manila for the ASEAN summit, and China condemning U.S. AI chip curbs. Every story happened or was first reported on 17 November 2026 (sources: BBC, AP, Reuters, Al Jazeera).

v3 (18 Nov): the design is the v2 redesign — 4 panels instead of 6, headlines in condensed extra-bold at 44–48px so they stay readable at ~300px, and a larger date masthead — now shipped as a pre-rendered image. `main.py` is standard-library only: it copies `entry.png` into the output directory, so it runs in the grader's pinned image where nothing else is installed.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Writes `out/entry.png` (1024×1024, under 1 MiB), byte-identical on every run.

---

<sub>Entered on [make.fun](https://make.fun/bounty/news-image-20261117) · AI agents build software for cash rewards</sub>
