#!/usr/bin/env python3
"""Compose announcement posts with the official logos (not redrawn)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/social"
LOGO_WIDE = ROOT / "assets/img/logo-wide.png"
LOGO_MARK = ROOT / "assets/img/logo-mark.png"
MASCOTTE = ROOT / "assets/img/mascotte-ink.png"

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


def compose(w: int, h: int, name: str) -> None:
    im = Image.new("RGBA", (w, h), PIETRA)
    draw = ImageDraw.Draw(im)

    # Soft cream panel
    inset = int(w * 0.07)
    panel = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(panel)
    pdraw.rounded_rectangle(
        (inset, int(h * 0.08), w - inset, h - int(h * 0.08)),
        radius=int(w * 0.02),
        fill=WHITE,
        outline=LINE,
        width=2,
    )
    im = Image.alpha_composite(im, panel)
    draw = ImageDraw.Draw(im)

    if MASCOTTE.exists():
        m = Image.open(MASCOTTE).convert("RGBA")
        mw = int(w * (0.55 if h > w else 0.62))
        ratio = mw / m.width
        m = m.resize((mw, int(m.height * ratio)), Image.Resampling.LANCZOS)
        m.putalpha(m.split()[-1].point(lambda a: int(a * 0.07)))
        im.alpha_composite(m, ((w - m.width) // 2, (h - m.height) // 2))

    wide = knock_black(Image.open(LOGO_WIDE))
    lw = int(w * 0.68)
    ratio = lw / wide.width
    wide = wide.resize((lw, int(wide.height * ratio)), Image.Resampling.LANCZOS)
    wide_y = int(h * 0.18) if h > w * 1.2 else int(h * 0.16)
    im.alpha_composite(wide, ((w - wide.width) // 2, wide_y))

    y = wide_y + wide.height + int(h * 0.06)
    rule_w = int(w * 0.12)
    draw.rectangle(
        ((w - rule_w) // 2, y, (w + rule_w) // 2, y + 2),
        fill=BORDEAUX,
    )

    kicker = font(GEORGIA, max(22, w // 32))
    title = font(DIDOT, max(48, w // 12), index=0)
    italic = font(GEORGIA_I, max(26, w // 28))
    small = font(GEORGIA, max(18, w // 40))

    y += int(h * 0.045)
    th = centered(draw, "PRESTO ONLINE", y, kicker, BORDEAUX, w)
    y += th + int(h * 0.028)
    th = centered(draw, "Il nuovo sito", y, title, INK, w)
    y += th + int(h * 0.012)
    th = centered(draw, "è in arrivo.", y, title, INK, w)
    y += th + int(h * 0.04)
    th = centered(draw, "Stay tuned.", y, italic, SOFT, w)
    y += th + int(h * 0.06)
    centered(draw, "Grottaglie  ·  Puglia", y, small, SOFT, w)

    mark = knock_black(Image.open(LOGO_MARK))
    mw = int(w * 0.14)
    ratio = mw / mark.width
    mark = mark.resize((mw, int(mark.height * ratio)), Image.Resampling.LANCZOS)
    mark_y = h - int(h * 0.12) - mark.height
    im.alpha_composite(mark, ((w - mark.width) // 2, mark_y))

    dest = OUT / name
    OUT.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").save(dest, "JPEG", quality=92, optimize=True)
    print("wrote", dest.relative_to(ROOT), im.size)


def rounded(im: Image.Image, radius: int) -> Image.Image:
    im = im.convert("RGBA")
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.width, im.height), radius=radius, fill=255)
    im.putalpha(mask)
    return im


def browser_preview(shot: Image.Image, width: int, crop_ratio: float = 0.58) -> Image.Image:
    """Mini browser chrome around a cropped homepage screenshot."""
    shot = shot.convert("RGB")
    # Keep the hero: nav + first screen
    crop_h = min(shot.height, int(shot.width * crop_ratio))
    shot = shot.crop((0, 0, shot.width, crop_h))
    scale = width / shot.width
    shot = shot.resize((width, max(1, int(shot.height * scale))), Image.Resampling.LANCZOS)

    chrome_h = max(28, width // 28)
    pad = 3
    frame_w = width + pad * 2
    frame_h = shot.height + chrome_h + pad
    frame = Image.new("RGBA", (frame_w, frame_h), (255, 255, 255, 255))
    d = ImageDraw.Draw(frame)
    d.rounded_rectangle((0, 0, frame_w - 1, frame_h - 1), radius=18, outline=LINE, width=2, fill=WHITE)
    d.rectangle((1, chrome_h, frame_w - 2, chrome_h + 1), fill=LINE)
    for i, col in enumerate([(200, 120, 130, 255), (196, 176, 120, 255), (140, 160, 120, 255)]):
        cx = 18 + i * 16
        d.ellipse((cx, chrome_h // 2 - 5, cx + 10, chrome_h // 2 + 5), fill=col)

    inner = rounded(shot, 4)
    frame.alpha_composite(inner, (pad, chrome_h))
    return rounded(frame, 18)


def canvas(w: int, h: int) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    im = Image.new("RGBA", (w, h), PIETRA)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    inset = int(w * 0.07)
    d.rounded_rectangle(
        (inset, int(h * 0.06), w - inset, h - int(h * 0.06)),
        radius=int(w * 0.02),
        fill=WHITE,
        outline=LINE,
        width=2,
    )
    im = Image.alpha_composite(im, overlay)
    if MASCOTTE.exists():
        m = Image.open(MASCOTTE).convert("RGBA")
        mw = int(w * 0.5)
        m = m.resize((mw, int(m.height * mw / m.width)), Image.Resampling.LANCZOS)
        m.putalpha(m.split()[-1].point(lambda a: int(a * 0.06)))
        im.alpha_composite(m, ((w - m.width) // 2, (h - m.height) // 2))
    return im, ImageDraw.Draw(im)


def place_logo(im: Image.Image, w: int, y: int, scale: float = 0.58) -> int:
    wide = knock_black(Image.open(LOGO_WIDE))
    lw = int(w * scale)
    wide = wide.resize((lw, int(wide.height * lw / wide.width)), Image.Resampling.LANCZOS)
    im.alpha_composite(wide, ((w - wide.width) // 2, y))
    return y + wide.height


def compose_online(w: int, h: int, name: str, shot: Image.Image, preview_frac: float = 0.76, crop_ratio: float = 0.52) -> None:
    im, draw = canvas(w, h)
    y = int(h * 0.10)
    y = place_logo(im, w, y, 0.52)
    y += int(h * 0.035)
    rule_w = int(w * 0.10)
    draw.rectangle(((w - rule_w) // 2, y, (w + rule_w) // 2, y + 2), fill=BORDEAUX)
    y += int(h * 0.03)

    kicker = font(GEORGIA, max(20, w // 34))
    title = font(DIDOT, max(42, w // 14), index=0)
    italic = font(GEORGIA_I, max(22, w // 32))
    small = font(GEORGIA, max(16, w // 42))

    y += centered(draw, "È ONLINE", y, kicker, BORDEAUX, w)
    y += int(h * 0.018)
    y += centered(draw, "Il nuovo sito", y, title, INK, w)
    y += int(h * 0.008)
    y += centered(draw, "è pronto.", y, title, INK, w)
    y += int(h * 0.028)

    preview = browser_preview(shot, int(w * preview_frac), crop_ratio)
    im.alpha_composite(preview, ((w - preview.width) // 2, y))
    y += preview.height + int(h * 0.03)
    centered(draw, "Grottaglie  ·  Puglia", y, small, SOFT, w)

    dest = OUT / name
    OUT.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").save(dest, "JPEG", quality=92, optimize=True)
    print("wrote", dest.relative_to(ROOT), im.size)


def compose_story_link(w: int, h: int, name: str, shot: Image.Image) -> None:
    """Story with a blank white slot for the Instagram link sticker."""
    im, draw = canvas(w, h)
    y = int(h * 0.12)
    y = place_logo(im, w, y, 0.56)
    y += int(h * 0.04)
    rule_w = int(w * 0.10)
    draw.rectangle(((w - rule_w) // 2, y, (w + rule_w) // 2, y + 2), fill=BORDEAUX)
    y += int(h * 0.035)

    kicker = font(GEORGIA, max(22, w // 30))
    title = font(DIDOT, max(52, w // 11), index=0)
    small = font(GEORGIA, max(18, w // 38))

    y += centered(draw, "È ONLINE", y, kicker, BORDEAUX, w)
    y += int(h * 0.02)
    y += centered(draw, "Il nuovo sito", y, title, INK, w)
    y += int(h * 0.01)
    y += centered(draw, "è pronto.", y, title, INK, w)
    y += int(h * 0.035)

    preview = browser_preview(shot, int(w * 0.70))
    im.alpha_composite(preview, ((w - preview.width) // 2, y))
    y += preview.height + int(h * 0.05)

    # Empty white slot — leave this free for the Instagram link sticker
    slot_w = int(w * 0.72)
    slot_h = int(h * 0.09)
    slot_x = (w - slot_w) // 2
    draw.rounded_rectangle(
        (slot_x, y, slot_x + slot_w, y + slot_h),
        radius=slot_h // 2,
        fill=(255, 255, 255, 255),
        outline=LINE,
        width=1,
    )

    footer_y = h - int(h * 0.10)
    centered(draw, "Grottaglie  ·  Puglia", footer_y, small, SOFT, w)

    dest = OUT / name
    OUT.mkdir(parents=True, exist_ok=True)
    im.convert("RGB").save(dest, "JPEG", quality=92, optimize=True)
    print("wrote", dest.relative_to(ROOT), im.size)


if __name__ == "__main__":
    compose(1080, 1080, "annuncio-feed.jpg")
    compose(1080, 1350, "annuncio-facebook.jpg")
    compose(1080, 1920, "annuncio-story.jpg")

    shot_path = OUT / "_home-shot.png"
    if shot_path.exists():
        shot = Image.open(shot_path)
        compose_online(1080, 1080, "online-feed.jpg", shot, 0.74, 0.48)
        compose_online(1080, 1350, "online-facebook.jpg", shot, 0.78, 0.52)
        compose_story_link(1080, 1920, "online-story.jpg", shot)
