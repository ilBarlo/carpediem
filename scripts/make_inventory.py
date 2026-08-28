#!/usr/bin/env python3
"""One catalog inventory image from the current studio photos."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
STUDIO = ROOT / "assets/img/foto/web/studio"
OUT = ROOT / "assets/social"
LOGO_WIDE = ROOT / "assets/img/logo-wide.png"
MASCOTTE = ROOT / "assets/img/mascotte-ink.png"

PIETRA = (245, 243, 238, 255)
WHITE = (250, 249, 246, 255)
BORDEAUX = (138, 49, 73, 255)
INK = (38, 34, 32, 255)
SOFT = (99, 91, 84, 255)
LINE = (227, 224, 216, 255)

FONT_DIR = Path("/System/Library/Fonts/Supplemental")

# Same order as catalogo.html: stem, name on the inventory
ITEMS = [
    ("pumi-dipinti", "Pumi dipinti a mano"),
    ("pumi-bianchi", "Pumi graffiti bianchi"),
    ("lampada-pumo", "Lampada Pumo"),
    ("lampada-volto", "Lampada Ius Primae Noctis"),
    ("testa-dipinta", "Pupe dello Ius Primae Noctis"),
    ("cavalieri", "Cavalieri Ius Primae Noctis"),
    ("centrotavola-melagrane", "Centrotavola Melograno"),
    ("piatto-ulivo", "Piatto Ulivo"),
    ("piatto-fichi-dindia", "Piatto Fichi d'India"),
    ("oliere-mediterranee", "Oliere Mediterranee"),
    ("gufi", "Gufi"),
    ("bonsai-ulivo", "Vasi per piante"),
    ("acquasantiera", "Acquasantiera"),
    ("acquasantiera-angeli", "Acquasantiera S. Michele"),
    ("presepe", "Presepe"),
    ("crocifisso", "Crocifisso"),
    ("piatto-cristo", "Ovale Cristo"),
    ("statuina-santo", "Statuina Sacra"),
    ("alberi-natale", "Alberi di Natale"),
    ("palline-natale", "Palline di Natale"),
    ("presepi-piccoli", "Presepi da Tavolo"),
    ("presepe-pumo", "Presepe Pumo"),
    ("uovo-colomba", "Uovo Portagioie"),
    ("uova-rose", "Uova pasquali con rose e fiori"),
    ("vassoi-mare", "Vassoi tema marino"),
    ("pesci-parete", "Pesci a Parete"),
    ("ricci-mare", "Ricci di Mare"),
    ("ovetto-ancora", "Portacandela con ancora"),
    ("polpo", "Polpo"),
    ("bomboniere-traforate", "Portacandela traforato"),
]


def font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size=size, index=index)
    except OSError:
        return ImageFont.load_default()


def knock_black(im: Image.Image, thresh: int = 28) -> Image.Image:
    im = im.convert("RGBA")
    px = list(im.getdata())
    out = []
    for r, g, b, a in px:
        if a < 12:
            out.append((0, 0, 0, 0))
        elif r < thresh and g < thresh and b < thresh:
            out.append((0, 0, 0, 0))
        else:
            out.append((r, g, b, a))
    im.putdata(out)
    bbox = im.getbbox()
    return im.crop(bbox) if bbox else im


def cover_crop(im: Image.Image, tw: int, th: int) -> Image.Image:
    im = im.convert("RGB")
    scale = max(tw / im.width, th / im.height)
    nw, nh = max(1, int(im.width * scale)), max(1, int(im.height * scale))
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = max(0, (nw - tw) // 2)
    top = max(0, int((nh - th) * 0.42))
    if top + th > nh:
        top = max(0, nh - th)
    return im.crop((left, top, left + tw, top + th))


def round_thumb(im: Image.Image, radius: int) -> Image.Image:
    im = im.convert("RGBA")
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.width, im.height), radius=radius, fill=255)
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    out.paste(im, mask=mask)
    return out


def wrap_lines(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        tw = draw.textbbox((0, 0), trial, font=fnt)[2]
        if tw <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines[:2]


def compose(w: int, h: int, cols: int, name: str) -> None:
    n = len(ITEMS)
    rows = (n + cols - 1) // cols
    canvas = Image.new("RGBA", (w, h), PIETRA)
    draw = ImageDraw.Draw(canvas)

    header_h = int(h * 0.155)
    footer_h = int(h * 0.048)
    side = int(w * 0.04)
    gap = max(10, int(w * 0.011))
    caption_h = int(h * 0.028)

    wide = knock_black(Image.open(LOGO_WIDE))
    lw = int(w * 0.40)
    wide = wide.resize((lw, max(1, int(wide.height * lw / wide.width))), Image.Resampling.LANCZOS)
    logo_y = int(h * 0.022)
    canvas.alpha_composite(wide, ((w - wide.width) // 2, logo_y))

    title = font(str(FONT_DIR / "Didot.ttc"), int(w * 0.036), 0)
    sub = font(str(FONT_DIR / "Georgia.ttf"), int(w * 0.016))
    cap_fnt = font(str(FONT_DIR / "Georgia.ttf"), max(13, int(w * 0.013)))
    title_y = logo_y + wide.height + int(h * 0.01)
    tb = draw.textbbox((0, 0), "Il Catalogo", font=title)
    draw.text(((w - (tb[2] - tb[0])) / 2, title_y), "Il Catalogo", font=title, fill=INK)
    sb = draw.textbbox((0, 0), "Tutto quello che trovi in bottega, ora.", font=sub)
    draw.text(
        ((w - (sb[2] - sb[0])) / 2, title_y + (tb[3] - tb[1]) + int(h * 0.006)),
        "Tutto quello che trovi in bottega, ora.",
        font=sub,
        fill=SOFT,
    )

    grid_top = header_h
    grid_bot = h - footer_h
    cell_w = (w - 2 * side - (cols - 1) * gap) // cols
    cell_h = (grid_bot - grid_top - (rows - 1) * gap) // rows
    photo_h = max(40, cell_h - caption_h)
    radius = max(8, int(min(cell_w, photo_h) * 0.08))

    for i, (stem, label) in enumerate(ITEMS):
        r, c = divmod(i, cols)
        x = side + c * (cell_w + gap)
        y = grid_top + r * (cell_h + gap)
        src = STUDIO / f"{stem}.jpg"
        if not src.exists():
            print("missing", src)
            continue
        thumb = cover_crop(Image.open(src), cell_w, photo_h)
        thumb = round_thumb(thumb, radius)
        canvas.alpha_composite(thumb, (x, y))
        lines = wrap_lines(draw, label, cap_fnt, cell_w - 4)
        ly = y + photo_h + max(2, int(h * 0.003))
        for line in lines:
            bb = draw.textbbox((0, 0), line, font=cap_fnt)
            draw.text((x + (cell_w - (bb[2] - bb[0])) / 2, ly), line, font=cap_fnt, fill=INK)
            ly += bb[3] - bb[1] + 1

    leftover = rows * cols - n
    if leftover and MASCOTTE.exists():
        r, c = divmod(n, cols)
        x = side + c * (cell_w + gap)
        y = grid_top + r * (cell_h + gap)
        slot = Image.new("RGBA", (cell_w, photo_h), WHITE)
        slot_mask = Image.new("L", (cell_w, photo_h), 0)
        ImageDraw.Draw(slot_mask).rounded_rectangle(
            (0, 0, cell_w, photo_h), radius=radius, fill=255
        )
        slot.putalpha(slot_mask)
        m = Image.open(MASCOTTE).convert("RGBA")
        mw = int(min(cell_w, photo_h) * 0.55)
        m = m.resize((mw, int(m.height * mw / m.width)), Image.Resampling.LANCZOS)
        m.putalpha(m.split()[-1].point(lambda a: int(a * 0.18)))
        slot.alpha_composite(m, ((cell_w - m.width) // 2, (photo_h - m.height) // 2))
        canvas.alpha_composite(slot, (x, y))

    foot = font(str(FONT_DIR / "Georgia.ttf"), int(w * 0.015))
    ft = "Grottaglie · Puglia"
    fb = draw.textbbox((0, 0), ft, font=foot)
    draw.text(((w - (fb[2] - fb[0])) / 2, h - footer_h + int(h * 0.01)), ft, font=foot, fill=SOFT)

    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / name
    canvas.convert("RGB").save(dest, "JPEG", quality=88, optimize=True, progressive=True)
    print(f"wrote {dest.relative_to(ROOT)}  {canvas.size}")


def main() -> None:
    compose(2160, 2700, 6, "inventario-catalogo.jpg")
    compose(1080, 1920, 5, "inventario-catalogo-story.jpg")


if __name__ == "__main__":
    main()
