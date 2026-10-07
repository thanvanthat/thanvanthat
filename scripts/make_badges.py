"""Draw the tech-stack panel and the connect badges as committed SVGs
(no shields.io). Icons are Simple Icons paths stored in scripts/icons.json.

    python scripts/make_badges.py   # writes stack.svg and badges/<name>.svg
"""
import json
import os
from pathlib import Path
from xml.sax.saxutils import escape

from config import SOCIALS, STACK

ROOT = Path(__file__).resolve().parent.parent
ICONS = json.loads((Path(__file__).parent / "icons.json").read_text())

FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
BG, BORDER, DIM = "#0d1117", "#30363d", "#8b949e"
PILL_H, FONT_SIZE, ICON = 28, 13, 15
CW = FONT_SIZE * 0.6
PAD, GAP = 10, 8


def luminance(hex_: str) -> float:
    r, g, b = (int(hex_[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def pill(x: float, y: float, label: str, slug: str) -> tuple[str, float]:
    """One badge at (x, y); returns its SVG and width. Near-black brands get a
    dark-grey pill with a border so they don't vanish into the background."""
    icon = ICONS[slug]
    fill = "#" + icon["hex"]
    dark = luminance(icon["hex"]) < 0.12
    if dark:
        fill = "#21262d"
    fg = "#0d1117" if luminance(fill[1:]) > 0.55 else "#ffffff"
    w = PAD + ICON + 7 + len(label) * CW + PAD
    stroke = f' stroke="{BORDER}"' if dark else ""
    s = ICON / 24
    svg = (f'<g transform="translate({x:g} {y:g})">'
           f'<rect width="{w:g}" height="{PILL_H}" rx="6" fill="{fill}"{stroke}/>'
           f'<path transform="translate({PAD} {(PILL_H - ICON) / 2:g}) scale({s:g})" fill="{fg}" d="{icon["path"]}"/>'
           f'<text x="{PAD + ICON + 7}" y="{PILL_H / 2 + FONT_SIZE * 0.36:g}" fill="{fg}" font-weight="bold" '
           f'textLength="{len(label) * CW:g}">{escape(label)}</text></g>')
    return svg, w


def stack_svg(static: bool) -> str:
    W, label_w, top, row_h = 860, 120, 20, PILL_H + 12
    rows, y = [], top
    for i, (cat, items) in enumerate(STACK):
        x, parts = 22 + label_w, []
        for label, slug in items:
            svg, w = pill(x, 0, label, slug)
            parts.append(svg)
            x += w + GAP
        delay = "" if static else f' style="animation-delay:{i * 0.12:.2f}s"'
        # outer <g> positions the row; the inner one animates (a CSS transform
        # would otherwise replace the transform attribute)
        rows.append(f'<g transform="translate(0 {y})"><g class="row"{delay}>'
                    f'<text x="22" y="{PILL_H / 2 + 4.5:g}" fill="{DIM}" style="font-size:13px">{escape(cat)}</text>'
                    f'{"".join(parts)}</g></g>')
        y += row_h
    H = y - 12 + top
    css = "" if static else (".row { opacity: 0; animation: in .5s ease-out forwards; }"
                             " @keyframes in { from { opacity: 0; transform: translateX(-12px); } to { opacity: 1; } }")
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
        f'aria-label="Tech stack: {escape(", ".join(l for _, items in STACK for l, _ in items))}">',
        f"<style>text {{ font-family: {FONT}; font-size: {FONT_SIZE}px; }} {css}</style>",
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
        *rows, "</svg>"]) + "\n"


def badge_svg(label: str, slug: str) -> str:
    body, w = pill(0, 0, label, slug)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {PILL_H}" width="{w:g}" '
            f'height="{PILL_H}" role="img" aria-label="{escape(label)}">'
            f"<style>text {{ font-family: {FONT}; font-size: {FONT_SIZE}px; }}</style>{body}</svg>\n")


def main() -> None:
    (ROOT / "stack.svg").write_text(stack_svg(static=os.environ.get("STATIC") == "1"))
    out = ROOT / "badges"
    out.mkdir(exist_ok=True)
    for name, label, slug, _ in SOCIALS:
        (out / f"{name}.svg").write_text(badge_svg(label, slug))
    print(f"wrote stack.svg and {len(SOCIALS)} badges in badges/")


if __name__ == "__main__":
    main()
