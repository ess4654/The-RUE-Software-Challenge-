#!/usr/bin/env python3
"""Re-frame the Conclusion plate so its drawn border sits in exactly the same
position on the page as every other full-page plate, with an even cream
border all round.

The original art has a pure-white surround, a torn-paper deckle strip running
down the extreme left and right of the sheet, and a drawn frame that is both
too small and off-centre. This script:

  1. finds the drawn frame in the master art (columns/rows where most pixels
     are dark),
  2. crops the framed artwork (plus a hair of bleed) away from the white
     surround and the deckle strips,
  3. scales it so the frame lands on the reference plate's frame box, and
  4. lays it on a cream paper canvas sampled from an existing plate margin.

Writes the 300 dpi master, the print interior image and the screen image.
"""
import numpy as np
from PIL import Image

SRC = "img_master/pl_conclusion.png"
REF = "img_print/pl_ch02.jpg"          # geometry + cream reference
CREAM_DONOR = "img_print/pl_ch01.jpg"  # paper texture donor

PAGE = (2550, 3300)   # 8.5 x 11 in at 300 dpi
PAD = 8               # bleed kept outside the frame line, in source pixels


def frame_box(arr, thresh=150, frac=0.7):
    """Return (x0, x1, y0, y1) of the drawn frame: the rows/columns that are
    mostly dark. Ignores stray marks, which never span the sheet."""
    dark = arr.astype(float).mean(2) < thresh
    rows = np.where(dark.mean(1) > frac)[0]
    cols = np.where(dark.mean(0) > frac)[0]
    return int(cols.min()), int(cols.max()), int(rows.min()), int(rows.max())


def cream_canvas(size, donor_path):
    """A page-sized cream canvas carrying the same paper grain as the other
    plates, built by tiling a strip of clean margin from a donor plate."""
    donor = np.array(Image.open(donor_path).convert("RGB"))
    strip = donor[:, 12:72]                     # clean left margin, no artwork
    reps = int(np.ceil(size[0] / strip.shape[1]))
    tiled = np.concatenate([strip, strip[:, ::-1]] * reps, axis=1)  # mirror-tile
    tiled = tiled[: size[1], : size[0]]
    if tiled.shape[0] < size[1]:                # donor shorter than the page
        pad = size[1] - tiled.shape[0]
        tiled = np.concatenate([tiled, tiled[-pad:][::-1]], axis=0)
    return Image.fromarray(tiled)


def main():
    src = Image.open(SRC).convert("RGB")
    sx0, sx1, sy0, sy1 = frame_box(np.array(src))
    tx0, tx1, ty0, ty1 = frame_box(np.array(Image.open(REF).convert("RGB")))
    print(f"source frame  x {sx0}-{sx1}  y {sy0}-{sy1}")
    print(f"target frame  x {tx0}-{tx1}  y {ty0}-{ty1}")

    # scale the source frame onto the reference frame box
    kx = (tx1 - tx0 + 1) / (sx1 - sx0 + 1)
    ky = (ty1 - ty0 + 1) / (sy1 - sy0 + 1)
    print(f"scale  x {kx:.4f}  y {ky:.4f}")

    crop = src.crop((sx0 - PAD, sy0 - PAD, sx1 + 1 + PAD, sy1 + 1 + PAD))
    new_w = round(crop.width * kx)
    new_h = round(crop.height * ky)
    art = crop.resize((new_w, new_h), Image.LANCZOS)

    page = cream_canvas(PAGE, CREAM_DONOR)
    page.paste(art, (round(tx0 - PAD * kx), round(ty0 - PAD * ky)))

    page.save("img_master/pl_conclusion.jpg", quality=96, subsampling=0)
    page.save("img_print/pl_conclusion.jpg", quality=92, subsampling=0)
    page.resize((PAGE[0] // 2, PAGE[1] // 2), Image.LANCZOS).save(
        "img_screen/pl_conclusion.jpg", quality=88)

    check = frame_box(np.array(Image.open("img_print/pl_conclusion.jpg").convert("RGB")))
    print("result frame ", check)
    print("margins L,R,T,B",
          check[0], PAGE[0] - 1 - check[1], check[2], PAGE[1] - 1 - check[3])


if __name__ == "__main__":
    main()
