#!/usr/bin/env python3
"""Generate self-contained GitHub contribution SVGs for a profile README."""

from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request
from typing import Any, Final

API_URL: Final = "https://api.github.com/graphql"
OWNER: Final = os.environ.get("PROFILE_OWNER") or os.environ.get("GITHUB_REPOSITORY_OWNER", "gonzo-max2")
TOKEN: Final = os.environ.get("GITHUB_TOKEN", "")
OUTPUT_DIR: Final = Path(os.environ.get("PROFILE_ASSET_DIR", "assets"))

QUERY: Final = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    name
    login
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            color
          }
        }
      }
    }
  }
}
"""

def graphql(query: str, variables: dict[str, Any]) -> dict[str, Any]:
    if not TOKEN:
        raise RuntimeError("GITHUB_TOKEN is required")

    request = urllib.request.Request(
        API_URL,
        data=json.dumps({"query": query, "variables": variables}).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "gonzo-max2-profile-metrics",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub GraphQL HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"GitHub GraphQL connection failed: {exc.reason}") from exc

    if payload.get("errors"):
        raise RuntimeError(f"GitHub GraphQL errors: {payload['errors']}")
    return payload["data"]

def calculate_streaks(days: list[dict[str, Any]], today: dt.date) -> tuple[int, int, int]:
    counts = {dt.date.fromisoformat(day["date"]): int(day["contributionCount"]) for day in days}
    active_days = sum(1 for count in counts.values() if count > 0)

    longest = 0
    run = 0
    for date in sorted(counts):
        if counts[date] > 0:
            run += 1
            longest = max(longest, run)
        else:
            run = 0

    current = 0
    cursor = today
    if counts.get(cursor, 0) == 0:
        cursor -= dt.timedelta(days=1)
    while counts.get(cursor, 0) > 0:
        current += 1
        cursor -= dt.timedelta(days=1)

    return active_days, longest, current

def level_for(count: int) -> int:
    if count <= 0:
        return 0
    if count <= 2:
        return 1
    if count <= 5:
        return 2
    if count <= 9:
        return 3
    return 4

def xml_escape(value: object) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )

def render(
    *,
    dark: bool,
    owner: str,
    total: int,
    commits: int,
    prs: int,
    reviews: int,
    issues: int,
    active_days: int,
    longest_streak: int,
    current_streak: int,
    days: list[dict[str, Any]],
    updated: str,
) -> str:
    palette = {
        "bg": "#0B1015" if dark else "#FFFFFF",
        "surface": "#111A22" if dark else "#F1F5F8",
        "border": "#26333E" if dark else "#C9D3DC",
        "text": "#F4F7FA" if dark else "#141A22",
        "muted": "#96A4B2" if dark else "#607080",
        "accent": "#2AD7B5" if dark else "#087C6B",
        "levels": (
            ["#172028", "#15372F", "#16614F", "#1A9A7C", "#2AD7B5"]
            if dark
            else ["#E5ECEF", "#C9E8E0", "#8FD2C1", "#42A58F", "#087C6B"]
        ),
    }

    by_date = {day["date"]: int(day["contributionCount"]) for day in days}
    end = dt.date.fromisoformat(max(by_date)) if by_date else dt.date.today()
    start = end - dt.timedelta(days=370)
    start -= dt.timedelta(days=(start.weekday() + 1) % 7)

    cells: list[str] = []
    cursor = start
    for week in range(53):
        for row in range(7):
            date = cursor + dt.timedelta(days=week * 7 + row)
            count = by_date.get(date.isoformat(), 0)
            fill = palette["levels"][level_for(count)]
            x = 56 + week * 20
            y = 192 + row * 20
            cells.append(
                f'<rect x="{x}" y="{y}" width="13" height="13" rx="3" '
                f'fill="{fill}"><title>{xml_escape(date)} · {count} contributions</title></rect>'
            )

    stat_data = [
        ("TOTAL", total),
        ("ACTIVE DAYS", active_days),
        ("CURRENT STREAK", current_streak),
        ("LONGEST STREAK", longest_streak),
    ]
    stat_nodes: list[str] = []
    for index, (label, value) in enumerate(stat_data):
        x = 56 + index * 270
        stat_nodes.append(
            f'<g transform="translate({x} 112)">'
            f'<text x="0" y="0" fill="{palette["muted"]}" font-family="ui-monospace, SFMono-Regular, Consolas, monospace" font-size="10" letter-spacing="1.4">{label}</text>'
            f'<text x="0" y="30" fill="{palette["text"]}" font-family="Inter, ui-sans-serif, system-ui, sans-serif" font-size="24" font-weight="700">{value}</text>'
            f'</g>'
        )

    detail = f"{commits} commits · {prs} pull requests · {reviews} reviews · {issues} issues"

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="380" viewBox="0 0 1200 380" role="img" aria-labelledby="title desc">
  <title id="title">GitHub engineering activity for {xml_escape(owner)}</title>
  <desc id="desc">{total} public contributions in the last year.</desc>
  <rect width="1200" height="380" rx="16" fill="{palette["bg"]}"/>
  <rect x="1" y="1" width="1198" height="378" rx="15" fill="none" stroke="{palette["border"]}"/>
  <text x="56" y="55" fill="{palette["muted"]}" font-family="ui-monospace, SFMono-Regular, Consolas, monospace" font-size="11" letter-spacing="2">ENGINEERING ACTIVITY · LAST 12 MONTHS</text>
  <text x="56" y="88" fill="{palette["text"]}" font-family="Inter, ui-sans-serif, system-ui, sans-serif" font-size="18" font-weight="650">{xml_escape(detail)}</text>
  {''.join(stat_nodes)}
  {''.join(cells)}
  <circle cx="56" cy="352" r="5" fill="{palette["accent"]}"/>
  <text x="72" y="356" fill="{palette["muted"]}" font-family="Inter, ui-sans-serif, system-ui, sans-serif" font-size="11">Verified refresh {xml_escape(updated)} UTC · repository-owned generator</text>
</svg>
"""

def main() -> int:
    today = dt.datetime.now(dt.timezone.utc)
    start = today - dt.timedelta(days=371)
    data = graphql(
        QUERY,
        {
            "login": OWNER,
            "from": start.isoformat().replace("+00:00", "Z"),
            "to": today.isoformat().replace("+00:00", "Z"),
        },
    )
    user = data.get("user")
    if not user:
        raise RuntimeError(f"GitHub user not found: {OWNER}")

    collection = user["contributionsCollection"]
    calendar = collection["contributionCalendar"]
    days = [
        day
        for week in calendar["weeks"]
        for day in week["contributionDays"]
    ]
    active_days, longest, current = calculate_streaks(days, today.date())
    updated = today.strftime("%Y-%m-%d %H:%M")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    common = {
        "owner": user["login"],
        "total": int(calendar["totalContributions"]),
        "commits": int(collection["totalCommitContributions"]),
        "prs": int(collection["totalPullRequestContributions"]),
        "reviews": int(collection["totalPullRequestReviewContributions"]),
        "issues": int(collection["totalIssueContributions"]),
        "active_days": active_days,
        "longest_streak": longest,
        "current_streak": current,
        "days": days,
        "updated": updated,
    }

    (OUTPUT_DIR / "activity-dark.svg").write_text(render(dark=True, **common), encoding="utf-8")
    (OUTPUT_DIR / "activity-light.svg").write_text(render(dark=False, **common), encoding="utf-8")
    print(json.dumps({"owner": OWNER, "total": common["total"], "updated": updated}))
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"profile metrics failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
