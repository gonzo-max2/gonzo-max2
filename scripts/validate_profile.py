#!/usr/bin/env python3
"""Validate the profile package without third-party dependencies."""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

def main() -> int:
    failures: list[str] = []
    text = README.read_text(encoding="utf-8")

    if len(text) < 2000:
        failures.append("README.md is unexpectedly short")
    if "ghp_" in text or "github_pat_" in text:
        failures.append("README.md contains a token-shaped secret")
    if "<script" in text.lower():
        failures.append("README.md contains a script tag")

    refs = re.findall(r'(?:src|srcset)="(\./[^"]+)"', text)
    for ref in refs:
        target = ROOT / ref.removeprefix("./")
        if not target.is_file():
            failures.append(f"missing referenced asset: {ref}")

    expected = {
        "assets/hero-dark.svg",
        "assets/hero-light.svg",
        "assets/maya-system-dark.svg",
        "assets/maya-system-light.svg",
        "assets/activity-dark.svg",
        "assets/activity-light.svg",
        "assets/continuum-divider.svg",
    }
    for rel in expected:
        if not (ROOT / rel).is_file():
            failures.append(f"missing required file: {rel}")

    for svg in (ROOT / "assets").glob("*.svg"):
        svg_text = svg.read_text(encoding="utf-8")
        if not svg_text.lstrip().startswith("<svg"):
            failures.append(f"invalid SVG root: {svg.relative_to(ROOT)}")
        if "<script" in svg_text.lower():
            failures.append(f"script tag in SVG: {svg.relative_to(ROOT)}")

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1

    print(f"Profile validation passed: {len(refs)} README asset references")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
