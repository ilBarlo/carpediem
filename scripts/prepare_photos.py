#!/usr/bin/env python3
"""Convert originals, crop, enhance, bake in a copyright watermark."""
from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets/img/foto"
OUT = ROOT / "assets/img/foto/web"
TMP = Path("/tmp/cd-work")
LOGO = ROOT / "assets/img/logo-wide.png"

# Rotation is extra after EXIF transpose. 0 unless a shot is still sideways.
# PIL rotate: 90 = CCW, 270 = CW
JOBS = [
    # src, out_stem, rotate, crop (w/h), max_side
    ("IMG_7558.HEIC", "pumi-dipinti", 0, 0.92, 1400),
    ("IMG_7560.HEIC", "pumi-bianchi", 0, 1.05, 1400),
    ("IMG_7540.HEIC", "piatto-ulivo", 0, 0.92, 1400),
    ("IMG_7579.HEIC", "centrotavola-melagrane", 0, 0.88, 1400),
    ("IMG_7580.HEIC", "piatto-fichi-dindia", 0, 0.92, 1400),
    ("IMG_7567.HEIC", "oliere-mediterranee", 0, 1.05, 1400),
    ("IMG_7562.HEIC", "gufi", 0, 1.05, 1400),
    ("IMG_9962.HEIC", "lampada-pumo", 0, 0.82, 1400),
    ("IMG_7578.HEIC", "lampada-volto", 0, 0.78, 1400),
    ("IMG_7549.HEIC", "acquasantiera", 0, 0.78, 1400),
    ("IMG_7551.HEIC", "piatto-cristo", 0, 0.86, 1400),
    ("IMG_7552.HEIC", "crocifisso", 0, 0.72, 1400),
    ("IMG_7553.HEIC", "statuina-santo", 0, 0.68, 1400),
    ("IMG_7548.HEIC", "acquasantiera-angeli", 0, 0.82, 1400),
    ("IMG_7572.HEIC", "presepe", 0, 0.78, 1400),
    ("IMG_7585.HEIC", "artigiano", 0, 0.82, 1400),
    ("IMG_7545.HEIC", "scaffale-bottega", 0, 1.15, 1400),
]

# Portrait of Leonardo: no watermark (Storia + home teaser).
NO_WATERMARK = {"artigiano"}


def to_jpeg(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "95", str(src), "--out", str(dest)],
        check=True,
        capture_output=True,
    )


def crop_center(im: Image.Image, ratio: float) -> Image.Image:
    w, h = im.size
    target = w / h
    if abs(target - ratio) < 0.02:
        return im
    if target > ratio:
        nw = int(h * ratio)
        left = (w - nw) // 2
        return im.crop((left, 0, left + nw, h))
    nh = int(w / ratio)
    top = (h - nh) // 2
    return im.crop((0, top, w, top + nh))


def enhance(im: Image.Image) -> Image.Image:
    im = ImageOps.exif_transpose(im) or im
    im = ImageEnhance.Contrast(im).enhance(1.08)
    im = ImageEnhance.Color(im).enhance(1.06)
    im = ImageEnhance.Sharpness(im).enhance(1.12)
    im = ImageEnhance.Brightness(im).enhance(1.03)
    return im.convert("RGB")


def logo_mark(width: int) -> Image.Image:
    """Horizontal site logo, black background knocked out, tiled as watermark."""
    logo = Image.open(LOGO).convert("RGBA")
    pixels = list(logo.getdata())
    cleaned = []
    for r, g, b, a in pixels:
        if r + g + b < 80:
            cleaned.append((0, 0, 0, 0))
        else:
            cleaned.append((r, g, b, min(a, 92)))
    logo.putdata(cleaned)
    lw = max(220, int(width * 0.42))
    ratio = lw / logo.width
    logo = logo.resize((lw, max(1, int(logo.height * ratio))), Image.Resampling.LANCZOS)
    return logo.rotate(28, expand=True, resample=Image.Resampling.BICUBIC)


def watermark(im: Image.Image) -> Image.Image:
    if not LOGO.exists():
        return im.convert("RGB")
    base = im.convert("RGBA")
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    tile = logo_mark(base.width)
    tw, th = tile.size
    step_x, step_y = int(tw * 0.78), int(th * 0.88)
    row = 0
    for y in range(-th, base.height + th, step_y):
        x0 = -(tw // 3) if row % 2 else -tw // 8
        for x in range(x0, base.width + tw, step_x):
            overlay.alpha_composite(tile, (x, y))
        row += 1
    return Image.alpha_composite(base, overlay).convert("RGB")


def resize_max(im: Image.Image, max_side: int) -> Image.Image:
    w, h = im.size
    m = max(w, h)
    if m <= max_side:
        return im
    scale = max_side / m
    return im.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)


def main() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    for src_name, stem, rot, ratio, max_side in JOBS:
        src = SRC / src_name
        if not src.exists():
            print("missing", src)
            continue
        work = TMP / f"{stem}.jpg"
        to_jpeg(src, work)
        im = Image.open(work)
        im = enhance(im)
        if rot:
            im = im.rotate(rot, expand=True)
        im = crop_center(im, ratio)
        im = resize_max(im, max_side)
        if stem not in NO_WATERMARK:
            im = watermark(im)
        dest = OUT / f"{stem}.jpg"
        im.save(dest, "JPEG", quality=84, optimize=True, progressive=True)
        print(f"wrote {dest.relative_to(ROOT)}  {im.size[0]}x{im.size[1]}")


if __name__ == "__main__":
    main()
