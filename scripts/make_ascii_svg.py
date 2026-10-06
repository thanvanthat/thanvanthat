"""Convert source-prepped.png into a monochrome ASCII portrait that types
itself in row by row (SMIL, plays once, then freezes).

    python scripts/make_ascii_svg.py            # writes ascii-portrait.svg

With no source-prepped.png present, the INITIALS from config.py are drawn
instead so the README still has something to show.
"""
import os
from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from config import INITIALS

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source-prepped.png"
OUT = ROOT / "ascii-portrait.svg"

RAMP = " .`:-=+*cs#%@"   # bright (sparse) -> dark (dense)
COLS = 100
CHAR_W, LINE_H = 6.0, 10.0          # cell size in SVG units (monospace ~0.6em)
FONT_SIZE = 10
FG = "#c9d1d9"
BG = "#0d1117"
ROW_DELAY, ROW_DUR = 0.045, 0.35    # seconds


def fallback_image() -> Image.Image:
    img = Image.new("L", (600, 600), 255)
    d = ImageDraw.Draw(img)
    d.ellipse((30, 30, 570, 570), outline=0, width=40)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 260)
    except OSError:
        font = ImageFont.load_default(size=260)
    d.text((300, 300), INITIALS, fill=0, font=font, anchor="mm")
    return img


def to_rows(img: Image.Image) -> list[str]:
    # Glyphs are ~twice as tall as wide, so halve the row count.
    rows = max(1, round(COLS * img.height / img.width * CHAR_W / LINE_H))
    px = np.asarray(img.convert("L").resize((COLS, rows), Image.LANCZOS), dtype=np.float32)
    # Stretch contrast, then push near-white to pure white so the
    # background collapses to the space glyph.
    lo, hi = np.percentile(px, 2), np.percentile(px, 98)
    px = ((px - lo) / max(hi - lo, 1)).clip(0, 1)
    px[px > 0.92] = 1.0
    idx = ((1.0 - px) * (len(RAMP) - 1)).round().astype(int)
    lines = ["".join(RAMP[i] for i in row) for row in idx]
    while lines and not lines[-1].strip():
        lines.pop()
    while lines and not lines[0].strip():
        lines.pop(0)
    return lines


def build_svg(lines: list[str], static: bool) -> str:
    width, pad = COLS * CHAR_W, 12
    height = len(lines) * LINE_H
    W, H = width + 2 * pad, height + 2 * pad
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:g} {H:g}" '
        f'width="{W:g}" height="{H:g}" role="img" aria-label="ASCII portrait">',
        f'<rect width="100%" height="100%" rx="10" fill="{BG}"/>',
        f'<g transform="translate({pad} {pad})" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" '
        f'font-size="{FONT_SIZE}" fill="{FG}">',
    ]
    for i, line in enumerate(lines):
        y = i * LINE_H
        text = (f'<text x="0" y="{y + LINE_H * 0.8:g}" xml:space="preserve" '
                f'textLength="{width:g}" lengthAdjust="spacing">{escape(line)}</text>')
        if static:
            out.append(text)
            continue
        begin = f"{i * ROW_DELAY:.3f}s"
        out += [
            f'<clipPath id="r{i}"><rect x="0" y="{y:g}" width="0" height="{LINE_H:g}">'
            f'<animate attributeName="width" from="0" to="{width:g}" begin="{begin}" '
            f'dur="{ROW_DUR}s" fill="freeze"/></rect></clipPath>',
            f'<g clip-path="url(#r{i})">{text}</g>',
            # block cursor riding the wipe edge, hidden once the row is done
            f'<rect x="0" y="{y + 1:g}" width="{CHAR_W:g}" height="{LINE_H - 2:g}" opacity="0">'
            f'<set attributeName="opacity" to="0.85" begin="{begin}"/>'
            f'<animate attributeName="x" from="0" to="{width:g}" begin="{begin}" dur="{ROW_DUR}s" fill="freeze"/>'
            f'<set attributeName="opacity" to="0" begin="{i * ROW_DELAY + ROW_DUR:.3f}s"/></rect>',
        ]
    out += ["</g>", "</svg>"]
    return "\n".join(out) + "\n"


def main() -> None:
    img = Image.open(SRC) if SRC.exists() else fallback_image()
    lines = to_rows(img)
    OUT.write_text(build_svg(lines, static=os.environ.get("STATIC") == "1"))
    print(f"wrote {OUT.name} ({len(lines)} rows x {COLS} cols"
          f"{'' if SRC.exists() else ', initials fallback'})")


if __name__ == "__main__":
    main()
