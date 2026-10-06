"""Scrape the public contribution calendar (no token needed) and write
data/contributions.json with raw days plus derived stats.

    python scripts/fetch_contributions.py [username]
"""
import json
import re
import sys
from collections import OrderedDict
from datetime import date, datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from config import USERNAME

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "contributions.json"
URL = "https://github.com/users/{}/contributions"


def parse_days(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    # Counts live in <tool-tip for="cell-id">N contributions on ...</tool-tip>.
    tips = {}
    for tip in soup.find_all("tool-tip"):
        m = re.match(r"\s*(No|[\d,]+) contributions?", tip.get_text())
        if m and tip.get("for"):
            tips[tip["for"]] = 0 if m.group(1) == "No" else int(m.group(1).replace(",", ""))
    days = []
    for cell in soup.select("td.ContributionCalendar-day[data-date]"):
        days.append({
            "date": cell["data-date"],
            "count": tips.get(cell.get("id"), 0),
            "level": int(cell.get("data-level", 0)),
        })
    days.sort(key=lambda d: d["date"])
    return days


def streaks(days: list[dict]) -> tuple[int, int]:
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] > 0 else 0
        longest = max(longest, run)
    # The current streak survives an empty *today* (the day isn't over yet).
    current, tail = 0, list(days)
    if tail and tail[-1]["count"] == 0 and tail[-1]["date"] == date.today().isoformat():
        tail.pop()
    for d in reversed(tail):
        if d["count"] == 0:
            break
        current += 1
    return current, longest


def main() -> None:
    user = sys.argv[1] if len(sys.argv) > 1 else USERNAME
    resp = requests.get(URL.format(user), timeout=30,
                        headers={"User-Agent": "profile-art-bot (+https://github.com)"})
    resp.raise_for_status()
    days = parse_days(resp.text)
    if not days:
        sys.exit("no contribution cells found — has GitHub changed the markup?")

    monthly: "OrderedDict[str, int]" = OrderedDict()
    for d in days:
        monthly[d["date"][:7]] = monthly.get(d["date"][:7], 0) + d["count"]
    best = max(days, key=lambda d: d["count"])
    current, longest = streaks(days)
    data = {
        "username": user,
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total": sum(d["count"] for d in days),
        "current_streak": current,
        "longest_streak": longest,
        "best_day": {"date": best["date"], "count": best["count"]},
        "monthly": monthly,
        "days": days,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1) + "\n")
    print(f"wrote {OUT.relative_to(ROOT)}: {data['total']} contributions over {len(days)} days")


if __name__ == "__main__":
    main()
