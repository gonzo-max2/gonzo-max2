#!/usr/bin/env python3
"""Fail-closed structural, security, and interaction verification for APEX Profile OS."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'README.md', 'content/profile.json', 'docs/index.html', 'docs/styles.css', 'docs/app.js',
    'docs/data/profile.json', 'docs/site.webmanifest', 'docs/sw.js', 'docs/assets/apex-social.svg',
    'PROFILE_OS_ARCHITECTURE.md', 'DEPLOYMENT.md', 'scripts/build_apex_assets.py',
    'assets/apex/hero-dark.svg', 'assets/apex/hero-light.svg',
    'assets/apex/maya-dark.svg', 'assets/apex/maya-light.svg',
    'assets/apex/systems-dark.svg', 'assets/apex/systems-light.svg',
    'assets/apex/vozime-dark.svg', 'assets/apex/vozime-light.svg',
    'assets/apex/ledger-dark.svg', 'assets/apex/ledger-light.svg',
    'assets/apex/capabilities-dark.svg', 'assets/apex/capabilities-light.svg',
]
TOKEN_PATTERNS = [
    re.compile(r'ghp_[A-Za-z0-9]{20,}'),
    re.compile(r'github_pat_[A-Za-z0-9_]{20,}'),
    re.compile(r'sk-[A-Za-z0-9]{20,}'),
]


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f'missing required file: {rel}')

    profile = json.loads((ROOT / 'content' / 'profile.json').read_text(encoding='utf-8'))
    if len(profile.get('systems', [])) != 9:
        errors.append('profile must contain exactly nine systems')
    if not any(item.get('id') == 'blockchain' for item in profile.get('systems', [])):
        errors.append('blockchain system missing')
    if not any(item.get('id') == 'vozime' for item in profile.get('systems', [])):
        errors.append('Vozime system missing')

    for path in ROOT.rglob('*'):
        if not path.is_file() or '.git' in path.parts or path.suffix in {'.zip', '.png'}:
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        for pattern in TOKEN_PATTERNS:
            if pattern.search(text):
                errors.append(f'credential-shaped secret in {path.relative_to(ROOT)}')

    for svg in (ROOT / 'assets' / 'apex').glob('*.svg'):
        try:
            root = ET.parse(svg).getroot()
        except ET.ParseError as exc:
            errors.append(f'invalid APEX SVG {svg.name}: {exc}')
            continue
        children = list(root)
        if not any(node.tag.endswith('title') for node in children) or not any(node.tag.endswith('desc') for node in children):
            errors.append(f'APEX SVG lacks title/desc: {svg.name}')

    html = (ROOT / 'docs' / 'index.html').read_text(encoding='utf-8')
    css = (ROOT / 'docs' / 'styles.css').read_text(encoding='utf-8')
    js = (ROOT / 'docs' / 'app.js').read_text(encoding='utf-8')
    if 'https://cdn.' in html or '<script src="http' in html or '<link rel="stylesheet" href="http' in html:
        errors.append('Pages site contains an external runtime dependency')
    for landmark in ['id="main"', 'class="skip-link"', 'aria-label="Primary navigation"']:
        if landmark not in html:
            errors.append(f'missing accessibility landmark: {landmark}')
    for feature in ['prefers-reduced-motion', 'forced-colors', 'data-motion="off"']:
        if feature not in css:
            errors.append(f'CSS feature missing: {feature}')
    for feature in ['crypto.subtle.digest', 'sha256Fallback', 'requestAnimationFrame', 'visibilitychange', 'IntersectionObserver', 'ResizeObserver']:
        if feature not in js:
            errors.append(f'advanced runtime feature missing: {feature}')
    for feature in ['buildLedger', 'buildMerkle', 'tamperLedger', 'repairLedger']:
        if feature not in js:
            errors.append(f'blockchain interaction missing: {feature}')

    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    refs = re.findall(r'(?:src|srcset)="(\./[^"]+)"', readme)
    for ref in refs:
        if not (ROOT / ref.removeprefix('./')).is_file():
            errors.append(f'missing README asset: {ref}')

    receipt = {
        'schema': 'gonzo-profile-apex-verification/v1',
        'passed': not errors,
        'systems': len(profile.get('systems', [])),
        'readme_asset_references': len(refs),
        'apex_svg_assets': len(list((ROOT / 'assets' / 'apex').glob('*.svg'))),
        'external_runtime_dependencies': 0,
        'errors': errors,
        'sha256': {},
    }
    for rel in REQUIRED:
        path = ROOT / rel
        if path.is_file():
            receipt['sha256'][rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    (ROOT / 'receipts').mkdir(exist_ok=True)
    (ROOT / 'receipts' / 'security-and-structure.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')

    if errors:
        for error in errors:
            print(f'ERROR: {error}', file=sys.stderr)
        return 1
    print(json.dumps({'passed': True, 'systems': receipt['systems'], 'assets': receipt['readme_asset_references'], 'apex_svg_assets': receipt['apex_svg_assets']}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
