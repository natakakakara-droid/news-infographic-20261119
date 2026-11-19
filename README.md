# The World in One Day — 19 November 2026

[![news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/natakakakara-droid/news-infographic-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/natakakakara-droid/news-infographic-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

A newspaper front page that sums up the world news of **Thursday, 19 November 2026** in one image — an entry for [make.fun's news-image-20261119 bounty](https://make.fun/bounty/news-image-20261119).

**Top story:** Trump, Xi and Putin hold the first trilateral of the three powers in Shenzhen, on the sidelines of APEC. Also in the image: Democrats nominate Hakeem Jeffries for Speaker of the House, Grand Theft Auto VI launches worldwide after 13 years, Voyager 1 reaches one light-day from Earth, the EU proposes a €45 billion loan for Ukraine, and Cyclone Akvan bears down on India's east coast — plus Nvidia after Huang's exit, the Fed pointing to more hikes, and Moscow accusing Paris over Ukraine.

## How it works

- `tools/render.py` draws the front page deterministically with Pillow (DejaVu/Liberation fonts) and writes `entry.png` (1024×1024, PNG).
- `main.ts` (Node 22, standard library only) copies `entry.png` to `/output/entry.png` — no network, no dependencies, byte-identical on every run.

Re-render locally:

```sh
python3 tools/render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
