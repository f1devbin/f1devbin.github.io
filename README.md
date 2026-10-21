# f1devbin.github.io

Landing page for all of f1devbin's projects, in 7 languages: <https://f1devbin.github.io/>

- `build.py` generates `index.html`, `<lang>/index.html`, `sitemap.xml`, `robots.txt`, `404.html` (run `python3 build.py`, commit the output).
- `robots.txt` is at the host root, so it applies to every project site under `f1devbin.github.io` and lists their sitemaps
  (Crypto Research Labs, Telegram Bot Manager). Add a project's sitemap to `PROJECT_SITEMAPS` in `build.py`.
- Search-engine verification: put codes in `verification.json`, e.g. `{"yandex": "…", "google": "…", "bing": "…"}`,
  then rebuild. The Google HTML verification file for this account is already at the root.
