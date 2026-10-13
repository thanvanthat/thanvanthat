"""One card per project (projects/<repo>.svg) and the README grid that
links each card to its repo, rewritten between the projects markers.

    python scripts/make_projects.py
"""
import re
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

from config import PROJECTS, USERNAME

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "projects"
README = ROOT / "README.md"

W, H, PAD = 420, 168, 20
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
BG, BAR, BORDER, FG, DIM = "#0d1117", "#161b22", "#30363d", "#c9d1d9", "#8b949e"
LANG_COLORS = {  # GitHub linguist colours
    "C#": "#178600", "TypeScript": "#3178c6", "JavaScript": "#f1e05a", "Python": "#3572A5",
    "C++": "#f34b7d", "Unreal Engine": "#8b949e",
}
STATUS = {"play": ("▶ play", "#7ee787"), "live": ("● live", "#7ee787"), "wip": ("◐ wip", "#f2cc60")}


def card_svg(name, repo, lang, desc, tags, live, status) -> str:
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-label="{escape(name)}: {escape(desc)}">',
        # no entrance animation: cards sit low on the page, and a renderer
        # that doesn't animate offscreen images would show them blank
        f"<style>text {{ font-family: {FONT}; font-size: 12px; }}</style>",
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
        # folder glyph + name
        f'<path transform="translate({PAD} 18)" fill="{DIM}" d="M0 2a2 2 0 0 1 2-2h4l2 2h6a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2z"/>',
        f'<text x="{PAD + 24}" y="30" fill="#79c0ff" font-weight="bold" style="font-size:15px">{escape(name)}</text>',
    ]
    if status:
        label, color = STATUS[status]
        out.append(f'<text x="{W - PAD}" y="30" text-anchor="end" fill="{color}">{escape(label)}</text>')
    for i, line in enumerate(textwrap.wrap(desc, int((W - 2 * PAD) / 7.2))[:4]):
        out.append(f'<text x="{PAD}" y="{56 + i * 18}" fill="{FG}">{escape(line)}</text>')
    # footer: language dot, then tags
    y = H - 20
    out.append(f'<circle cx="{PAD + 5}" cy="{y - 4}" r="5" fill="{LANG_COLORS.get(lang, DIM)}"/>'
               f'<text x="{PAD + 16}" y="{y}" fill="{DIM}">{escape(lang)}</text>')
    x = PAD + 16 + len(lang) * 7.2 + 14
    for tag in tags:
        if tag == lang:
            continue
        w = len(tag) * 6.6 + 14
        if x + w > W - PAD:
            break
        out.append(f'<rect x="{x:g}" y="{y - 14}" width="{w:g}" height="19" rx="9.5" fill="{BAR}" stroke="{BORDER}"/>'
                   f'<text x="{x + 7:g}" y="{y - 0.5}" fill="#d2a8ff" style="font-size:11px">{escape(tag)}</text>')
        x += w + 6
    out.append("</svg>")
    return "\n".join(out) + "\n"


def readme_block() -> str:
    cells = []
    for name, repo, lang, desc, tags, live, status in PROJECTS:
        url = f"https://github.com/{USERNAME}/{repo}"
        links = f'<a href="{url}">Repo</a>'
        if live:
            links = f'<a href="{live}">{"Play" if status == "play" else "Live"}</a> · ' + links
        cells.append(f'    <td valign="top"><a href="{url}"><img src="./projects/{repo}.svg" width="420" '
                     f'alt="{escape(name)}" /></a><br><sub>{links}</sub></td>')
    rows = ["  <tr>\n" + "\n".join(cells[i:i + 2]) + "\n  </tr>" for i in range(0, len(cells), 2)]
    return "<table>\n" + "\n".join(rows) + "\n</table>"


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    for p in PROJECTS:
        (OUT_DIR / f"{p[1]}.svg").write_text(card_svg(*p))
    text = README.read_text()
    new, n = re.subn(r"(<!-- projects:start -->\n)(?:.*?\n)?(<!-- projects:end -->)",
                     lambda m: m.group(1) + readme_block() + "\n" + m.group(2), text, flags=re.S)
    if n != 1:
        raise SystemExit("README.md needs one <!-- projects:start --> ... <!-- projects:end --> block")
    README.write_text(new)
    print(f"wrote {len(PROJECTS)} cards in projects/ and the README grid")


if __name__ == "__main__":
    main()
