"""A terminal prompt that types each HEADLINE line, erases it, and moves on
to the next, looping forever (SMIL, discrete keyframes per character).

    python scripts/make_headline.py             # writes headline.svg
    STATIC=1 python scripts/make_headline.py    # first line, frozen
"""
import os
from pathlib import Path
from xml.sax.saxutils import escape

from config import HANDLE, HEADLINE

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "headline.svg"

W, H = 860, 64
FONT_SIZE = 22
CW = FONT_SIZE * 0.6            # monospace advance; textLength pins it
PAD_X, BASE_Y = 22, 40
BG, BORDER, FG, GREEN, BLUE = "#0d1117", "#30363d", "#c9d1d9", "#7ee787", "#79c0ff"
TYPE, HOLD, ERASE, GAP = 0.07, 1.8, 0.03, 0.4   # seconds (per char for TYPE/ERASE)


def timeline() -> tuple[float, list[list[tuple[float, int]]]]:
    """Per line: [(time, visible chars), ...] keyframes over one full cycle."""
    t, frames = 0.0, []
    for line in HEADLINE:
        n = len(line)
        f = [(t + i * TYPE, i) for i in range(n + 1)]
        t += n * TYPE + HOLD
        f += [(t + i * ERASE, n - i) for i in range(n + 1)]
        t += n * ERASE + GAP
        frames.append(f)
    return t, frames


def keyframes(points: list[tuple[float, float]], total: float) -> tuple[str, str]:
    pts = [(0.0, points[0][1])] if points[0][0] > 0 else []
    pts += points
    if pts[-1][0] < total:
        pts.append((total, pts[-1][1]))
    times = ";".join(f"{min(p[0] / total, 1):.5f}" for p in pts)
    return times, ";".join(f"{p[1]:g}" for p in pts)


def build_svg(static: bool) -> str:
    prompt = f"{HANDLE}:~$ "
    x0 = PAD_X + len(prompt) * CW
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-label="{escape(" / ".join(HEADLINE))}">',
        f"<style>text {{ font-family: ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size: {FONT_SIZE}px; }}</style>",
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
        # trailing space is dropped from the text (SVG collapses it); x0 keeps the gap
        f'<text x="{PAD_X}" y="{BASE_Y}" fill="{GREEN}" textLength="{len(prompt.rstrip()) * CW:g}">{escape(prompt.rstrip())}</text>',
    ]
    total, frames = timeline()
    if static:
        line = HEADLINE[0]
        out.append(f'<text x="{x0:g}" y="{BASE_Y}" fill="{BLUE}" font-weight="bold" '
                   f'textLength="{len(line) * CW:g}">{escape(line)}</text>')
        out.append(f'<rect x="{x0 + len(line) * CW:g}" y="{BASE_Y - FONT_SIZE + 4}" width="{CW * 0.6:g}" '
                   f'height="{FONT_SIZE}" fill="{FG}"/>')
    else:
        cursor = []
        for i, (line, f) in enumerate(zip(HEADLINE, frames)):
            kt, vals = keyframes([(t, n * CW) for t, n in f], total)
            out += [
                f'<clipPath id="h{i}"><rect x="{x0:g}" y="0" width="0" height="{H}">'
                f'<animate attributeName="width" calcMode="discrete" dur="{total:.2f}s" repeatCount="indefinite" '
                f'keyTimes="{kt}" values="{vals}"/></rect></clipPath>',
                f'<text x="{x0:g}" y="{BASE_Y}" fill="{BLUE}" font-weight="bold" clip-path="url(#h{i})" '
                f'textLength="{len(line) * CW:g}">{escape(line)}</text>',
            ]
            cursor += [(t, x0 + n * CW) for t, n in f]
        kt, vals = keyframes(cursor, total)
        out.append(
            f'<rect x="{x0:g}" y="{BASE_Y - FONT_SIZE + 4}" width="{CW * 0.6:g}" height="{FONT_SIZE}" fill="{FG}">'
            f'<animate attributeName="x" calcMode="discrete" dur="{total:.2f}s" repeatCount="indefinite" '
            f'keyTimes="{kt}" values="{vals}"/>'
            f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" repeatCount="indefinite"/>'
            f"</rect>")
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> None:
    OUT.write_text(build_svg(static=os.environ.get("STATIC") == "1"))
    print(f"wrote {OUT.name}")


if __name__ == "__main__":
    main()
