# f1devbin.github.io

Personal page of Max (f1devbin) and the entry point to his projects, in 7 languages: <https://f1devbin.github.io/>
(English at the root, `/ru/ /es/ /pt/ /tr/ /vi/ /zh/`).

## Build

```bash
python3 build.py      # index.html, <lang>/index.html, assets/site.css, sitemap.xml, robots.txt, 404.html
```

Commit the output; GitHub Pages serves the repository root as is. All text lives in `T` in `build.py`; the build
stops if a key is missing in any language. `[label](key)` in a string becomes a link to `links(lang)[key]`.

Images are made by `tools/images.py` (Pillow, numpy, scipy, fonttools, brotli) from the projects' own files and
committed too:

```bash
python3 tools/images.py --icon ../my-ip-geo-plasma6/package/contents/icon.png \
  --crl ../Crypto-Research-Labs/docs/screenshots/dashboard.png \
  --tbm ../telegram-bot-manager/docs/screenshots/webhook.png \
  --myip ../my-ip-geo-plasma6/screenshots/main.png
```

It writes the cat sticker (the widget's icon without the "IP & Geo" lettering; the drawing itself is untouched),
the project screenshots in three widths, `assets/og/<lang>.png` share cards, `favicon.ico`, `apple-touch-icon.png`
and `assets/sizes.json`, which `build.py` reads for the `width`/`height` attributes.

## Privacy and speed

- No cookies, analytics or scripts, nothing loaded from other hosts. A Content Security Policy in a meta tag
  allows only same-origin styles, fonts and images (`connect-src 'self'` is there only so audit tools can read
  `robots.txt`).
- IBM Plex Sans is self-hosted (`assets/fonts`, SIL OFL 1.1, see `assets/fonts/OFL.txt`), split by script with
  `unicode-range`, so a page downloads only the subsets it uses. Chinese falls back to the system CJK font.
- Lighthouse (mobile, local): performance 98-99, accessibility 100, best practices 100, SEO 100.

## Search engines

- `robots.txt` sits at the host root, so it applies to every project site under `f1devbin.github.io` and lists
  their sitemaps (Crypto Research Labs, Telegram Bot Manager). Add a project's sitemap to `PROJECT_SITEMAPS`.
- Verification: codes in `verification.json` (`google`, `yandex`, `bing`), then rebuild. The Google HTML
  verification file for this account is at the root.
- Every page has a canonical URL, `hreflang` for all 7 languages plus `x-default`, Open Graph tags with a share card
  in its language, and JSON-LD: `ProfilePage` with the `Person`, and the projects (`Dataset` with creator and
  license for Crypto Research Labs, `SoftwareSourceCode` for the other two).

### Query map

This page should win the name queries and hand the rest to the project pages through descriptive links, so the
two don't compete for the same queries.

| Page | Queries it targets |
|---|---|
| this page | f1devbin, Max f1devbin, f1devbin github |
| Telegram Bot Manager and its guides | set telegram webhook online, check webhook getWebhookInfo, delete telegram webhook, telegram bot commands editor; установить вебхук телеграм бота онлайн, проверить вебхук, удалить вебхук телеграм бота |
| My IP & Geo | kde plasma 6 ip widget, plasma 6 network monitor widget, kde port scanner widget; виджет kde plasma 6 ip адрес |
| Crypto Research Labs | do crypto trading strategies work, crypto strategy backtest with fees, pre-registered trading research, crypto course for beginners; работают ли торговые стратегии криптовалют, курс по криптовалютам для начинающих |

The links from this page to those pages use the same words as the queries (see `tbm_proof`, `crl_proof`).

## Things to keep current

- `crl_cap` and the Crypto Research Labs screenshot are dated; refresh both when the dashboard changes a lot.
- `YEAR` in `build.py` for the copyright line.
