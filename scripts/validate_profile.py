#!/usr/bin/env python3
"""Validate GitHub-native profile README and all referenced local assets."""
from __future__ import annotations
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / 'README.md'
TOKEN_PATTERNS = [
    re.compile(r'ghp_[A-Za-z0-9]{20,}'),
    re.compile(r'github_pat_[A-Za-z0-9_]{20,}'),
    re.compile(r'sk-[A-Za-z0-9]{20,}'),
]
REQUIRED_APEX = {
    'assets/apex/hero-dark.svg', 'assets/apex/hero-light.svg',
    'assets/apex/maya-dark.svg', 'assets/apex/maya-light.svg',
    'assets/apex/systems-dark.svg', 'assets/apex/systems-light.svg',
    'assets/apex/vozime-dark.svg', 'assets/apex/vozime-light.svg',
    'assets/apex/ledger-dark.svg', 'assets/apex/ledger-light.svg',
    'assets/apex/capabilities-dark.svg', 'assets/apex/capabilities-light.svg',
    'assets/activity-dark.svg', 'assets/activity-light.svg',
    'assets/continuum-divider.svg',
}


def main() -> int:
    errors: list[str] = []
    text = README.read_text(encoding='utf-8')
    if len(text) < 3500:
        errors.append('README.md is unexpectedly short')
    if '<script' in text.lower():
        errors.append('README.md contains a script tag')
    for pattern in TOKEN_PATTERNS:
        if pattern.search(text):
            errors.append('README.md contains a credential-shaped secret')

    refs = re.findall(r'(?:src|srcset)="(\./[^"]+)"', text)
    for ref in refs:
        target = ROOT / ref.removeprefix('./')
        if not target.is_file():
            errors.append(f'missing referenced asset: {ref}')
    for rel in REQUIRED_APEX:
        if not (ROOT / rel).is_file():
            errors.append(f'missing required APEX file: {rel}')

    for svg in (ROOT / 'assets').rglob('*.svg'):
        try:
            root = ET.parse(svg).getroot()
        except ET.ParseError as exc:
            errors.append(f'invalid SVG {svg.relative_to(ROOT)}: {exc}')
            continue
        children = list(root)
        if not any(node.tag.endswith('title') for node in children):
            errors.append(f'SVG lacks title: {svg.relative_to(ROOT)}')
        if not any(node.tag.endswith('desc') for node in children):
            errors.append(f'SVG lacks desc: {svg.relative_to(ROOT)}')
        svg_text = svg.read_text(encoding='utf-8')
        if '<script' in svg_text.lower():
            errors.append(f'script tag in SVG: {svg.relative_to(ROOT)}')

    if errors:
        for error in errors:
            print(f'ERROR: {error}', file=sys.stderr)
        return 1
    print(f'Profile validation passed: {len(refs)} README asset references, {len(REQUIRED_APEX)} required assets')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
