"""Render data/contributions.json as an animated 53x7 contribution heatmap.

    python scripts/render_heatmap_svg.py        # writes contrib-heatmap.svg
    STATIC=1 python scripts/render_heatmap_svg.py

Without a data file it draws an empty year, so the README never shows a
broken image before the first workflow run.
"""
import json
import os
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "contributions.json"
OUT = ROOT / "contrib-heatmap.svg"

PALETTE = ["#161b22", "#0e4429", "#006d32",
           "#26a641", "#39d353", "#69f0a0"]
#          none -> brightest (level 5 is a neon top end)
CELL, GAP = 13, 3
LEFT, TOP = 34, 30
BG, FG, DIM, BORDER = "#0d1117", "#c9d1d9", "#8b949e", "#30363d"
DIAG_STEP, DUR = 0.025, 0.5  # seconds


def load_days() -> list[dict]:
    if DATA.exists():
        return json.loads(DATA.read_text())["days"]
    end = date.today()
    start = end - timedelta(days=364 + (end.weekday() + 1) % 7)
    return [{"date": (start + timedelta(i)).isoformat(), "count": 0}
            for i in range((end - start).days + 1)]


def assign_levels(days: list[dict]) -> None:
    """Quantile buckets over non-zero days -> levels 1..5, so a single huge
    day doesn't flatten everything else into level 1."""
    nonzero = sorted(d["count"] for d in days if d["count"] > 0)
    cuts = [nonzero[min(len(nonzero) - 1, int(len(nonzero) * q))] for q in (0.25, 0.5, 0.75, 0.95)] if nonzero else []
    for d in days:
        c = d["count"]
        d["lvl"] = 0 if c == 0 else 1 + sum(c > cut for cut in cuts)


def stats(days: list[dict]) -> dict:
    if DATA.exists():
        raw = json.loads(DATA.read_text())
        return {k: raw[k] for k in ("total", "current_streak", "longest_streak", "best_day")}
    return {"total": 0, "current_streak": 0, "longest_streak": 0, "best_day": {"count": 0, "date": ""}}


def build_svg(days: list[dict], st: dict, static: bool) -> str:
    assign_levels(days)
    first = date.fromisoformat(days[0]["date"])
    lead = (first.weekday() + 1) % 7  # GitHub weeks start on Sunday
    weeks = (lead + len(days) + 6) // 7
    grid_w = weeks * (CELL + GAP) - GAP
    grid_h = 7 * (CELL + GAP) - GAP
    W = LEFT + grid_w + 20
    H = TOP + grid_h + 74

    diag = weeks + 6
    css = "" if static else (
        f"\n  .c {{ opacity: 0; transform-box: fill-box; transform-origin: center;"
        f" animation: drop {DUR}s cubic-bezier(.2,.8,.3,1.2) forwards; }}"
        f"\n  @keyframes drop {{ from {{ opacity: 0; transform: translateY(-8px) scale(.6); }}"
        f" to {{ opacity: 1; transform: none; }} }}"
        + "".join(f"\n  .d{i} {{ animation-delay: {i * DIAG_STEP:.3f}s; }}" for i in range(diag))
        + f"\n  .ft {{ opacity: 0; animation: fade .6s ease-out {diag * DIAG_STEP:.2f}s forwards; }}"
        f"\n  @keyframes fade {{ to {{ opacity: 1; }} }}"
    )
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-label="{st["total"]} contributions in the last year">',
        f"<style>{css}\n  text {{ font-family: ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;"
        f" font-size: 11px; fill: {DIM}; }}\n</style>",
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="{BG}" stroke="{BORDER}"/>',
    ]
    for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        out.append(f'<text x="8" y="{TOP + row * (CELL + GAP) + CELL - 2}">{name}</text>')

    last_month = None
    for i, d in enumerate(days):
        slot = lead + i
        wk, dow = divmod(slot, 7)
        x, y = LEFT + wk * (CELL + GAP), TOP + dow * (CELL + GAP)
        dt = date.fromisoformat(d["date"])
        if dow == 0 or i == 0:
            month = dt.strftime("%b")
            if month != last_month and (dt.day <= 7 or i == 0) and wk < weeks - 2:
                out.append(f'<text x="{x}" y="{TOP - 9}">{month}</text>')
                last_month = month
        cls = "c" if static else f"c d{wk + dow}"
        out.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" '
                   f'fill="{PALETTE[d["lvl"]]}"><title>{d["count"]} on {d["date"]}</title></rect>')

    fy = TOP + grid_h + 30
    best = st["best_day"]
    summary = (f'<tspan fill="{FG}" font-weight="bold">{st["total"]:,}</tspan> contributions in the last year'
               f'  ·  streak <tspan fill="{FG}">{st["current_streak"]}d</tspan>'
               f'  ·  longest <tspan fill="{FG}">{st["longest_streak"]}d</tspan>'
               + (f'  ·  best <tspan fill="{FG}">{best["count"]}</tspan> on {best["date"]}' if best["count"] else ""))
    legend_x = LEFT + grid_w - (len(PALETTE) * (CELL + GAP)) - 30
    legend = "".join(f'<rect x="{legend_x + 4 + j * (CELL + GAP)}" y="{fy + 24 - CELL + 2}" width="{CELL}" '
                     f'height="{CELL}" rx="3" fill="{c}"/>' for j, c in enumerate(PALETTE))
    out.append(f'<g class="{"" if static else "ft"}">'
               f'<text x="{LEFT}" y="{fy}">{summary}</text>'
               f'<text x="{legend_x}" y="{fy + 24}" text-anchor="end">Less</text>{legend}'
               f'<text x="{legend_x + 8 + len(PALETTE) * (CELL + GAP)}" y="{fy + 24}">More</text>'
               f'<text x="{LEFT}" y="{fy + 24}" style="font-size:10px">$ updated daily by GitHub Actions</text></g>')
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> None:
    days = load_days()
    OUT.write_text(build_svg(days, stats(days), static=os.environ.get("STATIC") == "1"))
    print(f"wrote {OUT.name} ({len(days)} days{'' if DATA.exists() else ', empty placeholder'})")


if __name__ == "__main__":
    main()
