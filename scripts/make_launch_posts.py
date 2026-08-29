#!/usr/bin/env python3
"""Launch posts: wide Facebook + Instagram, official logos + mascotte."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/social"
LOGO_WIDE = ROOT / "assets/img/logo-wide.png"
LOGO_MARK = ROOT / "assets/img/logo-mark.png"
MASCOTTE = ROOT / "assets/img/mascotte-ink.png"
ILBARLO = ROOT / "assets/img/ilbarlo.png"
ILBARLO_SRC = Path(
    "/Users/francesco.barletta/.cursor/projects/"
    "Users-francesco-barletta-Desktop-Personal-Websites/assets/"
    "image-62692eed-56dd-4346-a4e5-11fbadb6587a.png"
)

PIETRA = (245, 243, 238, 255)
WHITE = (250, 249, 246, 255)
BORDEAUX = (138, 49, 73, 255)
INK = (38, 34, 32, 255)
SOFT = (99, 91, 84, 255)
LINE = (227, 224, 216, 255)

FONT_DIR = Path("/System/Library/Fonts/Supplemental")
DIDOT = str(FONT_DIR / "Didot.ttc")
GEORGIA = str(FONT_DIR / "Georgia.ttf")
GEORGIA_I = str(FONT_DIR / "Georgia Italic.ttf")


def knock_black(im: Image.Image, thresh: int = 28) -> Image.Image:
    im = im.convert("RGBA")
    px = list(im.getdata())
    out = []
    for r, g, b, a in px:
        if r < thresh and g < thresh and b < thresh:
            out.append((0, 0, 0, 0))
        else:
            out.append((r, g, b, a))
    im.putdata(out)
    return im


def knock_white(im: Image.Image, thresh: int = 238) -> Image.Image:
    im = im.convert("RGBA")
    px = list(im.getdata())
    out = []
    for r, g, b, a in px:
        if r >= thresh and g >= thresh and b >= thresh:
            out.append((255, 255, 255, 0))
        else:
            out.append((r, g, b, a))
    im.putdata(out)
    return im


def prepare_ilbarlo() -> None:
    src = ILBARLO_SRC if ILBARLO_SRC.exists() else ILBARLO
    im = Image.open(src).convert("RGBA")
    for y in range(min(48, im.height)):
        for x in range(min(48, im.width)):
            im.putpixel((x, y), (255, 255, 255, 0))
    im = knock_white(im)
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    ILBARLO.parent.mkdir(parents=True, exist_ok=True)
    im.save(ILBARLO)
    print("wrote", ILBARLO.relative_to(ROOT), im.size)


def font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size=size, index=index)
    except OSError:
        return ImageFont.load_default()


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont) -> tuple[int, int]:
    b = draw.textbbox((0, 0), text, font=fnt)
    return b[2] - b[0], b[3] - b[1]


def centered(draw: ImageDraw.ImageDraw, text: str, y: int, fnt: ImageFont.ImageFont, fill, w: int) -> int:
    tw, th = text_size(draw, text, fnt)
    draw.text(((w - tw) / 2, y), text, font=fnt, fill=fill)
    return th


def place_mascotte(im: Image.Image, w: int, h: int, scale: float, opacity: float) -> None:
    m = Image.open(MASCOTTE).convert("RGBA")
    mw = int(min(w, h) * scale)
    m = m.resize((mw, int(m.height * mw / m.width)), Image.Resampling.LANCZOS)
    m.putalpha(m.split()[-1].point(lambda a: int(a * opacity)))
    im.alpha_composite(m, ((w - m.width) // 2, (h - m.height) // 2 + int(h * 0.01)))


def place_wide(im: Image.Image, w: int, y: int, scale: float) -> int:
    wide = knock_black(Image.open(LOGO_WIDE))
    lw = int(w * scale)
    wide = wide.resize((lw, int(wide.height * lw / wide.width)), Image.Resampling.LANCZOS)
    im.alpha_composite(wide, ((w - wide.width) // 2, y))
    return y + wide.height


def fit_box(im: Image.Image, box: int) -> Image.Image:
    r = min(box / im.width, box / im.height)
    nw, nh = max(1, int(im.width * r)), max(1, int(im.height * r))
    resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (box, box), (0, 0, 0, 0))
    canvas.alpha_composite(resized, ((box - nw) // 2, (box - nh) // 2))
    return canvas


def credit_row(im: Image.Image, draw: ImageDraw.ImageDraw, w: int, y: int, box: int) -> None:
    label = font(GEORGIA, max(14, box // 7))
    th = centered(draw, "Realizzato da", y, label, SOFT, w)
    y += th + int(box * 0.12)

    cd = fit_box(knock_black(Image.open(LOGO_MARK)), box)
    ib = fit_box(Image.open(ILBARLO).convert("RGBA"), box)
    gap = max(36, box // 3)
    total = box + gap + box
    x = (w - total) // 2
    im.alpha_composite(cd, (x, y))
    mx = x + box + gap // 2
    draw.line((mx, y + int(box * 0.18), mx, y + box - int(box * 0.18)), fill=LINE, width=2)
    im.alpha_composite(ib, (x + box + gap, y))


def base(w: int, h: int, inset_x: float = 0.055, inset_y: float = 0.07) -> Image.Image:
    im = Image.new("RGBA", (w, h), PIETRA)
    wash = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wash)
    wd.ellipse(
        (-int(w * 0.15), -int(h * 0.45), int(w * 1.15), int(h * 0.55)),
        fill=(138, 49, 73, 16),
    )
    im = Image.alpha_composite(im, wash)
    panel = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(panel).rounded_rectangle(
        (int(w * inset_x), int(h * inset_y), w - int(w * inset_x), h - int(h * inset_y)),
        radius=int(min(w, h) * 0.018),
        fill=WHITE,
        outline=LINE,
        width=2,
    )
    return Image.alpha_composite(im, panel)


def save(im: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / name
    im.convert("RGB").save(dest, "JPEG", quality=94, optimize=True)
    print("wrote", dest.relative_to(ROOT), im.size)


def facebook_wide() -> None:
    w, h = 1920, 1080
    im = base(w, h, 0.045, 0.075)
    place_mascotte(im, w, h, 0.98, 0.09)
    draw = ImageDraw.Draw(im)

    y = int(h * 0.145)
    y = place_wide(im, w, y, 0.38)
    y += int(h * 0.042)
    rule_w = int(w * 0.065)
    draw.rectangle(((w - rule_w) // 2, y, (w + rule_w) // 2, y + 3), fill=BORDEAUX)
    y += int(h * 0.038)

    kicker = font(GEORGIA, 26)
    title = font(DIDOT, 82, index=0)
    italic = font(GEORGIA_I, 28)
    small = font(GEORGIA, 20)

    y += centered(draw, "OGGI", y, kicker, BORDEAUX, w)
    y += 18
    y += centered(draw, "Siamo online.", y, title, INK, w)
    y += 58
    y += centered(draw, "Scopri adesso il nostro sito.", y, italic, SOFT, w)
    y += 28
    centered(draw, "Grottaglie  ·  Puglia", y, small, SOFT, w)

    credit_row(im, draw, w, h - int(h * 0.22), 88)
    save(im, "lancio-facebook.jpg")


def instagram_post() -> None:
    w, h = 1080, 1350
    im = base(w, h, 0.07, 0.06)
    place_mascotte(im, w, h, 0.82, 0.085)
    draw = ImageDraw.Draw(im)

    y = int(h * 0.125)
    y = place_wide(im, w, y, 0.56)
    y += int(h * 0.042)
    rule_w = int(w * 0.11)
    draw.rectangle(((w - rule_w) // 2, y, (w + rule_w) // 2, y + 3), fill=BORDEAUX)
    y += int(h * 0.038)

    kicker = font(GEORGIA, 24)
    title = font(DIDOT, 68, index=0)
    italic = font(GEORGIA_I, 26)
    small = font(GEORGIA, 18)

    y += centered(draw, "OGGI", y, kicker, BORDEAUX, w)
    y += 18
    y += centered(draw, "Siamo online.", y, title, INK, w)
    y += 56
    y += centered(draw, "Scopri adesso il nostro sito.", y, italic, SOFT, w)
    y += 32
    centered(draw, "Grottaglie  ·  Puglia", y, small, SOFT, w)

    credit_row(im, draw, w, h - int(h * 0.20), 96)
    save(im, "lancio-instagram.jpg")


def instagram_story() -> None:
    w, h = 1080, 1920
    im = base(w, h, 0.075, 0.055)
    place_mascotte(im, w, h, 0.78, 0.08)
    draw = ImageDraw.Draw(im)

    y = int(h * 0.13)
    y = place_wide(im, w, y, 0.58)
    y += int(h * 0.038)
    rule_w = int(w * 0.12)
    draw.rectangle(((w - rule_w) // 2, y, (w + rule_w) // 2, y + 3), fill=BORDEAUX)
    y += int(h * 0.036)

    kicker = font(GEORGIA, 24)
    title = font(DIDOT, 70, index=0)
    italic = font(GEORGIA_I, 28)
    small = font(GEORGIA, 18)

    y += centered(draw, "OGGI", y, kicker, BORDEAUX, w)
    y += 20
    y += centered(draw, "Siamo online.", y, title, INK, w)
    y += 58
    y += centered(draw, "Scopri adesso il nostro sito.", y, italic, SOFT, w)
    y += 48

    slot_w = int(w * 0.70)
    slot_h = int(h * 0.085)
    slot_x = (w - slot_w) // 2
    draw.rounded_rectangle(
        (slot_x, y, slot_x + slot_w, y + slot_h),
        radius=slot_h // 2,
        fill=(255, 255, 255, 255),
        outline=LINE,
        width=2,
    )
    y += slot_h + 36
    centered(draw, "Grottaglie  ·  Puglia", y, small, SOFT, w)

    credit_row(im, draw, w, h - int(h * 0.175), 88)
    save(im, "lancio-story.jpg")


if __name__ == "__main__":
    prepare_ilbarlo()
    facebook_wide()
    instagram_post()
    instagram_story()
