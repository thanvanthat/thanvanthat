"""Featured-project panel: a terminal window that prints the project's
pipeline step by step, then its highlights and tags (plays once).

    python scripts/make_featured.py             # writes featured.svg
    STATIC=1 python scripts/make_featured.py
"""
import os
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

from config import FEATURED

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "featured.svg"

W, PAD = 860, 28
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
BG, BAR, BORDER, FG, DIM = "#0d1117", "#161b22", "#30363d", "#c9d1d9", "#8b949e"
GREEN, BLUE, ORANGE, PURPLE = "#7ee787", "#79c0ff", "#ffa657", "#d2a8ff"
BODY = 14
CW = BODY * 0.6
STEP = 0.18  # seconds between reveals


def build_svg(static: bool) -> str:
    f = FEATURED
    parts, t = [], 0.0

    def reveal(inner: str, delay: float) -> str:
        style = "" if static else f' style="animation-delay:{delay:.2f}s"'
        return f'<g class="in"{style}>{inner}</g>'

    y = 76
    parts.append(reveal(
        f'<text x="{PAD}" y="{y}" style="font-size:24px" font-weight="bold" fill="{GREEN}">{escape(f["name"])}</text>'
        f'<text x="{PAD}" y="{y + 26}" fill="{DIM}">{escape(f["tagline"])}</text>', t))
    t += STEP

    # pipeline: boxes joined by arrows, lit one after another
    y += 52
    x, sw = PAD, 13 * 0.6
    for i, step in enumerate(f["pipeline"]):
        w = len(step) * sw + 18
        lit = "" if static else (f'<animate attributeName="fill" from="{BAR}" to="#0e4429" begin="{t + 0.1:.2f}s" '
                                 f'dur="0.25s" fill="freeze"/>')
        box = (f'<rect x="{x:g}" y="{y}" width="{w:g}" height="26" rx="5" fill="{BAR if not static else "#0e4429"}" '
               f'stroke="#238636">{lit}</rect>'
               f'<text x="{x + 9:g}" y="{y + 17.5}" fill="{GREEN}" style="font-size:13px" font-weight="bold" '
               f'textLength="{len(step) * sw:g}">{step}</text>')
        if i < len(f["pipeline"]) - 1:
            box += f'<text x="{x + w + 5:g}" y="{y + 18}" fill="{DIM}">→</text>'
        parts.append(reveal(box, t))
        x += w + 24
        t += STEP

    # highlights, wrapped to the panel width
    y += 62
    max_chars = int((W - 2 * PAD - 2 * CW) / CW)
    for b in f["bullets"]:
        lines = textwrap.wrap(b, max_chars)
        inner = "".join(
            f'<text x="{PAD + 2 * CW:g}" y="{y + j * 21}" fill="{FG}">{escape(line)}</text>'
            for j, line in enumerate(lines))
        parts.append(reveal(f'<text x="{PAD}" y="{y}" fill="{ORANGE}">▸</text>{inner}', t))
        y += 21 * len(lines) + 8
        t += STEP

    # tags
    y += 14
    x, tags = PAD, []
    for tag in f["tags"]:
        w = len(tag) * 12 * 0.6 + 16
        if x + w > W - PAD:
            x, y = PAD, y + 30
        tags.append(f'<rect x="{x:g}" y="{y}" width="{w:g}" height="22" rx="11" fill="none" stroke="{PURPLE}"/>'
                    f'<text x="{x + 8:g}" y="{y + 15}" fill="{PURPLE}" style="font-size:12px">{escape(tag)}</text>')
        x += w + 8
    parts.append(reveal("".join(tags), t))
    t += STEP

    y += 48
    links = "  ·  ".join(f"{label}: {url.split('://', 1)[1]}" for label, url in f["links"])
    parts.append(reveal(f'<text x="{PAD}" y="{y}" fill="{BLUE}" style="font-size:12px">{escape(links)}</text>', t))
    H = y + 26

    css = "" if static else (".in { opacity: 0; animation: in .45s ease-out forwards; }"
                             " @keyframes in { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }")
    head = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
        f'aria-label="Featured project: {escape(f["name"])}, {escape(f["tagline"])}">',
        f"<style>text {{ font-family: {FONT}; font-size: {BODY}px; }} {css}</style>",
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{BG}" stroke="{BORDER}"/>',
        f'<path d="M1 13a12 12 0 0 1 12-12h{W - 26}a12 12 0 0 1 12 12v23H1z" fill="{BAR}"/>',
        f'<line x1="1" y1="36" x2="{W - 1}" y2="36" stroke="{BORDER}"/>',
        *(f'<circle cx="{22 + i * 20}" cy="18.5" r="6" fill="{c}"/>'
          for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"])),
        f'<text x="{W / 2:g}" y="24" text-anchor="middle" fill="{DIM}" style="font-size:13px">'
        f'{escape(f["path"])} — README.md</text>',
    ]
    return "\n".join(head + parts + ["</svg>"]) + "\n"


def main() -> None:
    OUT.write_text(build_svg(static=os.environ.get("STATIC") == "1"))
    print(f"wrote {OUT.name}")


if __name__ == "__main__":
    main()
