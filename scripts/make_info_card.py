"""Hand-author a neofetch-style info card that prints line by line.

    python scripts/make_info_card.py            # writes info-card.svg
    STATIC=1 python scripts/make_info_card.py   # frozen frame for previews
"""
import os
from pathlib import Path
from xml.sax.saxutils import escape

from config import HANDLE, INFO_ROWS

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "info-card.svg"

W = 660
PAD_X, TOP, LINE_H = 28, 78, 30
BG, BORDER, FG, DIM = "#0d1117", "#30363d", "#c9d1d9", "#8b949e"
KEY_COLORS = ["#ff7b72", "#ffa657", "#d2a8ff", "#79c0ff", "#7ee787", "#f2cc60"]
SWATCHES = ["#ff7b72", "#ffa657", "#f2cc60", "#7ee787", "#79c0ff", "#d2a8ff", "#c9d1d9"]
STEP, DUR = 0.12, 0.45  # seconds


def build_svg(static: bool) -> str:
    n = len(INFO_ROWS)
    body_bottom = TOP + (n + 1) * LINE_H
    H = body_bottom + 56
    css = "" if static else f"""
  .ln {{ opacity: 0; animation: in {DUR}s ease-out forwards; }}
  @keyframes in {{ from {{ opacity: 0; transform: translateX(-10px); }} to {{ opacity: 1; transform: none; }} }}"""
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-label="{escape(HANDLE)} info card">',
        f"<style>{css}\n  text {{ font-family: ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size: 17px; }}\n</style>",
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="{BG}" stroke="{BORDER}"/>',
        # title bar
        f'<path d="M1 13a12 12 0 0 1 12-12h{W - 26}a12 12 0 0 1 12 12v23H1z" fill="#161b22"/>',
        f'<line x1="1" y1="36" x2="{W - 1}" y2="36" stroke="{BORDER}"/>',
        *(f'<circle cx="{22 + i * 20}" cy="18.5" r="6" fill="{c}"/>'
          for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"])),
        f'<text x="{W / 2:g}" y="24" text-anchor="middle" fill="{DIM}" style="font-size:14px">'
        f'{escape(HANDLE)} — neofetch</text>',
    ]

    def line(i: int, inner: str) -> None:
        delay = "" if static else f' style="animation-delay:{i * STEP:.2f}s"'
        out.append(f'<g class="ln"{delay}>{inner}</g>')

    user, _, host = HANDLE.partition("@")
    line(0, f'<text x="{PAD_X}" y="{TOP - 10}"><tspan fill="#7ee787" font-weight="bold">{escape(user)}</tspan>'
            f'<tspan fill="{FG}">@</tspan><tspan fill="#7ee787" font-weight="bold">{escape(host)}</tspan></text>'
            f'<text x="{PAD_X}" y="{TOP + 8}" fill="{DIM}">{"-" * len(HANDLE)}</text>')
    color_i = 0
    for i, (key, val) in enumerate(INFO_ROWS, start=1):
        if not key and not val:
            continue
        y = TOP + 8 + i * LINE_H
        if key:
            color = KEY_COLORS[color_i % len(KEY_COLORS)]
            color_i += 1
        k = f'<tspan fill="{color}" font-weight="bold">{escape(key)}</tspan><tspan fill="{DIM}">:</tspan>' if key else ""
        line(i, f'<text x="{PAD_X}" y="{y}">{k}</text>'
                f'<text x="{PAD_X + 92}" y="{y}" fill="{FG}">{escape(val)}</text>')
    sw = "".join(f'<rect x="{PAD_X + j * 34}" y="{body_bottom + 4}" width="30" height="16" rx="3" fill="{c}"/>'
                 for j, c in enumerate(SWATCHES))
    line(n + 1, sw)
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> None:
    OUT.write_text(build_svg(static=os.environ.get("STATIC") == "1"))
    print(f"wrote {OUT.name}")


if __name__ == "__main__":
    main()
