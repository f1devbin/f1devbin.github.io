#!/usr/bin/env python3
"""Generates the landing's images from the source projects (run by hand, output is committed).

    python3 tools/images.py --icon ../my-ip-geo-plasma6/package/contents/icon.png \
        --crl ../Crypto-Research-Labs/docs/screenshots/dashboard.png \
        --tbm ../telegram-bot-manager/docs/screenshots/webhook.png \
        --myip ../my-ip-geo-plasma6/screenshots/main.png

Needs Pillow, numpy, scipy, fonttools and brotli. Writes assets/cat.webp (the widget's cat as a die-cut sticker, the
"IP & Geo" lettering left out; the drawing itself is not changed), the project screenshots,
assets/og/<lang>.png (1200x630 share cards), favicon.ico and apple-touch-icon.png.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage as ndi

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import build  # noqa: E402  (text for the share cards)

ASSETS = ROOT / "assets"
FONTS = ASSETS / "fonts"
NAVY = (15, 27, 45)


# ---------- sticker ----------

def cut_out(icon: Path):
    """Cat on a flat grey background -> (rgb, alpha, cat mask); the lettering and the ground shadow are dropped."""
    im = np.asarray(Image.open(icon).convert("RGB")).astype(np.float32)
    lum, sat = im.mean(2), im.max(2) - im.min(2)
    bgish = (sat < 14) & (lum > 55)  # flat grey, its shadow and anti-aliased edges; the black outline stops it
    lab, _ = ndi.label(bgish)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    background = np.isin(lab, list(edge))
    fg = ~background
    lab2, n2 = ndi.label(fg)
    sizes = ndi.sum(fg, lab2, range(1, n2 + 1))
    cat = ndi.binary_fill_holes(lab2 == int(np.argmax(sizes)) + 1)  # the biggest blob is the cat, letters go
    band = ndi.binary_dilation(cat, iterations=2) & ~cat
    local_bg = np.maximum(ndi.maximum_filter(np.where(background, lum, 0), size=9), 1)
    a_edge = np.clip((local_bg - lum) / local_bg, 0, 1)  # edge pixels = black ink over the local background
    a_edge[a_edge < 0.06] = 0
    alpha = np.where(cat, 1.0, np.where(band, a_edge, 0.0))
    rgb = np.where(cat[..., None], im, 0.0)
    return rgb, alpha, cat


def sticker(icon: Path, border: int = 11, smooth: int = 7, ss: int = 4) -> Image.Image:
    rgb, alpha, _ = cut_out(icon)
    h, w = alpha.shape
    big = np.kron(alpha > 0.35, np.ones((ss, ss), bool))
    out = ndi.distance_transform_edt(~big) <= (border + smooth) * ss          # grow
    out = ndi.distance_transform_edt(out) > smooth * ss                       # shrink back: rounds the notches
    out = ndi.binary_fill_holes(out)
    sa = np.asarray(Image.fromarray((out * 255).astype(np.uint8)).resize((w, h), Image.BOX)).astype(np.float32) / 255
    a = alpha[..., None]
    col = rgb * a + 255.0 * (1 - a)  # cat over white paper
    rgba = np.dstack([col, np.maximum(sa, alpha) * 255]).astype(np.uint8)
    ys, xs = np.where(rgba[..., 3] > 2)
    return Image.fromarray(rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1], "RGBA")


def with_shadow(img: Image.Image, angle: float, blur: int, offset, opacity: float, pad: int) -> Image.Image:
    rot = img.rotate(angle, resample=Image.BICUBIC, expand=True)
    canvas = Image.new("RGBA", (rot.width + 2 * pad, rot.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    a = rot.getchannel("A").point(lambda v: int(v * opacity))
    sh.paste(Image.new("RGBA", rot.size, (0, 0, 0, 255)), (pad + offset[0], pad + offset[1]), a)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(sh)
    canvas.alpha_composite(rot, (pad, pad))
    return canvas


# ---------- text with per-character font fallback (the woff2 files are split by script) ----------

class Face:
    def __init__(self, weight: int, size: int):
        from fontTools.ttLib import TTFont
        self.fonts = []
        for sub in ("latin", "latin-ext", "cyrillic", "vietnamese"):
            p = FONTS / f"ibm-plex-sans-{sub}-{weight}-normal.woff2"
            cmap = set(TTFont(p).getBestCmap())
            self.fonts.append((ImageFont.truetype(str(p), size), cmap))
        cjk = "/usr/share/fonts/opentype/noto/NotoSansCJK-" + ("Bold" if weight >= 600 else "Regular") + ".ttc"
        if Path(cjk).exists():  # index 2 = Simplified Chinese in Noto Sans CJK
            self.fonts.append((ImageFont.truetype(cjk, size, index=2), None))

    def pick(self, ch):
        for f, cmap in self.fonts:
            if cmap is None or ord(ch) in cmap:
                return f
        return self.fonts[0][0]

    def runs(self, text):
        out = []
        for ch in text:
            f = self.pick(ch)
            if out and out[-1][0] is f:
                out[-1][1] += ch
            else:
                out.append([f, ch])
        return out

    def width(self, text):
        return sum(f.getlength(t) for f, t in self.runs(text))

    def draw(self, d: ImageDraw.ImageDraw, xy, text, fill):
        x, y = xy
        for f, t in self.runs(text):
            d.text((x, y), t, font=f, fill=fill, anchor="ls")
            x += f.getlength(t)


def wrap(face: Face, text: str, width: int):
    cjk = any("　" <= c <= "鿿" or "＀" <= c <= "￯" for c in text)
    tokens = list(text) if cjk else text.split(" ")
    lines, cur = [], ""
    for tok in tokens:
        cand = tok if not cur else (cur + tok if cjk else cur + " " + tok)
        if face.width(cand) <= width or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = tok
    return lines + [cur]


def og_card(lang: str, cat: Image.Image) -> Image.Image:
    s = build.T[lang]
    W, H = 1200, 630
    card = Image.new("RGBA", (W, H), NAVY + (255,))
    c = cat.resize((round(cat.width * 455 / cat.height), 455), Image.LANCZOS)
    c = with_shadow(c, 4, 14, (0, 14), 0.55, 40)
    card.alpha_composite(c, (60 - 40, 92 - 40))
    d = ImageDraw.Draw(card)
    x, maxw = 470, W - 470 - 60
    big, mid, small = Face(700, 88), Face(400, 40), Face(600, 30)
    h1 = wrap(big, s["h1"], maxw)
    sub = wrap(mid, s["og_line"], maxw)
    block = len(h1) * 98 + 26 + len(sub) * 54
    y = (H - block) // 2 + 70
    for line in h1:
        big.draw(d, (x, y), line, (255, 255, 255))
        y += 98
    y += 26 - 98 + 54
    for line in sub:
        mid.draw(d, (x, y), line, (220, 230, 243))
        y += 54
    small.draw(d, (x, H - 56), "f1devbin.github.io", (143, 208, 255))
    return card.convert("RGB")


def shot(src: Path, box, name: str, widths):
    im = Image.open(src).convert("RGB").crop(box)
    for w in widths:
        out = im if w == im.width else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        out.save(ASSETS / f"{name}-{w}.webp", "WEBP", quality=80, method=6)
    return im.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--icon", type=Path, required=True)
    ap.add_argument("--crl", type=Path, required=True)
    ap.add_argument("--tbm", type=Path, required=True)
    ap.add_argument("--myip", type=Path, required=True)
    a = ap.parse_args()
    (ASSETS / "og").mkdir(parents=True, exist_ok=True)

    cat = sticker(a.icon)
    cat.save(ASSETS / "cat.webp", "WEBP", quality=88, method=6)
    cat.resize((240, round(cat.height * 240 / cat.width)), Image.LANCZOS).save(ASSETS / "cat-240.webp", "WEBP",
                                                                             quality=88, method=6)
    sizes = {"cat": cat.size}
    sizes["crl"] = shot(a.crl, (0, 0, 1280, 600), "crl", (640, 960, 1280))
    sizes["tbm"] = shot(a.tbm, (0, 0, 1280, 640), "tbm", (640, 960, 1280))
    myip = Image.open(a.myip)
    myip.save(ASSETS / "myip.webp", "WEBP", quality=88, method=6)
    sizes["myip"] = myip.size
    (ASSETS / "sizes.json").write_text(json.dumps({k: list(v) for k, v in sizes.items()}) + "\n")
    print(sizes)

    for lang in build.LANGS:
        og_card(lang, cat).save(ASSETS / "og" / f"{lang}.png", optimize=True)

    # favicons: the head (hood and face) of the sticker, a 245 px square at the top
    head = cat.crop((95, 0, 340, 245))
    head.resize((48, 48), Image.LANCZOS).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    touch = Image.new("RGBA", (180, 180), NAVY + (255,))
    touch.alpha_composite(head.resize((150, 150), Image.LANCZOS), (15, 18))
    touch.convert("RGB").save(ROOT / "apple-touch-icon.png", optimize=True)
    print("done")


if __name__ == "__main__":
    main()
